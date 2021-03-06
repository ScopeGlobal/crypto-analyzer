# Objective: to train the model to predict market cap values accurately.

# imports
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pycoingecko
import pickle

# save file for model
filename = "finalized_cap.sav"

# imports for error testing
# TODO: Remove before final submission
from sklearn.metrics import mean_absolute_error

def train_cap(currency):
    df = pd.read_csv('./data/archive/coin_' + currency + '.csv')

    # taking the features we are interested in and creating a new dataframe
    interested_features = ["Open", "Close", "High", "Low", "Marketcap", "Volume"]
    cleaned_df = df[interested_features]

    # now we select the features we think will affect the final marketcap
    influencing_features = ["Volume", "Close", "High"]
    x = cleaned_df[influencing_features]

    # values to be predicted
    y = cleaned_df["Marketcap"]

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
    print(rf_model.predict(x.tail()))

    print("Actual Values")
    print(y)

    # using mean absolute error to further determine accuracy
    rf_values_error = mean_absolute_error(yval, rf_prediction)
    print(rf_values_error)


train_cap('Bitcoin')