import pandas as pd
import re
from difflib import SequenceMatcher
from unidecode import unidecode


# -------------------------
# Normalization Helpers
# -------------------------
def normalize_programme_type(value: str) -> str:
    value = value.lower()

    mappings = {
        'national diploma': 'Diploma',
        'diploma': 'Diploma',
        'higher certificate': 'Higher Certificate',
        'certificate': 'Certificate',
        'bachelor': 'Bachelor’s Degree',
        'bsc': 'Bachelor’s Degree',
        'ba': 'Bachelor’s Degree',
        'bcom': 'Bachelor’s Degree',
        'beng': 'Bachelor’s Degree',
        'honours': 'Honours Degree',
        'postgraduate diploma': 'Postgraduate Diploma',
        'masters': 'Master’s Degree',
        'msc': 'Master’s Degree',
        'phd': 'Doctorate',
        'doctorate': 'Doctorate',
    }

    for key, val in mappings.items():
        if key in value:
            return val
    return value.title()


def normalize_duration(value: str) -> str:
    if not value or value.strip().lower() in ["unknown", "n/a"]:
        return "Unknown"

    value = value.lower().strip()
    match = re.search(r'(\d+)\s*(year|month|semester|week|day)s?', value)
    if match:
        num, unit = match.groups()
        return f"{num} {unit}{'s' if int(num) > 1 else ''}"

    if "yr" in value:
        num = re.findall(r'\d+', value)
        if num:
            return f"{num[0]} years"

    if "mon" in value:
        num = re.findall(r'\d+', value)
        if num:
            return f"{num[0]} months"

    return value.title()


def normalize_name(name: str) -> str:
    if not isinstance(name, str):
        return "Unknown"
    name = unidecode(name)
    name = re.sub(r'\s+', ' ', name.strip())
    return name.title()


# -------------------------
# Programme Similarity Logic
# -------------------------
def simplify_text(text: str) -> str:
    """
    Removes noise, abbreviations, and standardizes text for matching.
    """
    text = text.lower()
    text = unidecode(text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\b(bachelor|bsc|ba|bcom|degree|programme|program|course|of|in|national|diploma|certificate)\b', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def generate_programme_key(programme_name: str, programme_type: str = "") -> str:
    """
    Generates a canonical key (used for grouping similar programmes).
    """
    simplified = simplify_text(programme_name)
    programme_type = simplify_text(programme_type)
    combined = f"{simplified}_{programme_type}".strip("_")
    return combined.replace(" ", "_")


def group_similar_programmes(df: pd.DataFrame, threshold: float = 0.85) -> pd.DataFrame:
    """
    Groups similar programmes using fuzzy matching.
    - Adds a new column 'programme_key'
    - Programmes with similarity >= threshold share the same key
    """
    keys = {}
    programme_keys = []

    for _, row in df.iterrows():
        name = row.get("programme", "")
        ptype = row.get("programme_type", "")
        key = generate_programme_key(name, ptype)

        found_key = None
        for existing_key in keys:
            if SequenceMatcher(None, key, existing_key).ratio() >= threshold:
                found_key = keys[existing_key]
                break

        if found_key:
            programme_keys.append(found_key)
        else:
            keys[key] = key
            programme_keys.append(key)

    df["programme_key"] = programme_keys
    return df


# -------------------------
# Main Cleaning Pipeline
# -------------------------
def clean_programmes(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    # Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Clean string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # Normalize core fields
    if "programme" in df.columns:
        df["programme"] = df["programme"].apply(normalize_name)

    if "programme_type" in df.columns:
        df["programme_type"] = df["programme_type"].apply(normalize_programme_type)

    if "duration" in df.columns:
        df["duration"] = df["duration"].apply(normalize_duration)

    if "institution" in df.columns:
        df["institution"] = df["institution"].apply(normalize_name)

    # Drop duplicates & handle missing
    df.drop_duplicates(inplace=True)
    df.replace(["", "nan", "none", "null"], "Unknown", inplace=True)
    df.fillna("Unknown", inplace=True)

    # Generate and group programme keys
    df = group_similar_programmes(df)

    # Sort and reset
    sort_cols = [col for col in ["programme_key", "institution", "programme"] if col in df.columns]
    if sort_cols:
        df.sort_values(by=sort_cols, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


