# UnifiedGigs Rate Limiting & Error Fixes

This document explains how to address common rate limiting and error issues when using UnifiedGigs for job scraping.

## Common Errors

UnifiedGigs might encounter these common errors when scraping job sites:

1. **429 Too Many Requests** - The job site is rate limiting your requests
2. **403 Forbidden** - The job site is blocking your requests
3. **Location parsing errors** - Issues with parsing location data
4. **HTTP connection errors** - Network or connection issues

## Quick Fix Instructions

### 1. Install Required Dependencies

Make sure all required packages are installed:

```bash
pip install -r requirements.txt
```

### 2. Run the Fix Errors Tool

We've created a helpful tool to diagnose and fix common issues:

```bash
python fix_errors.py
```

This will:
- Check your IP address
- Test connections to job sites
- Create an optimized configuration
- Show best practices code example
- Provide recommendations

### 3. Use the Tool with Specific Flags

Run specific checks:

```bash
# Check your current IP address
python fix_errors.py --check-ip

# Test if your proxies are working 
python fix_errors.py --check-proxies

# Test connections to job sites
python fix_errors.py --test-connections

# Create optimized configuration
python fix_errors.py --create-config

# Show example code for best practices
python fix_errors.py --show-example
```

## Key Changes Made to UnifiedGigs Scrapers

We've improved the following scrapers to reduce rate limiting issues:

### ZipRecruiter Scraper
- Increased delay between requests (10-15 seconds)
- Added retry mechanism with exponential backoff
- Limited concurrent requests and maximum results

### Glassdoor Scraper
- Fixed location parsing issues
- Added better error handling for 403 errors
- Implemented retry mechanism with session refresh
- Added random user agent rotation

### Bayt Scraper
- Added comprehensive HTTP headers
- Implemented retry mechanism for 403 errors
- Added session refresh between retries
- Randomized delays between requests

### Google Scraper
- Significantly increased delays between requests
- Reduced maximum number of results
- Implemented retry mechanism
- Added user agent rotation
- Improved error handling

## Best Practices to Avoid Rate Limiting

1. **Use fewer job boards at once** - Split your searches to one job board at a time
2. **Reduce results requested** - Ask for 10-20 results instead of hundreds
3. **Add delays between searches** - Wait 30-60 seconds between searches
4. **Use proxies** - Rotate between different IP addresses
5. **Set appropriate timeouts** - Use longer timeouts for requests
6. **Handle errors gracefully** - Implement proper error handling
7. **Use official APIs when available** - Some job boards offer official APIs

## Using a Configuration File

The `fix_errors.py` tool can create a configuration file (`jobspy_config.py`) with optimized settings. To use it:

```python
# Import the config before using UnifiedGigs
from jobspy_config import *
from jobspy import scrape_jobs

# Use UnifiedGigs as usual
jobs = scrape_jobs(
    site_name=["linkedin", "indeed"],
    search_term="Software Development",
    location="New York, NY",
    results_wanted=20
)
```

## Additional Resources

- [UnifiedGigs Documentation](https://github.com/yourusername/jobspy)
- [Using Proxies with UnifiedGigs](https://www.example.com)
- [Rate Limiting Best Practices](https://www.example.com) 