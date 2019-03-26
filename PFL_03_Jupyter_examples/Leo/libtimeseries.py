import xarray as xr
import numpy as np

def read_monthly_from_timeseries(filename, varname, ys=1980, ye=1999):
    """
    read data from a single CESM monthly timeseries file
    
    filename  : string
    varname   : string
    ys        : starting year
    ye        : ending year
    """
    nyear = ye-ys+1
    print(varname, 'ys, ye, nyear', ys, ye, nyear)
    
    if (type(filename) == list or type(filename) == tuple):
        ds = xr.open_mfdataset(filename)
    else:
        ds = xr.open_dataset(filename)
        
    # shift time coordinate by one day
    # this is needed because CESM puts the time stamp at the very end of the
    # averaging period, see https://bb.cgd.ucar.edu/external-tools-dont-cesm-time-coordinate
    from datetime import timedelta
    time_index_shifted  = ds.time.get_index('time') - timedelta(days=1)
    ds['time'] = time_index_shifted

    var = ds[varname].sel(time=slice(str(ys), str(ye)))
    assert(len(var) == nyear * 12) # e.g. 20 years
    
    dpm = np.array((31 ,28 ,31 ,30 ,31 ,30 ,31 ,31 ,30 ,31 ,30 ,31 )) # days per month, assuming no leap
    if (var.units == 'mm/s' or var.units == 'kg/m2/s'):
        # convert mm/s to total mm per month
        print("INFO: converting units from mm/s to mm for variable "+varname)
        var.values *= np.tile(dpm, nyear)[:,np.newaxis,np.newaxis] * 86400
        var.attrs['units'] = 'mm'
    
    var = var.squeeze().load()
        
    ds.close()
    return var



def read_clim_from_timeseries(filename, varname, clim_type='mean', ys=1980, ye=1999):
    """
    read single CESM timeseries file and compute the climatology (12 months)
    
    filename  : string
    varname   : string
    ys        : starting year
    ye        : ending year
    clim_type : type of climatology (mean / std)
    """
    nyear = ye-ys+1
    
    var = read_monthly_from_timeseries(filename, varname, ys, ye)
    assert(len(var) == nyear * 12) # e.g. 20 years

    if (clim_type == 'mean'):
        var = var.groupby('time.month').mean('time')
    elif (clim_type == 'std'):
        var = var.groupby('time.month').std('time')
    else:
        raise(ValueError("unknown clim_type : "+ str(clim_type)))
        
    return var.squeeze()


def read_yearmean_from_timeseries(filename, varname, ys=1980, ye=1999):
    """
    read CESM timeseries file and compute yearly means
    
    filename  : string
    varname   : string
    ys        : starting year
    ye        : ending year
    clim_type : type of climatology (mean / std)
    """
    nyear = ye-ys+1
    
    var = read_monthly_from_timeseries(filename, varname, ys, ye)
    assert(len(var) == nyear * 12) # e.g. 20 years
        
    var = var.groupby('time.year').mean('time')
    return var.squeeze()

def read_lon_lat_from_timeseries(filename):
    """
    read CESM longitude latitude info
    """
    if (type(filename) == list or type(filename) == tuple):
        with xr.open_mfdataset(filename) as ds:
            return ds.lon, ds.lat
    else:
        with xr.open_dataset(filename) as ds:
            return ds.lon, ds.lat
        
    

def month_to_season(var, season, agg_type='mean'):
    """
    convert monthly variable (leading dimension 12) to seasonal mean
    
    var      :  xarray DataArray
    season   :  string
    agg_type :  aggregation type (mean or sum)
    
    returns: xarray DataArray
    """
    assert(len(var)==12)
    
    if (agg_type == 'mean'):
        if (season == "ANN"):
            return var.mean(axis=0)
        elif (season == "MAM"):
            return var[[2,3,4]].mean(axis=0)
        elif (season == "JJA"):
            return var[[5,6,7]].mean(axis=0)
        elif (season == "SON"):
            return var[[8,9,10]].mean(axis=0)
        elif (season == "DJF"):
            return var[[0,1,11]].mean(axis=0)
    elif (agg_type == 'sum'):
        if (season == "ANN"):
            return var.sum(axis=0)
        elif (season == "MAM"):
            return var[[2,3,4]].sum(axis=0)
        elif (season == "JJA"):
            return var[[5,6,7]].sum(axis=0)
        elif (season == "SON"):
            return var[[8,9,10]].sum(axis=0)
        elif (season == "DJF"):
            return var[[0,1,11]].sum(axis=0)
    else:
        raise ValueError('unknown agg_type: '+agg_type)
    

    
    