# generate CDO lat-lon grid file from xy and mapping information
import numpy as np
import os 
from wnc import wnc, wncatts
from polar_stereo import polar_xy_to_lonlat, polar_xy_scale_factor2

def generate_CDO_files(agrid, proj_info, output_data_type, flag_nc, flag_xy, flag_af2):

    # Grid parameters
    dx = agrid['dx']
    dy = agrid['dy']
    nx = agrid['nx']
    ny = agrid['ny']
    offsetx = agrid['offsetx']
    offsety = agrid['offsety']

    # Create gridded x and y. Dimension order is y,x!
    ycenters, xcenters = np.meshgrid((np.arange(ny)*dy), (np.arange(nx)*dx), indexing='ij')
    #print(xcenters.shape)

    # Generate xy corner coordinates. CDO needs bounds to rotate counterclockwise
    ycorners, xcorners = np.meshgrid((np.arange(ny+1)*dy-dy/2), (np.arange(nx+1)*dx-dx/2), indexing='ij')

    ybounds = np.zeros([ycenters.shape[0], ycenters.shape[1], 4])

    SEcorner= ycorners[:-1, 1:]
    ybounds[:,:,0] = SEcorner
    NEcorner= ycorners[1:, 1:]
    ybounds[:,:,1] = NEcorner
    NWcorner= ycorners[1:, :-1]
    ybounds[:,:,2] = NWcorner
    SWcorner= ycorners[:-1, :-1]
    ybounds[:,:,3] = SWcorner

    xbounds = np.zeros([xcenters.shape[0], xcenters.shape[1], 4])

    SEcorner= xcorners[:-1, 1:]
    xbounds[:,:,0] = SEcorner
    NEcorner= xcorners[1:, 1:]
    xbounds[:,:,1] = NEcorner
    NWcorner= xcorners[1:, :-1]
    xbounds[:,:,2] = NWcorner
    SWcorner= xcorners[:-1, :-1]
    xbounds[:,:,3] = SWcorner

    # Write 2d xy netcdf file
    if flag_xy:
        print(f"Generating {agrid['xyOutputFileName']}")

        try:
            os.remove(agrid['xyOutputFileName'])
        except OSError:
            pass

        # write 2D and 1D x,y
        wnc(xcenters+proj_info['falseeasting']+offsetx, agrid['xyOutputFileName'], 'x2', 'm', 'grid center x-coordinate', ['y', 'x'], 0, 'NETCDF4')
        wnc(ycenters+proj_info['falsenorthing']+offsety, agrid['xyOutputFileName'], 'y2', 'm', 'grid center y-coordinate', ['y', 'x'], 0, 'NETCDF4')
        
        wnc(xcenters[0, :]+proj_info['falseeasting']+offsetx, agrid['xyOutputFileName'], 'x1', 'm', 'grid center x-coordinate', 'x', 0, 'NETCDF4')
        wnc(ycenters[:, 0]+proj_info['falsenorthing']+offsety, agrid['xyOutputFileName'], 'y1', 'm', 'grid center y-coordinate', 'y', 0, 'NETCDF4')

        # write bounds
        wnc(xbounds+proj_info['falseeasting']+offsetx, agrid['xyOutputFileName'], 'x_bnds', 'm', 'grid corner x-coordinate', ['y', 'x', 'nv4'], 0, 'NETCDF4')
        wnc(ybounds+proj_info['falsenorthing']+offsety, agrid['xyOutputFileName'], 'y_bnds', 'm', 'grid corner y-coordinate', ['y', 'x', 'nv4'], 0, 'NETCDF4')

        
    ## Write CDO grid netcdf file
    if flag_nc:
        
        # Create lat,lon centers
        LI_grid_center_lon, LI_grid_center_lat, _ = polar_xy_to_lonlat(xcenters+proj_info['falseeasting']+offsetx, ycenters+proj_info['falsenorthing']+offsety, proj_info['standard_parallel'], proj_info['longitude_rot'], proj_info['earthradius'], proj_info['eccentricity'], proj_info['hemisphere'] )

        # Create lat,lon bounds 
        LI_grid_corner_lon, LI_grid_corner_lat, _ = polar_xy_to_lonlat(xbounds+proj_info['falseeasting']+offsetx, ybounds+proj_info['falsenorthing']+offsety, proj_info['standard_parallel'], proj_info['longitude_rot'], proj_info['earthradius'], proj_info['eccentricity'], proj_info['hemisphere'] )
        
        # Map to 360 range 
        LI_grid_center_lon = LI_grid_center_lon % 360.
        LI_grid_corner_lon = LI_grid_corner_lon % 360.

        # Map to -180 to 180 range, nicer for Greenland
        LI_grid_center_lon = np.where(LI_grid_center_lon < 180., LI_grid_center_lon, LI_grid_center_lon - 360.)
        LI_grid_corner_lon = np.where(LI_grid_corner_lon < 180., LI_grid_corner_lon, LI_grid_corner_lon - 360.)

        # Convert to radians if requested
        if output_data_type == 'radians':
            LI_grid_center_lat = np.deg2rad(LI_grid_center_lat)
            LI_grid_center_lon = np.deg2rad(LI_grid_center_lon)
            LI_grid_corner_lat = np.deg2rad(LI_grid_corner_lat)
            LI_grid_corner_lon = np.deg2rad(LI_grid_corner_lon)
            
        print(f"Generating {agrid['LatLonOutputFileName']}")

        try:
            os.remove(agrid['LatLonOutputFileName'])
        except OSError:
            pass
        
        # grid centers
        wnc(LI_grid_center_lat, agrid['LatLonOutputFileName'], 'lat', 'degrees_north', 'grid center latitude', ['y', 'x'], 0, 'NETCDF4')
        wncatts(agrid['LatLonOutputFileName'],'lat','standard_name', 'latitude')
        wncatts(agrid['LatLonOutputFileName'],'lat','bounds', 'lat_bnds')
        
        wnc(LI_grid_center_lon, agrid['LatLonOutputFileName'], 'lon', 'degrees_east', 'grid center longitude', ['y', 'x'], 0, 'NETCDF4')
        wncatts(agrid['LatLonOutputFileName'],'lon','standard_name', 'longitude')
        wncatts(agrid['LatLonOutputFileName'],'lon','bounds', 'lon_bnds')
        
        # bounds
        wnc(LI_grid_corner_lat, agrid['LatLonOutputFileName'], 'lat_bnds', 'degrees_north', 'grid corner latitude', ['y', 'x', 'nv4'], 0, 'NETCDF4')
        wnc(LI_grid_corner_lon, agrid['LatLonOutputFileName'], 'lon_bnds', 'degrees_east', 'grid corner longitude', ['y', 'x', 'nv4'], 0, 'NETCDF4')
        
        # dummy needed for mapping
        wnc(np.int8(LI_grid_center_lon*0+1), agrid['LatLonOutputFileName'], 'dummy', '1', 'dummy variable', ['y', 'x'], 0, 'NETCDF4')
        # add lat,lon mapping
        wncatts(agrid['LatLonOutputFileName'],'dummy', 'coordinates', 'lon lat')
        
    ## Write af2 netcdf file
    if flag_af2:

        # Create af2, lat,lon centers
        LI_grid_center_af2 = polar_xy_scale_factor2(xcenters+proj_info['falseeasting']+offsetx, ycenters+proj_info['falsenorthing']+offsety, proj_info['standard_parallel'], proj_info['longitude_rot'], proj_info['earthradius'], proj_info['eccentricity'], proj_info['hemisphere'])

        print(f"Generating {agrid['af2OutputFileName']}")

        try:
            os.remove(agrid['af2OutputFileName'])
        except OSError:
            pass
        
        # grid centers
        wnc(LI_grid_center_af2, agrid['af2OutputFileName'], 'af2', 'scale_factor2', 'squared map scale factor', ['y', 'x'], 0, 'NETCDF4')
        
        
    successfully_completed = True

