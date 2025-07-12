from __future__ import annotations

import math
import re
import json
import time
import random
from typing import Tuple
from datetime import datetime, timedelta

from google_jobs.constant import headers_jobs, headers_initial, async_param
from model import (
    Scraper,
    ScraperInput,
    Site,
    JobPost,
    JobResponse,
    Location,
    JobType,
)
from util import extract_emails_from_text, extract_job_type, create_session
from google_jobs.util import log, find_job_info_initial_page, find_job_info


class Google(Scraper):
    def __init__(
        self, proxies: list[str] | str | None = None, ca_cert: str | None = None
    ):
        """
        Initializes Google Scraper with the Goodle jobs search url
        """
        site = Site(Site.GOOGLE)
        super().__init__(site, proxies=proxies, ca_cert=ca_cert)

        self.country = None
        self.session = None
        self.scraper_input = None
        self.jobs_per_page = 10
        self.seen_urls = set()
        self.url = "https://www.google.com/search"
        self.jobs_url = "https://www.google.com/async/callback:550"
        # Add a delay attribute to control time between requests
        self.min_delay = 15  # Minimum delay between requests in seconds
        self.max_delay = 30  # Maximum delay
        self.max_retries = 3  # Number of retries for failed requests
        self.retry_delay = 60  # Base delay before retry in seconds
        
        # Additional user agents for rotation
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        ]

    def scrape(self, scraper_input: ScraperInput) -> JobResponse:
        """
        Scrapes Google for jobs with scraper_input criteria.
        :param scraper_input: Information about job search criteria.
        :return: JobResponse containing a list of jobs.
        """
        self.scraper_input = scraper_input
        # Reduce the maximum number of results to avoid rate limiting
        self.scraper_input.results_wanted = min(20, scraper_input.results_wanted)

        self.session = create_session(
            proxies=self.proxies, ca_cert=self.ca_cert, is_tls=False, has_retry=True
        )
        
        # Set a random user agent
        self.session.headers.update({
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        })
        
        forward_cursor, job_list = self._get_initial_cursor_and_jobs()
        if forward_cursor is None:
            log.warning(
                "Initial cursor not found, try changing your query or there was at most 10 results"
            )
            return JobResponse(jobs=job_list)

        page = 1

        while (
            len(self.seen_urls) < scraper_input.results_wanted + scraper_input.offset
            and forward_cursor
            and page < 3  # Limit to 3 pages to reduce likelihood of getting blocked
        ):
            log.info(
                f"search page: {page} / {math.ceil(scraper_input.results_wanted / self.jobs_per_page)}"
            )
            try:
                # Add a substantial delay between requests to avoid being rate-limited
                delay = random.uniform(self.min_delay, self.max_delay)
                log.info(f"Waiting {delay:.2f} seconds before next request")
                time.sleep(delay)
                jobs, forward_cursor = self._get_jobs_next_page(forward_cursor)
            except Exception as e:
                log.error(f"failed to get jobs on page: {page}, {e}")
                break
            if not jobs:
                log.info(f"found no jobs on page: {page}")
                break
            job_list += jobs
            page += 1
        return JobResponse(
            jobs=job_list[
                scraper_input.offset : scraper_input.offset
                + scraper_input.results_wanted
            ]
        )

    def _get_initial_cursor_and_jobs(self) -> Tuple[str, list[JobPost]]:
        """Gets initial cursor and jobs to paginate through job listings"""
        query = f"{self.scraper_input.search_term} jobs"

        def get_time_range(hours_old):
            if hours_old <= 24:
                return "since yesterday"
            elif hours_old <= 72:
                return "in the last 3 days"
            elif hours_old <= 168:
                return "in the last week"
            else:
                return "in the last month"

        job_type_mapping = {
            JobType.FULL_TIME: "Full time",
            JobType.PART_TIME: "Part time",
            JobType.INTERNSHIP: "Internship",
            JobType.CONTRACT: "Contract",
        }

        if self.scraper_input.job_type in job_type_mapping:
            query += f" {job_type_mapping[self.scraper_input.job_type]}"

        if self.scraper_input.location:
            query += f" near {self.scraper_input.location}"

        if self.scraper_input.hours_old:
            time_filter = get_time_range(self.scraper_input.hours_old)
            query += f" {time_filter}"

        if self.scraper_input.is_remote:
            query += " remote"

        if self.scraper_input.google_search_term:
            query = self.scraper_input.google_search_term

        params = {"q": query, "udm": "8"}
        
        for retry in range(self.max_retries):
            try:
                # Update user agent on each retry
                headers = headers_initial.copy()
                headers["User-Agent"] = random.choice(self.user_agents)
                self.session.headers.update(headers)
                
                log.info(f"Making initial Google request (attempt {retry+1}/{self.max_retries})")
                response = self.session.get(self.url, params=params)
                
                if response.status_code == 200:
                    break
                elif response.status_code == 429:
                    log.warning(f"Google rate-limited request (attempt {retry+1}/{self.max_retries})")
                    if retry < self.max_retries - 1:
                        wait_time = self.retry_delay * (retry + 2)  # Increase delay with each retry
                        log.info(f"Waiting {wait_time} seconds before retry")
                        time.sleep(wait_time)
                        
                        # Try to create a new session
                        self.session = create_session(
                            proxies=self.proxies, ca_cert=self.ca_cert, is_tls=False, has_retry=True,
                            clear_cookies=True
                        )
                    else:
                        log.error("Google has rate-limited your request (429 status code). Try again later or use a proxy.")
                        return None, []
                else:
                    log.warning(f"Google returned status code {response.status_code}")
                    if retry < self.max_retries - 1:
                        wait_time = self.retry_delay * (retry + 1)
                        log.info(f"Waiting {wait_time} seconds before retry")
                        time.sleep(wait_time)
                    else:
                        log.error(f"Error making initial request: HTTP status code {response.status_code}")
                        return None, []
            except Exception as e:
                log.error(f"Error making initial request: {e}")
                if retry < self.max_retries - 1:
                    wait_time = self.retry_delay * (retry + 1)
                    log.info(f"Waiting {wait_time} seconds before retry")
                    time.sleep(wait_time)
                else:
                    return None, []
            
        pattern_fc = r'<div jsname="Yust4d"[^>]+data-async-fc="([^"]+)"'
        match_fc = re.search(pattern_fc, response.text)
        data_async_fc = match_fc.group(1) if match_fc else None
        
        # If we couldn't find a cursor and the response contains "sorry"
        if not data_async_fc and "sorry" in response.text.lower():
            log.error("Google detected unusual traffic from your computer network. Try again later or with a different IP.")
            return None, []
        
        jobs_raw = find_job_info_initial_page(response.text)
        jobs = []
        for job_raw in jobs_raw:
            job_post = self._parse_job(job_raw)
            if job_post:
                jobs.append(job_post)
        return data_async_fc, jobs

    def _get_jobs_next_page(self, forward_cursor: str) -> Tuple[list[JobPost], str]:
        params = {"fc": [forward_cursor], "fcv": ["3"], "async": [async_param]}
        
        for retry in range(self.max_retries):
            try:
                # Update user agent on each retry
                headers = headers_jobs.copy()
                headers["User-Agent"] = random.choice(self.user_agents)
                self.session.headers.update(headers)
                
                log.info(f"Making Google pagination request (attempt {retry+1}/{self.max_retries})")
                response = self.session.get(self.jobs_url, headers=headers_jobs, params=params)
                
                if response.status_code == 200:
                    break
                elif response.status_code == 429:
                    log.warning(f"Google rate-limited pagination request (attempt {retry+1}/{self.max_retries})")
                    if retry < self.max_retries - 1:
                        wait_time = self.retry_delay * (retry + 2)  # Increase delay with each retry
                        log.info(f"Waiting {wait_time} seconds before retry")
                        time.sleep(wait_time)
                    else:
                        log.error("Google has rate-limited pagination request. Try again later or use a proxy.")
                        return [], None
                else:
                    log.warning(f"Google pagination returned status code {response.status_code}")
                    if retry < self.max_retries - 1:
                        wait_time = self.retry_delay * (retry + 1)
                        log.info(f"Waiting {wait_time} seconds before retry")
                        time.sleep(wait_time)
                    else:
                        log.error(f"Error making pagination request: HTTP status code {response.status_code}")
                        return [], None
            except Exception as e:
                log.error(f"Error making pagination request: {e}")
                if retry < self.max_retries - 1:
                    wait_time = self.retry_delay * (retry + 1)
                    log.info(f"Waiting {wait_time} seconds before retry")
                    time.sleep(wait_time)
                else:
                    return [], None
        
        return self._parse_jobs(response.text)

    def _parse_jobs(self, job_data: str) -> Tuple[list[JobPost], str]:
        """
        Parses jobs on a page with next page cursor
        """
        try:
            start_idx = job_data.find("[[[")
            end_idx = job_data.rindex("]]]") + 3
            s = job_data[start_idx:end_idx]
            parsed = json.loads(s)[0]

            pattern_fc = r'data-async-fc="([^"]+)"'
            match_fc = re.search(pattern_fc, job_data)
            data_async_fc = match_fc.group(1) if match_fc else None
            jobs_on_page = []
            
            for array in parsed:
                if len(array) < 2:
                    continue
                _, job_data = array
                if not job_data or not isinstance(job_data, str) or not job_data.startswith("[[["):
                    continue
                    
                try:
                    job_d = json.loads(job_data)
                    job_info = find_job_info(job_d)
                    job_post = self._parse_job(job_info)
                    if job_post:
                        jobs_on_page.append(job_post)
                except Exception as e:
                    log.warning(f"Error parsing job data: {e}")
                    continue
                    
            return jobs_on_page, data_async_fc
        except Exception as e:
            log.error(f"Error parsing jobs: {e}")
            return [], None

    def _parse_job(self, job_info: list):
        try:
            if not job_info or len(job_info) < 29:
                return None
                
            job_url = job_info[3][0][0] if job_info[3] and job_info[3][0] else None
            if not job_url or job_url in self.seen_urls:
                return None
            self.seen_urls.add(job_url)

            title = job_info[0]
            company_name = job_info[1]
            location = city = job_info[2]
            state = country = date_posted = None
            if location and "," in location:
                city, state, *country = [*map(lambda x: x.strip(), location.split(","))]

            days_ago_str = job_info[12]
            if type(days_ago_str) == str:
                match = re.search(r"\d+", days_ago_str)
                days_ago = int(match.group()) if match else None
                date_posted = (datetime.now() - timedelta(days=days_ago)).date() if days_ago else None

            description = job_info[19] if len(job_info) > 19 else ""

            job_post = JobPost(
                id=f"go-{job_info[28]}",
                title=title,
                company_name=company_name,
                location=Location(
                    city=city, state=state, country=country[0] if country else None
                ),
                job_url=job_url,
                date_posted=date_posted,
                is_remote="remote" in description.lower() or "wfh" in description.lower(),
                description=description,
                emails=extract_emails_from_text(description),
                job_type=extract_job_type(description),
            )
            return job_post
        except Exception as e:
            log.warning(f"Error parsing individual job: {e}")
            return None
