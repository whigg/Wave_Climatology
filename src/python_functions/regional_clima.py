def regional_clima(data_mean, data_var, lon, lat, lon_grid, lat_grid, ngrid, dof, loc): 
    
    """
    regional_clima(data_mean, data_var, lon, lat, lon_gird, lat_grid, ngrid, dof, loc)
    
        Function to compute the regional climatology from seasonally averaged data with its variance over the time period for a specified sized grid and location on earth
        
        Parameters 
        ----------
        data_mean : Seasonally averaged data with the following dimensions in 2D masked geospatial arrays:
                      e.g : data_mean.shape = (ntime, nlat, nlon) = (4, 133, 360)
                    Seasons are defined as: 
                      Winter = DJF
                      Spring = MAM
                      Summer = JJA
                      Fall = SON
        date_var : Seasonally averaged data's variance with the following dimensions in 2D masked geospatial arrays:
                      e.g : data_var.shape = (ntime, nlat, nlon) = (4, 133, 360)
        lon : longitude vector 
                e.g. : lon = np.arange(0, 360, 1)
        lat : latitude vector 
                e.g. : lon = np.arange(-66, 66, 1)
        lon_grid : initial longitude grid point to compute the regional climatology 
                     e.g. : lon_grid = 230
        lat_grid : initial latitude grid point to compute the regional climatology
                     e.g. : lon_grid = 230
        ngrid : The step amount of grid point that the regional climatology will average over 
                  e.g. : n_grid = 2
        dof : degrees of freedom (used to compute standard deviation of the mean) 
               e.g. : dof = 23
        loc : specifies if the regional climatology is in the northern or southern hemisphere or if it is east or west of the prime meridinal. 
               e.g : loc = [loc_lat, loc_lon] loc[0] = 'NH' or loc[0] = 'SH' and loc[1] = 'west' or loc[1] = 'east'
        
        Returns
        -------
        
        data_reg_mean : regional climatology averaged data 
                         e.g. data_reg_mean.shape = (1,12)
        data_reg_stdm : regional climatology averaged data's standard deviation of the mean
                         e.g. data_reg_stdm.shape = (1,12)
        hfit : least square fit model from a 5 parameter model (mean, annual cycle, semi-annual cycle)
        residual : model - data 
        grid_coordinates : indices from longitude and latitude which the climatology is computed for
        
        Libraries necessary to run function
        -----------------------------------
        import numpy as np
        from unweighted_least_square_fit import least_square_fit 
    
    
    """
    
    #import libraries
    import numpy as np
    from unweighted_least_square_fit import least_square_fit 
    
    #case 1: west of prime meridian
    if loc[1] == 'west':
        loc_lon = 360
    #case 2: east of prime meridian
    elif loc[1] == 'east':
        loc_lon = 0
    
    #latitude and longitude grid points that will be averaged over: 
    lat_grid_i = lat[lat_grid]
    lat_grid_f = lat[lat_grid+ngrid-1]
    lon_grid_i = lon[lon_grid]-loc_lon
    lon_grid_f = lon[lon_grid+ngrid-1]-loc_lon
    grid_cor = [lat_grid_i, lat_grid_f, lon_grid_i, lon_grid_f]
    
    #call mean and variance data from grid box indices:
    data_grid_mean = data_mean[:,lat_grid:(lat_grid+ngrid),lon_grid:(lon_grid+ngrid)]
    data_grid_var = data_var[:,lat_grid:(lat_grid+ngrid),lon_grid:(lon_grid+ngrid)]
    
    #average over the region along the column and depth dimension of the 3D array (the row axis is the time dimension): 
    data_reg_mean = np.ma.mean(np.ma.mean(data_grid_mean, axis = 1, dtype=np.float64), axis = 1)
    
    #compute the average variance over the region 
    data_reg_var = np.ma.mean(np.ma.mean(data_grid_var, axis = 1, dtype=np.float64), axis = 1)
    
    #compute the standard error of the mean assuming that degrees of freedom N = 23 years
    data_reg_stdm = np.sqrt(data_reg_var)/np.sqrt(dof)
    
    #compute the least square fit: 
    hfit, x_data = least_square_fit(data = data_reg_mean, trend = 'sinusoidal', 
                                           parameters = 5, period = 12, fill_val = 'mask')
    
    #compute the residue between the model and observed SWH data:
    residual_swh = swh_hfit - swh_reg_mean_i
        
    #Case 1: Southern hemisphere region
    if loc[0] == 'SH':
        
        #In the southern hemisphere, shift the time series over such that summer months of Dec, Jan, and Feb are center of figure:    
        data_reg_mean = np.reshape(np.ma.array([data_reg_mean[6:13], data_reg_mean[0:6]]), (1,12))[0]
        data_reg_stdm = np.reshape(np.ma.array([data_reg_stdm[6:13], data_reg_stdm[0:6]]), (1,12))[0]
        hfit = np.reshape(np.ma.array([hfit[6:13], hfit[0:6]]), (1,12))[0]
        residual_swh = np.reshape(np.ma.array([residual_swh[6:13], residual_swh[0:6]]), (1,12))[0]
                
    return data_reg_mean, data_reg_stdm, hfit, residual, grid_cor


