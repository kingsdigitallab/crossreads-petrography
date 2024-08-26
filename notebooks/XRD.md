```python
import sys; sys.path.append('..')
from crossreads_petrography import *
```

↓

    Using user-specific config file: /Users/ryan/crossreads_petrography_data/config.yaml @ 2024-08-26 18:21:16,577
    Initializing Config with yaml_path: /Users/ryan/crossreads_petrography_data/config.yaml @ 2024-08-26 18:21:16,578
    Loading config from /Users/ryan/crossreads_petrography_data/config.yaml @ 2024-08-26 18:21:16,578
    Config loaded and processed successfully @ 2024-08-26 18:21:16,583

```python
xrd_converter = XRDConverter()
```

```python
xrd_converter.df_input
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>File</th>
      <th>Sample</th>
      <th>Sample ID</th>
      <th>Parameter, Goal</th>
      <th>Value</th>
      <th>ESD</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>E:/nextcloud/ISicily/petrography/XRD/001207vg.lst</td>
      <td>001207vg</td>
      <td></td>
      <td>QCalcite</td>
      <td>0.00441</td>
      <td>0.00085,</td>
    </tr>
    <tr>
      <th>1</th>
      <td>E:/nextcloud/ISicily/petrography/XRD/001207vg.lst</td>
      <td>001207vg</td>
      <td></td>
      <td>Qquartz</td>
      <td>0.40860</td>
      <td>0.0033,</td>
    </tr>
    <tr>
      <th>2</th>
      <td>E:/nextcloud/ISicily/petrography/XRD/001207vg.lst</td>
      <td>001207vg</td>
      <td></td>
      <td>Qmicroint2</td>
      <td>0.09400</td>
      <td>0.0025,</td>
    </tr>
    <tr>
      <th>3</th>
      <td>E:/nextcloud/ISicily/petrography/XRD/001207vg.lst</td>
      <td>001207vg</td>
      <td></td>
      <td>Qmusc2m1</td>
      <td>0.13600</td>
      <td>0.0044,</td>
    </tr>
    <tr>
      <th>4</th>
      <td>E:/nextcloud/ISicily/petrography/XRD/001207vg.lst</td>
      <td>001207vg</td>
      <td></td>
      <td>Qchlorite2b</td>
      <td>0.05540</td>
      <td>0.0023,</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>201</th>
      <td>C:/Users/Alessia/OneDrive - Nexus365/oxford/in...</td>
      <td>004365</td>
      <td></td>
      <td>QIron</td>
      <td>0.05320</td>
      <td>0.0022</td>
    </tr>
    <tr>
      <th>202</th>
      <td>C:/Users/Alessia/OneDrive - Nexus365/oxford/in...</td>
      <td>004365</td>
      <td></td>
      <td>Rwp</td>
      <td>11.80000</td>
      <td></td>
    </tr>
    <tr>
      <th>203</th>
      <td>C:/Users/Alessia/OneDrive - Nexus365/oxford/in...</td>
      <td>004365</td>
      <td></td>
      <td>Rexp</td>
      <td>11.65000</td>
      <td></td>
    </tr>
    <tr>
      <th>204</th>
      <td>C:/Users/Alessia/OneDrive - Nexus365/oxford/in...</td>
      <td>004365</td>
      <td></td>
      <td>Chi2</td>
      <td>1.02590</td>
      <td></td>
    </tr>
    <tr>
      <th>205</th>
      <td>C:/Users/Alessia/OneDrive - Nexus365/oxford/in...</td>
      <td>004365</td>
      <td></td>
      <td>GOF</td>
      <td>1.01290</td>
      <td></td>
    </tr>
  </tbody>
</table>
<p>1269 rows × 6 columns</p>
</div>

```python
xrd_converter.df_mineral_types
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>subtype</th>
      <th>colname</th>
      <th>category</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>*</td>
      <td>XRD other minerals</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>QALBINT</td>
      <td>XRD albite content (%)</td>
      <td>Plagioclase</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Qalbint</td>
      <td>XRD albite content (%)</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>QAlbite</td>
      <td>XRD albite content (%)</td>
      <td>Plagioclase</td>
    </tr>
    <tr>
      <th>4</th>
      <td>QAnalbite</td>
      <td>XRD albite content (%)</td>
      <td>Plagioclase</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>82</th>
      <td>QSanina75</td>
      <td>XRD Na-sanidine content (%)</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>83</th>
      <td>QSANINA85</td>
      <td>XRD Na-sanidine content (%)</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>84</th>
      <td>QSiO2p3121</td>
      <td>XRD quartz content (%)</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>85</th>
      <td>QSiO2p3221</td>
      <td>XRD quartz content (%)</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>86</th>
      <td>Qsmectitedi2wfix1</td>
      <td>XRD smectite content (%)</td>
      <td>Clay Mineral</td>
    </tr>
  </tbody>
