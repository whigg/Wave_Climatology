#!/usr/bin/env python
# coding: utf-8

# # Wave Watch 3 CFSR binning wnd, hs and fp data from January 1st, 1993 to December 31st, 2016

# Plot figure within jupyter notebook

# In[1]:


#get_ipython().run_line_magic('matplotlib', 'inline')


# Use the sys library in order to tell the notebook to look for files within the followinf directory path: 

# In[2]:


import sys
sys.path.append('/zdata/home/lcolosi/python_functions/')


# Import all libraries and functions

# In[3]:


#libraries
import numpy as np #contains the major of functions used for matrix arrays  
import matplotlib.pyplot as plt # matplotlib contains functions for graphics and plot manipulation
from netCDF4 import Dataset, num2date # netCDF4 handles netCDF files
import glob 
import datetime
from scipy import signal
import cartopy.feature as cfeature
import cmocean.cm as cmo
from matplotlib import cm 

#my functions
from running_mean import running_mean
from save_binned_ww3_hs import save_netcdf_fields_ww3_hs
from save_binned_ww3_wnd import save_netcdf_fields_ww3_wsp
from save_binned_ww3_fp import save_netcdf_fields_ww3_fp
from shift_grid import shift_grid
from mean_temporal_masked_data import mean_mask_t


# Set dimensions for data of space and time which depends on the spatial orientation of the data set and the time period which the data is collected from. For the WW3 data set, we want the following data orientation: 

# In[4]:


nt, nlon, nlat = 8766, 720, 265
res_time = 8 #three 8 hour time steps in a single day 


# Call WW3 data from the server using glob from January 1st, 1993 to December 31st, 2016 and sort them numerically with the sort function.

# In[5]:


#Hs: 
filenames_hs = sorted(glob.glob('/zdata/downloads/ww3_CFSR/Hs/*.nc'))
#Wnd: 
filenames_wnd = sorted(glob.glob('/zdata/downloads/ww3_CFSR/Wnd/*.nc'))
#fp:
filenames_fp = sorted(glob.glob('/zdata/downloads/ww3_CFSR/fp/*.nc'))


# Look at the name of the key variables in one of the files: 

# In[6]:


#look at one file:
file_hs = filenames_hs[0]
file_wnd = filenames_wnd[0]
file_fp = filenames_fp[0]

#set nc variable in order to read attributes and obtained data: 
nc_hs1 = Dataset(file_hs, 'r')
nc_wnd1 = Dataset(file_wnd, 'r')
nc_fp1 = Dataset(file_fp, 'r')

#print key variables:
print(nc_hs1.variables.keys())
print('')
print(nc_wnd1.variables.keys())
print('')
print(nc_fp1.variables.keys())
print('')


# Look at the dimensions of lon, lat, and time: 

# In[7]:


#longitude
for at in nc_hs1.variables['longitude'].ncattrs():
    print("%s : %s" %(at, nc_hs1.variables['longitude'].getncattr(at)))
print('')
for at in nc_fp1.variables['longitude'].ncattrs():
    print("%s : %s" %(at, nc_fp1.variables['longitude'].getncattr(at)))
print('')
#laitude
for at in nc_hs1.variables['latitude'].ncattrs():
    print("%s : %s" %(at, nc_hs1.variables['latitude'].getncattr(at)))
print('')
for at in nc_fp1.variables['latitude'].ncattrs():
    print("%s : %s" %(at, nc_fp1.variables['latitude'].getncattr(at)))
print('')
#time 
for at in nc_hs1.variables['time'].ncattrs():
    print("%s : %s" %(at, nc_hs1.variables['time'].getncattr(at)))
print('')
for at in nc_fp1.variables['time'].ncattrs():
    print("%s : %s" %(at, nc_fp1.variables['time'].getncattr(at)))
print('')
#hs: 
for at in nc_hs1.variables['hs'].ncattrs():
    print("%s : %s" %(at, nc_hs1.variables['hs'].getncattr(at)))


# Note that the time coordinate for the WW3 data has 3 hour resolution instead of 1 day and the time series in one file extends over an entire month

# Set longitude and latitude vectors

