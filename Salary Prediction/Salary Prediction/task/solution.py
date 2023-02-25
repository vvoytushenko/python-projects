import os
import requests

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error as mape

import itertools

# checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# download data if  it is unavailable
if 'data.csv' not in os.listdir('../Data'):
    url = "https://www.dropbox.com/s/3cml50uv7zm46ly/data.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/data.csv', 'wb').write(r.content)

# read data
#df = pd.read_csv('..\data.csv')



# write your code here
#1. Load the dataframe using the pandas.read_csv method;
df = pd.read_csv('..\data.csv')

#2. Make X a dataframe with a predictor rating and y a series with a target salary;
X = df[["rating"]]
y = df[["salary"]]

#3. Split predictor and target into training and test parts.
    #Use test_size=0.3
    #and random_state=100 parameters — they guarantee that the results will be as expected;
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

#4. Fit the linear regression model with the following formula on the training data: salary?rating.
model = LinearRegression()
model.fit(X_train, y_train)

#5. Predict a salary with the fitted model on test data and calculate the MAPE;
y_pred = model.predict(X_test)

#6. Print three float numbers: the model intercept, the slope, and the MAPE rounded to five digits after the dot and separated by whitespace.
intercept1 = float((model.intercept_.flatten()).round(5))
slope1 = float((model.coef_.flatten()).round(5))
mape1 = float((mape(y_test, y_pred)).round(5))
#print(f"{intercept} {slope} {mape}")




#1. Load the data with pandas.read_csv;
df = pd.read_csv('..\data.csv')
mape_list = []

# Make X a dataframe with a predictor rating and y a series with a target salary;
X = df[["rating"]]
y = df[["salary"]]

# 2. Raise predictor to the power of 2.
for i in range(2, 5):
    X_new = X ** i

    # Split the predictors and target into training and test parts.
    # Use test_size=0.3
    # and random_state=100 parameters — they guarantee that the results will be as expected;
    X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.3, random_state=100)

    # Fit the linear model of salary on rating, make predictions and calculate the MAPE;
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Repeat steps 2–5 for the power of 3 and 4;
    y_predict = model.predict(X_test)
    mape_list.append(mape(y_test, y_predict))

# 3. Print the best MAPE obtained by fitting and running the models described above. The MAPE is a float number rounded to five digits after the dot.
#print(round(min(mape_list), 5))





#Read the data. For downloading the dataset refer to Stage 1;
#Load data with pandas.read_csv;
df = pd.read_csv('..\data.csv')

#Make X a dataframe with predictors and y a series with a target.
    #To make X, you must drop target variable from the data.
    #All other variables are left unchanged.
X = df[["rating", "draft_round", "age", "experience", "bmi"]]
y = df["salary"]

#Split the predictors and target into training and test parts.
    #Use test_size=0.3
    #and random_state=100 — they guarantee that the results will be the same as the test system expects.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)


#Fit the model predicting salary based on all other variables;
model = LinearRegression()
model.fit(X_train, y_train)

#Print the model coefficients separated by a comma.
#print(*model.coef_, sep=', ')




# Read the data. For downloading the dataset refer to Stage 1;
# 1. Load the data with pandas.read_csv;
df = pd.read_csv('..\data.csv')

# 2. Calculate the correlation matrix for the numeric variables;
corr_df = df.drop('salary', axis=1).corr()
correlated_features = []

# Find the variables where the correlation coefficient is greater than 0.2. Hint: there should be three of them.
for i in range(corr_df.shape[0]):
    for j in range(0, i):
        if corr_df.iloc[i, j] > 0.2:
            if corr_df.columns[i] not in correlated_features:
                correlated_features.append(corr_df.columns[i])
            if corr_df.columns[j] not in correlated_features:
                correlated_features.append(corr_df.columns[j])

# 3. Make X, a dataframe with all the predictor variables, and y, a series with the target.
X = df.select_dtypes('number').drop(columns='salary')
y = df['salary']

# 4. Split the predictors and the target into training and test parts.
    # Use test_size=0.3
    # and random_state=100 — they guarantee that the results will be as expected.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

# 5. Fit the linear models for salary prediction based on the subsets of other variables. The subsets are as follows.
    # First, try to remove each of the three variables you've found in Stage 4.
    # Second, remove each possible pair of these three variables.
    # For example, if you have found out that the highly correlated variables are x, y, and z,
        # then first you fit a model where x is removed,
        # then a model without y,
        # and then the model without z.
        # After this, you estimate the model without both x and y, then without both y and z, and last, without both x and z.
            # As a result, you will have six models to choose the best from.
model = LinearRegression()
mape_list = []

for i in range(1, len(correlated_features)):
    for combination in itertools.combinations(correlated_features, i):
        new_X_train = X_train.drop(columns=list(combination))
        new_X_test = X_test.drop(columns=list(combination))
        model.fit(new_X_train, y_train)
        y_predict = model.predict(new_X_test)
        mape_list.append(mape(y_test, y_predict))

# 6. Make predictions and print the lowest MAPE. The MAPE is a floating number rounded to five digits after the decimal separator.
#print(round(min(mape_list), 5))




# Read the data. For downloading the dataset refer to Stage 1;
# 1. Load data with pandas.read_csv;
df = pd.read_csv('..\data.csv')

# 2. As predictors select those variables that gave the best metric in the previous stage.
    # Make X a dataframe with predictors and y a series with a target.
    # To make X, you must drop target variable from the data.
X = df.select_dtypes('number').drop(columns=["age", "experience", "salary"])
y = df["salary"]

# 3. Split predictors and the target into train and test parts.
    # Use test_size=0.3
    # and random_state=100 — they guarantee that the results will be the same as the test system expects.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

# 4. Fit the model that predicts salary based on all other variables;
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Predict the salaries.
# 6. Try two techniques to deal with negative predictions:
    # replace the negative values with 0;
    # replace the negative values with the median of the training part of y.
y_pred1 = [max(i, 0) for i in model.predict(X_test)]
y_pred2 = [i if i < 0 else y_test.median() for i in iter(model.predict(X_test))]

# 7. Calculate the MAPE for every two options and print the best as a floating number rounded to five digits after the decimal separator.
print(min([mape(y_test, y_pred1), mape(y_test, y_pred2)]))