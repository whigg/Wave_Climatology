#!/usr/bin/env python
# coding: utf-8

# # Ifremer Product 1 Altimeter SWH and WSP Binning along track data from January 1st, 1993 till December 31st, 2016

# Plot figure within jupyter notebook 

# In[2]:





# Use the sys library in order to tell the notebook to look for files within the followinf directory path: 

# In[3]:


import sys
sys.path.append('/zdata/home/lcolosi/python_functions/')


# Import all libraries and functions

# In[4]:


#libraries
import numpy as np #contains the major of functions used for matrix arrays  
import matplotlib.pyplot as plt # matplotlib contains functions for graphics and plot manipulation
from netCDF4 import Dataset, num2date # netCDF4 handles netCDF files
import glob 
import cmocean.cm as cmo
from matplotlib import cm 

#my functions
from binning_along_track_data import bin_data
from shift_grid import shift_grid
from save_binned_data_nc import save_netcdf_fields


# Before continuing, I must make functions in order to make my program more modular which that the main program is a collection of modules that perform a specific role in the over all goal of the program and has a specific number of input and outputs. Within each module includes functions that have specific input variable that can be slightly changed to change the output. The benifit of having modularized data is that it: 1) Reduces human error 2) Makes the code more efficient 3) Reduces debugging and changing code. So, I will need to have several functions defined in the code below before running it. Right now, I have what is called "hard code" which means that I have code very specific to the data and purpose of the program. The code can be broken very easily with a simple human error or a wrongly defined variable. THIS IS NOT GOOD AT ALL!!! To reduce my hard code, I should use as little amount of numbers as possible and obtain all the information about the data from the data file itself. 

# Set dimensions for data of space and time which depends on the spatial orientation of the data set and the time period which the data is collected from. For the Ifremer data set, we want the following data orientation: 

# In[4]:


nt, nlon, nlat = 8766, 360, 133


# Call Ifremer Product 1 data from the server using glob from January 1st, 1993 to December 31st, 2015 and sort them numerically with the sort function

# In[5]:


filenames = sorted(glob.glob('/zdata/downloads/Ifremer/altimeter_data/*.nc'))
#print(filenames)


# Look at the name of the key variables in one of the files: 

# In[6]:


#look at one file:
file = filenames[0]

#set nc variable in order to read attributes and obtained data: 
nc = Dataset(file, 'r')

#print key variables:
print(nc.variables.keys())


# Look at the dimensions of lon, lat, and time: 

# In[7]:


#longitude
for at in nc.variables['lon'].ncattrs():
    print("%s : %s" %(at, nc.variables['lon'].getncattr(at)))

#laitude
for at in nc.variables['lat'].ncattrs():
    print("%s : %s" %(at, nc.variables['lat'].getncattr(at)))
    
#time 
for at in nc.variables['time'].ncattrs():
    print("%s : %s" %(at, nc.variables['time'].getncattr(at)))


# Note that the time variable consists of a time array for each measurement down to the millisecond it was recorded (approximately one measurement every second) 

# Set longitude and latitude vectors

# In[8]:


#lon = nc.variables['longitude'][:]
lon = np.arange(-180,180,1)
#lat = nc.variables['latitude'][:]
lat = np.arange(-66,67,1)


# Loop through each of the filenames and bin each file. Because each file is a separate day, I do not need to worry about making sure what file correspond to which day

# In[ ]:


#initialize masked array to concatinate 2d arrays directly into a 3D array:
swhcor_d = np.ma.masked_all([nt, nlat, nlon])
wspcor_d = np.ma.masked_all([nt, nlat, nlon])
time_d = []

#initialize counter:
i = 0
                                   
#call each data file separately from each day in order:
for f in filenames:
                                   
    #set nc variable in order to read attributes and obtained data: 
    nc = Dataset(f, 'r')

    #call corrected swh, corrected wsp, lon, and lat data from data file f: 
    swh_i = nc.variables['swhcor'][:]
    wsp_i = nc.variables['wind_speed_cor'][:]
    lon_i = nc.variables['lon'][:]
    lat_i = nc.variables['lat'][:]
    time_i = num2date(nc.variables['time'][:], nc.variables['time'].units) #convert time directly into datetime format instead of integer value time 
                                                             
    #bin data from current day: 
    swh_bin = bin_data(data = swh_i, lon = lon_i, lat = lat_i, dim = [nlon, nlat], orientation = ['Atlantic',[-180, 179], [-66,66]])
    wsp_bin = bin_data(data = wsp_i, lon = lon_i, lat = lat_i, dim = [nlon, nlat], orientation = ['Atlantic',[-180, 179], [-66,66]])
    
    #shift the data from the atlantic prespective to the Pacific perspective
    swh_bin_shift, lon_shift = shift_grid(data = swh_bin, lon = lon, dlon = 180)
    wsp_bin_shift, lon_shift = shift_grid(data = wsp_bin, lon = lon, dlon = 180)
    
    #save the swh and wsp data in a masked array: 
    swhcor_d[i,:,:] = swh_bin_shift
    wspcor_d[i,:,:] = wsp_bin_shift
    time_d.append([time_i[0]])
    
    #counter sum 
    i = i + 1
    print(i)                               


# Reinitialize latitude vectors with new orientations and resolutions

# In[8]:


lat_n = np.arange(-66,67,1)
lon_n = np.arange(0,360,1)
print(lat_n.shape,lon_n.shape)


# Save data into a netcdf file

