import requests_cache
import requests
import typer
import re

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from typing import Optional

# Set up caching for use with all requests as default
requests_cache.install_cache('scraping-cache', backend='sqlite')
scrape_app = typer.Typer()

@scrape_app.command()
def scrape(job: str = typer.Option(..., help="Job title to search on indeed."),
           loc: str = typer.Option(..., help="Location of job."),
           salary: Optional[str] = typer.Option(None, help="Minimum salary to use in search."),
           no_cache: Optional[bool] = typer.Option(False, help="Whether to bypass locally cached search.")):
    """
    Executes a web scrape on the Australian site of indeed.com for a given job in a given location.
    Extracts all items of value, including ratings and job descriptions, and collates them in a pandas dataframe.
    Args:
        job: (str) The job title to use in the search.
        loc: (str) The location to use in the search.
        salary: (str) optional, minimum salary to use in search.
        no_cache: (bool) optional, whether to bypass the local web cache from previous searches.

    Returns:
        None
    """
    # Prepare job and location strings for insertion into search request
    # TODO: add further checks for non-compatible symbols in job string (multiple plusses do not affect search)
    # TODO: change fixed query signifiers to arguments
    # TODO: allow flexible salary entry
    job_url = "q=" + "+".join(job.split(" "))
    loc_url = "&l=" + "+".join(loc.split(" "))
    if salary:
        job_url = job_url + "+" + salary

    # Prepare search parameters
    base_url = "https://au.indeed.com/jobs?" + job_url + loc_url
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'}

    # Run request and gather all possible results
    print("Attempting web scrape...")
    if no_cache:
        with requests_cache.disabled():
            result = requests.get(base_url, headers=headers)
    else:
        result = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(result.text, features='html.parser')
    num_results = soup.find("div", {"id": "searchCountPages"})
    num_results = int(re.findall("\d+(?=\sjob)", num_results.text)[0])
    job_results = soup.findAll("div", class_="jobsearch-SerpJobCard")
    # Repeat scrape if not all results are contained on page
    if num_results > 10:
        for num in range(10, num_results + 9, 10):
            page_url = base_url + f"&start={num}"
            if no_cache:
                with requests_cache.disabled():
                    result = requests.get(page_url, headers= headers)
            else:
                result = requests.get(page_url, headers=headers)
            soup = BeautifulSoup(result.text, features='html.parser')
            new_results = soup.findAll("div", class_="jobsearch-SerpJobCard")
            job_results += new_results

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


@scrape_app.command()
def filter(job: Optional[str] = typer.Option(None, help="Search string to filter job titles."),
           rating: Optional[str] = typer.Option(None, help="Minimum rating value to filter companies"),
           salary: Optional[str] = typer.Option(None, help="Minimum salary to filter job offers"),
           save: Optional[str] = typer.Option(None, help="If given, saves results file as json")):
    """
    Filters job results based on job title, company rating or minimum salary.
    Outputs results to screen or, if chosen, saves as json.
    Args:
        job: filter term for job title
        rating: minimum value for company rating
        salary: minimum salary for job offer
        save: (str) (optional) filename for results

    Returns:
        None
    """
    # Open existing results dataframe
    results = pd.read_pickle("temp_scrape_results.pkl")

    # Filter by values
    if job:
        results = results[results["Job Title"].str.contains(job)]
    if rating:
        results = results[results["Rating"] >= int(rating)]
    if salary:
        results = results[results["Salary"] >= int(salary)]

    if not save:
        print(results)
    else:
        if ".json" in save:
            filename = save
        else:
            filename = save + ".json"
        results.to_json(filename, orient="index")

@scrape_app.command()
def clear_cache():
    """
    Clears current requests cache.
    """
    print("Clearing cache...")
    requests_cache.patcher.clear()
    print("Done!")

if __name__ == "__main__":
    scrape_app()