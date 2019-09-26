#!/usr/bin/env python
# coding: utf-8

# # Ifremer Product 1  Altimeter SWH and WSP data binning from Jan 1st, 1993 to Dec 31st, 2016 following bia's method of binning 

# Use the sys library in order to tell the notebook to look for files within the followinf directory path: 

# In[1]:


import sys
sys.path.append('/zdata/home/lcolosi/python_functions/')


# Import libraries and my functions 

# In[2]:


#Libraries
import numpy as np 
from datetime import datetime, timedelta 
import glob
from netCDF4 import Dataset, num2date, date2num

#My functions 
#from binning_along_track_data_bia_method import bin_along_track_sat
from save_binned_ifremer_p1_swh import save_netcdf_swh
from save_binned_ifremer_p1_wsp import save_netcdf_wsp


# Call Ifremer Product 1 data from the server using glob from January 1st, 1993 to December 31st, 2015 and sort them numerically with the sort function

# In[3]:


filenames = sorted(glob.glob('/zdata/downloads/Ifremer/altimeter_data/*.nc'))


# Recall the orientation of the Ifremer longitude and latitude: 
# 
# 1) longitude : -180 to 180 degrees east  
# 
# 2) latitude : -90 to 90 degrees north 

# Set the following geospatial dimensions for the binning process:
# 
# 1) grid size (regular_grid) : size of grid boxes or resolution 
# 
# 2) length of longitude and latitude (nlon, nlat) : length of lon and lat normalized by the size of the grid box size 
# 
# 3) grid (grid_lon, grid_lat) : longitude and latitude vectors
# 
# 4) length of time series

# In[4]:


regular_grid = 1.
nlon, nlat = int(360./regular_grid), int(180./regular_grid)
grid_lat, grid_lon = np.arange(-90,90,regular_grid), np.arange(0,360,regular_grid)
nt = 8766


# Initialize a dictionary to save the daily data into

# In[5]:


data_base = {}


# Initialize key variables in the dictionary for: 
# 
# 1) Corrected Altimeter swh 
# 
# 2) Corrected Altimeter wsp 
# 
# 3) Number of observations at each grid point 
# 
# as masked arrays

# In[6]:


data_base['swh'] = np.ma.zeros([nlat,nlon])
data_base['swhcor'] = np.ma.zeros([nlat,nlon])
data_base['wspcor'] = np.ma.zeros([nlat,nlon])
data_base['time'] = np.ma.array(nt)
data_base['lat'] = grid_lat
data_base['lon'] = grid_lon
data_base['N'] = np.ma.zeros([nlat,nlon])


# Initialize data to be saved in a 3D array

# In[7]:


swh_array = np.ma.masked_all([nt, nlat, nlon])
swhcor_array = np.ma.masked_all([nt, nlat, nlon])
wspcor_array = np.ma.masked_all([nt, nlat, nlon])
time_array = []


# Loop through filenames in order to bin each daily data file

# In[8]:


#set day counter 
c = 0
    
for f in filenames:
    
    #initialize dictionary for each file I loop through: 
    data_base = {}
    data_base['swh'] = np.ma.zeros([nlat,nlon])
    data_base['swhcor'] = np.ma.zeros([nlat,nlon])
    data_base['wspcor'] = np.ma.zeros([nlat,nlon])
    data_base['time'] = np.ma.array(nt)
    data_base['lat'] = grid_lat
    data_base['lon'] = grid_lon
    data_base['N'] = np.ma.zeros([nlat,nlon]) 
    #initialize nc variable:
    nc = Dataset(f,'r')
    #call data 
    swh = nc.variables['swh'][:]
    swhcor = nc.variables['swhcor'][:]
    wspcor = nc.variables['wind_speed_cor'][:]
    lat = nc.variables['lat'][:]
    lon = nc.variables['lon'][:]
    #take all longitude values less than zero and add 360 to them in order to place all grid point on the opposite side of the data set 
    lon[lon<0] = lon[lon<0] + 360
    #set date for day binning 
    #call time data
    time = num2date(nc.variables['time'][:], nc.variables['time'].units) 
    #loop through all time steps in along track data and simplify the data_time step to just the date (remove hours minutes, seconds)
    days = np.array([t.date() for t in time])
    #obtain the unique day time step
    day = np.unique(days)[0]
    
    #loop through each along track data point: 
    for i in range(len(swh)):
        
        #set indices for lon and lat:
        indlat = np.abs(grid_lat - lat[i]).argmin()
        indlon = np.abs(grid_lon - lon[i]).argmin()
        #apply indices to data: 
        data_base['swh'][indlat, indlon] += swh[i] # += adds the values following and reinitialize the variable such that it is equal to the new value 
        data_base['swhcor'][indlat, indlon] += swhcor[i]
        data_base['wspcor'][indlat,indlon] += wspcor[i]
        data_base['N'][indlat, indlon] += 1
        
    #take the average of data points that have been summed together on the same grid point
    N = np.ma.masked_where(data_base['N'] == 0, data_base['N'])
    swh_bin = np.ma.masked_where(data_base['N'] == 0, data_base['swh'])/N
    swhcor_bin = np.ma.masked_where(data_base['N'] == 0, data_base['swhcor'])/N
    wspcor_bin = np.ma.masked_where(data_base['N'] == 0, data_base['wspcor'])/N
    
    #save the data in a 3D array: 
    swh_array[c,:,:] = swh_bin
    swhcor_array[c,:,:] = swhcor_bin
    wspcor_array[c,:,:] = wspcor_bin
    t0 = datetime(day.year,day.month,day.day,0,0)
    time_array.append([t0])
    N_array = N

    #set counter 
    c += 1
    print(f)


# In[9]:


print(time_array)


# Save Data into a netCDF file

# In[10]:


save_netcdf_swh(swh = swhcor_array, lon = grid_lon, lat = grid_lat, time = time_array, output = '/zdata/downloads/colosi_data_bk/binned_data/ifremer_p1_daily_data/my_daily_binned_ifremer_data/ifremer_swh_daily_binned_data_93_16_bia.nc')
save_netcdf_wsp(wsp = wspcor_array, lon = grid_lon, lat = grid_lat, time = time_array, output = '/zdata/downloads/colosi_data_bk/binned_data/ifremer_p1_daily_data/my_daily_binned_ifremer_data/ifremer_wsp_daily_binned_data_93_16_bia.nc')


#  

#  

#  

# ### Development Code: 

#  

#  

#  

# In[12]:


nc = Dataset(filenames[0],'r')
time = num2date(nc.variables['time'][:], nc.variables['time'].units) 
#loop through all time steps in along track data and simplify the data_time step to just the date (remove hours minutes, seconds)
days = np.array([t.date() for t in time])
print(time)
print(days)


# In[18]:


print(grid_lat)
print(grid_lat - (-60))
print(np.abs(grid_lat - (-60)))
print(np.abs(grid_lat - (-60)).argmin())
print(np.abs(grid_lat - 39.4)[130],grid_lat[129])


# In[22]:


0.4<0.6


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




