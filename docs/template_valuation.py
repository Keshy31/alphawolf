import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import io

# 🐺 ALPHA WOLF: VALUATION TEMPLATE
# Target: [TICKER]
# Objective: [Objective, e.g., "SOTP Monte Carlo"]

# --- 0. SYSTEM SETUP ---
# Force UTF-8 for stdout (Windows support)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Set Seed for "The Wolf's Code" (Reproducibility)
np.random.seed(42)
SIMULATIONS = 50000

# --- 1. SETTING THE SCENE (CONSTANTS) ---
# Hard data points (Shares, Debt, Cash, Tax Rate)
SHARES_OUT = 100.0 # Million
CURRENT_PRICE = 50.00 # Currency
TAX_RATE = 0.25

# --- 2. INPUT DISTRIBUTIONS (THE ASSUMPTIONS) ---
# Use vectorization. No loops.

# Example: Revenue Growth (Triangular View)
# Bear: 5%, Base: 10%, Bull: 15%
growth_rate = np.random.triangular(0.05, 0.10, 0.15, SIMULATIONS)

# Example: Margin (Normal Volatility)
# Mean: 20%, StdDev: 2%
margin = np.random.normal(0.20, 0.02, SIMULATIONS)

# Example: Multiple (Uniform Uncertainty)
multiple = np.random.uniform(10, 14, SIMULATIONS)

# --- 3. THE ENGINE (CALCULATIONS) ---
# Example: Simple Future Value -> Present Value
base_revenue = 1000 # Million
future_revenue = base_revenue * (1 + growth_rate)
future_ebitda = future_revenue * margin
future_ev = future_ebitda * multiple

# Discounting
WACC = 0.10
years = 1
pv_ev = future_ev / ((1 + WACC) ** years)

# Bridge to Equity
net_debt = 200 # Million
equity_value = pv_ev - net_debt

# Per Share
fair_value_per_share = equity_value / SHARES_OUT

# --- 4. ANALYZE THE KILL (STATISTICS) ---
mean_val = np.mean(fair_value_per_share)
p10 = np.percentile(fair_value_per_share, 10) # Bear
p50 = np.median(fair_value_per_share)         # Base
p90 = np.percentile(fair_value_per_share, 90) # Bull
prob_profit = np.mean(fair_value_per_share > CURRENT_PRICE)
upside_mean = (mean_val - CURRENT_PRICE) / CURRENT_PRICE

# --- 5. REPORT (STDOUT) ---
print(f"🐺 SIMULATION REPORT [N={SIMULATIONS}]")
print(f"Current Price: {CURRENT_PRICE:,.2f}")
print("-" * 30)
print(f"Mean Fair Value:   {mean_val:,.2f}")
print(f"Median Fair Value: {p50:,.2f}")
print(f"P10 (Bear Case):   {p10:,.2f}")
print(f"P90 (Bull Case):   {p90:,.2f}")
print("-" * 30)
print(f"PROBABILITY OF PROFIT: {prob_profit:.1%}")
print(f"Expected Upside (Mean): {upside_mean:.1%}")

# --- 6. VISUALIZATION (THE CHART) ---
plt.figure(figsize=(12, 6))
sns.histplot(fair_value_per_share, bins=100, kde=True, color='#2c3e50', stat='density', alpha=0.6)

# Annotations
plt.axvline(CURRENT_PRICE, color='red', linestyle='--', linewidth=2, label=f'Price ({CURRENT_PRICE})')
plt.axvline(p50, color='gold', linestyle='-', linewidth=2, label=f'Median ({p50:.2f})')
plt.axvline(p10, color='maroon', linestyle=':', linewidth=2, label=f'P10 Bear ({p10:.2f})')
plt.axvline(p90, color='green', linestyle=':', linewidth=2, label=f'P90 Bull ({p90:.2f})')

plt.title('Valuation Distribution', fontsize=16, fontweight='bold', color='#1a1a1a')
plt.xlabel('Fair Value Per Share', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Save
plt.savefig('valuation_dist.png')

