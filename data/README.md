# Colab Folder Structure

This README provides an overview of the Colab folder structure for the project.

## Root Directory

The root directory is located at:


```8:9:data/default_config.yaml
    local: "{paths.repo.local}/data"
    colab: /content/drive/MyDrive/Crossreads B D1/crossreads_petrography_data
```


## Data Directory

The main data directory is located at:


```11:13:data/default_config.yaml
  data:
    local: "{paths.repo.local}/data"
    colab: "{paths.root.colab}"
```


## Subdirectories

### Metadata


```15:25:data/default_config.yaml
  metadata:
    local: "{paths.root.local}/Metadata"
    colab: "{paths.root.colab}/Metadata"

    metamorphic:
      local: "{paths.metadata.local}/Metamorphic.xlsx"
      colab: "{paths.metadata.colab}/Metamorphic.xlsx"

    sedimentary:
      local: "{paths.metadata.local}/Sedimentary.xlsx"
      colab: "{paths.metadata.colab}/Sedimentary.xlsx"
```


### Isotopes


```27:37:data/default_config.yaml
  isotopes:
    local: "{paths.data.local}/Isotopes"
    colab: "{paths.data.colab}/Isotopes"

    input:
      local: "{paths.isotopes.local}/input"
      colab: "{paths.isotopes.colab}/input"

    output: 
      local: "{paths.isotopes.local}/output"
      colab: "{paths.isotopes.colab}/output"
```


### MGS (Maximum Grain Size)


```39:49:data/default_config.yaml
  mgs:
    local: "{paths.data.local}/MGS"
    colab: "{paths.data.colab}/MGS"

    input:
      local: "{paths.mgs.local}/input"
      colab: "{paths.mgs.colab}/input"

    output: 
      local: "{paths.mgs.local}/output"
      colab: "{paths.mgs.colab}/output"
```


### XRD (X-Ray Diffraction)


```51:65:data/default_config.yaml
  xrd:
    local: "{paths.data.local}/XRD"
    colab: "{paths.data.colab}/XRD"

    input:
      local: "{paths.xrd.local}/input"
      colab: "{paths.xrd.colab}/input"

    mineral_types:
      local: "{paths.xrd.local}/Mineral Categories.xlsx"
      colab: "{paths.xrd.colab}/Mineral Categories.xlsx"

    output:
      local: "{paths.xrd.local}/output"
      colab: "{paths.xrd.colab}/output"
```


### pXRF (Portable X-Ray Fluorescence)


```67:85:data/default_config.yaml
  pxrf:
    local: "{paths.data.local}/pXRF"
    colab: "{paths.data.colab}/pXRF"

    input:
      local: "{paths.pxrf.local}/input"
      colab: "{paths.pxrf.colab}/input"

    standards:
      local: "{paths.pxrf.local}/pXRF Standards.xlsx"
      colab: "{paths.pxrf.colab}/pXRF Standards.xlsx"

    descriptions:
      local: "{paths.pxrf.local}/pXRF Logbook.xlsx"
      colab: "{paths.pxrf.colab}/pXRF Logbook.xlsx"
      
    output:
      local: "{paths.pxrf.local}/output"
      colab: "{paths.pxrf.colab}/output"
```


## Input and Output Directories

Each subdirectory (Isotopes, MGS, XRD, pXRF) contains:

1. An `input` directory for raw data
2. An `output` directory for processed data

## Additional Files

- XRD subdirectory includes a "Mineral Categories.xlsx" file
- pXRF subdirectory includes "pXRF Standards.xlsx" and "pXRF Logbook.xlsx" files

## Jupyter Notebooks

The following Jupyter notebooks are present in the project:

1. `data/Tools/Zip and backup data folder.ipynb`
2. `data/XRD/XRD.ipynb`
3. `data/Isotopes/Isotopes.ipynb`

These notebooks likely contain data processing, analysis, and visualization code for their respective subdirectories.

## Data Files

The project includes various CSV files containing XRD results, such as:

- `data/XRD/input/XRD-results-sample.CSV`
- `data/XRD/input/ISic000101-ISic000200.CSV`
- `data/XRD/input/ISic001001-ISic001200.CSV`
- `data/XRD/input/ISic000001-ISic000100.CSV`
- `data/XRD/input/ISic001501-ISic004500.CSV`
- `data/XRD/input/ISic000201-ISic001000.CSV`

These files contain detailed XRD analysis results for different samples.
