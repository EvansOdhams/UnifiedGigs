# UnifiedGigs User Interface

A modern, user-friendly interface for searching and filtering jobs across multiple job boards including LinkedIn, Indeed, Glassdoor, and more.

## Features

- **Multi-platform search**: Search jobs across LinkedIn, Indeed, Glassdoor, Google, ZipRecruiter, Bayt, and Naukri
- **Category filters**: Filter jobs by various categories like Software Development, Data Science, Graphic Design, etc.
- **Work type filters**: Find remote, on-site, or hybrid positions
- **Job freshness**: Show only recent jobs (within the last 24 hours by default)
- **Location filtering**: Search jobs in specific locations
- **User-friendly interface**: Presents jobs in both card and table views
- **Export capability**: Download search results as CSV files

## Installation

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:

```bash
streamlit run app.py
```

## Usage

1. Select your desired job boards from the sidebar
2. Choose a job category
3. Enter your preferred location
4. Select the work type (Remote, On-site, Hybrid, or All)
5. Adjust any additional filters as needed
6. Click the "Search Jobs" button
7. View and interact with the search results
8. Download results as CSV if desired

## Notes

- Each job board has its own limitations and search capabilities
- For best results, try different combinations of filters
- If you encounter 404 errors or other issues, try different job boards or modify your search criteria
- The app enforces a 24-hour freshness filter by default to avoid stale job listings

## Requirements

- Python 3.10 or higher
- Streamlit 1.30.0 or higher
- UnifiedGigs 1.1.80 or higher
- Pandas 2.1.0 or higher 