# 🎓 University Application Scraper (DHET Map Extractor)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Selenium](https://img.shields.io/badge/Selenium-Automation-brightgreen.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

> **Automated Web Scraper** that extracts South African higher education institutions from the official DHET (Department of Higher Education and Training) interactive map.  
> The scraper stores structured data for further use in research, education portals, or analytics pipelines.

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
The **University Application Scraper** automates data collection from DHET’s institutional map and extracts:
- Institution names  
- Institution type (TVET, University, etc.)  
- Source URLs  
- Timestamps of when data was scraped  

All outputs are stored in structured **JSON** format inside the `data/` directory.

---

## ✨ Features
✅ Headless browser automation via Selenium  
✅ Dynamic marker extraction from the DHET map  
✅ Error handling and retry mechanisms  
✅ JSON output for easy integration  
✅ Logger system for debugging and tracking  
✅ Auto-generating dynamic README (with timestamp and scraper metrics)

---

## 🗂️ Project Structure
uniapplicationscraper/
├── scrapers/
│ ├── scraper.py # Main scraper controller
│ ├── dhet_map_scraper.py # Extracts DHET institutions
├── utils/
│ ├── logger.py # Logging setup utility
├── data/
│ └── sources.json # Scraped output (auto-generated)
├── tests/
│ └── test_scraper_output.py # Validates scraper output
├── generate_readme.py # Dynamic README generator
├── README.md # This file (auto-updated)
└── requirements.txt

yaml
Copy code

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/uniapplicationscraper.git
cd uniapplicationscraper
2️⃣ Create & Activate Virtual Environment
bash
Copy code
python -m venv venv
venv\Scripts\activate    # On Windows
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Verify ChromeDriver Path
Ensure you have the correct ChromeDriver path in
scrapers/dhet_map_scraper.py

python
Copy code
CHROMEDRIVER_PATH = "C:/path/to/chromedriver.exe"
🚀 Usage
Run the scraper from the terminal:

bash
Copy code
python scrapers/dhet_map_scraper.py
Once complete, the output will be saved at:

bash
Copy code
data/sources.json
To regenerate your README dynamically:

bash
Copy code
python generate_readme.py
📦 Example Output
json
Copy code
[
  {
    "name": "University of Cape Town",
    "type": "University",
    "url": "https://www.uct.ac.za/",
    "logo": "https://www.uct.ac.za/favicon.ico"
  },
  {
    "name": "Durban University of Technology",
    "type": "University",
    "url": "https://www.dut.ac.za/",
    "logo": "https://www.dut.ac.za/favicon.ico"
  }
]
🧾 Logging
All logs are automatically stored in /logs/:

Success and error tracking

Timestamped scraper sessions

Progress monitoring

🪄 Auto-Generated README
The generate_readme.py script automatically:

Inserts the last run timestamp

Counts the number of institutions scraped

Updates this README.md file dynamically

Run:

bash
Copy code
python generate_readme.py
Example console output:

yaml
Copy code
✅ README updated successfully at 2025-11-03 07:42
📊 Total institutions: 212
🧠 Contributing
Pull requests and issue reports are welcome!
Please make sure your changes pass the tests before submission:

bash
Copy code
pytest tests/
📜 License
Licensed under the MIT License.
You are free to modify, distribute, and use this project for educational or research purposes.

🕓 Last Updated
🗓️ Auto-generated on: {{timestamp}}
🏫 Institutions Scraped: {{scraper_count}}

💡 Maintainer
Author: Sakhumuzi Khuzwayo
Project Purpose: Enable accessible educational data extraction and system interoperability.

yaml
Copy code

