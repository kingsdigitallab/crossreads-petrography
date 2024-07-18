# Crossreads: Petrography

This project provides tools and scripts for petrographic analysis as part of the Crossreads Project at the University of Oxford. It includes functionality for processing XRD (X-ray Diffraction) and pXRF (portable X-ray Fluorescence) data, as well as utilities for interacting with Google Sheets for data storage and retrieval.

Project structure:

- `crossreads_petrography/`: Main package directory
  - `isotopes.py`: For processing isotope data
  - `pxrf.py`: For processing pXRF data
  - `xrd.py`: For processing XRD data
  - `utils.py`: Utility functions for data handling and Google Sheets integration
- `notebooks/`: Jupyter notebooks for data analysis
- `tests/`: Unit tests
- `data/`: Directory for input and output data (not tracked in git)

## Install

Install the package directly from GitHub using pip:

```python
!pip install -qU git+https://github.com/quadrismegistus/crossreads-petrography
```

For development or local modifications, clone the repo and install via `pip install -e ". [dev]"`.

### Configure

The project uses a flexible configuration system to manage paths and settings across different environments (local development, Google Colab, and production).

#### Setup

1. On first run, a default `config.yaml` file will be created in `~/crossreads_petrography_data/`.
2. Modify this file to adjust paths or URLs as needed for your environment.

#### Key Configuration Options

- `production`: Set to `true` for production environment, `false` for development.
- `paths`: Contains paths for various data sources and outputs.
  - Each path typically has `local` and `colab` options.
  - Some paths include `url` options for Google Sheets integration.

#### Environment-specific Behavior

- Local development: Uses local file paths by default.
- Google Colab: Automatically uses Colab-specific paths and authentication.
- Production: Can use different URLs or paths as specified in the config.

#### Google Sheets Integration

To use the Google Sheets integration:

1. For Google Colab: Authentication is handled automatically.

2. For local development: Place your Google service account credentials JSON file at:
   ```
   ~/crossreads_petrography_data/credentials.json
   ```

This path is defined in the config file as `paths.credentials.local`.

#### Further Configuration

For detailed configuration options, refer to the `config.yaml` file in your project directory. You can customize paths, URLs, and other settings to suit your specific environment and needs.

```python
# for readme
from crossreads_petrography.utils import logger
logger.remove()
```

## Usage

### Metadata

```python
from crossreads_petrography.utils import read_crossreads_spreadsheet
df_meta = read_crossreads_spreadsheet()
```

### Isotope Processing

The `IsotopeConverter` class in `crossreads_petrography.isotopes` handles the processing of isotope data. It performs the following tasks:

- Reads isotope curve data and sample data from Google Sheets
- Determines polygon intersections for marble types
- Generates interactive plots of isotope curves and sample points
- Saves the processed data and plots to output files

```python
from crossreads_petrography.isotopes import *
isotope_converter = IsotopeConverter()
isotope_converter.run()
```

```python

```

### pXRF Processing

The `PXRFConverter` class in `pxrf.py` handles the processing of portable X-ray Fluorescence (pXRF) data. It performs the following tasks:

- Loads pXRF standard values and descriptions
- Parses pXRF measurements
- Calculates linear regressions for standard values
- Computes adjusted element fractions based on the regressions
- Generates plots of the linear regressions
- Saves the processed data to an Excel file

```python
from crossreads_petrography.pxrf import PXRFConverter
pxrf_converter = PXRFConverter()
pxrf_converter.df_standards
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>standard</th>
      <th>0CC</th>
      <th>10CC</th>
      <th>20CC</th>
      <th>30CC</th>
      <th>40CC</th>
      <th>50CC</th>
      <th>60CC</th>
      <th>70CC</th>
      <th>80CC</th>
      <th>90CC</th>
      <th>100CC</th>
    </tr>
    <tr>
      <th>Element</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Si</th>
      <td>90.647740</td>
      <td>84.341530</td>
      <td>78.459710</td>
      <td>73.463040</td>
      <td>64.173610</td>
      <td>55.238040</td>
      <td>32.494610</td>
      <td>27.119980</td>
      <td>21.505530</td>
      <td>11.571160</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>K</th>
      <td>5.976381</td>
      <td>5.560614</td>
      <td>5.172827</td>
      <td>4.843398</td>
      <td>4.230949</td>
      <td>3.641829</td>
      <td>2.142361</td>
      <td>1.788013</td>
      <td>1.417853</td>
      <td>0.762884</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Ca</th>
      <td>0.954312</td>
      <td>7.844756</td>
      <td>14.271480</td>
      <td>19.731070</td>
      <td>29.881110</td>
      <td>39.644510</td>
      <td>64.494970</td>
      <td>70.367520</td>
      <td>76.502120</td>
      <td>87.356840</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>Fe</th>
      <td>2.421567</td>
      <td>2.253103</td>
      <td>2.095976</td>
      <td>1.962495</td>
      <td>1.714336</td>
      <td>1.475631</td>
      <td>0.868062</td>
      <td>0.724484</td>
      <td>0.574500</td>
      <td>0.309113</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>

### XRD Processing

The `XRDConverter` class in `xrd.py` handles the processing of X-ray Diffraction (XRD) data. It performs the following tasks:

- Reads XRD data from input files
- Maps XRD parameters to standardized column names
- Calculates combined columns for clay minerals, K-feldspar, and plagioclase
- Updates the main CrossReads spreadsheet with processed XRD data

```python
from crossreads_petrography.xrd import XRDConverter
xrd_converter = XRDConverter()
xrd_converter.run()
```

## Explanation

### Isotopes

```python
from crossreads_petrography.isotopes import *
isotope_converter = IsotopeConverter()
```

#### Polygon data

The class pulls polygon data locally or from Google Drive if on Colab:

```python
print(f'In Colab? {IN_COLAB}')
print(f'Isotope input data path is: {get_path("isotopes.polygons")}')
```

↓

    In Colab? False
    Isotope input data path is: /Users/ryan/crossreads_petrography_data/data/input/isotopes

From here the sample polygons (ranged x,y values) are taken, where x is delta13C and y is delta18O:

```python
isotope_converter.df_curves
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>marble_type</th>
      <th>x</th>
      <th>y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Göktepe</td>
      <td>-3.268530</td>
      <td>3.470874</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Carrara</td>
      <td>-0.170109</td>
      <td>3.094660</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Proconnesos-2</td>
      <td>-9.126092</td>
      <td>2.862408</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Naxos</td>
      <td>-13.932584</td>
      <td>2.653563</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Docimium</td>
      <td>-11.409500</td>
      <td>4.077670</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4063</th>
      <td>EphesosWhites1</td>
      <td>-9.307172</td>
      <td>3.005405</td>
    </tr>
    <tr>
      <th>4083</th>
      <td>EphesosWhites1</td>
      <td>-9.144790</td>
      <td>3.135135</td>
    </tr>
    <tr>
      <th>4103</th>
      <td>EphesosWhites1</td>
      <td>-8.982409</td>
      <td>3.254054</td>
    </tr>
    <tr>
      <th>4123</th>
      <td>EphesosWhites1</td>
      <td>-8.779432</td>
      <td>3.362162</td>
    </tr>
    <tr>
      <th>4143</th>
      <td>EphesosWhites1</td>
      <td>-8.568336</td>
      <td>3.524324</td>
    </tr>
  </tbody>
