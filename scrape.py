from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time
from openai import clean_events


def scrape_page(url):

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    driver.quit()
    return html

def parse_events(html, source):

    soup = BeautifulSoup(html, "html.parser")

    events = []
    cards = soup.find_all(["article", "div", "a"])

    for card in cards:

        try:
            title = ""
            title_tag = card.find(["h1", "h2", "h3", "h4"])
            if title_tag:
                title = title_tag.get_text(strip=True)

            if not title or len(title) < 5:
                continue
            link = ""

            if card.name == "a":
                link = card.get("href", "")

            else:
                a_tag = card.find("a")

                if a_tag:
                    link = a_tag.get("href", "")

            if link and link.startswith("/"):
                link = f"https://{source.lower()}.com{link}"

            image_url = ""

            img = card.find("img")

            if img:
                image_url = (
                    img.get("src")
                    or img.get("data-src")
                    or ""
                )

            description = ""
            p_tag = card.find("p")
            if p_tag:
                description = p_tag.get_text(strip=True)

            date = ""
            time_tag = card.find("time")

            if time_tag:
                date = time_tag.get_text(strip=True)

            else:
                text = card.get_text(" ", strip=True)

                keywords = [
                    "Jan", "Feb", "Mar", "Apr", "May",
                    "Jun", "Jul", "Aug", "Sep", "Oct",
                    "Nov", "Dec"
                ]

                for k in keywords:
                    if k in text:
                        date = text
                        break

            location = ""

            spans = card.find_all(["span", "div"])

            for s in spans:

                txt = s.get_text(strip=True)

                if any(city in txt for city in [
                    "Bangalore",
                    "Bengaluru"
                ]):
                    location = txt
                    break

            organizer = ""
            possible_org = card.find_all(["span", "div"])
            for o in possible_org:
                txt = o.get_text(strip=True)
                if "by " in txt.lower():
                    organizer = txt
                    break

            fee = ""

            text = card.get_text(" ", strip=True)

            if "free" in text.lower():
                fee = "Free"

            elif "₹" in text:
                fee = text

            event = {
                "title": title,
                "date": date,
                "location": location,
                "organizer": organizer,
                "link": link,
                "image_url": image_url,
                "description": description,
                "fee": fee,
                "source": source
            }
            events.append(event)

        except:
            pass

    return events

sources = {
    "Luma": "https://luma.com/bengaluru",
    "Eventbrite": "https://www.eventbrite.com/d/india--bangalore/events/",
}

all_events = []

for source, url in sources.items():
    print(f"\nScraping {source}...")
    html = scrape_page(url)
    events = parse_events(html, source)
    print(f"Found {len(events)} events")
    all_events.extend(events)

unique_events = []
seen_titles = set()

for e in all_events:
    if e["title"] not in seen_titles:
        unique_events.append(e)
        seen_titles.add(e["title"])

with open("events.json", "w", encoding="utf-8") as f:
    json.dump(unique_events, f, indent=4, ensure_ascii=False)


print("\nSaved all events to events.json")

if unique_events:

    print("\nSample Event:\n")
    print(json.dumps(unique_events[0], indent=4, ensure_ascii=False))
    cleaned_json = clean_events(unique_events)
    with open("cleaned_events.json", "w", encoding="utf-8") as f:
        f.write(cleaned_json)
    print("Cleaned JSON saved!")