# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from constants import LINKEDIN_SCRAPED, GLASSDOOR_SCRAPED, H1B_SCRAPED, LINKEDIN_CLEANED_DATA, AGGREGATED_DATA, PROCESSED_AGGREGATED_DATA


def clean_linkedin_data(input_path, output_path):
    """
    Cleans the LinkedIn job data and saves the cleaned data to a new CSV file.
    @param input_path: Path to the input CSV file.
    @param output_path: Path to the output CSV file.
    """
    data = pd.read_csv(input_path)
    if 'employment type' in data.columns:
        data = data.drop(['employment type'], axis=1)
    data = data[data['company'].notna()]

    data['level'] = data['level'].str.replace(
        'Employment type\n\s*Full-time', 'Full-Time', regex=True)

    values_to_drop = ['Employment type\n        \n\n          Contract',
                      'Employment type\n        \n\n          Internship',
                      'Employment type\n        \n\n          Temporary']

    data = data[~data['level'].isin(values_to_drop)].reset_index(drop=True)

    data.to_csv(output_path)
    return data


def combine_tables(csv_file1, csv_file2, output_path):
    """
    Combines two CSV files into a single DataFrame and saves the result to a new CSV file.
    @param csv_file1: Path to the first CSV file.
    @param csv_file2: Path to the second CSV file.
    @param output_path: Path to the output CSV file.
    """
    # Read CSV files into DataFrames
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)

    # Rename columns in the second table to match the first table
    df2.rename(columns={'company': 'name-of-company',
               'job-title': 'name-of-job'}, inplace=True)

    # Add a new column 'level' with NA values for the first table
    df1['level'] = None

    # Append rows from the second table to the first table
    result = pd.concat([df1, df2], ignore_index=True, sort=False)

    result['name-of-company'] = result['name-of-company'].str.replace(r'\d+\.\d+', '', regex=True)
    print(result)
    result.to_csv(output_path)
    return result


def clean_salary_data(input_path, output_path):
    """
    Cleans the salary data and saves the cleaned data to a new CSV file.
    @param input_path: Path to the input CSV file.
    @param output_path: Path to the output CSV file.
    @return: Cleaned DataFrame.
    """
    data = pd.read_csv(input_path)

    data['salary'] = data['salary'].str.replace(
        '\(Employer est.\)', '', regex=True)
    data['salary'] = data['salary'].str.replace('(Per Hour)', '', regex=True)
    data['salary'] = data['salary'].str.replace(
        '\(Glassdoor est.\)', '', regex=True)

    def hourly_to_yearly(salary):
        if pd.isna(salary) or str(salary).lower() == 'not applicable':
            return 'Not Applicable', 'Not Applicable'
        elif ' - ' in salary:
            low, high = map(float, salary.replace(
                '$', '').replace('K', '000').split(' - '))
            return low, high
        else:
            try:
                single_value = float(salary.replace(
                    '$', '').replace('K', '000'))
                min_value = single_value * 0.6
                return min_value, single_value
            except ValueError:
                return 'Not Applicable', 'Not Applicable'

    data[['Min_Salary', 'Max_Salary']] = pd.DataFrame(
        data['salary'].apply(hourly_to_yearly).tolist(), index=data.index)

    for index, row in data.iterrows():
        if row['Min_Salary'] == 'Not Applicable':
            data.at[index, 'Min_Salary'] = 'Not Applicable'
        elif float(row['Min_Salary']) < 200.0:
            data.at[index, 'Min_Salary'] = float(row['Min_Salary']) * 40 * 52

    for index, row in data.iterrows():
        if row['Max_Salary'] == 'Not Applicable':
            data.at[index, 'Max_Salary'] = 'Not Applicable'
        elif float(row['Max_Salary']) < 200.0:
            data.at[index, 'Max_Salary'] = float(row['Max_Salary']) * 40 * 52

    data = data.drop(['salary', 'Unnamed: 0.1', 'Unnamed: 0'], axis=1)
    data = data.rename(columns={'name-of-company': 'employer', 'name-of-job': 'job_title', 'location': 'location',
                       'date-posted': 'submit_date', 'level': 'job_type', 'tech': 'tech', 'Min_Salary': 'min_salary', 'Max_Salary': 'max_salary'})
    data.to_csv(output_path, index=False)
    return data


# Clean LinkedIn job data
clean_linkedin_data(LINKEDIN_SCRAPED, LINKEDIN_CLEANED_DATA)

# Combine LinkedIn and Glassdoor job data
combine_tables(GLASSDOOR_SCRAPED, LINKEDIN_CLEANED_DATA, AGGREGATED_DATA)

# Clean salary data
clean_salary_data(AGGREGATED_DATA, PROCESSED_AGGREGATED_DATA)
