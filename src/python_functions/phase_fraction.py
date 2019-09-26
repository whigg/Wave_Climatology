def phase_fraction(data):
    
    """
    phase_fraction(data)
    
        Function for computing the fraction of the world (coastal regions, open ocean regions, total) that experiences the wind anomaly 
        
        Parameters 
        ----------
        data : Regional histograms data of frequeny and bin boundary for Annual phase constant data for WSP using 5 parameter lsf model 
               
        Returns
        -------
        swa_map : Global map of all regions experiencing a wind anomaly with a maximum during the boreal summer in the SH (wave fields dominated by SH storms) and the austral winter in the NH (wave fields dominated by NH storms)
        swa_tot : Fraction of world ocean experiencing anomalous surface winds
        swa_coast : Fraction of world ocean closer than 550km (5 degrees of longitude) from shore experiencing anomalous surface winds
        swa_open : Fraction of world ocean further than 550km from shore experiencing anomalous surface winds
        
        Libraries necessary to run function
        -----------------------------------
        import numpy as np
    
    """
    
    #import libaries: 
    import numpy as np 
    
    #initialize variables
    swa_count = 0
    
    #loop through each partition region to compute the amount of data point that are considered anomalous
    for ireg in range(0,5,1): 
        
        #call data 
        loc = data['location'][ireg]
        freq = data['freq'][ireg]
        bins = data['bins'][ireg]
        
        #case 1: Northern Hemisphere 
        if loc == 'North_pacific' or loc == 'North_atlantic':
            
            #find bins where phase values are set by northern hemisphere storms (phase = 0 to pi/2)
            bin_lower = bins>= -np.pi
            bin_upper = bins<=(-np.pi/2)
            bin_lim = bin_lower * bin_upper
            bin_lim = bin_lim[0:len(bin_lim)-1]
            
            #apply indices to frequency data
            freq_n = freq[bin_lim]
            
            #count amount of anomalous points
            swa_count = swa_count + np.sum(freq_n)
            
        #case 2: Southern Hemisphere 
        if loc == 'Indian_ocean' or 'South_pacific' or 'South_atlantic': 
            
            #find bins where phase values are set by northern hemisphere storms (phase = 0 to pi/2)
            bin_lower = bins>= 0
            bin_upper = bins<=(np.pi/2)
            bin_lim = bin_lower * bin_upper
            bin_lim = bin_lim[0:len(bin_lim)-1]
            
            #apply indices to frequency data
            freq_n = freq[bin_lim]
            
            #count amount of anomalous points
            swa_count = swa_count + np.sum(freq_n)
    
    #find the totoal amount of observations over the world oceans for phase
    obs_tot = np.sum(data['freq'][5])
    
    #compute fraction of world oceans experiencing wind anomaly 
    swa_tot = swa_count/obs_tot
    
    return swa_tot
