# Bash script for downloading buoy SWH and WSP (and if available 2D Wave Spectra) data in SWA regions from the National Data Buoy Center from the following websites:https://dods.ndbc.noaa.gov/thredds/catalog/data/stdmet/catalog.html and https://dods.ndbc.noaa.gov/thredds/catalog/data/swden/catalog.html 

#List of SWA region stations:
#1) Northern California Coast (Station #: 46013 (Bodega bay) and 46059 (Offshore West San Fran))
#2) South Caribbean Sea (Station #: 42058)
#3) Northern Africa Coast (Morocco) (Station #: 13002)
#4) North Western Arabian Sea (Somalia) (Station #: 23011)
#5) Western Australia Coast (Station #: 56055)
#6) West Central South American Coast (Chile) (Station #: 34420)
#7) South Western African Coast Namibia (Station #: none) 

#Morocco coast
#SWH and WSP
cd stdmet/13002/
wget https://dods.ndbc.noaa.gov/thredds/fileServer/data/stdmet/13002/13002h9999.nc
cd ../../

#Northern California Coast (Bodega Bay)
#SWH and WSP
cd stdmet/46013/  
for i in seq 1993 1994 1995 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015
do 
wget https://dods.ndbc.noaa.gov/thredds/fileServer/data/stdmet/46013/46013h$i.nc
done
cd ../../swden/46013/
#Spectral Wave Density
for i in seq 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015
do 
wget https://dods.ndbc.noaa.gov/thredds/fileServer/data/swden/46013/46013w$i.nc
done 
cd ../../

#Northern California Coast (Offshore San Francisco)
#SWH and WSP
cd stdmet/46059/
for i in seq 1994 1995 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015
do 
wget https://dods.ndbc.noaa.gov/thredds/fileServer/data/stdmet/46059/46059h$i.nc
done
cd ../../swden/46059/
#Spectral Wave Density
for i in 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015
do 
wget https://dods.ndbc.noaa.gov/thredds/fileServer/data/swden/46059/46059w$i.nc
done
cd ../../

#South Caribbean Sea
#SWH and WSP
cd stdmet/42058/  
for i in 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015
do 
wget https://dods.ndbc.noaa.gov/thredds/fileServer/data/stdmet/42058/42058h$i.nc
done 
cd ../../swden/42058/
#Spectral Wave Density
for i in 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015
do 
wget https://dods.ndbc.noaa.gov/thredds/fileServer/data/swden/42058/42058w$i.nc
done
cd ../../

