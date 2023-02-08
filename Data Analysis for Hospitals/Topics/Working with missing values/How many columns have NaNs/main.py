#  write your code here 
import pandas as pd
df =  pd.read_csv('../How many columns have NaNs/data/dataset//input.txt',
                  sep=',',
                  engine='python')
print(df.isnull().dropna(axis=0).nunique()[1])
