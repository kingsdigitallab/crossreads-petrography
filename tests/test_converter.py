import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from crossreads_petrography import *
from unittest.mock import patch, PropertyMock, MagicMock, mock_open
import pandas as pd
import os
import numpy as np
import plotnine as p9
from datetime import datetime
from crossreads_petrography.isotopes import plot_curves, determine_polygon_intersections


class TestConverterBase:
    @property
    def converter_class(self):
        pass

    @property
    def expected_output_files(self):
        pass

    @pytest.fixture
    def converter(self):
        return self.converter_class()

    def test_init(self, converter):
        assert isinstance(converter, CrossreadsPetrographyTool)
        assert converter.name is not None

    def test_output_path_now(self, converter):
        with patch("crossreads_petrography.tools.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 5, 1)
            expected_path = os.path.join(converter.paths["output"], "2023-05-01")
            assert converter.output_path_now == expected_path

    def test_run(self, converter):
        with patch.object(self.converter_class, "save") as mock_save:
            converter.run()
            mock_save.assert_called_once()

    @patch("pandas.DataFrame.to_excel")
    def test_save(self, mock_to_excel, converter, tmp_path):
        converter.paths["output"] = str(tmp_path)

        # Mock the DataFrame.to_excel method to create an empty file
        def to_excel_side_effect(filename, *args, **kwargs):
            file_path = Path(filename)
            file_path.parent.mkdir(
                parents=True, exist_ok=True
            )  # Create parent directories
            file_path.touch()  # Create an empty file

        mock_to_excel.side_effect = to_excel_side_effect

        converter.save()
        expected_dir = tmp_path / datetime.now().strftime("%Y-%m-%d")
        for expected_file in self.expected_output_files:
            expected_path = expected_dir / expected_file
            assert expected_path.exists(), (
                f"{expected_file} not found in {expected_dir}"
            )

        assert mock_to_excel.call_count == len(self.expected_output_files)
        assert Path(mock_to_excel.call_args[0][0]).samefile(expected_path), (
            f"Expected file {expected_file} was not created"
        )


TestConverterBase.__test__ = False


@pytest.mark.usefixtures("converter")
class TestMgsConverter(TestConverterBase):
    converter_class = MgsConverter
    expected_output_files = ["mgs_intersections.xlsx"]

    @patch("crossreads_petrography.mgs.read_path")
    def test_df_input(self, mock_read_path, converter):
        mock_df = pd.DataFrame(
            {
                "subtype": ["Goktepe", "Docimian", "Penteli"],
                "value_type": ["min wh", "max wh", "min box"],
                "value_mm": [1.0, 2.0, 1.5],
            }
        )
        mock_read_path.return_value = mock_df

        result = converter.df_input

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert "subtype" in result.columns
        assert "value_type" in result.columns
        assert "value_mm" in result.columns

    @patch(
        "crossreads_petrography.mgs.MgsConverter.df_input", new_callable=PropertyMock
    )
    @patch("crossreads_petrography.mgs.read_metadata")
    def test_df_output(self, mock_read_metadata, mock_df_input, converter):
        mock_df_input.return_value = pd.DataFrame(
            {
                "subtype": ["Carrara"] * 5,
                "value_type": ["min wh", "min box", "median", "max box", "max wh"],
                "value_mm": [0.28, 0.49, 0.71, 1.01, 1.37],
            }
        )

        mock_metadata = pd.DataFrame(
            {
                "optical microscopy MGS (mm)": [1.2, 1.8, 2.2, 2.5, 3.0],
                "digital microscopy MGS (mm)": [1.3, 1.9, 2.3, 2.6, 3.1],
            },
            index=["ISic001", "ISic002", "ISic003", "ISic004", "ISic005"],
        )
        mock_read_metadata.return_value = mock_metadata

        result = converter.df_output

        assert isinstance(result, pd.DataFrame)
        assert "Carrara" in result.columns
        assert "ISic001" in result.index


@pytest.mark.usefixtures("converter")
class TestPXRFConverter(TestConverterBase):
    converter_class = PXRFConverter
    expected_output_files = [
        "pXRF_calculated_fractions_mean.xlsx",
        "pXRF_calculated_fractions_std.xlsx",
    ]

    @patch("crossreads_petrography.pxrf.read_path")
    def test_df_standards(self, mock_read_path, converter):
        mock_df = pd.DataFrame(
            {
                "standard": [
                    "100CC",
                    "90CC",
                    "80CC",
                    "70CC",
                    "60CC",
                    "50CC",
                    "40CC",
                    "30CC",
                    "20CC",
                    "10CC",
                    "0CC",
                ],
                "SiO2": [
                    0.00,
                    11.57,
                    21.53,
                    27.17,
                    32.97,
                    55.45,
                    64.45,
                    73.80,
                    78.82,
                    84.72,
                    91.04,
                ],
                "K2O": [
                    0.00,
                    0.76,
                    1.42,
                    1.79,
                    2.15,
                    3.66,
                    4.22,
                    4.87,
                    5.32,
                    5.59,
                    6.00,
                ],
                "CaO": [
                    99.87,
                    87.37,
                    76.59,
                    70.49,
                    64.64,
                    39.80,
                    30.01,
                    19.82,
                    14.34,
                    7.88,
                    0.00,
                ],
                "Fe2O3": [
                    0.13,
                    0.30,
                    0.46,
                    0.55,
                    0.64,
                    1.09,
                    1.29,
                    1.52,
                    1.65,
                    1.81,
                    2.00,
                ],
            }
        )
        mock_read_path.return_value = mock_df

        result = converter.df_standards

        assert isinstance(result, pd.DataFrame)
        assert len(result.columns) == 11
        assert list(result.index) == ["SiO2", "K2O", "CaO", "Fe2O3"]
        assert list(result.columns) == [
            "0CC",
            "10CC",
            "20CC",
            "30CC",
            "40CC",
            "50CC",
            "60CC",
            "70CC",
            "80CC",
            "90CC",
            "100CC",
        ]
        assert result.loc["SiO2", "50CC"] == pytest.approx(55.45)
        assert result.loc["CaO", "100CC"] == pytest.approx(99.87)

    @patch("crossreads_petrography.pxrf.read_path")
    def test_df_descriptions(self, mock_read_path, converter):
        mock_df = pd.DataFrame(
            {
                "Isic": ["CU", "marpo", "demo-MK.317"],
                "site": ["CU", "marpo", "taormina"],
                "day": ["16", "", "22"],
                "month": ["2", "10", "1"],
                "year": ["2022", "2022", "2024"],
                "cass": ["epicum 3", "mag B", ""],
                "inv/id": ["a", "74355", "torso"],
                "a": ["", "short edge, corner", "under right armpit"],
                "b": ["", "long edge, corner", "left shoulder"],
                "c": ["", "back", "right shoulder"],
            }
        )
        mock_read_path.return_value = mock_df

        result = converter.df_descriptions.reset_index()

        assert isinstance(result, pd.DataFrame)
        assert "Isic" in result.columns
        assert "a" in result.columns
        assert "b" in result.columns

    @patch("crossreads_petrography.pxrf.read_path")
    def test_txt_input(self, mock_read_path, converter):
        mock_txt = [
            (
                "file1.csv",
                "SOURCE: 0-1.csv\nKEY: 1.1.00001.1\nElement Mass_fraction\nFe 0.5\nCa 0.3",
            ),
            (
                "file2.csv",
                "SOURCE: 0-2.csv\nKEY: 1.1.00001.2\nElement Mass_fraction\nFe 0.4\nCa 0.2",
            ),
        ]
        mock_read_path.return_value = mock_txt

        result = converter.txt_input

        assert result == mock_txt

    @patch(
        "crossreads_petrography.pxrf.PXRFConverter.txt_input", new_callable=PropertyMock
    )
    def test_df_input(self, mock_txt_input, converter):
        mock_txt_input.return_value = [
            ("file1.csv", "content1"),
            ("file2.csv", "content2"),
        ]

        result = converter.df_input

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "filename" in result.columns
        assert "text" in result.columns

    @patch(
        "crossreads_petrography.pxrf.PXRFConverter.txt_input", new_callable=PropertyMock
    )
    @patch(
        "crossreads_petrography.pxrf.PXRFConverter.df_standards",
        new_callable=PropertyMock,
    )
    def test_df_standards_parsed(self, mock_df_standards, mock_txt_input, converter):
        mock_txt_input.return_value = [
            (
                "file1.csv",
                "Sample: t0-10CC-1.csv\nKey: Value\nElement Mass_fraction\nFe 0.5\nCa 0.3",
            ),
            (
                "file2.csv",
                "Sample: t0-50CC-1.csv\nKey: Value\nElement Mass_fraction\nFe 0.4\nCa 0.2",
            ),
        ]
        mock_df_standards.return_value = pd.DataFrame(
            {"10CC": [1.0, 2.0], "50CC": [3.0, 4.0]}, index=["Fe", "Ca"]
        )

        result = converter.df_standards_parsed

        assert isinstance(result, pd.DataFrame)
        assert "Mass_fraction" in result.columns
        assert "standard_val" in result.columns
        assert "standard_group" in result.columns
        assert "filename" in result.columns

    @patch(
        "crossreads_petrography.pxrf.PXRFConverter.df_standards_parsed",
        new_callable=PropertyMock,
    )
    def test_df_linreg(self, mock_df_standards_parsed, converter):
        mock_df = pd.DataFrame(
            {
                "Element": ["Fe", "Ca", "Fe", "Ca"],
                "standard_group": ["10-50", "10-50", "50-100", "50-100"],
                "Mass_fraction": [0.5, 0.3, 0.4, 0.2],
                "standard_val": [1.0, 2.0, 3.0, 4.0],
            }
        )
        mock_df_standards_parsed.return_value = mock_df

        result = converter.df_linreg

        assert isinstance(result, pd.DataFrame)
        assert "m" in result.columns
        assert "q" in result.columns

    @patch(
        "crossreads_petrography.pxrf.PXRFConverter.df_linreg", new_callable=PropertyMock
    )
    @patch(
        "crossreads_petrography.pxrf.PXRFConverter.df_descriptions",
        new_callable=PropertyMock,
    )
    @patch(
        "crossreads_petrography.pxrf.PXRFConverter.txt_input", new_callable=PropertyMock
    )
    def test_df_adjusted(
        self, mock_txt_input, mock_df_descriptions, mock_df_linreg, converter
    ):
        mock_txt_input.return_value = [
            (
                "file1.csv",
                "Sample: ISic001-A.csv\nKey: Value\nElement Mass_fraction Fit_Area Sigma_Area\nFe 0.5 100 10\nCa 0.3 80 8\nSi 0.2 60 6",
            ),
            (
                "file2.csv",
                "Sample: ISic002-B.csv\nKey: Value\nElement Mass_fraction Fit_Area Sigma_Area\nFe 0.4 90 9\nCa 0.2 70 7\nSi 0.4 80 8",
            ),
        ]
        mock_df_descriptions.return_value = pd.DataFrame(
            {
                "Isic": ["Isic000001", "Isic000002"],
                "a": ["Description 1", "Description 2"],
                "b": ["Description 3", "Description 4"],
            }
        )
        mock_df_linreg.return_value = pd.DataFrame(
            {
                "Element": ["Fe", "Ca", "Si"],
                "standard_group": ["10-50", "10-50", "10-50"],
                "m": [1.0, 1.0, 1.0],
                "q": [0.0, 0.0, 0.0],
            }
        )

        result = converter.df_adjusted.reset_index()

        assert isinstance(result, pd.DataFrame)
        assert "Calc_fraction" in result.columns
        assert "desc" in result.columns
        # assert result.index.names == ['source_name', 'Element']

    @patch(
        "crossreads_petrography.pxrf.PXRFConverter.df_standards_parsed",
        new_callable=PropertyMock,
    )
    def test_plot(self, mock_df_standards_parsed, converter):
        mock_df = pd.DataFrame(
            {
                "Element": ["Fe", "Ca", "Si", "Fe", "Ca", "Si"],
                "Mass_fraction": [0.5, 0.3, 0.2, 0.4, 0.2, 0.4],
                "standard_val": [1.0, 2.0, 1.5, 3.0, 4.0, 3.5],
                "standard_group": [
                    "10-50",
                    "10-50",
                    "10-50",
                    "50-100",
                    "50-100",
                    "50-100",
                ],
            }
        )
        mock_df_standards_parsed.return_value = mock_df

        result = converter.plot()

        assert isinstance(result, p9.ggplot)
        assert len(result.layers) == 2
        assert result.mapping.get("x") == "Mass_fraction"
        assert result.mapping.get("y") == "standard_val"
        assert result.mapping.get("color") == "standard_group"


@pytest.mark.usefixtures("converter")
class TestXRDConverter(TestConverterBase):
    converter_class = XRDConverter
    expected_output_files = [
        "xrd_data_postprocessed_sums.xlsx",
        "xrd_data_postprocessed_esds.xlsx",
    ]

    @patch("crossreads_petrography.xrd.read_path")
    def test_df_input(self, mock_read_path, converter):
        mock_df = pd.DataFrame(
            {
                "File": ["ISic001.csv"] * 51,
                "Parameter, Goal": ["Qcalcite"] * 51,
                "Value": [0.5] * 51,
                "ESD": [0.01] * 51,
            }
        )
        mock_read_path.return_value = mock_df

        result = converter.df_input

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 51
        assert "Parameter, Goal" in result.columns

    # @patch('crossreads_petrography.xrd.read_path')
    # def test_df_mineral_types(self, mock_read_path, converter):
    #     mock_df = pd.DataFrame({
    #         'subtype': ['Qcalcite', 'Qquartz'],
    #         'colname': ['XRD calcite content (%)', 'XRD quartz content (%)'],
    #         'category': ['', '']
    #     })
    #     mock_read_path.return_value = mock_df

    #     result = converter.df_mineral_types

    #     assert isinstance(result, pd.DataFrame)
    #     assert 'subtype' in result.columns
    #     assert 'colname' in result.columns
    #     assert 'category' in result.columns

    # @patch.object(XRDConverter, 'df_input', new_callable=PropertyMock)
    # @patch.object(XRDConverter, 'df_mineral_types', new_callable=PropertyMock)
    # def test_df_xrd(self, mock_df_mineral_types, mock_df_input, converter):
    #     mock_df_input.return_value = pd.DataFrame({
    #         'File': ['ISic001.csv'],
    #         'Parameter, Goal': ['Qcalcite'],
    #         'Value': [0.5],
    #         'ESD': [0.01]
    #     })
    #     mock_df_mineral_types.return_value = pd.DataFrame({
    #         'subtype': ['qcalcite', '*'],
    #         'colname': ['XRD calcite content (%)', 'XRD other minerals'],
    #         'category': ['Calcite', 'Other']
    #     })

    #     result = converter.df_output_sums

    #     assert isinstance(result, pd.DataFrame)
    #     assert 'Sample' in result.columns
    #     assert 'Calcite' in result.columns
    #     assert 'Total' in result.columns


@pytest.mark.usefixtures("converter")
class TestIsotopeConverter(TestConverterBase):
    converter_class = IsotopeConverter
    expected_output_files = ["isotope_intersections.xlsx"]

    @pytest.mark.parametrize("numrows", [100])
    @patch("crossreads_petrography.isotopes.read_path")
    def test_df_curves(self, mock_read_folder, converter, numrows):
        mock_df = pd.DataFrame(
            {
                "Naxos_x": list(range(numrows)),
                "Naxos_y": list(range(numrows)),
            }
        )
        mock_read_folder.return_value = mock_df

        result = converter.df_curves

        assert isinstance(result, pd.DataFrame)
        assert "marble_type" in result.columns
        assert "x" in result.columns
        assert "y" in result.columns
        assert len(result) == numrows

    @patch("crossreads_petrography.isotopes.read_metadata")
    def test_df_points(self, read_metadata, converter):
        read_metadata.return_value = pd.DataFrame(
            {
                "isotopes delta13C": [1, 2, 3],
                "isotopes delta18O": [4, 5, 6],
                "reference or rock id": ["ISic001", "ISic002", "ISic003"],
            }
        ).set_index("reference or rock id")

        result = converter.df_points
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert "x" in result.columns
        assert "y" in result.columns
        assert "Sample" in result.columns

    @patch("crossreads_petrography.isotopes.read_metadata")
    @patch("crossreads_petrography.isotopes.plot_curves")
    def test_plot(self, mock_plot_curves, mock_read_crossreads, converter):
        mock_read_crossreads.return_value = pd.DataFrame(
            {
                "isotopes delta13C": [1, 2, 3],
                "isotopes delta18O": [4, 5, 6],
                "reference or rock id": ["ISic001", "ISic002", "ISic003"],
            }
        ).set_index("reference or rock id")

        mock_plot_curves.return_value = "mock_figure"
        result = converter.plot()
        assert result == "mock_figure"
        mock_plot_curves.assert_called_once()

    @patch(
        "crossreads_petrography.isotopes.IsotopeConverter.df_curves",
        new_callable=PropertyMock,
    )
    @patch(
        "crossreads_petrography.isotopes.IsotopeConverter.df_points",
        new_callable=PropertyMock,
    )
    def test_df_intersections(self, mock_df_points, mock_df_curves, converter):
        mock_df_curves.return_value = pd.DataFrame(
            {
                "marble_type": ["marble_type1"] * 4 + ["marble_type2"] * 4,
                "x": [0, 2, 2, 0, 0, 2, 2, 0],
                "y": [0, 0, 2, 2, 1, 1, 3, 3],
            }
        )
        mock_df_points.return_value = pd.DataFrame(
            {"Sample": ["ISic001", "ISic002"], "x": [1, 3], "y": [1, 3]}
        )

        result = converter.df_intersections

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.loc["ISic001", "marble_type1"] == "✔️"
        assert result.loc["ISic002", "marble_type1"] == "✖️"

    @patch(
        "crossreads_petrography.isotopes.IsotopeConverter.df_intersections",
        new_callable=PropertyMock,
    )
    @patch("crossreads_petrography.isotopes.IsotopeConverter.plot")
    def test_save(self, mock_plot, mock_df_intersections, converter):
        mock_df = pd.DataFrame({"Sample": ["ISic001", "ISic002"]})
        mock_df_intersections.return_value = mock_df
        mock_plot.return_value = MagicMock()

        with patch("pandas.DataFrame.to_excel") as mock_to_excel, patch(
            "plotly.graph_objects.Figure.write_image"
        ) as mock_write_image, patch(
            "plotly.graph_objects.Figure.write_html"
        ) as mock_write_html:
            converter.save()
            assert mock_to_excel.call_count == 1
            mock_plot.assert_called_once()

    def test_plot_curves(self):
        df_curves = pd.DataFrame(
            {
                "marble_type": ["type1", "type1", "type2", "type2"],
                "x": [0, 2, 0, 2],
                "y": [0, 2, 1, 3],
            }
        )
        df_points = pd.DataFrame(
            {"Sample": ["ISic001", "ISic002"], "x": [1, 3], "y": [1, 3]}
        )

        result = plot_curves(df_curves, df_points)

        assert result is not None
        # Add more specific assertions about the figure if needed

    def test_determine_polygon_intersections(self):
        df_curves = pd.DataFrame(
            {
                "marble_type": ["type1"] * 4 + ["type2"] * 4,
                "x": [0, 2, 2, 0, 0, 2, 2, 0],
                "y": [0, 0, 2, 2, 1, 1, 3, 3],
            }
        )
        df_points = pd.DataFrame(
            {"Sample": ["ISic001", "ISic002"], "x": [1, 3], "y": [1, 3]}
        )

        result = determine_polygon_intersections(df_curves, df_points)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.loc["ISic001", "type1"] == "✔️"
        assert result.loc["ISic002", "type1"] == "✖️"


for cls in [
    TestMgsConverter,
    TestXRDConverter,
    TestPXRFConverter,
    TestIsotopeConverter,
]:
    cls.__test__ = True

if __name__ == "__main__":
    pytest.main()
