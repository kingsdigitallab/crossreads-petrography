# Crossreads: Petrography


This project  provides tools and scripts supporting (geo)chemical, mineralogic and petrographic analyses as part of the Crossreads Project (Faculty of Classics, University of Oxford), in collaboration with King's Digital Lab of King's College London and the Department of Biological, Geological and Environmental Sciences at the University of Catania. 
Within Crossreads, the identification of stone supports used for inscriptions of Ancient Sicily is obtained through a multi-analytical approach combining both non-invasive, non-destructive and destructive methodologies. 

The tools developed in this project include functionalities for pre- and post-processing, as well as utilities for interacting with Google Sheets for data storage and retrieval of different types of (geo)chemical, mineralogical and petrographic data deriving from the analysis of rocks. Different analytical techniques require different strategies to obtain usable data for comparisons within the dataset and/or with the literature. To facilitate the interpretation of complex data, the developed tools generate self-standing outputs, which are also consolidated into two separate spreadsheets, one for Metamorphic and one for Sedimentary rocks. 

The inclusion of a sample (ISic00000X) into one or the other worksheet is done manually in a new row. Reference materials can also be added as new rows. The columns are slightly different for Metamorphic and Sedimentary rocks and have been foreseen to cover all the distinctive features of rocks that are needed for their description and to assess their provenance. 
These cover:
-	Macroscopic appearance (colour, homogeneity, granulometry, smell, etc) from autoptic observations (Crossreads),
-	Microscopic appearance (minerals, texture, grain borders, etc) from digital and/or optical microscopy (Crossreads),
-	Mineralogical composition from XRD analyses (Crossreads),
-	Chemical composition from pXRF and/or LA-ICP-MS analyses (external laboratory),
-	Geochemical composition from isotopic analyses (external laboratory),
-	Paramagnetic properties from EPR analyses (external laboratory),
-	additional columns can be added.

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
-	The spreadsheet Metamorphic.xlsx in the Metadata folder contains isotopic values of the ISic samples in columns “isotopes delta13C” and “isotopes delta18O”, as provided from an external laboratory. 
-	The folder Isotopes/input contains spreadsheets with x, y coordinates of the contours of reference isotopic ranges from literature, i.e. polygons. The coordinates have been extracted using PlotDigitizer — Extract Data from Graph Image Online on published graphs. Such coordinates are saved in columns, whose headers are MarbleType1_x, MarbleType1_y, MarbleType2_x, MarbleType2_y, etc. It is possible to have multiple spreadsheets in the folder. 

Output data: 
Dated folders in Isotopes/output contain:
-	A graphical representation of the isotope curves, portrayed as smoothed polygons, over which the marble sample values are displayed as points. The individual marble types can be selected for display. 
-	A tabular representation of which marble polygons a given marble sample is contained within, indicated by a tick mark. 

The Isotopes.ipynb notebook (`IsotopeConverter` class in `crossreads_petrography.isotopes`) handles the processing of isotope data. It performs the following tasks:

-	Reads isotope polygons data and sample data from Google Sheets
-	Determines polygon intersections for marble types
-	Generates a table and interactive plots of isotope curves and sample points intersections
-	Saves the processed data and plots to output files


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
-	The spreadsheet Metamorphic.xlsx in the Metadata folder contains MGS of the samples in columns “digital microscopy MGS (mm)” and “optical microscopy MGS (mm)”, as observed in respective microscopic images. 
-	The folder MGS/input contains a spreadsheet where the minimum and maximum values of the box and whiskers for each marble type, as well as the median value, are collected from the literature. 

Output data:
Dated folders in MGS/output contain:
-	A tabular representation of which marbles are compatible with the values for each sample: 
  -	If the value falls in the whiskers range, one symbol is provided, while two symbols are printed if it falls in the box;
  -	If the value was obtained with the digital microscope, the symbol is a magnifying glass, while the microscope icon indicates optical microscopy. 

🔍🔍 = sample has digital microscopy measurement falling within box range of boxplot
🔍 = sample has digital microscopy measurement falling within whisker range of boxplot
🔬🔬 = sample has optical microscopy measurement falling within box range of boxplot
🔬 = sample has optical microscopy measurement falling within whisker range of boxplot

The MGS.ipynb notebook performs the following tasks:
-	Reads MGS range data and sample data from Google Sheets
-	Determines range intersections for marble types
-	Generates a table with intersections between sample points and ranges
-	Saves the processed data and plots to output files

### XRD Processing

