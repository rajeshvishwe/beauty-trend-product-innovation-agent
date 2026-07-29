"""
End-to-end test for the Beauty Trend &
Product Innovation Agent workflow.

Runs:

1. Trend Research Agent
2. Consumer Insight Agent
3. Competitor Intelligence Agent
4. Product Innovation Agent
5. Marketing Campaign Agent

Run from project root:

    python scripts/test_orchestration.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path


# ============================================================
# Project Root
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


from services.orchestration import (
    run_beauty_innovation_workflow,
)


# ============================================================
# Test
# ============================================================

async def test_workflow() -> None:
    """
    Run complete beauty innovation workflow.
    """

    category = "Makeup"

    target_audience = "Gen Z"

    market = "India"

    business_question = (
        "Identify emerging everyday makeup opportunities "
        "and suggest a differentiated product concept "
        "for consumers who prefer lightweight, natural "
        "and multi-benefit beauty products."
    )

    result = await run_beauty_innovation_workflow(
        category=category,
        target_audience=target_audience,
        market=market,
        business_question=business_question,
    )

    # ========================================================
    # Print Results
    # ========================================================

    print("\n")
    print("=" * 70)
    print("1. TREND INTELLIGENCE")
    print("=" * 70)
    print(
        result.trend_insights
    )

    print("\n")
    print("=" * 70)
    print("2. CONSUMER INSIGHTS")
    print("=" * 70)
    print(
        result.consumer_insights
    )

    print("\n")
    print("=" * 70)
    print("3. COMPETITOR INTELLIGENCE")
    print("=" * 70)
    print(
        result.competitor_insights
    )

    print("\n")
    print("=" * 70)
    print("4. PRODUCT INNOVATION CONCEPT")
    print("=" * 70)
    print(
        result.product_concept
    )

    print("\n")
    print("=" * 70)
    print("5. MARKETING CAMPAIGN")
    print("=" * 70)
    print(
        result.campaign_concept
    )

    print("\n")
    print("=" * 70)
    print(
        "✅ END-TO-END ORCHESTRATION TEST PASSED"
    )
    print("=" * 70)


# ============================================================
# Main
# ============================================================

def main() -> None:
    """
    Script entry point.
    """

    asyncio.run(
        test_workflow()
    )


if __name__ == "__main__":
    main()