def detrend(data):
    
    """
    detrend(data)
    
        Function for removing a linear trend from a multi-modal signal  
        
        Parameters 
        ----------
        data : signal you wish to detrend 
        
        Returns
        -------
        data_detrend : detrended signal
        
        Libraries necessary to run function
        -----------------------------------
        import numpy as np
        from unweighted_least_square_fit import least_square_fit
    
    """
    
    #import libraries
    import numpy as np
    from unweighted_least_square_fit import least_square_fit
    
    #detrend linear trend at grid point: 
    data_trend, x_trend = least_square_fit(data = data, trend = 'linear', parameters = 2, 
                                            period = 12, fill_val = 'mask')
    #initialize time vector and linear trend: 
    time = np.arange(1,len(data)+1,1)
    linear_trend = x_trend[1]*time
    
    #remove linear trend: 
    data_detrend = data-linear_trend
    
    return data_detrend

    
