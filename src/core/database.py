#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Date: 07/11/2025
    Author: Joshua David Golafshan
    Description: Base class for the database.
"""

import logging
from sqlalchemy import text, inspect, MetaData, func
from sqlalchemy import create_engine
from src.core.database_models import Base
from src.core.application_constants import DATABASE_URI
from sqlalchemy.orm import sessionmaker, Session as SessionType, aliased
from src.core.database_models import Order, Position

logger = logging.getLogger(__name__)


class BaseDatabase:
    def __init__(self, database_uri: str = DATABASE_URI, echo: bool = False):
        self.engine = create_engine(
            database_uri,
            connect_args={"ssl": {"ssl_mode": "VERIFY_IDENTITY"}},
            pool_pre_ping=True,
            echo=echo,
        )
        self._Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()

    def get_session(self) -> SessionType:
        """Returns a new SQLAlchemy session."""
        return self._Session()

    def dispose(self):
        """Properly dispose of the engine (closes all connections)."""
        self.engine.dispose()

    def close(self):
        """Close the connection to the database"""
        self._Session.close_all()

    def _generate_tables(self) -> None:
        """Generate Tables from the predefined models."""
        logger.info("Generating tables from Base metadata.")
        Base.metadata.create_all(self.engine)

    def _reset_db(self):
        """Drop and recreate all tables based on SQLAlchemy models."""
        logger.warning("Resetting database: Dropping and recreating all tables.")
        self.metadata.reflect(bind=self.engine, resolve_fks=False)
        self.metadata.drop_all(self.engine)
        self.get_session().commit()
        self.get_session().close()
        self.engine.dispose()

    def is_alive(self) -> bool:
        """Pings the database"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1;"))
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

    def get_columns(self, table_name: str) -> list[str]:
        """Returns a list of column names for a given table."""
        inspector = inspect(self.engine)
        return [col["name"] for col in inspector.get_columns(table_name)]

    def show_tables(self) -> list[str]:
        """Returns a list of all table names in the connected database."""
        inspector = inspect(self.engine)
        return inspector.get_table_names()


from datetime import datetime, timedelta


class TradingDatabase(BaseDatabase):
    def __init__(self):
        super().__init__()

    def get_trade_history(self, duration: int = None):
        """Returns a list of trade history records."""
        session = self.get_session()
        EntryOrder = aliased(Order)
        ExitOrder = aliased(Order)

        query = (
            session.query(
                Position.stock_symbol,
                Position.entry_datetime,
                Position.exit_datetime,
                Position.quantity,
                ((ExitOrder.price - EntryOrder.price) * Position.quantity).label("pnl"),
                (func.extract('epoch', Position.exit_datetime) - func.extract('epoch', Position.entry_datetime))
                .label("duration_seconds")
            )
            .select_from(Position)
            .join(EntryOrder, Position.entry_order_id == EntryOrder.id)
            .join(ExitOrder, Position.exit_order_id == ExitOrder.id)
            .filter(Position.status == "CLOSED")
        )

        if duration is not None:
            since = datetime.utcnow() - timedelta(days=duration)
            query = query.filter(Position.exit_datetime >= since)

        trades = query.all()
        session.close()
        return trades

    def get_pnl(self, duration: int = None):
        """Returns total net PnL across all closed positions."""
        session = self.get_session()
        EntryOrder = aliased(Order)
        ExitOrder = aliased(Order)

        pnl_expr = (ExitOrder.price - EntryOrder.price) * Position.quantity

        query = (
            session.query(func.sum(pnl_expr))
            .select_from(Position)
            .join(EntryOrder, Position.entry_order_id == EntryOrder.id)
            .join(ExitOrder, Position.exit_order_id == ExitOrder.id)
            .filter(Position.status == "CLOSED")
        )

        if duration is not None:
            since = datetime.utcnow() - timedelta(days=duration)
            query = query.filter(Position.exit_datetime >= since)

        total_pnl = query.scalar()
        session.close()
        return total_pnl or 0.0

    def get_win_loss_ratio(self, duration: int = None):
        """Returns (win_count, loss_count, win_ratio) across closed trades."""
        session = self.get_session()
        EntryOrder = aliased(Order)
        ExitOrder = aliased(Order)

        pnl_expr = (ExitOrder.price - EntryOrder.price) * Position.quantity

        base_query = (
            session.query(func.count())
            .select_from(Position)
            .join(EntryOrder, Position.entry_order_id == EntryOrder.id)
            .join(ExitOrder, Position.exit_order_id == ExitOrder.id)
            .filter(Position.status == "CLOSED")
        )

        if duration is not None:
            since =  datetime.utcnow() - timedelta(days=duration)
            base_query = base_query.filter(Position.exit_datetime >= since)

        wins = base_query.filter(pnl_expr > 0).scalar()
        losses = base_query.filter(pnl_expr < 0).scalar()

        total = wins + losses
        win_ratio = wins / total if total > 0 else 0

        session.close()
        return {"wins": wins, "losses": losses, "win_ratio": round(win_ratio, 3)}

    def get_cumm_returns(self, duration: int = None):
        """Returns cumulative return data points as a list of (datetime, cumulative_pnl)."""
        session = self.get_session()
        EntryOrder = aliased(Order)
        ExitOrder = aliased(Order)

        pnl_expr = (ExitOrder.price - EntryOrder.price) * Position.quantity

        query = (
            session.query(
                ExitOrder.filled_datetime.label("exit_time"),
                pnl_expr.label("pnl")
            )
            .select_from(Position)
            .join(EntryOrder, Position.entry_order_id == EntryOrder.id)
            .join(ExitOrder, Position.exit_order_id == ExitOrder.id)
            .filter(Position.status == "CLOSED")
            .order_by(ExitOrder.filled_datetime.asc())
        )

        if duration is not None:
            since = datetime.utcnow() - timedelta(days=duration)
            query = query.filter(Position.exit_datetime >= since)

        trades = query.all()
        session.close()

        # Calculate cumulative return
        cum_returns = []
        total = 0.0
        for t in trades:
            pnl_value = t.pnl or 0.0
            total += pnl_value
            cum_returns.append((t.exit_time, round(total, 2)))

        return cum_returns
