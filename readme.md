# Bengaluru Events Discovery 🎉

An AI-powered Bengaluru events discovery platform built using **Anakin AI**, local LLMs, and Streamlit.

This project automatically:

* Scrapes event websites using Anakin AI
* Extracts structured event data
* Cleans messy event information with AI
* Removes duplicates & garbage entries
* Categorizes events intelligently
* Shows personalized event recommendations in a modern UI

---

# ✨ Powered by Anakin AI

This project primarily uses:

## 🚀 Anakin AI URL Scraper API

Using Anakin AI, the system can:

* scrape modern JavaScript-heavy websites
* extract page content reliably
* generate structured JSON
* simplify event data collection

The scraper automatically pulls events from:

* Luma
* Eventbrite

without manually handling browser rendering complexity.

---

# 🔥 Features

* 🤖 AI-powered event scraping
* 🧹 Automatic data cleaning
* 🔍 Duplicate detection
* 🎯 Personalized recommendations
* 👤 Introvert-friendly filtering
* 🤝 Networking-level filtering
* 🆓 Free events filter
* 🌈 Beautiful Streamlit UI
* ⚡ Fast recommendation engine

---

# 📁 Project Structure

```bash id="vhzhh4"
project/
│
├── anakin_scrape.py        # Anakin AI scraper
├── scrape.py               # Event parser & AI cleaning
├── event_app.py            # Streamlit frontend
├── cleaned_events.json     # Final cleaned events
├── events.json             # Parsed events
├── all_events_raw.json     # Raw Anakin responses
├── .env
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash id="t30i5m"
git clone https://github.com/yourusername/bengaluru-events.git

cd bengaluru-events
```

---

## 2. Create Virtual Environment

### Windows

```bash id="e6o08r"
python -m venv venv

venv\Scripts\activate
```

### Mac/Linux

```bash id="m1mbs0"
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash id="vabvw4"
pip install -r requirements.txt
```

---

# 📦 Requirements

Create a `requirements.txt` file:

```txt id="u2ncr9"
streamlit
beautifulsoup4
requests
webdriver-manager
python-dotenv
ollama
openai
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env id="swfml3"
ANAKIN_API_KEY=your_api_key_here
```

---

# 🧠 How Anakin AI Works Here

The project uses the **Anakin AI URL Scraper API**.

Flow:

```text id="85qq0x"
Website URL
     ↓
Anakin AI Scraper
     ↓
Structured Raw JSON
     ↓
AI Cleaning Pipeline
     ↓
cleaned_events.json
     ↓
Streamlit Recommendation UI
```

---

# 🚀 Step 1 — Scrape Events Using Anakin AI

Run:

```bash id="92ylg7"
python anakin_scrape.py
```

This script:

* sends URLs to Anakin AI
* creates scraping jobs
* polls job status
* downloads structured JSON results
* stores raw responses locally

Sources scraped:

* Luma Bengaluru
* Eventbrite Bengaluru

Generated files:

```text id="yjlwmj"
luma_raw.json
eventbrite_raw.json
all_events_raw.json
```

---

# 📄 anakin_scrape.py Overview

Main responsibilities:

* Connect to Anakin AI API
* Submit scrape jobs
* Poll scrape completion
* Save raw JSON data

Example API flow:

```python id="4ehlom"
submitted = request(
    "POST",
    "/url-scraper",
    {
        "url": url,
        "generateJson": True
    }
)
```

---

# 🧹 Step 2 — Parse & Clean Events

Run:

```bash id="efgmz6"
python scrape.py
```

This script:

* extracts event information
* parses titles, dates, locations, fees
* removes duplicate events
* prepares normalized JSON
* runs AI cleaning

Generated files:

```text id="5j6h7n"
events.json
cleaned_events.json
```

---

# 🤖 AI Cleaning Pipeline

The project uses a local LLM through Ollama + Mistral.

The AI automatically:

* removes junk entries
* removes duplicates
* keeps only real events
* fixes formatting
* enriches event metadata

Additional metadata added:

* vibe
* networking level
* introvert friendliness
* best_for tags

---

# 🦙 Setup Ollama

Install Ollama:

[Ollama Official Website](https://ollama.com?utm_source=chatgpt.com)

Pull Mistral:

```bash id="c2x6fc"
ollama pull mistral
```

Start Ollama:

```bash id="yt5m0t"
ollama serve
```

---

# 🎨 Step 3 — Launch Streamlit UI

Run:

```bash id="y7i99n"
streamlit run event_app.py
```

---

# 🖥️ Streamlit Features

The frontend provides:

* 🌟 Personalized recommendations
* 🎯 AI-based event matching
* 📋 Browse all events
* 👤 Introvert/extrovert matching
* 🤝 Networking preference matching
* 🆓 Free event filtering
* ✨ Modern glassmorphism cards
* 😕 Friendly empty states

---

# 🧠 Recommendation Logic

Events are scored using:

* user interests
* networking preference
* social style
* free/paid preference
* vibe matching
* event categories

High-scoring events appear in:

```text id="t1w7jl"
🌟 Recommended For You
```

Other events appear under:

```text id="k3e7mz"
🗓️ Other Events
```

---

# 📊 Final Event Schema

```json id="1md5ca"
[
  {
    "title": "AI Meetup Bengaluru",
    "date": "2026-05-13",
    "location": "Bengaluru",
    "organizer": "AI Community",
    "link": "https://example.com",
    "image_url": "",
    "description": "Networking meetup for AI enthusiasts",
    "fee": "Free",
    "source": "Luma",
    "vibe": "professional",
    "introvert_friendly": true,
    "networking_level": "Medium",
    "best_for": ["AI", "Networking"]
  }
]
```

---

# 🌐 Supported Sources

Currently integrated:

* Luma
* Eventbrite

---

# 🔥 Future Improvements

* Real-time scraping
* Google Calendar integration
* Event bookmarking
* User profiles
* AI event assistant
* WhatsApp/Telegram notifications
* Trending events
* Smart recommendations
* Nearby event suggestions

---

# 🛠️ Tech Stack

* Python
* Anakin AI
* Streamlit
* Requests
* BeautifulSoup
* Ollama
* Mistral AI
* JSON APIs

---

# 🚀 Full Run Pipeline

```bash id="32m0mo"
python anakin_scrape.py

python scrape.py

streamlit run event_app.py
```

---

# ❤️ Built For

People who want to:

* discover meaningful events
* meet like-minded people
* explore Bengaluru communities
* find startup & AI events
* avoid boring networking events
* discover better social experiences
