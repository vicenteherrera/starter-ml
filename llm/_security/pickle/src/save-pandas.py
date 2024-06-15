import pandas as pd
import numpy as np

# Set random seed
np.random.seed(123)

data = {'Column1': np.random.randint(0, 10, size=100000),
        'Column2': np.random.choice(['A', 'B', 'C'], size=100000),
        'Column3': np.random.rand(100000)}

# Create Pandas dataframe
df = pd.DataFrame(data)

df.to_pickle("data/pandas_dataframe.pkl")
