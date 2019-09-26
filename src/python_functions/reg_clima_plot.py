def region_clima_plot(ax, swh_mean, swh_stdm, swh_hfit, wsp_mean, wsp_stdm, wsp_hfit, swh_model_mean, swh_model_stdm, wsp_model_mean, wsp_model_stdm, time, time_ticks, xlim, ylim, subplot_label, fontsize, task):
    
    """
    region_clima_plot(ax, swh_mean, swh_stdm, swh_hfit, wsp_mean, wsp_stdm, wsp_hfit, swh_model_mean, swh_model_stdm, wsp_model_mean, wsp_model_stdm, time, xlim, ylim, subplot_label, task):
    
        Function for plotting regional climatologies for each subplot
        
        Parameters 
        ----------
        ax : geospatial axes for the subplot (cartopy object)
               e.g. fig, axes = plt.subplots(3, 2, figsize=(16,12),
                        subplot_kw={'projection': projection})
                    ax1, ax2, ax3, ax4, ax5, ax6 = axes.flatten() 
        swh_mean : Ifremer SWH regional climatology mean
        swh_stdm : Ifremer SWH regional climatology standard deviation of the mean
        swh_hfit : Ifremer SWH regional climatology model 
        wsp_mean : CCMP v2 regional climatology mean
        wsp_stdm : CCMP v2 regional climatology standard deviation of the mean
        wsp_hfit : CCMP v2 regional climatology model
        swh_model_mean : WW3 swh regional climatology mean
        swh_model_stdm : WW3 swh regional climatology standard deviation of the mean
        wsp_model_mean : WW3 wsp regional climatology mean
        wsp_model_stdm : WW3 wsp regional climatology standard deviation of the mean
        time : time vector for plotting regional climatologies 
            e.g. time = np.arange(0,13)
        time_ticks : tick_marks for subplot 
            e.g. time_ticks = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        xlim : x_axis limits 
            e.g xlim = [0,13]
        ylim : y axis lims for both axes in the form of a list: 
                ylim = [[swh_limits], [wsp_limits]]
            e.g. ylim = [[1,4], [6, 10]]
        subplot_label : subplot label for paper 
            e.g. subplot_label = 'A'
        fontsize : Specifies the size of the x and y tickmarks as well as the x and y axes labels. 
            e.g. fontsize = 15
        task : Specifies whether the plot will be displaying WW3, Ifremer, and CCMP2 comparision, Ifremer and CCMP2 climatology only with models, or residual of SWH with CCMP2 climatology. Options include:
            e.g. task = 'ww3' or task = 'IC' or task = 'residual' or task = 'chi'
        
               
        Returns
        -------
        plots regional climatology subplot from specific region 
        
        Libraries necessary to run function
        -----------------------------------
        import numpy as np
        import matplotlib.pyplot as plt
    
    """
    
    #import libraries: 
    import numpy as np
    import matplotlib.pyplot as plt
    import cartopy_fig_module as cart

    #SWH axis: 
    ax_twin = ax.twinx()

    #set color of left axis:
    color = 'tab:blue'
    ax_twin.tick_params(axis='y', labelcolor=color)

    if task == 'ww3':

        #plot WW3
        ax_twin.plot(time, swh_model_mean, 'k-')
        ax_twin.fill_between(time, swh_model_mean - swh_model_stdm, swh_model_mean + swh_model_stdm, 
                             color='black', alpha = 0.3)  
        #Plot Ifremer SWH
        ax_twin.plot(time, swh_mean, 'b-')
        ax_twin.fill_between(time, swh_mean - swh_stdm, swh_mean + swh_stdm, 
                             color=color, alpha = 0.3)
    elif task == 'IC':

        #Plot Ifremer SWH
        ax_twin.plot(time, swh_mean, 'b-')
        ax_twin.plot(time, swh_hfit, 'b--')
        ax_twin.fill_between(time, swh_mean - swh_stdm, swh_mean + swh_stdm, 
                             color=color, alpha = 0.3) 
    elif task == 'residual':
        
        #Compute residual 
        res_swh = swh_hfit - swh_mean
        #Plot Ifremer SWH residual
        ax_twin.plot(time, res_swh, 'b-')
        ax_twin.fill_between(time, 0, res_swh, facecolor='blue', alpha=0.2)

    elif task == 'chi':
        
        #Compute chi squared stat 
        chi_swh = (swh_hfit - swh_mean)/swh_stdm
        #Plot Ifremer SWH residual
        ax_twin.plot(time, chi_swh, 'b-')
        ax_twin.fill_between(time, 0, chi_swh, facecolor='blue', alpha=0.2)
        
    #set subplot attributes: 
    if task == 'residual':
        ax_twin.set_ylabel('Residual SWH [m]', color=color, fontsize=fontsize)
    else:
        ax_twin.set_ylabel('SWH [m]', color=color, fontsize=fontsize)
        
    ax_twin.set_ylim(ylim[0])
    ax_twin.tick_params(axis="y", labelsize=fontsize)
    ax_twin.grid(color=color, linestyle='-.', linewidth=1, alpha = 0.2)

    #WSP axis:

    #set color:
    color = 'tab:red'
    ax.tick_params(axis='y', labelcolor=color)

    if task == 'ww3':
        #plot WW3 WSP
        ax.plot(time, wsp_model_mean, color = 'tab:purple')
        ax.fill_between(time, wsp_model_mean - wsp_model_stdm, wsp_model_mean + wsp_model_stdm, 
                        color='tab:purple', alpha = 0.3)
        #plot CCMP2 WSP
        ax.plot(time, wsp_mean, 'r-')
        ax.fill_between(time, wsp_mean - wsp_stdm, wsp_mean + wsp_stdm, 
                        color=color, alpha = 0.3)
    else:

        #plot CCMP2 WSP
        ax.plot(time, wsp_mean, 'r-')
        ax.plot(time, wsp_hfit, 'r--')
        ax.fill_between(time, wsp_mean - wsp_stdm, wsp_mean + wsp_stdm, 
                        color=color, alpha = 0.3)
        
    #set attributes of subplot: 
    ax.set_xlim([0, 13])
    ax.set_xticklabels(time_ticks, fontsize=fontsize)
    ax.tick_params(axis="x", labelsize=fontsize)
    #hind every other ticklabel
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start+1, end+1, 1))
    for label in ax.xaxis.get_ticklabels()[::2]:
        label.set_visible(False)

    ax.set_ylabel('WSP [m/s]', color=color, fontsize=fontsize)
    ax.set_ylim(ylim[1])
    ax.tick_params(axis="y", labelsize=fontsize)
    #set gridlines
    ax.grid(color=color, linestyle='-.', linewidth=1, alpha = 0.2)
    #set labels on figure
    cart.subplot_label(ax, xdist_label = 0.08, ydist_label = 0.94, 
                       subplot_label = subplot_label, fs_shade = 28, fs_main = 12)
    #cart.subplot_label(ax_twin, xdist_label = 0.58, ydist_label = 0.94, 
    #                   subplot_label = 'Lat:''%s' %grid_cor[0] + ' to ' + '%s' %grid_cor[1] + '  ' + 'Lon:' + '%s' %grid_cor[2] + ' to ' + '%s' %grid_cor[3] , fs_shade = 28, fs_main = 8)

