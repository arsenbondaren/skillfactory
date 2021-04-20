import pandas as pd
from IPython.display import display





footballers = pd.read_csv('data_sf.csv')

small_footballers = footballers[footballers.columns[0:8]].head(25)
print(small_footballers)