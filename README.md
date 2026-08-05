# Crossreads: Petrography

This project provides tools and scripts supporting (geo)chemical, mineralogic and petrographic analyses as part of the Crossreads Project (Faculty of Classics, University of Oxford), in collaboration with King's Digital Lab of King's College London and the Department of Biological, Geological and Environmental Sciences at the University of Catania.
Within Crossreads, the identification of stone supports used for inscriptions of Ancient Sicily is obtained through a multi-analytical approach combining both non-invasive, non-destructive and destructive methodologies.

The tools developed in this project include functionalities for pre- and post-processing, as well as utilities for interacting with Google Sheets for data storage and retrieval of different types of (geo)chemical, mineralogical and petrographic data deriving from the analysis of rocks. Different analytical techniques require different strategies to obtain usable data for comparisons within the dataset and/or with the literature. To facilitate the interpretation of complex data, the developed tools generate self-standing outputs, which are also consolidated into two separate spreadsheets, one for Metamorphic and one for Sedimentary rocks.

The inclusion of a sample (ISic00000X) into one or the other worksheet is done manually in a new row. Reference materials can also be added as new rows. The columns are slightly different for Metamorphic and Sedimentary rocks and have been foreseen to cover all the distinctive features of rocks that are needed for their description and to assess their provenance.
These cover:

- Macroscopic appearance (colour, homogeneity, granulometry, smell, etc) from autoptic observations (Crossreads),
- Microscopic appearance (minerals, texture, grain borders, etc) from digital and/or optical microscopy (Crossreads),
- Mineralogical composition from XRD analyses (Crossreads),
- Chemical composition from pXRF and/or LA-ICP-MS analyses (external laboratory),
- Geochemical composition from isotopic analyses (external laboratory),
- Paramagnetic properties from EPR analyses (external laboratory),
- additional columns can be added.

Some of these data have to be input manually by the user as numbers, yes/no values, strings of text (micro- and macroscopic appearance) into the appropriate cell of the spreadsheet; some datasets are provided by external laboratories (isotopes, LA-ICP-MS, EPR) and are copy-pasted into the spreadsheet; finally, the chemical (pXRF) and mineralogical (XRD) data acquired within the project require manipulation before they can be written in the appropriate cells of the spreadsheet.

Project structure:

- `crossreads_petrography/`: Main package directory
  - `isotopes.py`: For processing isotope data
  - `pxrf.py`: For processing pXRF data
  - `xrd.py`: For processing XRD data
  - `utils.py`: Utility functions for data handling and Google Sheets integration
- `notebooks/`: Jupyter notebooks for data analysis
- `tests/`: Unit tests
- `data/`: Directory for input and output data

## Install

Install the package directly from GitHub using pip:

```python
!pip install -qU git+https://github.com/kingsdigitallab/crossreads-petrography
```

For development or local modifications, clone the repo and install via `pip install -e ".[dev]"`.

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

- Local development: Uses Google sheets integration if available, otherwise local files
- Google Colab: Automatically uses Colab-specific paths and authentication.
- Production: Can use different URLs or paths as specified in the config; requires Google sheets integration

#### Google Sheets Integration

To use the Google Sheets integration:

1. For Google Colab: Authentication is handled automatically.

2. For local development: Place your Google service account credentials JSON file at:
   ```
   ~/crossreads_petrography_data/credentials.json
   ```

This path is defined in the config file as `paths.credentials.local`.

```python
# disabling logs for readme
from crossreads_petrography.utils import logger
logger.remove()
```

## Usage

The following folders contain all the data and the pre- and post-processing tools developed within the Crossreads project.
The data and tools are divided according to the type of analysis (Isotopes, MGS, pXRF, XRD). The Metadata folder contains all the manually input data and the aggregated ones, as obtained with a dedicated script.

### Metadata

The Metadata folder contains two spreadsheets, called Sedimentary and Metamorphic, dedicated to the two types of rocks. Only a few ancient Sicilian inscriptions are on Igneous rocks, so a dedicated spreadsheet was not created. The rows (i.e. ISic numbers) are added manually to the two spreadsheets, after checking if the inscription’s support belongs to one or the other category.
The general layout of the spreadsheets is the same:

- the column "ISic", containing the ISic code,
- a set of columns with a selection of metadata from the I.Sicily database to facilitate data interpretation (filled in automatically by reading the corpus),
- a set of columns for the macroscopic description of the rocks (filled manually),
- a set of columns for the microscopic description of the rocks (filled manually),
- a set of columns for other data (filled manually through copy-paste of externally obtained analytical results),
- a set of columns for XRD data (to be filled with post-processed data obtained within Crossreads), a set of columns for pXRF data (to be filled with post-processed data obtained within Crossreads).

