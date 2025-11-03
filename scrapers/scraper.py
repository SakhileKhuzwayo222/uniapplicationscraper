from dhet_map_scraper import scrape_dhet_institutions
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from typing import Dict


def get_institution_info(url: str) -> Dict[str, str] | None:
    """
    Fetches institution information from a webpage.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the institution's name, type, URL, and logo URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    name_tag = soup.title
    if name_tag is None:
        print(f"Error: Could not find title tag in {url}")
        return None

    name = name_tag.string.strip() if name_tag else "Unknown"

    logo_tag = soup.find("link", rel="icon")
    if logo_tag is None:
        print(f"Error: Could not find logo tag in {url}")
        logo = None
    else:
        logo = logo_tag.get("href")
        if logo and not str(logo).startswith("http"):
            logo = str(logo)  # Convert logo to str
            logo = urljoin(url, logo)

    # For now, mark all as University; can refine later
    institution_type = "University"

    return {
        "name": name,
        "type": institution_type,
        "url": url,
        "logo": logo
    } if logo is not None else {}

def main():
    # Step 1: Get institution names from DHET
    institution_names = scrape_dhet_institutions()  # returns a list of names

    # Step 2: Convert names to URLs (this can be refined with a more advanced function)
    institution_pages = [f"https://www.{name.lower().replace(' ', '')}.ac.za/" for name in institution_names]

    all_institutions = []
    for page in institution_pages:
        info = get_institution_info(page)
        if info:
            all_institutions.append(info)

    # Step 3: Print or save results
    for inst in all_institutions:
        print(inst)

if __name__ == "__main__":
    main()

