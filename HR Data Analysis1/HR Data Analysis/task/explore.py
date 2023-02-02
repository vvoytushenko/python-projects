import pandas as pd
import requests
import os

# scroll down to the bottom to implement your solution

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
        'B_office_data.xml' not in os.listdir('../Data') and
        'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # write your code here
    office_a = pd.read_xml("../Data/A_office_data.xml")
    office_b = pd.read_xml("../Data/B_office_data.xml")
    hr = pd.read_xml("../Data/hr_data.xml")
    office_a.index = [f"A{num}" for num in office_a['employee_office_id'].tolist()]
    office_b.index = [f"B{num}" for num in office_b['employee_office_id'].tolist()]
    hr.index = hr['employee_id'].tolist()
    #print(office_a.index.tolist())
    #print(office_b.index.tolist())
    #print(hr.index.tolist())


    # Use the concat() function from pandas to generate a unified dataset for offices A and B
    office_df = pd.concat([office_a, office_b])

    # Use df.merge() to carry out the left merging of the unified office dataset with HR's dataset.
    # Merge both datasets by index.
    # For the final table, leave only those employees whose data is contained in both datasets.
    # Set indicator=True in df.merge();
    df = pd.merge(office_df, hr, left_index=True, right_index=True, indicator=True)

    # Drop the employee_office_id, employee_id columns and the column that contains a row source;
    df = df.drop(['employee_office_id', 'employee_id', '_merge'], axis=1)

    # Sort the final dataset by index and print two Python lists:
    # the final DataFrame index and the column names.
    # Output each list on a separate line.
    df.sort_index(inplace=True)
    #print(df.index.tolist())
    #print(df.columns.tolist())


    # The HR boss asks for the following metrics:
        # the median number of projects the employees in a group worked upon,
            # and how many employees worked on more than five projects;
        # the mean and median time spent in the company;
        # the share of employees who've had work accidents;
        # the mean and standard deviation of the last evaluation score
    # Print the resulting table as a Python dictionary. To do so, use the to_dict() method.
    def count_bigger_5(arr):
        return sum(arr > 5)

    metrics = df.groupby("left").agg({"number_project": ["median", count_bigger_5],
                                      "time_spend_company": ["mean", "median"],
                                      "Work_accident": ["mean"],
                                      "last_evaluation": ["mean", "std"], }
                                     ).round(2).to_dict()
    #print(metrics)

    #The HR boss desperately needs your pivot tables for their report.
    working_hours = df.pivot_table(index='Department',
                                   columns=['left', 'salary'],
                                   values='average_monthly_hours',
                                   aggfunc='median')

    # For the currently employed:
    #    the median value of the working hours of high-salary employees is
    #    smaller
    #    than the hours of the medium-salary employees, OR:

    # For the employees who left:
    #    the median value of working hours of low-salary employees is
    #    smaller
    #    than the hours of high-salary employees
    wh = working_hours.loc[(working_hours[(0, 'high')] < working_hours[(0, 'medium')]) |
                           (working_hours[(1, 'low')] < working_hours[(1, 'high')])]
    print(wh.to_dict())


    evaluation_satisfaction = df.pivot_table(index='time_spend_company',
                                             columns=['promotion_last_5years'],
                                             values=['satisfaction_level', 'last_evaluation'],
                                             aggfunc=['min', 'max', 'mean'])
    # Filter the table by the following rule:
    #    select only those rows where
    #    the last mean evaluation score is
    #    higher
    #    for those who didn't have any promotion than those who had.

    es = evaluation_satisfaction.loc[(evaluation_satisfaction['mean', 'last_evaluation', 0] >
                                      evaluation_satisfaction['mean', 'last_evaluation', 1])]
    print(es.to_dict())