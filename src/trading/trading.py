#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Date: 07/11/2025
    Author: Joshua David Golafshan
"""

from typing import Literal
from binance.client import Client
from src.utils.enums import TradingType
from src.core.application_constants import BINANCE_API_KEY, BINANCE_SECRET_KEY


class BinanceBase:
    def __init__(self, api_key: str, api_secret: str, trading_type: Literal["LIVE", "PAPER"]):
        self.trading_type = trading_type
        self.client = Client(api_key, api_secret, testnet=self.set_trading_type)

    @property
    def set_trading_type(self) -> bool:
        return self.trading_type == TradingType.PAPER

    def get_data(self):
        pass


test = BinanceBase(BINANCE_API_KEY, BINANCE_SECRET_KEY, "PAPER")
