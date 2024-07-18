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
#pip install git+https://github.com/quadrismegistus/crossreads-petrography
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

    [34m[1mAuthenticating and accessing Google Spreadsheet[0m[36m @ 2024-07-18 12:00:31,275[0m
    [34m[1mReading data from spreadsheet worksheet 0[0m[36m @ 2024-07-18 12:00:32,470[0m
    [34m[1mRead 151 rows from spreadsheet[0m[36m @ 2024-07-18 12:00:33,932[0m


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

    [1mInitializing IsotopeConverter[0m[36m @ 2024-07-18 12:00:33,944[0m
    [1mProcessing isotope data[0m[36m @ 2024-07-18 12:00:33,945[0m
    [1mGenerating isotope outputs[0m[36m @ 2024-07-18 12:00:33,945[0m
    [1mReading isotope curve data[0m[36m @ 2024-07-18 12:00:33,945[0m
    [34m[1mReading spreadsheet data from /Users/ryan/github/crossreads-petrography/data/input/isotopes[0m[36m @ 2024-07-18 12:00:33,946[0m
    [34m[1mReading dataframe from file: /Users/ryan/github/crossreads-petrography/data/input/isotopes/isotopes-curves.xlsx[0m[36m @ 2024-07-18 12:00:33,947[0m
    [34m[1mReading dataframe from file: /Users/ryan/github/crossreads-petrography/data/input/isotopes/other-marbles-polygons-2.xlsx[0m[36m @ 2024-07-18 12:00:34,081[0m
    [34m[1mRead 208 rows from input data[0m[36m @ 2024-07-18 12:00:34,095[0m
    [34m[1mAuthenticating and accessing Google Spreadsheet[0m[36m @ 2024-07-18 12:00:34,114[0m
    [34m[1mReading data from spreadsheet worksheet 0[0m[36m @ 2024-07-18 12:00:35,067[0m
    [34m[1mRead 151 rows from spreadsheet[0m[36m @ 2024-07-18 12:00:36,598[0m
    [34m[1mSaved: /Users/ryan/github/crossreads-petrography/data/output/isotopes/isotope_intersections.xlsx[0m[36m @ 2024-07-18 12:00:36,669[0m
    [34m[1mSaved: /Users/ryan/github/crossreads-petrography/data/output/isotopes/isotope_graph.png[0m[36m @ 2024-07-18 12:00:37,185[0m
    [34m[1mSaved: /Users/ryan/github/crossreads-petrography/data/output/isotopes/isotope_graph.html[0m[36m @ 2024-07-18 12:00:37,212[0m
    [34m[1mSaved: /Users/ryan/github/crossreads-petrography/data/output/isotopes/isotope_graph.pdf[0m[36m @ 2024-07-18 12:00:37,295[0m


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

    [1mInitializing PXRFConverter[0m[36m @ 2024-07-18 12:00:37,302[0m
    [1mProcessing pXRF data[0m[36m @ 2024-07-18 12:00:37,303[0m
    [1mSaving pXRF processed data[0m[36m @ 2024-07-18 12:00:37,303[0m
    [1mParsing pXRF measurements and calculating new fractions[0m[36m @ 2024-07-18 12:00:37,304[0m
    [1mCalculating linear regressions for standard values[0m[36m @ 2024-07-18 12:00:37,304[0m
    [1mParsing pXRF standards data[0m[36m @ 2024-07-18 12:00:37,304[0m
    [34m[1mReading txt data from /Users/ryan/github/crossreads-petrography/data/input/pXRF[0m[36m @ 2024-07-18 12:00:37,304[0m
    [1mLoading pXRF standard values[0m[36m @ 2024-07-18 12:00:37,307[0m
    [34m[1mAuthenticating and accessing Google Spreadsheet[0m[36m @ 2024-07-18 12:00:37,308[0m
    [34m[1mReading data from spreadsheet worksheet 0[0m[36m @ 2024-07-18 12:00:38,370[0m
    [34m[1mRead 11 rows from spreadsheet[0m[36m @ 2024-07-18 12:00:39,332[0m
    [1mLoading pXRF descriptions[0m[36m @ 2024-07-18 12:00:39,383[0m
    [34m[1mAuthenticating and accessing Google Spreadsheet[0m[36m @ 2024-07-18 12:00:39,383[0m
    [34m[1mReading data from spreadsheet worksheet 0[0m[36m @ 2024-07-18 12:00:39,946[0m
    [34m[1mRead 22 rows from spreadsheet[0m[36m @ 2024-07-18 12:00:40,448[0m
    [1mSaved: /Users/ryan/github/crossreads-petrography/data/output/pXRF/pXRF_calculated_fractions.xlsx[0m[36m @ 2024-07-18 12:00:41,150[0m


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

    [34m[1mInitializing XRDConverter: /Users/ryan/github/crossreads-petrography/data/input/XRD / /content/drive/MyDrive/Crossreads B D1/XRD input data[0m[36m @ 2024-07-18 12:00:41,156[0m
    [34m[1mAuthenticating and accessing Google Spreadsheet[0m[36m @ 2024-07-18 12:00:41,157[0m
    [34m[1mUpdating CrossReads sheet with XRD data[0m[36m @ 2024-07-18 12:00:42,109[0m
    [34m[1mReading XRD data[0m[36m @ 2024-07-18 12:00:42,110[0m
    [34m[1mReading spreadsheet data from /Users/ryan/github/crossreads-petrography/data/input/XRD[0m[36m @ 2024-07-18 12:00:42,111[0m
    [34m[1mReading dataframe from file: /Users/ryan/github/crossreads-petrography/data/input/XRD/xrd-results-tao.CSV[0m[36m @ 2024-07-18 12:00:42,111[0m
    [34m[1mReading dataframe from file: /Users/ryan/github/crossreads-petrography/data/input/XRD/XRD-results-sample.CSV[0m[36m @ 2024-07-18 12:00:42,119[0m
    [34m[1mRead 426 rows from input data[0m[36m @ 2024-07-18 12:00:42,124[0m
    [34m[1mReading CrossReads sheet from Google Spreadsheet[0m[36m @ 2024-07-18 12:00:42,134[0m
    [34m[1mReading data from spreadsheet worksheet 0[0m[36m @ 2024-07-18 12:00:42,134[0m
    [34m[1mRead 151 rows from spreadsheet[0m[36m @ 2024-07-18 12:00:43,574[0m
    [1m[ISic000104] XRD other minerals: "" -> "Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,577[0m
    [1m[ISic000004] XRD other minerals: "" -> "Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,578[0m
    [1m[ISic000034] XRD other minerals: "" -> "Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,579[0m
    [1m[ISic000036] XRD other minerals: "" -> "Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,579[0m
    [1m[ISic000068] XRD other minerals: " QIron Qgypsum QNa2SO14H20" -> "QIron; QNa2SO14H20; Qcalcitmg; Qgypsum" [0m[36m @ 2024-07-18 12:00:43,580[0m
    [1m[ISic000069] XRD other minerals: " Qquartz QIron" -> "QIron; Qquartz" [0m[36m @ 2024-07-18 12:00:43,581[0m
    [1m[ISic000121] XRD other minerals: " QIron" -> "QIron; Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,581[0m
    [1m[ISic000148] XRD other minerals: " QSiO2p3221" -> "QSiO2p3221; Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,582[0m
    [1m[ISic000163] XRD other minerals: "" -> "Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,583[0m
    [1m[ISic000178] XRD other minerals: " Qorthoclase" -> "Qcalcitmg; Qorthoclase" [0m[36m @ 2024-07-18 12:00:43,583[0m
    [1m[ISic000207] XRD other minerals: "" -> "Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,584[0m
    [1m[ISic000220] XRD other minerals: "" -> "Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,585[0m
    [1m[ISic000227] XRD other minerals: "" -> "Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,585[0m
    [1m[ISic000229] XRD other minerals: "" -> "Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,586[0m
    [1m[ISic000232] XRD other minerals: "" -> "Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,587[0m
    [1m[ISic000579] XRD other minerals: " Qmicroint2" -> "Qcalcitmg; Qmicroint2" [0m[36m @ 2024-07-18 12:00:43,587[0m
    [1m[ISic000871] XRD other minerals: " QMirabilite Qironalpha" -> "QMirabilite; Qcalcitmg; Qironalpha" [0m[36m @ 2024-07-18 12:00:43,588[0m
    [1m[ISic001120] XRD other minerals: "" -> "Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,589[0m
    [1m[ISic001135] XRD other minerals: "" -> "Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,590[0m
    [1m[ISic003335] XRD other minerals: "" -> "Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,590[0m
    [1m[ISic004341] XRD other minerals: " QIron" -> "QIron; Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,591[0m
    [1m[ISic004363] XRD other minerals: " QIron" -> "QIron; Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,591[0m
    [1m[ISic004364] XRD other minerals: "" -> "Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,592[0m
    [1m[ISic004365] XRD other minerals: " QIron" -> "QIron; Qcalcitmg" [0m[36m @ 2024-07-18 12:00:43,593[0m
    [1mUpdated 24 values in 24 samples[0m[36m @ 2024-07-18 12:00:43,593[0m
    [1mAdding 26 new rows: ISic000097p, ISic001399-1, tao100, tao105, tao106, tao227, tao240, tao31, tao5, tao57, tao60, tao63, tao64, tao64bis, tao67, tao67malta, tao69, tao7, tao74, tao87, tao90, taoLastraR, taoPiedi, taoSarcofago, taomascherome, taoreclinato[0m[36m @ 2024-07-18 12:00:43,594[0m
    [34m[1mCalculating combined columns[0m[36m @ 2024-07-18 12:00:43,595[0m
    [34m[1mCalculated XRD clay minerals, K-feldspar, and plagioclase columns[0m[36m @ 2024-07-18 12:00:43,609[0m
    [34m[1mUpdating Google Sheet with processed data (177 rows)[0m[36m @ 2024-07-18 12:00:43,611[0m
    [34m[1mUpdating Google Sheet with processed data (177 rows)[0m[36m @ 2024-07-18 12:00:43,612[0m
    [34m[1mPreparing to update 178 rows and 96 columns[0m[36m @ 2024-07-18 12:00:43,836[0m
    [34m[1mSuccessfully updated 17088 cells in the Google Sheets worksheet.[0m[36m @ 2024-07-18 12:00:45,385[0m


## Explanation

### Isotopes

#### Polygons

The class pulls polygon data locally or from Google Drive if on Colab:


```python
print(f'In Colab? {IN_COLAB}')
print(f'Isotope input data path is: {PATH_ISOTOPE_INPUT_COLAB if IN_COLAB else PATH_ISOTOPE_INPUT_DATA}')
```

    In Colab? False
    Isotope input data path is: /Users/ryan/github/crossreads-petrography/data/input/isotopes


From here the sample polygons (ranged x,y values) are taken, where x is delta13C and y is delta18O:


```python
isotope_converter.df_curves
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>Hymettus</td>
      <td>-4.422843</td>
      <td>2.293689</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Göktepe</td>
      <td>-3.268530</td>
      <td>3.470874</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Thasos-1 (2)</td>
      <td>-3.445693</td>
      <td>3.894349</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Thasos-3</td>
      <td>-10.174782</td>
      <td>2.211302</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Pentelikon</td>
      <td>-12.089915</td>
      <td>1.334951</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4077</th>
      <td>EphesosWhites1</td>
      <td>-9.307172</td>
      <td>3.005405</td>
    </tr>
    <tr>
      <th>4097</th>
      <td>EphesosWhites1</td>
      <td>-9.144790</td>
      <td>3.135135</td>
    </tr>
    <tr>
      <th>4117</th>
      <td>EphesosWhites1</td>
      <td>-8.982409</td>
      <td>3.254054</td>
    </tr>
    <tr>
      <th>4137</th>
      <td>EphesosWhites1</td>
      <td>-8.779432</td>
      <td>3.362162</td>
    </tr>
    <tr>
      <th>4157</th>
      <td>EphesosWhites1</td>
      <td>-8.568336</td>
      <td>3.524324</td>
    </tr>
  </tbody>
</table>
<p>1067 rows × 3 columns</p>
</div>



#### Samples

And from the crossreads spreadsheet are taken points for the same values for samples:


```python
isotope_converter.df_points
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
isotope_converter.plot()
```



##### Intersection table

As well as map intersections:


```python
# Dataframe for intersections
isotope_converter.df_intersections
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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




```python

```
