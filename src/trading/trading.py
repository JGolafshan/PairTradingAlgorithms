#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Date: 07/11/2025
    Author: Joshua David Golafshan
"""
from typing import Optional

from binance.client import Client
from src.core.application_constants import PAPER_BINANCE_API_KEY, PAPER_BINANCE_API_SECRET, PAPER_TRADE


class BinanceBase:
    def __init__(self, api_key: str, api_secret: str, trading_type: bool):
        self.trading_type = trading_type
        self.client = Client(api_key, api_secret, testnet=trading_type)

    def generate_order(self, _symbol: str, _side: str, _order_type: str, _tim: Optional[str], _quantity: float,
                       _price: Optional[float]):
        return self.client.create_order(
            symbol=_symbol,
            side=_side,
            type=_order_type,
            timeInForce=_tim,
            quantity=_quantity,
            price=_price
        )


test = BinanceBase(PAPER_BINANCE_API_KEY, PAPER_BINANCE_API_SECRET, PAPER_TRADE)
#print(test.generate_order(_symbol="ETHUSDT", _side="SELL", _order_type="MARKET", _tim=None, _price=None, _quantity=2))
x = test.client.get_asset_balance("USDT")
print(x)
