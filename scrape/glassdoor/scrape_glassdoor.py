from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd


def scrape_glassdoor_jobs(technologies, locations, chromedriver_path, output_csv_path):
    """
    Scrapes job postings from Glassdoor for specified technologies and locations.

    Args:
        technologies (list): List of technologies to scrape jobs for.
        locations (dict): Dictionary of locations with corresponding Glassdoor location IDs.
        chromedriver_path (str): Path to the ChromeDriver executable.
        output_csv_path (str): Path to save the scraped data as a CSV file.
    """

    # Initialize the Selenium WebDriver
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)

    job_data = []

    for tech in technologies:
        for location, location_id in locations.items():
            # Generate the target URL
            target_url = generate_url(tech, location, location_id)

            print(f"Scraping {tech} jobs in {location} with URL: {target_url}...")

            # Scrape the webpage
            driver.get(target_url)
            driver.maximize_window()  # Maximizing the browser window is optional
            time.sleep(2)  # Wait for the page to load

            # Parse the page content
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            all_jobs = extract_job_data(soup, tech)

            # Append job data to the list
            job_data.extend(all_jobs)

            time.sleep(5)  # Pause before scraping the next page

    # Convert the job data to a DataFrame and save as a CSV file
    pd.DataFrame(job_data).to_csv(
        output_csv_path, index=False, encoding='utf-8')

    # Close the WebDriver
    driver.close()


def generate_url(tech, location, location_id):
    """
    Generates a Glassdoor URL for a given technology and location.

    Args:
        tech (str): Technology to search for.
        location (str): Location to search in.
        location_id (str): Glassdoor's location ID for the specified location.

    Returns:
        str: Generated URL.
    """
    formatted_location = location.lower().replace(", ", "-").replace(" ", "-")
    formatted_tech = tech.replace(" ", "-").lower()
    return f"https://www.glassdoor.com/Job/{formatted_location}-{formatted_tech}-jobs-SRCH_IL.0,{len(formatted_location)}_{location_id}_KO{len(formatted_location) + 1},{len(formatted_location) + 1 + len(formatted_tech)}.htm?clickSource=searchBox"


def extract_job_data(soup, tech):
    """
    Extracts job data from a BeautifulSoup object.

    Args:
        soup (BeautifulSoup): Parsed HTML content of the webpage.
        tech (str): Technology associated with the job listings.

    Returns:
        list: List of dictionaries containing job data.
    """
    jobs = []
    all_jobs_container = soup.find("ul", {"class": "JobsList_jobsList__Ey2Vo"})
    if all_jobs_container:
        for job in all_jobs_container.find_all("li"):
            jobs.append({
                "name-of-company": extract_text(job, "div", {"class": "EmployerProfile_profileContainer__d5rMb"}),
                "name-of-job": extract_text(job, "a", {"class": "JobCard_seoLink__WdqHZ"}),
                "location": extract_text(job, "div", {"class": "JobCard_location__N_iYE"}),
                "salary": extract_text(job, "div", {"class": "JobCard_salaryEstimate___m9kY"}),
                "tech": tech
            })
    return jobs


def extract_text(job_element, tag, attrs):
    """
    Extracts text from a specified HTML tag and attributes within a job element.

    Args:
        job_element (bs4.element.Tag): HTML element representing a job.
        tag (str): HTML tag to find.
        attrs (dict): Attributes of the HTML tag to find.

    Returns:
        str: Extracted text or None if not found.
    """
    element = job_element.find(tag, attrs)
    return element.text if element else None

