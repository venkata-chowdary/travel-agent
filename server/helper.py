import hashlib
import json

def generate_itinerary_hash(itinerary: dict) -> str:
    normalized = json.dumps(itinerary, sort_keys=True)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()