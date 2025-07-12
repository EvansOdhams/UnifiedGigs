import sys
from __init__ import scrape_jobs

def main():
    try:
        print("Testing job search without Google...")
        jobs = scrape_jobs(
            site_name=["linkedin", "indeed"],  # Avoid Google for now
            search_term="Software Development",
            location="New York, NY",
            results_wanted=5,  # Limit results to avoid rate limiting
            country_indeed='USA'
        )
        print(f"Found {len(jobs)} jobs")
        
        if len(jobs) > 0:
            print("\nSample job found:")
            # Get the first job in the results and print key details
            job = jobs.iloc[0]
            print(f"Title: {job.get('title')}")
            print(f"Company: {job.get('company')}")
            print(f"Location: {job.get('location')}")
            print(f"URL: {job.get('job_url')}")
    except Exception as e:
        print(f"Error occurred: {e}", file=sys.stderr)
        
if __name__ == "__main__":
    main() 