from glassdoor.scrape_glassdoor import scrape_glassdoor_jobs
from h1b.scrape_h1b import H1B_Scraper
from linkedin.scrape_linkedin import scrape_linkedin_jobs
from dotenv import load_dotenv
from constants import LINKEDIN_SCRAPED, GLASSDOOR_SCRAPED, H1B_SCRAPED
import os


def main():
    load_dotenv()

    # Scrape Glassdoor jobs
    try:
        technologies = ["Python", "Java", "JavaScript", "C++", "C#",
                        "Ruby", "Swift", "Kotlin", "Go", "Rust", "Scala", "TypeScript"]
        locations = {
            "San-Jose-CA-US": "IC1147436",
            "San-Francisco-CA-US": "IC1147401",
            "Seattle-WA-US": "IC1150505",
            "Boston-MA-US": "IC1154532",
            "San-Diego-CA-US": "IC1147311",
            "Los-Angeles-CA-US": "IC1146821",
            "Austin-TX-US": "IC1139761",
            "Washington-DC-US": "IC1138213",
            "New-York-NY-US": "IC1132348",
            "Raleigh-NC-US": "IC1138960",
            "Denver-CO-US": "IC1148170",
            "Atlanta-GA-US": "IC1155583",
            "Chicago-IL-US": "IC1128808",
            "Dallas-TX-US": "IC1139977",
            "Houston-TX-US": "IC1140171",
            "Minneapolis-MN-US": "IC1142551",
            "Philadelphia-PA-US": "IC1152672",
            "Portland-OR-US": "IC1151614",
            "Charlotte-NC-US": "IC1138644",
            "Tampa-FL-US": "IC1154429"
        }

        print("Scraping Glassdoor jobs...")
        scrape_glassdoor_jobs(technologies, locations, os.getenv(
            'CHROME_DRIVER_PATH'), GLASSDOOR_SCRAPED)
        print("Glassdoor jobs scraped successfully!")
    except Exception as e:
        print(f"Error scraping Glassdoor jobs: {e}")

    # Scrape H1B data
    try:
        print("Scraping H1B data...")
        scraper = H1B_Scraper()
        h1b_data = scraper.scrape([2018, 2019, 2020, 2021, 2022, 2023], ['Software Engineer', 'Data Scientist',
                                  'Product Manager', 'Graphic Designer', 'Marketing Manager', 'Sales'])
        h1b_data.to_csv(H1B_SCRAPED, index=False)
        print("H1B data scraped successfully!")
    except Exception as e:
        print(f"Error scraping H1B data: {e}")

    # Scrape LinkedIn jobs
    try:
        print("Scraping LinkedIn jobs...")
        job_roles = ['Software Engineer', 'Data Scientist',
                     'Product Manager', 'Graphic Designer', 'Marketing Manager', 'Sales']
        df = scrape_linkedin_jobs(job_roles, 30)
        df.to_csv(LINKEDIN_SCRAPED, index=False)
        print("LinkedIn jobs scraped successfully!")
    except Exception as e:
        print(f"Error scraping LinkedIn jobs: {e}")


if __name__ == "__main__":
    print("Starting scrape jobs for Linkedin, Glassdoor and H1B.")
    print("This will take approximately 25 minutes to complete.")

    main()

    print("Scraping complete!")
    print("You can now run the data processing script to clean and aggregate the data.")
