A simple web scraper that collects Python job listings from [PythonJobs](https://pythonjobs.github.io/) and saves them to CSV and JSON files.

This project is meant as a **portfolio / learning project** in Python and web scraping.

## Features

- Fetches job listings from a public job board
- Extracts:
  - job title
  - company
  - location
  - link to the full listing
  - short summary/description
- Saves results to:
  - `data/python_jobs.csv`
  - `data/python_jobs.json`
- Clean, reusable scraping logic (`scraper.py`)
- Ready to extend (pagination, filters, different sources)

## Tech stack

- Python 3.10+  
- [requests](https://pypi.org/project/requests/)  
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)

## Installation

```bash
git clone https://github.com/<your-username>/python-jobs-scraper.git
cd python-jobs-scraper

# (Optional but recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# or
.venv\Scripts\activate      # Windows

pip install -r requirements.txt