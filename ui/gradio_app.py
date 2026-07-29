"""
Gradio UI for the Beauty Trend & Product Innovation Agent.

Features:

1. Collect innovation brief
2. Run complete multi-agent workflow
3. Display all agent outputs
4. Generate executive report
5. Download executive report as Markdown
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import gradio as gr


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
# Output Directory
# ============================================================

OUTPUT_DIR = PROJECT_ROOT / "outputs"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# Save Executive Report
# ============================================================

def save_executive_report(
    report: str,
) -> str:
    """
    Save executive report as a Markdown file.

    Args:
        report:
            Generated executive report.

    Returns:
        Absolute path to generated report.
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    file_path = OUTPUT_DIR / (
        f"beauty_innovation_report_{timestamp}.md"
    )

    file_path.write_text(
        report,
        encoding="utf-8",
    )

    return str(
        file_path.resolve()
    )


# ============================================================
# Main Workflow
# ============================================================

async def generate_innovation(
    category: str,
    target_audience: str,
    market: str,
    business_question: str,
):
    """
    Run complete beauty innovation workflow.
    """

    if not category:
        raise gr.Error(
            "Please select a beauty category."
        )

    if not target_audience.strip():
        raise gr.Error(
            "Please enter the target audience."
        )

    if not market.strip():
        raise gr.Error(
            "Please enter the target market."
        )

    if not business_question.strip():
        raise gr.Error(
            "Please enter a business question."
        )

    try:

        result = await run_beauty_innovation_workflow(
            category=category,
            target_audience=target_audience.strip(),
            market=market.strip(),
            business_question=business_question.strip(),
        )

        report_file = save_executive_report(
            result.executive_report
        )

        return (
            result.trend_insights,
            result.consumer_insights,
            result.competitor_insights,
            result.product_concept,
            result.campaign_concept,
            result.executive_report,
            report_file,
        )

    except Exception as exc:

        raise gr.Error(
            f"Workflow failed: {exc}"
        ) from exc


# ============================================================
# Gradio Application
# ============================================================

with gr.Blocks(
    title="Beauty Trend & Product Innovation AI",
) as demo:

    # ========================================================
    # Header
    # ========================================================

    gr.Markdown(
        """
# 💄 Beauty Trend & Product Innovation AI

### Enterprise Agentic GenAI POC

Transform **beauty trends + consumer feedback +
competitive intelligence** into a new product concept
and marketing campaign.
"""
    )

    # ========================================================
    # Input Section
    # ========================================================

    gr.Markdown(
        "## 🔍 Innovation Brief"
    )

    with gr.Row():

        category = gr.Dropdown(
            choices=[
                "Makeup",
                "Skincare",
                "Haircare",
            ],
            value="Makeup",
            label="Beauty Category",
        )

        target_audience = gr.Textbox(
            value="Gen Z",
            label="Target Audience",
            placeholder=(
                "Example: Gen Z"
            ),
        )

        market = gr.Textbox(
            value="India",
            label="Market",
            placeholder=(
                "Example: India"
            ),
        )

    business_question = gr.Textbox(
        value=(
            "Identify emerging everyday makeup opportunities "
            "and suggest a differentiated product concept "
            "for consumers who prefer lightweight, natural "
            "and multi-benefit beauty products."
        ),
        label="Business Question",
        lines=4,
    )

    generate_button = gr.Button(
        "✨ Generate Beauty Innovation",
        variant="primary",
    )

    gr.Markdown(
        """
---

## 🤖 AI Innovation Results
"""
    )

    # ========================================================
    # Output Tabs
    # ========================================================

    with gr.Tabs():

        # ----------------------------------------------------
        # Trend
        # ----------------------------------------------------

        with gr.Tab(
            "📈 Trends"
        ):

            trend_output = gr.Markdown(
                "Trend intelligence will appear here."
            )

        # ----------------------------------------------------
        # Consumer
        # ----------------------------------------------------

        with gr.Tab(
            "👥 Consumer"
        ):

            consumer_output = gr.Markdown(
                "Consumer insights will appear here."
            )

        # ----------------------------------------------------
        # Competitor
        # ----------------------------------------------------

        with gr.Tab(
            "🏢 Market Gap"
        ):

            competitor_output = gr.Markdown(
                "Competitor whitespace will appear here."
            )

        # ----------------------------------------------------
        # Product
        # ----------------------------------------------------

        with gr.Tab(
            "💡 Product"
        ):

            product_output = gr.Markdown(
                "Product concept will appear here."
            )

        # ----------------------------------------------------
        # Campaign
        # ----------------------------------------------------

        with gr.Tab(
            "📣 Campaign"
        ):

            campaign_output = gr.Markdown(
                """
## Campaign Concept

Campaign name, core message, channels,
social strategy and influencer activation
will appear here.

**Example style:**  
*"Your Skin, Just Smarter"*
"""
            )

        # ----------------------------------------------------
        # Executive Report
        # ----------------------------------------------------

        with gr.Tab(
            "📋 Executive Report"
        ):

            executive_output = gr.Markdown(
                """
# Executive Beauty Innovation Report

Run the workflow to generate the complete
executive summary.
"""
            )

            gr.Markdown(
                "### 📥 Download Report"
            )

            report_file = gr.File(
                label="Executive Innovation Report",
                interactive=False,
            )

    # ========================================================
    # Architecture Description
    # ========================================================

    gr.Markdown(
        """
---

### 🧠 Agentic Workflow

**Trend Research Agent**  
→ Live beauty trend research

**Consumer Insight Agent**  
→ FAISS RAG over consumer reviews

**Competitor Intelligence Agent**  
→ Competitor analysis and whitespace

**Product Innovation Agent**  
→ New product concept

**Marketing Campaign Agent**  
→ Campaign strategy

**Executive Report Generator**  
→ Business-ready innovation summary
"""
    )

    # ========================================================
    # Event
    # ========================================================

    generate_button.click(
        fn=generate_innovation,
        inputs=[
            category,
            target_audience,
            market,
            business_question,
        ],
        outputs=[
            trend_output,
            consumer_output,
            competitor_output,
            product_output,
            campaign_output,
            executive_output,
            report_file,
        ],
    )


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    demo.queue()

    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
    )