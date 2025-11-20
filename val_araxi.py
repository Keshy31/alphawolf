import numpy as np
import matplotlib.pyplot as plt

# 1. Setup - 10,000 Realities
n_sims = 100000
np.random.seed(42) # Wolf's Code is reproducible

# 2. Define Distributions (The "Scent")
# Payments Revenue (High Base, Low Growth)
pay_rev_base = 690
pay_growth = np.random.triangular(-0.05, 0.08, 0.15, n_sims)
pay_rev = pay_rev_base * (1 + pay_growth)

# Software Revenue (Lower Base, High Volatility)
soft_rev_base = 550
soft_growth = np.random.triangular(0.0, 0.05, 0.15, n_sims) # AI driven
soft_rev = soft_rev_base * (1 + soft_growth)

# Margins (The Structural Shift)
# Payments Margin: Sensitive to ZAR
pay_margin = np.random.triangular(0.40, 0.43, 0.45, n_sims)
# Software Margin: Driven by AI adoption
soft_margin = np.random.triangular(0.11, 0.13, 0.18, n_sims)

# 3. Calculate EBITDA & Valuation
ebitda = (pay_rev * pay_margin) + (soft_rev * soft_margin) - 60 # -40m Corp Drag
# Add Cash Interest (R400m * 7.5%)
net_income_proxy = (ebitda + 30) * 0.72 # Tax effect approx
shares = 1310 # million

eps_cents = (net_income_proxy / shares) * 100

# Valuation Logic: Market assigns different PE based on growth
pe_ratio = np.random.choice([8.0, 9.0, 10.0, 12.0], n_sims, p=[0.3, 0.4, 0.2, 0.1])

fair_value = eps_cents * pe_ratio # Add 32c Cash per share explicitly

# 4. The Output Stats
p10 = np.percentile(fair_value, 10)
p50 = np.percentile(fair_value, 50)
p90 = np.percentile(fair_value, 90)
prob_profit = np.mean(fair_value > 165) # % runs above current price

print(f"P10 (Bear): {p10:.1f}c")
print(f"P50 (Base): {p50:.1f}c")
print(f"P90 (Bull): {p90:.1f}c")
print(f"Probability of Profit: {prob_profit*100:.1f}%")