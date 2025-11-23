
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional, List

import requests
from bs4 import BeautifulSoup, Tag


@dataclass
class SiteConfig:
    base_url: str

    list_url: str  # e.g. "https://pythonjobs.github.io/" or ".../page/{page}/"


    job_selector: str
    title_selector: str
    company_selector: str
    location_selector: Optional[str] = None
    summary_selector: Optional[str] = None
    link_selector: str = "a"
    link_attribute: str = "href"

    company_location_splitter: Optional[str] = " - "

PYTHONJOBS_CONFIG = SiteConfig(
    base_url="https://pythonjobs.github.io",
    list_url="https://pythonjobs.github.io/",
    job_selector=".job",
    title_selector="h1, h2",
    company_selector=".info",
    summary_selector="p",
    company_location_splitter=" - ",
)



def _get_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def _abs_url(base_url: str, maybe_relative: str) -> str:
    if maybe_relative.startswith("http://") or maybe_relative.startswith("https://"):
        return maybe_relative
    return base_url.rstrip("/") + "/" + maybe_relative.lstrip("/")


def parse_job(job_tag: Tag, cfg: SiteConfig) -> dict:
    """Turn a single job HTML block into a Python dict, using only cfg."""

    title_el = job_tag.select_one(cfg.title_selector)
    title = title_el.get_text(strip=True) if title_el else ""

    company = ""
    location = ""

    info_el = job_tag.select_one(cfg.company_selector)
    info_text = info_el.get_text(" ", strip=True) if info_el else ""

    if cfg.location_selector:
        company = info_text
        loc_el = job_tag.select_one(cfg.location_selector)
        if loc_el:
            location = loc_el.get_text(strip=True)
    else:
        if cfg.company_location_splitter and cfg.company_location_splitter in info_text:
            company, location = info_text.split(cfg.company_location_splitter, 1)
        else:
            company = info_text

    # link
    link_el = job_tag.select_one(cfg.link_selector)
    link = ""
    if link_el and cfg.link_attribute in link_el.attrs:
        link = _abs_url(cfg.base_url, link_el[cfg.link_attribute])

    # summary
    summary = ""
    if cfg.summary_selector:
        sum_el = job_tag.select_one(cfg.summary_selector)
        if sum_el:
            summary = sum_el.get_text(strip=True)

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": link,
        "summary": summary,
    }


def scrape(config: SiteConfig, pages: int = 1) -> List[dict]:
    all_jobs: List[dict] = []

    for page in range(1, pages + 1):
        if "{page}" in config.list_url:
            url = config.list_url.format(page=page)
        else:
            # no pagination: only scrape once
            if page > 1:
                break
            url = config.list_url

        print(f"[INFO] Scraping {url} ...")
        soup = _get_soup(url)

        blocks = soup.select(config.job_selector)
        if not blocks:
            print("[WARN] No job blocks found with selector:", config.job_selector)
            break

        for b in blocks:
            try:
                all_jobs.append(parse_job(b, config))
            except Exception as e:
                print("[WARN] Failed to parse one job:", e)

    return all_jobs