</table>
<p>87 rows × 3 columns</p>
</div>

```python
xrd_converter.df_xrd
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>XRD calcite content (%)</th>
      <th>XRD calcite content (%) ESD</th>
      <th>XRD quartz content (%)</th>
      <th>XRD quartz content (%) ESD</th>
      <th>XRD microcline content (%)</th>
      <th>XRD microcline content (%) ESD</th>
      <th>XRD muscovite content (%)</th>
      <th>XRD muscovite content (%) ESD</th>
      <th>XRD chlorite content (%)</th>
      <th>XRD chlorite content (%) ESD</th>
      <th>...</th>
      <th>XRD Na-sanidine content (%)</th>
      <th>XRD Na-sanidine content (%) ESD</th>
      <th>XRD kaolinite content (%)</th>
      <th>XRD kaolinite content (%) ESD</th>
      <th>XRD andesine content (%)</th>
      <th>XRD andesine content (%) ESD</th>
      <th>XRD other minerals</th>
      <th>XRD Clay Mineral</th>
      <th>XRD K_Feldspar</th>
      <th>XRD Plagioclase</th>
    </tr>
    <tr>
      <th>Sample</th>
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
      <th>ISic000004</th>
      <td>96.39</td>
      <td>0.87</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.000</td>
      <td>0.0</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>ISic000009grey</th>
      <td>100.0</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.000</td>
      <td>0.0</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>ISic000009pink</th>
      <td>87.45</td>
      <td>0.38</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td>8.24</td>
      <td>0.33</td>
      <td></td>
      <td></td>
      <td>Qcerussite; Qhydrotalcite</td>
      <td>8.240</td>
      <td>0.0</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>ISic000015</th>
      <td>100.0</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.000</td>
      <td>0.0</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>ISic000017</th>
      <td>100.0</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.000</td>
      <td>0.0</td>
      <td>0.00</td>
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
      <td>...</td>
    </tr>
    <tr>
      <th>taoLastraR</th>
      <td>99.6</td>
      <td>0.11</td>
      <td>0.0</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>0.225</td>
      <td>0.074</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.225</td>
      <td>0.0</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>taoPiedi</th>
      <td>88.05</td>
      <td>0.22</td>
      <td>0.025</td>
      <td>0.062</td>
      <td></td>
      <td></td>
      <td>0.59</td>
      <td>0.15</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.590</td>
      <td>0.0</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>taoSarcofago</th>
      <td>98.96</td>
      <td>0.16</td>
      <td>0.242</td>
      <td>0.048</td>
      <td></td>
      <td></td>
      <td>0.35</td>
      <td>0.11</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.350</td>
      <td>0.0</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>taomascherome</th>
      <td>99.22</td>
      <td>0.37</td>
      <td>0.13</td>
      <td>0.13</td>
      <td></td>
      <td></td>
      <td>0.0</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.000</td>
      <td>0.0</td>
      <td>0.46</td>
    </tr>
    <tr>
      <th>taoreclinato</th>
      <td>99.591</td>
      <td>0.084</td>
      <td>0.07</td>
      <td>0.021</td>
      <td></td>
      <td></td>
      <td>0.0</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.000</td>
      <td>0.0</td>
      <td>0.00</td>
    </tr>
  </tbody>
</table>
<p>159 rows × 40 columns</p>
</div>

```python
xrd_converter.run()
```

↓

    Postprocessing XRD data @ 2024-08-26 18:21:17,126
    Saved: xrd_data_postprocessed.xlsx @ 2024-08-26 18:21:17,200

