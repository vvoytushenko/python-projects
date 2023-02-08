#  write your code here
import pandas as pd
df =  pd.read_csv('../Replace with the mode/data/dataset//input.txt',
                  sep=',',
                  engine='python')

mode_district = df['location'].mode()[0] # calculate the mode
df['location'].fillna(mode_district, inplace=True) # replace NaNs with that mode

print(df.head(5))