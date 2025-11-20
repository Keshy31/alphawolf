import numpy as np
import matplotlib.pyplot as plt
import sys
import io

# Force UTF-8 for stdout to handle emojis on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. SETUP & ASSUMPTIONS
# ---------------------------------------------------------
SIMULATIONS = 500000
np.random.seed(42) # for reproducibility

# CURRENT MARKET DATA (The "Hard" Numbers)
SHARES_OUTSTANDING = 12.15  # Billions
NET_DEBT_MEAN = 14.5       # $ Billions (H1 2025)
NET_DEBT_STD = 0.5         # Uncertainty buffer
TAX_RATE = 0.28            # Effective tax rate
WACC_MARKETING = 0.12      # Discount rate for trading arm

# 2. RANDOMIZED INPUTS (The "Red Team" Ranges)
# ---------------------------------------------------------

# A. Marketing EBIT ($ Billions) - The Annuity
# Range: Bear $2.2B / Base $2.9B / Bull $3.5B
marketing_ebit = np.random.triangular(2.2, 2.8, 3.2, SIMULATIONS)

# B. Industrial EBITDA ($ Billions) - The Cyclical Engine
industrial_ebitda = np.random.triangular(10.0, 13.0, 17.5, SIMULATIONS)

# C. Valuation Multiple (EV/EBITDA) - Market Sentiment
# Range: Bear 4.5x (Hated) / Base 5.5x (Fair) / Bull 6.5x (Loved)
valuation_multiple = np.random.triangular(3.2, 4.5, 6.0, SIMULATIONS)

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

# 5. VISUALIZE DISTRIBUTION
# ---------------------------------------------------------
plt.figure(figsize=(12, 6))
plt.hist(share_price_zar, bins=50, color='skyblue', alpha=0.7, edgecolor='black', density=True)

# Add vertical lines
plt.axvline(current_price, color='red', linestyle='--', linewidth=2, label=f'Current Price: R{current_price:.2f}')
plt.axvline(p10, color='orange', linestyle=':', linewidth=2, label=f'P10 (Bear): R{p10:.2f}')
plt.axvline(p50, color='green', linestyle='-', linewidth=2, label=f'P50 (Base): R{p50:.2f}')
plt.axvline(p90, color='purple', linestyle=':', linewidth=2, label=f'P90 (Bull): R{p90:.2f}')

plt.title(f'Monte Carlo Simulation: Glencore Share Price Distribution (ZAR)\n({SIMULATIONS} Iterations)', fontsize=14)
plt.xlabel('Share Price (ZAR)', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

# Add text box with summary stats
textstr = '\n'.join((
    f'Prob Profit: {prob_profit:.1f}%',
    f'Mean: R{np.mean(share_price_zar):.2f}',
    f'Std Dev: R{np.std(share_price_zar):.2f}'
))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

plt.show()