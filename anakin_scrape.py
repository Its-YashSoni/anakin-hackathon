import os
import time
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE = "https://api.anakin.io/v1"
API_KEY = os.getenv("ANAKIN_API_KEY")

if not API_KEY:
    raise SystemExit("ANAKIN_API_KEY is not set")

sources = {
    "Luma": "https://luma.com/bengaluru",
    "Eventbrite": "https://www.eventbrite.com/d/india--bangalore/events/",
}

session = requests.Session()

session.headers.update({
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
})

def request(method: str, path: str, json_data=None):

    try:

        response = session.request(
            method,
            BASE + path,
            json=json_data,
            timeout=60
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:

        print(f"Request Error: {e}")

        return None


def scrape(url: str):

    print(f"\nSubmitting scrape job for: {url}")

    submitted = request(
        "POST",
        "/url-scraper",
        {
            "url": url,
            "generateJson": True
        }
    )

    if not submitted:
        print("Failed to submit job")
        return None

    job_id = submitted.get("jobId")

    if not job_id:
        print("No jobId returned")
        return None

    print(f"Job ID: {job_id}")

    # Polling
    for _ in range(60):

        job = request("GET", f"/url-scraper/{job_id}")

        if job is None:

            time.sleep(3)
            continue

        status = job.get("status")

        print(f"Status: {status}")

        if status == "completed":
            return job

        if status == "failed":
            print(f"Scrape failed: {job.get('error')}")
            return None

        time.sleep(3)

    print("Timed out")
    return None


if __name__ == "__main__":

    all_results = []

    for source_name, url in sources.items():

        print(f"\n==============================")
        print(f"Scraping {source_name}")
        print(f"==============================")

        result = scrape(url)

        if result:

            structured = {
                "source": source_name,
                "url": url,
                "data": result
            }

            all_results.append(structured)

            # Save individual file
            filename = f"{source_name.lower()}_raw.json"

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(structured, f, indent=4, ensure_ascii=False)

            print(f"Saved: {filename}")

        else:
            print(f"Failed scraping {source_name}")

    with open("all_events_raw.json", "w", encoding="utf-8") as f:

        json.dump(all_results, f, indent=4, ensure_ascii=False)

    print("\nSaved all results to all_events_raw.json")