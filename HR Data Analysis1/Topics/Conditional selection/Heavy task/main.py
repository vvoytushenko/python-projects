import pandas as pd

penguins_dict = {'species': {0: 'Gentoo', 1: 'Gentoo', 2: 'Adelie', 3: 'Chinstrap', 4: 'Adelie', 5: 'Adelie'}, 'body_mass_g': {0: 5550.0, 1: 5850.0, 2: 3975.0, 3: 4050.0, 4: 3200.0, 5: 4700.0}, 'sex': {0: 'MALE', 1: 'MALE', 2: 'MALE', 3: 'MALE', 4: 'FEMALE', 5: 'MALE'}}

penguins_df = pd.DataFrame(penguins_dict)

# your code here
print(penguins_df.loc[penguins_df['body_mass_g'] > 4500, ['body_mass_g']])