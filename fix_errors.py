#!/usr/bin/env python
"""
Fix for UnifiedGigs Rate Limiting and Error Handling

This script helps diagnose and fix common issues with UnifiedGigs scrapers, particularly
rate limiting (429) and access forbidden (403) errors from job sites.

Usage: python fix_errors.py
"""

import argparse
import logging
import sys
import os
import requests
import time
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("UnifiedGigs-Fixer")

def check_ip_address():
    """Check current IP address to see if it might be blocked"""
    logger.info("Checking your current IP address status...")
    
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        if response.status_code == 200:
            ip = response.json().get("ip", "Unknown")
            logger.info(f"Your current public IP address is: {ip}")
            logger.info("If you've been getting rate limited, consider using a different IP address or proxy.")
        else:
            logger.warning("Could not determine your IP address.")
    except Exception as e:
        logger.error(f"Error checking IP address: {e}")

def check_proxies(test_urls):
    """Test if configured proxies are working"""
    logger.info("Looking for configured proxies...")
    
    proxy_env_vars = ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]
    found_proxies = False
    
    for var in proxy_env_vars:
        if var in os.environ:
            found_proxies = True
            proxy_value = os.environ[var]
            logger.info(f"Found proxy in environment: {var}={proxy_value}")
            
            # Test the proxy
            try:
                for url in test_urls:
                    logger.info(f"Testing proxy with {url}...")
                    proxies = {
                        "http": proxy_value,
                        "https": proxy_value
                    }
                    response = requests.get(url, proxies=proxies, timeout=10)
                    if response.status_code == 200:
                        logger.info(f"✅ Proxy works for {url} (Status: {response.status_code})")
                    else:
                        logger.warning(f"⚠️ Proxy may not work for {url} (Status: {response.status_code})")
            except Exception as e:
                logger.error(f"Error testing proxy: {e}")
    
    if not found_proxies:
        logger.info("No proxies found in environment variables.")
        logger.info("Consider setting up proxies to avoid rate limiting. Example:")
        logger.info("    export HTTP_PROXY=http://your-proxy-url:port")
        logger.info("    export HTTPS_PROXY=http://your-proxy-url:port")

def fix_jobspy_settings():
    """Creates or updates a local configuration file to override default settings"""
    logger.info("Creating local configuration to avoid rate limiting...")
    
    config = """# UnifiedGigs rate limiting fix configuration
# This file contains settings to help avoid rate limiting

# ZipRecruiter settings
ZIPRECRUITER_MIN_DELAY = 15
ZIPRECRUITER_MAX_DELAY = 25
ZIPRECRUITER_MAX_RETRIES = 3

# Glassdoor settings
GLASSDOOR_MIN_DELAY = 15
GLASSDOOR_MAX_DELAY = 20
GLASSDOOR_MAX_RETRIES = 3

# Google settings
GOOGLE_MIN_DELAY = 30
GOOGLE_MAX_DELAY = 45
GOOGLE_MAX_RETRIES = 3
GOOGLE_MAX_RESULTS = 20

# Bayt settings
BAYT_MIN_DELAY = 10
BAYT_MAX_DELAY = 15
BAYT_MAX_RETRIES = 3
"""
    
    try:
        with open("jobspy_config.py", "w") as f:
            f.write(config)
        logger.info("Created jobspy_config.py with optimized settings.")
        logger.info("To use this configuration, import it before using UnifiedGigs:")
        logger.info("")
        logger.info("    from jobspy_config import *")
        logger.info("    from __init__ import scrape_jobs")
        logger.info("    # then use scrape_jobs as usual")
    except Exception as e:
        logger.error(f"Error creating configuration file: {e}")

def demonstrate_best_practices():
    """Show example code for avoiding rate limiting"""
    example_code = """
# Example of using UnifiedGigs with best practices to avoid rate limiting

from __init__ import scrape_jobs
import random
import time

# 1. Limit the number of results requested
results_wanted = 20  # Ask for fewer results

# 2. Only use necessary job boards (skip problematic ones)
job_boards = ["linkedin", "indeed"]  # Skip Google, ZipRecruiter, etc. if they're causing issues

# 3. Implement your own delay between searches
try:
    # First search - LinkedIn only
    jobs_linkedin = scrape_jobs(
        site_name=["linkedin"],
        search_term="Software Development",
        location="New York, NY",
        results_wanted=results_wanted
    )
    print(f"Found {len(jobs_linkedin)} jobs from LinkedIn")
    
    # Add a substantial delay between searches
    delay = random.uniform(30, 60)
    print(f"Waiting {delay:.2f} seconds before next search...")
    time.sleep(delay)
    
    # Second search - Indeed only
    jobs_indeed = scrape_jobs(
        site_name=["indeed"],
        search_term="Software Development",
        location="New York, NY",
        results_wanted=results_wanted,
        country_indeed='USA'
    )
    print(f"Found {len(jobs_indeed)} jobs from Indeed")
    
    # Combine results
    all_jobs = jobs_linkedin.append(jobs_indeed)
    print(f"Total jobs found: {len(all_jobs)}")
    
except Exception as e:
    print(f"Error during job search: {e}")
"""
    
    print("\n" + "-" * 80)
    print("EXAMPLE CODE: HOW TO AVOID RATE LIMITING")
    print("-" * 80)
    print(example_code)
    print("-" * 80)

