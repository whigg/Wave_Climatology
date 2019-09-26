def monthly_average(date_time, data, fill_val):

    """
    monthly_average(date_time, data)
    
        Function to compute the unweighted least square fit of temporal data 
        
        Parameters 
        ----------
        data : numpy 2D array of temporal data along a single grid point or a 3D array of spatial and temporal data. Data fill values are NaNs. If fill values are masks, then change np.nanmean to np.ma.mean (same for all other calculations)
               e.g. print(data.shape) => (8766,) or print(data.shape) => (8766,133,360)
        date_time : numpy 2D array of date_time values which correspond to the time series of the data set
        
        fill_val : determines what fill value is present in your data set. Options include:
               fill_val = 'NaN' or fill_val = 'mask'
        
        Returns
        -------
        monthly_data : A dictionary contain the folloing key variables (all are lists type): 
            a) 'mean' : data monthly mean 
            b) 'median' : data monthly median
            c) 'std' : data monthly standard deviation 
            d) 'N' : amount of observations averaged over (used for calculating the standard deviation of the mean)
        
        Libraries necessary to run function
        -----------------------------------
        Numpy : import numpy as np
        datetime : import datetime
        
        Function is originally created by Bia Villas Bôas with small changes by Luke Colosi
    
    """

    #import library: 
    import datetime
    import numpy as np
    
    #make an assertion that the date_time variable must be an array for the function to continue: 
    assert isinstance(date_time, np.ndarray), 'date_time should be an array'

    #set year and month 2D time arrays that correspond to the year and month at which swh data point was collected (time series indice array for year and month)
    years = np.array([y.year for y in date_time])
    months = np.array([m.month for m in date_time])

    #initialize the dictionary that will hold all the resulting monthly mean, std, median, and nobs data
    monthly_data = {}
    monthly_data = {'time': [], 'mean': [], 'median': [],'std': [],'N': [] }
    
    #initialize a year loop that will go through years 1993 to 2016 by using the unique function on the years and month vector (np.unique outputs once the values in the year variable that appear several times)
    for year in np.unique(years):
        for month in np.unique(months):
            
            #initialize the indices where the years vector elements are equal to the year value and the indices where the months vector elements are equal to the month value. Then using the two boolean matrices, find the indices where both are true (outputs one month from one year)
            ind_year = years == year 
            ind_month = months == month
            ind = ind_year*ind_month
            
            #case 1: fill values are NaNs
            if fill_val == 'NaN':
                #apply indice to swh and time arrays and calculate mean, std, median, and nobs using a try block (the try block will run a  block of code until an error occurs or the block of code is complete. If an error occurs, the code stops and is transfered down to the except block) 
                try:
                    #grab data and time steps from the specified month of the specificed year
                    tmp = data[ind,:,:]
                    time = date_time[ind]
                    #set delta time variable so that each time averaged data from a given month is saved in the dictionary there is a corresponding time step for the month which is averaged
                    delta_t = datetime.timedelta(seconds=np.mean([(t-time[0]).total_seconds() for t in time]))
                    monthly_data['time'].append(time[0] + delta_t)
                    #compute mean, std, median, and nobs for the month at each grid point in the 2D array while ignoring nan values
                    monthly_data['mean'].append(np.nanmean(tmp, axis=0))
                    monthly_data['median'].append(np.nanmedian(tmp, axis=0))
                    monthly_data['std'].append(np.nanstd(tmp, axis=0))
                    #monthly_data['N'].append(np.size(tmp[~np.isnan(tmp)]))
                    monthly_data['N'].append(tmp.count(axis=0))
                except: pass
                    
            #case 2: fill values are masked values
            elif fill_val == 'mask':
                #apply indice to swh and time arrays and calculate mean, std, median, and nobs using a try block (the try block will run a  block of code until an error occurs or the block of code is complete. If an error occurs, the code stops and is transfered down to the except block) 
                try:
                    #grab data and time steps from the specified month of the specificed year
                    tmp = data[ind,:,:]
                    time = date_time[ind]
                    #set delta time variable so that each time averaged data from a given month is saved in the dictionary there is a corresponding time step for the month which is averaged
                    delta_t = datetime.timedelta(seconds=np.mean([(t-time[0]).total_seconds() for t in time]))
                    monthly_data['time'].append(time[0] + delta_t)
                    #compute mean, std, median, and nobs for the month at each grid point in the 2D array while ignoring nan values
                    monthly_data['mean'].append(np.ma.mean(tmp, axis=0))
                    monthly_data['median'].append(np.ma.median(tmp, axis=0))
                    monthly_data['std'].append(np.ma.std(tmp, axis=0))
                    monthly_data['N'].append(tmp.count(axis=0))
                except: pass

    return monthly_data
