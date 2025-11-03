from fastapi import APIRouter, Query
import json
import os

router = APIRouter()

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
SOURCES_FILE = os.path.join(DATA_DIR, "sources.json")

@router.get("/")
def list_institutions(
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Results to skip for pagination"),
    sort: str = Query("name", description="Sort by field: name | province | type"),
    search: str = Query(None, description="Search by institution name"),
    type: str = Query(None, description="Filter by type: University | TVET"),
    province: str = Query(None, description="Filter by province")
):
    """List institutions with pagination, filtering, and sorting."""
    if not os.path.exists(SOURCES_FILE):
        return {"total": 0, "results": []}

    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        institutions = json.load(f)

    # Optional filters
    if search:
        institutions = [i for i in institutions if search.lower() in i["name"].lower()]
    if type:
        institutions = [i for i in institutions if i.get("type", "").lower() == type.lower()]
    if province:
        institutions = [i for i in institutions if i.get("province", "").lower() == province.lower()]

    # Sorting
    try:
        institutions = sorted(institutions, key=lambda x: x.get(sort, "").lower())
    except KeyError:
        pass

    total = len(institutions)
    institutions = institutions[offset: offset + limit]

    return {"total": total, "results": institutions}
