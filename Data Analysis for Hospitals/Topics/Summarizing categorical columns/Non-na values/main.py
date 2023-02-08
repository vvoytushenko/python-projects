#  write your code here
import pandas as pd

df_rock =  pd.read_csv('../Non-na values/data/dataset/input.txt',
                  sep=',',
                  engine='python')

print(df_rock['labels'].count())