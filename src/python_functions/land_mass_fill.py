def land_fill(data, fill, res):
    
    """
    land_fill(data, fill)
    
        Function to place NaN or zero values at all grid points in a numpy geospatial array where continents or islands exist 
        
        Parameters 
        ----------
        data : geospatial data that does not have continental regions filled with masked values. Data must be a numpy masked array and have 1 degree resolution.
               e.g. swh = [2.34543 2.45345 ...] 
        fill : Gives the option to fill data with continents and islands or only along satellite tracks. Input options include:
               fill = 'Land' or fill = 'Satellite'
               For Land, temporal resolution can be anything. For Satellite, temporal resolution must be 1 day!
        res : resolution of data set which has the following options:
               res = '1_deg' or res = '0.5_deg'
               
        Returns
        -------
        data_filled : continental and island land mass filled 2D array of swh or wsp
        
        Libraries necessary to run function
        -----------------------------------
        Numpy : import numpy as np
        NetCDF : from netCDF4 import Dataset, num2date
        temporal mean: from mean_temporal_masked_data import mean_mask_t
        
    """
    
    #import libraries: 
    import numpy as np
    from netCDF4 import Dataset, num2date
    from mean_temporal_masked_data import mean_mask_t
    
    #import data from the Ifremer p1 product: 
    nc_1deg = Dataset('/zdata/home/lcolosi/data/ifremer_p1_daily_data/my_daily_binned_ifremer_data', 'r')
    swh = nc_1deg.variables['swh'][:]
    
    nc_25deg = Dataset('/zdata/home/lcolosi/data/WW3/CFSR/lc_binned_data/ww3_hs_wnd_fp_daily_binned_data_93_16.nc', 'r')
    hs = nc_25deg.variables['hs'][:]
    
    #For land fill case 
    if fill == 'Land':
        
        if res == '1_deg':
            
            #set time, longitude, and latitude dimensions: 
            nt, nlat, nlon = swh.shape 

            #average Ifremer swh data 
            swh_mean = mean_mask_t(data = swh)

            #initialize variable: 
            data_filled = np.ma.masked_all([nt, nlat, nlon])

            #loop through each time step in order to fill continent values: 
            for iday in range(0,nt-1,1):

                #call data: 
                data_i = data[i,:,:]
                #set masks points present in the Ifremer day to masked points in the data file: 
                data_i.mask = swh_mean.mask
                #save data in 3D array: 
                data_filled[iday,:,:] = data_i
                
        elif res == '0.5_deg':
            
            #set time, longitude, and latitude dimensions: 
            nt, nlat, nlon = hs.shape 
            
            #call one time step of the hs data: 
            hs_c = hs[0,:,:]
            
            #initialize variable: 
            data_filled = np.ma.masked_all([nt, nlat, nlon])

            #loop through each time step in order to fill continent values: 
            for iday in range(0,nt-1,1):

                #call data: 
                data_i = data[i,:,:]
                #set masks points present in the Ifremer day to masked points in the data file: 
                data_i.mask = hs_c.mask
                #save data in 3D array: 
                data_filled[iday,:,:] = data_i
            
            
    #For Satellite fill case: 
    elif fill == 'Satellite':
        
        #initialize variable: 
        data_filled = np.ma.masked_all([nt, nlat, nlon])

        #loop through each time step in order to fill continent values: 
        for iday in range(0,nt-1,1):

            #call data: 
            data_i = data[i,:,:]
            #set masks points present in the Ifremer day to masked points in the data file: 
            data_i.mask = swh.mask
            #save data in 3D array: 
            data_filled[iday,:,:] = data_i
        
    return data_filled
