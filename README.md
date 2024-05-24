# generate-ismip7-grid-files-py
Python scripts to generate ISMIP7 grid description files used for CDO regridding.  
(The grids did not change since ISMIP6)  
See also [matlab version of scripts](https://github.com/ismip/generate-ismip7-grid-files)

## Setup
Needs a python3 environment with  
numpy, netCDF4, os

## Usage
The scripts can generate 3 different types of files for Greenland and Antarctica

### grid description files (needed for CDO regridding)
  ```grid_ISMIP7_g?_IS_res.nc```
### xy coordinates 
  ```xy_ISMIP7_g?_IS_res.nc```
### area factors 
  ```af2_ISMIP7_g?_IS_res.nc```

All files are produced for the diagnostic grid g1 (ice thickness, SMB, ..)  
The scripts can also generate files for a staggered grid g0, where e.g. CISM defines horizontal velocities.  

  ```ISMIP7_AIS_multigrid_generator_nc.py```  
  ```ISMIP7_GrIS_multigrid_generator_nc.py```  

using  

  ```polar_stereo.py```  
  ```wnc.py```  
