# 🎓 University Application Scraper (DHET Map Extractor)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)  
![Selenium](https://img.shields.io/badge/Selenium-Automation-brightgreen.svg)  
![Status](https://img.shields.io/badge/Status-Active-success.svg)  
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

> **Automated Web Scraper** that extracts data on South African higher education institutions from the official DHET (Department of Higher Education and Training) interactive map.  
> The scraper outputs structured data for use in research, education portals, data analytics, and more.

---

## 🧭 Table of Contents

- [Overview](#-overview)  
- [Features](#-features)  
- [Project Structure](#-project-structure)  
- [Setup & Installation](#-setup--installation)  
- [Usage](#-usage)  
- [Example Output](#-example-output)  
- [Logging](#-logging)  
- [Auto-Generated README](#-auto-generated-readme)  
- [License](#-license)  

---

## 🧩 Overview

The **University Application Scraper** automates data extraction from the interactive DHET institutional map to collect:

- Institution names  
- Institution types (TVET colleges, Universities, etc.)  
- Source URLs for reference  
- Date and time stamps indicating when the data was scraped  

All collected data is saved in structured **JSON** format located in the `data/` directory for downstream consumption.

---

## ✨ Features

- ✅ Headless browser automation using Selenium for efficient scraping  
- ✅ Dynamic extraction of institution markers directly from the DHET map interface  
- ✅ Robust error handling and retry logic for scraping stability  
- ✅ JSON output format to facilitate easy integration with other systems  
- ✅ Detailed logging system to aid debugging and monitor scraper activity  
- ✅ Auto-generation of README including scraping timestamp and key metrics  
---

## ⚙️ Setup & Installation

1. Clone the repository:

git clone https://github.com/yourusername/uniapplicationscraper.git
cd uniapplicationscraper

text

2. (Optional) Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows

text

3. Install dependencies:

pip install -r requirements.txt

text

4. Ensure a compatible ChromeDriver or GeckoDriver is installed and accessible in your PATH for Selenium.

---

## 🚀 Usage

Run the scraper:

python scrapers/scraper.py

text

Scraped data output will be saved in the `data/` folder.

---

## 🖼️ Example Output

Sample entry in `data/sources.json`:

{
"institution_name": "University of Johannesburg",
"institution_type": "University",
"source_url": "https://www.dhet.gov.za/universities/uj",
"scraped_timestamp": "2025-11-03T08:00:00Z"
}

text

---

## 📜 Logging

Logs are stored inside the `logs/` directory, recording scraping activity, errors, and timestamps. Use tail or similar tools to monitor logs in real-time.

---

## 📄 Auto-Generated README

This repository contains `generate_readme.py` which dynamically updates this README to include the latest scrape timestamps and key metrics.

---

## 📝 License

This project is open source under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 💡 Maintainer

**Author:** Sakhumuzi Khuzwayo  
**Purpose:** Enable accessible extraction of South African higher education institution data for research and integration.

---

