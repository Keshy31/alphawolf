import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import io

# 🐺 ALPHA WOLF: PICK N PAY (Distressed / Sum-of-Parts)
# Target: JSE: PIK
# Objective: Value the "Boxer Unbundling" + "Core Turnaround" Option

# --- 0. SYSTEM SETUP ---
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

np.random.seed(42)
SIMULATIONS = 50000

# --- 1. SETTING THE SCENE (CONSTANTS) ---
SHARES_OUT = 745.0 # Million (Post Rights Offer estimate)
CURRENT_PRICE = 25.78 # ZAR

# --- 2. INPUT DISTRIBUTIONS (THE ASSUMPTIONS) ---

# A. Asset 1: The Anchor (Boxer Stake)
# Logic: PIK owns a majority stake. We value the stake based on Boxer's IPO valuation range.
boxer_base_value_per_share = 29.20 # Implied value per PIK share
boxer_price_shock = np.random.normal(1.0, 0.25, SIMULATIONS) # 25% Volatility
boxer_value_sim = boxer_base_value_per_share * boxer_price_shock

# B. Asset 2: The Cash (Liquidity)
# Post Rights Offer Cash Injection
net_cash_per_share = 5.45 # Fixed

# C. Asset 3: The Gamble (Core Supermarkets Turnaround)
# Logic: Revenue R60bn. Can they get margins back to 1.5%?
# Terminal Margin: Triangular (Min 0%, Mode 1.5%, Max 3.5%)
core_margin_sim = np.random.triangular(0.00, 0.015, 0.035, SIMULATIONS)

# Distressed Multiple (EV/EBITDA)
# 5.0x (Fire Sale) to 8.0x (Recovery)
multiple = np.random.choice([5.0, 6.5, 8.0], SIMULATIONS, p=[0.3, 0.5, 0.2])

# Core Value Calculation
core_revenue = 60000.0 # R60bn
core_ev = core_revenue * core_margin_sim * multiple
core_value_per_share = core_ev / SHARES_OUT

# D. The Friction (HoldCo Discount)
# Discount applied to the TOTAL sum (Triangular: 5% to 25%, Mode 15%)
holdco_discount = np.random.triangular(0.05, 0.15, 0.25, SIMULATIONS)

# --- 3. THE ENGINE (CALCULATIONS) ---
gross_value = boxer_value_sim + net_cash_per_share + core_value_per_share
final_value = gross_value * (1 - holdco_discount)

# --- 4. ANALYZE THE KILL (STATISTICS) ---
mean_val = np.mean(final_value)
p10 = np.percentile(final_value, 10)
p50 = np.median(final_value)
p90 = np.percentile(final_value, 90)
prob_profit = np.mean(final_value > CURRENT_PRICE)
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
sns.histplot(final_value, bins=100, kde=True, color='#2c3e50', stat='density', alpha=0.6)

# Annotations
plt.axvline(CURRENT_PRICE, color='red', linestyle='--', linewidth=2, label=f'Price (R{CURRENT_PRICE})')
plt.axvline(p50, color='gold', linestyle='-', linewidth=2, label=f'Median (R{p50:.2f})')
plt.axvline(p10, color='maroon', linestyle=':', linewidth=2, label=f'P10 Bear (R{p10:.2f})')
plt.axvline(p90, color='green', linestyle=':', linewidth=2, label=f'P90 Bull (R{p90:.2f})')

plt.title('Pick n Pay: Distressed SOTP Valuation Distribution', fontsize=16, fontweight='bold', color='#1a1a1a')
plt.xlabel('Fair Value Per Share (ZAR)', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Save
plt.savefig('val_picknpay_dist.png')
