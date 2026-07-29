"""
Premium Gradio UI for the Beauty Trend & Product Innovation Agent.

Features:
1. Premium beauty-tech dashboard design
2. Innovation brief input panel
3. Multi-agent workflow visualization
4. Trend intelligence
5. Consumer insights
6. Competitor / market-gap intelligence
7. Product innovation concept
8. Marketing campaign concept
9. Executive report
10. Downloadable report
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
# Premium Custom CSS
# ============================================================

CUSTOM_CSS = """
/* =========================================================
   GLOBAL APP
========================================================= */

.gradio-container {
    max-width: 1500px !important;
    margin: 0 auto !important;
    background:
        radial-gradient(circle at 5% 5%, rgba(255, 220, 235, 0.40), transparent 25%),
        radial-gradient(circle at 95% 10%, rgba(232, 220, 255, 0.35), transparent 25%),
        linear-gradient(180deg, #fffafd 0%, #ffffff 42%, #fbf9ff 100%);
}


/* =========================================================
   HERO SECTION
========================================================= */

#hero-section {
    background:
        linear-gradient(
            120deg,
            rgba(95, 27, 78, 1) 0%,
            rgba(157, 54, 121, 1) 48%,
            rgba(213, 110, 151, 1) 100%
        );

    padding: 34px 38px;
    border-radius: 26px;
    margin-top: 12px;
    margin-bottom: 24px;

    box-shadow:
        0 18px 45px rgba(100, 35, 90, 0.18);

    border: 1px solid rgba(255, 255, 255, 0.25);
}

#hero-section h1 {
    color: white !important;
    font-size: 38px !important;
    font-weight: 800 !important;
    margin-bottom: 8px !important;
    letter-spacing: -0.5px;
}

#hero-section h3 {
    color: #ffe9f4 !important;
    margin-top: 0 !important;
    font-weight: 500 !important;
}

#hero-section p {
    color: rgba(255, 255, 255, 0.93) !important;
    font-size: 16px !important;
    line-height: 1.6 !important;
}


/* =========================================================
   BADGES
========================================================= */

.hero-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.16);
    border: 1px solid rgba(255, 255, 255, 0.28);
    color: white;
    font-size: 12px;
    font-weight: 700;
    margin-right: 7px;
    margin-top: 10px;
}


/* =========================================================
   SECTION TITLES
========================================================= */

.section-title {
    font-size: 23px;
    font-weight: 800;
    color: #40223d;
    margin-top: 8px;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #796575;
    font-size: 14px;
    margin-bottom: 16px;
}


/* =========================================================
   CARDS
========================================================= */

.premium-card {
    background: rgba(255, 255, 255, 0.90);
    border: 1px solid rgba(148, 97, 137, 0.13);
    border-radius: 20px;
    padding: 18px;

    box-shadow:
        0 8px 30px rgba(78, 43, 70, 0.07);
}

#input-card {
    background:
        linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.96),
            rgba(255, 246, 251, 0.96)
        );

    border: 1px solid rgba(194, 116, 158, 0.18);
    border-radius: 22px;
    padding: 22px;

    box-shadow:
        0 12px 35px rgba(95, 55, 85, 0.08);
}


/* =========================================================
   GENERATE BUTTON
========================================================= */

#generate-btn {
    min-height: 52px !important;
    border-radius: 16px !important;

    font-size: 16px !important;
    font-weight: 800 !important;

    border: none !important;

    background:
        linear-gradient(
            90deg,
            #7a295f 0%,
            #ae3d82 50%,
            #d7689c 100%
        ) !important;

    color: white !important;

    box-shadow:
        0 8px 22px rgba(151, 50, 113, 0.28) !important;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease !important;
}

#generate-btn:hover {
    transform: translateY(-2px);

    box-shadow:
        0 12px 28px rgba(151, 50, 113, 0.36) !important;
}


/* =========================================================
   WORKFLOW CARDS
========================================================= */

.workflow-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-top: 16px;
    margin-bottom: 26px;
}

.workflow-card {
    min-height: 118px;

    background:
        linear-gradient(
            145deg,
            #ffffff,
            #fff8fc
        );

    border: 1px solid #f0dce8;
    border-radius: 18px;
    padding: 16px;

    box-shadow:
        0 7px 20px rgba(91, 55, 79, 0.06);
}

