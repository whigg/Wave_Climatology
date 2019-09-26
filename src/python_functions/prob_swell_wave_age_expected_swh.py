def prob_swell(data, observed_swh, date_time, task):
    
    """
    prob_swell(wave_age, expected_swh)
    
        Function for calculating the probability of swell from either wave age or expected SWH (wind-wave relaionship method). 
        
        Parameters 
        ----------
        Data : Can be two types of data: 
                wave_age : numpy masked array of geospatial maps of wave age which is defined as the stage of development of a wave and 
                           mathematically as wave_age = c_p/U_10 where c_p is peak phase speed (c_p = 2*pi*f_p = 2*pi*T_p for lambda << h (deep water waves) and f_p = peak frequency) 
                           and U_10 is wind speed 10 meters above the surface of the ocean. 
                             e.g : wave_age.shape = (8766, 133, 360)
                           If I am using wave age to compute probability of swell, set expected_swh = 'none'
                expected_swh : numpy masked array of geospatial maps of expected swh computed from wind-wave relationship
                             e.g : expected_swh.shape = (8766, 133, 360)
                               If I am using expected_swh to compute probability of swell, set wave_age = 'none'
        date_time : date_time numpy array with time series for data set
        task : specifies whether the probability of swell is computed seasonally or over the entire time series. Options include: 
                     e.g : task = 'seasonally' or task = 'all_time'
        
        Returns
        -------
        prob_swell : Dictionary 2D numpy masked array(s) (geospatial map(s)) of probability of swell which is defined as: 
                     e.g : P_swell = N_swell/N_total where N_swell = number of swell events (when wave age surpasses 1.2) 
                                                           N_wind = number of wind events (when wave age is below or equal to 1.2)
                                                           N_total = N_swell + N_wind
        
        Libraries necessary to run function
        -----------------------------------
        import numpy as np
    
    """
    
    #import libraries
    import numpy as np
    
    #create prob_swell dictionary 
    prob_swell = {}
    prob_swell = {'p_swell': [], 'p_wind': []}
        
    #Case 1: compute prob of swell for entire time series
    if task == 'all_time':

        #Case 1: Compute Probability of swell with wave age
        if observed_swh == 'none':

            #create a boolean matrix of true or false values for wave age surpassing 1.2
            swell_ind = data > 1.2
            wind_ind = data <= 1.2

        #Case 2: Compute Probability of Swell with expected_swh 
        elif observed != 'none': 

            #create a boolean matrix of true or false values for wave age surpassing 1.2
            swell_ind = data > observed_swh
            wind_ind = data <= observed_swh

        #count the number of True boolean values that are in each boolean array for swell events and wind_sea events 
        N_swell = np.sum(swell_ind, axis=0)
        N_wind = np.sum(wind_ind, axis=0)
        N_total = N_swell + N_wind

        #Compute probability of swell
        p_swell = N_swell/N_total

        #append 
        prob_swell['p_swell'].append(p_swell)

    #Case 2: compute prob of swell seasonally 
    elif task == 'seasonally':

        #set year and month 2D time arrays that correspond to the month at which swh data point was collected (time series indice array for month)
        months = np.array([m.month for m in date_time])

        #loop through time series to call months for each season: DJF, MAM, JJA, SON:
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

            #call wave age or expected swh data from season
            data_s = data[ind]
            
            #Case 1: Compute Probability of swell with wave age
            if observed_swh == 'none':

                #create a boolean matrix of true or false values for wave age surpassing 1.2
                swell_ind = data_s > 1.2
                wind_ind = data_s <= 1.2

            #Case 2: Compute Probability of Swell with expected_swh 
            elif observed_swh != 'none': 

                #call observed swh data from season:
                observed_swh_s = observed_swh[ind]
                
                #create a boolean matrix of true or false values for wave age surpassing 1.2
                swell_ind = data_s > observed_swh
                wind_ind = data_s <= observed_swh

            #count the number of True boolean values that are in each boolean array for swell events and wind_sea events 
            N_swell = np.sum(swell_ind, axis=0)
            N_wind = np.sum(wind_ind, axis=0)
            N_total = N_swell + N_wind

            #Compute probability of swell
            p_swell = N_swell/N_total
            p_wind = 1 - p_swell

            #append to key variables in prob_swell:
            prob_swell['p_swell'].append(p_swell)
            prob_swell['p_wind'].append(p_wind)
