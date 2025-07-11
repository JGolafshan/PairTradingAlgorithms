# Crypto Pairs Trading Strategy with Streamlit Dashboard

This repository implements a **mean-reverting pairs trading strategy** on cryptocurrency pairs, complete with a **Streamlit dashboard** for interactive reporting, analysis, and visualization.

---

## Features

- **Statistical Arbitrage Strategy** using cointegration and z-score thresholds  
- **Automatic Pair Selection** from crypto market data  
- **Backtesting Engine** with performance metrics  
- **Streamlit Dashboard** for live reporting & visual insights  
- Modular codebase for extensibility and real-time integration  
- MYSQL support for storing trade logs and positions

---

## Strategy Overview

---

## 🧪 Streamlit Dashboard

The `Streamlit` dashboard provides:

- Live trade logs
- Spread and z-score plots
- Strategy PnL over time
- Trade signal annotations

```bash
streamlit streamlit run .\reporting_platform\app.py 
```

### 📺 Run the Dashboard

```bash
git clone https://github.com/yourusername/crypto-pairs-trading.git
cd crypto-pairs-trading
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```