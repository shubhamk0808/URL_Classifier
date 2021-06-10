import pandas as pd
import numpy as np
import random
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from tokenizerUtility import sanitization



def urlResult(url):
   
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fullpath_m = os.path.join(dir_path, 'pickel_model_new.pkl')
    fullpath_v = os.path.join(dir_path, 'pickel_vector_new.pkl')

    vectorizer = pickle.load(open(fullpath_v,'rb'))
    tf_model = pickle.load(open(fullpath_m,'rb'))

    x_predict = [url]
    x_predict = vectorizer.transform(x_predict)
    # y_predict = tf_model.predict(x_predict)   #uncomment this line when probability thing is over
    y_predict = tf_model.predict_proba(x_predict)[:,1]    #remove this line..just for checking probability
    return(y_predict[0])
    

