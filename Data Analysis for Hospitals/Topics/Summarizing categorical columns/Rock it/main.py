#  write your code here
import pandas as pd

df_rock =  pd.read_csv('../Rock it/data/dataset/input.txt',
                  sep=',',
                  engine='python')

print(df_rock['labels'].value_counts().loc[['R']][0])