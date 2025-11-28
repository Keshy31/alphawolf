---
tags:
  - valuation
  - sum-of-the-parts
  - sotp
  - conglomerates
aliases:
  - SOTP
  - Sum of the Parts
  - Break-Up Value
  - The Dissection
created: 2025-11-28
---
# Sum-of-the-Parts (The Dissection)

> [!INFO] Metadata
> * **Category:** Valuation > Component-Based
> * **Target Phase:** Conglomerates / Multi-Segment Firms
> * **Key Levers:** Segment Multiples, Corporate Drag
> * **Complexity:** ⭐⭐ (Medium-Low)

---

## 1. Core Concept: The Whole < The Sum of Parts
Corporations are often collections of distinct businesses (e.g., a Tech unit + a Retail unit + a Real Estate portfolio). The market often fails to value the hidden gems inside a messy conglomerate.

**SOTP (Sum-of-the-Parts)** values each segment individually as if it were a standalone company, then adds them up and subtracts the cost of the headquarters.

> [!NOTE] 🧠 Mental Model: The Junk Yard
> Imagine a wrecked Ferrari.
> * As a car (the whole), it's worth $0 because it doesn't run.
> * But the engine, the leather seats, and the tires (the parts) might be worth $50,000 sold separately.
> 
> SOTP helps us find "wrecked Ferraris" where the market sees a mess, but we see valuable components.

---

## 2. The Calculation (The Engine)
We apply the best-fit valuation method to *each* segment, then bridge to equity value.

### The Formula
$$ \text{Value}_{firm} = \sum (\text{Segment}_i \times \text{Multiple}_i) + \text{Cash} - \text{Debt} - \text{Corp Overhead} $$

*   **Segment Value:** Usually EBITDA $\times$ Peer Multiple.
*   **Corporate Drag:** The capitalized cost of the Head Office (Negative Value).
    *   $Value_{HQ} = \frac{\text{Overhead Cost}}{WACC}$
*   **Conglomerate Discount:** The market often applies a 10-20% discount for complexity. We model this as a distribution.

---

## 3. The Wolf's Edge (Regime Modeling)
We use SOTP to model **"Hidden Alpha"**—where one high-growth segment is being masked by a low-growth core.

### Python Implementation
```python
import numpy as np

# 1. SEGMENTS
# Segment A: The Cash Cow (Low multiple)
ebitda_A = np.random.normal(500, 20, SIMULATIONS)
mult_A = np.random.uniform(4.0, 6.0, SIMULATIONS)
val_A = ebitda_A * mult_A

# Segment B: The Star (High multiple)
ebitda_B = np.random.triangular(50, 80, 100, SIMULATIONS)
mult_B = np.random.triangular(15.0, 20.0, 25.0, SIMULATIONS)
val_B = ebitda_B * mult_B

# 2. THE BRIDGE
net_debt = 200
corp_drag = 50 / 0.10 # Capitalized overhead

equity_value = (val_A + val_B) - corp_drag - net_debt
```

---

## 4. Interpretation: The Arb
We look for **Negative Enterprise Value** in specific segments.

*   *Example:* If Market Cap is \$100M, and Segment A is clearly worth \$120M, you are getting Segment B (and its potential) for **free**. This is the ultimate "Margin of Safety."

