#!/usr/bin/env python
"""
Freelance Job Search Example with UnifiedGigs
----------------------------------------
This example script demonstrates how to use UnifiedGigs to search for freelance opportunities
across different platforms and categories.
"""

import csv
import pandas as pd
from __init__ import scrape_jobs
import datetime
import os

# Define freelance job categories with their search terms
freelance_categories = {
    "Virtual Assistance": "virtual assistant OR VA OR remote assistant OR personal assistant OR executive VA OR administrative assistant",
    "Social Media Management": "social media manager OR social media strategist OR community manager OR social media specialist OR content scheduler OR social media coordinator",
    "Content Creation": "content creator OR content writer OR blogger OR copywriter OR content strategist OR ghostwriter OR article writer OR creative writer",
    "Freelance Writing": "freelance writer OR freelance content writer OR copywriter OR editor OR proofreader OR technical writer OR SEO writer",
    "Freelance Design": "freelance designer OR graphic design freelancer OR logo designer OR illustrator OR brand identity designer OR web designer"
}

def search_freelance_jobs(category_name, country="USA", days_old=7, results_per_site=20, 
                         remote_only=True, job_boards=None):
    """
    Search for freelance jobs in a specific category
    
    Args:
        category_name (str): Name of the category from freelance_categories
        country (str): Country to search in (for Indeed & Glassdoor)
        days_old (int): How many days old the job posts should be
        results_per_site (int): Number of results to fetch per job board
        remote_only (bool): Whether to only fetch remote jobs
        job_boards (list): List of job boards to search on. Defaults to Indeed, LinkedIn, and ZipRecruiter
        
    Returns:
        pandas.DataFrame: DataFrame containing the scraped job listings
    """
    if job_boards is None:
        job_boards = ["indeed", "linkedin", "zip_recruiter"]
        
    if category_name not in freelance_categories:
        raise ValueError(f"Category {category_name} not found. Available categories: {', '.join(freelance_categories.keys())}")
    
    search_term = freelance_categories[category_name]
    
    print(f"Searching for {category_name} jobs...")
    print(f"Using search terms: {search_term}")
    
    jobs = scrape_jobs(
        site_name=job_boards,
        search_term=search_term,
        location="Remote" if remote_only else None,
        results_wanted=results_per_site,
        is_remote=remote_only,
        hours_old=days_old * 24,  # Convert days to hours
        country_indeed=country
    )
    
    print(f"Found {len(jobs)} jobs for {category_name}")
    return jobs

def save_results_to_csv(jobs_df, category_name):
    """Save the search results to a CSV file"""
    if jobs_df.empty:
        print("No jobs found, skipping CSV creation.")
        return None
        
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{category_name.lower().replace(' ', '_')}_jobs_{timestamp}.csv"
    
    jobs_df.to_csv(filename, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
    print(f"Saved results to {filename}")
    return filename

def main():
    """Run searches for all freelance categories and combine results"""
    all_jobs = []
    
    # Search each category
    for category in freelance_categories:
        jobs_df = search_freelance_jobs(
            category_name=category,
            country="USA",
            days_old=14,  # Look for jobs from the last 14 days
            results_per_site=30,
            remote_only=True
        )
        
        if not jobs_df.empty:
            jobs_df['category'] = category
            all_jobs.append(jobs_df)
            
            # Save individual category results
            save_results_to_csv(jobs_df, category)
    
    # Combine all results
    if all_jobs:
        combined_jobs = pd.concat(all_jobs, ignore_index=True)
        print(f"Total jobs found across all categories: {len(combined_jobs)}")
        
        # Save combined results
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        combined_filename = f"all_freelance_jobs_{timestamp}.csv"
        combined_jobs.to_csv(combined_filename, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        print(f"Saved combined results to {combined_filename}")
    else:
        print("No jobs found across any categories.")

if __name__ == "__main__":
    main() 