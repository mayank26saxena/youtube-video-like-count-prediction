import sqlite3
import matplotlib.pyplot as plt
from numpy import *
import numpy as np
import pandas as pd
import seaborn as sns

db_connection = sqlite3.connect('/home/mayank/Desktop/precog/youtube/big-database/youtube.db')
db = db_connection.cursor()

likeCount = []
viewCount = []
commentCount = []
favoriteCount = []
dislikeCount = []
duration = []
description = []
categoryId = []

try:
    for i, row in enumerate(db.execute("SELECT \
    likeCount, \
    viewCount, \
    commentCount, \
    favoriteCount, \
    dislikeCount, \
    duration, \
    description, \
    categoryId \
    FROM \
    youtube_static").fetchall()):
               
        # numerical features
        likeCount.append(int(row[0])) # = row[0]
        viewCount.append(int(row[1])) # = row[1]
        commentCount.append(int(row[2])) # = row[2] 
        favoriteCount.append(int(row[3])) # = row[3] 
        dislikeCount.append(int(row[4])) # = row[4] 
        duration.append(int(row[5])) # = row[5] 
        description.append(row[6]) # = row[6]
        categoryId.append(int(row[7])) # = row[7]
        if (i+1) % 1000 == 0:
            print i+1
except sqlite3.OperationalError, e:
    print 'sqlite3.OperationalError:', e




    
#plt.hist(likeCount) #plotting the column as histogram 
#plt.show()

#plt.savefig("like-frequency.png) # save as png
#plt.clf()
 
#cols = ['likeCount','viewCount','commentCount', 'dislikeCount']
#data = zip(likeCount,viewCount,commentCount, dislikeCount)
#df =  pd.DataFrame(data, index=range(1,len(likeCount)+1), columns=cols)
#corr = df.corr(method='pearson')
#print corr
#corr= corr.round(2)
# Generate a mask for the upper triangle
#mask = np.zeros_like(corr, dtype=np.bool)
#mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
#ax = plt.subplots(figsize=(8,6))

#Generate a custom diverging colormap
#cmap = sns.diverging_palette(220, 20, sep=20, as_cmap=True) 
#cmap = sns.diverging_palette(150, 275, s=80, l=55, n=9,center="dark",as_cmap=True)     # center="dark"    
# Draw the heatmap with the mask and correct aspect ratio
#sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3,square=True, linewidths=.5, cbar_kws={"shrink": .5}, ax=ax) 
	                                        #xticklabels=5, yticklabels=5,
	
#sns.heatmap(corr, mask=mask, cmap=cmap, annot=True, fmt=".2f", linewidths=.5)
#plt.savefig('corplot.png') # save as png
#plt.show()
