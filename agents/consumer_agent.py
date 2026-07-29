"""
Consumer Insight Agent.

Responsibilities:
1. Retrieve relevant consumer reviews using FAISS.
2. Identify consumer pain points.
3. Identify desired features.
4. Summarize product opportunity signals.

The retrieval function is exposed to Google ADK as a native Python tool.
"""

from __future__ import annotations

from google.adk.agents import LlmAgent

from services.config import GEMINI_MODEL
from services.vector_store import create_beauty_vector_store


# ============================================================
# Initialize FAISS knowledge base
# ============================================================

print("Initializing Consumer Insight knowledge base...")

vector_store = create_beauty_vector_store()


# ============================================================
# ADK Tool
# ============================================================

def search_consumer_reviews(
    query: str,
    top_k: int = 6,
) -> dict:
    """
    Search beauty consumer reviews and product information.

    Use this tool whenever consumer feedback, pain points,
    preferences, desired features, complaints, or unmet needs
    must be analyzed.

    Args:
        query:
            Natural-language description of the consumer
            insight to retrieve.

        top_k:
            Number of relevant documents to retrieve.

    Returns:
        Dictionary containing retrieved review/product data.
    """

    try:
        results = vector_store.search(
            query=query,
            top_k=top_k,
        )

        documents = []

        for result in results:
            documents.append(
                {
                    "type": result["type"],
                    "category": result["category"],
                    "product_name": result["product_name"],
                    "content": result["text"],
                    "distance": result["distance"],
                }
            )

        return {
            "status": "success",
            "query": query,
            "documents_found": len(documents),
            "documents": documents,
        }

    except Exception as exc:
        return {
            "status": "error",
            "query": query,
            "message": str(exc),
        }


# ============================================================
# Agent Instruction
# ============================================================

CONSUMER_AGENT_INSTRUCTION = """
You are the Consumer Insight Agent for a beauty product
innovation team.

Your responsibility is to identify meaningful consumer
insights from beauty reviews and product information.

IMPORTANT:

You MUST use the search_consumer_reviews tool before
providing consumer insight.

Never invent consumer feedback that is not supported by
the retrieved information.

Analyze the retrieved evidence and identify:

1. Top Consumer Needs
2. Top Pain Points
3. Desired Product Features
4. Positive Consumer Signals
5. Product Opportunity Signals

Keep the analysis concise and business-oriented.

Use the following response format:

## Consumer Insight Summary

### Top Consumer Needs
- ...
- ...
- ...

### Pain Points
- ...
- ...
- ...

### Desired Features
- ...
- ...
- ...

### Positive Signals
- ...
- ...

### Product Opportunity
Provide 2-3 concise sentences describing the strongest
product innovation opportunity based on the retrieved
consumer evidence.

Do not produce a full product concept yet.

The Product Innovation Agent will handle that later.
"""


# ============================================================
# Google ADK Agent
# ============================================================

consumer_agent = LlmAgent(
    name="consumer_insight_agent",
    model=GEMINI_MODEL,
    description=(
        "Analyzes beauty consumer reviews to identify "
        "needs, pain points, preferences, and product "
        "innovation opportunities."
    ),
    instruction=CONSUMER_AGENT_INSTRUCTION,
    tools=[
        search_consumer_reviews,
    ],
)


# ADK convention.
# This also makes the agent easy to expose later through
# ADK CLI/Web if required.

root_agent = consumer_agent