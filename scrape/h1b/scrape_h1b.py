import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import logging

class HTMLTableParser:
    """
    A class to parse HTML tables from a given URL.
    """

    def __init__(self):
        """Initializes the HTMLTableParser with a logger."""
        self.logger = logging.getLogger(self.__class__.__name__)

    def parse(self, url):
        """
        Parses tables from a given URL into a list of pandas DataFrames.

        Args:
            url (str): URL of the webpage to scrape tables from.

        Returns:
            list: A list of pandas DataFrames, each representing an HTML table.
        """
        try:
            if not isinstance(url, str):
                raise ValueError("URL must be a string")
            soup = self.read_url(url)
            return self.obtain_tables(soup)
        except Exception as e:
            self.logger.error(f"Error parsing URL {url}: {e}")
            return []

    def read_url(self, url):
        """
        Reads HTML content from a URL.

        Args:
            url (str): URL to read.

        Returns:
            BeautifulSoup: BeautifulSoup object representing the webpage content.
        """
        try:
            response = urllib.request.urlopen(url)
            page_source = response.read()
            return BeautifulSoup(page_source, 'lxml')
        except Exception as e:
            self.logger.error(f"Error reading URL {url}: {e}")
            return BeautifulSoup('', 'lxml')

    def obtain_tables(self, soup):
        """
        Extracts tables from a BeautifulSoup object.

        Args:
            soup (BeautifulSoup): BeautifulSoup object of a webpage.

        Returns:
            list: A list of pandas DataFrames.
        """
        return [self.parse_html_table(table) for table in soup.find_all('table') if not self.parse_html_table(table).empty]

    def parse_html_table(self, table):
        """
        Parses an HTML table into a pandas DataFrame.

        Args:
            table (bs4.element.Tag): HTML table element to parse.

        Returns:
            pd.DataFrame: DataFrame representation of the HTML table.
        """
        rows = table.find_all('tr')
        header = [th.get_text(strip=True) for th in rows[0].find_all('th')]
        data = [[td.get_text(strip=True) for td in tr.find_all('td')] for tr in rows[1:]]
        return pd.DataFrame(data, columns=header)


class H1B_Scraper:
    """
    A class to scrape H1B visa data for specific job titles and years.
    """

    def __init__(self):
        """Initializes the H1B_Scraper with an HTMLTableParser and a logger."""
        self.parser = HTMLTableParser()
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def str2int(df, column):
        """
        Converts a string column in a DataFrame to integers.

        Args:
            df (pd.DataFrame): DataFrame containing the column.
            column (str): Name of the column to convert.
        """
        try:
            df[column] = pd.to_numeric(df[column].str.replace(',', ''), errors='coerce').astype('Int64')
        except Exception as e:
            logging.error(f"Error converting string to int in column {column}: {e}")

    def scrape(self, years, jobs):
        """
        Scrapes H1B data for given years and job titles.

        Args:
            years (list or tuple): Years to scrape data for.
            jobs (list or tuple): Job titles to scrape data for.

        Returns:
            pd.DataFrame: DataFrame containing the scraped H1B data.
        """
        if not isinstance(years, (list, tuple)):
            raise TypeError("years should be list or tuple")
        if not isinstance(jobs, (list, tuple)):
            raise TypeError("jobs should be list or tuple")

        all_data = pd.DataFrame()
        for year in years:
            for job in jobs:
                url = f"https://h1bdata.info/index.php?em=&job={urllib.parse.quote_plus(job)}&city=&year={year}"
                print(f"Scraping URL: {url} for year {year} and job {job}")
                tables = self.parser.parse(url)
                for table in tables:
                    self.str2int(table, 'BASE SALARY')
                    table['Year'] = year
                    all_data = pd.concat([all_data, table], ignore_index=True)

        return all_data

