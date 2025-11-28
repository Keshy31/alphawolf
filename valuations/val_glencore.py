import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import io

# 🐺 ALPHA WOLF: GLENCORE (SOTP/Resource)
# Target: LSE/JSE: GLN
# Objective: Value Marketing (Annuity) vs Industrial (Cyclical)

# --- 0. SYSTEM SETUP ---
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

np.random.seed(42)
SIMULATIONS = 50000

# --- 1. SETTING THE SCENE (CONSTANTS) ---
SHARES_OUT = 12.15  # Billions
CURRENT_PRICE = 79.58 # ZAR
TAX_RATE = 0.28
WACC_MARKETING = 0.12

# --- 2. INPUT DISTRIBUTIONS (THE ASSUMPTIONS) ---

# A. Marketing EBIT ($ Billions) - The Annuity
# Range: Bear $2.2B / Base $2.9B / Bull $3.5B
marketing_ebit = np.random.triangular(2.2, 2.8, 3.2, SIMULATIONS)

# B. Industrial EBITDA ($ Billions) - The Cyclical Engine
industrial_ebitda = np.random.triangular(10.0, 13.0, 17.5, SIMULATIONS)

# C. Valuation Multiple (EV/EBITDA) - Market Sentiment
valuation_multiple = np.random.triangular(3.2, 4.5, 6.0, SIMULATIONS)

# D. USD/ZAR Exchange Rate - The Currency Risk
usd_zar = np.random.normal(17.25, 0.75, SIMULATIONS)

# E. Net Debt ($ Billions)
net_debt = np.random.normal(14.5, 0.5, SIMULATIONS)

# --- 3. THE ENGINE (CALCULATIONS) ---
# Value Marketing Arm (Perpetuity)
marketing_val = (marketing_ebit * (1 - TAX_RATE)) / WACC_MARKETING

# Value Industrial Arm (Multiple)
industrial_val = industrial_ebitda * valuation_multiple

# Enterprise Value
enterprise_value = marketing_val + industrial_val

# Equity Value (USD)
equity_value_usd = enterprise_value - net_debt

# Share Price (USD -> ZAR)
share_price_usd = equity_value_usd / SHARES_OUT
fair_value_zar = share_price_usd * usd_zar

# --- 4. ANALYZE THE KILL (STATISTICS) ---
mean_val = np.mean(fair_value_zar)
p10 = np.percentile(fair_value_zar, 10)
p50 = np.median(fair_value_zar)
p90 = np.percentile(fair_value_zar, 90)
prob_profit = np.mean(fair_value_zar > CURRENT_PRICE)
upside_mean = (mean_val - CURRENT_PRICE) / CURRENT_PRICE

# --- 5. REPORT (STDOUT) ---
print(f"🐺 SIMULATION REPORT [N={SIMULATIONS}]")
print(f"Current Price: R {CURRENT_PRICE:,.2f}")
print("-" * 30)
print(f"Mean Fair Value:   R {mean_val:.2f}")
print(f"Median Fair Value: R {p50:.2f}")
print(f"P10 (Bear Case):   R {p10:.2f}")
print(f"P90 (Bull Case):   R {p90:.2f}")
print("-" * 30)
print(f"PROBABILITY OF PROFIT: {prob_profit:.1%}")
print(f"Expected Upside (Mean): {upside_mean:.1%}")

# --- 6. VISUALIZATION ---
plt.figure(figsize=(12, 6))
sns.histplot(fair_value_zar, bins=100, kde=True, color='#2c3e50', stat='density', alpha=0.6)

# Annotations
plt.axvline(CURRENT_PRICE, color='red', linestyle='--', linewidth=2, label=f'Price (R{CURRENT_PRICE})')
plt.axvline(p50, color='gold', linestyle='-', linewidth=2, label=f'Median (R{p50:.2f})')
plt.axvline(p10, color='maroon', linestyle=':', linewidth=2, label=f'P10 Bear (R{p10:.2f})')
plt.axvline(p90, color='green', linestyle=':', linewidth=2, label=f'P90 Bull (R{p90:.2f})')

plt.title('Glencore: SOTP/NAV Valuation Distribution (ZAR)', fontsize=16, fontweight='bold', color='#1a1a1a')
plt.xlabel('Fair Value Per Share (ZAR)', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Save
plt.savefig('val_glencore_dist.png')
