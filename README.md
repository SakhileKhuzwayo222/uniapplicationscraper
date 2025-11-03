🎓 DHET Institution Scraper & Data Enrichment Pipeline
Overview

The DHET Institution Scraper is a data extraction and enrichment pipeline built to automatically source, clean, and structure data on South African universities and TVET colleges directly from the official Department of Higher Education and Training (DHET) map interface.

The goal of this project is to serve as the data foundation for the MatricLink system — enabling users to access accurate, validated, and enriched institutional data for use in education-related applications.

🧭 Project Purpose

South Africa’s higher education landscape lacks easily accessible structured data for use in modern applications.
This scraper automates that process by:

Extracting all institution names directly from the DHET interactive map.

Cleaning and validating the extracted data.

Optionally enriching institution data with URLs, types, and logos using intelligent inference (Mistral AI integration planned).

Exporting a structured JSON file (sources.json) that can feed into downstream systems or APIs.

🏗️ System Architecture
uniapplicationscraper/
│
├── scrapers/
│   ├── dhet_map_scraper.py        # Extracts institution names from DHET map
│   ├── scraper.py                 # Fetches and enriches data for each institution
│
├── utils/
│   ├── logger.py                  # Provides color-coded console logging
│   ├── cleaner.py                 # (Optional) Cleans and validates data
│
├── data/
│   └── sources.json               # Output JSON file of all scraped institutions
│
├── tests/
│   └── test_scraper_outputs.py    # Validates scraper output and JSON integrity
│
├── venv/                          # Python virtual environment (ignored in git)
│
└── README_WebScraper.md           # This file

⚙️ Key Features
🔹 1. Automated Institution Extraction

The scraper navigates the official DHET map (https://www.dhet.gov.za/SitePages/Map.aspx) using Selenium WebDriver to extract every educational marker (universities and TVET colleges).

🔹 2. Dynamic Content Handling

Handles dynamically loaded content (JavaScript-driven map) using Selenium’s wait conditions and safe interaction with each map marker.

🔹 3. Structured Output

Outputs all results as structured JSON data under data/sources.json, sorted alphabetically and easily parsable by other systems.

🔹 4. Intelligent Data Enrichment (Planned)

Integrates with Mistral AI for automatic enrichment — including identifying missing logos, website URLs, and correct institution categories.

🔹 5. Modular Design

Each part of the pipeline (scraping, cleaning, enrichment, validation) is built as an independent, reusable Python module.

💻 Installation Guide
1️⃣ Clone the Repository
git clone https://github.com/yourusername/uniapplicationscraper.git
cd uniapplicationscraper

2️⃣ Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate     # On Mac/Linux
venv\Scripts\activate        # On Windows

3️⃣ Install Dependencies
pip install -r requirements.txt


Example dependencies include:

selenium
beautifulsoup4
requests
pandas
numpy

4️⃣ Set ChromeDriver Path

In dhet_map_scraper.py, update this line with your local path:

CHROMEDRIVER_PATH = "C:/path/to/chromedriver.exe"

🚀 Usage
🔸 Run the DHET Map Scraper
python scrapers/dhet_map_scraper.py


➡ Extracts all institution names and saves them into data/sources.json.

🔸 Run the Data Enricher / Web Info Scraper
python scrapers/scraper.py


➡ Uses sources.json to fetch more data (logos, types, websites) for each institution.

🔸 Test Data Integrity
python tests/test_scraper_outputs.py


➡ Checks that the JSON file exists, is non-empty, valid, and correctly structured.

🧩 Core Functions
File	Function	Purpose
dhet_map_scraper.py	scrape_dhet_institutions()	Extracts institution names from DHET map markers
	get_marker_name()	Interacts safely with map popups to extract text
	setup_driver()	Configures a headless Selenium ChromeDriver
scraper.py	get_institution_info(url)	Fetches title and logo metadata from institution websites
	main()	Coordinates data scraping and enrichment
logger.py	setup_logger()	Provides color-coded and timestamped log output
test_scraper_outputs.py	test_sources_json()	Validates and verifies sources.json integrity
🧠 Planned AI Integration: Mistral

A future phase introduces Mistral integration for intelligent enrichment and validation:

Automatic Classification (University, TVET, Private)

Domain Guessing (detect correct institution URL using model reasoning)

Metadata Completion (logo, motto, city, province inference)

Example prompt for enrichment:

prompt = f"""
Given this institution name: "{name}", return structured JSON with:
- verified official website
- institution type
- logo URL
- location (city, province)
"""

🧾 Output Format Example
[
  {
    "name": "University of Johannesburg",
    "type": "University",
    "url": "https://www.uj.ac.za/",
    "logo": "https://www.uj.ac.za/favicon.ico"
  },
  {
    "name": "Sedibeng TVET College",
    "type": "TVET College",
    "url": "https://www.sedcol.co.za/",
    "logo": "https://www.sedcol.co.za/favicon.ico"
  }
]

🧪 Testing and Validation

All tests can be run independently using:

pytest tests/


Or manually:

python tests/test_scraper_outputs.py


✅ The test checks:

File existence

Non-empty content

JSON validity

Correct data structure

🧭 Future Enhancements

 AI enrichment using Mistral

 Integration with MatricLink Backend (C#) API

 Parallel scraping using asyncio or concurrent.futures

 Automatic database sync (PostgreSQL or MongoDB)

 Web dashboard for visualizing scrape progress

👨‍💻 Author

Developer: Sakhumuzi Khuzwayo
Project: MatricLink Data Pipeline
Purpose: Provide verified, structured data for educational applications in South Africa.
