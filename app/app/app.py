from flask import Flask, render_template, request
import sqlite3
import pandas as pd
from scrape import H1B_Scraper  # Replace with the actual name of your scraper script

app = Flask(__name__)

@app.cli.command("scrape")
def initialize_database():
    try:
        scraper = H1B_Scraper()
        data = scraper.scrape([2020, 2023], ['Software Engineer', 'Data Scientist'])

        print(data.head())
        load_data_into_database(data)
        print("Database initialized with scraped data.")
    except Exception as e:
        print(f"Error initializing database: {e}")

def load_data_into_database(data):
    conn = sqlite3.connect('h1b_data.db')
    data.to_sql('h1b_jobs', conn, if_exists='replace', index=False)
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    job_title = request.form['job_title']
    conn = sqlite3.connect('h1b_data.db')
    cursor = conn.cursor()
    query = "SELECT * FROM h1b_jobs WHERE `JOB TITLE` LIKE ? LIMIT 50"
    parameters = ('%' + job_title + '%',)
    cursor.execute(query, parameters)
    jobs = cursor.fetchall()
    conn.close()
    return render_template('search_results.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
