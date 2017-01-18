import numpy as np
import matplotlib.pyplot as plt
from numpy import *
import pandas as pd
import math
from scipy import stats, integrate
import seaborn as sns
from mpl_toolkits.basemap import Basemap


# Define the projection, scale, the corners of the map, and the resolution.
m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
# Draw the coastlines
m.drawcoastlines()
# Color the continents
m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
m.drawparallels(np.arange(-90.,91.,30.))
m.drawmeridians(np.arange(-180.,181.,60.))
# fill in the oceans
m.drawmapboundary(fill_color='aqua')
#plt.title("Mercator Projection")
#plt.show()

df = pd.read_csv('likeCount-latitude-longitude')
lat = df['latitude'].tolist()
lon = df['longitude'].tolist()
lc = df['likeCount'].tolist()
lc = [math.log10(x+1) for x in lc]
x,y = m(lon, lat) 
m.plot(x,y, 'bo', markersize=3)
# Color the transformed points!
# Define a colormap
jet = plt.cm.get_cmap('jet')
sc = plt.scatter(x,y, c=lc, vmin=0, vmax =35, cmap=jet, s=20, edgecolors='none')
# And let's include that colorbar
cbar = plt.colorbar(sc, shrink = .5)
cbar.set_label('Log10(LikeCounts)')
#plt.show()
plt.savefig('likeCount-location.png') 

