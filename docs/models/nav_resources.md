---
tags:
  - valuation
  - nav
  - resources
  - mining
  - banks
aliases:
  - Net Asset Value
  - NAV
  - The Resource
created: 2025-11-28
---
# NAV & Resources (The Resource)

> [!INFO] Metadata
> * **Category:** Valuation > Asset-Based
> * **Target Phase:** Mining / Oil & Gas / Real Estate / Banks
> * **Key Levers:** Commodity Prices, Reserves, Book Value
> * **Complexity:** ⭐⭐⭐ (Medium)

---

## 1. Core Concept: Finite Life
Miners and Oil companies are not "Going Concerns" in the infinite sense. They dig a hole, sell the dirt, and eventually, the hole is empty.

We do not project terminal value growth. We project the **depletion of the asset**.

> [!NOTE] 🧠 Mental Model: The Locker of Gold
> A gold mine is just a locker with a fixed amount of gold in it.
> *   **Value** = (Amount of Gold $\times$ Price of Gold) - Cost to open the locker.
> 
> Once the locker is empty, the business is worth zero.

---

## 2. The Calculation (The Engine)
We use a **Net Asset Value (NAV)** model or a **Dividend Discount Model (DDM)** for banks (where money is the inventory).

### The Formula (Miners)
$$ \text{NAV} = \sum_{t=1}^{Life} \frac{\text{Production}_t \times (\text{Price}_t - \text{Cost}_t)}{(1+r)^t} + \text{Cash} - \text{Debt} - \text{Rehab Costs} $$

*   **Life of Mine (LOM):** Reserves / Annual Production.
*   **Commodity Price:** The single biggest driver. Modeled with high volatility.

### The Formula (Banks)
$$ \text{Value} = \frac{\text{Book Value} \times (\text{ROE} - g)}{r - g} $$
*   **Price/Book Ratio:** The standard metric.

---

## 3. The Wolf's Edge (Commodity Volatility)
We never assume a flat commodity price. We use global volatility data.

### Python Implementation
```python
import numpy as np

# 1. COMMODITY PRICE PATHS
# Random Walk or Mean Reversion for Gold/Oil
price_commodity = np.random.normal(2000, 200, SIMULATIONS) # e.g., Gold

# 2. MARGIN EXPANSION
# Costs are often fixed, so higher price = exploded margin
revenue = production * price_commodity
costs = fixed_costs + (variable_cost * production)
fcf = revenue - costs - tax

# 3. NAV
nav = np.sum(fcf_years) + cash - debt
```

---

## 4. Interpretation: The Macro Bet
When you value a resource company, you are implicitly betting on the underlying commodity.

*   **The Signal:** Buy when the stock price implies a commodity price *lower* than the spot price.
    *   *Example:* Stock is trading at \$10. Our model says it's worth \$10 only if Gold drops to \$1,500. Since Gold is \$2,000, the stock is mispriced.

