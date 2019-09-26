def stat_moments_temporal(data, date_time, task):
    
    """
    stat_moments_monthly(date, data_time, task)
    
        Function to computes a climatology such that it obtains the monthly mean for a given time series
        
        Parameters 
        ----------
        data : numpy masked array row vector of temporal data at a single latitude or longitude grid point or a numpy 3D array whaere the climatology is calculated at each grid point 
               e.g. print(data.shape) => (8766,) or print(data.shape) => (8766,133, 360)
        date_time : numpy 2D array of date_time values which correspond to the time series of the data set
        task : choose between computing the seasonal progression or monthly progression. Options include: 
               task = monthly or task = seasonally
               
        Returns
        -------
        montly_data : dictionary of raw data, monthly mean, median, variance, skewness, and kurtosis statistical moments of the data and number of unmasked data points at each grid point for a given grid point or for an entire 2D geospatial array 
        
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
    monthly_data = {'month(s)': [],'data':[],'mean': [],'median': [],'var': [],'skew':[],'kurt':[],'N': [] }
    
    #case 1: monthly progression
    if task == 'monthly':
        
        #initialize a month loop that will go through each month 1 to 12 
        for m in range(1,13):

            #initialize the indices where the months vector elements are equal to the month value of the loop. Therefore, we obtain all the 2D arrays of swh wave height data that has been collected during the month of January, February, etc. in our given time series. 
            ind = months==m

            #save the time step of the month in the dictionary as a list 
            monthly_data['month(s)'].append(m)

            #apply the indice to the data to extect data collected just during the designated month
            tmp = np.ma.array(data[ind,:,:])

            #save data in raw data in monthly blocks in the dictionary
            monthly_data['data'].append(tmp)
            #compute the mean, median, var, and the number of observations for each month:
            #monthly_data['mean'].append(np.ma.mean(tmp, axis=0))
            monthly_data['median'].append(np.ma.median(tmp, axis=0))
            #monthly_data['var'].append(np.ma.var(tmp,axis = 0))
            monthly_data['N'].append(tmp.count(axis=0))

            #compute variance, skewness, and kurtosis
            #compute the second, third, and fourth power of the daily data for each month:
            tmp_square = tmp**2
            tmp_cube = tmp**3
            tmp_quad = tmp**4
            #sum the data, second power of data, third power of data, and fourth power of data and divide each sum by the number of data points in tmp time series:
            monthly_mean = np.ma.sum(tmp, axis=0)/tmp.count(axis=0)
            monthly_var_mean = np.ma.sum(tmp_square, axis=0)/tmp.count(axis=0)
            monthly_skew_mean = np.ma.sum(tmp_cube, axis=0)/tmp.count(axis=0)
            monthly_kurt_mean = np.ma.sum(tmp_quad, axis=0)/tmp.count(axis=0)
            #compute var, skew, and kurtosis of data:
            monthly_var = monthly_var_mean - monthly_mean**2
            monthly_std = (monthly_var)**(1/2)
            monthly_skew = (monthly_skew_mean - 3*monthly_mean*monthly_var - monthly_mean**3)/(monthly_std)**3
            monthly_kurt = ((monthly_kurt_mean - 4*monthly_mean*monthly_skew_mean + 6*monthly_var_mean*monthly_mean**2 - 3*monthly_mean**4)/(monthly_std**4))-3

            #append skew and kurt to dictionary:
            monthly_data['mean'].append(monthly_mean)
            monthly_data['var'].append(monthly_var)
            monthly_data['skew'].append(monthly_skew)
            monthly_data['kurt'].append(monthly_kurt)
            
    elif task == 'seasonally':

        #initialize variables
        seasons = [[12,1,2], [3,4,5], [6,7,8], [9,10,11]]

        #initialize a seasonal loop that will go through each month 1 to 12 
        for s in range(0,4):

            #call season:
            season = seasons[s]

            #initialize the indices where the months vector elements are equal to the month value of the loop. Therefore, we obtain all the 2D arrays of swh wave height data that has been collected during the month of January, February, etc. in our given time series. 
            bool_1 = months==season[0]
            bool_2 = months==season[1]
            bool_3 = months==season[2]
            ind_1 = bool_1 | bool_2
            ind = ind_1 |bool_3

            #save the time step of the month in the dictionary as a list 
            monthly_data['month(s)'].append(s)

            #apply the indice to the data to extect data collected just during the designated month
            tmp = np.ma.array(data[ind,:,:])

            #save data in raw data in monthly blocks in the dictionary
            monthly_data['data'].append(tmp)
            #compute the mean, median, var, and the number of observations for each month:
            #monthly_data['mean'].append(np.ma.mean(tmp, axis=0))
            monthly_data['median'].append(np.ma.median(tmp, axis=0))
            #monthly_data['var'].append(np.ma.var(tmp,axis = 0))
            monthly_data['N'].append(tmp.count(axis=0))

            #compute variance, skewness, and kurtosis
            #compute the second, third, and fourth power of the daily data for each month:
            tmp_square = tmp**2
            tmp_cube = tmp**3
            tmp_quad = tmp**4
            #sum the data, second power of data, third power of data, and fourth power of data and divide each sum by the number of data points in tmp time series:
            monthly_mean = np.ma.sum(tmp, axis=0)/tmp.count(axis=0)
            monthly_var_mean = np.ma.sum(tmp_square, axis=0)/tmp.count(axis=0)
            monthly_skew_mean = np.ma.sum(tmp_cube, axis=0)/tmp.count(axis=0)
            monthly_kurt_mean = np.ma.sum(tmp_quad, axis=0)/tmp.count(axis=0)
            #compute var, skew, and kurtosis of data:
            monthly_var = monthly_var_mean - monthly_mean**2
            monthly_std = (monthly_var)**(1/2)
            monthly_skew = (monthly_skew_mean - 3*monthly_mean*monthly_var - monthly_mean**3)/(monthly_std)**3
            monthly_kurt = ((monthly_kurt_mean - 4*monthly_mean*monthly_skew_mean + 
                             6*monthly_var_mean*monthly_mean**2 - 3*monthly_mean**4)/(monthly_std**4))-3

            #append skew and kurt to dictionary:
            monthly_data['mean'].append(monthly_mean)
            monthly_data['var'].append(monthly_var)
            monthly_data['skew'].append(monthly_skew)
            monthly_data['kurt'].append(monthly_kurt)
            

    return monthly_data
