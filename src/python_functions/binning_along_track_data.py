def bin_data(data, lon, lat, dim, orientation):
    
    #documentation: 
    """ 
    bin_data(data, lon, lat, dim, orientation)
    
        Function to bin alongtrack satellite data onto a specified grid
        
        Parameters 
        ----------
        data : numpy array column vector of along track float data points that are desired to be binned on a grid
               e.g. swh = [2.34543 2.45345 ...] 
        lon : numpy array column vector of along track longitude data that correspond to the longitudinal geographic location that the data was collected from
        lat : numpy array column vector of along track latitude data that correspond to the latitudinal geographic location that the data was collected from
        dim : dimesnions of the grid that data will be placed on in the form of a list (dim = [lon, lat])
              e.g. dim = [360, 133]
        orientation : orientation of binned data in a list with three elements in the list (orientation = ['Pacific' or 'Atlantic', [lon_min lon_max] [lat_min, lat_max]])
              e.g. orientation = ['Pacific', [-179 179] [-66, 66]]
        
        Returns
        -------
        data_bin : 2D numpy array of binned data on specified grid
        
        Libraries necessary to run function
        -----------------------------------
        Numpy : import numpy as np
    """ 
    
    #Import libraries
    import numpy as np
    
    #define dimensional variables:
    nlon,nlat = dim
    lon_min = orientation[1][0]
    lon_max = orientation[1][1]
    lat_min = orientation[2][0]
    lat_max = orientation[2][1]
    
    #initialize variables: 
    data_m = np.ma.zeros((nlat,nlon))
    data_nc = np.ma.zeros((nlat,nlon))
    #data_m_sum = np.zeros((nlat,nlon))
    #data_nc_sum = np.zeros((nlat,nlon))

    #create a loop to got through each data point and bin the data onto a grid  
    for idata in range(0,len(data),1):

        #call data from data array and set lon and lat to integers (incase they are floats): 
        data_point = data[idata]
        lon_point = lon[idata]
        lat_point = lat[idata]
        
        #round longitude and latitude grid point in order that the boundary points of longitude and latitude do not exceed the size of the zero matrices: 
        
        #Method 1: round values outside of the range towards zero (increases the amount of data one binns if range of data is specified)
        if orientation[0] == 'Atlantic':
            #For longitude: 
            if abs(lon_point) < lon_max:
                #round regularly
                lon_point_int = int(lon_point)
            else:
                #round towards zero:
                lon_point_int = int(np.fix(lon_point))
        elif orientation == 'Pacific':
            #For longitude: 
            if lon_point < lon_max and lon_point > lon_min:
                #round regularly
                lon_point_int = int(lon_point)
            else: 
                #round towards zero:
                lon_point_int = int(np.fix(lon_point))  
        #For latitude: 
        if abs(lat_point) < lat_max:
            #round regularly
            lat_point_int = int(lat_point)
        else:
            #round towards zero:
            lat_point_int = int(np.fix(lat_point))
        
        #method 2: simply just round: 
        #lon_point_int = int(round(lon_point))
        #lat_point_int = int(round(lat_point))
            
        #create a conditional statement in order to only bin data that are recorded at lat_max degrees north or south or between: 
        if abs(lat_point_int) <= lat_max and lon_point_int >= lon_min:
            
            if orientation[0] == 'Atlantic':

                #For longitude: 
                lon_point_i = lon_point_int + lon_max 
                #For latitude:
                lat_point_i = lat_point_int + lat_max 

            elif orientation[0] == 'Pacific': 

                #For longitude: 
                lon_point_i = lon_point_int
                #For latitude:
                lat_point_i = lat_point_int + lat_max

            #place the swh and wind speed data onto the summation grid:
            data_m[lat_point_i,lon_point_i] += data_point

            #sum counter matrix: 
            data_nc[lat_point_i,lon_point_i] += 1
    
    #find the point where the data is not masked (note that np.ma.masked_where is looking 
    #at the boolean array of masked versus non-masked points; by finding where false point 
    #(data_nc == 0) in the boolean array, we find places where there are non masked values in the 2D array)
    N = np.ma.masked_where(data_nc == 0, data_nc)
    data_val = np.ma.masked_where(data_nc == 0, data_m)
    
    #take the average of all gridded data points (note that element wise division is a/b in python):
    data_bin = data_val/N
            
    return data_bin, N
    
