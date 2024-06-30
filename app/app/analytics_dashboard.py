import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dashboard import load_data

def analytics_tab():
    st.subheader("Data Analytics")

    # Fetch data from both tables
    h1b_data = pd.read_csv("scrape/h1b/scrape_h1b.csv")
    current_jobs_data = pd.read_csv("data_processing/processed_aggregated_data.csv")

    current_jobs_data['min_salary'] = pd.to_numeric(current_jobs_data['min_salary'], errors='coerce')
    current_jobs_data['max_salary'] = pd.to_numeric(current_jobs_data['max_salary'], errors='coerce')

    # You can choose to either drop NaN values or fill them with a default value (like 0)
    # To drop NaN values:
    current_jobs_data = current_jobs_data.dropna(subset=['min_salary', 'max_salary'])

    # H1B Data Analysis
    if not h1b_data.empty:
        st.subheader("H1B Jobs Salary Distribution")
        plt.figure(figsize=(10, 6))
        sns.histplot(h1b_data['BASE SALARY'], kde=True)
        plt.xlabel("Base Salary")
        plt.ylabel("Frequency")
        st.pyplot(plt)

        # 2. Top Employers in H1B Jobs
        st.subheader("Top Employers in H1B Jobs")
        top_employers = h1b_data['EMPLOYER'].value_counts().head(10)
        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_employers.values, y=top_employers.index)
        plt.xlabel("Number of Jobs")
        plt.ylabel("Employers")
        st.pyplot(plt)

        # 3. Job Distribution by Year
        st.subheader("Job Distribution by Year (H1B Jobs)")
        jobs_by_year = h1b_data['Year'].value_counts().sort_index()
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=jobs_by_year.index, y=jobs_by_year.values)
        plt.xlabel("Year")
        plt.ylabel("Number of Jobs")
        st.pyplot(plt)

        # 4. Job Titles Pie Chart
        st.subheader("Job Titles Distribution (H1B Jobs)")
        top_titles = h1b_data['JOB TITLE'].value_counts().head(5)
        plt.figure(figsize=(8, 8))
        plt.pie(top_titles, labels=top_titles.index, autopct='%1.1f%%')
        plt.title("Top 5 Job Titles")
        st.pyplot(plt)

    # Current Jobs Data Analysis
    if not current_jobs_data.empty:
        # 7. Technology Frequency
        # Assuming 'Tech' field contains comma-separated values
        tech_series = current_jobs_data['tech'].dropna().str.split(',').explode()
        tech_count = tech_series.value_counts().head(10)
        st.subheader("Technology Frequency (Current Jobs)")
        plt.figure(figsize=(10, 6))
        sns.barplot(x=tech_count.values, y=tech_count.index)
        plt.xlabel("Frequency")
        plt.ylabel("Technology")
        st.pyplot(plt)

        # 9. Company-wise Job Distribution
        st.subheader("Company-wise Job Distribution (Current Jobs)")
        company_job_dist = current_jobs_data['employer'].value_counts().head(10)
        plt.figure(figsize=(10, 6))
        sns.barplot(x=company_job_dist.values, y=company_job_dist.index)
        plt.xlabel("Number of Jobs")
        plt.ylabel("Company")
        st.pyplot(plt)

        # 10. Location-based Job Distribution
        st.subheader("Location-based Job Distribution (Current Jobs)")
        location_job_dist = current_jobs_data['location'].value_counts().head(10)
        plt.figure(figsize=(10, 6))
        sns.barplot(x=location_job_dist.values, y=location_job_dist.index)
        plt.xlabel("Number of Jobs")
        plt.ylabel("Location")
        st.pyplot(plt)

        if not h1b_data.empty and not current_jobs_data.empty:
            st.subheader("Average Base Salary Comparison")
            avg_salary_h1b = h1b_data['BASE SALARY'].mean()
            avg_salary_current = current_jobs_data[['min_salary', 'max_salary']].astype(float).mean(axis=1).mean()

            plt.figure(figsize=(10, 6))
            sns.barplot(x=['H1B Jobs', 'Current Jobs'], y=[avg_salary_h1b, avg_salary_current])
            plt.ylabel('Average Salary')
            st.pyplot(plt)

            # Salary Distribution for Current Jobs
            st.subheader("Salary Distribution (Current Jobs)")
            current_jobs_salaries = current_jobs_data[['min_salary', 'max_salary']].astype(float).mean(axis=1)
            plt.figure(figsize=(10, 6))
            sns.histplot(current_jobs_salaries, kde=True)
            plt.xlabel("Average Salary")
            plt.ylabel("Frequency")
            st.pyplot(plt)

            # Salary by Location (For either dataset if location data is consistent)
            st.subheader("Salary by Location")
            # Example for H1B data; replace with current_jobs_data if needed
            location_salary = h1b_data.groupby('LOCATION')['BASE SALARY'].mean().sort_values(ascending=False).head(10)
            plt.figure(figsize=(10, 6))
            sns.barplot(x=location_salary.values, y=location_salary.index)
            plt.xlabel("Average Salary")
            plt.ylabel("Location")
            st.pyplot(plt)

            # Tech-wise Salary Distribution (If applicable for current_jobs)
            if 'tech' in current_jobs_data.columns:
                st.subheader("Tech-wise Salary Distribution")
                tech_salary = current_jobs_data.dropna(subset=['tech'])
                tech_salary['average_salary'] = tech_salary[['min_salary', 'max_salary']].astype(float).mean(axis=1)
                tech_salary = tech_salary.explode('tech').groupby('tech')['average_salary'].mean().sort_values(ascending=False).head(10)
                plt.figure(figsize=(10, 6))
                sns.barplot(x=tech_salary.values, y=tech_salary.index)
                plt.xlabel("Average Salary")
                plt.ylabel("Technology")
                st.pyplot(plt)
