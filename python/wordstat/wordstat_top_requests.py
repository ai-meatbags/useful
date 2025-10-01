"""Command-line helper for the Yandex Wordstat Top Requests API."""

import argparse
import json
import os
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

API_URL = "https://api.wordstat.yandex.net/v1/topRequests"


def load_api_token(env_file: Optional[str] = ".env") -> str:
    """Load the Wordstat API token from the given .env file or environment."""
    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv()

    token = os.getenv("WORDSTAT_API_KEY")
    if not token:
        raise RuntimeError(
            "WORDSTAT_API_KEY is not set. Add it to your .env or export it before running the script."
        )
    return token


def fetch_top_requests(phrases: List[str], token: str) -> Dict[str, Dict]:
    """Fetch top requests for each phrase from the Wordstat API."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    results: Dict[str, Dict] = {}
    for phrase in phrases:
        payload = {"phrase": phrase}
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            results[phrase] = response.json()
        except requests.exceptions.RequestException as exc:
            results[phrase] = {"error": str(exc)}
        except json.JSONDecodeError:
            results[phrase] = {"error": "Unable to decode JSON", "response": response.text}

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch top queries from Yandex Wordstat for the supplied phrases.",
    )
    parser.add_argument("phrases", nargs="+", help="One or more phrases to check.")
    parser.add_argument(
        "--env",
        dest="env_file",
        default=".env",
        help="Path to the .env file with WORDSTAT_API_KEY (default: .env). Use '' to skip.",
    )
    args = parser.parse_args()

    try:
        token = load_api_token(args.env_file)
    except RuntimeError as err:
        parser.error(str(err))

    results = fetch_top_requests(args.phrases, token)
    print(json.dumps(results, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
