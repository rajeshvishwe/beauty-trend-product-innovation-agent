"""
FAISS vector store service for the Beauty Trend & Product Innovation Agent.

This module:
1. Loads consumer reviews and beauty product data.
2. Converts text into embeddings.
3. Creates a FAISS index.
4. Retrieves relevant beauty knowledge for user queries.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict

import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

REVIEWS_FILE = DATA_DIR / "consumer_reviews.csv"
PRODUCTS_FILE = DATA_DIR / "beauty_products.csv"


# ---------------------------------------------------------
# Embedding model
# ---------------------------------------------------------

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


class BeautyVectorStore:
    """
    Small in-memory FAISS vector database for the POC.
    """

    def __init__(self) -> None:
        """
        Initialize the embedding model and empty vector store.
        """

        print("Loading embedding model...")

        self.embedding_model = SentenceTransformer(
            EMBEDDING_MODEL_NAME
        )

        self.documents: List[Dict[str, str]] = []

        self.index: faiss.IndexFlatL2 | None = None

    def load_data(self) -> None:
        """
        Load consumer reviews and product data.
        """

        if not REVIEWS_FILE.exists():
            raise FileNotFoundError(
                f"Reviews file not found: {REVIEWS_FILE}"
            )

        if not PRODUCTS_FILE.exists():
            raise FileNotFoundError(
                f"Products file not found: {PRODUCTS_FILE}"
            )

        reviews_df = pd.read_csv(REVIEWS_FILE)

        products_df = pd.read_csv(PRODUCTS_FILE)

        self.documents = []

        # -------------------------------------------------
        # Consumer reviews
        # -------------------------------------------------

        for _, row in reviews_df.iterrows():

            text = (
                f"Document Type: Consumer Review\n"
                f"Category: {row['category']}\n"
                f"Product: {row['product_name']}\n"
                f"Rating: {row['rating']}\n"
                f"Review: {row['review']}"
            )

            self.documents.append(
                {
                    "type": "consumer_review",
                    "category": str(row["category"]),
                    "product_name": str(row["product_name"]),
                    "text": text,
                }
            )

        # -------------------------------------------------
        # Product information
        # -------------------------------------------------

        for _, row in products_df.iterrows():

            text = (
                f"Document Type: Beauty Product\n"
                f"Category: {row['category']}\n"
                f"Product: {row['product_name']}\n"
                f"Features: {row['features']}\n"
                f"Target Segment: {row['target_segment']}"
            )

            self.documents.append(
                {
                    "type": "product",
                    "category": str(row["category"]),
                    "product_name": str(row["product_name"]),
                    "text": text,
                }
            )

        print(
            f"Loaded {len(self.documents)} beauty documents."
        )

    def build_index(self) -> None:
        """
        Generate embeddings and build FAISS index.
        """

        if not self.documents:
            raise RuntimeError(
                "No documents loaded. Run load_data() first."
            )

        texts = [
            document["text"]
            for document in self.documents
        ]

        print("Generating embeddings...")

        embeddings = self.embedding_model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        embeddings = np.asarray(
            embeddings,
            dtype="float32",
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.index.add(
            embeddings
        )

        print(
            f"FAISS index created with "
            f"{self.index.ntotal} vectors."
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict[str, str]]:
        """
        Search the FAISS vector database.

        Args:
            query:
                Natural-language user query.

            top_k:
                Number of documents to return.

        Returns:
            List of relevant beauty documents.
        """

        if self.index is None:
            raise RuntimeError(
                "FAISS index is not initialized."
            )

        query_embedding = self.embedding_model.encode(
            [query],
            convert_to_numpy=True,
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32",
        )

        distances, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results: List[Dict[str, str]] = []

        for distance, index_position in zip(
            distances[0],
            indices[0],
        ):

            if index_position == -1:
                continue

            document = self.documents[
                index_position
            ].copy()

            document["distance"] = str(
                round(float(distance), 4)
            )

            results.append(
                document
            )

        return results


def create_beauty_vector_store() -> BeautyVectorStore:
    """
    Convenience function for creating a ready-to-use
    BeautyVectorStore.
    """

    store = BeautyVectorStore()

    store.load_data()

    store.build_index()

    return store