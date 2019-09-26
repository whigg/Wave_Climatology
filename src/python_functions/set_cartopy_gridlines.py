def grid_labels_lines(ax, xticks, yticks, fontsize, linewidth, color, alpha, linestyle, task):
    
    """
    grid_labels_lines(ax, xticks, yticks, fontsize, linewidth, color, alpha, linestyle, task)
    
    Function for placing x and y axes tick marks for longitude and latitude respectively
        
        Parameters 
        ----------
        ax : geospatial axes for the subplot (cartopy object)
               e.g. fig, axes = plt.subplots(3, 2, figsize=(16,12),
                        subplot_kw={'projection': projection})
                    ax1, ax2, ax3, ax4, ax5, ax6 = axes.flatten() 
        xticks : list of longitudinal tick marks 
               e.g. xticks = [0, 60, 120, 180, -120, -60, -0]
        yticks : list of latitudinal tick marks
               e.g. yticks = [-60, -30, 0, 30, 60]
        fontsize : Specifies the size of the tickmarks on the x and y axes 
               e.g. fontsize = 20
        linewidth, color, alpha, linestyle : all specifications for what the gridlines will look like 
        
        task : specifies if grid lines should be plotted or not. Options for tsk include: 
               e.g. task = 'grid on' or task = 'grid off'
               
        Returns
        -------
        plots with gridline and and tick marks on the left and bottom axes 
        
        Libraries necessary to run function
        -----------------------------------
        import cartopy.crs as ccrs
        import cartopy.mpl.ticker as cticker
    
    
    """
    #import libraries: 
    import cartopy.crs as ccrs
    import cartopy.mpl.ticker as cticker
    
    #set x and y tick labels
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_xticklabels(xticks, fontsize=fontsize)
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    ax.set_yticklabels(yticks, fontsize=fontsize)

    #make the labels have degrees 
    lon_formatter = cticker.LongitudeFormatter()
    lat_formatter = cticker.LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    
    #case 1: place gridlines on map
    if task == 'grid on': 
        
        ax.grid(linewidth=linewidth, color=color, alpha=alpha, linestyle=linestyle)
