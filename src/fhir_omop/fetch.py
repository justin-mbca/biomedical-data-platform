"""
FHIR resource fetcher (from fhir_omop_agent).
Fetches resources from HAPI FHIR or any FHIR R4 endpoint.
"""

import json
from typing import List

# Optional: use requests if available
try:
    import urllib.request
    import urllib.error
except ImportError:
    pass


FHIR_BASE_DEFAULT = "https://hapi.fhir.org/baseR4"
RESOURCE_TYPES_DEFAULT = ["Patient", "Condition", "Encounter", "Observation"]


def fetch_fhir_resources(
    resource_type: str,
    base_url: str = FHIR_BASE_DEFAULT,
    count: int = 10,
) -> List[dict]:
    """Fetch n resources of a given type from a FHIR server."""
    url = f"{base_url.rstrip('/')}/{resource_type}?_count={count}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        bundle = json.loads(resp.read().decode())
    return [e["resource"] for e in bundle.get("entry", []) if "resource" in e]


def fetch_and_save(
    resource_types: List[str] | None = None,
    base_url: str = FHIR_BASE_DEFAULT,
    count: int = 10,
    out_dir: str = "data/fhir_samples",
) -> None:
    """Fetch resources and save to JSON files."""
    import os
    os.makedirs(out_dir, exist_ok=True)
    for rt in resource_types or RESOURCE_TYPES_DEFAULT:
        try:
            resources = fetch_fhir_resources(rt, base_url, count)
            path = os.path.join(out_dir, f"sample_{rt.lower()}.json")
            with open(path, "w") as f:
                json.dump(resources, f, indent=2)
            print(f"Saved {len(resources)} {rt} resources to {path}")
        except Exception as e:
            print(f"Failed to fetch {rt}: {e}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--base", default=FHIR_BASE_DEFAULT)
    p.add_argument("--count", type=int, default=10)
    p.add_argument("--out", default="data/fhir_samples")
    p.add_argument("--types", nargs="+", default=RESOURCE_TYPES_DEFAULT)
    args = p.parse_args()
    fetch_and_save(args.types, args.base, args.count, args.out)
