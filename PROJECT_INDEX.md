# UnifiedGigs (JobSpy) - Project Index

## Overview
UnifiedGigs is a comprehensive job scraping library that aggregates job postings from multiple popular job boards into a unified interface. It supports both traditional employment and freelance job categories, with specialized search capabilities for various professional domains.

## Project Structure

### Core Files
- **`__init__.py`** - Main entry point with `scrape_jobs()` function
- **`model.py`** - Data models and enums (JobPost, Location, Country, etc.)
- **`util.py`** - Utility functions for HTTP requests, salary parsing, logging
- **`app.py`** - Streamlit web application for job search interface
- **`example.py`** - Usage examples and demonstrations
- **`freelance_search_example.py`** - Specialized freelance job search examples

### Job Board Modules
Each job board has its own module with consistent structure:

#### LinkedIn (`linkedin/`)
- **`__init__.py`** - LinkedIn scraper implementation
- **`constant.py`** - LinkedIn-specific constants and endpoints
- **`util.py`** - LinkedIn-specific utility functions

#### Indeed (`indeed/`)
- **`__init__.py`** - Indeed scraper implementation
- **`constant.py`** - Indeed-specific constants and endpoints
- **`util.py`** - Indeed-specific utility functions

#### Glassdoor (`glassdoor/`)
- **`__init__.py`** - Glassdoor scraper implementation
- **`constant.py`** - Glassdoor-specific constants
- **`util.py`** - Glassdoor-specific utilities

#### Google (`google/`)
- **`__init__.py`** - Google Jobs scraper implementation
- **`constant.py`** - Google-specific constants
- **`util.py`** - Google-specific utilities

#### ZipRecruiter (`ziprecruiter/`)
- **`__init__.py`** - ZipRecruiter scraper implementation
- **`constant.py`** - ZipRecruiter-specific constants
- **`util.py`** - ZipRecruiter-specific utilities

#### Bayt (`bayt/`)
- **`__init__.py`** - Bayt scraper implementation
- **`constant.py`** - Bayt-specific constants
- **`util.py`** - Bayt-specific utilities

#### Naukri (`naukri/`)
- **`__init__.py`** - Naukri scraper implementation
- **`constant.py`** - Naukri-specific constants
- **`util.py`** - Naukri-specific utilities

### Configuration Files
- **`pyproject.toml`** - Poetry configuration and dependencies
- **`requirements.txt`** - Python package dependencies
- **`README.md`** - Comprehensive documentation
- **`README_APP.md`** - Application-specific documentation

## Key Features

### Supported Job Boards
1. **LinkedIn** - Professional networking platform
2. **Indeed** - Global job search engine
3. **Glassdoor** - Company reviews and job listings
4. **Google Jobs** - Google's job search aggregator
5. **ZipRecruiter** - US/Canada focused job board
6. **Bayt** - Middle East job platform
7. **Naukri** - Indian job portal

### Job Categories
- **Traditional Employment**: Software Development, Data Science, Marketing, etc.
- **Freelance Opportunities**: Virtual Assistance, Social Media Management, Content Creation
- **Specialized Roles**: Cybersecurity, DevOps, Healthcare, Education

### Advanced Features
- **Concurrent Scraping** - Multi-threaded job board scraping
- **Proxy Support** - Rotating proxy support to bypass rate limits
- **Salary Extraction** - Automatic salary parsing from job descriptions
- **Location Filtering** - Country and city-based job filtering
- **Remote Work Support** - Dedicated remote job search capabilities
- **Rate Limiting Protection** - Built-in delays and retry mechanisms

## Data Models

### Core Models (`model.py`)

#### JobPost
```python
class JobPost(BaseModel):
    id: str | None
    title: str
    company_name: str | None
    job_url: str
    location: Optional[Location]
    description: str | None
    job_type: list[JobType] | None
    compensation: Compensation | None
    date_posted: date | None
    is_remote: bool | None
    # ... additional fields
```

#### Location
```python
class Location(BaseModel):
    country: Country | str | None
    city: Optional[str]
    state: Optional[str]
```

#### Compensation
```python
class Compensation(BaseModel):
    interval: Optional[CompensationInterval]
    min_amount: float | None
    max_amount: float | None
    currency: Optional[str] = "USD"
```

### Enums
- **JobType**: FULL_TIME, PART_TIME, CONTRACT, INTERNSHIP, etc.
- **Country**: Support for 50+ countries with proper domain mapping
- **Site**: Job board identifiers
- **CompensationInterval**: YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY

