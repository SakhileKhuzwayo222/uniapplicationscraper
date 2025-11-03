from fastapi import APIRouter, Query
import pandas as pd
import os

router = APIRouter()

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
PROGRAMMES_FILE = os.path.join(DATA_DIR, "programmes_clean.csv")

@router.get("/")
def list_programmes(
    keyword: str = Query(None, description="Search by programme name or description"),
    institution: str = Query(None, description="Filter by institution name"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Results to skip for pagination"),
    sort: str = Query("programme_name", description="Sort by field name (e.g. programme_name, level, faculty)")
):
    """List programmes with pagination, filtering, and sorting."""
    if not os.path.exists(PROGRAMMES_FILE):
        return {"total": 0, "results": []}

    df = pd.read_csv(PROGRAMMES_FILE)

    # Filtering
    if keyword:
        df = df[df["programme_name"].str.contains(keyword, case=False, na=False)]
    if institution:
        df = df[df["institution"].str.contains(institution, case=False, na=False)]

    # Sorting
    if sort in df.columns:
        df = df.sort_values(by=sort, ascending=True)

    total = len(df)
    df = df.iloc[offset: offset + limit]

    return {"total": total, "results": df.to_dict(orient="records")}
