import csv
import json
from pathlib import Path

from scraper import scrape, PYTHONJOBS_CONFIG
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


def main() -> None:
    config = PYTHONJOBS_CONFIG

    print("[INFO] Starting scraper...")
    jobs = scrape(config, pages=1)

    print(f"[INFO] Scraped {len(jobs)} jobs.\n")
    for job in jobs[:5]:
        print(f"- {job['title']} @ {job['company']} ({job['location']})")
        print(f"  {job['link']}")
        if job["summary"]:
            print(f"  {job['summary'][:120]}...")
        print()

    save_to_csv(jobs, OUTPUT_DIR / "jobs.csv")
    save_to_json(jobs, OUTPUT_DIR / "jobs.json")


if __name__ == "__main__":
    main()