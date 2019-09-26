#!/usr/bin/env python
# coding: utf-8

# # CCMP Version 2 WSP binning data from January 1st, 1993 to December 31st, 2016

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
from datetime import datetime
import glob 
from scipy import signal
import cmocean.cm as cmo
from matplotlib import cm 

#my functions
from running_mean import running_mean
from save_binned_ccmp2_wsp import save_netcdf_fields


# Set dimensions for data of space and time which depends on the spatial orientation of the data set and the time period which the data is collected from. For the CCMP v2 data set, we want the following data orientation: 

# In[4]:


#For one to one grid point comparison of ccmp v2 and Ifremer product 1:
#nt, nlon, nlat = 8766, 360, 133
#For climatological and least square fitting data analysis (the spatial and temporal scales can be the same):
nt, nlat, nlon = 8766, 529, 1440
initial_year = 1993
final_year = 2016
initial_mon = 1
final_mon = 12


# Call CCMP version 2 data from the server using glob from January 1st, 1993 to December 31st, 2016 and sort them numerically with the sort function. Because the data is separated into yearly and monthly directories, I  will have to loop through all the years and months, in order obtain the names for all the files: 

# In[5]:


#Initialize empty file to place all filenames into: 
filenames = []
#Initialize monthly time vector:
imonth = ['01','02','03','04','05','06','07','08','09','10','11','12']

#create year loop: 
for iyear in range(initial_year,final_year+1,1):
    
    #create month loop:
    #for imos in range(initial_mon,final_mon+1,1):
    for imos in imonth:
        
        #obtain filenames from all days within the directory: 
        files = sorted(glob.glob('/zdata/downloads/ccmp/v02.0/Y' + '%s' %iyear + '/M' + '%s' %imos + '/*_V02.0_L3.0_RSS.nc'))
        
        #concatinate all filenames into a list 
        filenames = filenames + files
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
for at in nc.variables['longitude'].ncattrs():
    print("%s : %s" %(at, nc.variables['longitude'].getncattr(at)))

#laitude
for at in nc.variables['latitude'].ncattrs():
    print("%s : %s" %(at, nc.variables['latitude'].getncattr(at)))
    
#time 
for at in nc.variables['time'].ncattrs():
    print("%s : %s" %(at, nc.variables['time'].getncattr(at)))
#dimension: 
print('')
print(nc.variables['longitude'][:].shape,nc.variables['latitude'][:].shape)


# Set longitude and latitude vectors

# In[8]:


#Call longitutde and latitude data:
lon = nc.variables['longitude'][:]
#lon = np.arange(0,360,0.25)
lat = nc.variables['latitude'][:]
#lat = np.arange(-78,79,0.25)


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
# 3)Decrease the resolution of the data from 0.25 degree to 1 degree (I only need to do this when the data needs to be a one to one comparison with the Ifremer daily binned data) 
# 
# 4)Make sure the orientation of longitude is pacific centered (this is true) and latitude ranges from -66 to 66
# 
# 5)Place satellite tracks and continents into data set using the Ifremer product 1 data set ((I only need to do this when the data needs to be a one to one comparison with the Ifremer daily binned data) 
# 
# 5)Bin wsp and time data 

# Because each file is a separate day, I do not need to worry about making sure what file correspond to which day. In addition, recall the CCMP version 2 winds have data points at every grid point for all time steps because it is a product using multiple wind products and modelled data to produce a smooth grid through time and space. 

# In[10]:


#initialize masked array to concatinate 2d arrays directly into a 3D array:
wsp_ccmp_d = np.ma.masked_all([nt, nlat, nlon])
time_d = []

#initialize counter:
i = 0
                                   
#call each data file separately from each day in order:
for f in filenames:
                                   
    #set nc variable in order to read attributes and obtained data: 
    nc = Dataset(f, 'r')

    #call corrected swh, corrected wsp, lon, and lat data from data file f: 
    uwnd = nc.variables['uwnd'][:]
    vwnd = nc.variables['vwnd'][:]
    time_i = num2date(nc.variables['time'][:], nc.variables['time'].units) #convert time directly into datetime format instead of integer value time 
    
    #compute wind speed: 
    wsp_h = np.sqrt((uwnd**2) + (vwnd**2))
    
    #print(wsp_h.shape)
    
    #Average the time steps from each day to obtain a daily average
    wsp_d = (wsp_h[0,:,:]+wsp_h[1,:,:]+wsp_h[2,:,:]+wsp_h[3,:,:])/4

    #decrease the resolution of the the wsp matrix via convolution: 
    #wsp_conv = running_mean(data = wsp_d, k_dim = [4,4]) #For one to one grid point comparison of ccmp v2 and Ifremer product 1
    
    #take only the data points from CCMP v2 which match with the along track satellite data points Ifremer:
    #wsp_along_track = land_fill(data = wsp_d, fill = 'Satellite', res = '1_deg') #For one to one grid point comparison of ccmp v2 and Ifremer product 1
    
    #truncate wsp data such that we are only looking at data from -66 to 66 degrees:
    trunc = abs(int((min(lat)-lat_min)/dlat))
    #wsp_c = wsp_conv[trunc:len(lat)-trunc,:] #For one to one grid point comparison of ccmp v2 and Ifremer product 1
    wsp_c = wsp_d[trunc:len(lat)-trunc-1,:]
    
    #bin wsp and time data (make sure that wsp_c is a masked array): 
    wsp_ccmp_d[i,:,:] = wsp_c
    time_d.append([time_i[0]])
    
    #counter sum 
    i = i + 1
    print(i)


# Make sure the truncation worked

# In[14]:


print(trunc,len(lat)-trunc-1,lat[49],lat[579-1])
print(wsp_ccmp_d.shape)


