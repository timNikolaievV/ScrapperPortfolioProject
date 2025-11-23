from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://pythonjobs.github.io"


@dataclass
class Job:
    title: str
    company: str
    location: str
    link: str
    summary: str

    @classmethod
    def from_html(cls, job_tag) -> "Job":
        # Title is usually in <h1> or <h2>
        title_el = job_tag.find(["h1", "h2"])
        title = title_el.get_text(strip=True) if title_el else "N/A"

        # Company + location often live in a small <p> / <span> block
        info_el = job_tag.find(class_="info") or job_tag.find("p")
        info_text = info_el.get_text(" ", strip=True) if info_el else ""

        # Split "Company – Location" if possible
        if " - " in info_text:
            company, location = info_text.split(" - ", maxsplit=1)
        else:
            company, location = info_text, ""

        # First link in the job block
        link_el = job_tag.find("a", href=True)
        link = link_el["href"] if link_el else ""
        if link and not link.startswith("http"):
            link = BASE_URL.rstrip("/") + "/" + link.lstrip("/")

        # Short description / summary
        summary_el = job_tag.find("p")
        summary = summary_el.get_text(strip=True) if summary_el else ""

        return cls(
            title=title,
            company=company,
            location=location,
            link=link,
            summary=summary,
        )


def _get_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def fetch_jobs(page: Optional[int] = None) -> List[Job]:
    if page is None or page == 1:
        url = BASE_URL + "/"
    else:
        # If pagination is different, adjust this pattern.
        url = f"{BASE_URL}/page/{page}/"

    soup = _get_soup(url)

    # Main job containers – class name may need tweaking if site changes.
    job_blocks = soup.select(".job") or soup.select("li.job") or soup.select("div.job")

    jobs: List[Job] = []
    for block in job_blocks:
        try:
            jobs.append(Job.from_html(block))
        except Exception as exc:  # skip malformed entries, but keep scraping
            print(f"[WARN] Failed to parse a job: {exc}")

    return jobs


def scrape_many_pages(pages: int = 1) -> List[Job]:
    all_jobs: List[Job] = []
    for page in range(1, pages + 1):
        print(f"[INFO] Scraping page {page}...")
        page_jobs = fetch_jobs(page=page)
        if not page_jobs:
            print(f"[INFO] No jobs found on page {page}, stopping.")
            break
        all_jobs.extend(page_jobs)
    return all_jobs


def jobs_to_dicts(jobs: List[Job]) -> List[dict]:
    return [asdict(job) for job in jobs]