# In[8]:


#lon = np.arange(-180,180,0.5)
lon = nc_hs1.variables['longitude'][:]
#lat = np.arange(-78,80.5,0.5)
lat = nc_hs1.variables['latitude'][:]
print(lon.shape,lat.shape)


# Set resolution of longitude and latitude. Also set the desired indices for where latitude will be truncated:

# In[9]:


dlon = abs(lon[1]-lon[0])
dlat = abs(lat[1]-lat[0])
lat_min, lat_max = -66, 66 #extend the matrix to 66 north and south for latitude 


# Loop through each of the filenames and complete the following: 
# 
# 1)Compute wind speed from wind velocity components
# 
# 2) Average each six hour time steps for each day (four time steps) 
# 
# 3)Decrease the resolution of the data from 0.5 degree to 1 degree
# 
# 4)Make sure the orientation of longitude is pacific centered and latitude ranges from -66 to 66 (both need to be done)
# 
# 5)Place land masses into data set using the Ifremer product 1 data set or cartopy
# 
# 5)Bin wsp and time data 

# Because each file is a separate day, I do not need to worry about making sure what file correspond to which day. Because each variable for hs, wind velocity components, and peak frequency are in their own files, I will need to complete these separately 

# ##### Hs: 

# In[10]:


#initialize masked array to concatinate 2d arrays directly into a 3D array:
hs_ww3_cfsr_d = np.ma.masked_all([nt, nlat, nlon])
time_d = []

#initialize counter:
i = 0
                                   
#call each data file separately from each day in order:
for f in filenames_hs:
                                   
    #set nc variable in order to read attributes and obtained data: 
    nc_hs = Dataset(f, 'r')
    
    #call corrected swh and time data from data file f: 
    hs = nc_hs.variables['hs'][:]
    time_i = num2date(nc_hs.variables['time'][:], nc_hs.variables['time'].units) #convert time directly into datetime format instead of integer value time
    
    #create a loop to go through each time step and find the indices for where 
    for iday in range(res_time,len(time_i)+1,res_time):
        
        #call data from 1 day: 
        hs_d = hs[(iday-res_time):iday,:,:]
        
        #average the data each day in order to obtain the daily mean hs global grid: 
        hs_mean = mean_mask_t(data = hs_d)
        
        #decrease resolution up to 1 degree: 
        #hs_conv = running_mean(data = hs_mean, k_dim = [2,2]) #Only for one to one comparison of data with Ifremer 
        
        #orientate the data over to the Pacific: 
        hs_shift, lon_shift = shift_grid(data = hs_mean, lon = lon, dlon = 180)
        
        #take only the data points from ww3 which match with the along track satellite data points Ifremer:
        #wsp_along_track = land_fill(data = hs_conv, fill = 'Satellite', res = '1_deg') #For one to one grid point comparison of ww3 and Ifremer product 1
        
        #truncate the latitude dimension from -78:78 to -66:66
        trunc = abs(int((min(lat)-lat_min)/dlat))
        #wsp_c = wsp_conv[trunc:len(lat)-trunc,:] #For one to one grid point comparison of ccmp v2 and Ifremer product 1
        hs_c = hs_shift[trunc:len(lat)-trunc-4,:]
        
        #save the average daily array in a 3D array: 
        hs_ww3_cfsr_d[i,:,:] = hs_c
        time_d.append([time_i[iday-res_time]])
        
        #counter sum 
        i = i + 1
        print(i)


# In[11]:


print(time_d)
#trunc = abs(int((min(lat)-lat_min)/dlat))
#print(lat[trunc:len(lat) - trunc - 4])
#print(hs_ww3_cfsr_d.shape)


# ##### Wnd: 

# In[33]:


#initialize masked array to concatinate 2d arrays directly into a 3D array:
wsp_ww3_cfsr_d = np.ma.masked_all([nt, nlat, nlon])

#initialize counter:
i = 0
                                   
