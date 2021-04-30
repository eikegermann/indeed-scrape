# Application - 🕸️ Web scraping

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/ghandic/PyCap-TODO-CRUD)
![coverage](https://img.shields.io/badge/coverage-0%25-red)

<description>

## Requirements

This program requires the following Python packages

- requests-cache
- pandas
- numpy
- typer
- bs4

They can be installed manually or using pip with the supplied `requirements.txt` by running the following

```bash
pip3 install -r requirements.txt
```

## Usage

The program can be run in a virtual environment (I recommend conda) with the command line:

```bash
python scrape.py [task] [options]
```
### Program options

The program's tasks and options can always be displayed with

```bash
python scrape.py --help
```
It currently supports 3 tasks as main functions:
- scrape
- filter
- clear-cache

#### Scrape 
The scrape function requires a minimum of two arguments to run, a string with a job title and a location:

```bash
python scrape.py scrape --job "elephant washer" --location "Toowoomba QLD"
```

If the website has not been searched for this term at this location before, the program will request the information
from the server, otherwise it will use the data cached previously in a local file.

To access the server without replacing the local data cache, the option --no-cache can be added to the command:

```bash
python scrape.py scrape --job "elephant washer" --location "Toowoomba QLD" --no-cache
```

The scrape task stores all available information (such as descriptions, age of job ad etc) in a pandas data frame save locally as "temp_scrape_results.pkl".
It can be accessed via e.g. a jupyter notebook and opened with pandas or used by the filter task to produce a screen
output or json file with a selected subset of the results.

#### Filter

The filter task takes the last saved data frame and either displays it on screen or saves it to disk by a given name:

```bash
python scrape.py filter --save "job_results"
```

The scraped results can be further sorted through by filtering 3 aspects:
- job
- rating
- salary

Job refers to a term in the job title given the by company offering the position.
Rating refers to the rating of the prospective employer given by users of indeed.
Salary refers to the minimum of a given range or the value given as the salary for the position.

**NB**: Not all job offers have a rating or a salary proposal. The default value for these cases is 0.

The filter values are passed in as strings in the same way as for the scrape task:

```bash
python scrape.py scrape --job "elephant" --rating "3" --salary "200000"
```

#### Clear-cache

The clear-cache task
```bash
python scrape.py clear-cache
```
removes all data from the local cache.


## Pros, cons and next steps

### Pros

- Local caching is fast for repetitive tasks
- Storing temporary data frame in pickle format makes it compatible with other platforms
- Automatically scrapes all available pages for job offers without clicks

### Cons

- So far only indeed.com
- Filtering is limited, could have more options such as searching within job descriptions
- The program tries to estimate how many jobs it is gathering, but the results seem to vary during the scraping process

### Next steps

- multiple todos across script have suggestions for possible extensions
- add flexibility to search terms in scraping and filtering

## License

This project is licensed under the terms of the MIT license.
