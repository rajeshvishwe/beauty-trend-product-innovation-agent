"""
Standalone test for the Competitor Intelligence Agent.

Run from project root:

    python scripts/test_competitor_agent.py
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


from agents.competitor_agent import competitor_agent


# ============================================================
# Test Configuration
# ============================================================

APP_NAME = "beauty_trend_innovation_agent"

USER_ID = "demo_user"

SESSION_ID = "competitor_agent_test"


# ============================================================
# Competitor Agent Test
# ============================================================

async def run_competitor_agent() -> None:
    """
    Execute one competitor intelligence test.
    """

    print("=" * 70)
    print("Competitor Intelligence Agent Test")
    print("=" * 70)

    runner = InMemoryRunner(
        agent=competitor_agent,
        app_name=APP_NAME,
    )

    session_service = runner.session_service

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    question = """
Research competitor products relevant to a new everyday
makeup product for Gen Z consumers in India.

Focus on products such as:

- skin tints
- lightweight foundations
- BB creams
- serum foundations
- SPF makeup
- skincare + makeup hybrids

Compare common features such as:

- lightweight coverage
- hydration
- SPF
- natural finish
- skincare ingredients
- long wear

Identify potential market gaps and product whitespace.
"""

    print("\nBusiness Question:")
    print("-" * 70)
    print(question.strip())
    print("-" * 70)

    user_message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=question,
            )
        ],
    )

    print(
        "\nRunning Competitor Intelligence Agent...\n"
    )

    final_response = None

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message,
    ):

        if event.content and event.content.parts:

            for part in event.content.parts:

                if part.function_call:

                    print(
                        "🔎 Search Tool Called:"
                    )

                    print(
                        f"   {part.function_call.name}"
                    )

                    print(
                        f"   Args: "
                        f"{part.function_call.args}"
                    )

                    print()

        if event.is_final_response():

            if event.content and event.content.parts:

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
    print("COMPETITOR INTELLIGENCE RESULT")
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
            "\n✅ Competitor Intelligence Agent test PASSED"
        )


def main() -> None:
    """
    Script entry point.
    """

    asyncio.run(
        run_competitor_agent()
    )


if __name__ == "__main__":
    main()