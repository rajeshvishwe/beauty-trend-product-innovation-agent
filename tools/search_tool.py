"""
Live web search tool using Serper.

This module provides structured Google search results
for beauty trend research.

It can also be used as a Google ADK function tool.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import requests


# ============================================================
# Add Project Root to Python Path
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


# Import after project root is available
from services.config import SERPER_API_KEY


# ============================================================
# Serper Configuration
# ============================================================

SERPER_SEARCH_URL = "https://google.serper.dev/search"


# ============================================================
# Search Tool
# ============================================================

def search_beauty_trends(
    query: str,
    num_results: int = 8,
) -> dict[str, Any]:
    """
    Search the web for current beauty trends.

    Use this tool for current information about:

    - makeup trends
    - skincare trends
    - beauty ingredients
    - Gen Z beauty behavior
    - consumer beauty trends
    - emerging beauty products
    - beauty market developments

    Args:
        query:
            Search query describing the beauty trend
            information required.

        num_results:
            Maximum number of organic search results.

    Returns:
        Structured search results containing titles,
        snippets, URLs and dates when available.
    """

    if not SERPER_API_KEY:
        return {
            "status": "error",
            "message": "SERPER_API_KEY is not configured.",
            "results": [],
        }

    # Keep result count within POC limits
    num_results = max(
        1,
        min(
            int(num_results),
            10,
        ),
    )

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "q": query,
        "gl": "in",
        "hl": "en",
        "num": num_results,
    }

    try:
        response = requests.post(
            SERPER_SEARCH_URL,
            headers=headers,
            json=payload,
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()

        organic_results = data.get(
            "organic",
            [],
        )

        formatted_results = []

        for item in organic_results[:num_results]:
            formatted_results.append(
                {
                    "title": item.get(
                        "title",
                        "",
                    ),
                    "snippet": item.get(
                        "snippet",
                        "",
                    ),
                    "link": item.get(
                        "link",
                        "",
                    ),
                    "date": item.get(
                        "date",
                        "",
                    ),
                }
            )

        return {
            "status": "success",
            "query": query,
            "results_found": len(
                formatted_results
            ),
            "results": formatted_results,
        }

    except requests.RequestException as exc:
        return {
            "status": "error",
            "query": query,
            "message": str(exc),
            "results": [],
        }

    except ValueError as exc:
        return {
            "status": "error",
            "query": query,
            "message": (
                "Unable to parse Serper response: "
                f"{exc}"
            ),
            "results": [],
        }


# ============================================================
# Standalone Test
# ============================================================

def main() -> None:
    """
    Test Serper beauty trend search independently.
    """

    print("=" * 70)
    print("Beauty Trend Web Search Test")
    print("=" * 70)

    test_query = (
        "2026 Gen Z makeup beauty trends India "
        "skin tint SPF lightweight makeup"
    )

    print("\nSearch Query:")
    print(test_query)

    print("\nSearching...\n")

    result = search_beauty_trends(
        query=test_query,
        num_results=5,
    )

    print(
        f"Status        : {result.get('status')}"
    )

    print(
        f"Results Found : {result.get('results_found', 0)}"
    )

    if result.get("status") == "error":
        print(
            f"\n❌ Error: {result.get('message')}"
        )
        return

    print("\nSearch Results:")
    print("-" * 70)

    for position, item in enumerate(
        result.get(
            "results",
            [],
        ),
        start=1,
    ):
        print(
            f"\nRESULT {position}"
        )

        print(
            f"Title   : {item.get('title')}"
        )

        print(
            f"Date    : {item.get('date') or 'N/A'}"
        )

        print(
            f"Link    : {item.get('link')}"
        )

        print(
            f"Snippet : {item.get('snippet')}"
        )

        print("-" * 70)

    print(
        "\n✅ Serper web search test PASSED"
    )


if __name__ == "__main__":
    main()