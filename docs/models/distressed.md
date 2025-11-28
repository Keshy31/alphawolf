---
tags:
  - valuation
  - distressed
  - turnaround
  - liquidation
aliases:
  - Distressed Valuation
  - The Phoenix
  - Liquidation Value
created: 2025-11-28
---
# Distressed Valuation (The Phoenix)

> [!INFO] Metadata
> * **Category:** Valuation > Special Situations
> * **Target Phase:** Decline / Distress / Bankruptcy (Phase 4)
> * **Key Levers:** Burn Rate, Asset Sale Value, Debt Haircut
> * **Complexity:** ⭐⭐⭐⭐⭐ (Very High)

---

## 1. Core Concept: Survival vs. Liquidation
When a company is dying, "Growth" and "Margins" don't matter. **Time** and **Liquidity** matter.

The valuation is a fork in the road:
1.  **Going Concern (The Phoenix):** They fix the balance sheet and return to profitability.
2.  **Liquidation (The Carcass):** They sell everything for scrap value to pay debt.

> [!NOTE] 🧠 Mental Model: The Falling Knife
> Catching a falling knife is dangerous. You only do it if you know the floor is made of diamond.
> 
> *   **The Floor:** The Liquidation Value (Assets - Liabilities).
> *   **The Upside:** The Option Value of survival.
> 
> If the stock trades *below* the cash on the books (Net Net), the risk is theoretically zero.

---

## 2. The Calculation (The Engine)
We model the probability of bankruptcy explicitly.

### The Formula
$$ \text{Value} = [P_{survive} \times \text{DCF}_{turnaround}] + [P_{bankrupt} \times (\text{Assets} \times \text{Discount} - \text{Debt})] $$

*   **Asset Discount:** In a fire sale, you get 50c on the dollar for inventory, 80c for receivables, 30c for PP&E.
*   **Debt:** The absolute priority. Equity gets nothing until debt is full.

---

## 3. The Wolf's Edge (Burn Rate Sims)
We focus intensely on the **Cash Runway**.

### Python Implementation
```python
import numpy as np

# 1. CASH BURN
months_runway = cash_balance / monthly_burn
# If runway < time_to_profit, Value -> 0

# 2. LIQUIDATION ANALYSIS
assets_book = 1000
# Fire sale discounts
recovery_rate = np.random.triangular(0.3, 0.5, 0.7, SIMULATIONS)
liquidation_val = assets_book * recovery_rate - debt_face_value
# Equity cannot be negative (limited liability)
liquidation_val = np.maximum(liquidation_val, 0)

# 3. WEIGHTED VALUE
value = (dcf_val * p_survive) + (liquidation_val * (1 - p_survive))
```

---

## 4. Interpretation: The Call Option
Distressed equity is essentially a **Call Option on the firm's assets** with a strike price equal to the Debt.

*   **High Volatility is Good:** Since downside is capped at zero, higher variance increases the value of the option (chance of clearing the debt hurdle).
*   **The Signal:** Buy when the company is priced for certain death ($P_{survive} \approx 0$), but you see a lifeline (asset sale, rate cut, new CEO).

