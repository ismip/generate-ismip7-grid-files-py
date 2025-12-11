# Create a number of ISMIP7 grid description files
# EPSG:3413 projection
# Heiko Goelzer 2025
# python make_GDF_GrIS.py

# standard Settings
resref = 1000
nxref = 1681
nyref = 2881
xfirst = -720000
yfirst = -3450000
fname_base = "gdf_ISMIP7_GrIS_"

resolutions = [16000, 8000, 5000, 4000, 2000, 1000, 500, 250]

for resn in resolutions:

   # Checking. Not all resolutions work.
   if ((resref/resn*(nxref-1) % 1 > 0.0) | (resref/resn*(nyref-1) % 1 > 0.0)): 
       print('resolution is not commensurable !')
       exit
   
   # Calculating grid parameters
   nx = round(resref/resn*(nxref-1)+1)
   ny = round(resref/resn*(nyref-1)+1)
   res_str = f"{resn:0>5}"
   nx_str = f"{nx}"
   ny_str = f"{ny}"
   xfirst_str = f"{xfirst}"
   yfirst_str = f"{yfirst}"
   resn_str = f"{resn}"
   
   fname = fname_base + res_str + 'm.txt' ;
   
   # Write grid description file
   f = open(fname, "w")
   
   f.write('#\n')
   f.write('# ISMIP7 grid description file\n')
   f.write('# Greenland EPSG:3413\n')
   f.write('#\n')
   
   f.write('gridtype  = projection\n')
   f.write('xsize     = ' + nx_str + '\n')
   f.write('ysize     = ' + ny_str + '\n')
   f.write('xunits    = "meter"\n')
   f.write('yunits    = "meter"\n')
   f.write('xfirst    = ' + xfirst_str + '\n')
   f.write('yfirst    = ' + yfirst_str + '\n')
   f.write('xinc      = ' + resn_str + '\n')
   f.write('yinc      = ' + resn_str + '\n')
   f.write('grid_mapping = crs\n')
   f.write('grid_mapping_name = polar_stereographic\n')
   f.write('proj_params = "+proj=stere +lon_0=-45 +lat_ts=70 +lat_0=90 +x_0=0 +y_0=0"\n')
   
   f.close()
