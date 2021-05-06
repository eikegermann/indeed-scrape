import requests_cache
import requests
import typer
import re

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from typing import (
    Optional, Tuple
)

def query_website(base_url: str,
                  no_cache: bool) -> object:
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'}
    # Run request and gather all possible results
    print("Attempting web scrape...")
    if no_cache:
        with requests_cache.disabled():
            result = requests.get(base_url, headers=headers)
    else:
        result = requests.get(base_url, headers=headers)
    return result


def extract_job_offers(result: object) -> Tuple[list, int]:
    soup = BeautifulSoup(result.text, features='html.parser')
    num_results = soup.find("div", {"id": "searchCountPages"})
    num_results = int(re.findall("\d+(?=\sjob)", num_results.text)[0])
    job_results = soup.findAll("div", class_="jobsearch-SerpJobCard")
    return job_results, num_results


def collate_jobs_data(job_results: list, num_results: int) -> None:
    # Collate job data in dataframe
    # TODO: Find nicer way to iterate
    job_title = []
    company = []
    location = []
    rating = []
    job_description = []
    age_of_ad = []
    job_salary = []
    print(f"Collating data for {num_results} jobs...")
    for entry in job_results:

        # Job title, company and location and age of ad are available for all entries by default
        job_title.append(entry.find("h2", class_=["title"]).text)
        company.append(entry.find("span", class_=["company"]).text)
        location.append(entry.find("span", class_=["location"]).text)
        age_of_ad.append(entry.find("span", class_=["date"]).text)

        # Ratings, descriptions and salaries are not always available
        # TODO: Get better default values or entry methods
        entry_rating = entry.findAll("span", class_=["ratingContent"])
        if len(entry_rating) > 0:
            rating.append(int(entry_rating[0].text))
        else:
            rating.append(0)
        entry_summary = entry.findAll("div", class_=["summary"])
        if len(entry_summary) > 0:
            job_description.append(entry_summary[0].text)
        else:
            job_description.append("N/A")
        entry_salary = entry.findAll("span", class_=["salaryText"])
        if len(entry_salary) > 0:
            salary_string = entry_salary[0].text
            cleaned_salary = salary_string.replace("$", "").replace(",", "")
            salary_values = re.findall("\d+", cleaned_salary)
            min_salary = np.min(list(map(int, salary_values)))
            job_salary.append(min_salary)
        else:
            job_salary.append(0)
    all_results = pd.DataFrame({"Job Title": job_title,
                                "Company": company,
                                "Rating": rating,
                                "Location": location,
                                "Age of ad": age_of_ad,
                                "Salary": job_salary,
                                "Description": job_description})
    # Save resulting frame for use with filter
    all_results.to_pickle("temp_scrape_results.pkl")
    print("Done!")