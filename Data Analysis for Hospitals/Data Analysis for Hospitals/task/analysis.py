# write your code here
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#After all the libraries imports write the following line of code:
pd.set_option('display.max_columns', 8)

#Read 3 CSV files containing the datasets
#data_dir = Path('D:\\projects\\jetbrains\\Data Analysis for Hospitals\\Data Analysis for Hospitals\\task\\test\\')
#df = pd.concat([pd.read_csv(f) for f in data_dir.glob("*.csv")], ignore_index=True)
general = pd.read_csv('../task/test/general.csv')
prenatal = pd.read_csv('../task/test/prenatal.csv')
sports = pd.read_csv('../task/test/sports.csv')

#Print the first 20 rows of each DataFrame.
# Use the following order: general, prenatal, sports
#print(general.head(20))
#print(prenatal.head(20))
#print(sports.head(20))

#Change the column names. All column names in the sports and prenatal tables must match the column names in the general table
prenatal = prenatal.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender'})
sports = sports.rename(columns={'Hospital': 'hospital', 'Male/female': 'gender'})

#Merge the DataFrames into one. Use the ignore_index=True parameter and the following order: general, prenatal, sports
df = pd.concat([general, prenatal, sports], ignore_index=True)

#Delete the Unnamed: 0 column
df = df.drop('Unnamed: 0', axis=1)

#Print random 20 rows of the resulting DataFrame. For the reproducible output set random_state=30
#print(df.sample(random_state=30, n=20))




#Delete all the empty rows
df.dropna(axis=0, how='all', inplace=True)

#Correct all the gender column values to f and m respectively
df['gender'].replace({'man': 'm',
                      'male': 'm',
                      'female': 'f',
                      'woman': 'f'},
                     inplace=True)

#Replace the NaN values in the gender column of the prenatal hospital with f
df.loc[(df['gender'].isnull()), ['gender']] = "f"

#Replace the NaN values in the
    # bmi, diagnosis, blood_test, ecg,
    # ultrasound, mri, xray, children, months columns with zeros
df = df.fillna(0)

#Print shape of the resulting DataFrame like in example
#print('Data shape:', df.shape)

#Print random 20 rows of the resulting DataFrame. For the reproducible output set random_state=30
#print(df.sample(n=20, random_state=30))





#Which hospital has the highest number of patients?
top_hospital = df['hospital'].value_counts().index[0]
#print('The answer to the 1st question is', top_hospital)

#What share of the patients in the general hospital suffers from stomach-related issues?
#Round the result to the third decimal place.
stomach_share = (df[(df['hospital'] == 'general') &
   (df['diagnosis'] =='stomach')].diagnosis.count() / df[(df['hospital'] == 'general')].diagnosis.count()).round(3)
#print('The answer to the 2nd question is', stomach_share)

#What share of the patients in the sports hospital suffers from dislocation-related issues?
#Round the result to the third decimal place.
dislocation_share = (df[(df['hospital'] == 'sports') &
   (df['diagnosis'] =='dislocation')].diagnosis.count() / df[(df['hospital'] == 'sports')].diagnosis.count()).round(3)
#print('The answer to the 3rd question is', dislocation_share)

#What is the difference in the median ages of the patients in the general and sports hospitals?
median_diff = (df[(df['hospital'] == 'general')].age.median() - df[(df['hospital'] == 'sports')].age.median())
#print('The answer to the 4th question is', median_diff)

#After data processing at the previous stages, the blood_test column has three values:
    #t= a blood test was taken,
    #f= a blood test wasn't taken,
    #and 0= there is no information.
#In which hospital the blood test was taken the most often
    #(there is the biggest number of t in the blood_test column among all the hospitals)?
    #How many blood tests were taken?
top_blood_test = df['hospital'][(df['blood_test'] == 't')].value_counts()
#print('The answer to the 5th question is', top_blood_test.index[0], ',', top_blood_test[0], 'blood tests')





#What is the most common age of a patient among all hospitals?
#Plot a histogram and choose one of the following age ranges: 0-15, 15-35, 35-55, 55-70, or 70-80
df.plot(y='age', kind='hist', bins=[0, 15, 35, 55, 70, 80])
plt.show()
print('The answer to the 1st question: 15-35')

#What is the most common diagnosis among patients in all hospitals? Create a pie chart
df.diagnosis.value_counts().plot(kind="pie",
                                autopct='%.1f%%')
plt.show()
print('The answer to the 2nd question: pregnancy')

#Build a violin plot of height distribution by hospitals. Try to answer the questions.
    #What is the main reason for the gap in values?
    #Why there are two peaks, which correspond to the relatively small and big values?
    #No special form is required to answer this question
distribution_of_height = sns.violinplot(x='hospital', y='height', data=df)
distribution_of_height.set_title('Distribution of height', fontsize=16)
plt.show()
print("The answer to the 3rd question: This is because different hospitals use different units of measurement to "
      "display height: meters and feet. The two peaks correspond to a small number of people whose height is much "
      "larger or smaller than the average height of adults.")