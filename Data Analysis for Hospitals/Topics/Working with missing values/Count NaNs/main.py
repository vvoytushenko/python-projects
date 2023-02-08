#  write your code here 
import pandas as pd
df =  pd.read_csv('../Count NaNs/data/dataset//input.txt',
                  sep=',',
                  engine='python')
print(df.isna().sum())
