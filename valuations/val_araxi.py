import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import io

# 🐺 ALPHA WOLF: MODULE 7 - ARAXI SOTP
# Target: Araxi (formerly Capital Appreciation / Capprec)
# Strategy: SOTP (Payments Cash Cow + Software Growth Engine)

# --- 0. SYSTEM SETUP ---
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

np.random.seed(42) # The Wolf's Code: Reproducibility
SIMULATIONS = 50000

# --- 1. SETTING THE SCENE (PARAMETERS) ---
SHARES_OUT = 1310.0 # Million
CURRENT_PRICE = 170.0 # cents (ZAR)

# Financials (R Millions)
GROSS_CASH = 445.0 # Cash on hand
GROSS_DEBT = 5.0   # Assumed zero or negligible for this model
CORP_OVERHEAD = 65.0 # Head office drag
TAX_RATE = 0.27 # SA Corp Tax Rate

# Calculated Metrics
NET_CASH = GROSS_CASH - GROSS_DEBT
CASH_PER_SHARE = (NET_CASH / SHARES_OUT) * 100 # Converted to cents

# --- 2. THE HUNT: SEGMENT DRIVERS ---
# A. PAYMENTS (The "Mule" - Cash Cow, Low Growth)
# Hardware/Terminal Sales & Transaction Fees
pay_rev_base = np.random.triangular(655,689,758, SIMULATIONS) # Adjusted slightly up for inflation
pay_growth = np.random.triangular(-0.01, 0.03, 0.08, SIMULATIONS) # Risk of hardware slowdown
pay_rev = pay_rev_base * (1 + pay_growth)

# Payments Margin: Hardware margins are tighter than SaaS
pay_margin = np.random.triangular(0.38, 0.42, 0.44, SIMULATIONS)

# Valuation Multiple for Payments (Commodity Tech)
pe_pay = np.random.choice([4.0, 5.0, 6.0], SIMULATIONS, p=[0.3, 0.5, 0.2])

# B. SOFTWARE (The "Racehorse" - Synthesis/AI - High Growth)
# Cloud, Security, AI services
soft_rev_base = np.random.triangular(530,549,560, SIMULATIONS)
soft_growth = np.random.triangular(0.05, 0.12, 0.20, SIMULATIONS) # AI tailwind
soft_rev = soft_rev_base * (1 + soft_growth)
# Software Margin: High value services
soft_margin = np.random.triangular(0.10, 0.11, 0.13, SIMULATIONS)
# Valuation Multiple for Software (High Growth/AI Premium)
pe_soft = np.random.choice([6.0, 8.0, 10.0], SIMULATIONS, p=[0.3, 0.5, 0.2])

# --- 3. THE ENGINE (CALCULATIONS) ---
# Step 0: Calculate EBITDA
pay_ebitda = pay_rev * pay_margin
soft_ebitda = soft_rev * soft_margin

# Step 1: Gross Segment Value (Enterprise Value of Ops)
ev_payments = pay_ebitda * pe_pay
ev_software = soft_ebitda * pe_soft

# Step 2: Capitalize Corporate Overhead
# We treat Head Office as a perpetuity of cost: Value = Cost / WACC
# This is "Negative Value"
ev_corp_drag = CORP_OVERHEAD

# Step 3: Total Enterprise Value (Firm Value)
total_ev = ev_payments + ev_software - ev_corp_drag

# Step 4: Bridge to Equity Value
# Equity = EV + Cash - Debt - Minorities
equity_value_total = total_ev + GROSS_CASH - GROSS_DEBT

# Step 5: Per Share Calculation
fair_value_per_share = (equity_value_total / SHARES_OUT) * 100 # Cents

# --- 4. ANALYZE THE KILL (STATISTICS) ---
mean_val = np.mean(fair_value_per_share)
p10 = np.percentile(fair_value_per_share, 10) # Bear
p50 = np.median(fair_value_per_share)         # Base
p90 = np.percentile(fair_value_per_share, 90) # Bull
prob_profit = np.mean(fair_value_per_share > CURRENT_PRICE)
upside_mean = (mean_val - CURRENT_PRICE) / CURRENT_PRICE

# Contribution Analysis (Where is the value?)
# We take the means for the report
val_pay_share = (np.mean(ev_payments) / SHARES_OUT) * 100
val_soft_share = (np.mean(ev_software) / SHARES_OUT) * 100
val_cash_share = ((GROSS_CASH - GROSS_DEBT) / SHARES_OUT) * 100
val_drag_share = (np.mean(ev_corp_drag) / SHARES_OUT) * 100

# --- 5. REPORTING ---
print(f"🐺 ALPHA WOLF: ARAXI EV/EBITDA SOTP VALUATION")
print(f"==============================================")
print(f"Current Price: {CURRENT_PRICE}c")
print(f"----------------------------------------------")
print(f"SOTP BREAKDOWN (Per Share Contribution):")
print(f"  (+) Payments Value:   {val_pay_share:5.1f}c  (Mean EV/EBITDA: {np.mean(pe_pay):.1f}x)")
print(f"  (+) Software Value:   {val_soft_share:5.1f}c  (Mean EV/EBITDA: {np.mean(pe_soft):.1f}x)")
print(f"  (+) Net Cash:         {val_cash_share:5.1f}c")
print(f"  (-) Corp Structure:  ({val_drag_share:5.1f}c) (Capitalized Overhead)")
print(f"  (=) Total:            {val_pay_share + val_soft_share + val_cash_share - val_drag_share:5.1f}c   (Enterprise Value)")
print(f"----------------------------------------------")
print(f"FAIR VALUE DISTRIBUTION:")
print(f"  P10 (Bear):     {p10:.2f}c")
print(f"  P50 (Base):     {np.median(fair_value_per_share):.2f}c")
print(f"  Mean:           {mean_val:.2f}c")
print(f"  P90 (Bull):     {p90:.2f}c")
print(f"----------------------------------------------")
print(f"SIGNAL STRENGTH:")
print(f"  Prob(Upside):   {prob_profit:.1%}")
print(f"  Exp. Return:    {(mean_val - CURRENT_PRICE)/CURRENT_PRICE:.1%}")
print(f"==============================================")

# --- 6. VISUALIZATION ---
plt.figure(figsize=(12, 6))

# Histogram
sns.histplot(fair_value_per_share, bins=100, kde=True, color='#34495e', line_kws={'linewidth': 2})

# Key Lines
plt.axvline(CURRENT_PRICE, color='red', linestyle='--', linewidth=2, label=f'Market Price ({CURRENT_PRICE}c)')
plt.axvline(mean_val, color='#27ae60', linestyle='-', linewidth=2, label=f'Fair Value ({mean_val:.0f}c)')

# Shading the "Margin of Safety"
plt.axvspan(p10, CURRENT_PRICE, color='red', alpha=0.1, label='Bear Risk Zone')
plt.axvspan(CURRENT_PRICE, p90, color='green', alpha=0.1, label='Alpha Zone')

plt.title('Araxi: Sum-of-the-Parts (EV/EBITDA) Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Fair Value (cents per share)')
plt.ylabel('Probability Density')
plt.legend()
plt.tight_layout()

# Save
plt.savefig('val_araxi_dist.png')