</table>
<p>1067 rows × 3 columns</p>
</div>

#### Sample data

And from the crossreads spreadsheet are taken points for the same values for samples:

```python
isotope_converter.df_points
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Sample</th>
      <th>x</th>
      <th>y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ISic000104</td>
      <td>-2.29</td>
      <td>1.92</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ISic000097</td>
      <td>-1.49</td>
      <td>3.71</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ISic000004</td>
      <td>-2.69</td>
      <td>2.39</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ISic000034</td>
      <td>-0.71</td>
      <td>2.56</td>
    </tr>
    <tr>
      <th>5</th>
      <td>ISic000036</td>
      <td>-1.35</td>
      <td>2.72</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>91</th>
      <td>EXMFT109</td>
      <td>-2.01</td>
      <td>2.26</td>
    </tr>
    <tr>
      <th>92</th>
      <td>EXMFT112</td>
      <td>-2.18</td>
      <td>2.26</td>
    </tr>
    <tr>
      <th>93</th>
      <td>EXMFT134</td>
      <td>-2.87</td>
      <td>2.54</td>
    </tr>
    <tr>
      <th>94</th>
      <td>ICT005</td>
      <td>-1.78</td>
      <td>1.96</td>
    </tr>
    <tr>
      <th>95</th>
      <td>ICT006</td>
      <td>-8.37</td>
      <td>2.71</td>
    </tr>
  </tbody>
</table>
<p>81 rows × 3 columns</p>
</div>

#### Intersecting samples and polygons

##### Plotting intersections

From here we can plot the samples onto the polygons:

```python
isotope_converter.plot(output_folder=get_path('isotopes.output'))
show_img(get_path('isotopes.output') / 'isotope_graph.png')
```

↓

    
![png](README_files/README_26_0.png)
    

##### Intersection table

As well as map intersections:

```python
isotope_converter.df_intersections
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Aphrodisias</th>
      <th>CapDeGardeScritto</th>
      <th>Carrara</th>
      <th>Docimium</th>
      <th>EphesosBigio</th>
      <th>EphesosScritto</th>
      <th>EphesosWhites1</th>
      <th>EphesosWhites2</th>
      <th>FilfilaScritto</th>
      <th>Göktepe</th>
      <th>Hymettus</th>
      <th>Naxos</th>
      <th>Paros-1</th>
      <th>Paros-2 (3)</th>
      <th>Paros-4</th>
      <th>Pentelikon</th>
      <th>Proconnesos-1</th>
      <th>Proconnesos-2</th>
      <th>Thasos-1 (2)</th>
      <th>Thasos-3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>nan</th>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
    </tr>
    <tr>
      <th>ISic000104</th>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
    </tr>
    <tr>
      <th>ISic001135</th>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
    </tr>
    <tr>
      <th>ISic000181</th>
      <td>✔️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✔️</td>
      <td>✖️</td>
      <td>✔️</td>
      <td>✔️</td>
      <td>✖️</td>
      <td>✔️</td>
      <td>✔️</td>
      <td>✔️</td>
      <td>✔️</td>
      <td>✔️</td>
      <td>✔️</td>
      <td>✖️</td>
      <td>✔️</td>
      <td>✔️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✔️</td>
    </tr>
    <tr>
      <th>ISic000107</th>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>taoLastraR</th>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
    </tr>
    <tr>
      <th>taoPiedi</th>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
    </tr>
    <tr>
      <th>taoSarcofago</th>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
    </tr>
    <tr>
      <th>taomascherome</th>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
    </tr>
    <tr>
      <th>taoreclinato</th>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
      <td>✖️</td>
    </tr>
  </tbody>
</table>
<p>122 rows × 20 columns</p>
</div>

