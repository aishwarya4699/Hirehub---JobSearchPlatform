import streamlit as st
import pandas as pd
import numpy as np

def main_dashboard():
    st.subheader("Current Jobs Dashboard")

    # Load data from CSV file

    df = pd.read_csv("data_processing/processed_aggregated_data.csv")
    if 'Unnamed: 0.2' in df.columns:
        df = df.drop(columns=['Unnamed: 0.2'])

    # Convert 'min_salary' and 'max_salary' to numeric types, handling non-numeric values
    df['min_salary'] = pd.to_numeric(df['min_salary'], errors='coerce')
    df['max_salary'] = pd.to_numeric(df['max_salary'], errors='coerce')

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    col7 = st.columns(1)[0]
    col8 = st.columns(1)[0]

    with col1:
        company = st.text_input("Filter by Company", key='company_filter')
    with col2:
        job_title = st.text_input("Filter by Job Title", key='job_title_filter')
    with col3:
        min_salary = st.number_input("Minimum Salary", min_value=0, step=1000, key='min_salary_filter')
    with col4:
        max_salary = st.number_input("Maximum Salary", min_value=0, step=1000, key='max_salary_filter')
    with col5:
        location = st.text_input("Filter by Location", key='location_filter')
    with col6:
        job_type = st.text_input("Filter by Job Type", key='job_type_filter')
    with col7:
        tech_filter = st.text_input("Filter by Technologies (e.g., 'Python, Java')", key='tech_filter')
    with col8:
        h1b_sponsorship = st.checkbox("Filter by H1B Sponsorship", key='h1b_sponsorship_filter')

    # Filtering logic using Pandas
    if company:
        df = df[df['employer'].str.contains(company, case=False, na=False)]
    if job_title:
        df = df[df['job_title'].str.contains(job_title, case=False, na=False)]
    if location:
        df = df[df['location'].str.contains(location, case=False, na=False)]
    if min_salary > 0:
        df = df[df['min_salary'] >= min_salary]
    if max_salary > 0:
        df = df[df['max_salary'] <= max_salary]
    if job_type:
        df = df[df['job_type'].str.contains(job_type, case=False, na=False)]
    if tech_filter:
        tech_list = [tech.strip().lower() for tech in tech_filter.split(',')]
        df = df[df['tech'].apply(lambda x: any(tech in str(x).lower() for tech in tech_list))]

    # H1B Sponsorship filtering
    if h1b_sponsorship:
        h1b_companies = pd.read_csv("scrape/h1b/scrape_h1b.csv")
        h1b_companies_list = h1b_companies['EMPLOYER'].dropna().str.lower().unique()

        # Function to check if any H1B company name contains the employer name as a substring
        def is_h1b_sponsor(employer):
            employer_lower = employer.lower()
            return any(employer_lower in h1b_company for h1b_company in h1b_companies_list)

        # Filter the DataFrame
        df['employer'] = df['employer'].astype(str)  # Ensure 'employer' is string
        df = df[df['employer'].apply(is_h1b_sponsor)]

    # Renaming columns and replacing values
    rename_dict = {
        'employer': 'Employer',
        'job_title': 'Job Title',
        'location': 'Location',
        'tech': 'Technology',
        'job_type': 'Job Type',
        'min_salary': 'Min Salary',
        'max_salary': 'Max Salary'
    }
    df.rename(columns=rename_dict, inplace=True)
    replace_values = [None, 'None', 'Null', 'NaN', 'Not Applicable']
    df.replace(replace_values, 'N/A', inplace=True)

    # ignore any row which has N/A or null in employer
    # df = df[df['Employer'] not in ['N/A', None]]

    # reset th index start from 1
    df.reset_index(drop=True, inplace=True)

    st.dataframe(df, width=1200, height=600)