import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
import model as m


app = Flask(__name__)
result = pickle.load(open('result.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    d = request.form['experience']
    prediction = result.predict(d)
    return render_template('index.html', prediction_text='Consumption should be {}\n'.format(np.expm1(prediction.values)))
  


if __name__ == "__main__":
    app.run(debug=True)
