from __future__ import annotations

import random
import time

from bs4 import BeautifulSoup

from model import (
    Scraper,
    ScraperInput,
    Site,
    JobPost,
    JobResponse,
    Location,
    Country,
)
from util import create_logger, create_session

log = create_logger("Bayt")


class BaytScraper(Scraper):
    base_url = "https://www.bayt.com"
    min_delay = 5  # Minimum delay between requests
    max_delay = 10  # Maximum delay
    max_retries = 3  # Number of retries

    def __init__(
        self, proxies: list[str] | str | None = None, ca_cert: str | None = None
    ):
        super().__init__(Site.BAYT, proxies=proxies, ca_cert=ca_cert)
        self.scraper_input = None
        self.session = None
        self.country = "worldwide"
        
        # Adding user agents to make requests appear more like a browser
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        ]

    def scrape(self, scraper_input: ScraperInput) -> JobResponse:
        self.scraper_input = scraper_input
        self.session = create_session(
            proxies=self.proxies, ca_cert=self.ca_cert, is_tls=False, has_retry=True
        )
        
        # Set a random user agent
        self.session.headers.update({
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.bayt.com/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        })
        
        job_list: list[JobPost] = []
        page = 1
        # Limit the number of results to avoid excessive requests
        results_wanted = min(60, scraper_input.results_wanted if scraper_input.results_wanted else 10)

        while len(job_list) < results_wanted:
            log.info(f"Fetching Bayt jobs page {page}")
            
            # Add delay between requests (first page doesn't need delay)
            if page > 1:
                delay = random.uniform(self.min_delay, self.max_delay)
                log.info(f"Waiting {delay:.2f} seconds before next request")
                time.sleep(delay)
                
            job_elements = self._fetch_jobs(self.scraper_input.search_term, page)
            if not job_elements:
                break

            if job_elements:
                log.debug(
                    "First job element snippet:\n" + job_elements[0].prettify()[:500]
                )

            initial_count = len(job_list)
            for job in job_elements:
                try:
                    job_post = self._extract_job_info(job)
                    if job_post:
                        job_list.append(job_post)
                        if len(job_list) >= results_wanted:
                            break
                    else:
                        log.debug(
                            "Extraction returned None. Job snippet:\n"
                            + job.prettify()[:500]
                        )
                except Exception as e:
                    log.error(f"Bayt: Error extracting job info: {str(e)}")
                    continue

            if len(job_list) == initial_count:
                log.info(f"No new jobs found on page {page}. Ending pagination.")
                break

            page += 1

        job_list = job_list[:results_wanted]
        return JobResponse(jobs=job_list)

    def _fetch_jobs(self, query: str, page: int) -> list | None:
        """
        Grabs the job results for the given query and page number with retry mechanism.
        """
        url = f"{self.base_url}/en/international/jobs/{query}-jobs/?page={page}"
        
        for retry in range(self.max_retries):
            try:
                log.info(f"Making request to Bayt (attempt {retry+1}/{self.max_retries})")
                
                # Rotate user agent on retries
                self.session.headers.update({
                    "User-Agent": random.choice(self.user_agents)
                })
                
                response = self.session.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    job_listings = soup.find_all("li", attrs={"data-js-job": ""})
                    log.debug(f"Found {len(job_listings)} job listing elements")
                    return job_listings
                elif response.status_code == 403:
                    log.warning(f"Bayt returned 403 Forbidden (attempt {retry+1}/{self.max_retries})")
                    if retry < self.max_retries - 1:
                        # Increase backoff time with each retry
                        wait_time = (retry + 1) * 30
                        log.info(f"Waiting {wait_time} seconds before retry")
                        time.sleep(wait_time)
                        
                        # Recreate session on retry to get fresh connection
                        self.session = create_session(
                            proxies=self.proxies, ca_cert=self.ca_cert, is_tls=False, has_retry=True,
                            clear_cookies=True
                        )
                    else:
                        log.error(f"Bayt: Error fetching jobs - 403 Client Error: Forbidden for url: {url}")
                        return None
                else:
                    log.warning(f"Bayt returned status code {response.status_code}")
                    if retry < self.max_retries - 1:
                        wait_time = (retry + 1) * 15
                        log.info(f"Waiting {wait_time} seconds before retry")
                        time.sleep(wait_time)
                    else:
                        log.error(f"Bayt: Error fetching jobs - {response.status_code} response for url: {url}")
                        return None
            except Exception as e:
                log.error(f"Bayt: Error fetching jobs - {str(e)}")
                if retry < self.max_retries - 1:
                    wait_time = (retry + 1) * 15
                    log.info(f"Waiting {wait_time} seconds before retry")
                    time.sleep(wait_time)
                else:
                    return None
        
        return None

    def _extract_job_info(self, job: BeautifulSoup) -> JobPost | None:
        """
        Extracts the job information from a single job listing.
        """
        # Find the h2 element holding the title and link (no class filtering)
        job_general_information = job.find("h2")
        if not job_general_information:
            return None

        job_title = job_general_information.get_text(strip=True)
        job_url = self._extract_job_url(job_general_information)
        if not job_url:
            return None

        # Extract company name using the original approach:
        company_tag = job.find("div", class_="t-nowrap p10l")
        company_name = (
            company_tag.find("span").get_text(strip=True)
            if company_tag and company_tag.find("span")
            else None
        )

        # Extract location using the original approach:
        location_tag = job.find("div", class_="t-mute t-small")
        location = location_tag.get_text(strip=True) if location_tag else None

        job_id = f"bayt-{abs(hash(job_url))}"
        location_obj = Location(
            city=location,
            country=Country.from_string(self.country),
        )
        return JobPost(
            id=job_id,
            title=job_title,
            company_name=company_name,
            location=location_obj,
            job_url=job_url,
        )

    def _extract_job_url(self, job_general_information: BeautifulSoup) -> str | None:
        """
        Pulls the job URL from the 'a' within the h2 element.
        """
        a_tag = job_general_information.find("a")
        if a_tag and a_tag.has_attr("href"):
            return self.base_url + a_tag["href"].strip()
        return None
