from __init__ import scrape_jobs
import pandas as pd

# Example of using UnifiedGigs to search for software engineer jobs in New York
print("Starting job search...")

# Scrape jobs from different job boards
jobs = scrape_jobs(
    site_name=["indeed", "linkedin"],  # Using only a few sites for demo
    search_term="software engineer",
    location="New York, NY",
    results_wanted=10,  # Limiting results for demo
    country_indeed='USA',
)

# Print results
print(f"Found {len(jobs)} jobs")
if not jobs.empty:
    print("\nSample of jobs found:")
    # Display the most relevant columns
    relevant_columns = ['title', 'company', 'location', 'job_type', 'interval', 'min_amount', 'max_amount', 'job_url']
    print(jobs[relevant_columns].head())
    
    # Save to CSV
    jobs.to_csv("jobs_results.csv", index=False)
    print("\nResults saved to jobs_results.csv")
else:
    print("No jobs found. Check your search criteria or try different job boards.") 