## API Usage

### Basic Usage
```python
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "zip_recruiter"],
    search_term="software engineer",
    location="San Francisco, CA",
    results_wanted=20,
    hours_old=72,
    country_indeed='USA'
)
```

### Freelance Job Search
```python
freelance_jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "zip_recruiter"],
    search_term="virtual assistant OR remote assistant OR VA",
    location="Remote",
    is_remote=True,
    results_wanted=20
)
```

## Web Application

### Streamlit Interface (`app.py`)
- **Interactive Search Interface** - User-friendly job search form
- **Multiple Job Categories** - Pre-defined search terms for different roles
- **Advanced Filtering** - Location, work type, job type, and age filters
- **Results Display** - Formatted job listings with company information
- **Export Capabilities** - CSV export functionality

### Key Features
- **Responsive Design** - Modern UI with custom CSS styling
- **Real-time Search** - Live job search with progress indicators
- **Multi-platform Support** - Search across all supported job boards
- **Freelance Focus** - Specialized search terms for freelance opportunities

## Technical Architecture

### Scraping Strategy
1. **Concurrent Execution** - Uses ThreadPoolExecutor for parallel scraping
2. **Rate Limiting** - Built-in delays and proxy rotation
3. **Error Handling** - Graceful handling of network errors and timeouts
4. **Data Normalization** - Consistent data format across all job boards

### HTTP Management
- **Session Management** - Custom session classes with proxy support
- **TLS Client** - Advanced TLS handling for anti-bot protection
- **Retry Logic** - Automatic retry with exponential backoff
- **Cookie Management** - Session persistence and rotation

### Data Processing
- **Salary Parsing** - Intelligent salary extraction from text
- **Location Normalization** - Standardized location formatting
- **Job Type Classification** - Automatic job type detection
- **Email Extraction** - Contact information parsing

## Dependencies

### Core Dependencies
- **requests** (^2.31.0) - HTTP client library
- **beautifulsoup4** (^4.12.2) - HTML parsing
- **pandas** (^2.1.0) - Data manipulation
- **pydantic** (^2.3.0) - Data validation
- **tls-client** (^1.0.1) - Advanced TLS handling
- **markdownify** (^0.13.1) - HTML to Markdown conversion

### Development Dependencies
- **jupyter** (^1.0.0) - Development environment
- **black** - Code formatting
- **pre-commit** - Git hooks

## Configuration

### Environment Setup
- **Python Version**: >= 3.10 required
- **Package Manager**: Poetry (recommended) or pip
- **Virtual Environment**: Recommended for development

### Proxy Configuration
```python
proxies = [
    "user:pass@host:port",
    "localhost"  # Direct connection
]
```

### Country Support
- **LinkedIn**: Global search with location parameter
- **ZipRecruiter**: US/Canada only
- **Indeed/Glassdoor**: 50+ countries with country-specific domains
- **Bayt**: International search
- **Naukri**: India-focused

## Performance Considerations

### Rate Limiting
- **LinkedIn**: Most restrictive (10 pages per IP)
- **Indeed**: Best performance, no rate limiting
- **Other Platforms**: Variable limits, proxy recommended

### Optimization Tips
- Use proxies for high-volume scraping
- Implement delays between requests
- Filter results early to reduce processing
- Use specific search terms for better relevance

## Error Handling

### Common Issues
- **429 Errors**: Rate limiting - use proxies or wait
- **Blocked IPs**: Rotate proxies or reduce request frequency
- **No Results**: Check search term specificity
- **Network Timeouts**: Implement retry logic

### Debugging
- **Verbose Logging**: Set verbose=2 for detailed logs
- **Error Logs**: Check console output for specific errors
- **Proxy Testing**: Verify proxy connectivity before use

## Future Enhancements

### Planned Features
- Additional job board support
- Enhanced salary parsing
- Job application automation
- Advanced filtering options
- Real-time job alerts

### Scalability Improvements
- Distributed scraping capabilities
- Database integration
- API rate limit optimization
- Enhanced proxy management

## Contributing

### Development Setup
1. Clone the repository
2. Install dependencies with Poetry
3. Set up pre-commit hooks
4. Follow coding standards (Black formatting)

### Testing
- Unit tests for core functionality
- Integration tests for job board scrapers
- Performance testing for rate limits

## License
This project is licensed under the MIT License - see LICENSE file for details.

---

*This index provides a comprehensive overview of the UnifiedGigs job scraping library. For detailed usage examples and API documentation, refer to the README.md file.* 