"""
Standalone test for the Executive Report Generator.

Run:

    python scripts/test_report_generator.py
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


from services.report_generator import (
    generate_executive_report,
)


def main() -> None:
    """
    Test executive report generation.
    """

    report = generate_executive_report(
        category="Makeup",

        target_audience="Gen Z",

        market="India",

        business_question=(
            "Identify emerging everyday makeup "
            "opportunities."
        ),

        trend_insights="""
Lightweight complexion products, skinification,
natural finish and multi-benefit beauty are
important emerging signals.
""",

        consumer_insights="""
Consumers prefer lightweight makeup, hydration,
natural-looking coverage and simplified routines.
Heavy foundations are a recurring pain point.
""",

        competitor_insights="""
Existing products commonly offer lightweight
coverage or hydration, while combining stronger
SPF, skincare positioning and simple Gen Z
positioning may represent whitespace.
""",

        product_concept="""
SkinGlow Smart Tint is a lightweight hybrid
complexion product combining natural coverage,
hydration and everyday sun protection.
""",

        campaign_concept="""
Campaign concept:
Your Skin, Just Smarter.

Primary channels:
Instagram, YouTube Shorts, creators and e-commerce.
""",
    )

    print("=" * 70)
    print("EXECUTIVE INNOVATION REPORT")
    print("=" * 70)

    print(report)

    print("=" * 70)
    print(
        "\n✅ Executive Report Generator test PASSED"
    )


if __name__ == "__main__":
    main()