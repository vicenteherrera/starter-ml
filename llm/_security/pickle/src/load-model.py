import pickle
import pandas as pd
import numpy as np

with open("data/linear_regression.pkl", "rb") as f:
    unpickled_linear_model = pickle.load(f)

# summary of the model
print('Model intercept :', unpickled_linear_model.intercept_)
print('Model coefficients : ', unpickled_linear_model.coef_)
print('Model score : ', unpickled_linear_model.score(X, y))