---
tags:
  - valuation
  - real-options
  - biotech
  - startups
aliases:
  - Real Options
  - The Quantum Bet
  - Binary Valuation
created: 2025-11-28
---
# Real Options (The Quantum Bet)

> [!INFO] Metadata
> * **Category:** Valuation > Probabilistic
> * **Target Phase:** Startups / Biotech / Exploration Mining (Phase 1)
> * **Key Levers:** Probability of Success (PoS), Payoff Size
> * **Complexity:** ⭐⭐⭐⭐ (High)

---

## 1. Core Concept: Binary Outcomes
Standard DCFs fail for early-stage assets. Averaging a "0" outcome (failure) and a "100" outcome (success) gives "50", which exists nowhere in reality.

**Real Options** valuation treats the company like a financial option: You pay a premium (burn rate/investment) for the *right* (but not the obligation) to capture a future payoff if the technology works.

> [!NOTE] 🧠 Mental Model: The Lottery Ticket
> You don't value a lottery ticket by averaging the jackpot with zero.
> You value it by:
> $$ \text{Price} = (\text{Jackpot Size} \times \text{Odds of Winning}) - \text{Cost of Ticket} $$
> 
> If a biotech stock is "all or nothing," we model it as two separate universes, not one average universe.

---

## 2. The Calculation (The Engine)
We model discrete branches of the future (Success vs. Failure) using a Decision Tree or Binomial Model.

### The Formula
$$ \text{Value} = (P_{success} \times \text{PV}_{payoff}) + (P_{fail} \times \text{Liquidation Value}) - \text{Cost} $$

*   **$P_{success}$:** The probability of the catalyst occurring (e.g., FDA approval, drilling success).
*   **Payoff:** The value of the business *if* it succeeds (usually a Target DCF).
*   **Cost:** The cash burn required to get to the decision point.

---

## 3. The Wolf's Edge (Binomial Simulations)
We use `np.random.binomial` or `np.random.choice` to create "Regime Masks" in our Monte Carlo simulations.

### Python Implementation
```python
import numpy as np

# 1. THE CATALYST (The Coin Flip)
# 30% chance of success
success_mask = np.random.binomial(1, 0.30, SIMULATIONS)

# 2. THE PAYOFFS
# Success: $1B - $2B Outcome
val_success = np.random.uniform(1000, 2000, SIMULATIONS)

# Failure: $0 - $50M Scrap Value
val_fail = np.random.uniform(0, 50, SIMULATIONS)

# 3. THE COLLAPSE
# Combine the two universes
final_value = (val_success * success_mask) + (val_fail * (1 - success_mask))
```

---

## 4. Interpretation: Asymmetry
We are hunting for **Asymmetric Bets**.

*   **Convexity:** Limited Downside (can only lose 1x), Unlimited Upside (can make 10x, 20x).
*   **The Signal:** We buy when the market prices the asset as if failure is *certain* (Option Price $\approx$ 0), but we assess $P_{success} > 0$.