.workflow-number {
    width: 30px;
    height: 30px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 10px;

    background:
        linear-gradient(135deg, #8b2d6c, #d66b9d);

    color: white;
    font-size: 13px;
    font-weight: 800;

    margin-bottom: 10px;
}

.workflow-title {
    color: #44243d;
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 5px;
}

.workflow-desc {
    color: #846f7e;
    font-size: 12px;
    line-height: 1.45;
}


/* =========================================================
   OUTPUT AREA
========================================================= */

#results-container {
    border-radius: 22px;
    overflow: hidden;
}

.output-panel {
    min-height: 430px;

    padding: 18px !important;

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #fffafd
        );

    border-radius: 18px;

    border:
        1px solid rgba(187, 135, 167, 0.13);
}


/* =========================================================
   CAMPAIGN AREA
========================================================= */

#campaign-panel {
    background:
        linear-gradient(
            135deg,
            rgba(255, 245, 250, 1),
            rgba(252, 242, 255, 1)
        );

    border: 1px solid rgba(191, 102, 157, 0.20);
    border-radius: 20px;

    padding: 20px;

    box-shadow:
        0 10px 28px rgba(139, 57, 112, 0.08);
}


/* =========================================================
   EXECUTIVE REPORT
========================================================= */

#executive-panel {
    background:
        linear-gradient(
            145deg,
            #ffffff,
            #fdf9ff
        );

    border-radius: 20px;

    border:
        1px solid rgba(117, 83, 142, 0.15);

    padding: 20px;

    box-shadow:
        0 10px 28px rgba(85, 55, 110, 0.07);
}


/* =========================================================
   FOOTER / TECH STACK
========================================================= */

.tech-strip {
    margin-top: 28px;
    padding: 18px 22px;

    border-radius: 18px;

    background:
        linear-gradient(
            90deg,
            #fbf5f9,
            #f7f3ff
        );

    border: 1px solid #eee1ea;

    text-align: center;

    color: #61485b;

    font-size: 13px;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 1000px) {

    .workflow-grid {
        grid-template-columns: repeat(2, 1fr);
    }

}

@media (max-width: 650px) {

    .workflow-grid {
        grid-template-columns: 1fr;
    }

    #hero-section {
        padding: 24px;
    }

    #hero-section h1 {
        font-size: 29px !important;
    }
}
"""


# ============================================================
# Save Executive Report
# ============================================================

def save_executive_report(
    report: str,
) -> str:
    """
    Save executive report as Markdown.

    Args:
        report:
            Generated executive report.

    Returns:
        Absolute path of generated report.
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
    Run the complete beauty innovation workflow.
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
# Theme
# ============================================================

APP_THEME = gr.themes.Soft()


# ============================================================
# Gradio Application
# ============================================================

