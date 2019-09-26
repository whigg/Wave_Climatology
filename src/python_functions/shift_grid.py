def shift_grid(data, lon, dlon):
    """
    shift_grid(data, lon, dlon)
    
        Function to shift gridded data horizontally to the right in order to center the geographic grid around a desired location
        
        Parameters 
        ----------
        data : numpy 2D array of float data points that are desired to be shifted
               e.g. print(swh.shape) => (133,360,) 
        lon : numpy array column vector of longitude coordinates 
        dlon : integer or float value corresponding to how many degrees of longitude are to be shifted 
        
        Returns
        -------
        data_shift : 2D numpy array of shifted data
        lon_shift : numpy array column vector shifted 
        
        Libraries necessary to run function
        -----------------------------------
        Numpy : import numpy as np
    """
    
    #import libraries: 
    import numpy as np
    
    #initialize variables: 
    nlon = len(lon)
    lon_min = np.min(lon)
    lon_max = np.max(lon)
    
    #Determine the resolution of the longitude: 
    dl = lon[1] -lon[0]
    #determine how much to shift over by: 
    nshift = int(round(dlon/dl))
    
    #set indices 
    indxs_1, indxs_2 = np.arange(nshift,nlon,1), np.arange(0,nshift,1)
    indxs = np.concatenate((indxs_1,indxs_2),axis=0)
    
    #transform indxs from a array to a list
    indxs = indxs.tolist()
    
    #Apply to data and longitude vector: 
    lon_shift = np.arange(lon_min+dlon, lon_max+dlon+1, dl)
    data_shift = data[:,indxs]
    
    return data_shift, lon_shift
