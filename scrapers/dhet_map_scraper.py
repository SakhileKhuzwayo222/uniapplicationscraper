# scrapers/dhet_map_scraper.py

import json
import time
import os
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import setup_logger

logger = setup_logger("dhet_map_scraper")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "sources.json")

MAP_URL = "https://www.dhet.gov.za/SitePages/Map.aspx"
CHROMEDRIVER_PATH = "path/to/chromedriver"


def setup_driver() -> webdriver.Chrome:
    """Initialize and return a headless Chrome WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def get_marker_name(driver: webdriver.Chrome, marker, index: int) -> Optional[str]:
    """Click a map marker and extract the institution name."""
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", marker)
        marker.click()

        popup = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ms-rtestate-field"))
        )

        name = popup.text.strip()
        if name:
            return name

    except Exception as e:
        logger.warning(f"Skipping marker {index}: {e}")

    finally:
        # Click empty space to close popup
        driver.execute_script("document.querySelector('.leaflet-container').click()")
        time.sleep(0.2)

    return None


def scrape_dhet_institutions() -> list[dict[str, str]]:
    """Scrape DHET Map for institution names and return as structured data."""
    logger.info("Starting DHET map scrape...")

    driver = setup_driver()
    driver.get(MAP_URL)

    # Wait for map to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "leaflet-marker-icon"))
    )
    time.sleep(2)

    markers = driver.find_elements(By.CLASS_NAME, "leaflet-marker-icon")
    logger.info(f"Found {len(markers)} markers on map.")

    institutions: list[dict[str, str]] = []
    seen_names = set()

    for i, marker in enumerate(markers):
        name = get_marker_name(driver, marker, i)
        if name and name.lower() not in seen_names:
            seen_names.add(name.lower())
            institutions.append({
                "name": name,
                "type": "TVET College",
                "url": None,
            })

    driver.quit()

    # Sort alphabetically
    institutions.sort(key=lambda x: x["name"])

    # Save results
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(institutions, f, ensure_ascii=False, indent=4)

    logger.info(f"Saved {len(institutions)} DHET institutions to {OUTPUT_FILE}")
    return institutions


if __name__ == "__main__":
    scrape_dhet_institutions()
    logger.info("Scraping completed successfully.")
