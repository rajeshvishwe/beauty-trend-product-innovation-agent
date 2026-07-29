"""
Central configuration for the Beauty Trend & Product Innovation Agent.

This module loads environment variables and exposes application settings
to the rest of the project.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()


# ============================================================
# Application configuration
# ============================================================

APP_NAME = os.getenv(
    "APP_NAME",
    "beauty_trend_innovation_agent",
)

APP_ENV = os.getenv(
    "APP_ENV",
    "local",
)

GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY"
)

SERPER_API_KEY = os.getenv(
    "SERPER_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.1-flash-lite",
)


# ============================================================
# Validation
# ============================================================

def validate_config() -> None:
    """
    Validate mandatory application configuration.

    Raises:
        ValueError:
            If required configuration is missing.
    """

    missing_values = []

    if not GOOGLE_API_KEY:
        missing_values.append(
            "GOOGLE_API_KEY"
        )

    if not SERPER_API_KEY:
        missing_values.append(
            "SERPER_API_KEY"
        )

    if missing_values:
        raise ValueError(
            "Missing required environment variables: "
            + ", ".join(missing_values)
        )


# ============================================================
# Safe Configuration Display
# ============================================================

def print_config() -> None:
    """
    Print application configuration without exposing secrets.
    """

    print("=" * 60)

    print(
        "Beauty Trend & Product Innovation Agent"
    )

    print("=" * 60)

    print(
        f"App Name     : {APP_NAME}"
    )

    print(
        f"Environment  : {APP_ENV}"
    )

    print(
        f"Gemini Model : {GEMINI_MODEL}"
    )

    print(
        "Google API   : "
        + (
            "Configured"
            if GOOGLE_API_KEY
            else "Missing"
        )
    )

    print(
        "Serper API   : "
        + (
            "Configured"
            if SERPER_API_KEY
            else "Missing"
        )
    )

    print("=" * 60)


# ============================================================
# Standalone Test
# ============================================================

if __name__ == "__main__":

    validate_config()

    print_config()