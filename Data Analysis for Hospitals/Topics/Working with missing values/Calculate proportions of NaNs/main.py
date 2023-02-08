#  write your code here 
import pandas as pd
df =  pd.read_csv('../Calculate proportions of NaNs/data/dataset//input.txt',
                  sep=',',
                  engine='python')
print((df.isnull().sum() / df.isnull().count()).round(2))