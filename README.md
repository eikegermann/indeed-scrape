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

The scrape task stores all available information in a pandas data frame save locally as "temp_scrape_results.pkl".
It can be accessed via e.g. a jupyter notebook and opened with pandas or used by the filter task to produce a screen
output or json file with a selected subset of the results.

#### Filter

The filter task takes the last saved data frame and either displays it on screen or saves it to disk by a given name:

```bash
python scrape.py filter --save "job_results"
```



The clear-cache task
```bash
python scrape.py clear-cache
```
removes all data from the local cache.


## Pros, cons and next steps

### Pros

- pro 1
- pro 2

### Cons

- con 1
- con 2

### Next steps

- next step 1
- next step 2

## License

This project is licensed under the terms of the MIT license.
