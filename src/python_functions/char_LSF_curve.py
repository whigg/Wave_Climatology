def character_LSF(data, model, x_solution, trend, parameters, fill_val):
    
    """
    character_LSF(data, model, x_solution, trend, parameters, fill-val)
    
        Function to compute the unweighted least square fit Characteristics 
        
        Parameters 
        ----------
        data : numpy 2D array of temporal data
               e.g. print(data.shape) => (133,) 
        model : Least square fit model computed using temporal data
        x_solution : x solutions from the matrix equation Ax = b
        trend : type of function least square is fitting. Options for this variables include: 
               a) trend = 'linear'
               b) trend = 'exponential'
               c) trend = 'sinusoidal' 
        parameters : number of parameters in model 
               a) if trend = 'linear', then options for parameters includes: 
                    i) parameters = 1 : fits mean 
                    ii) parameters = 2 : fits mean and linear trend 
               b) if trend = 'exponential', then the only option for paramters includes: 
                    i) parameters = 2: fits linear trend and mean offset to a linearized exponential equation 
               c) if trend = 'sinusiodal', then options for paramters includes: 
                    i) parameters = 3 : fits mean, and annual cycle (period = 1 year, 12 months, or 365.25 days)
                    ii) parameters = 4 : fits mean, linear trend, and annual cycle
                    iii) parameters = 5 : fits mean, annual cycle, and semi-annual cycle (period= 1/2 year,6 months,182.625 days)
                    iv) paramters = 6: fits mean, linear trend, annual cycle, and semi-annual cycle 
        fill_val : determines what fill value is present in your data set. Options include:
               a) fill_val = 'NaN' 
               b) fill_val = 'mask'
        
        
        Returns
        -------
        rms : Root mean square error of least square fit (rough estimate of how well the model fits the data) 
        amp1 : Amplitude of the Annual Cycle 
        phase1 : Phase Constant of the Annual Cycle 
        amp2 : Amplitude of the Semi-annual Cycle
        phase2 : Phase Constant of the Semi-annual Cycle
        cod : Coefficient of determination (robust way of determining the goodness of fit of the model)
        
        Libraries necessary to run function
        -----------------------------------
        Numpy : import numpy as np
    """
    #import library:
    import numpy as np
    
    #consider for LSF only unmasked or non-nan data: 
    if fill_val == 'mask':
        ind = ~data.mask
    elif fill_val == 'NaN':
        ind = ~np.isnan(data)
        
    #apply to data set: 
    data_c = data[ind]
    
    #set conditional statements for each case that the lsf will be applied: 
    if trend == 'linear':
        
        #set the two cases for the linear trend parameters: 
        if parameters == 1: 
            #calcluate characteristics from model:
            #residual: 
            residual  = data_c - model 
            #root mean square error: 
            rms = np.sqrt(np.mean((residual)**2))
            #Annual cycle amplitude:
            amp1 = 'None'
            #Annual cycle phase constant: 
            phase1 = 'None'
            #semi-annual cycle amplitude: 
            amp2 = 'None'
            #semi-annual cycle phase constant: 
            phase2 = 'None'
            #coefficient of determination: 
            cod = 1 - (np.sum((residual)**2)/np.sum((data_c - np.mean(data_c))**2))
            
        elif parameter == 2: 
            #calcluate characteristics from model:
            #residual: 
            residual  = data_c - model 
            #root mean square error: 
            rms = np.sqrt(np.mean((residual)**2))
            #Annual cycle amplitude:
            amp1 = 'None'
            #Annual cycle phase constant: 
            phase1 = 'None'
            #semi-annual cycle amplitude: 
            amp2 = 'None'
            #semi-annual cycle phase constant: 
            phase2 = 'None'
            #coefficient of determination: 
            cod = 1 - (np.sum((residual)**2)/np.sum((data_c - np.mean(data_c))**2))
            
    
    elif trend == 'exponential':
        
        #set the two cases for the linear trend parameters: 
        if parameters == 2: 
           #calcluate characteristics from model:
            #residual: 
            residual  = data_c - model 
            #root mean square error: 
            rms = np.sqrt(np.mean((residual)**2))
            #Annual cycle amplitude:
            amp1 = 'None'
            #Annual cycle phase constant: 
            phase1 = 'None'
            #semi-annual cycle amplitude: 
            amp2 = 'None'
            #semi-annual cycle phase constant: 
            phase2 = 'None'
            #coefficient of determination: 
            cod = 1 - (np.sum((residual)**2)/np.sum((data_c - np.mean(data_c))**2))
        
    elif trend == 'sinusoidal':
        
        #set the two cases for the linear trend parameters: 
        if parameters == 3: 
            #calcluate characteristics from model:
            #residual: 
            residual  = data_c - model 
            #root mean square error: 
            rms = np.sqrt(np.mean((residual)**2))
            #annual cycle amplitude: 
            amp1 = np.sqrt((x_solution[1]**2) + (x_solution[2]**2))
            #annual cycle phase constant: 
            phase1 = np.arctan2(x_solution[1],x_solution[2])
            #semi-annual cycle amplitude: 
            amp2 = 'None'
            #semi-annual cycle phase constant: 
            phase2 = 'None'
            #coefficient of determination: 
            cod = 1 - (np.sum((residual)**2)/np.sum((data_c - np.mean(data_c))**2))
            
        elif parameters == 4: 
            #calcluate characteristics from model:
            #residual: 
            residual  = data_c - model 
            #root mean square error: 
            rms = np.sqrt(np.mean((residual)**2))
            #annual cycle amplitude: 
            amp1 = np.sqrt((x_solution[2]**2) + (x_solution[3]**2))
            #annual cycle phase constant: 
            phase1 = np.arctan2(x_solution[2],x_solution[3])
            #semi-annual cycle amplitude: 
            amp2 = 'None'
            #semi-annual cycle phase constant: 
            phase2 = 'None'
            #coefficient of determination: 
            cod = 1 - (np.sum((residual)**2)/np.sum((data_c - np.mean(data_c))**2))
            
        elif parameters == 5:
            #calcluate characteristics from model:
            #residual: 
            residual  = data_c - model 
            #root mean square error: 
            rms = np.sqrt(np.mean((residual)**2))
            #annual cycle amplitude: 
            amp1 = np.sqrt((x_solution[1]**2) + (x_solution[2]**2))
            #annual cycle phase constant: 
            phase1 = np.arctan2(x_solution[1],x_solution[2])
            #semi-annual cycle amplitude: 
            amp2 = np.sqrt((x_solution[3]**2) + (x_solution[4]**2))
            #semi-annual cycle phase constant: 
            phase2 = np.arctan2(x_solution[3],x_solution[4])
            #coefficient of determination: 
            cod = 1 - (np.sum((residual)**2)/np.sum((data_c - np.mean(data_c))**2))
            
        elif parameters == 6: 
            #calcluate characteristics from model:
            #residual: 
            residual  = data_c - model 
            #root mean square error: 
            rms = np.sqrt(np.mean((residual)**2))
            #Annual cycle amplitude: 
            amp1 = np.sqrt((x_solution[2]**2) + (x_solution[3]**2))
            #Annual Cycle phase constant: 
            phase1 = np.arctan2(x_solution[2],x_solution[3])
            #semi-annual cycle amplitude: 
            amp2 = np.sqrt((x_solution[4]**2) + (x_solution[5]**2))
            #semi-annual cycle phase constant: 
            phase2 = np.arctan2(x_solution[4],x_solution[5])
            #coefficient of determination: 
            cod = 1 - (np.sum((residual)**2)/np.sum((data_c - np.mean(data_c))**2))
    
    return rms, amp1, phase1, amp2, phase2, cod