The goal of this tool is to reshape and reorganize the output of Profex-processed XRD-patterns to obtain a simplified mineralogical composition for internal comparisons and cross-referencing with published literature. 
X-ray diffractometry yields the mineralogical composition of samples, analysed as powders in a diffractometer. Profex is used to unravel the mineralogical composition of samples by using an internal database of mineral species, with very precise compositions and code names. Such individual species can be grouped into higher levels (and their respective compositions summed accordingly), so that the results become easier to manage and interpret. 

Input data:
-	The folder XRD contains the spreadsheet “new colnames.xlsx” with the correspondences of Profex individual subtypes with sub-categories and categories. This is editable to maintain as much detail as needed. 
-	The input folder contains the .csv outputs of exporting GLOBAL GOALS from batch processing in Profex. 

Output data:

-	Dated folders in XRD/output contain the reformatted table of samples’ compositions, with columns interoperable with those in Metamorphic and Sedimentary spreadsheets in the Metadata folder.

The XRD.ipynb notebook (`XRDConverter` class in `xrd.py`) handles the processing of X-ray Diffraction (XRD) data. It performs the following tasks:  
-	Reads data from Input folder
-	Reads the correspondence between the mineralogical species and subcategories/categories as stated in new colnames.xlsx 
-	Calculates combined columns for mineral categories by summing the mineralogical species and expresses them as %
-	Generates two files in the Output folder: one for the sums and one with the analytical errors
-	Writes the sums in the Metamorphic/Sedimentary spreadsheets, based on the ISic codes and on the matching column headers, duplicating lines if needed.  


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
-	The folder pXRF contains 
  -	pxrf_coefficients.py, that summarizes the standardization coefficients and their validity ranges for a selection of elements and oxides, based on reference materials of known composition. 
  -	pXRF Logbook.xlsx, with the description of every individual region of interest (1 = a, 2 = b, etc.) in the format “description, other details”. The text before the comma is used to establish what to average together. 
- The input folder pXRF/input contains the .txt files obtained from batch processing of spectra in PyMCA with an adapted configuration file. Filenames indicate the settings that were used for acquisition (M for light elements with the original vacuum window, MK for light elements with the replacement window, t for heavier elements). 

Output data:

-	Dated folders in pXRF/output with:
  -	pXRF_corrected_values.csv with the corrected PyMCA mass fractions according to the established coefficients for individual regions of interest 
  -	pXRF_corrected_values_with_descriptions.csv displaying the descriptions from the pXRF Logbook
  -	pXRF_corrected_values_with descriptions_mean.csv averaging the values from different regions of interest sharing the same colour. 

The pXRF.ipynb notebook (`PXRFConverter` class in `pxrf.py`) handles the processing of portable X-ray Fluorescence (pXRF) data. It performs the following tasks:

- Reads data from Input folder
-	Assigns sets of coefficients to the mass fractions in the Input files, based on the elements, type of analysis (MK for light elements, t for the heavy ones), and validity range of the calibration curves
-	Calculates corrected mass fractions for each element/oxide
-	Merges MK and t data for each region of interest (indicated by the suffixes) of each ISic code
-	Averages the different regions of interest, based on the description provided for each suffix (a=1, b=2, etc) in the pXRF Logbook file
-	Generates three files in the Output folder: one for the corrected values, one for the corrected values with description, one with the averages
-	Writes the averages in the Metamorphic/Sedimentary spreadsheets, based on the ISic codes and on the matching column headers, duplicating lines if needed.

