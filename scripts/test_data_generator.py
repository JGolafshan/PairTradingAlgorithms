#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Test Data Generator for Crypto Pair Trading Strategy
    Simulates 1 year of pair trading using mean reversion on BTC/ETH
"""

import random
import datetime

from src.core.database import Database
from src.core.database_models import Signal, Order, Position
from src.utils.enums import SignalType, OrderType, OrderSide, StatusType, PositionType

# Initialize DB and session
db = Database(echo=False)
session = db.get_session()

# Simulation config
START_DATE = datetime.datetime(2024, 7, 1)
INTERVAL_MINUTES = 15
NUM_INTERVALS = 50000
PAIR = "BTC/ETH"
BASE_PRICE = 15.0

open_position = None


def generate_price(mean=BASE_PRICE):
    """Simulate ratio around mean with noise"""
    return round(mean + random.uniform(-1.5, 1.5), 3)


def simulate():
    current_time = START_DATE
    created = 0

    for _ in range(NUM_INTERVALS):
        price = generate_price()
        signal_type = None

        if price > BASE_PRICE + 1:
            signal_type = SignalType.SELL
        elif price < BASE_PRICE - 1:
            signal_type = SignalType.BUY
        else:
            current_time += datetime.timedelta(minutes=INTERVAL_MINUTES)
            continue

        # 1. Create Signal
        signal = Signal(
            stock_symbol=PAIR,
            signal_type=signal_type,
            confidence=round(random.uniform(0.7, 0.95), 3),
            signal_datetime=current_time,
        )
        session.add(signal)
        session.flush()  # get signal.id

        # 2. Create Order
        order = Order(
            signal_id=signal.id,
            stock_symbol=PAIR,
            order_type=OrderType.MARKET,
            side=OrderSide.BUY if signal_type == SignalType.BUY else OrderSide.SELL,
            quantity=round(random.uniform(0.5, 2.5), 3),
            price=price,
            status=StatusType.FILLED,
            submission_datetime=current_time,
            filled_datetime=current_time + datetime.timedelta(seconds=2),
        )
        session.add(order)
        session.flush()  # get order.id

        # 3. Create or close Position
        global open_position

        if signal_type == SignalType.BUY and open_position is None:
            open_position = Position(
                stock_symbol=PAIR,
                entry_order_id=order.id,
                quantity=order.quantity,
                entry_price=order.price,
                entry_datetime=order.filled_datetime,
                status=PositionType.OPEN,
            )
            session.add(open_position)

        elif signal_type == SignalType.SELL and open_position:
            open_position.exit_order_id = order.id
            open_position.exit_price = order.price
            open_position.exit_datetime = order.filled_datetime
            open_position.status = PositionType.CLOSED
            session.merge(open_position)
            open_position = None

        current_time += datetime.timedelta(minutes=INTERVAL_MINUTES)
        created += 1

        if created % 500 == 0:
            session.commit()
            print(f"Inserted {created} records...")

    session.commit()
    print("✅ Finished simulating test data.")


if __name__ == "__main__":
    simulate()
