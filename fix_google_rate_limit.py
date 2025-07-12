"""
Fix for Google rate limiting issues in UnifiedGigs

This script demonstrates how to avoid Google rate limiting when using UnifiedGigs
by configuring the search properly.
"""

from __init__ import scrape_jobs
import sys
import time

def main():
    """
    Run job searches safely without triggering Google rate limits
    """
    print("UnifiedGigs Google Rate Limit Fix Demonstration")
    print("===========================================\n")
    
    # Option 1: Skip Google entirely and use other job boards
    print("Option 1: Skip Google and use other job boards\n")
    try:
        print("Searching on LinkedIn and Indeed...")
        jobs = scrape_jobs(
            site_name=["linkedin", "indeed"],  # Exclude Google
            search_term="Software Development",
            location="New York, NY",
            results_wanted=5,
            country_indeed='USA'
        )
        print(f"Found {len(jobs)} jobs without using Google\n")
    except Exception as e:
        print(f"Error with option 1: {e}", file=sys.stderr)
    
    # Option 2: Use Google with reduced results and proper delay
    print("\nOption 2: Use Google with reduced settings\n")
    try:
        print("Searching on Google with limited results...")
        jobs = scrape_jobs(
            site_name=["google"],
            search_term="Software Development",
            location="New York, NY",
            results_wanted=5,  # Very small number
        )
        print(f"Found {len(jobs)} jobs using Google with limited results\n")
    except Exception as e:
        print(f"Error with option 2: {e}", file=sys.stderr)
        print("\nIf you received a 429 error, Google is currently rate-limiting your IP address.")
        print("Recommendations:")
        print("1. Wait a few hours before trying Google searches again")
        print("2. Use a proxy or VPN to change your IP address")
        print("3. Use the LinkedIn, Indeed, and other job boards instead")
    
    print("\nTo avoid Google rate limiting in the future:")
    print("1. Limit 'results_wanted' to 10 or less when using Google")
    print("2. Don't make too many searches in a short time period")
    print("3. Consider modifying the Google scraper in the library code to add more delay")
    print("4. Use a proxy rotation service for web scraping\n")

if __name__ == "__main__":
    main() 