import csv
import json
from pathlib import Path

from scraper import scrape_many_pages, jobs_to_dicts

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)


def save_to_csv(jobs: list[dict], path: Path) -> None:
    if not jobs:
        print("[WARN] No jobs to save to CSV.")
        return

    fieldnames = list(jobs[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)

    print(f"[OK] Saved CSV to {path}")


def save_to_json(jobs: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

    print(f"[OK] Saved JSON to {path}")


def main(pages: int = 1) -> None:
    print("[INFO] Starting Python jobs scraper...")
    jobs = scrape_many_pages(pages=pages)
    jobs_dicts = jobs_to_dicts(jobs)

    print(f"[INFO] Scraped {len(jobs_dicts)} jobs.\n")

    # Pretty-print first few
    for job in jobs_dicts[:5]:
        print(f"- {job['title']} @ {job['company']} ({job['location']})")
        print(f"  {job['link']}")
        if job["summary"]:
            print(f"  {job['summary'][:120]}...")
        print()

    csv_path = OUTPUT_DIR / "python_jobs.csv"
    json_path = OUTPUT_DIR / "python_jobs.json"

    save_to_csv(jobs_dicts, csv_path)
    save_to_json(jobs_dicts, json_path)


if __name__ == "__main__":
    main(pages=1)