#call each data file separately from each day in order:
for f in filenames_wnd:
                                   
    #set nc variable in order to read attributes and obtained data: 
    nc_wnd = Dataset(f, 'r')
    
    #call corrected wind velocity components, lon, and lat data from data file f: 
    uwnd = nc_wnd.variables['uwnd'][:]
    vwnd = nc_wnd.variables['vwnd'][:]
    time_i = num2date(nc_wnd.variables['time'][:], nc_wnd.variables['time'].units) #convert time directly into datetime format instead of integer value time 
    
    #compute wind speed: 
    wsp = np.sqrt((uwnd**2) + (vwnd**2))
    
    #create a loop to go through each time step and find the indices for where 
    for iday in range(res_time,len(time_i)+1,res_time):
        
        #call data from 1 day: 
        wsp_d = wsp[(iday-res_time):iday,:,:]
        
        #average the data each day in order to obtain the daily mean hs global grid: 
        wsp_mean = mean_mask_t(data = hs_d)
        
        #decrease resolution up to 1 degree: 
        #wsp_conv = running_mean(data = wsp_mean, k_dim = [2,2]) #Only for one to one comparison of data with Ifremer 
        
        #orientate the data over to the Pacific: 
        wsp_shift, lon_shift = shift_grid(data = wsp_mean, lon = lon, dlon = 180)
        
        #take only the data points from ww3 which match with the along track satellite data points Ifremer:
        #wsp_along_track = land_fill(data = wsp_conv, fill = 'Satellite', res = '1_deg') #For one to one grid point comparison of ww3 and Ifremer product 1
        
        #truncate the latitude dimension from -78:78 to -66:66
        trunc = abs(int((min(lat)-lat_min)/dlat))
        #wsp_c = wsp_conv[trunc:len(lat)-trunc,:] #For one to one grid point comparison of ccmp v2 and Ifremer product 1
        wsp_c = wsp_shift[trunc:len(lat)-trunc-4,:]
        
        #save the average daily array in a 3D array: 
        wsp_ww3_cfsr_d[i,:,:] = wsp_c
        
        #counter sum 
        i = i + 1
        print(i)
    


# ##### fp:

# In[34]:


#initialize masked array to concatinate 2d arrays directly into a 3D array:
fp_ww3_cfsr_d = np.ma.masked_all([nt, nlat, nlon])

#initialize counter:
i = 0
                                   
#call each data file separately from each day in order:
for f in filenames_fp:
                                   
    #set nc variable in order to read attributes and obtained data: 
    nc_fp = Dataset(f, 'r')
    
    #call corrected swh and time data from data file f: 
    fp = nc_fp.variables['fp'][:]
    time_i = num2date(nc_fp.variables['time'][:], nc_fp.variables['time'].units) #convert time directly into datetime format instead of integer value time 
    
    #create a loop to go through each time step and find the indices for where 
    for iday in range(res_time,len(time_i)+1,res_time):
        
        #call data from 1 day: 
        fp_d = fp[(iday-res_time):iday,:,:]
        
        #average the data each day in order to obtain the daily mean hs global grid: 
        fp_mean = mean_mask_t(data = fp_d)
        
        #decrease resolution up to 1 degree: 
        #fp_conv = running_mean(data = fp_mean, k_dim = [2,2])
        
        #orientate the data over to the Pacific: 
        fp_shift, lon_shift = shift_grid(data = fp_mean, lon = lon, dlon = 180)
        
        #take only the data points from ww3 which match with the along track satellite data points Ifremer:
        #fp_along_track = land_fill(data = fp_conv, fill = 'Satellite', res = '1_deg') #For one to one grid point comparison of ww3 and Ifremer product 1
        
        #truncate the latitude dimension from -78:78 to -66:66
        trunc = abs(int((min(lat)-lat_min)/dlat))
        #wsp_c = wsp_conv[trunc:len(lat)-trunc,:] #For one to one grid point comparison of ccmp v2 and Ifremer product 1
        fp_c = fp_shift[trunc:len(lat)-trunc-4,:]
        
        #save the average daily array in a 3D array: 
        fp_ww3_cfsr_d[i,:,:] = fp_c
        
        #counter sum 
        i = i + 1
        print(i)

    


# Reinitialize longitude anlatitude vectors with new orientations and resolutions

# In[13]:


