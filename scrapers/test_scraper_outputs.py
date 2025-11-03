import os
import json
import pandas as pd

# Paths (dynamic)
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "../data")
SOURCES_FILE = os.path.join(DATA_DIR, "sources.json")
TVET_DETAILS_FILE = os.path.join(DATA_DIR, "tvet_details.json")
PROGRAMMES_CLEAN_FILE = os.path.join(DATA_DIR, "programmes_clean.csv")


def test_json_file(file_path, expected_type=list, description="JSON file"):
    """Generic JSON file test with decoding and type checks."""
    if not os.path.exists(file_path):
        print(f"[❌] {file_path} not found. Run the scraper first.")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            print(f"[❌] {file_path} is empty!")
            return False
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"[❌] JSON decode error in {file_path}: {e}")
            return False

    if not isinstance(data, expected_type):
        print(f"[❌] {file_path} should contain a {expected_type.__name__}.")
        return False

    print(f"[✅] {description} loaded successfully, {len(data)} entries found.")
    return True, data


def test_csv_file(file_path, description="CSV file"):
    """Generic CSV file test with emptiness check."""
    if not os.path.exists(file_path):
        print(f"[❌] {file_path} not found. Run the scraper first.")
        return False

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"[❌] Error reading {file_path}: {e}")
        return False

    if df.empty:
        print(f"[❌] {file_path} is empty!")
        return False

    print(f"[✅] {description} loaded successfully, {len(df)} rows found.")
    print(df.head())
    return True


def main():
    print("=== Testing Scraper Outputs ===\n")
    all_ok = True

    # Test sources.json
    ok, sources = test_json_file(SOURCES_FILE, expected_type=list, description="sources.json")
    all_ok &= ok

    # Test tvet_details.json
    ok, tvet_details = test_json_file(TVET_DETAILS_FILE, expected_type=list, description="tvet_details.json")
    all_ok &= ok

    # Test programmes_clean.csv
    ok = test_csv_file(PROGRAMMES_CLEAN_FILE, description="programmes_clean.csv")
    all_ok &= ok

    if all_ok:
        print("\n[🎉] All scraper outputs look good!")
    else:
        print("\n[⚠️] Some outputs are missing or invalid. Check logs and rerun the scrapers.")


if __name__ == "__main__":
    main()

