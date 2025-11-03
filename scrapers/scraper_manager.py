# scrapers/scraper_manager.py
import os
import importlib
import logging
import json
import pandas as pd
from utils.logger import setup_logger
from utils.cleaner import clean_programmes
from scrapers.mistral_ai_parser import MistralAIParser
from scrapers.dhet_details_scraper import main as enrich_tvet_details

# Setup logger
logger = setup_logger('scraper_manager')

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SOURCES_FILE = os.path.join(DATA_DIR, 'sources.json')
PROGRAMMES_RAW_FILE = os.path.join(DATA_DIR, 'programmes_raw.csv')
PROGRAMMES_CLEAN_FILE = os.path.join(DATA_DIR, 'programmes_clean.csv')


def run_general_scraper():
    """Run scraper.py to get universities."""
    try:
        scraper_module = importlib.import_module('scrapers.scraper')
        universities = scraper_module.scrape_institutions()  # returns list of dicts
        logger.info(f"Found {len(universities)} universities from general scraper.")
        return universities
    except Exception as e:
        logger.error(f"Error running general scraper: {e}")
        return []


def run_dhet_scraper():
    """Run dhet_scraper.py to get TVET colleges."""
    try:
        dhet_module = importlib.import_module('scrapers.dhet_scraper')
        tvet_colleges = dhet_module.scrape_dhet_colleges()  # returns list of dicts
        logger.info(f"Found {len(tvet_colleges)} TVET colleges from DHET scraper.")
        return tvet_colleges
    except Exception as e:
        logger.error(f"Error running DHET scraper: {e}")
        return []


def merge_and_save_sources(tvets, universities):
    """Merge universities and TVET colleges and save to sources.json."""
    merged = tvets + universities
    seen = set()
    unique_institutions = []

    for inst in merged:
        name_lower = inst['name'].strip().lower()
        if name_lower not in seen:
            seen.add(name_lower)
            unique_institutions.append(inst)

    with open(SOURCES_FILE, 'w', encoding='utf-8') as f:
        json.dump(unique_institutions, f, indent=4, ensure_ascii=False)

    logger.info(f"Saved {len(unique_institutions)} institutions to {SOURCES_FILE}")
    return unique_institutions


def run_institution_scrapers(institutions):
    """Run all institution-specific scrapers dynamically and collect programme data."""
    programme_data = []

    scraper_dir = os.path.dirname(__file__)
    for file in os.listdir(scraper_dir):
        if file.endswith('_scraper.py') and file not in ('scraper.py', 'scraper_manager.py', 'dhet_scraper.py'):
            module_name = f"scrapers.{file[:-3]}"
            try:
                module = importlib.import_module(module_name)
                for inst in institutions:
                    # Match scraper to institution by name
                    scraper_base = module_name.split('.')[-1].replace('_scraper', '')
                    if scraper_base in inst['name'].lower():
                        data = module.scrape_programmes(inst)  # returns list of dicts
                        programme_data.extend(data)
                        logger.info(f"Scraped {len(data)} programmes from {inst['name']}")
            except Exception as e:
                logger.error(f"Error running {module_name}: {e}")

    if programme_data:
        df = pd.DataFrame(programme_data)
        df.to_csv(PROGRAMMES_RAW_FILE, index=False, encoding='utf-8')
        logger.info(f"Saved {len(df)} raw programmes to {PROGRAMMES_RAW_FILE}")

        cleaned_df = clean_programmes(df)
        cleaned_df.to_csv(PROGRAMMES_CLEAN_FILE, index=False, encoding='utf-8')
        logger.info(f"Saved {len(cleaned_df)} cleaned programmes to {PROGRAMMES_CLEAN_FILE}")


def main():
    logger.info("=== Starting scraping sequence ===")

    # 1️⃣ Scrape universities
    universities = run_general_scraper()

    # 2️⃣ Scrape TVET colleges
    tvet_colleges = run_dhet_scraper()

    # 3️⃣ Merge sources
    institutions = merge_and_save_sources(tvet_colleges, universities)

    # 4️⃣ Enrich TVET college details
    from scrapers.dhet_details_scraper import main as enrich_tvet_details
    enrich_tvet_details()

    # 5️⃣ Optionally load enriched TVETs and update institutions
    tvet_details_file = os.path.join(DATA_DIR, 'tvet_details.json')
    if os.path.exists(tvet_details_file):
        with open(tvet_details_file, 'r', encoding='utf-8') as f:
            tvet_details = json.load(f)
        # Replace basic TVET entries with enriched ones
        for i, inst in enumerate(institutions):
            if inst['type'].lower() == 'tvet college':
                for enriched in tvet_details:
                    if inst['name'].lower() == enriched['name'].lower():
                        institutions[i] = enriched
                        break

    # 6️⃣ Run institution-specific programme scrapers
    if institutions:
        run_institution_scrapers(institutions)

    logger.info("=== Scraping sequence completed ===")
    logger.info(f"Programmes saved to {PROGRAMMES_CLEAN_FILE}")


if __name__ == "__main__":
    main()

    