# Reinitialize latitude vectors with new orientations and resolutions

# In[12]:


lat_n = lat[trunc:len(lat)-trunc-1]


# Save WSP, longitude, latitude, and time variables into yearly netCDF files (data is too larger for 0.25 resolution)

# Create a loop to go through all the data year by year

# In[13]:


#set year indices 
years = np.array([y[0].year for y in time_d])

#creat loop: 
for year in np.unique(years):
    
    #initialize the indices where the years vector elements are equal to the year value 
    ind_year = years == year
    
    #call wsp and time data for the given idices: 
    wsp_ccmp_y = wsp_ccmp_d[ind_year,:,:]
    
    #convert time to a numpy row vector: 
    time_c = np.array(time_d).reshape(1,len(time_d))[0]
    time_y = time_c[ind_year]
    
    #save data into a netCDF file:
    save_netcdf_fields(wsp = wsp_ccmp_y, lon = lon, lat = lat_n, time = time_y, output = '/zdata/downloads/colosi_data_bk/binned_data/ccmpv2_wind_data/daily_binned_ccmp_v2_data/ccmp_v2_wsp_daily_binned_data_' + '%s' %year + '_high_res.nc')


# Check that data is properly binned 

# In[17]:


#set variables for ploting one time step of swh 
wsp_test = wsp_ccmp_d[0,:,:]
print(wsp_test.shape)
type(wsp_test)

#create figure and set figure size where figsize(width, length)
#plt.figure(figsize=(16,6))
#plot a colormap of swh with contours with a colormap
#plt.contourf(lon,lat,swh_test,30)
#plt.pcolor(lon,lat_n,wsp_test, cmap=cmo.speed) #or cmap=cm.
#plt.xlabel('longitude', fontsize=14)
#plt.ylabel('latitude', fontsize=14)
#set colorbar
#cbar = plt.colorbar()
#label colorbar and set font
#cbar.set_label(r'$WSP(\frac{m}{s})$', fontsize=14)
#label figure 
#title = time_d[0]
#plt.title('Wind Speed on %s' %title,fontsize=16)


# Check dimensions of data set 

# In[75]:


print(len(time_d), len(lat), len(lon), wsp_ccmp_d.shape)


# ### Development Code: 

# In[80]:


fi = filenames[0]
#set nc variable in order to read attributes and obtained data: 
nc = Dataset(fi, 'r')

#call corrected swh, corrected wsp, lon, and lat data from data file f: 
uwnd = nc.variables['uwnd'][:]
vwnd= nc.variables['vwnd'][:]
time_i = num2date(nc.variables['time'][:], nc.variables['time'].units) #convert time directly into datetime format instead of integer value time 

print(uwnd.shape,vwnd.shape)

#compute wind speed: 
wsp_h = np.sqrt((uwnd**2) + (vwnd**2))

print(type(wsp_h[1,:,:]))


# In[81]:


np.set_printoptions(threshold=sys.maxsize)
t = np.array([(1,2,3,4,5,6,7,8),(1,2,3,4,5,6,7,8),(1,2,3,4,5,6,7,8),(1,2,3,4,5,6,7,8)])
k = np.array([(1,1,1,1),(1,1,1,1),(1,1,1,1),(1,1,1,1)])
k = k/np.sum(k)
#print(t)
#print(k)
test = signal.convolve2d(t,k)
print(test)
print('')
print(test[3::4,3::4])


# In[82]:


0.0625 + 2*0.0625 + 3*0.0625


# In[83]:


628/4


# In[91]:


#kernal matrix:
w = np.array([(1,1,1,1),(1,1,1,1),(1,1,1,1),(1,1,1,1)])
#normalize kernal matrix: 
w = w/np.sum(w)
#convolve image matrix with kernal matrix: 
wsp_conv = signal.convolve2d(wsp_d,w)
#select the elements from the convolved wsp matrix that are the averaged of four element boxes that do not overlap with each other and the edges of the matrix:
#Code below reads: take every four element begining at position 3 (0,1,2,3) and continuing till the end
wsp_c = wsp_conv[3::4,3::4]


# In[84]:


print(filenames[30],filenames[31])


# In[85]:


print(wsp_ccmp_d.shape)
print(wsp_c.shape)
time_d[-1]


# In[86]:


#initialize empty array
wsp_ccmp_d2 = np.ma.masked_all([8766, nlat, nlon])

#create loop to re-concatinate all wsp daily 2d arrays
for iday in range(0,8766):
    if iday <= 8764:
        wsp_ccmp_d2[iday,:,:] = wsp_ccmp_d[iday,:,:]
    elif iday == 8765:
        wsp_ccmp_d2[iday,:,:] = wsp_c
print(wsp_ccmp_d2.shape)


# In[87]:


print(time_i[0])
time_d.append([time_i[0]])


# In[88]:


len(time_d)


# In[89]:


print(min(lat))
print((int(min(lat))-lat_min)/dlat)
print((-78-(-66))/1)


# In[90]:


157-12


# In[25]:


print(time_i)
years = np.array([y.years for y in time_i])
print(k)


# In[26]:


help(np.array)


# In[27]:


month_data = {}
type(month_data)


# In[8]:


year = 1993

output = '/zdata/home/lcolosi/data/ccmpv2_wind_data/daily_binned_ccmp_v2_data/ccmp_v2_wsp_daily_binned_data_' + '%s' %year + '_high_res.nc'
print(output)


# In[ ]:


#look if there is any nan values in the 2D array
imask = wsp_c == wsp_c.mask
#ival = ~np.isnan(wsp_c)

print(len(wsp_c[~imask]), len(wsp_c[imask]), len(wsp_c), 529*1440)
print(imask)

