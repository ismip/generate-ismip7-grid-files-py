# Calculations for the polar stereographic projection 
import numpy as np
import netCDF4 as nc

def _hemi_direction(hemisphere):
    """Return `1` for 'north' and `-1` for 'south'"""
    return {'north': 1, 'south': -1}[hemisphere]


def polar_xy_to_lonlat(x, y, true_scale_lat, central_lon, re, e, hemisphere):
    """Convert from Polar Stereographic (x, y) coordinates to
    geodetic longitude and latitude.

    Args:
        x (float): X coordinate(s) in km
        y (float): Y coordinate(s) in km
        true_scale_lat (float): true-scale latitude in degrees
        central_lon: central_meridian, longitude offset in degrees
        re (float): Earth radius in km
        e (float): Earth eccentricity
        hemisphere ('north' or 'south'): Northern or Southern hemisphere

    Returns:
        If x and y are scalars then the result is a
        two-element list containing [longitude, latitude].
        If x and y are numpy arrays then the result will be a two-element
        list where the first element is a numpy array containing
        the longitudes and the second element is a numpy array containing
        the latitudes.
    """

    hemi_direction = _hemi_direction(hemisphere)

    g2r = np.pi/180

    e2 = e * e
    e4 = e2 ** 2
    e6 = e2 ** 3
    e8 = e2 ** 4
    slat = g2r * true_scale_lat
    lambda_0 = g2r * central_lon
    rho = np.sqrt(x ** 2 + y ** 2)
    if abs(true_scale_lat - 90.) < 1e-5:
        t = rho * np.sqrt((1 + e) ** (1 + e) * (1 - e) ** (1 - e)) / (2 * re)
    else:
        cm = np.cos(slat) / np.sqrt(1 - e2 * (np.sin(slat) ** 2))
        t_c = np.tan(np.pi/4.-slat/2.) / ( ((1.-e*np.sin(slat))/(1.+e*np.sin(slat)))**(e/2.) )                   
        t = rho * t_c / (re * cm)

    chi = (np.pi / 2) - 2 * np.arctan(t)
    # from polar_convert
    #phi = chi + \
    #    ((e2 / 2) + (5 * e2 ** 2 / 24) + (e2 ** 3 / 12)) * np.sin(2 * chi) + \
    #    ((7 * e2 ** 2 / 48) + (29 * e2 ** 3 / 240)) * np.sin(4 * chi) + \
    #    (7 * e2 ** 3 / 120) * np.sin(6 * chi)
    ## from snyder including e8 terms 
    phi = (chi + \
        (e2/2. + 5.*e4/24. + e6/12. + 13.*e8/360.) * np.sin(2.*chi) + \
        (7.*e4/48. + 29.*e6/240. + 811.*e8/11520.) * np.sin(4.*chi) + \
        (7.*e6/120. + 81.*e8/1120.) * np.sin(6.*chi) + \
        (4279.*e8/161280.) * np.sin(8.*chi))
    
    lambda_ = np.arctan2(hemi_direction * x,(-hemi_direction * y)) + lambda_0

    # Compute area factors
    m = np.cos(phi)/(1 - e**2 * (np.sin(phi))**2)**0.5
    k = rho/(re*m)
    # solution for pole(s), where x=0 and y=0
    poleloc = np.where((x==0) * (y==0))
    if poleloc[1].size:
        #print(k[poleloc])
        k_0 = cm * ( ((1.+e)**(1.+e)) * ((1.-e)**(1.-e)))**(1./2.) / (2.*t_c)
        k[poleloc] = k_0
    af2 = (1./k)**2
    
    # Lat,lon 
    lat = phi/g2r * hemi_direction
    lon = lambda_/g2r * hemi_direction

    return [lon, lat, af2]


def polar_xy_scale_factor2(x, y, true_scale_lat, central_lon, re, e, hemisphere):
    """Calculate scale factor from Polar Stereographic (x, y) coordinates

    Args:
        x (float): X coordinate(s) in km
        y (float): Y coordinate(s) in km
        true_scale_lat (float): true-scale latitude in degrees
        central_lon: central_meridian, longitude offset in degrees ! not used 
        re (float): Earth radius in km
        e (float): Earth eccentricity
        hemisphere ('north' or 'south'): Northern or Southern hemisphere ! not used

    Returns:
        If x and y are scalars then the result is a
        scalar af2, the squared map scale factor.
        If x and y are numpy arrays then the result will be a numpy array 
        containing af2, the squared map scale factor.
    """

    g2r = np.pi/180

    e2 = e * e
    e4 = e2 ** 2
    e6 = e2 ** 3
    e8 = e2 ** 4
    slat = g2r * true_scale_lat
    rho = np.sqrt(x ** 2 + y ** 2)
    if abs(true_scale_lat - 90.) < 1e-5:
        t = rho * np.sqrt((1 + e) ** (1 + e) * (1 - e) ** (1 - e)) / (2 * re)
    else:
        cm = np.cos(slat) / np.sqrt(1 - e2 * (np.sin(slat) ** 2))
        t_c = np.tan(np.pi/4.-slat/2.) / ( ((1.-e*np.sin(slat))/(1.+e*np.sin(slat)))**(e/2.) )                   
        t = rho * t_c / (re * cm)

    chi = (np.pi / 2) - 2 * np.arctan(t)
    # from polar_convert
    #phi = chi + \
    #    ((e2 / 2) + (5 * e2 ** 2 / 24) + (e2 ** 3 / 12)) * np.sin(2 * chi) + \
    #    ((7 * e2 ** 2 / 48) + (29 * e2 ** 3 / 240)) * np.sin(4 * chi) + \
    #    (7 * e2 ** 3 / 120) * np.sin(6 * chi)
    ## from snyder including e8 terms 
    phi = (chi + \
        (e2/2. + 5.*e4/24. + e6/12. + 13.*e8/360.) * np.sin(2.*chi) + \
        (7.*e4/48. + 29.*e6/240. + 811.*e8/11520.) * np.sin(4.*chi) + \
        (7.*e6/120. + 81.*e8/1120.) * np.sin(6.*chi) + \
        (4279.*e8/161280.) * np.sin(8.*chi))
    
    m = np.cos(phi)/(1 - e**2 * (np.sin(phi))**2)**0.5
    k = rho/(re*m)
    # solution for pole(s), where x=0 and y=0
    poleloc = np.where((x==0) * (y==0))
    if poleloc[1].size:
        #print(k[poleloc])
        k_0 = cm * ( ((1.+e)**(1.+e)) * ((1.-e)**(1.-e)))**(1./2.) / (2.*t_c)
        k[poleloc] = k_0
    af2 = (1./k)**2
    
    return af2
