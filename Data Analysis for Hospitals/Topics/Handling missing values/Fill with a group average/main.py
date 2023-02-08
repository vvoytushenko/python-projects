#  write your code here 
import pandas as pd
df =  pd.read_csv('../Fill with a group average/data/dataset//input.txt',
                  sep=',',
                  engine='python')
df['height'] = df.groupby('location')['height'].apply(lambda x: x.fillna(x.mean())).round(1)
print(df['height'].sum())