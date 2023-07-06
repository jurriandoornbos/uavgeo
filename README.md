<div align="center">
  <p>
    <a href="https://icaerus.eu" target="_blank">
      <img width="50%" src="https://icaerus.eu/wp-content/uploads/2022/09/ICAERUS-logo-white.svg"></a>
    <h3 align="center">uavgeo ⛰️</h3>
    
   <p align="center">
    A UAV-specific image processing library built upon <i>xarray</i> and <i>zen3geo</i>.
    <br/>
    <br/>
    <a href="https://github.com/jurriandoornbos/uavgeo/wiki"><strong>Explore the wiki »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/jurriandoornbos/uavgeo/issues">Report Bug</a>
    .
    <a href="https://github.com/jurriandoornbos/uavgeo/issues">Request Feature</a>
  </p>
</p>
</div>

![Downloads](https://img.shields.io/github/downloads/jurriandoornbos/uavgeo/total) ![Contributors](https://img.shields.io/github/contributors/jurriandoornbos/uavgeo?color=dark-green) ![Forks](https://img.shields.io/github/forks/jurriandoornbos/uavgeo?style=social) ![Stargazers](https://img.shields.io/github/stars/jurriandoornbos/uavgeo?style=social) ![Issues](https://img.shields.io/github/issues/jurriandoornbos/uavgeo) ![License](https://img.shields.io/github/license/jurriandoornbos/uavgeo) 

## Table Of Contents

* [Summary](#summary)
* [Features](#features)
* [Usage](#usage)
* [Installation](#installation)
  
## Summary
UAV image analysis is a powerful tool to gain valuable insights into the rural, urban and natural environment. Especially in conjunction with Deep Learning, large strides can be made. The problem however is that there is little standardization and a lot of boilerplate code to be written for image analysis. This package serves to bridge the gap in image processing and machine learning in UAV applications. It builds upon the efforts in the `zen3geo` packages: which implements `xarray` datapipelines from PyTorch. As well as introduces computations that are often performed in UAV analysis: spectral indices, CHM, etc. It covers UAV data import/export (raw images, ortho, and labels), image chipping (with and without spatial coordinates), spectral analysis (index and products calculation), (Deep) model training and visualization.

## Features

- [ ] Import and export drone images (and labels)
- [ ] Spectral analysis:
  - [x] Index calculation
  - [ ] Product calculation (CHM [x], LAI [ ])
- [ ] Visualization
- [ ] Deep Learning Pipeline:
  - [ ] Train/Test/Validation splitting
  - [ ] Chip images (requires `xbatcher`)
  - [ ] Data augmentation
  - [ ] YOLO (object detection) training and evaluation

## Usage
The `uavgeo` package can be installed through `pip` or `conda` (in the conda forge channel). Additionally, a docker container with jupyterlab can be used. See the Installation section for more information.

### Importing data:
`rioxarray` already has many handlers for dealing with various geospatial data, and should be used for importing:

```python
# loading your orthomosaic file:
import rioxarray as rx
# Relative path in the 'data' folder:
f = "data/my_ortho_output.tif"
ortho = rx.open_rasterio(filename = f, default_name = "ortho")
ortho.plot.imshow()
#check all the variables inside the ortho
ortho
```

When you are working with raw image files, you could also load a whole folder, using the datapipe methods from `torchdata` and `zen3geo`.

```python
import torchdata
import os
import zen3geo

#for example straight from a UAV flight folder
folder_to_search = "data/raw"
files = [os.path.join(folder_to_search, item) for item in os.listdir(folder_to_search)]

#setup the files inthe datapipe:
dp = torchdata.datapipes.iter.IterableWrapper(files)
dp_rio = dp.read_from_rioxarray()
```

Check the contents in the pipe:
```python
it = iter(dp_rio)
img = next(it)
#check first item in the pipe
img
#plot this image
img.plot.imshow()
```

Loading object detection labels from a COCO structure (built on `bboxconverter`):

```python
```

### Exporting data

Exporting object detection labels to a YOLO structure

```python
```


### Index calculations
You can use it to calculate a variety of indices from your imagery:
```python
# assuming you already loaded your data as ortho:
import uavgeo as ug

savi  = ug.compute.calc_savi(bandstack = ortho, red_id=1, nir_id=4, l = 0.51)
savi.plot.imshow(cmap = "greens")
```

#### Implemented indices:
Based on the list from [FieldImageR](https://www.opendronemap.org/fieldimager/). With some additional indices added.
They can be accesses through the `uavgeo.compute` module. All functions expect a `bandstack`, which is an `xarray.DataArray`wityh multiple bands as`bands` data. And the required bands ids, eg.: `red_id=1`. By default the functions rescale the output floats back to uint8 (0-255). This behaviour can be turned of with the `rescale = False` parameter.

| Index | calc_indexname | Description | Formula | Related Traits | References |
|-------|----------------|-------------|---------|----------------|------------|
| BI    | `calc_bi`        | Brightness Index | sqrt((RA^2+GA^2+B^2)/3) | Vegetation coverage, water content | Richardson and Wiegand (1977) |
| SCI   | `calc_sci`       | Soil Color Index | (R-G)/(R+G) | Soil color | Mathieu et al. (1998) |
| GLI   | `calc_gli`       | Green Leaf Index | (2 * G-R-B)/(2 * G+R+B) | Chlorophyll | Louhaichi et al. (2001) |
| HI    | `calc_hi`        | Hue Index | (2*R-G-B)/(G-B) | Soil color | Escadafal et al. (1994) |
| NGRDI | `calc_ngrdi`     | Normalized Green Red Difference Index | (G-R)/(G+R) | Chlorophyll, biomass, water content | Tucker (1979) |
| SI    | `calc_si`        | Saturation Index | (R-B)/(R+B) | Soil color | Escadafal et al. (1994) |
| VARI  | `calc_vari`      | Visible Atmospherically Resistant Index | (G-R)/(G+R-B) | Canopy, biomass, chlorophyll | Gitelson et al. (2002) |
| HUE   | `calc_hue`       | Overall Hue Index# | atan(2*(B-G-R)/30.5*(G-R)) | Soil color | Escadafal et al. (1994) |
| BGI   | `calc_bgi`      | Blue Green Pigment Index | B/G | Chlorophyll | Zarco-Tejada et al. (2005) |
| PSRI  | `calc_psri`      | Plant Senescence Reflectance Index | (R-G)/(RE) | Chlorophyll, LAI | Merzlyak et al. (1999) |
| NDVI  | `calc_ndvi`      | Normalized Difference Vegetation Index | (NIR-R)/(NIR+R) | Chlorophyll, nitrogen, maturity | Rouse et al. (1974) |
| GNDVI | `calc_gndvi`     | Green Normalized Difference Vegetation Index | (NIR-G)/(NIR+G) | Chlorophyll, LAI, biomass, yield | Gitelson et al. (1996) |
| RVI   | `calc_rvi`       | Ratio Vegetation Index | NIR/R | Chlorophyll, LAI, nitrogen, protein content, water content | Pearson and Miller (1972) |
| NDRE  | `calc_ndre`      | Normalized Difference Red Edge Index | (NIR-RE)/(NIR+RE) | Biomass, water content, nitrogen | Gitelson and Merzlyak (1994) |
| TVI   | `calc_tvi`       | Triangular Vegetation Index | 0.5 * (120 * (NIR — G)-200 * (R — G)) | Chlorophyll | Broge and Leblanc (2000) |
| CVI   | `calc_cvi`       | Chlorophyll Vegetation Index | (NIR * R)/(GA^2) | Chlorophyll | Vincini et al. (2008) |
| EVI   | `calc_evi`       | Enhanced Vegetation Index | 2.5  *(NIR — R)/(NIR + 6 * R — 7.5 * B) | Nitrogen, chlorophyll | Huete et al. (2002) |
| CIG   | `calc_cig`       | Chlorophyll Index — Green | (NIR/G) — 1 | Chlorophyll | Gitelson et al. (2003) |
| CIRE  | `calc_cire`      | Chlorophyll Index — Red Edge | (NIR/RE) — 1 | Chlorophyll | Gitelson et al. (2003) |
| DVI   | `calc_dvi`       | Difference Vegetation Index | NIR-RE | Nitrogen, chlorophyll | Jordan (1969) |
|-------|----------------|-------------|---------|----------------|------------|
| SAVI  | `calc_savi`      | Soil Adjusted Vegetation Index | (NIR-R)/(NIR+R+l)*(1+l) | Vegetation coverage, LAI | Huete (1988) |
| NDWI  | `calc_ndwi`      | Normalized Difference Water Index | (G-NIR)/(G+NIR) | Water coverage, water content| McFeeters (1996) |
| MNDWI | `calc_mndwi`     | Modified Normalized Difference Water Index | (G-SWIR)/(GREEN+SWIR) | Water coverage, water content| McFeeters (1996) |
| AWEIsh | `calc_aweish`     | Automated water extraction index (sh) | B + 2.5 * G - 1.5 * (NIR-SWIR1) - 0.25 * SWIR2 | Water coverage, water content| Fayeisha (2014) |
| AWEInsh | `calc_aweinsh`     | Automated water extraction index (nsh) | 4 * (G - SWIR1) - (0.25 * NIR + 2.75* SWIR1) | Water coverage, water content| Fayeisha (2014) |

#### Custom/other spectral index:
You could also write your own index calculators, according to the following template:

```python
def calc_custom(bandstack:xr.DataArray, band_a=1, band_b=2, rescale=True):
    
    ds_b = bandstack.astype(float)
    a: xr.DataArray = ds_b.sel(band=band_a)
    b: xr.DataArray = ds_b.sel(band=band_b)
    
    custom = a/b+1
    custom.name = "custom index"
    if rescale:
        custom = uavgeo.compute.rescale_floats(custom)
    return custom
```


## Installation:

It is built upon the work in `zen3geo`, which makes use of `rioxarray` and `pytorch`.
Additionally, when working with the object detection part, the `ultralytics` library is also a prerequisite.
You can choose to install everything in a Python virtual environment or directly run a jupyterlab docker:

##### Option A: Setup directly in python:
0. Create a new environment (optional but recommended):
   
   ```bash
   conda create -n uavgeo_env python=3.10
   conda activate uavgeo_env
   ```
1.   Install the required dependencies:

        Using conda (not recommended):

        ```bash
        conda install -c conda-forge zen3geo ultralytics xbatcher bboxconverter
        ```
        Using pip:
        ```bash
        pip install -f zen3geo ultralytics xbatcher bboxconverter
        ```
2. Install this package (for now: pre-pip and conda setup.)
   ```bash
       git clone https://github.com/jurriandoornbos/uavgeo.git
       cd uavgeo
       pip install -e .
   ```
##### Option B: Setup through Docker:
This starts a premade jupyter environment with everything preinstalled, based around a nvidia docker image for DL support.
* Linux/Ubuntu:
  ```bash
  docker run --rm -it --runtime=nvidia -p 8888:8888 --gpus 1 --shm-size=5gb --network=host -v /path_to_local/dir:/home/jovyan jurrain/drone-ml:gpu-torch11.8-uavgeoformers
  ```

`--network=host` flag whether you want to run it on a different machine in the same network, and want to access the notebook. (does not run locally)

`-v` flag makes sure that once downloaded, it stays in that folder, accessible from the PC, and when restarting, all the weights etc. remain in that folder. `path_to_local/dir` is thew path to your working dir where you want to access the notebook from. can be `.` if you already `cd`ed into it.

` --runtime=nvidia` can be skipped when working on WSL2



* Windows requires WSL2 and NVIDIA drivers, WSL2 should also have the nvidia toolkit (for deep learning)


