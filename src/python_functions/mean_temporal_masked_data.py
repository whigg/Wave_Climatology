def mean_mask_t(data):
    
    """
    mean_mask(data, lon, lat, time)
        
        Function to average geospatial variables in the ocean such as swh and wsp: 
        
        Parameters 
        ----------
        data : numpy masked 3D array of float data points 
               e.g. print(swh.shape) => (133,360,) 
        lon : numpy array column vector of longitude coordinates 
        lat : numpy array column vector of longitude coordinates 
        time : numpy array of date2num or datetime values of time for days 
        
        Returns
        -------
        data_mean : 2D numpy array of the data temporal average over the designated time period 
        
        Libraries necessary to run function
        -----------------------------------
        Numpy : import numpy as np
    
    """
    
    #import libraries
    import numpy as np
    
    #set dimesnions: 
    nt, nlat, nlon = data.shape 
    
    #initialize summation and counter zero arrays: 
    data_sum = np.zeros((nlat,nlon))
    data_nc = np.zeros((nlat,nlon))
    
    #average temporally: 
    for itime in range(0,nt,1):

        #call data 
        data_i = data[itime,:,:]

        #find data points where continental fill values are. Because, hs_h is a masked array, we cn use boolean to find the indices where the grid point is masked 
        ind = data_i.mask == True

        #take only the non masked point and sum them onto the zeros matrix: 
        data_sum[~ind] = data_sum[~ind] + data_i[~ind]
        data_nc[~ind] = data_nc[~ind] + 1
    
    #Take the average: 
    data_mean = data_sum/data_nc

    return np.ma.masked_invalid(data_mean)
