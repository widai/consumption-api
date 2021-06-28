import numpy as np                               
import pandas as pd                              


def transform():
    #Reading the dataset
    dataset = pd.read_csv("data_widai.csv")
    dataset = dataset.rename(columns={"ASSOCIATED SITE": "Associated_Site", "LEG ID": "Leg_Id", "UNIT CONSUMPTION": "Unit_Consumption", "READING FOR": "Reading"})
    data = dataset.loc[dataset["Leg_Id"] != 1691]
    luhari = dataset.copy()
    luhari = luhari.drop(data.index,axis=0)
    luhari = luhari.reset_index(drop=True)
    luhari = luhari.drop(['Associated_Site','Leg_Id'],axis=1)
    luhari['Reading'] = pd.to_datetime(luhari['Reading'])

    #Data Transformations
    indexed_data = luhari.set_index('Reading')
    idx = pd.date_range('01-01-2020', '31-12-2020')
    indexed_data = indexed_data.reindex(idx, fill_value=0)

    #Averaging out peaks of June
    indexed_data.loc['2020-06-06':'2020-06-09'] = float(indexed_data.loc['2020-06-09']/4)
    indexed_data.loc['2020-06-16':'2020-06-17'] = float(indexed_data.loc['2020-06-17']/2)
    indexed_data.loc['2020-06-13':'2020-06-14'] = float((indexed_data.loc['2020-06-13']+indexed_data.loc['2020-06-14'])/2)

    #Filling out the missing value of first five days of June with first five days of July
    indexed_data.loc['2020-06-01':'2020-06-05'].Unit_Consumption = indexed_data.loc['2020-07-01':'2020-07-05'].values

    #Filling rest values with median values
    m = indexed_data.Unit_Consumption['2020-06-01':'2020-06-30'].median()
    indexed_data.Unit_Consumption['2020-06-19':'2020-06-29'] = m

    #Creating a dataframe avg to calculate mean of three months and substitute in the month of April
    avg = pd.DataFrame(columns=['Jan','Feb','March','Mean'])
    avg['Jan'] = indexed_data.loc['2020-01-01':'2020-01-31'].Unit_Consumption.values
    avg['March'] = indexed_data.loc['2020-03-01':'2020-03-31'].Unit_Consumption.values
    Feb = indexed_data.Unit_Consumption.loc['2020-02-01':'2020-02-29'].values
    Feb = np.append(Feb, [0,0])
    avg['Feb'] = Feb
    avg['Mean'] = avg.mean(axis=1)
    avg = avg.drop([30],axis=0)

    #Filling values of April
    indexed_data.Unit_Consumption['2020-04-01':'2020-04-30'] = avg.Mean

    #Filling missing values in July with median
    m = indexed_data.Unit_Consumption['2020-07-01':'2020-07-31'].median()
    indexed_data.Unit_Consumption['2020-07-19':'2020-07-30'] = m

    #Creating a dataframe may to calculate mean of months april and june and substitute in the month of may
    may = pd.DataFrame(columns=['april','june','mean'])
    may['april'] = indexed_data.Unit_Consumption['2020-04-01':'2020-04-30'].values
    may['june'] = indexed_data.Unit_Consumption['2020-06-01':'2020-06-30'].values
    may['mean'] = may.mean(axis=1)

    #Filling values for may
    indexed_data.Unit_Consumption['2020-05-01':'2020-05-30'] = may['mean']
    indexed_data.loc['2020-05-31'] = indexed_data.loc['2020-05-01':'2020-05-31'].mean()

    #Filling missing values of August with its mean value
    indexed_data.Unit_Consumption['2020-08-20':'2020-08-23'] = indexed_data.Unit_Consumption['2020-08-01':'2020-08-31'].mean()

    #Averaging peaks 
    indexed_data.Unit_Consumption['2020-09-07':'2020-09-11'] = float(indexed_data.Unit_Consumption['2020-09-11']/5)
    indexed_data.Unit_Consumption['2020-09-14':'2020-09-16'] = float(indexed_data.Unit_Consumption['2020-09-16']/3)
    indexed_data.Unit_Consumption['2020-09-20':'2020-09-21'] = float(indexed_data.Unit_Consumption['2020-09-21']/2)
    indexed_data.Unit_Consumption['2020-03-29':'2020-03-30'] = float(indexed_data.Unit_Consumption['2020-03-30']/2)
    indexed_data.Unit_Consumption['2020-02-10':'2020-02-11'] = float(indexed_data.Unit_Consumption['2020-02-11']/2)
    indexed_data.Unit_Consumption['2020-08-28':'2020-08-29'] = float(indexed_data.Unit_Consumption['2020-08-29']/2)

    #Dissolving other higher peaks with outlier type values
    indx = (indexed_data.loc[indexed_data.Unit_Consumption > 2200 ]).index
    for i in indx:
        if i in indexed_data.index:
            indexed_data.Unit_Consumption[i] = indexed_data.Unit_Consumption.mean()

    indx = (indexed_data.loc[indexed_data.Unit_Consumption < 500 ]).index
    for i in indx:
        if i in indexed_data.index:
            indexed_data.Unit_Consumption[i] = 400

    indexed_data.Unit_Consumption = indexed_data.Unit_Consumption.astype(float)

    return indexed_data