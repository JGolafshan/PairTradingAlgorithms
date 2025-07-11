#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Date: 07/11/2025
    Author: Joshua David Golafshan
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from configparser import ConfigParser

# Load .env file
load_dotenv()

# Load config.ini
config = ConfigParser()
config.read(Path(__file__).resolve().parents[2] / "config.ini")


# === Helper to get from config.ini or fallback to .env ===
def get_config_var(key, section="application_settings", default=None, required=False):
    val = os.getenv(key)  # .env has priority
    if not val and config.has_option(section, key):
        val = config.get(section, key)
    if required and not val:
        raise EnvironmentError(f"Missing required configuration: {key}")
    return val or default


# === Core Paths ===
SCRIPT_DIR = Path(__file__).resolve()
PROJECT_LOCATION = SCRIPT_DIR.parents[2]

raw_save_location = get_config_var("SAVE_LOCATION", default="DEFAULT")
LOGGING_LEVEL = get_config_var("LOGGING_LEVEL", default="INFO")
DELIMITER_GLOBAL = get_config_var("DELIMITER_GLOBAL", default=",")

if raw_save_location.strip().upper() == "DEFAULT":
    SAVE_LOCATION = PROJECT_LOCATION / "data_repository"
else:
    SAVE_LOCATION = Path(raw_save_location).expanduser().resolve()

# === Webscraping Contestants ===
NA_VALUE = "N/A"

# === .ENV VARIABLES ===

EMAIL_ADDRESS = get_config_var("EMAIL_ADDRESS")
EMAIL_TO_ADDRESS = get_config_var("EMAIL_TO_ADDRESS")
EMAIL_SECRET = get_config_var("EMAIL_SECRET")

BINANCE_API_KEY = get_config_var("BINANCE_API_KEY")
BINANCE_SECRET_KEY = get_config_var("BINANCE_SECRET_KEY")


DATABASE_URI = get_config_var("DATABASE_URI")
