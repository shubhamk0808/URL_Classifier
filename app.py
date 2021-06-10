from flask import Flask, render_template,url_for,request
import jsonify
import requests
import pickle
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
import joblib
import xgboost
from xgboost import XGBClassifier
import url_feature_extraction
from url_tfidf_check import urlResult
from url_tfidf_check import sanitization

app = Flask(__name__)

sc = StandardScaler()
#model = XGBClassifier()
# model = pickle.load(open('xgboost.pkl', 'rb'))
model = joblib.load("XGBoost.pkl")
# model.load_model("XGBoost_model.pkl")
#model = pickle.load(open('XGBoost_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')


def generateFeatures(url):
    featLst, tblDict = url_feature_extraction.combineFeatures(url)
    return (np.array([featLst]), tblDict)


@app.route("/predict", methods=['POST'])
def predict():    
    if request.method == 'POST':
        
        input_url = request.form['url']
        features, tblDict = generateFeatures(input_url)
        # sc = pickle.load(open('scaler.pkl','rb'))
        # prediction=model.predict(sc.transform(features))
        if(tblDict['validURL'] == False):
            prediction = 2
        else:
            # prediction= (model.predict(features)[0] and urlResult(input_url))     #uncomment this
            xgbprob= model.predict_proba(features)[:,1][0]   #remove this 1
            tfprob = urlResult(input_url)   #remove this 2
        # tblDict['prediction'] = prediction        #uncomment this
            
            if(np.mean([xgbprob, tfprob]) >= 0.6):
                prediction = 1
            else:
                prediction = 0
        
            tblDict['tfprob'] = round(tfprob,4)        #remove this 2
            tblDict['xgbprob'] = round(xgbprob,4)        #remove this 1
        tblDict['prediction'] = prediction
                
        return render_template('result.html',data = tblDict)

    else:
        return render_template('result.html')

if __name__=="__main__":
    app.run(debug=True), port = int(os.environ.get('PORT', 33507), threaded = True)