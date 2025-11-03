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
│   ├── dhet_map_scraper.py       # Extracts DHET institution data from the map
│   ├── scraper.py                # Main orchestrator — combines data sources
│
├── utils/
│   ├── logger.py                 # Handles logging configuration and formatting
│
├── tests/
│   ├── test_scraper_output.py    # Validates scraper outputs and data integrity
│
├── data/
│   └── sources.json              # Auto-generated file containing scraped results
│
├── generate_readme.py            # Dynamically rebuilds README with timestamp + stats
├── requirements.txt              # Python dependencies
├── .gitignore                    # Excludes venv, logs, and temporary files
└── README.md                     # Auto-updating project documentation

---

## ⚙️ Setup & Installation



💡 Maintainer
Author: Sakhumuzi Khuzwayo
Project Purpose: Enable accessible educational data extraction and system interoperability.


