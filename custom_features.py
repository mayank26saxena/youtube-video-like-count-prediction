import math
import sqlite3
from pprint import pprint

import numpy as np

from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn import linear_model

import utils as utils

import csv
import cPickle as pickle

db_connection = sqlite3.connect('/home/mayank/Desktop/precog/youtube/create-database/youtube.db')
#db_connection = sqlite3.connect('/home/mayank/Desktop/precog/youtube/create-database/youtube_repeated_measures.db')
db = db_connection.cursor()

X = []
y = [] # LikeCount

numerical_features = []
categorical_features = []

# titles = []
# channels = []
# descriptions = []

try:
    for i, row in enumerate(db.execute("SELECT \
    likeCount, \
    viewCount, \
    commentCount, \
    favoriteCount, \
    dislikeCount, \
    duration, \
    description \
    FROM \
    youtube_static").fetchall()):
        # target
        #y.append(math.log10(row[0]) if row[0] != 0 else 0)
        y.append(math.log10(row[0]) if row[0] != 0 else 0 )
        
        
        # numerical features
        viewCount = math.log10(row[1]) if row[1] != 0 else 0
        commentCount = row[2] 
        favoriteCount = row[3] 
        dislikeCount = row[4] 
        duration = row[5] 
        description = row[6] 
        
        numerical_features.append([
        	viewCount,
        	commentCount,
        	favoriteCount,
        	dislikeCount,
        	duration,
        ]) 
        
        # categorical features
        description_containsWebsite = jordy.containsWebsite(description)
        description_containsSocialMedia = jordy.containsSocialMedia(description)
        
        categorical_features.append([
            description_containsWebsite,
            description_containsSocialMedia,
        ])

        if (i+1) % 1000 == 0:
            print i+1

except sqlite3.OperationalError, e:
    print 'sqlite3.OperationalError:', e

db_connection.close()

scaler = StandardScaler()
numencoder = scaler.fit(numerical_features)
numerical_features2 = numencoder.transform(numerical_features)
#numerical_features2 = scaler.fit_transform(numerical_features)

print '\nnumerical before:\n'
print numerical_features[0]
print '\nnumerical after:\n'
print numerical_features2[0]

onehot = OneHotEncoder()
catencoder = onehot.fit(categorical_features)
categorical_features2 = catencoder.transform(categorical_features)
#categorical_features2 = onehot.fit_transform(categorical_features)

print '\ncategorical before:\n'
print categorical_features[0]

print '\ncategorical after:\n'
print categorical_features2[0].toarray()

from scipy.sparse import coo_matrix, hstack

print ''
print numerical_features2.shape, 'numerical_features2'
print categorical_features2.shape, 'categorical_features2'

X = hstack([numerical_features2, categorical_features2])

print '\nall combined:\n'
print X.shape

with open('my_numerical_encoder.pkl', 'wb') as fid:
       pickle.dump(numencoder, fid) 

with open('my_categorical_encoder.pkl', 'wb') as fid:
       pickle.dump(catencoder, fid) 


print ''
print 'final X:', X.getrow(0).todense()
print 'final y:', y[0]



X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.4,
    random_state=3
)

X_eval, X_test, y_eval, y_test = train_test_split(
    X_test,
    y_test,
    test_size=0.5,
    random_state=3
)



from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

print '\n\n'
    
for set_to_use in ['train', 'eval', 'test']:
    outputfile = 'regression_custom_features_results_%s.txt' % set_to_use
    outputfile = open(outputfile, 'w')
    
    if set_to_use == 'train':
        X_to_use = X_train
        y_to_use = y_train
    if set_to_use == 'eval':
        X_to_use = X_eval
        y_to_use = y_eval
    if set_to_use == 'test':
        X_to_use = X_test
        y_to_use = y_test
    
    print 'X used = ' , X_to_use[0]
    print 'Y used = ' , y_to_use[0]
    
    
    sgd = linear_model.SGDRegressor(
       loss='squared_loss',
       penalty='none',
       alpha=10,
    )
    model = sgd.fit(X_train, y_train)
    
    with open('my_dumped_classifier.pkl', 'wb') as fid:
       pickle.dump(model, fid) 
    
    for loss in ['squared_loss', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive']:
        for penalty in ['none', 'l2', 'l1', 'elasticnet']:
            for alpha in [10, 1, .1, .01, .001, .0001, .00001]:
            
                sgd = linear_model.SGDRegressor(
                    loss=loss,
                    penalty=penalty,
                    alpha=alpha,
                )
                y_pred = sgd.fit(X_train, y_train).predict(X_to_use)
                y_true = y_to_use
                
                print 'r^2=%s, ev=%s, mae=%s, mse=%s, loss=%s, penalty=%s, alpha=%s, set=%s' % (
                    r2_score(y_true, y_pred),
                    explained_variance_score(y_true, y_pred),
                    mean_absolute_error(y_true, y_pred),
                    mean_squared_error(y_true, y_pred),
                    loss,
                    penalty,
                    alpha,
                    set_to_use,
                )
                outputfile.write('r^2=%s, ev=%s, mae=%s, mse=%s, loss=%s, penalty=%s, alpha=%s\n' % (
                    r2_score(y_true, y_pred),
                    explained_variance_score(y_true, y_pred),
                    mean_absolute_error(y_true, y_pred),
                    mean_squared_error(y_true, y_pred),
                    loss,
                    penalty,
                    alpha)
                )
                # print 'coefs:', sgd.coef_
                # print 'intercept:', sgd.intercept_
                # print '(test) R^2 from regressor:', sgd.score(X_eval, y_eval)
    outputfile.close()
 
