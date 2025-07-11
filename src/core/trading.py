#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Date: 07/11/2025
    Author: Joshua David Golafshan
"""

import os
import pandas as pd
from binance.client import Client
from application_constants import BINANCE_API_KEY, BINANCE_SECRET_KEY

# Test

client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY, testnet=True)

# Live trading
# client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

ping = client.ping()
print(ping)
time_res = client.get_server_time()
print(time_res)


class bianace_base:
    pass
