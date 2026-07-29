"""
Standalone test for the Consumer Insight Agent.

Run from project root:

    python scripts/test_consumer_agent.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from google.adk.runners import InMemoryRunner
from google.genai import types


# ============================================================
# Make project root importable
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


from agents.consumer_agent import consumer_agent


# ============================================================
# Test Configuration
# ============================================================

APP_NAME = "beauty_trend_innovation_agent"

USER_ID = "demo_user"

SESSION_ID = "consumer_agent_test"


# ============================================================
# Test Agent
# ============================================================

async def run_consumer_agent() -> None:
    """
    Run one Consumer Insight Agent test using ADK.
    """

    print("=" * 70)
    print("Consumer Insight Agent Test")
    print("=" * 70)

    # --------------------------------------------------------
    # Create ADK runner
    # --------------------------------------------------------

    runner = InMemoryRunner(
        agent=consumer_agent,
        app_name=APP_NAME,
    )

    session_service = runner.session_service

    # --------------------------------------------------------
    # Create session
    # --------------------------------------------------------

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    # --------------------------------------------------------
    # Business question
    # --------------------------------------------------------

    question = """
Analyze consumer needs and pain points for everyday
makeup products for Gen Z consumers.

Focus especially on:

- foundation
- skin tint
- lightweight makeup
- hydration
- SPF
- natural finish

Identify opportunities for a new beauty product.
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

    print("\nRunning Consumer Insight Agent...\n")

    final_response = None

    # --------------------------------------------------------
    # Execute ADK Agent
    # --------------------------------------------------------

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message,
    ):

        # ----------------------------------------------------
        # Display tool calls for learning/debugging
        # ----------------------------------------------------

        if event.content and event.content.parts:

            for part in event.content.parts:

                if part.function_call:
                    print(
                        "🔧 Tool Called:"
                    )

                    print(
                        f"   {part.function_call.name}"
                    )

                    print(
                        f"   Args: "
                        f"{part.function_call.args}"
                    )

                    print()

        # ----------------------------------------------------
        # Capture final agent response
        # ----------------------------------------------------

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
    # Display Final Output
    # --------------------------------------------------------

    print("=" * 70)
    print("CONSUMER INSIGHT RESULT")
    print("=" * 70)

    if final_response:

        print(
            final_response.strip()
        )

    else:

        print(
            "❌ No final response was returned."
        )

    print("=" * 70)

    if final_response:

        print(
            "\n✅ Consumer Insight Agent test PASSED"
        )


# ============================================================
# Main
# ============================================================

def main() -> None:
    """
    Script entry point.
    """

    asyncio.run(
        run_consumer_agent()
    )


if __name__ == "__main__":
    main()