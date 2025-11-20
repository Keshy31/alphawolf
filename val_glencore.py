import numpy as np
import matplotlib.pyplot as plt

# 1. SETUP & ASSUMPTIONS
# ---------------------------------------------------------
SIMULATIONS = 50000
np.random.seed(42) # for reproducibility

# CURRENT MARKET DATA (The "Hard" Numbers)
SHARES_OUTSTANDING = 12.2  # Billions
NET_DEBT_MEAN = 14.5       # $ Billions (H1 2025)
NET_DEBT_STD = 0.5         # Uncertainty buffer
TAX_RATE = 0.25            # Effective tax rate
WACC_MARKETING = 0.10      # Discount rate for trading arm

# 2. RANDOMIZED INPUTS (The "Red Team" Ranges)
# ---------------------------------------------------------

# A. Marketing EBIT ($ Billions) - The Annuity
# Range: Bear $2.2B / Base $2.9B / Bull $3.5B
marketing_ebit = np.random.triangular(2.2, 2.9, 3.5, SIMULATIONS)

# B. Industrial EBITDA ($ Billions) - The Cyclical Engine
# Range: Bear $12.0B (Execution Fail) / Base $15.0B / Bull $19.0B (Supercycle)
industrial_ebitda = np.random.triangular(12.0, 15.0, 19.0, SIMULATIONS)

# C. Valuation Multiple (EV/EBITDA) - Market Sentiment
# Range: Bear 4.5x (Hated) / Base 5.5x (Fair) / Bull 6.5x (Loved)
valuation_multiple = np.random.triangular(4.5, 5.5, 6.5, SIMULATIONS)

# D. USD/ZAR Exchange Rate - The Currency Risk
# Normal Distribution: Mean 17.25, Volatility implied by recent moves
usd_zar = np.random.normal(17.25, 0.75, SIMULATIONS)

# E. Net Debt Uncertainty
net_debt = np.random.normal(NET_DEBT_MEAN, NET_DEBT_STD, SIMULATIONS)

# 3. THE VALUATION ENGINE (Run 50k times)
# ---------------------------------------------------------

# Value Marketing Arm (Perpetuity: EBIT * (1-t) / WACC)
marketing_val = (marketing_ebit * (1 - TAX_RATE)) / WACC_MARKETING

# Value Industrial Arm (EBITDA * Multiple)
industrial_val = industrial_ebitda * valuation_multiple

# Sum of Parts (SOTP) Enterprise Value
enterprise_value = marketing_val + industrial_val

# Equity Value (EV - Debt)
equity_value_usd = enterprise_value - net_debt

# Share Price in USD
share_price_usd = equity_value_usd / SHARES_OUTSTANDING

# Share Price in ZAR
share_price_zar = share_price_usd * usd_zar

# 4. ANALYZE RESULTS
# ---------------------------------------------------------
current_price = 79.58
p10 = np.percentile(share_price_zar, 10)  # Bear Case
p50 = np.percentile(share_price_zar, 50)  # Base Case
p90 = np.percentile(share_price_zar, 90)  # Bull Case
prob_profit = np.mean(share_price_zar > current_price) * 100

print(f"--- 🎲 MONTE CARLO RESULTS ({SIMULATIONS} Runs) ---")
print(f"Current Market Price: R{current_price:.2f}")
print(f"P10 (Bear Case):      R{p10:.2f}  (Downside Floor)")
print(f"P50 (Base Case):      R{p50:.2f}  (Expected Value)")
print(f"P90 (Bull Case):      R{p90:.2f}  (Upside Potential)")
print(f"Probability of Profit: {prob_profit:.1f}%")