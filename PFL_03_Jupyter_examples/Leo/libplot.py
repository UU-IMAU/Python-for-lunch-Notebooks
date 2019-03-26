
import libtimeseries


def define_global_map(fig, sps=None):
    """
    creates and returns GeoAxes in Orthographic projection,
    
    """
    import matplotlib
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    
    # Plate Carree
    myproj3 = ccrs.PlateCarree()
    
    #myproj3 = ccrs.Mollweide()


    if (sps == None):
        ax = plt.axes(projection=myproj3)
    elif (type(sps) == matplotlib.gridspec.SubplotSpec): 
        ax = fig.add_subplot(sps, projection=myproj3)
    else: 
        raise TypeError("sps not of type matplotlib.gridspec.SubplotSpec")
    
    #ax.coastlines(resolution='50m') # high res
    ax.coastlines()
        
    ax.set_global()
    #ax.set_extent([-54.5, -27, 59, 84], crs=ccrs.PlateCarree())
    
    gridlines = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, alpha=0.5) 
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(0.0)
    return ax


def define_greenland_map(fig, sps=None):
    """
    creates and returns GeoAxes in Orthographic projection,
    constrained to the Greater Greenland region
    
    """
    import matplotlib
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    
    # Orthographic sometimes doesn't work in Cartopy 0.16 because of this bug https://github.com/SciTools/cartopy/issues/1142
    #myproj3 = ccrs.Orthographic(central_longitude=-40, central_latitude=72) 
    
    # Stereographic
    myproj3 = ccrs.Stereographic(central_longitude=-40, central_latitude=72)

    if (sps == None):
        ax = plt.axes(projection=myproj3)
    elif (type(sps) == matplotlib.gridspec.SubplotSpec): 
        ax = fig.add_subplot(sps, projection=myproj3)
    else: 
        raise TypeError("sps not of type matplotlib.gridspec.SubplotSpec")
    
    ax.coastlines(resolution='50m') # high res
    #ax.coastlines()
        
    #ax.set_global()
    ax.set_extent([-54.5, -27, 59, 84], crs=ccrs.PlateCarree())
    
    gridlines = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, alpha=0.5) 
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(0.0)
    return ax



def define_greater_greenland_map(fig, sps=None):
    """
    creates and returns GeoAxes in Orthographic projection,
    constrained to the Greater Greenland region
    
    """
    import matplotlib
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    
    # Orthographic sometimes doesn't work in Cartopy 0.16 because of this bug https://github.com/SciTools/cartopy/issues/1142
    #myproj3 = ccrs.Orthographic(central_longitude=-40, central_latitude=72) 
    
    # Stereographic
    myproj3 = ccrs.Stereographic(central_longitude=-40, central_latitude=72)

    if (sps == None):
        ax = plt.axes(projection=myproj3)
    elif (type(sps) == matplotlib.gridspec.SubplotSpec): 
        ax = fig.add_subplot(sps, projection=myproj3)
    else: 
        raise TypeError("sps not of type matplotlib.gridspec.SubplotSpec")
    
    #ax.coastlines(resolution='50m') # high res
    ax.coastlines()
        
    #ax.set_global()
    ax.set_extent([-70, -10, 55, 85], crs=ccrs.PlateCarree())
    
    gridlines = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, alpha=0.5) 
    return ax
    

def define_north_polar_map(fig, lat_min = 40., sps = None):
    """
    creates and returns GeoAxes in NorthPolarStereo projection, constrained to 55-90 N
    
    when plotting on a GridSpec, the SubplotSpec can be passed as an argument
    https://matplotlib.org/api/_as_gen/matplotlib.gridspec.GridSpec.html
    
    e.g.
        gs = gridspec.GridSpec(1, 2, figure=fig)
        ax = define_north_polar_map(fig, gs[0,0])
    
    fig     : Matplotlib figure
    lat_min : minimum latitude still shown
    sps     : subplotspec instance
    """
    from matplotlib.path import Path
    import matplotlib
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import numpy as np

    if (sps == None):
        ax = plt.axes(projection=ccrs.NorthPolarStereo())
    elif (type(sps) == matplotlib.gridspec.SubplotSpec): 
        ax = fig.add_subplot(sps, projection=ccrs.NorthPolarStereo())
    else: 
        raise TypeError("sps not of type matplotlib.gridspec.SubplotSpec")
    
    #ax.coastlines(resolution='50m') # high res
    ax.coastlines()
        
    # From example: http://scitools.org.uk/cartopy/docs/latest/examples/always_circular_stereo.html
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = Path(verts * radius + center)


    ax.set_extent([-180, 180, lat_min, 90], crs=ccrs.PlateCarree())
    ax.set_boundary(circle, transform=ax.transAxes)
    
    #gridlines = ax.gridlines(draw_labels=True) # NOT SUPPORTED AT PRESENT FOR NorthPolarStereo
    return ax


def add_cyclic_point(xarray_obj, dim, period=None):
    """
    to prevent a gap at 0 longitude in Cartopy plot, add one extra longitude 
    to xarray object, the so-called cyclic point
    
    This code was adapted from https://github.com/pydata/xarray/issues/1005
    
    usage: 
        erai_jja = libplot.add_cyclic_point(erai_jja, dim='lon')
    """
    import xarray as xr
    import xarray
    
    if period is None:
        period = xarray_obj.sizes[dim] / xarray_obj.coords[dim][:2].diff(dim).item()
    first_point = xarray_obj.isel({dim: slice(1)})
    first_point.coords[dim] = first_point.coords[dim]+period
    return xr.concat([xarray_obj, first_point], dim=dim)
