# tools/diagnose_project.py
import os
import sys
import compileall
import importlib
import json

ROOT = os.path.dirname(os.path.dirname(__file__)) if os.path.basename(__file__) == 'diagnose_project.py' else os.getcwd()
print("Project root:", ROOT)
os.chdir(ROOT)

# 1) Ensure package markers exist for scrapers and utils
for pkg in ("scrapers", "utils", "api"):
    init = os.path.join(ROOT, pkg, "__init__.py")
    if not os.path.exists(init):
        print(f"[INFO] Creating missing {pkg}/__init__.py")
        open(init, "a").close()

# 2) Check requirements file
req_file = os.path.join(ROOT, "requirements.txt")
if os.path.exists(req_file):
    print(f"[INFO] requirements.txt exists")
else:
    print("[WARN] requirements.txt not found - create one listing pandas, selenium, requests, beautifulsoup4, fastapi, uvicorn, python-dotenv")

# 3) Try to compile all .py files to surface syntax errors
print("\n=== Compiling all Python files to find syntax errors ===")
compile_success = compileall.compile_dir(ROOT, force=True, quiet=1)
print("compile success:", compile_success)

# 4) Try importing core modules (will surface ImportError)
def try_import(module_name: str):
        try:
            importlib.import_module(module_name)
            print(f"[OK] Imported {module_name}")
        except Exception as e:
            print(f"[ERR] Importing {module_name}: {e}")
        else:
             print(f"[ERR] Invalid module name: {module_name}")

to_check = [
    "utils.logger",
    "utils.cleaner",
    "scrapers.scraper",
    "scrapers.scraper_manager",
    "scrapers.dhet_scraper",
    "scrapers.dhet_details_scraper",
    "api.main"
]

print("\n=== Attempting imports (these may print expected runtime errors like chromedriver path) ===")
for m in to_check:
    try_import(m)

# 5) Quick check for common bad strings (hard-coded paths, placeholders)
print("\n=== Quick file checks for obvious placeholders ===")
bad_phrases = ["path/to/chromedriver", "your_mistral_api_key_here", "MISTRAL_API_KEY=your", "TODO"]
for root, _, files in os.walk(ROOT):
    for f in files:
        if not f.endswith(".py"):
            continue
        path = os.path.join(root, f)
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            txt = fh.read()
            for ph in bad_phrases:
                if ph in txt:
                    print(f"[WARN] Found placeholder '{ph}' in {path}")

print("\nDiagnosis complete. Use the messages above to begin fixing issues.")

# Now we are using sys
print(sys.version)