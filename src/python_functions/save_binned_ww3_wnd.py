def save_netcdf_fields_ww3_wsp(wsp, lon, lat, time, output):
    
    """
    save_netcdf_fields(wsp, lon, lat, time, output)
    
        Function to save corrected binned satellite altimeter swh and wsp with longitude, latitude, and time variables into a netCDF file 
        
        Parameters 
        ----------
        swh : numpy 3D array of float swh data points 
               e.g. print(swh.shape) => (133,360,) 
        wsp : numpy 3D array of float wsp data points
        fp : numpy 3D array of float peak frequency data points
        lon : numpy array column vector of longitude coordinates 
        lat : numpy array column vector of longitude coordinates 
        time : numpy array of date2num values of time for days since 1900-02-02 00:00:0
        output: filename (path to file and file's name)
               e.g. output = '/zdata/home/lcolosi/data/ccmpv2_wind_data/daily_binned_ccmp_v2_data/ccmp_v2_wsp_daily_binned_data_93_16.nc'
        
        Returns
        -------
        NetCDF file in the current directory on is in or the directory specified by the path in the output variable 
        
        Libraries necessary to run function
        -----------------------------------
        NetCDF : from netCDF4 import Dataset, num2date, date2num
                 import netCDF4
        
        Important Note
        --------------
        The NetCDF file cannot be saved to a directory that has a file with the same name as the file being saved (permission will be denied to write over that file. Therefore, make sure all data file in the directory one is saveing to have different names
    """
    
    #import libraries:
    from netCDF4 import Dataset, num2date, date2num
    import netCDF4 

    nc = Dataset(output, 'w', format='NETCDF4')

    time_units = 'days since 1990-01-01 00:00:00'
    calendar = 'julian'
        
    Nt, Ny, Nx = wsp.shape
    
    input_vars = {}
    input_vars['wsp'] = {}
    input_vars['wsp']['units'] = 'm/s'
    input_vars['wsp']['long_name'] = 'WW3 CFSR modelled wind speed'
    input_vars['wsp']['fill_values'] = 'masked'
    input_vars['wsp']['resolution'] = '0.5 degree'
        
    time_dim = nc.createDimension('time', Nt)
    lon_dim = nc.createDimension('lon', Nx)
    lat_dim = nc.createDimension('lat', Ny)

    vars={}
    vars['time'] = nc.createVariable('time', '<f4', ('time',))
    vars['lon'] = nc.createVariable('lon', '<f4', ('lon',))
    vars['lat'] = nc.createVariable('lat', '<f4', ('lat',))


    vars_att = ['units', 'long_name']
    #vars_att = ['units', 'long_name', 'scale_factor']
    for var in input_vars.keys():
        vars[var] = nc.createVariable(var,'<f8' , ('time','lat','lon'),\
            fill_value=netCDF4.default_fillvals['f8'])
        for a in vars_att:
            setattr(vars[var], a, input_vars[var][a])

    for var_all in vars.keys():
        vars[var_all].set_auto_maskandscale(True)

    setattr(vars['lat'], 'units', 'degrees north')
    setattr(vars['lon'], 'units', 'degrees east')

    time_att = {}
    time_att['units'] = time_units
    time_att['calendar'] = calendar

    for a in time_att:
        setattr(vars['time'], a, time_att[a])

    vars['lat'][:] = lat
    vars['lon'][:] = lon
    vars['time'][:] = date2num(time, nc.variables['time'].units)
    
    vars['wsp'][:] = wsp
    
    nc.close()
