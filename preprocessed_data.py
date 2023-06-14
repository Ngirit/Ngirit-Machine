import pandas as pd
import numpy as np

# Load and preprocess your dataset
data = pd.read_csv('ngirit_datasetnew.csv')

data = data.drop('merchant_area',axis=1).replace(to_replace = 'NAN', value=np.NaN)
data['rating'] = pd.to_numeric(data['rating'])
data['rating'].fillna(float(data['rating'].mean()),inplace=True)