with gr.Blocks(
    title="Beauty Trend & Product Innovation AI",
    theme=APP_THEME,
    css=CUSTOM_CSS,
    fill_width=True,
) as demo:

    # ========================================================
    # HERO
    # ========================================================

    gr.HTML(
        """
        <div id="hero-section">

            <div style="
                font-size: 13px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1.4px;
                color: #ffe0ef;
                margin-bottom: 10px;
            ">
                ENTERPRISE BEAUTY INTELLIGENCE
            </div>

            <h1>
                💄 Beauty Trend & Product Innovation AI
            </h1>

            <h3>
                From emerging trends to launch-ready product concepts
            </h3>

            <p>
                An agentic GenAI innovation engine that combines
                live beauty intelligence, consumer voice,
                competitive whitespace and generative product strategy.
            </p>

            <div>
                <span class="hero-badge">Google ADK</span>
                <span class="hero-badge">Gemini</span>
                <span class="hero-badge">FAISS RAG</span>
                <span class="hero-badge">Live Search</span>
                <span class="hero-badge">Multi-Agent AI</span>
            </div>

        </div>
        """
    )

    # ========================================================
    # INNOVATION BRIEF TITLE
    # ========================================================

    gr.HTML(
        """
        <div class="section-title">
            ✨ Create an Innovation Brief
        </div>

        <div class="section-subtitle">
            Define the business opportunity and let the AI agents
            research, reason and develop a new beauty concept.
        </div>
        """
    )

    # ========================================================
    # INPUT CARD
    # ========================================================

    with gr.Group(
        elem_id="input-card",
    ):

        with gr.Row():

            category = gr.Dropdown(
                choices=[
                    "Makeup",
                    "Skincare",
                    "Haircare",
                ],
                value="Makeup",
                label="💄 Beauty Category",
                info="Select the innovation category",
            )

            target_audience = gr.Textbox(
                value="Gen Z",
                label="👥 Target Audience",
                placeholder=(
                    "Example: Gen Z, Millennials"
                ),
                info="Primary consumer segment",
            )

            market = gr.Textbox(
                value="India",
                label="🌍 Target Market",
                placeholder=(
                    "Example: India"
                ),
                info="Geography for trend research",
            )

        business_question = gr.Textbox(
            value=(
                "Identify emerging everyday makeup opportunities "
                "and suggest a differentiated product concept "
                "for consumers who prefer lightweight, natural "
                "and multi-benefit beauty products."
            ),
            label="💡 Business Innovation Question",
            lines=4,
            placeholder=(
                "Example: What emerging Gen Z makeup opportunity "
                "should we explore in India?"
            ),
        )

        generate_button = gr.Button(
            "✨ Generate Innovation Strategy",
            variant="primary",
            elem_id="generate-btn",
        )

    # ========================================================
    # WORKFLOW
    # ========================================================

    gr.HTML(
        """
        <div style="margin-top: 30px;">

            <div class="section-title">
                🧠 Agentic Innovation Workflow
            </div>

            <div class="section-subtitle">
                Five specialized AI agents collaborate across
                research, consumer intelligence and innovation.
            </div>

            <div class="workflow-grid">

                <div class="workflow-card">
                    <div class="workflow-number">01</div>
                    <div class="workflow-title">
                        📈 Trend Research
                    </div>
                    <div class="workflow-desc">
                        Searches live beauty signals and
                        identifies emerging consumer trends.
                    </div>
                </div>

                <div class="workflow-card">
                    <div class="workflow-number">02</div>
                    <div class="workflow-title">
                        👥 Consumer Insight
                    </div>
                    <div class="workflow-desc">
                        Uses FAISS RAG to uncover needs,
                        pain points and desired features.
                    </div>
                </div>

                <div class="workflow-card">
                    <div class="workflow-number">03</div>
                    <div class="workflow-title">
                        🏢 Competitor Intelligence
                    </div>
                    <div class="workflow-desc">
                        Maps competitive patterns and
                        potential market whitespace.
                    </div>
                </div>

                <div class="workflow-card">
                    <div class="workflow-number">04</div>
                    <div class="workflow-title">
                        💡 Product Innovation
                    </div>
                    <div class="workflow-desc">
                        Synthesizes evidence into one
                        differentiated beauty concept.
                    </div>
                </div>

                <div class="workflow-card">
                    <div class="workflow-number">05</div>
                    <div class="workflow-title">
                        📣 Campaign Strategy
                    </div>
                    <div class="workflow-desc">
                        Converts the product concept into
                        a market-ready campaign direction.
                    </div>
                </div>

            </div>

        </div>
        """
    )

    # ========================================================
    # RESULTS TITLE
    # ========================================================

    gr.HTML(
        """
        <div class="section-title">
            🤖 AI Innovation Intelligence
        </div>

        <div class="section-subtitle">
            Explore the output generated by each specialist agent.
        </div>
        """
    )

    # ========================================================
    # OUTPUT TABS
    # ========================================================

    with gr.Tabs(
        elem_id="results-container",
    ):

        # ----------------------------------------------------
        # TREND TAB
        # ----------------------------------------------------

        with gr.Tab(
            "📈 Trends"
        ):

            gr.Markdown(
                """
### 📈 Beauty Trend Intelligence

Live market signals and emerging beauty directions
identified by the **Trend Research Agent**.
"""
            )

            trend_output = gr.Markdown(
                value=(
                    """
> ✨ Run the innovation workflow to discover
> emerging beauty trends.
"""
                ),
                elem_classes=[
                    "output-panel"
                ],
            )

        # ----------------------------------------------------
        # CONSUMER TAB
        # ----------------------------------------------------

        with gr.Tab(
            "👥 Consumer"
        ):

            gr.Markdown(
                """
### 👥 Voice of the Consumer

Consumer needs, pain points and product expectations
identified through **FAISS RAG**.
"""
            )

            consumer_output = gr.Markdown(
                value=(
                    """
> 👥 Consumer intelligence will appear here
> after running the workflow.
"""
                ),
                elem_classes=[
                    "output-panel"
                ],
            )

        # ----------------------------------------------------
        # MARKET GAP TAB
        # ----------------------------------------------------

        with gr.Tab(
            "🏢 Market Gap"
        ):

            gr.Markdown(
                """
### 🏢 Competitor & Whitespace Intelligence

Competitive product patterns, differentiators and
potential whitespace identified by the
**Competitor Intelligence Agent**.
"""
            )

            competitor_output = gr.Markdown(
                value=(
                    """
> 🔎 Competitive whitespace will appear here
> after market research is completed.
"""
                ),
                elem_classes=[
                    "output-panel"
                ],
            )

        # ----------------------------------------------------
        # PRODUCT TAB
        # ----------------------------------------------------

        with gr.Tab(
            "💡 Product"
        ):

            gr.Markdown(
                """
### 💡 AI Product Innovation Concept

The strongest concept synthesized from trends,
consumer evidence and competitive whitespace.
"""
            )

            product_output = gr.Markdown(
                value=(
                    """
> 💡 Your AI-generated beauty product concept
> will appear here.
"""
                ),
                elem_classes=[
                    "output-panel"
                ],
            )

        # ----------------------------------------------------
        # CAMPAIGN TAB
        # ----------------------------------------------------

        with gr.Tab(
            "📣 Campaign"
        ):

            with gr.Group(
                elem_id="campaign-panel",
            ):

                gr.Markdown(
                    """
# 📣 Campaign Concept

### From Product Innovation → Consumer Story

The Marketing Campaign Agent converts the proposed
product into a launch-ready campaign direction.

> **Example campaign style:**  
> *"Your Skin, Just Smarter"*
"""
                )

                campaign_output = gr.Markdown(
                    value=(
                        """
---

### Campaign strategy will include:

**Campaign Name**  
AI-generated brand campaign concept

**Core Message**  
Consumer-facing product story

**Target Audience**  
Primary campaign segment

**Recommended Channels**  
Instagram · YouTube Shorts · Beauty Creators · E-commerce

**Social Content Ideas**  
Short-form activation concepts

**Influencer Activation**  
Creator-led campaign direction
"""
                    ),
                )

        # ----------------------------------------------------
        # EXECUTIVE REPORT TAB
        # ----------------------------------------------------

        with gr.Tab(
            "📋 Executive Report"
        ):

            with gr.Group(
                elem_id="executive-panel",
            ):

                gr.Markdown(
                    """
# 📋 Executive Beauty Innovation Report

A management-ready synthesis of the entire
multi-agent innovation workflow.
"""
                )

                executive_output = gr.Markdown(
                    value=(
                        """
> Run the workflow to generate the complete
> executive innovation report.
"""
                    ),
                )

                gr.Markdown(
                    """
---

### 📥 Export Innovation Report
"""
                )

                report_file = gr.File(
                    label="Download Executive Innovation Report",
                    interactive=False,
                )

    # ========================================================
    # EXECUTIVE VALUE SECTION
    # ========================================================

    gr.HTML(
        """
        <div style="margin-top: 28px;">

            <div class="section-title">
                🎯 Business Value
            </div>

            <div class="workflow-grid">

                <div class="workflow-card">
                    <div class="workflow-title">
                        ⚡ Faster Insight Discovery
                    </div>
                    <div class="workflow-desc">
                        Compress market research and trend
                        discovery into an AI-assisted workflow.
                    </div>
                </div>

                <div class="workflow-card">
                    <div class="workflow-title">
                        ❤️ Consumer-Led Innovation
                    </div>
                    <div class="workflow-desc">
                        Bring consumer reviews and unmet
                        needs directly into ideation.
                    </div>
                </div>

                <div class="workflow-card">
                    <div class="workflow-title">
                        🔍 Whitespace Identification
                    </div>
                    <div class="workflow-desc">
                        Compare market patterns to uncover
                        possible differentiation opportunities.
                    </div>
                </div>

                <div class="workflow-card">
                    <div class="workflow-title">
                        💡 Faster Concept Generation
                    </div>
                    <div class="workflow-desc">
                        Convert research evidence into
                        structured product concepts quickly.
                    </div>
                </div>

                <div class="workflow-card">
                    <div class="workflow-title">
                        📣 Campaign Acceleration
                    </div>
                    <div class="workflow-desc">
                        Extend product strategy directly into
                        campaign and activation concepts.
                    </div>
                </div>

            </div>

        </div>
        """
    )

    # ========================================================
    # TECH STACK FOOTER
    # ========================================================

    gr.HTML(
        """
        <div class="tech-strip">

            <strong>Powered by:</strong>

            Google ADK
            &nbsp; • &nbsp;
            Gemini
            &nbsp; • &nbsp;
            FAISS
            &nbsp; • &nbsp;
            Sentence Transformers
            &nbsp; • &nbsp;
            Serper Search
            &nbsp; • &nbsp;
            Gradio

            <br><br>

            <span style="color:#8c7485;">
                Beauty Trend & Product Innovation AI
                · Enterprise GenAI Proof of Concept
            </span>

        </div>
        """
    )

    # ========================================================
    # EVENT
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