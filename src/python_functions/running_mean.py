def running_mean(data, k_dim, task, fill_val):
    
    """
    running_mean(data, k_dim, task, fill_val)
    
        Function for computing the running mean of any given data set with any dimensions
        
        Parameters 
        ----------
        data : numpy array of any 2d or 1d dimensional size. If the data set is 1d (i.e. data.shape => (ndim,)), then the data must be a column vector. 
               e.g. columen vector, row vector, 2d array
        k_dim : dimensions of the kernal matrix (window matrix) in list format. If the data set is 1d, the kernal dimension must be k_dim = [ndim,1] such that the kernal matrix will slide down the coloumn vector 
               e.g. k_dim = [4, 4]
        task : specifies the purpose of the box car filter. Options for this input include: 
               task = 'running_mean' => used for smoothing out data sets  
               task = 'deresolve' => used for being down the resolution of a data set or image
        fill_val : specifies if the array has filled values for continents. Options include: 
               fill_val = 'nan' or fill_val = 'mask' or fill_val = 'none'        
        Returns
        -------
        data_rm : 2D numpy array of running mean averaged data for given window
        
        Libraries necessary to run function
        -----------------------------------
        Scipy: from scipy import signal
        Numpy: import numpy as np
    """
    
    #import libraries
    from scipy import signal
    import numpy as np
    
    #create Kernal matrix:
    w = np.ones((k_dim[0],k_dim[1]))
    #normalize Kernal matrix:
    w_norm = w/np.sum(w)
    
    #case 1: fill_val is masked: 
    if fill_val == 'mask':
        ind_mask = np.ma.getmask(data)
        data[ind_mask] = 0
    #case 2: fill_val is nan:
    elif fill_val == 'nan':
        ind_nan = ~np.nan.nonzero(data)
        data[ind_nan] = 0

    #case 1: 1d convolution: 
    if k_dim[1] == 1:
        #flatten both data and w_norm to make sure that they are 1d arrays:
        w_norm = w_norm.flatten()
        data = data.flatten()
        #convolve data and kernal matrix: 
        w_conv = np.convolve(data,w_norm)
        #case 1: deresolve
        if task == 'deresolve':
            #extract lower resolution averaged elements in w_conv matrix: 
            data_rm = w_conv[(k_dim[0]-1)::k_dim[0]]
        #case 2: running mean
        elif task == 'running_mean':
            #extract running mean elements in w_conv matrix: 
            data_rm = w_conv[(k_dim[0]-1):len(w_conv)-k_dim[0]+1]
        
        
    #case 2: 2d convolution
    elif k_dim[0] > 1:
        #convolve data and kernal matrix: 
        w_conv = signal.convolve2d(data,w_norm)
        w_row, w_coln = w_conv.shape
        #case 1: deresolve
        if task == 'deresolve':
            #extract lower resolution averaged elements in w_conv matrix: 
            data_rm = w_conv[(k_dim[0]-1)::k_dim[0],(k_dim[1]-1)::k_dim[1]]
        #case 2: running mean
        elif task == 'running_mean':
            rdata, cdata = data.shape
            #extract running mean elements in w_conv matrix: 
            data_rm = w_conv[(k_dim[0]-1):w_row-k_dim[0]+1,(k_dim[1]-1):w_coln-k_dim[1]+1]
    
     #set fill_val back to mask or nan values:
    if fill_val == 'mask':
        data_rm = np.ma.masked_equal(data_rm, 0)
    elif fill_val == 'nan':
        data_rm[ind_nan] = nan

    return data_rm #,w_conv 

