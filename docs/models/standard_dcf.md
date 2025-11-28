---
tags:
  - valuation
  - intrinsic-value
  - dcf
  - fundamentals
aliases:
  - Standard DCF
  - Discounted Cash Flow
  - The Time Machine
created: 2025-11-28
---
# The Standard DCF (The Time Machine)

> [!INFO] Metadata
> * **Category:** Valuation > Intrinsic
> * **Target Phase:** Mature / Stable Growth (Phase 3)
> * **Key Levers:** WACC, Growth Rate, Margins
> * **Complexity:** ⭐⭐⭐ (Medium)

---

## 1. Core Concept: The Physics of Money
The Discounted Cash Flow (DCF) is the bedrock of finance. It treats a company not as a ticker symbol, but as a machine that prints money over time.

Because money printed *tomorrow* is worth less than money held *today* (due to inflation, opportunity cost, and risk), we must "discount" those future cash flows back to the present.

> [!NOTE] 🧠 Mental Model: The Reverse Bank Account
> Imagine you want to buy a machine that spits out $100 every year forever.
> * If the bank pays 5% interest, you would need $2,000 in the bank to get $100/year.
> * Therefore, the machine is worth **$2,000** today.
> 
> The DCF just runs this math in reverse: It looks at the future payments ($100) and the risk (5%) to tell you the price tag ($2,000).

---

## 2. The Calculation (The Engine)
We project cash flows for a specific period (e.g., 5-10 years) and then estimate a "Terminal Value" for everything after that.

### The Formula
$$ \text{Value} = \sum_{t=1}^{n} \frac{\text{FCF}_t}{(1 + r)^t} + \frac{\text{Terminal Value}}{(1 + r)^n} $$

*   **FCF (Free Cash Flow):** The cash left over after paying bills and reinvesting for growth.
    *   $FCF = \text{EBIT}(1-t) + \text{D\&A} - \text{CapEx} - \Delta \text{Working Capital}$
*   **$r$ (WACC):** The discount rate. The return investors demand for the risk they are taking.
*   **Terminal Value:** The value of the company from Year $n$ until forever.
    *   Gordon Growth Method: $TV = \frac{FCF_{n+1}}{r - g}$

---

## 3. The Wolf's Edge (Probabilistic DCF)
Single-point DCFs are dangerous ("Garbage in, Garbage out"). We use **Monte Carlo Simulations** to replace static inputs with probability distributions.

*   **Growth:** Triangular Distribution (Bear / Base / Bull).
*   **Margins:** Normal Distribution (Historical mean + volatility).
*   **WACC:** Normal Distribution (Risk-free rate variance).

### Python Implementation
```python
import numpy as np

# 1. SETUP
SIMULATIONS = 50000
growth_dist = np.random.triangular(0.05, 0.08, 0.10, SIMULATIONS)
margin_dist = np.random.normal(0.20, 0.02, SIMULATIONS)
wacc_dist = np.random.normal(0.10, 0.01, SIMULATIONS)

# 2. THE ENGINE
revenues = current_rev * (1 + growth_dist)
ebit = revenues * margin_dist
fcf = ebit * (1 - tax_rate) * conversion_ratio

# Discounting
pv = fcf / (1 + wacc_dist)
```

---

## 4. Interpretation: The Kill Zone
We do not look for a specific number. We look for the **Probability of Profit**.

> [!TIP] Strategy
> * **Buy Signal:** Price < P10 (Bear Case). The market is pricing in a disaster that likely won't happen.
> * **Sell Signal:** Price > P90 (Bull Case). The market is pricing in perfection.
> * **The Edge:** When the "Story" (Qualitative) disagrees with the "Math" (Quantitative), and you know why.

