import pandas as pd
import os
import requests
import re
from dateutil.parser import parse
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'Nobel_laureates.json' not in os.listdir('../Data'):
        print('Nobel_laureates.json')
        url = "https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1"
        r = requests.get(url, allow_redirects=True)
        with open('../Data/Nobel_laureates.json', 'wb') as f:
            f.write(r.content)
        print('Loaded.')

    # 1. Load the dataset from the JSON file;
    df = pd.read_json('../Data/Nobel_laureates.json')

    # 2. Explore the data and check what the axes are, get the shape of the DataFrame,
    # use .info() to check for the data types and whether there are any missing values;
    #df.info()

    # 3. Use the .duplicated() method to check whether there are any duplicate rows.
    # Print False if there are no duplicate rows, otherwise print True.
    #print(df.duplicated().any())

    # 4. Drop all the rows where the gender column does not contain any values.
    # Hint: use the subset parameter of the .dropna() method in pandas.
    # 5. Re-index the DataFrame so that the index contains consecutive numbers.
    # Do not forget to remove the old index column.
    df = df.dropna(subset='gender').reset_index(drop=True)
    #print(df[['country', 'name']].head(20).to_dict())



    # 1. Extract the country names from the place_of_birth column.
    # Typically, this column contains the name of the city and, sometimes, the country of birth.
    # The values are separated by a comma.
    # To extract the country, split each column value by comma (if it is present) and take the last value.
    # Apply .strip() to the Python string to remove the excessive white spaces.
    # If no comma is present in the column value, replace the value with None;
    for i in range(0, df.shape[0]):
        if df.iloc[i, 0] == '':
            if re.findall(',', str(df.iloc[i, 8])):
                df.iloc[i, 0] = (df.iloc[i, 8]).split(',')[-1].strip()
            else:
                df.iloc[i, 0] = None

    # 2. Fill the born_in empty values with the new values of the place_of_birth column.
    # If the born_in column still contains empty values, drop the respective rows.
    # Reset the DataFrame index;
    df.dropna(subset=['born_in'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # 3. Modify the names of countries — replace US, United States, and U.S with USA, and United Kingdom with UK.
    df = df.replace({'born_in': {'US': 'USA', 'United States': 'USA', 'U.S.': 'USA', 'United Kingdom': 'UK'}})

    # 4. As a result, output a list of born_in column values.
    #print(df['born_in'].tolist())




    # Calculate the age when a laureate received the Nobel Prize.
        #  Use the information present in the dataset to get it.
    # 1. The dates of birth are present in 3 formats: 26 April 1932, 1951-3-26, December 13, 1923.
        # Generate a new column, representing a year each Nobel Laureate was born.
    df['year_of_birth'] = df.apply(lambda x: parse(x['date_of_birth'], fuzzy=True).year, axis=1)

    # 2. Create a new column, representing the age of winning the prize.
        # It is the year of winning the prize minus the year of birth.
    df['winning_age'] = df['year'] - df['year_of_birth']

    # 3. As a result of this stage, output two lists
        # the year of birth column values
        # and the age of obtaining the prize column values, separated by a new line character ("\n").
        # Use the .to_list() method of Series.
    #print(f"{df['year_of_birth'].to_list()}\n{df['winning_age'].to_list()}")

    # Plot the exact pie chart as depicted below, using the country of birth information.
    # Re-code the countries.
    # If the number of the Nobel Laureates born in the country is less than 25, re-code it to the Other countries group;
    country_count_dict = {country: len(df[df.born_in == country]) for country in df.born_in.unique()}
    pie_data = []

    for country in df.born_in:
        if country_count_dict[country] < 25:
            pie_data.append('Other countries')
        else:
            pie_data.append(country)

    pie_data = pd.Series(pie_data)
    data = pie_data.value_counts().tolist()
    labels = pie_data.value_counts().index

    # Use the following colors: blue, orange, red, yellow, green, pink, brown, cyan, purple;
    colors = ['blue', 'orange', 'red', 'yellow', 'green', 'pink', 'brown', 'cyan', 'purple']

    # Set figure size to (12, 12);
    #plt.figure(figsize=(12, 12))

    # For countries whose slices are exploded, set the explode parameter to 0.08.
    #explode = [0, 0, 0, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]

    # Hint: the format of the text displayed on the slices is {:.2f}%\n({:.0f}).
    #plt.pie(data, labels=labels, colors=colors, explode=explode,
            #autopct=lambda p: f'{p:.2f}%\n({p * sum(data) / 100 :.0f})')
    #plt.show()




    # Generate the following grouped bar plot:
    # 1. Set figure size to (10, 10);
    # 2. The bar centers are moved by 0.2 from the tick center, the width of bars is 0.4;
    # 3. The axis font size is 14, the plot font size is 20.

    df = df[df.category != '']
    male_count = df[df.gender == 'male'].groupby(['category']).count()['born_in']
    category = male_count.index
    male = male_count.tolist()
    female = df[df.gender == 'female'].groupby(['category']).count()['born_in'].tolist()
    x_axis = np.arange(len(category))

    #plt.figure(figsize=(10, 10))
    #plt.bar(x_axis - 0.2, male, width=0.4, label='Males')
    #plt.bar(x_axis + 0.2, female, width=0.4, label='Females')
    #plt.xticks(x_axis, category)
    #plt.xlabel('Category', fontsize=14)
    #plt.ylabel('Nobel Laureates Count', fontsize=14)
    #plt.title('The total count of male and female Nobel Prize winners in each category', fontsize=20)
    #plt.legend()
    #plt.show()




    # Generate a box plot for ages of getting the Nobel Prize for each category:
        # Set figure size to (10, 10);
        # Set the font size of the axis labels to 14 and the font size of the plot label is 20.
    cat_data = {}
    all_categories = []
    for cat in df['category'].unique():
        values = df[df['category'] == cat]['winning_age'].tolist()
        cat_data[cat] = values
        all_categories.extend(values)
    cat_data['All categories'] = all_categories

    plt.figure(figsize=(10, 10))
    plt.boxplot(cat_data.values(), labels=cat_data.keys(), showmeans=True)
    plt.title('The total count of male and female Nobel Prize winners in each category', fontsize=20)
    plt.ylabel('Age of obtaining the Nobel Price', fontsize=14)
    plt.xlabel('Category', fontsize=14)
    plt.show()