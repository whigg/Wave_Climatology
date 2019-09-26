def set_grid_labels(ax,xticks,yticks, xgrid, ygrid, fontsize, color):
    
    """
    set_grid_labels(ax,xticks,yticks, xgrid, ygrid, fontsize, color)
    
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
        xgrid : displaying latitude gridlines with boolean of either true or false where true means there are xgrid lines
               e.g. xgrid = True or xgrid = False
        ygrid : displaying longitude gridlines with boolean of either true or false where true means there are ygrid lines
               e.g. xgrid = True or xgrid = False
        fontsize : Specifies the fontsize of the x and y tickmarks
        color : Specifies color of tickmarks and gridlines
               
        Returns
        -------
        plots with gridline and and tick marks on the left and bottom axes 
        
        Libraries necessary to run function
        -----------------------------------
        import cartopy.crs as ccrs
        from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
        import matplotlib.ticker as mticker
        
    """
    
    import cartopy.crs as ccrs
    from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
    import matplotlib.ticker as mticker
    
    grd = ax.gridlines(crs=ccrs.PlateCarree(central_longitude=0.0), draw_labels=True, linewidth=2, color=color, alpha=0.3, linestyle='--')
    grd.xlabels_top = False 
    grd.ylabels_right = False 
    grd.xlines = xgrid
    grd.ylines = ygrid
    grd.xlocator = mticker.FixedLocator(xticks)
    grd.ylocator = mticker.FixedLocator(yticks)
    grd.xformatter = LONGITUDE_FORMATTER
    grd.yformatter = LATITUDE_FORMATTER
    grd.xlabel_style = {'size': fontsize, 'color': color}
    grd.ylabel_style = {'size': fontsize, 'color': color}
    
    return

def set_axes_label(ax, xdist_lat, ydist_lat, xdist_lon, ydist_lon, fontsize):
    
    """
    set_axes_label(ax, xdist_lat, ydist_lat, xdist_lon, ydist_lon, fontsize)
    
        Function for placing x and y axes labels for longitude and latitude respectively
        
        Parameters 
        ----------
        ax : geospatial axes for the subplot (cartopy object)
               e.g. fig, axes = plt.subplots(3, 2, figsize=(16,12),
                        subplot_kw={'projection': projection})
                    ax1, ax2, ax3, ax4, ax5, ax6 = axes.flatten() 
        xdist_lat : horizontal distance from plot for latitude label
               e.g. xdist_lat = -0.1
        ydist_lat : vertical distance for latitude label referenced from bottom of figure 
               e.g. yticks = 0.50
        xdist_lon : horizontal distance for longitude label referenced from right side of figure 
               e.g. xdist_lon = 0.5
        ydist_lon : vertical distance from the plot for longitude label 
               e.g. ydist_lon = -0.25
        fontsize : font size of label 
        
               
        Returns
        -------
        plots with axes labels on the left and bottom axes 
        
        Libraries necessary to run function
        -----------------------------------
        import cartopy.crs as ccrs
        
    """
    
    ax.text(xdist_lat, ydist_lat, 'Latitude', va='bottom', ha='center',
        rotation='vertical', rotation_mode='anchor',
        transform=ax.transAxes, fontsize=fontsize)
    ax.text(xdist_lon, ydist_lon, 'Longitude', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes, fontsize=fontsize)
    
    return
    
def subplot_label(ax, xdist_label, ydist_label, subplot_label, fs_shade, fs_main):
    
    """
    subplot_label(ax, xdist_label, ydist_label, subplot_label, fs_shade, fs_main)
    
        Function for placing subplot labels on subplots for figures that will be used in research papers 
        
        Parameters 
        ----------
        ax : geospatial axes for the subplot (cartopy object)
               e.g. fig, axes = plt.subplots(3, 2, figsize=(16,12),
                        subplot_kw={'projection': projection})
                    ax1, ax2, ax3, ax4, ax5, ax6 = axes.flatten() 
        xdist_label : horizontal distance from plot for latitude label
               e.g. xdist_label = 0.2
        ydist_label : vertical distance for latitude label referenced from bottom of figure 
               e.g. ydist_label = 0.8
        subplot_label : string of words for label 
               e.g. subplot_label = 'A'
        fs_shade : font size of shading label
               e.g. fs_shade = 28
        fs_main : font size of main label 
               e.g. fs_main = 18
               
        Returns
        -------
        plots with subplot labels on the left and top corner (or any disired location)
    
        Libraries necessary to run function
        -----------------------------------
        import cartopy.crs as ccrs
    
    
    """
    
    #ax.text(xdist_label, ydist_label, '%s' %subplot_label, va='center', ha='center',
    #    transform=ax.transAxes, fontsize=fs_shade, fontweight='bold', color='gray')
    ax.text(xdist_label, ydist_label, '%s' %subplot_label, va='center', ha='center',
        transform=ax.transAxes, fontsize=fs_main, 
        bbox = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=1, alpha=.8), fontweight='bold')
    
    return
    