# In[ ]:


save_netcdf_fields(swh = swhcor_d, wsp = wspcor_d, lon = lon_n, lat = lat_n, time = time_d, output = '/zdata/home/lcolosi/data/ifremer_p1_daily_data/my_daily_binned_ifremer_data/ifremer_swh_wsp_daily_binned_data_93_16_update.nc')


# Plot one time step of the binned data in order to see the orientation of the binned data 

# In[ ]:


#set variables for ploting one time step of swh 
swh_test = swhcor_d[0,:,:]
print(swh_test.shape)
type(swh_test)

#create figure and set figure size where figsize(width, length)
#plt.figure(figsize=(16,6))
#plot a colormap of swh with contours with a colormap
#plt.contourf(lon,lat,swh_test,30)
#plt.pcolor(lon,lat,swh_test, cmap=cmo.amp)
#plt.xlabel('longitude', fontsize=14)
#plt.ylabel('latitude', fontsize=14)
#set colorbar
#cbar = plt.colorbar()
#label colorbar and set font
#cbar.set_label('SWH [m]', fontsize=14)
#label figure 
#title = time_d[0]
#plt.title('Significant Wave Height on %s' %title,fontsize=16)


# ### Development Code (Hard Code):

# In[46]:


filename = '/zdata/downloads/IFREMER/altimeter_denoised/ESACCI-SEASTATE-L2P-SWH-Jason-1-20130620T232420-fv01_denoised.nc'

#set nc variable in order to read attributes and obtained data: 
nc = Dataset(filename, 'r')

#call data
swh_i = nc.variables['swh_denoised'][:]
lon_i = nc.variables['lon'][:]
lat_i = nc.variables['lat'][:]
time_i = num2date(nc.variables['time'][:], nc.variables['time'].units)

#loop through each element in the time 
dates = [t0.date() for t0 in time_i]
dates = np.array(dates)

if ~(dates == dates[0]).all():
    ind = dates == dates[0]

print(ind)


# In[40]:


print(dates)


# In[15]:


import datetime
(dates == dates[0]).all()
~(dates == dates[0]).all()


# In[21]:


ind = dates == dates[0]
swh_i[ind]


# In[27]:


print(swh_i.shape, swh_i[ind].shape, swh_i[~ind].shape)
print(swh_i[0:len(swh_i[ind])])


# In[24]:


1784+1213


# In[26]:


swh_day1 = swh_i[ind]


# In[41]:


print(time_i[0])
print(time_i[0].date())


# In[ ]:


ESACCI-SEASTATE-L2P-SWH-Jason-1-20020101*-fv01_denoised.nc


# In[47]:


print(filename)


# In[11]:


np.arange(1,32)


# In[14]:


month_final_day = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
print(month_final_day)


# In[17]:


print('surf' + 'life')


# In[8]:


swh_cor = np.zeros((360,133))
swh_nc = np.zeros((360,133))
print(swh_nc.shape)


# In[18]:


swh_n = np.arange(11)
print(swh_n.shape)
for idata in range(0,len(swh_n),1):
    swh_point = swh_n[idata]
    print(swh_point)


# In[21]:


a = 189.9574
print(a)
a_int = int(a)
print(a_int)


# In[22]:


b = -100
b_n = abs(b)
print(b_n)


# In[126]:


swh_cor = np.zeros((360,133))
lon_point = 103
lat_point = 40
swh_point = 3
swh_cor[lon_point,lat_point] = swh_cor[lon_point,lat_point] + swh_point
(swh_cor == 0).all()

ind_test = swh_cor == 3

swh_test = swh_cor[ind_test]

print(swh_test)

#script to print the entire array:
import sys

np.set_printoptions(threshold=sys.maxsize)

print(swh_cor)


# In[125]:


swh = np.random.rand(3,4, 1)
#np.concatenate([swh_test_m, swh], -1)
swh_test_m = np.concatenate((swh, swh, swh), axis=2)
print(swh_test_m)
swh_2 = np.random.rand(3,4)
swh_test_m = np.dstack((swh_test_m, swh_2))
print(swh_test_m)


# In[113]:


print(swh_test_m.shape)
type(swh_test_m)
swh_test_m[2][0:3][1]


# In[88]:


np.random.rand(3,4)


# In[14]:


# create masked array with the final shape of what you want my_array[Ntime, Nlat, Nlon]
Nt, Nlat, Nlon = 5, 3, 2
new_array = np.ma.masked_all([Nt, Nlat, Nlon])


# In[8]:


# fake data just to illustrate
a = np.random.random([Nlat, Nlon])
print(a.shape)


# In[16]:


for i in range(Nt):
    new_array[i] = np.random.random([Nlat, Nlon])


# In[17]:


new_array[0]


# In[19]:


nt, ny, nx = new_array.shape


# In[20]:


nt


# In[21]:


b = []
for i in range(Nt):
    b.append(np.random.random([Nlat, Nlon]))


# In[22]:


c = np.array(b)


# In[23]:


c.shape


# In[11]:


for i in range(nt):
    print(i)


# In[21]:


time_i = num2date(nc.variables['time'][:], nc.variables['time'].units) #convert time directly into datetime format instead of integer value time 
print(time_i)
len(test)


# In[33]:


lon = np.arange(-180,180,1)
print(len(lon))
lat = np.arange(-66,67,1)
print(len(lat))


# In[53]:


test = np.zeros((3,3))
print(test)


# In[ ]:




