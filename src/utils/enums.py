#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Date: 07/11/2025
    Author: Joshua David Golafshan
"""

from enum import Enum


class SignalType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


class StatusType(Enum):
    PENDING = "PENDING"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class PositionType(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
