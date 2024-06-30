import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse


def scrape_linkedin_jobs(job_roles, pages=1):
    """
    Scrapes job postings from LinkedIn for given job roles.

    Args:
    job_roles (list): A list of job roles to search for.
    pages (int): Number of pages to scrape for each job role.

    Returns:
    DataFrame: A pandas DataFrame containing details of the job postings.
    """
    base_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?'
    job_details = []

    for role in job_roles:
        for page in range(pages):
            job_ids = get_job_ids(base_url, role, page)
            for job_id in job_ids:
                job_details.append(get_job_details(job_id))

    return pd.DataFrame(job_details)


def get_job_ids(base_url, role, page):
    """
    Fetches job IDs for a specific role and page.

    Args:
    base_url (str): The base URL for LinkedIn job search.
    role (str): The job role to search for.
    page (int): The page number to scrape.

    Returns:
    list: A list of job IDs.
    """
    headers = get_headers()
    encoded_role = urllib.parse.quote(role)
    try:
        print(f"Fetching job IDs for {role} on page {page} with URL: {base_url}keywords={encoded_role}&start={page}")
        response = requests.get(
            f"{base_url}keywords={encoded_role}&start={page}", headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [job.find("div", {"class": "base-card"}).get('data-entity-urn').split(":")[3]
                for job in soup.find_all("li") if job.find("div", {"class": "base-card"})]
    except Exception as e:
        print(f"Error fetching job IDs: {e}")
        return []


def get_job_details(job_id):
    """
    Fetches details of a job posting using its job ID.

    Args:
    job_id (str): The ID of the job posting.

    Returns:
    dict: A dictionary containing details of the job posting.
    """
    headers = get_headers()
    try:
        response = requests.get(
            f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}', headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        job_info = {"company": None, "job-title": None,
                    "level": None, "employment type": None}

        # Extract job details
        job_info["company"] = extract_company(soup)
        job_info["job-title"] = extract_job_title(soup)
        job_info.update(extract_job_criteria(soup))

        return job_info
    except Exception as e:
        print(f"Error fetching job details: {e}")
        return {"company": None, "job-title": None, "level": None, "employment type": None}


def get_headers():
    """
    Returns the headers to be used in the requests.

    Returns:
    dict: Headers for the request.
    """
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }


def extract_company(soup):
    """
    Extracts company name from the soup object.

    Args:
    soup (BeautifulSoup): BeautifulSoup object of the job posting page.

    Returns:
    str: The name of the company.
    """
    try:
        top_card = soup.find("div", {"class": "top-card-layout__card"})
        if top_card:
            img = top_card.find("a").find("img")
            if img:
                return img.get('alt')
    except Exception as e:
        print(f"Error extracting company: {e}")
    return None


def extract_job_title(soup):
    """
    Extracts job title from the soup object.

    Args:
    soup (BeautifulSoup): BeautifulSoup object of the job posting page.

    Returns:
    str: The job title.
    """
    try:
        entity_info = soup.find(
            "div", {"class": "top-card-layout__entity-info"})
        if entity_info:
            a_tag = entity_info.find("a")
            if a_tag:
                return a_tag.text.strip()
    except Exception as e:
        print(f"Error extracting job title: {e}")
    return None


def extract_job_criteria(soup):
    """
    Extracts job criteria like level and employment type from the soup object.

    Args:
    soup (BeautifulSoup): BeautifulSoup object of the job posting page.

    Returns:
    dict: A dictionary containing the job level and employment type.
    """
    criteria = {"level": None, "employment type": None}
    try:
        job_criteria_list = soup.find(
            "ul", {"class": "description__job-criteria-list"})
        if job_criteria_list:
            li_tags = job_criteria_list.find_all("li")
            for li in li_tags:
                if "Seniority level" in li.text:
                    criteria["level"] = li.text.replace(
                        "Seniority level", "").strip()
                elif "Employment type" in li.text:
                    span_tag = li.find(
                        "span", {"class": "description__job-criteria-text--criteria"})
                    if span_tag:
                        criteria["employment type"] = span_tag.text.strip()
    except Exception as e:
        print(f"Error extracting job criteria: {e}")
    return criteria


if __name__ == "__main__":
    job_roles = ['Software Engineer']
    df = scrape_linkedin_jobs(job_roles, 2)
    print(df.head())
    df.to_csv("scrape/linkedin/test_linkedin_jobs.csv", index=False)
    print("LinkedIn jobs scraped successfully!")