def set_cbar(cs, cax, fig, orientation, cbar_label, nbins, fontsize, cbar_ticks, task):
    
    """
    set_cbar(cs, cax, fig, cbar_label, nbins, fontsize, cbar_ticks, task)
    
        Function for placing colorbar on a plot
        
        Parameters 
        ----------
        cs : map of data on subplot axis using cartopy projection 
               e.g. cs = ax.pcolor(lon,lat,swh_phase2_m,vmin=-np.pi,vmax=np.pi, cmap=cm.hsv, transform=ccrs.PlateCarree(central_longitude=0.0))
        cax : colorbar axis with positioning vector of the colorbar with the folowing parameters: 
               cax = plt.axes([left, bottom, width, height])
               e.g. cax = plt.axes([.47, .17, 0.01, 0.16])
        fig : fig with the colorbar will attached to (not refering to the subplots)
        orientation : Specifies if the colorbar is vertical or horizontal. Options for keyword argument includes: 
               e.g. orientation = 'horizontal' or orientation = 'vertical'
        cbar_label : colobar label in string format 
               e.g. cbar_label = '[m]'
        fontsize : font size of cbar label and tick marks
               e.g. fontsize = 10
        nbins : number of tick marks on colorbar axis 
               e.g. nbins = 5
        cbar_ticks : A list of tick marks that will be placed on colorbar (note that the number of tick mark labels must be equal to the number of bins on color bar)
               e.g. cbar_ticks = [Jun, Aug, October, Dec, Feb, Apr, June]
        task : Specifies whether the colorbar will need to be maodified with custom tick marks. Options include: 
                task = 'custom ticks' or task = 'regular'
      
        Returns
        -------
        plots with subplot labels on the left and top corner (or any disired location)
    
        Libraries necessary to run function
        -----------------------------------
        import cartopy.crs as ccrs
        from matplotlib import ticker
    
    """
    #import libraries
    from matplotlib import ticker
    
    #create colorbar for plot
    if task == 'regular':
        cbar = fig.colorbar(cs, cax=cax, orientation=orientation, extend='both')
    elif task == 'custom ticks':
        cbar = fig.colorbar(cs, cax=cax, orientation=orientation, ticks=cbar_ticks[0], extend='both')
    #set the number of tickmarks on colorbar
    tick_locator = ticker.MaxNLocator(nbins=nbins)
    cbar.locator = tick_locator
    cbar.update_ticks()
    #case 1: vertical colorbar
    if orientation == 'vertical':
        cbar.ax.set_ylabel('%s' %cbar_label, fontsize=fontsize)
        if task == 'custom ticks':
            cbar.ax.set_yticklabels(cbar_ticks[1])
    #case 2: horizontal colorbar
    elif orientation == 'horizontal':
        cbar.ax.set_xlabel('%s' %cbar_label, fontsize=fontsize)
        if task == 'custom ticks':
            cbar.ax.set_xticklabels(cbar_ticks[1])
    #set the fontsize of colorbar tickmarks
    cbar.ax.tick_params(labelsize=fontsize)
    
    return

def set_subplots(ax, projection, resolution, lon_min, lon_max, lat_min, lat_max):
    
    """
    set_subplots(ax, projection)
    
        Function for placing x and y axes labels for longitude and latitude respectively
        
        Parameters 
        ----------
        ax : geospatial axes for the subplot (cartopy object)
               e.g. fig, axes = plt.subplots(3, 2, figsize=(16,12),
                        subplot_kw={'projection': projection})
                    ax1, ax2, ax3, ax4, ax5, ax6 = axes.flatten() 
        lon_min, lon_max : minimum and maximum extent for longitude on the scale from -180 to 179 
               e.g. lon_min = -180, lon_max = 179
        lat_min, lat_max : minimum and maximum extent for latitude on the scale from -90 to 89
               e.g. lat_min = -66, lat_max = 66
        
              
        Returns
        -------
        plots with subplot labels on the left and top corner (or any disired location)
    
        Libraries necessary to run function
        -----------------------------------
        import cartopy.crs as ccrs
        from matplotlib import ticker
    
    """
    #import libraries
    import cartopy.feature as cfeature

    ax.set_extent([lon_min, lon_max, lat_min, lat_max], projection)
    ax.coastlines(resolution=resolution)
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', resolution, facecolor = 'Gray'))
    
    return

