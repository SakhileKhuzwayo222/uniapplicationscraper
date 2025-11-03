# scrapers/mistral_assistant.py
import json
from mistral import MistralModel  # offline model

DATA_DIR = "../data"
SOURCES_FILE = f"{DATA_DIR}/sources.json"
UPDATED_SOURCES_FILE = f"{DATA_DIR}/sources_updated.json"

class MistralAssistant:
    def __init__(self, model_path):
        self.model = MistralModel(model_path=model_path)

    def load_sources(self):
        with open(SOURCES_FILE, "r", encoding="utf-8") as f:
            self.sources = json.load(f)

    def analyze_sources(self):
        # Generate prompt for Mistral
        prompt = f"""
        You are a data assistant for scraping South African institutions.
        Here is the scraped data so far: {json.dumps(self.sources[:50])}

        1. Identify missing universities or TVET colleges based on patterns in names.
        2. Suggest URLs or pages that likely contain programme listings.
        3. Flag entries with missing or inconsistent names/URLs.
        Output in JSON format with keys: 'missing', 'suggested_urls', 'flagged'.
        """
        response = self.model.generate(prompt)
        try:
            suggestions = json.loads(response)
        except Exception:
            # fallback if model returns non-JSON text
            suggestions = {"missing": [], "suggested_urls": [], "flagged": []}
        return suggestions

    def apply_suggestions(self, suggestions):
        # Merge suggested URLs and flag issues
        for url in suggestions.get("suggested_urls", []):
            if not any(s["url"] == url for s in self.sources):
                self.sources.append({"name": "TBD", "url": url, "type": "Unknown", "logo": None})

        # Optionally mark flagged entries
        for flagged in suggestions.get("flagged", []):
            for s in self.sources:
                if s.get("url") == flagged.get("url"):
                    s["flagged"] = True

    def save_sources(self):
        with open(UPDATED_SOURCES_FILE, "w", encoding="utf-8") as f:
            json.dump(self.sources, f, ensure_ascii=False, indent=4)
        print(f"Updated sources saved to {UPDATED_SOURCES_FILE}")


if __name__ == "__main__":
    assistant = MistralAssistant(model_path="../models/mistral_offline")
    assistant.load_sources()
    suggestions = assistant.analyze_sources()
    assistant.apply_suggestions(suggestions)
    assistant.save_sources()
