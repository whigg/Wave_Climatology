def clima_mean(date_time, data, fill_val):

    """
    clima_mean(date_time, data, fill_val)
    
        Function to computes a climatology such that it obtains the monthly mean for a given time series
        
        Parameters 
        ----------
        data : numpy masked array row vector of temporal data at a single latitude or longitude grid point or a numpy 3D array whaere the climatology is calculated at each grid point 
               e.g. print(data.shape) => (8766,) or print(data.shape) => (8766,133, 360)
        date_time : numpy 2D array of date_time values which correspond to the time series of the data set
        fill_val : determines what fill value is present in your data set. Options include:
               fill_val = 'NaN' or fill_val = 'mask'
               
        Returns
        -------
        montly_data : monthly mean data for a given grid point or for an entire 2D geospatial array 
        
        Libraries necessary to run function
        ---------------------------
        Numpy: import numpy as np
    """
    
    #import library
    import numpy as np 
    
    #set year and month 2D time arrays that correspond to the year and month at which swh data point was collected (time series indice array for year and month)
    months = np.array([m.month for m in date_time])

    #initialize the dictionary that will hold all the resulting monthly mean, std, median, and nobs data
    monthly_data = {}
    monthly_data = {'month': [],'data':[],'mean': [],'median': [],'std': [],'var':[],'N': [] }
    
    #initialize a month loop that will go through each month 1 to 12 
    for m in range(1,13):
        
        #initialize the indices where the months vector elements are equal to the month value of the loop. Therefore, we obtain all the 2D arrays of swh wave height data that has been collected during the month of January, February, etc. in our given time series. 
        ind = months==m
        #save the time step of the month in the dictionary as a list 
        monthly_data['month'].append(m)
        
        #Case 1: fill values for continents or where no data is collected are NaN values
        if fill_val == 'NaN':
            #apply the indice to the data to extect data collected just during the designated month
            tmp = np.ma.array(data[ind])
        #case 2: fill values for continents or where no data is collected are mask values
        elif fill_val == 'mask':
            #apply the indice to the data to extect data collected just during the designated month
            tmp = np.ma.array(data[ind])
            
        #save data in raw data in monthly blocks in the dictionary
        monthly_data['data'].append(tmp)
        #compute the mean, median, std, and the number of observations for each month:
        monthly_data['mean'].append(np.ma.mean(tmp, axis=0))
        monthly_data['median'].append(np.ma.median(tmp, axis=0))
        monthly_data['std'].append(np.ma.std(tmp, axis=0))
        monthly_data['var'].append(np.ma.var(tmp,axis = 0))
        monthly_data['N'].append(tmp.count(axis=0))

    return monthly_data 
