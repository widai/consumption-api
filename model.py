import transform as tr
import pandas as pd
import numpy as np
import pickle
import statsmodels.api as sm

def training():

  indexed_data = tr.transform()
  log_indexed_data = np.log1p(indexed_data)

  #Preparing the training data
  train = log_indexed_data[:274]
  test = log_indexed_data[274:]

  #Modelling the data
  model = sm.tsa.statespace.SARIMAX(train,order=(3,1,1),seasonal_order=(3,1,1,10))
  results = model.fit()

  pickle.dump(results, open('result.pkl','wb'))
  result = pickle.load(open('result.pkl','rb'))

  return result
