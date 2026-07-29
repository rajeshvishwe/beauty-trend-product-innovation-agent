"""
Executive report generator for the
Beauty Trend & Product Innovation Agent.

This module converts the outputs of all five agents into
one concise executive innovation report.
"""

from __future__ import annotations

from google import genai

from services.config import (
    GEMINI_MODEL,
    GOOGLE_API_KEY,
)


def generate_executive_report(
    category: str,
    target_audience: str,
    market: str,
    business_question: str,
    trend_insights: str,
    consumer_insights: str,
    competitor_insights: str,
    product_concept: str,
    campaign_concept: str,
) -> str:
    """
    Generate a concise executive innovation report.

    Args:
        category:
            Beauty category.

        target_audience:
            Target consumer group.

        market:
            Geographic market.

        business_question:
            Original business question.

        trend_insights:
            Trend Research Agent output.

        consumer_insights:
            Consumer Insight Agent output.

        competitor_insights:
            Competitor Intelligence Agent output.

        product_concept:
            Product Innovation Agent output.

        campaign_concept:
            Marketing Campaign Agent output.

    Returns:
        Executive report as Markdown text.
    """

    if not GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY is not configured."
        )

    client = genai.Client(
        api_key=GOOGLE_API_KEY,
    )

    prompt = f"""
You are preparing an executive innovation summary for a
global beauty company.

Create a concise, presentation-ready report using the
research below.

Do not invent statistics.

Do not create unsupported scientific or medical claims.

Keep the report business-oriented and easy to read.

============================================================
BUSINESS CONTEXT
============================================================

Category:
{category}

Target Audience:
{target_audience}

Market:
{market}

Business Question:
{business_question}


============================================================
TREND INTELLIGENCE
============================================================

{trend_insights}


============================================================
CONSUMER INSIGHTS
============================================================

{consumer_insights}


============================================================
COMPETITOR INTELLIGENCE
============================================================

{competitor_insights}


============================================================
PRODUCT CONCEPT
============================================================

{product_concept}


============================================================
CAMPAIGN CONCEPT
============================================================

{campaign_concept}


Use this exact structure:


# Executive Beauty Innovation Report

## Opportunity

Summarize the strongest business opportunity in
2-3 sentences.


## Why This Opportunity Matters

Provide 3 concise bullets covering:

- trend signal
- consumer need
- market whitespace


## Recommended Product Direction

Summarize:

- product concept
- target consumer
- core benefits
- differentiation


## Campaign Direction

Include:

- campaign concept
- core message
- recommended channels


## Business Value

Provide 3 concise bullets describing potential business
value, such as:

- stronger personalization
- faster innovation discovery
- reduced research effort
- better consumer insight utilization
- faster concept generation


## Recommended Next Steps

Provide exactly 3 next steps:

1. Validate consumer demand
2. Test product concept
3. Run campaign experimentation


## Executive Takeaway

Provide one strong 2-sentence conclusion suitable for
an interview presentation.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError(
            "Executive report generation returned "
            "an empty response."
        )

    return response.text.strip()