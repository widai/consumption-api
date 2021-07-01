import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
import matplotlib.pyplot as plt


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
    date_initial = request.form['date_initial']
    date_final = request.form['date_final']
    prediction = result.predict(start=date_initial,end=date_final)      
    prediction = np.expm1(prediction)

    monthly = prediction.resample('m').sum()
    monthly = pd.DataFrame(monthly,columns=['unit'])
    monthly.index = pd.to_datetime(monthly.index).month

    monthly.plot(kind='bar',colormap='rainbow',width=0.70)
    plt.xticks(rotation=90)
    plt.xlabel('Months')
    plt.ylabel('Unit Consumption')
    plt.savefig('static/plot.png')

    return render_template('index.html',
    prediction_text= 'Monthly power consumption from {} to {} should be {}\n'.format(date_initial,date_final,prediction.resample('m').sum().values),
    filename='plot.png')    


if __name__ == "__main__":
    app.run(debug=True)
    
