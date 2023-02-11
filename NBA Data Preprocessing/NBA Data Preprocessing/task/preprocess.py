import pandas as pd
import os
import requests
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# Download data if it is unavailable.
if 'nba2k-full.csv' not in os.listdir('../Data'):
    print('Train dataset loading.')
    url = "https://www.dropbox.com/s/wmgqf23ugn9sr3b/nba2k-full.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/nba2k-full.csv', 'wb').write(r.content)
    print('Loaded.')

data_path = "../Data/nba2k-full.csv"

# write your code here
# 1. In this first stage, create a function called clean_data that takes the path to the dataset as a parameter.
    # 1.1. Load a DataFrame from the location specified in the path parameter;
    # 1.2. Parse the b_day and draft_year features as datetime objects;
    # 1.3. Replace the missing values in team feature with "No Team";
    # 1.4. Take the height feature in meters, the height feature contains metric and customary units;
    # 1.5. Take the weight feature in kg, the weight feature contains metric and customary units;
    # 1.6. Remove the extraneous $ character from the salary feature;
    # 1.7. Parse the height, weight, and salary features as floats;
    # 1.8. Categorize the country feature as "USA" and "Not-USA";
    # 1.9. Replace the cells containing "Undrafted" in the draft_round feature with the string "0";
    # 1.10. Return the modified DataFrame.
def clean_data (path):
    df = pd.read_csv(path)
    df['b_day'] = pd.to_datetime(df['b_day'], format='%m/%d/%y')
    df['draft_year'] = pd.to_datetime(df['draft_year'], format='%Y')
    df.loc[(df['team'].isnull()), ['team']] = "No Team"
    df['height'] = df.apply(lambda x: x['height'].split('/')[1].strip(), axis=1)
    df['weight'] = df.apply(lambda x: x['weight'].split('/')[1].replace('kg.', '').strip(), axis=1)
    df['salary'] = df['salary'].str[1:]
    df[['height', 'weight', 'salary']] = df[['height', 'weight', 'salary']].astype(float)
    df.loc[(df['country'] != 'USA'), ['country']] = 'Not-USA'
    df.loc[(df['draft_round'] == 'Undrafted'), ['draft_round']] = '0'
    return df
#df = clean_data(data_path)
#print(df[['b_day', 'team', 'height', 'weight', 'country', 'draft_round', 'draft_year', 'salary']].head())





# 2. The input parameter is the returned DataFrame from the clean_data function from the previous stage;
    # Get the unique values in the version column of the DataFrame you got from clean_data as a year (2020, for example)
        # and parse as a datetime object;
    # 2.1. Engineer the age feature by subtracting b_day column from version. Calculate the value as year;
    # 2.2.  Engineer the experience feature by subtracting draft_year column from version. Calculate the value as year;
    # 2.3. Engineer the bmi (body mass index) feature from weight and height
    # 2.4. Drop the version, b_day, draft_year, weight, and height columns;
    # 2.5. Remove the high cardinality features;
    # 2.6. Return the modified DataFrame.
def feature_data(df):
    df['version_new'] = pd.to_numeric(df['version'].str.replace('NBA2k', '20'))
    df['age'] = df['version_new'] - pd.DatetimeIndex(df['b_day']).year
    df['experience'] = df['version_new'] - pd.DatetimeIndex(df['draft_year']).year
    df['bmi'] = df['weight'] / (df['height'] * df['height'])
    df = df.drop(columns=['version', 'b_day', 'draft_year', 'weight', 'height', 'version_new'])

    for i in df.columns:
        if df[i].nunique() > 50 and i not in ['age', 'experience', 'bmi', 'salary']:
            df.drop(i, axis=1, inplace=True)

    return df
#df_cleaned = clean_data(data_path)
#df = feature_data(df_cleaned)
#print(df[['age', 'experience', 'bmi']].head())





# 3. In this stage, you will build the multicol_data function given the DataFrame preprocessed by feature_data function
    #from the previous stage. Inside the multicol_data function:
#The input parameter is the returned DataFrame from the feature_data function.
    #It contains features and the target variable, which is salary.
    # 3.1. Drop multicollinear features from the DataFrame that you got from the feature_data;
    # 3.2. Return the modified DataFrame.
def multicol_data(df):
    corr = df.select_dtypes('number').drop(columns='salary').corr()
    correlated_features = []
    for i in range(corr.shape[0]):
        for j in range(0, i):
            if corr.iloc[i, j] > 0.5 or corr.iloc[i, j] < -0.5:
                correlated_features.append([corr.columns[i], corr.index[j]])

    for feature1, feature2 in correlated_features:
        if df[[feature1, 'salary']].corr().iloc[1, 0] > df[[feature2, 'salary']].corr().iloc[1, 0]:
            df.drop(columns=feature2, inplace=True)
        else:
            df.drop(columns=feature1, inplace=True)
    return df
#df_cleaned = clean_data(data_path)
#df_featured = feature_data(df_cleaned)
#df = multicol_data(df_featured)
#print(list(df.select_dtypes('number').drop(columns='salary')))


# 4. In this stage, implement the data preprocessing pipeline inside the transform_data function. Your function must:
# As the input parameter, take the DataFrame returned from multicol_data function, which you implemented in the previous stage;
    # 4.1. Transform numerical features in the DataFrame it got from multicol_data using StandardScaler;
    # 4.2. Transform nominal categorical variables in the DataFrame using OneHotEncoder;
    # 4.3. Concatenate the transformed numerical and categorical features in the following order: numerical features,
        # then nominal categorical features;
    # 4.4. Return two objects: X, where all the features are stored, and y with the target variable.

def transform_data(df):
    num_feat_df = df.select_dtypes('number')  # numerical features
    cat_feat_df = df.select_dtypes('object')  # categorical features
    object_ = StandardScaler()
    num_feat_df_scaled = object_.fit_transform(num_feat_df[['rating', 'experience', 'bmi']])
    num_feat_df_scaled = pd.DataFrame(num_feat_df_scaled, columns=num_feat_df[['rating', 'experience', 'bmi']].columns)
    enc = OneHotEncoder(sparse=False)

    def one_hot(dataframe):
        new_df = pd.DataFrame()
        for column in dataframe:
            result = enc.fit_transform(pd.DataFrame(dataframe[column]))
            df_enc = pd.DataFrame(result, columns=enc.categories_[0])
            new_df = pd.concat([new_df, df_enc], axis=1)
        return new_df

    cat_feat_df_enc = one_hot(cat_feat_df)
    x = pd.concat([num_feat_df_scaled, cat_feat_df_enc], axis=1)
    y = df.salary
    return x, y
df_cleaned = clean_data(data_path)
df_featured = feature_data(df_cleaned)
df = multicol_data(df_featured)
X, y = transform_data(df)

answer = {
    'shape': [X.shape, y.shape],
    'features': list(X.columns),
}
print(answer)