def test_connection_to_sites(sites):
    """Test connection to job sites without scraping"""
    logger.info("Testing connection to job sites...")
    
    for site, url in sites.items():
        try:
            # Use a random user agent
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
            ]
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept-Language": "en-US,en;q=0.9"
            }
            
            logger.info(f"Testing connection to {site}...")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"✅ Connection to {site} successful (Status: {response.status_code})")
            else:
                logger.warning(f"⚠️ Connection to {site} returned status: {response.status_code}")
                if response.status_code == 403:
                    logger.warning(f"Site {site} may be blocking requests from your IP address")
                elif response.status_code == 429:
                    logger.warning(f"Site {site} is rate limiting requests from your IP address")
        except Exception as e:
            logger.error(f"Error connecting to {site}: {e}")
        
        # Add delay between tests
        time.sleep(random.uniform(3, 5))

def provide_recommendations():
    """Provide recommendations for fixing rate limiting issues"""
    recommendations = [
        "1. Wait at least 1-2 hours before trying again with the same IP address",
        "2. Use a VPN or proxy to change your IP address",
        "3. Reduce the number of results you request (try 10-20 at most)",
        "4. Split your searches across different job boards instead of using all at once",
        "5. Add longer delays between your searches (30-60 seconds)",
        "6. Run searches during off-peak hours",
        "7. If you're scraping a lot, consider rotating between multiple IP addresses",
        "8. For Google specifically, try using the 'custom search API' instead of scraping",
        "9. Check if the job board provides an official API you can use instead",
        "10. For ZipRecruiter, try their official jobs API: https://www.ziprecruiter.com/zipsearch"
    ]
    
    print("\n" + "-" * 80)
    print("RECOMMENDATIONS TO AVOID RATE LIMITING")
    print("-" * 80)
    for rec in recommendations:
        print(rec)
    print("-" * 80)

def main():
    parser = argparse.ArgumentParser(description="Fix UnifiedGigs rate limiting issues")
    parser.add_argument("--check-ip", action="store_true", help="Check your current IP address")
    parser.add_argument("--check-proxies", action="store_true", help="Check configured proxies")
    parser.add_argument("--test-connections", action="store_true", help="Test connections to job sites")
    parser.add_argument("--create-config", action="store_true", help="Create optimized configuration file")
    parser.add_argument("--show-example", action="store_true", help="Show example code with best practices")
    parser.add_argument("--all", action="store_true", help="Run all checks and fixes")
    
    args = parser.parse_args()
    
    # If no arguments provided or --all specified, run everything
    run_all = args.all or (not any([args.check_ip, args.check_proxies, 
                                    args.test_connections, args.create_config,
                                    args.show_example]))
    
    print("=" * 80)
    print("UnifiedGigs Rate Limiting and Error Fix Tool")
    print("=" * 80)
    print("This tool helps diagnose and fix common issues with UnifiedGigs scrapers.")
    print("It can help resolve rate limiting (429) and forbidden access (403) errors.\n")
    
    if args.check_ip or run_all:
        check_ip_address()
        print()
    
    if args.check_proxies or run_all:
        check_proxies(["https://www.google.com", "https://www.linkedin.com"])
        print()
    
    if args.test_connections or run_all:
        test_sites = {
            "LinkedIn": "https://www.linkedin.com/jobs/",
            "Indeed": "https://www.indeed.com/",
            "ZipRecruiter": "https://www.ziprecruiter.com/",
            "Glassdoor": "https://www.glassdoor.com/",
            "Google Jobs": "https://www.google.com/search?q=software+developer+jobs",
            "Bayt": "https://www.bayt.com/"
        }
        test_connection_to_sites(test_sites)
        print()
    
    if args.create_config or run_all:
        fix_jobspy_settings()
        print()
    
    if args.show_example or run_all:
        demonstrate_best_practices()
        print()
    
    if run_all:
        provide_recommendations()

if __name__ == "__main__":
    main() 