lon_n = np.arange(0,360,0.5)
lat_n = lat[trunc:len(lat)-trunc-4]
print(lat_n.shape, lon_n.shape, hs_ww3_cfsr_d.shape)


# Save data in a netCDF files (note that each of the individual 3D arrays for hs, wsp, and peak frequency are too big for all three variable to be saved onto one such that permission will be denied to writ that many variables onto one netCDF. Therefore, I will need to have three separate NetCDF files for each key variable)  

# ##### Hs

# In[14]:


save_netcdf_fields_ww3_hs(swh = hs_ww3_cfsr_d, lon = lon_n, lat = lat_n, time = time_d, output = '/zdata/downloads/colosi_data_bk/binned_data/WW3/CFSR/lc_binned_data/ww3_hs_daily_binned_data_93_16.nc')


# ##### Wnd

# In[ ]:


save_netcdf_fields_ww3_wsp(wsp = wsp_ww3_cfsr_d, lon = lon_n, lat = lat_n, time = time_d, output = '/zdata/downloads/colosi_data_bk/binned_data/WW3/CFSR/lc_binned_data/ww3_wnd_daily_binned_data_93_16.nc')


# ##### fp

# In[ ]:


save_netcdf_fields_ww3_fp(fp = fp_ww3_cfsr_d, lon = lon_n, lat = lat_n, time = time_d, output = '/zdata/downloads/colosi_data_bk/binned_data/WW3/CFSR/lc_binned_data/ww3_fp_daily_binned_data_93_16.nc')


# Check that data is being correctly binned

# In[ ]:


#set variables for ploting one time step of wsp 
wsp_test = wsp_ww3_cfsr_d[0,:,:]
print(wsp_test.shape)
type(wsp_test)

#create figure and set figure size where figsize(width, length)
#plt.figure(figsize=(16,6))
#plot a colormap of swh with contours with a colormap
#plt.contourf(lon,lat,swh_test,30)
#plt.pcolor(lon_n,lat_n,wsp_test)
#plt.xlabel('longitude', fontsize=14)
#plt.ylabel('latitude', fontsize=14)
#set colorbar
#cbar = plt.colorbar()
#label colorbar and set font
#cbar.set_label('SWH [m]', fontsize=14)
#label figure 
#title = time_d[0]
#plt.title('Wind Speed on %s' %title,fontsize=16)


# ### Development Code: 

# In[19]:


lon_test = nc_hs.variables['longitude'][:]
lat_test = nc_hs.variables['latitude'][:]
print(len(lon_test))
print('')
print(lat_test)
time_test = num2date(nc_hs.variables['time'][:], nc_hs.variables['time'].units)
print(time_test[0])


# In[20]:


(31*24)//3


# In[21]:


hs_test = nc_hs.variables['hs'][:]
#time_test = num2date(nc_hs.variables['time'][:], nc_hs.variables['time'].units) 
hs_t = hs_test[(8-8):8,:,: ]
time_t = time_test[(8-res_time):8]
print(hs_t.shape)
print(len(hs_t))
print(time_t)
print(len(time_t))


# In[22]:


for iday in range(8,len(time_test)+1,8):
    print(iday)


# In[26]:


#plot the hs for one time step: 

#create figure and set figure size where figsize(width, length)
#plt.figure(figsize=(16,6))
#plot a colormap of swh with contours with a colormap
#plt.contourf(lon_test,lat_test,hs_test[0],30)
#plt.pcolor(lon_test,lat_test,hs_test[0], cmap=cmo.speed)
#plt.xlabel('longitude', fontsize=14)
#plt.ylabel('latitude', fontsize=14)
#set colorbar
#cbar = plt.colorbar()
#label colorbar and set font
#cbar.set_label('SWH [m]', fontsize=14)
#label figure 
#title = time_d[0]
#plt.title('Wind Speed on %s' %title,fontsize=16)


# In[22]:


print(type(hs_d[0]))
#ind = hs_d[0].mask == False
#print(ind)
#print(hs_d[0])


# In[38]:


test = np.full((20,13,2),4)
print(test.shape)
#np.sqrt(test)


# In[39]:


365.25/2


# In[ ]:




