import streamlit as st
import pandas as pd
import numpy as np

def h1b_job_insights():
    st.subheader("H1B Job Insights")

    # Load data from CSV file
    df = pd.read_csv("scrape/h1b/scrape_h1b.csv")

    col1, col2 = st.columns(2)  # First row of columns
    col3, col4 = st.columns(2)  # Second row of columns
    col5, col6 = st.columns(2)  # Third row of columns

    with col1:
        employer = st.text_input("Search by Employer")
    with col2:
        job_title = st.text_input("Search by Job Title")
    with col3:
        min_salary = st.number_input("Minimum Salary", value=0, step=10000)
    with col4:
        max_salary = st.number_input("Maximum Salary", value=0, step=10000)
    with col5:
        location = st.text_input("Search by Location")
    with col6:
        year = st.selectbox("Select Year", options=["", "2020", "2021", "2022"], index=0)

    # Filtering logic using Pandas
    if employer:
        df = df[df['EMPLOYER'].str.contains(employer, case=False, na=False)]
    if job_title:
        df = df[df['JOB TITLE'].str.contains(job_title, case=False, na=False)]
    if min_salary > 0:
        df = df[df['BASE SALARY'] >= min_salary]
    if max_salary > 0:
        df = df[df['BASE SALARY'] <= max_salary]
    if location:
        df = df[df['LOCATION'].str.contains(location, case=False, na=False)]
    if year:
        df = df[df['Year'] == year]

    df.reset_index(drop=True, inplace=True)
    st.dataframe(df, width=700, height=300)

# The main function to call our dashboard
def main():
    h1b_job_insights()

if __name__ == "__main__":
    main()
