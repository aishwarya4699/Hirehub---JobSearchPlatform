import pandas as pd
import numpy as np

def clean_scraped_data(file_path):
    """
    Cleans the scraped LinkedIn job data.

    Args:
    file_path (str): File path of the scraped CSV file.

    Returns:
    None: The function saves the cleaned data to a CSV file.
    """

    # Read the data from the CSV file
    data = pd.read_csv(file_path)

    # Dropping the 'employment type' column
    data.drop(['employment type'], axis=1, inplace=True)

    # Removing rows where 'company' is NaN
    data = data[data['company'].notna()]

    # Replace specific string patterns in 'level' column
    data['level'] = data['level'].str.replace(
        'Employment type\n\s*Full-time', 'Full-Time', regex=True)

    # Values to be dropped from 'level' column
    values_to_drop = ['Employment type\n        \n\n          Contract',
                      'Employment type\n        \n\n          Internship',
                      'Employment type\n        \n\n          Temporary']

    # Dropping the specified values and resetting index
    data = data[~data['level'].isin(values_to_drop)].reset_index(drop=True)

    # Save the cleaned data to a new CSV file
    data.to_csv('LinkedinFinalScrapedData.csv', index=False)


file_path = 'linkedin_jobs.csv'
clean_scraped_data(file_path)
