import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
import matplotlib.pyplot as plt
import os
plt.style.use('seaborn-bright')

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
    prediction = result.predict(start=date_initial,end=date_final,result.params)      
    #prediction = np.expm1(prediction)
    prediction = round(prediction,3)

    monthly = prediction.resample('m').sum()
    monthly = pd.DataFrame(monthly,columns=['Units'])
    monthly = round(monthly,3)
    monthly.index = pd.to_datetime(monthly.index).month_name()

    headings = ("Month","Consumption (Units)")
    tup = monthly.to_records(index=True).tolist()
    unit_list = [i[1] for i in tup]
    total = ('Total',int(sum(unit_list)))
    tup.append(total)
    tup = tuple(tup)

    monthly.plot(kind='bar',colormap='Set3',width=0.60)
    plt.xticks(rotation = 20)
    plt.xlabel('Months')
    plt.ylabel('Unit Consumption')    
    plt.savefig('static/plot.png', transparent=True, bbox_inches='tight')

    return render_template('index.html',
    prediction_text= 'Monthly power consumption from {} to {}\n'.format(date_initial,date_final),
    filename='plot.png',headings= headings, tup=tup)  


if __name__ == "__main__":
    app.run(debug=True) 
