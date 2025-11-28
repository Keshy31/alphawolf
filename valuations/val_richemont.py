import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import io

# 🐺 ALPHA WOLF: RICHEMONT (Holding Co Discount)
# Target: JSE: CFR
# Objective: SOTP with specific Holding Discount logic

# --- 0. SYSTEM SETUP ---
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

np.random.seed(42)
SIMULATIONS = 50000

# --- 1. SETTING THE SCENE (CONSTANTS) ---
SHARES_OUT = 570.0 # Million
CURRENT_PRICE = 3635.53 # ZAR

# --- 2. INPUT DISTRIBUTIONS (THE ASSUMPTIONS) ---

# A. The Crown Jewel (Cartier/VCA)
# Logic: Base EBITDA €5.32bn with slight operational variance.
jewellery_ebitda = np.random.normal(5320, 150, SIMULATIONS) # € Millions
jewellery_multiple = np.random.triangular(18, 22, 28, SIMULATIONS)

# B. The Distressed Asset (Watchmakers)
# Logic: Beta PERT distribution
def pert(min_val, mode_val, max_val, n):
    alpha = 1 + 4 * (mode_val - min_val) / (max_val - min_val)
    beta = 1 + 4 * (max_val - mode_val) / (max_val - min_val)
    return min_val + np.random.beta(alpha, beta, n) * (max_val - min_val)

watch_ebitda = pert(150, 260, 800, SIMULATIONS) # € Millions
watch_multiple = np.random.uniform(8, 12, SIMULATIONS)

# C. The "Other" & Corp Costs
other_value = 1300 # €1.3bn Fixed
corp_drag_value = np.random.normal(-7500, 500, SIMULATIONS) # Capitalized Costs
net_cash = 6500 # €6.5bn

# D. The Tax (Holding Discount)
holding_discount = np.random.uniform(0.05, 0.15, SIMULATIONS)

# E. The Currency (The Rand Hedge)
eur_zar = np.random.normal(20.50, 1.5, SIMULATIONS)

# --- 3. THE ENGINE (CALCULATIONS) ---
# Gross Enterprise Value
ev_gross = (jewellery_ebitda * jewellery_multiple) + (watch_ebitda * watch_multiple) + other_value + corp_drag_value

# Equity Value (EUR)
equity_value_eur = (ev_gross + net_cash) * (1 - holding_discount)

# Per Share Value (EUR -> ZAR)
fair_value_eur_per_share = equity_value_eur / SHARES_OUT
fair_value_zar = fair_value_eur_per_share * eur_zar

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
print(f"Mean Fair Value:   R {mean_val:,.2f}")
print(f"Median Fair Value: R {p50:,.2f}")
print(f"P10 (Bear Case):   R {p10:,.2f}")
print(f"P90 (Bull Case):   R {p90:,.2f}")
print("-" * 30)
print(f"PROBABILITY OF PROFIT: {prob_profit:.1%}")
print(f"Expected Upside (Mean): {upside_mean:.1%}")

# --- 6. VISUALIZATION ---
plt.figure(figsize=(12, 6))
sns.histplot(fair_value_zar, bins=100, kde=True, color='#2c3e50', stat='density', alpha=0.6)

# Annotations
plt.axvline(CURRENT_PRICE, color='red', linestyle='--', linewidth=2, label=f'Price (R{CURRENT_PRICE:,.0f})')
plt.axvline(p50, color='gold', linestyle='-', linewidth=2, label=f'Median (R{p50:,.0f})')
plt.axvline(p10, color='maroon', linestyle=':', linewidth=2, label=f'P10 Bear (R{p10:,.0f})')
plt.axvline(p90, color='green', linestyle=':', linewidth=2, label=f'P90 Bull (R{p90:,.0f})')

plt.title('Richemont: SOTP Valuation Distribution (ZAR)', fontsize=16, fontweight='bold', color='#1a1a1a')
plt.xlabel('Fair Value Per Share (ZAR)', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Save
plt.savefig('val_richemont_dist.png')
