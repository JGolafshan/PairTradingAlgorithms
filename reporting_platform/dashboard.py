#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Date: 07/11/2025
    Author: Joshua David Golafshan
"""

import utils
import os.path
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_extras import *
from pathlib import Path
import plotly.express as px
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy.engine.base import Engine


@st.cache_resource
def inject_css_files():
    SCRIPT_DIR = Path(__file__).resolve()
    PROJECT_LOCATION = SCRIPT_DIR.parents[1]
    css_path = os.path.join(str(PROJECT_LOCATION), "reporting_platform", "style.css")
    print(css_path)
    return st.markdown(utils.load_css(css_path), unsafe_allow_html=True)


@st.cache_resource
def get_db_connection() -> Engine:
    mysql_data = st.secrets["mysql"]
    uri = mysql_data["uri"]
    return create_engine(uri)


def time_selector_logic(time_frame):
    if time_frame == "Custom Range":
        start_date = st.date_input("Start Date", datetime.now().date() - timedelta(days=30))
        end_date = st.date_input("End Date", datetime.now().date())
        if start_date > end_date:
            st.error("Start Date must be before End Date.")
            return
    else:
        end_date = datetime.now().date()
        if time_frame == "Last 7 days":
            start_date = end_date - timedelta(days=7)
        elif time_frame == "Last 30 days":
            start_date = end_date - timedelta(days=30)
        elif time_frame == "Last 90 days":
            start_date = end_date - timedelta(days=90)
    return start_date, end_date


def transaction_history(date_range):
    return pd.DataFrame({
        "Pair": np.random.choice(["BTC-ETH", "ETH-USDT", "BTC-USDT"], size=len(date_range)),
        "Entry Date": date_range,
        "Exit Date": date_range + pd.to_timedelta(np.random.randint(1, 5, size=len(date_range)), unit='D'),
        "Return": np.round(np.random.uniform(-0.05, 0.10, size=len(date_range)), 4)
    })


def return_histogram():
    fake_returns = np.random.normal(loc=0.02, scale=0.05, size=100)
    fig = px.histogram(fake_returns, nbins=8)
    fig.update_layout(
        showlegend=False,
        margin=dict(l=4, r=4, t=6, b=4),
        height=90,
        xaxis=dict(visible=False, fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        bargap=0.1,
    )

    fig.update_traces(
        marker_color='#1f77b4',
        marker_line_width=0,
        opacity=0.65,
        hovertemplate='%{x:.2%} return<br>%{y} trades<extra></extra>',
    )

    fig.add_vline(x=0, line_dash="dot", line_color="gray", opacity=0.3)
    return fig


def main():
    inject_css_files()
    db = get_db_connection()

    # Header
    st.set_page_config(page_title="Algo Trading Dashboard", layout="wide")
    st.title("Pairs Trading Metrics")

    # Timeframe selector
    col1, col2 = st.columns([0.2, 0.8])
    time_frame = col1.selectbox("Select Time Period",
                                options=["Last 7 days", "Last 30 days", "Last 90 days", "Custom Range"])

    tf_logic = time_selector_logic(time_frame)
    date_range = pd.date_range(start=tf_logic[0], end=tf_logic[1])

    # Metrics
    col1, col2, col3 = st.columns([0.2, 0.2, 0.2], gap="small", vertical_alignment="center")
    col1.metric("PnL", "1.70", "+1.2%", delta_color="normal", help="Profit/Loss Ratio")
    col2.metric("W/L", "1.12", "-8%", delta_color="inverse", help="Winning vs Losing Trades")
    col3.metric("Returns", "86%", "+4%", delta_color="normal", help="Cumulative return")

    # col4.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Table
    st.markdown(f"""
    <div class="trade-header">
        <h3>Trade History</h3>
        <div class="time-period"><strong>Time Period:</strong> {tf_logic[0]} to {tf_logic[1]}</div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        transaction_history(date_range),
        use_container_width=True,
        height=300,
        hide_index=True,
        on_select="ignore",
        column_config={
            "Return": st.column_config.NumberColumn(
                "Return (%)",
                help="Strategy return as a percentage",
                min_value=0.0,
                max_value=100.0,
                step=0.01,
                format="%.2f%%",  # <-- Correct format for percent with 2 decimals
            )
        },
    )


if __name__ == "__main__":
    main()
