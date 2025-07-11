#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Date: 07/11/2025
    Author: Joshua David Golafshan
    Description: MYSQL Database Modals
"""

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, func, ForeignKey
from src.utils.enums import SignalType, OrderType, OrderSide, StatusType, PositionType

# TODO Executions (Partial Fills), Accounts, Strats (use those 2 handle metrics)


Base = declarative_base()


class Signal(Base):
    __tablename__ = 'signals'

    id = Column(Integer, primary_key=True)
    stock_symbol = Column(String(10), nullable=False)
    signal_type = Column(SQLEnum(SignalType, name="signaltype"), nullable=False)
    confidence = Column(Float)
    signal_datetime = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return (
            f"<Signal(id={self.id}, symbol='{self.stock_symbol}', "
            f"type={self.signal_type}, confidence={self.confidence})>"
        )


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    signal_id = Column(Integer, ForeignKey("signals.id"))
    stock_symbol = Column(String(10), nullable=False)
    order_type = Column(SQLEnum(OrderType, name="ordertype"), nullable=False)
    side = Column(SQLEnum(OrderSide, name="sidetype"), nullable=False)

    quantity = Column(Float, nullable=False)
    price = Column(Float)

    status = Column(SQLEnum(StatusType, name="statustype"), nullable=False, default=StatusType.PENDING)
    submission_datetime = Column(DateTime(timezone=True), server_default=func.now())
    filled_datetime = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return (
            f"<Order(id={self.id}, symbol='{self.stock_symbol}', side={self.side}, "
            f"type={self.order_type}, qty={self.quantity}, status={self.status})>"
        )


class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    stock_symbol = Column(String(10), nullable=False)

    entry_order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    exit_order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)

    quantity = Column(Float, nullable=False)
    entry_price = Column(Float, nullable=True)
    exit_price = Column(Float, nullable=True)

    entry_datetime = Column(DateTime(timezone=True), nullable=True)
    exit_datetime = Column(DateTime(timezone=True), nullable=True)

    status = Column(SQLEnum(PositionType, name="positiontype"), nullable=False, default=StatusType.PENDING)

    def __repr__(self):
        return (
            f"<Position(id={self.id}, symbol='{self.stock_symbol}', "
            f"qty={self.quantity}, status={self.status})>"
        )
