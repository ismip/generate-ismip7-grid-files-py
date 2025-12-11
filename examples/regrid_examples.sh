#!/bin/bash
# CDO regridding examples

# Usage
# cdo remapycon,outgdf -setgrid,ingdf   infile.nc outfile.nc
# or
# cdo genycon,outgdf -setgrid,ingdf   infile.nc weights.nc
# cdo remap,outgdf,weights.nc -setgrid,ingdf   infile.nc outfile.nc


# AIS 8km to 4km
cdo -v remapycon,../textGDFs/gdf_ISMIP7_AIS_04000m.txt -setgrid,../textGDFs/gdf_ISMIP7_AIS_08000m.txt af2_ISMIP6_AIS_08000m.nc af2_ISMIP6_AIS_04000m_ycon.nc


# GrIS 5km to 1km
cdo -v remapycon,../textGDFs/gdf_ISMIP7_GrIS_01000m.txt -setgrid,../textGDFs/gdf_ISMIP7_GrIS_05000m.txt lithk_2100_GIS_NCAR_CISM_ctrl-proj_05000m.nc lithk_2100_GIS_NCAR_CISM_ctrl-proj_01000m_ycon.nc


# GrIS 5km to 1km with weights file
cdo -v genycon,../textGDFs/gdf_ISMIP7_GrIS_01000m.txt -setgrid,../textGDFs/gdf_ISMIP7_GrIS_05000m.txt lithk_2100_GIS_NCAR_CISM_ctrl-proj_05000m.nc weights_GrIS_05000m-01000m.nc
# Use weights file
cdo -v remap,../textGDFs/gdf_ISMIP7_GrIS_01000m.txt,weights_GrIS_05000m-01000m.nc -setgrid,../textGDFs/gdf_ISMIP7_GrIS_05000m.txt lithk_2100_GIS_NCAR_CISM_ctrl-proj_05000m.nc lithk_2100_GIS_NCAR_CISM_ctrl-proj_01000m_ycon_wgt.nc


# GrIS 5km to 1km with netcdf grid file
cdo -v remapycon,../grid_ISMIP7_g1_GrIS_01000m.nc -setgrid,../grid_ISMIP7_g1_GrIS_05000m.nc lithk_2100_GIS_NCAR_CISM_ctrl-proj_05000m.nc lithk_2100_GIS_NCAR_CISM_ctrl-proj_01000m_ycon_nc.nc