```python
from crossreads_petrography.pxrf import PXRFConverter
pxrf_converter = PXRFConverter()
pxrf_converter.run()
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
print(f'In Colab? {in_colab()}')
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
      <th>2</th>
      <td>Aphrodisias</td>
      <td>-6.529338</td>
      <td>1.953317</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Naxos</td>
      <td>-13.932584</td>
      <td>2.653563</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Paros-2 (3)</td>
      <td>-3.583021</td>
      <td>3.157248</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Pentelikon</td>
      <td>-12.089915</td>
      <td>1.334951</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Paros-4</td>
      <td>-5.617978</td>
      <td>0.872236</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4071</th>
      <td>EphesosWhites1</td>
      <td>-9.307172</td>
      <td>3.005405</td>
    </tr>
    <tr>
      <th>4091</th>
      <td>EphesosWhites1</td>
      <td>-9.144790</td>
      <td>3.135135</td>
    </tr>
    <tr>
      <th>4111</th>
      <td>EphesosWhites1</td>
      <td>-8.982409</td>
      <td>3.254054</td>
    </tr>
    <tr>
      <th>4131</th>
      <td>EphesosWhites1</td>
      <td>-8.779432</td>
      <td>3.362162</td>
    </tr>
    <tr>
      <th>4151</th>
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
      <th>6</th>
      <td>ISic000068</td>
      <td>-2.69</td>
      <td>2.66</td>
    </tr>
    <tr>
      <th>8</th>
      <td>ISic000163</td>
      <td>-2.56</td>
      <td>1.00</td>
    </tr>
    <tr>
      <th>9</th>
      <td>ISic000368</td>
      <td>-1.72</td>
      <td>1.94</td>
    </tr>
    <tr>
      <th>10</th>
      <td>ISic000711</td>
      <td>-1.52</td>
      <td>2.87</td>
    </tr>
    <tr>
      <th>11</th>
      <td>ISic000729</td>
      <td>-3.17</td>
      <td>1.91</td>
    </tr>
    <tr>
      <th>12</th>
      <td>ISic003300</td>
      <td>-1.97</td>
      <td>3.15</td>
    </tr>
    <tr>
      <th>13</th>
      <td>CU269</td>
      <td>-1.04</td>
      <td>2.15</td>
    </tr>
    <tr>
      <th>14</th>
      <td>CU431</td>
      <td>-1.99</td>
      <td>1.83</td>
    </tr>
    <tr>
      <th>15</th>
      <td>CU477</td>
      <td>-0.60</td>
      <td>2.54</td>
    </tr>
    <tr>
      <th>16</th>
      <td>CU478</td>
      <td>-2.17</td>
      <td>2.42</td>
    </tr>
    <tr>
      <th>17</th>
      <td>EXMFT003</td>
      <td>-3.91</td>
      <td>3.59</td>
    </tr>
    <tr>
      <th>18</th>
      <td>EXMFT013</td>
      <td>-1.69</td>
      <td>2.26</td>
    </tr>
    <tr>
      <th>19</th>
      <td>EXMFT033</td>
      <td>-1.62</td>
      <td>2.39</td>
    </tr>
    <tr>
      <th>20</th>
      <td>EXMFT096</td>
      <td>-2.06</td>
      <td>1.89</td>
    </tr>
    <tr>
      <th>21</th>
      <td>EXMFT109</td>
      <td>-2.01</td>
      <td>2.26</td>
    </tr>
    <tr>
      <th>22</th>
      <td>EXMFT112</td>
      <td>-2.18</td>
      <td>2.26</td>
    </tr>
    <tr>
      <th>23</th>
      <td>EXMFT134</td>
      <td>-2.87</td>
      <td>2.54</td>
    </tr>
    <tr>
      <th>24</th>
      <td>ICT005</td>
      <td>-1.78</td>
      <td>1.96</td>
    </tr>
    <tr>
      <th>25</th>
      <td>ICT006</td>
      <td>-8.37</td>
      <td>2.71</td>
    </tr>
  </tbody>
</table>
</div>

#### Intersecting samples and polygons

##### Plotting intersections

From here we can plot the samples onto the polygons:

```python
isotope_converter.plot(output_folder=get_path('isotopes.output'))
show_img(get_path('isotopes.output') / 'isotope_graph.png')
```

↓

    
![png](README_files/README_24_0.png)
    

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
      <th>ISic000097</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
    </tr>
    <tr>
      <th>ISic000004</th>
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
      <td>✔️</td>
      <td>✔️</td>
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
      <th>ISic000034</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
    </tr>
    <tr>
      <th>ISic000036</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
    </tr>
    <tr>
      <th>ISic000068</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
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
      <td>✔️</td>
    </tr>
    <tr>
      <th>ISic000163</th>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>ISic000368</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
    </tr>
    <tr>
      <th>ISic000711</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
    </tr>
    <tr>
      <th>ISic000729</th>
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
      <td>✔️</td>
      <td>✔️</td>
      <td>✔️</td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>ISic003300</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
    </tr>
    <tr>
      <th>CU269</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
    </tr>
    <tr>
      <th>CU431</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
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
      <th>CU477</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
    </tr>
    <tr>
      <th>CU478</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
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
      <th>EXMFT003</th>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
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
      <th>EXMFT013</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
    </tr>
    <tr>
      <th>EXMFT033</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
    </tr>
    <tr>
      <th>EXMFT096</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
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
      <th>EXMFT109</th>
      <td></td>
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
      <th>EXMFT112</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
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
      <th>EXMFT134</th>
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
      <td>✔️</td>
      <td>✔️</td>
      <td>✔️</td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
    </tr>
    <tr>
      <th>ICT005</th>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
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
      <th>ICT006</th>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td></td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
      <td></td>
      <td>✔️</td>
    </tr>
  </tbody>
</table>
</div>

