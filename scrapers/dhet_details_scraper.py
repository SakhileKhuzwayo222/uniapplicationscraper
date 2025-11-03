# scrapers/dhet_details_scraper.py
import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import setup_logger

logger = setup_logger("dhet_details_scraper")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
SOURCES_FILE = os.path.join(DATA_DIR, "sources.json")
DETAILS_FILE = os.path.join(DATA_DIR, "tvet_details.json")

CHROMEDRIVER_PATH = "path/to/chromedriver"
MAP_URL = "https://www.dhet.gov.za/SitePages/Map.aspx"


def setup_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    service = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)


def scrape_institution_details(driver: webdriver.Chrome, name: str) -> dict[str, str]:
    """Scrape a single TVET college from DHET map."""
    details: dict[str, str] = {
        "name": name,
        "type": "TVET College",
        "url": None,
        "address": None,
        "phone": None,
        "email": None
    }

    try:
        marker = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//img[contains(@class,'leaflet-marker-icon') and @title='{name}']")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", marker)
        marker.click()

        popup = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ms-rtestate-field"))
        )

        details["address"] = popup.text.strip()
        try:
            link_tag = popup.find_element(By.TAG_NAME, "a")
            details["url"] = link_tag.get_attribute("href")
        except:
            pass
    except Exception as e:
        logger.warning(f"Failed to scrape {name}: {e}")

    return details


def main() -> None:
    driver = setup_driver()
    driver.get(MAP_URL)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "leaflet-marker-icon"))
    )

    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        institutions = json.load(f)

    enriched = []
    for inst in institutions:
        if inst["type"].lower() == "tvet college":
            enriched.append(scrape_institution_details(driver, inst["name"]))

    driver.quit()

    with open(DETAILS_FILE, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=4, ensure_ascii=False)

    logger.info(f"Saved {len(enriched)} TVET entries to {DETAILS_FILE}")


if __name__ == "__main__":
    main()
