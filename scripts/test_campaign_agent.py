"""
Standalone test for the Marketing Campaign Agent.

Run from project root:

    python scripts/test_campaign_agent.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from google.adk.runners import InMemoryRunner
from google.genai import types


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


from agents.campaign_agent import campaign_agent


APP_NAME = "beauty_trend_innovation_agent"

USER_ID = "demo_user"

SESSION_ID = "campaign_agent_test"


PRODUCT_CONCEPT = """
## Product Innovation Concept

### Product Name
SkinGlow Smart Tint

### Product Category
Hybrid Skin Tint

### Target Consumer
Gen Z consumers in India looking for simple,
lightweight everyday complexion products.

### Consumer Problem
Traditional foundation can feel heavy and consumers
may need separate products for hydration, complexion
coverage and sun protection.

### Trend Opportunity
Consumers are increasingly interested in lightweight
makeup, skinification and simplified beauty routines.

### Product Concept
A lightweight skincare-inspired skin tint designed
to provide natural everyday coverage, hydration and
sun protection in one step.

### Key Features

- Lightweight coverage
- Natural skin-like finish
- Hydrating texture
- Everyday SPF
- Comfortable daily wear

### Hero Ingredients / Technology Direction

- Hyaluronic acid
- Niacinamide
- Lightweight UV filter system

### Differentiation
Combines makeup, hydration and everyday sun protection
within one simple Gen Z-oriented complexion product.

### Value Proposition
Your everyday skin, simplified.

### Innovation Confidence
High
"""


async def run_campaign_agent() -> None:
    """
    Execute the Marketing Campaign Agent test.
    """

    print("=" * 70)
    print("Marketing Campaign Agent Test")
    print("=" * 70)

    runner = InMemoryRunner(
        agent=campaign_agent,
        app_name=APP_NAME,
    )

    await runner.session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    question = f"""
Create a marketing campaign for the following
beauty product concept.

Market:
India

Product Innovation Concept:

{PRODUCT_CONCEPT}
"""

    print("\nSending Product Concept to Campaign Agent...\n")

    user_message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=question,
            )
        ],
    )

    final_response = None

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

    print("=" * 70)
    print("MARKETING CAMPAIGN RESULT")
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
            "\n✅ Marketing Campaign Agent test PASSED"
        )


def main() -> None:
    """
    Script entry point.
    """

    asyncio.run(
        run_campaign_agent()
    )


if __name__ == "__main__":
    main()