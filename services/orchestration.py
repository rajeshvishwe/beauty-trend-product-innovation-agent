"""
End-to-end orchestration service for the
Beauty Trend & Product Innovation Agent.

Workflow:

1. Trend Research Agent
2. Consumer Insight Agent
3. Competitor Intelligence Agent
4. Product Innovation Agent
5. Marketing Campaign Agent
6. Executive Innovation Report
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from google.adk.runners import InMemoryRunner
from google.genai import types

from agents.campaign_agent import campaign_agent
from agents.competitor_agent import competitor_agent
from agents.consumer_agent import consumer_agent
from agents.innovation_agent import innovation_agent
from agents.trend_agent import trend_agent

from services.report_generator import (
    generate_executive_report,
)


APP_NAME = "beauty_trend_innovation_agent"
USER_ID = "demo_user"


@dataclass
class BeautyInnovationResult:
    """
    Stores outputs produced by the complete workflow.
    """

    trend_insights: str
    consumer_insights: str
    competitor_insights: str
    product_concept: str
    campaign_concept: str
    executive_report: str


async def run_agent(
    agent: Any,
    prompt: str,
    session_prefix: str,
) -> str:
    """
    Run one Google ADK agent and return final text.
    """

    session_id = (
        f"{session_prefix}_{uuid4().hex[:8]}"
    )

    runner = InMemoryRunner(
        agent=agent,
        app_name=APP_NAME,
    )

    await runner.session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    user_message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=prompt,
            )
        ],
    )

    final_response = None

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
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

    if not final_response:
        raise RuntimeError(
            f"Agent '{agent.name}' returned no final response."
        )

    return final_response.strip()


async def run_beauty_innovation_workflow(
    category: str,
    target_audience: str,
    market: str,
    business_question: str,
) -> BeautyInnovationResult:
    """
    Execute complete beauty innovation workflow.
    """

    print("=" * 70)
    print("BEAUTY TREND & PRODUCT INNOVATION WORKFLOW")
    print("=" * 70)

    print(f"Category        : {category}")
    print(f"Target Audience : {target_audience}")
    print(f"Market          : {market}")
    print(f"Business Query  : {business_question}")

    # ========================================================
    # 1. Trend Research
    # ========================================================

    print(
        "\n[1/6] Running Trend Research Agent..."
    )

    trend_prompt = f"""
Research current and emerging beauty trends.

Category:
{category}

Target Audience:
{target_audience}

Market:
{market}

Business Question:
{business_question}

Identify relevant trends and innovation signals.
"""

    trend_insights = await run_agent(
        agent=trend_agent,
        prompt=trend_prompt,
        session_prefix="trend",
    )

    print("✅ Trend Research completed")

    # ========================================================
    # 2. Consumer Insight
    # ========================================================

    print(
        "\n[2/6] Running Consumer Insight Agent..."
    )

    consumer_prompt = f"""
Analyze consumer needs, pain points and desired features.

Category:
{category}

Target Audience:
{target_audience}

Market:
{market}

Business Question:
{business_question}

Use the consumer review knowledge base.
"""

    consumer_insights = await run_agent(
        agent=consumer_agent,
        prompt=consumer_prompt,
        session_prefix="consumer",
    )

    print("✅ Consumer Insight completed")

    # ========================================================
    # 3. Competitor Intelligence
    # ========================================================

    print(
        "\n[3/6] Running Competitor Intelligence Agent..."
    )

    competitor_prompt = f"""
Research competitor patterns and potential whitespace.

Category:
{category}

Target Audience:
{target_audience}

Market:
{market}

Business Question:
{business_question}

Trend Intelligence:

{trend_insights}

Identify:

- competitor patterns
- common features
- differentiation
- potential market gaps
"""

    competitor_insights = await run_agent(
        agent=competitor_agent,
        prompt=competitor_prompt,
        session_prefix="competitor",
    )

    print(
        "✅ Competitor Intelligence completed"
    )

    # ========================================================
    # 4. Product Innovation
    # ========================================================

    print(
        "\n[4/6] Running Product Innovation Agent..."
    )

    innovation_prompt = f"""
Create ONE strongest beauty product concept.

BUSINESS CONTEXT

Category:
{category}

Target Audience:
{target_audience}

Market:
{market}

Business Question:
{business_question}


TREND INTELLIGENCE

{trend_insights}


CONSUMER INSIGHTS

{consumer_insights}


COMPETITOR INTELLIGENCE

{competitor_insights}


Create one differentiated product concept.

Do not create the marketing campaign.
"""

    product_concept = await run_agent(
        agent=innovation_agent,
        prompt=innovation_prompt,
        session_prefix="innovation",
    )

    print(
        "✅ Product Innovation completed"
    )

    # ========================================================
    # 5. Marketing Campaign
    # ========================================================

    print(
        "\n[5/6] Running Marketing Campaign Agent..."
    )

    campaign_prompt = f"""
Create a concise beauty marketing campaign.

Market:
{market}

Target Audience:
{target_audience}

Product Concept:

{product_concept}

Create a presentation-friendly campaign concept.
"""

    campaign_concept = await run_agent(
        agent=campaign_agent,
        prompt=campaign_prompt,
        session_prefix="campaign",
    )

    print(
        "✅ Marketing Campaign completed"
    )

    # ========================================================
    # 6. Executive Report
    # ========================================================

    print(
        "\n[6/6] Generating Executive Innovation Report..."
    )

    executive_report = generate_executive_report(
        category=category,
        target_audience=target_audience,
        market=market,
        business_question=business_question,
        trend_insights=trend_insights,
        consumer_insights=consumer_insights,
        competitor_insights=competitor_insights,
        product_concept=product_concept,
        campaign_concept=campaign_concept,
    )

    print(
        "✅ Executive Report completed"
    )

    print(
        "\n✅ COMPLETE WORKFLOW FINISHED"
    )

    return BeautyInnovationResult(
        trend_insights=trend_insights,
        consumer_insights=consumer_insights,
        competitor_insights=competitor_insights,
        product_concept=product_concept,
        campaign_concept=campaign_concept,
        executive_report=executive_report,
    )