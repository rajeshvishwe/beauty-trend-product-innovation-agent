"""
Main application entry point for the
Beauty Trend & Product Innovation Agent.

Run:

    python app.py
"""

from __future__ import annotations

from ui.gradio_app import demo


def main() -> None:
    """
    Launch the local Gradio application.
    """

    print("=" * 70)
    print("Beauty Trend & Product Innovation AI")
    print("=" * 70)

    print(
        "Starting local Gradio application..."
    )

    print(
        "Open: http://127.0.0.1:7860"
    )

    print("=" * 70)

    demo.queue()

    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
    )


if __name__ == "__main__":
    main()