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

To use the Google Sheets integration:

1. For Google Colab: Authentication is handled automatically.
2. For local development: Place your Google service account credentials JSON file at:
   ```
   ~/.config/crossreads_petrography/credentials.json
   ```

## Usage

### Metadata

```python
from crossreads_petrography.utils import read_crossreads_spreadsheet
df_meta = read_crossreads_spreadsheet()
```

↓

    Authenticating and accessing Google Spreadsheet @ 2024-07-18 17:56:59,098
    Reading data from spreadsheet worksheet 0 @ 2024-07-18 17:57:00,047
    Read 177 rows from spreadsheet @ 2024-07-18 17:57:01,441

### Isotope Processing

The `IsotopeConverter` class in `crossreads_petrography.isotopes` handles the processing of isotope data. It performs the following tasks:

- Reads isotope curve data and sample data from Google Sheets
- Determines polygon intersections for marble types
- Generates interactive plots of isotope curves and sample points
- Saves the processed data and plots to output files

```python
from crossreads_petrography.isotopes import IsotopeConverter
isotope_converter = IsotopeConverter()
isotope_converter.run()
```

↓

    Initializing IsotopeConverter @ 2024-07-18 17:57:01,449
    Processing isotope data @ 2024-07-18 17:57:01,450
    Generating isotope outputs @ 2024-07-18 17:57:01,450
    Reading isotope curve data @ 2024-07-18 17:57:01,450
    Reading spreadsheet data from isotopes @ 2024-07-18 17:57:01,451
    Reading dataframe from file: isotopes-curves.xlsx @ 2024-07-18 17:57:01,451
    Reading dataframe from file: other-marbles-polygons-2.xlsx @ 2024-07-18 17:57:01,624
    Read 208 rows from input data @ 2024-07-18 17:57:01,643
    Authenticating and accessing Google Spreadsheet @ 2024-07-18 17:57:01,663
    Reading data from spreadsheet worksheet 0 @ 2024-07-18 17:57:02,538
    Read 177 rows from spreadsheet @ 2024-07-18 17:57:03,047
    Saved: isotope_intersections.xlsx @ 2024-07-18 17:57:03,117
    Saved: isotope_graph.png @ 2024-07-18 17:57:03,653
    Saved: isotope_graph.html @ 2024-07-18 17:57:03,664
    Saved: isotope_graph.pdf @ 2024-07-18 17:57:03,747

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
pxrf_converter.run()
```

↓

    Initializing PXRFConverter @ 2024-07-18 17:57:03,756
    Processing pXRF data @ 2024-07-18 17:57:03,756
    Saving pXRF processed data @ 2024-07-18 17:57:03,757
    Parsing pXRF measurements and calculating new fractions @ 2024-07-18 17:57:03,757
    Calculating linear regressions for standard values @ 2024-07-18 17:57:03,758
    Parsing pXRF standards data @ 2024-07-18 17:57:03,758
    Reading txt data from /Users/ryan/github/crossreads-petrography/data/input/pXRF @ 2024-07-18 17:57:03,758
    Loading pXRF standard values @ 2024-07-18 17:57:03,761
    Authenticating and accessing Google Spreadsheet @ 2024-07-18 17:57:03,762
    Reading data from spreadsheet worksheet 0 @ 2024-07-18 17:57:04,191
    Read 11 rows from spreadsheet @ 2024-07-18 17:57:04,545
    Loading pXRF descriptions @ 2024-07-18 17:57:04,588
    Authenticating and accessing Google Spreadsheet @ 2024-07-18 17:57:04,588
    Reading data from spreadsheet worksheet 0 @ 2024-07-18 17:57:05,017
    Read 22 rows from spreadsheet @ 2024-07-18 17:57:05,906
    Saved: pXRF_calculated_fractions.xlsx @ 2024-07-18 17:57:06,818

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

↓

    Initializing XRDConverter: /Users/ryan/github/crossreads-petrography/data/input/XRD / /content/drive/MyDrive/Crossreads B D1/XRD input data @ 2024-07-18 17:57:06,826
    Authenticating and accessing Google Spreadsheet @ 2024-07-18 17:57:06,827
    Updating CrossReads sheet with XRD data @ 2024-07-18 17:57:07,701
    Reading XRD data @ 2024-07-18 17:57:07,702
    Reading spreadsheet data from XRD @ 2024-07-18 17:57:07,702
    Reading dataframe from file: xrd-results-tao.CSV @ 2024-07-18 17:57:07,703
    Reading dataframe from file: XRD-results-sample.CSV @ 2024-07-18 17:57:07,711
    Read 426 rows from input data @ 2024-07-18 17:57:07,717
    Reading CrossReads sheet from Google Spreadsheet @ 2024-07-18 17:57:07,727
    Reading data from spreadsheet worksheet 0 @ 2024-07-18 17:57:07,728
    Read 177 rows from spreadsheet @ 2024-07-18 17:57:08,688
    Updated 0 values in 0 samples @ 2024-07-18 17:57:08,709
    No updates to apply @ 2024-07-18 17:57:08,709

## Explanation

### Isotopes

```python
from crossreads_petrography.isotopes import *
isotope_converter = IsotopeConverter()
```

↓

    Initializing IsotopeConverter @ 2024-07-18 17:57:08,714

#### Polygon data

The class pulls polygon data locally or from Google Drive if on Colab:

```python
print(f'In Colab? {IN_COLAB}')
print(f'Isotope input data path is: {PATH_ISOTOPE_INPUT.relative_to(PATH_DATA)}')
```

↓

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Cell In[1], line 1
    ----> 1 print(f'In Colab? {IN_COLAB}')
          2 print(f'Isotope input data path is: {PATH_ISOTOPE_INPUT.relative_to(PATH_DATA)}')

    NameError: name 'IN_COLAB' is not defined

From here the sample polygons (ranged x,y values) are taken, where x is delta13C and y is delta18O:

```python
isotope_converter.df_curves
```

↓

    Reading isotope curve data @ 2024-07-18 17:57:08,726
    Reading spreadsheet data from isotopes @ 2024-07-18 17:57:08,727
    Reading dataframe from file: isotopes-curves.xlsx @ 2024-07-18 17:57:08,727
    Reading dataframe from file: other-marbles-polygons-2.xlsx @ 2024-07-18 17:57:08,752
    Read 208 rows from input data @ 2024-07-18 17:57:08,769

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
      <td>Paros-1</td>
      <td>-2.417983</td>
      <td>6.031553</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Thasos-3</td>
      <td>-10.174782</td>
      <td>2.211302</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Docimium</td>
      <td>-11.409500</td>
      <td>4.077670</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Paros-2 (3)</td>
      <td>-3.583021</td>
      <td>3.157248</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Proconnesos-2</td>
      <td>-9.126092</td>
      <td>2.862408</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4066</th>
      <td>EphesosWhites1</td>
      <td>-9.307172</td>
      <td>3.005405</td>
    </tr>
    <tr>
      <th>4086</th>
      <td>EphesosWhites1</td>
      <td>-9.144790</td>
      <td>3.135135</td>
    </tr>
    <tr>
      <th>4106</th>
      <td>EphesosWhites1</td>
      <td>-8.982409</td>
      <td>3.254054</td>
    </tr>
    <tr>
      <th>4126</th>
      <td>EphesosWhites1</td>
      <td>-8.779432</td>
      <td>3.362162</td>
    </tr>
    <tr>
      <th>4146</th>
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

↓

    Authenticating and accessing Google Spreadsheet @ 2024-07-18 17:57:08,796
    Reading data from spreadsheet worksheet 0 @ 2024-07-18 17:57:09,338
    Read 177 rows from spreadsheet @ 2024-07-18 17:57:12,406

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
isotope_converter.plot(output_folder=PATH_ISOTOPE_OUTPUT)
show_img(PATH_ISOTOPE_OUTPUT / 'isotope_graph.png')
```

↓

    Saved: isotope_graph.png @ 2024-07-18 17:57:12,531
    Saved: isotope_graph.html @ 2024-07-18 17:57:12,543
    Saved: isotope_graph.pdf @ 2024-07-18 17:57:12,627

    
![png](README_files/README_25_1.png)
    

##### Intersection table

As well as map intersections:

```python
# Dataframe for intersections
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
<p>81 rows × 20 columns</p>
</div>

