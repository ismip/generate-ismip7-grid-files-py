# generate-ismip7-grid-files-py
Python scripts to generate ISMIP7 grid description files used for CDO regridding.  
(The grids did not change since ISMIP6)  
See also old [matlab version of scripts](https://github.com/ismip/generate-ismip7-grid-files)

## Setup
Needs a python3 environment with  
numpy, netCDF4

## Usage
The scripts can generate 3 different types of files for Greenland and Antarctica

### grid description files (e.g. used for CDO regridding)
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

## New text-based grid description files
In new versions of CDO, the grid description can be provided per text files that specify the projection information. These files are much smaller in size and can be produced with the following scripts.

  ```make_GDF_AIS.py```  
  ```make_GDF_GrIS.py```  

## Example of CDO regridding
Conservative remapping (here from 16 km to 8 km grid)  
remapycon,gdf_.. specifies the output grid  
-setgrid,gdf_.. specifies the input grid  

   ```cdo -v remapycon,gdf_ISMIP7_AIS_08000 -setgrid,gdf_ISMIP7_AIS_16000 lithk_AIS_16000m.nc lithk_AIS_08000m.nc```
