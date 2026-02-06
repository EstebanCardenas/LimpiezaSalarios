import json
from pathlib import Path

cache: dict[str, float] = {}

def get_cached_rate(base_currency: str) -> float | None:
    return cache.get(base_currency)

def set_cached_rate(base_currency: str, rate: float) -> None:
    cache[base_currency] = rate

def save_cache():
    with open('cache/conversion_cache.json', 'w') as f:
        json.dump(cache, f)

def load_cache():
    global cache
    if Path('cache/conversion_cache.json').exists():
        with open('cache/conversion_cache.json', 'r') as f:
            cache = json.load(f)
