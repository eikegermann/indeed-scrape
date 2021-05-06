import requests_cache
import typer

from typing import Optional

from src.scrape.scrape import (
    query_website, extract_job_offers, collate_jobs_data, filter_results
)

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
    result = query_website(base_url, no_cache)
    job_results, num_results = extract_job_offers(result)
    # Repeat scrape if not all results are contained on page
    if num_results > 10:
        for num in range(10, num_results + 9, 10):
            page_url = base_url + f"&start={num}"
            result = query_website(page_url, no_cache)
            new_results, _ = extract_job_offers(result)
            job_results += new_results

    collate_jobs_data(job_results, num_results)

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
    filter_results(job, rating, salary, save)


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