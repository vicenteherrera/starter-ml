import pickle
import pandas as pd
import numpy as np


df_pkl = pd.read_pickle("data/pandas_dataframe.pkl")

print('Data type: '+str(type(df_pkl)))
print('Array shape: '+str(df_pkl.shape))
