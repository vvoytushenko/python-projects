import pandas as pd
import os
import requests

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

    df = pd.read_json('../Data/Nobel_laureates.json')

    # Check for duplicates
    print(df.duplicated().any())

    # Drop missing gender values
    df = df.dropna(subset='gender').reset_index(drop=True)

    # Print the first 20 rows of the country and name columns
    print(df[['country', 'name']].head(20).to_dict())