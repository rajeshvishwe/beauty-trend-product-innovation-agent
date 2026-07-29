"""
Standalone test for the Product Innovation Agent.

This test supplies representative outputs from:

1. Trend Research Agent
2. Consumer Insight Agent
3. Competitor Intelligence Agent

Later, the orchestrator will generate these inputs
automatically.

Run from project root:

    python scripts/test_innovation_agent.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from google.adk.runners import InMemoryRunner
from google.genai import types


# ============================================================
# Project Root
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


from agents.innovation_agent import innovation_agent


# ============================================================
# Test Configuration
# ============================================================

APP_NAME = "beauty_trend_innovation_agent"

USER_ID = "demo_user"

SESSION_ID = "innovation_agent_test"


# ============================================================
# Sample Research Inputs
# ============================================================

TREND_RESEARCH = """
Beauty Trend Intelligence

Top Emerging Trends:

1. Lightweight complexion products
   Consumers are showing interest in skin-like,
   lightweight everyday makeup.

2. Skinification of makeup
   Makeup products increasingly include skincare-style
   ingredients and benefits.

3. Multi-benefit beauty
   Consumers increasingly prefer simplified routines
   where one product provides multiple benefits.

Consumer Behavior Signals:

- Natural-looking makeup
- Lightweight textures
- Simplified beauty routines
- Skincare + makeup hybrids
- Everyday sun protection

Emerging Product Features:

- Lightweight coverage
- Hydration
- Natural glow
- SPF
- Skincare-inspired ingredients
"""


CONSUMER_RESEARCH = """
Consumer Insight Summary

Top Consumer Needs:

- Lightweight everyday coverage
- Natural skin-like finish
- Hydration
- Comfortable wear
- Sun protection

Pain Points:

- Traditional foundation can feel heavy
- Some foundations become cakey
- Some products become oily after several hours
- Shade matching can be difficult
- Lightweight products may offer limited SPF

Desired Features:

- Lightweight skin tint
- Hydrating texture
- Natural glow
- Higher SPF
- Comfortable everyday wear

Positive Signals:

- Consumers respond positively to skin tints
- Natural-looking products receive positive feedback
- Lightweight products are preferred for everyday use

Product Opportunity:

A hybrid complexion product combining lightweight
coverage, hydration and sun protection could address
several repeated consumer needs.
"""


COMPETITOR_RESEARCH = """
Competitor Intelligence

Common Market Features:

- Lightweight coverage
- Natural finish
- Hydration
- Some skincare positioning
- SPF in selected products

Less Common / Differentiating Features:

- Stronger combination of skincare + makeup + SPF
- Long-lasting hydration with lightweight texture
- Simplified multi-benefit positioning
- Natural coverage with higher everyday SPF

Potential Market Gaps:

- Multi-benefit everyday complexion product
- Lightweight tint with stronger SPF positioning
- Hydration + coverage + sun protection
- Product specifically positioned for Gen Z
  simplified beauty routines

Whitespace Summary:

There may be an opportunity to combine lightweight
coverage, skincare-inspired hydration and everyday
sun protection in one simple complexion product.
"""


# ============================================================
# Run Innovation Agent
# ============================================================

async def run_innovation_agent() -> None:
    """
    Execute Product Innovation Agent test.
    """

    print("=" * 70)
    print("Product Innovation Agent Test")
    print("=" * 70)

    runner = InMemoryRunner(
        agent=innovation_agent,
        app_name=APP_NAME,
    )

    session_service = runner.session_service

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    # --------------------------------------------------------
    # Build Agent Input
    # --------------------------------------------------------

    question = f"""
Create the strongest beauty product innovation concept
for the following business context.

BUSINESS CONTEXT

Category:
Makeup

Target Audience:
Gen Z

Market:
India


============================================================
TREND RESEARCH
============================================================

{TREND_RESEARCH}


============================================================
CONSUMER INSIGHTS
============================================================

{CONSUMER_RESEARCH}


============================================================
COMPETITOR INTELLIGENCE
============================================================

{COMPETITOR_RESEARCH}


Based on the combined evidence above, create ONE
strong product innovation concept.

Do not create the marketing campaign yet.
"""

    print("\nSending research to Product Innovation Agent...\n")

    user_message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=question,
            )
        ],
    )

    final_response = None

    # --------------------------------------------------------
    # Run Agent
    # --------------------------------------------------------

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message,
    ):

        if event.is_final_response():

            if (
                event.content
                and event.content.parts
            ):

                text_parts = []

                for part in event.content.parts:

                    if part.text:

                        text_parts.append(
                            part.text
                        )

                if text_parts:

                    final_response = "\n".join(
                        text_parts
                    )

    # --------------------------------------------------------
    # Display Output
    # --------------------------------------------------------

    print("=" * 70)
    print("PRODUCT INNOVATION RESULT")
    print("=" * 70)

    if final_response:

        print(
            final_response.strip()
        )

    else:

        print(
            "❌ No final response returned."
        )

    print("=" * 70)

    if final_response:

        print(
            "\n✅ Product Innovation Agent test PASSED"
        )


# ============================================================
# Main
# ============================================================

def main() -> None:
    """
    Script entry point.
    """

    asyncio.run(
        run_innovation_agent()
    )


if __name__ == "__main__":
    main()