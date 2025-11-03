🎓 University Application Scraper (DHET Map Extractor)
![Python](https://img.shields.io/badge

![Selenium](https://img.shields.io/badge/Selenium-Automation-bright

![Status](https://img.shields.io/badge/Status-Active-success.svghttps://img.shields.io/badge/License-MIT-lightgrey.svg Web Scraper** that extracts data on South African higher education institutions from the official DHET (Department of Higher Education and Training) interactive map.

The scraper outputs structured data for use in research, education portals, data analytics, and more.

🧭 Table of Contents
Overview

Features

Project Structure

Setup & Installation

Usage

Example Output

Logging

Auto-Generated README

License

🧩 Overview
The University Application Scraper automates data extraction from the interactive DHET institutional map to collect:

Institution names

Institution types (TVET colleges, Universities, etc.)

Source URLs for reference

Date and time stamps indicating when the data was scraped

All collected data is saved in a structured JSON format located in the data/ directory for downstream consumption.

✨ Features
✅ Headless browser automation using Selenium for efficient scraping

✅ Dynamic extraction of institution markers directly from the DHET map interface

✅ Robust error handling and retry logic for scraping stability

✅ JSON output format to facilitate easy integration with other systems

✅ Detailed logging system to aid debugging and monitor scraping activity

✅ Auto-generation of README including scraping timestamp and key metrics

🗂️ Project Structure
text
uniapplicationscraper/
├── scrapers/
│   ├── dhet_map_scraper.py       # Extracts institution data from DHET map
│   ├── scraper.py                # Main orchestrator combining all scrapers
│
├── utils/
│   ├── logger.py                 # Logging setup and configuration
│
├── tests/
│   ├── test_scraper_output.py   # Unit tests for validating scraper output
│
├── data/
│   └── sources.json              # Auto-generated JSON containing scraped data
│
├── generate_readme.py            # Automatically rebuilds README with current stats and timestamp
├── requirements.txt              # Python dependencies and versions
├── .gitignore                    # Files and folders excluded from git (venv, logs, etc.)
└── README.md                     # Project documentation (this file)
⚙️ Setup & Installation
Clone the repository:

bash
git clone https://github.com/yourusername/uniapplicationscraper.git
cd uniapplicationscraper
Create a Python virtual environment and activate it (optional but recommended):

bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
Install the required Python packages:

bash
pip install -r requirements.txt
Ensure you have a compatible version of ChromeDriver or GeckoDriver installed and accessible in your system PATH for Selenium to operate.

🚀 Usage
Run the main scraper:

bash
python scrapers/scraper.py
The output JSON file will be updated in the data/ directory.

🖼️ Example Output
A sample entry in data/sources.json looks like:

json
{
  "institution_name": "University of Johannesburg",
  "institution_type": "University",
  "source_url": "https://www.dhet.gov.za/universities/uj",
  "scraped_timestamp": "2025-11-03T08:00:00Z"
}
📜 Logging
Logs are saved to logs/ directory with detailed scraper activity, errors, and timestamps. Tail the log file for real-time monitoring.

📄 Auto-Generated README
The project includes a script, generate_readme.py, that dynamically updates this README with the latest scrape timestamp and scraper metrics.

📝 License
This project is licensed under the MIT License. See the LICENSE file for details.

💡 Maintainer
Author: Sakhumuzi Khuzwayo

Purpose: To enable accessible extraction of higher education data in South Africa for research and system interoperability.