In the same spreadsheet are also added, in individual lines, references from the literature, with the retrieved data distributed in the columns to facilitate comparisons.

Some of the data in the spreadsheets are used as input for post-processing (namely isotopes and MGS), while some others are the output of processing steps (namely XRD and pXRF).

Finally, Aggregator.ipynb allows to automatically fill in the metadata from the I.Sicily corpus.

```python
from crossreads_petrography.utils import read_metadata
df_meta = read_metadata()
```

### Isotopic intersections

The goal of this tool is to identify marble samples that fall within known isotopic ranges for marble subtypes as polygons from the literature.
It has been demonstrated that the stable isotopes of carbon and oxygen can be successfully used for discrimination purposes (i.e. provenance), as the geochemical properties of marbles have a correspondence with their origin.
Delta18O or d18O or δ18O is the x; delta13C or d13C or δ13C is the y. Values are expressed as per mille (‰). Values are only present in the Metamorphic spreadsheet, as they are only used for marble.

Input data:

- The spreadsheet Metamorphic.xlsx in the Metadata folder contains isotopic values of the ISic samples in columns “isotopes delta13C” and “isotopes delta18O”, as provided from an external laboratory.
- The folder Isotopes/input contains spreadsheets with x, y coordinates of the contours of reference isotopic ranges from literature, i.e. polygons. The coordinates have been extracted using PlotDigitizer — Extract Data from Graph Image Online on published graphs. Such coordinates are saved in columns, whose headers are MarbleType1_x, MarbleType1_y, MarbleType2_x, MarbleType2_y, etc. It is possible to have multiple spreadsheets in the folder.

Output data:
Dated folders in Isotopes/output contain:

- A graphical representation of the isotope curves, portrayed as smoothed polygons, over which the marble sample values are displayed as points. The individual marble types can be selected for display.
- A tabular representation of which marble polygons a given marble sample is contained within, indicated by a tick mark.

The Isotopes.ipynb notebook (`IsotopeConverter` class in `crossreads_petrography.isotopes`) handles the processing of isotope data. It performs the following tasks:

- Reads isotope polygons data and sample data from Google Sheets
- Determines polygon intersections for marble types
- Generates a table and interactive plots of isotope curves and sample points intersections
- Saves the processed data and plots to output files

```python
from crossreads_petrography.isotopes import IsotopeConverter
isotope_converter = IsotopeConverter()
isotope_converter.run()
```

### MGS intersections

The goal of this tool is to identify samples that fall within known granulometric ranges (as box and whiskers plot) for marble subtypes.
The Maximum Grain Size or MGS is the result of metamorphic processes, and as different marbles have been produced at different temperature and pressure values, this parameter can be used for discriminating purposes.
The MGS can be measured on marbles either by digital or optical microscopy, and is expressed in mm. MGS is only listed in the Metamorphic spreadsheet.

Input data:

- The spreadsheet Metamorphic.xlsx in the Metadata folder contains MGS of the samples in columns “digital microscopy MGS (mm)” and “optical microscopy MGS (mm)”, as observed in respective microscopic images.
- The folder MGS/input contains a spreadsheet where the minimum and maximum values of the box and whiskers for each marble type, as well as the median value, are collected from the literature.

Output data:
Dated folders in MGS/output contain:

- A tabular representation of which marbles are compatible with the values for each sample:
- If the value falls in the whiskers range, one symbol is provided, while two symbols are printed if it falls in the box;
- If the value was obtained with the digital microscope, the symbol is a magnifying glass, while the microscope icon indicates optical microscopy.

🔍🔍 = sample has digital microscopy measurement falling within box range of boxplot
🔍 = sample has digital microscopy measurement falling within whisker range of boxplot
🔬🔬 = sample has optical microscopy measurement falling within box range of boxplot
🔬 = sample has optical microscopy measurement falling within whisker range of boxplot

The MGS.ipynb notebook performs the following tasks:

- Reads MGS range data and sample data from Google Sheets
- Determines range intersections for marble types
- Generates a table with intersections between sample points and ranges
- Saves the processed data and plots to output files

### XRD Processing

The goal of this tool is to reshape and reorganize the output of Profex-processed XRD-patterns to obtain a simplified mineralogical composition for internal comparisons and cross-referencing with published literature.
X-ray diffractometry yields the mineralogical composition of samples, analysed as powders in a diffractometer. Profex is used to unravel the mineralogical composition of samples by using an internal database of mineral species, with very precise compositions and code names. Such individual species can be grouped into higher levels (and their respective compositions summed accordingly), so that the results become easier to manage and interpret.

