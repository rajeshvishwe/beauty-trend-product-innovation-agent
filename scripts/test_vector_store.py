"""
Test script for the Beauty FAISS vector store.

Run from project root:

    python scripts/test_vector_store.py
"""

from __future__ import annotations

import sys
from pathlib import Path


# ---------------------------------------------------------
# Allow imports from project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


from services.vector_store import create_beauty_vector_store


def main() -> None:
    """
    Build the vector store and test semantic retrieval.
    """

    print("=" * 70)
    print("Beauty FAISS RAG Test")
    print("=" * 70)

    store = create_beauty_vector_store()

    query = (
    "What do customers want from daily sunscreen?"
	)

    print("\nQuery:")
    print(query)

    print("\nRetrieved Documents:")
    print("-" * 70)

    results = store.search(
        query=query,
        top_k=5,
    )

    for position, result in enumerate(
        results,
        start=1,
    ):

        print(
            f"\nRESULT {position}"
        )

        print(
            f"Type     : {result['type']}"
        )

        print(
            f"Category : {result['category']}"
        )

        print(
            f"Product  : {result['product_name']}"
        )

        print(
            f"Distance : {result['distance']}"
        )

        print("\nContent:")

        print(
            result["text"]
        )

        print("-" * 70)

    print(
        "\n✅ FAISS retrieval test PASSED"
    )


if __name__ == "__main__":
    main()