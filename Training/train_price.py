# Objective : to train the model to predict crypto prices accurately

# imports
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pycoingecko
import pickle

filename = 'finalized.sav'

# Secondary Imports to Test for error testing
# TODO: Remove all Error related imports when designing final version.
from sklearn.metrics import mean_absolute_error

def train_price(currency):
   df = pd.read_csv('./data/archive/coin_' + currency + '.csv')
   
   # taking the features we are interested in and creating a new dataframe
   interested_features = ["Open", "Close", "High", "Low", "Marketcap"]
   cleaned_df = df[interested_features]

   # now, out of these interests, we select the features we think will influence the values
   # TODO: Finetune
   influencing_features = ["High", "Low", "Marketcap"]
   x = cleaned_df[influencing_features]
   
   # values to be predicted
   y = cleaned_df["Close"]

   # we create the split between training and testing values. As is done in most cases, an 80-20 split is taken.
   xtrain, xval, ytrain, yval = train_test_split(x, y, train_size=0.8, test_size=0.2)
   
   # now, we create our Random Forests Model.
   # TODO: Add parameters to prevent overfitting.
   rf_model = RandomForestRegressor(n_estimators=500, max_features=3, min_samples_leaf=50)
   rf_model.fit(xtrain, ytrain.values.ravel())
   
   # predicting the values 
   rf_prediction = rf_model.predict(xval)
   if not os.path.isfile(filename):
    pickle.dump(rf_model, open(filename, 'wb'))

   # testing to see if our values are accurate
   # TODO: remove before submission
   print(rf_model.predict(x.tail()))

   print("Actual Values")
   print(y)

   # using mean absolute error to further determine accuracy
   rf_values_error = mean_absolute_error(yval, rf_prediction)
   print(rf_values_error)


def real_time_test(currency):
    cg = pycoingecko.CoinGeckoAPI()
    real_time_df = pd.DataFrame(
        cg.get_coin_ohlc_by_id(id=currency.lower(), days=30, vs_currency='usd'), 
        columns=['Marketcap', 'Open', 'High', 'Low', 'Close']
    )
    print(real_time_df)

    cleaned_real_time_df = real_time_df[["High", "Low", "Marketcap"]]
    real_time_result = real_time_df["Close"]

    load_model = pickle.load(open(filename, 'rb'))
    result = load_model.predict(cleaned_real_time_df)
    print(result)

    result_error = mean_absolute_error(real_time_result, result)
    print(result_error)         


train_price('Bitcoin')
real_time_test('Bitcoin') 