Input data:

- The folder XRD contains the spreadsheet “new colnames.xlsx” with the correspondences of Profex individual subtypes with sub-categories and categories. This is editable to maintain as much detail as needed.
- The input folder contains the .csv outputs of exporting GLOBAL GOALS from batch processing in Profex.

Output data:

- Dated folders in XRD/output contain the reformatted table of samples’ compositions, with columns interoperable with those in Metamorphic and Sedimentary spreadsheets in the Metadata folder.

The XRD.ipynb notebook (`XRDConverter` class in `xrd.py`) handles the processing of X-ray Diffraction (XRD) data. It performs the following tasks:

- Reads data from Input folder
- Reads the correspondence between the mineralogical species and subcategories/categories as stated in new colnames.xlsx
- Calculates combined columns for mineral categories by summing the mineralogical species and expresses them as %
- Generates two files in the Output folder: one for the sums and one with the analytical errors
- Writes the sums in the Metamorphic/Sedimentary spreadsheets, based on the ISic codes and on the matching column headers, duplicating lines if needed.

```python
from crossreads_petrography.xrd import XRDConverter
xrd_converter = XRDConverter()
xrd_converter.run()
```

### pXRF Processing

The goal of this tool is to obtain standardized compositions of selected elements for different regions of interest (main colour of the rock, veins, rubrication, etc) of inscriptions from the processing of X-ray fluorescence spectra obtained in situ with a portable device (pXRF).
XRF yields qualitative and semi-quantitative information on a wide range of elements (13 < Z < 92). Two sets of parameters (current and voltage, filter) have been used on the selected spots, to obtain a complete characterization of light and heavy elements (MK for light elements, t for the heavy ones).
Quantitative considerations in XRF are affected by complex radiation-matter interactions and the instrumental parameters. In order to obtain reliable semi-quantitative information, a first processing step is achieved through PyMCA, which gives mass fraction values.
Furthermore, the obtained mass fractions are standardized thanks to correction coefficients calculated from standards of known composition (both carbonatic and silicatic rocks and minerals).
Finally, in order to account for rocks variability and the presence of pigments, multiple analyses (in general 3, with two different measuring setups each) have been acquired on different areas of the same object, to calculate averages.

Input data:

- The folder pXRF contains
- pxrf_coefficients.py, that summarizes the standardization coefficients and their validity ranges for a selection of elements and oxides, based on reference materials of known composition.
- pXRF Logbook.xlsx, with the description of every individual region of interest (1 = a, 2 = b, etc.) in the format “description, other details”. The text before the comma is used to establish what to average together.
- The input folder pXRF/input contains the .txt files obtained from batch processing of spectra in PyMCA with an adapted configuration file. Filenames indicate the settings that were used for acquisition (M for light elements with the original vacuum window, MK for light elements with the replacement window, t for heavier elements).

Output data:

- Dated folders in pXRF/output with:
- pXRF_corrected_values.csv with the corrected PyMCA mass fractions according to the established coefficients for individual regions of interest
- pXRF_corrected_values_with_descriptions.csv displaying the descriptions from the pXRF Logbook
- pXRF_corrected_values_with descriptions_mean.csv averaging the values from different regions of interest sharing the same colour.

The pXRF.ipynb notebook (`PXRFConverter` class in `pxrf.py`) handles the processing of portable X-ray Fluorescence (pXRF) data. It performs the following tasks:

- Reads data from Input folder
- Assigns sets of coefficients to the mass fractions in the Input files, based on the elements, type of analysis (MK for light elements, t for the heavy ones), and validity range of the calibration curves
- Calculates corrected mass fractions for each element/oxide
- Merges MK and t data for each region of interest (indicated by the suffixes) of each ISic code
- Averages the different regions of interest, based on the description provided for each suffix (a=1, b=2, etc) in the pXRF Logbook file
- Generates three files in the Output folder: one for the corrected values, one for the corrected values with description, one with the averages
- Writes the averages in the Metamorphic/Sedimentary spreadsheets, based on the ISic codes and on the matching column headers, duplicating lines if needed.

```python
from crossreads_petrography.pxrf import PXRFConverter
pxrf_converter = PXRFConverter()
pxrf_converter.run()
```

## How to cite

```bibtex
@software{Heuser_CROSSREADS_Petrography_2026,
author = {Heuser, Ryan and Vieira, Miguel and Coccato, Alessia},
month = aug,
title = {{CROSSREADS Petrography}},
url = {https://github.com/kingsdigitallab/crossreads-petrography},
version = {v1.0.0},
year = {2026}
}
```

(Generated from codemeta.json)
