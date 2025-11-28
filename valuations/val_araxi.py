import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import io

# 🐺 ALPHA WOLF: ARAXI SOTP
# Target: Araxi (formerly Capital Appreciation / Capprec)
# Strategy: SOTP (Payments Cash Cow + Software Growth Engine)

# --- 0. SYSTEM SETUP ---
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

np.random.seed(42)
SIMULATIONS = 50000

# --- 1. SETTING THE SCENE (PARAMETERS) ---
SHARES_OUT = 1310.0 # Million
CURRENT_PRICE = 170.0 # cents (ZAR)

# Financials (R Millions)
GROSS_CASH = 445.0
GROSS_DEBT = 5.0
CORP_OVERHEAD = 65.0
TAX_RATE = 0.27

# Calculated Metrics
NET_CASH = GROSS_CASH - GROSS_DEBT

# --- 2. THE HUNT: SEGMENT DRIVERS ---
# A. PAYMENTS (The "Mule")
pay_rev_base = np.random.triangular(655,689,758, SIMULATIONS)
pay_growth = np.random.triangular(-0.01, 0.03, 0.08, SIMULATIONS)
pay_rev = pay_rev_base * (1 + pay_growth)
pay_margin = np.random.triangular(0.38, 0.42, 0.44, SIMULATIONS)
pe_pay = np.random.choice([4.0, 5.0, 6.0], SIMULATIONS, p=[0.3, 0.5, 0.2])

# B. SOFTWARE (The "Racehorse")
soft_rev_base = np.random.triangular(530,549,560, SIMULATIONS)
soft_growth = np.random.triangular(0.05, 0.12, 0.20, SIMULATIONS)
soft_rev = soft_rev_base * (1 + soft_growth)
soft_margin = np.random.triangular(0.10, 0.11, 0.13, SIMULATIONS)
pe_soft = np.random.choice([6.0, 8.0, 10.0], SIMULATIONS, p=[0.3, 0.5, 0.2])

# --- 3. THE ENGINE (CALCULATIONS) ---
# Segment Values
pay_ebitda = pay_rev * pay_margin
soft_ebitda = soft_rev * soft_margin

ev_payments = pay_ebitda * pe_pay
ev_software = soft_ebitda * pe_soft

# Corporate Drag
ev_corp_drag = CORP_OVERHEAD / 0.132 # Capitalized at WACC ~13.2% (Standardized)

# Total Enterprise Value
total_ev = ev_payments + ev_software - ev_corp_drag

# Equity Value
equity_value_total = total_ev + GROSS_CASH - GROSS_DEBT

# Per Share Calculation (Cents)
fair_value_per_share = (equity_value_total / SHARES_OUT) * 100

# --- 4. ANALYZE THE KILL (STATISTICS) ---
mean_val = np.mean(fair_value_per_share)
p10 = np.percentile(fair_value_per_share, 10)
p50 = np.median(fair_value_per_share)
p90 = np.percentile(fair_value_per_share, 90)
prob_profit = np.mean(fair_value_per_share > CURRENT_PRICE)
upside_mean = (mean_val - CURRENT_PRICE) / CURRENT_PRICE

# Contribution Analysis
val_pay_share = (np.mean(ev_payments) / SHARES_OUT) * 100
val_soft_share = (np.mean(ev_software) / SHARES_OUT) * 100
val_cash_share = ((GROSS_CASH - GROSS_DEBT) / SHARES_OUT) * 100
val_drag_share = (np.mean(ev_corp_drag) / SHARES_OUT) * 100

# --- 5. REPORTING ---
print(f"🐺 DETAILED SOTP BREAKDOWN (Cents Per Share)")
print(f"----------------------------------------------")
print(f"  (+) Payments Value:   {val_pay_share:5.1f}c")
print(f"  (+) Software Value:   {val_soft_share:5.1f}c")
print(f"  (+) Net Cash:         {val_cash_share:5.1f}c")
print(f"  (-) Corp Structure:  ({val_drag_share:5.1f}c)")
print(f"----------------------------------------------")
print()
print(f"🐺 SIMULATION REPORT [N={SIMULATIONS}]")
print(f"Current Price: R {CURRENT_PRICE/100:,.2f} ({CURRENT_PRICE}c)")
print("-" * 30)
print(f"Mean Fair Value:   R {mean_val/100:,.2f} ({mean_val:.0f}c)")
print(f"Median Fair Value: R {p50/100:,.2f} ({p50:.0f}c)")
print(f"P10 (Bear Case):   R {p10/100:,.2f} ({p10:.0f}c)")
print(f"P90 (Bull Case):   R {p90/100:,.2f} ({p90:.0f}c)")
print("-" * 30)
print(f"PROBABILITY OF PROFIT: {prob_profit:.1%}")
print(f"Expected Upside (Mean): {upside_mean:.1%}")

# --- 6. VISUALIZATION ---
plt.figure(figsize=(12, 6))
sns.histplot(fair_value_per_share, bins=100, kde=True, color='#2c3e50', stat='density', alpha=0.6)

# Annotations
plt.axvline(CURRENT_PRICE, color='red', linestyle='--', linewidth=2, label=f'Price ({CURRENT_PRICE}c)')
plt.axvline(p50, color='gold', linestyle='-', linewidth=2, label=f'Median ({p50:.0f}c)')
plt.axvline(p10, color='maroon', linestyle=':', linewidth=2, label=f'P10 Bear ({p10:.0f}c)')
plt.axvline(p90, color='green', linestyle=':', linewidth=2, label=f'P90 Bull ({p90:.0f}c)')

plt.title('Araxi: SOTP Valuation Distribution', fontsize=16, fontweight='bold', color='#1a1a1a')
plt.xlabel('Fair Value (cents per share)', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Save
plt.savefig('val_araxi_dist.png')
