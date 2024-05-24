# wnc - write netcdf files and attributes
import numpy as np
import netCDF4 as nc

def wnc(var,fname,vname,uname,lname,dnames,add_singleton_time_dim,ncformat):
    # Write data from workspace to netCDF file.
    # Syntax:
    # wnc(var,fname,vname,uname,lname,dnames,add_singleton_time_dim,ncformat)
    # var=variable array
    # fname=name of netcdf file (in quotations, i.e. 'example.nc')
    # vname=name of variable (also in quotations)
    # uname=name of variable units (also in quotations)
    # lname=long variable name
    # dnames=names of dimensions
    # add_singleton_time_dim=0/1 to not add/add a singleton time dimension
    # ncformat=netcdf file format

    if np.ndim(var)==1:
        dnames=[dnames]
        nDims=1
        var_dims=len(var)
    else:
        nDims=np.ndim(var)
        var_dims=np.shape(var)
        
    if len(dnames) != nDims:
        raise ValueError('Dimension name list not equal in size to dimensionality of variable')

    #print(dnames)
    #print(var_dims)
    DimNames=[]
    DimSizes=[]
    for n in range(nDims):
        if isinstance(var_dims, (list, tuple)):
            DimNames+= [dnames[n]]
            DimSizes+= [var_dims[n]]
        else:
            DimNames+= [dnames[n]]
            DimSizes+= [var_dims]

    if add_singleton_time_dim:
        # if no time dimension, add an unlimited time dimension
        if not 'time' in dnames:
            DimNames+= [dnames[n]]
            DimSizes+= [None]
        else:
           raise ValueError('You requested to add unlimited time dim, but a time dim already exists.')
    #print(vname)
    #print(DimNames)
    #print(DimSizes)
    #print(var)

    ncf = nc.Dataset(fname,'a', format=ncformat)
    dims = []
    for x in ncf.dimensions:
        dims += [x]
    #print(dims)
    for n in range(len(DimNames)):
        if DimNames[n] not in dims:
            #print(DimNames[n])
            ncf.createDimension(DimNames[n],DimSizes[n])
    #print(ncf.dimensions)
    data = ncf.createVariable(vname, var.dtype,DimNames[:])
    #print(data)
    data[:] = var
    ncf.variables[vname].setncattr('units', uname)
    ncf.variables[vname].setncattr('long_name', lname)
    ncf.close()

    
def wncatts(fname,vname,attname,value):
    # Write attributes to netCDF file.
    # Syntax:
    # wncatts(fname,vname,att,value)
    # fname = name of netcdf file (in quotations, i.e. 'example.nc')
    # vname = name of variable (also in quotations)
    # attname = name of attribute (also in quotations)
    # value = attribute value
    ncf = nc.Dataset(fname,'a')
    ncf.variables[vname].setncattr(attname, value)
    ncf.close()

