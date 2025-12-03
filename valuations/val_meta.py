import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. SETUP
np.random.seed(42)
SIMULATIONS = 10000
CURRENT_PRICE = 648.00 # As of Dec 1, 2025

# --- SEGMENT 1: FAMILY OF APPS (THE CASH COW) ---
# The Engine: Facebook, Instagram, WhatsApp. High margin, steady growth.
# Revenue Base (TTM '25 est): $178B
foa_rev_base = 178.0 
foa_growth = np.random.triangular(0.08, 0.12, 0.16, SIMULATIONS) # Slowing but steady
foa_margin = np.random.triangular(0.48, 0.52, 0.55, SIMULATIONS) # AI efficiency keeps margins elite
foa_wacc = np.random.triangular(0.08, 0.09, 0.10, SIMULATIONS) # Lower risk (Cash Cow)
foa_terminal_g = np.random.normal(0.03, 0.005, SIMULATIONS)

# --- SEGMENT 2: REALITY LABS (THE VENTURE BET) ---
# The Incinerator: Metaverse, VR, AR. Huge losses, potential future platform.
# Revenue Base (TTM '25 est): $2.0B
# Operating Loss (TTM '25 est): -$18.0B (The "Burn")
rl_burn_annual = np.random.triangular(-20.0, -18.0, -15.0, SIMULATIONS) # Annual Loss
rl_burn_years = 5 # Years of burn before potential profitability
rl_success_prob = np.random.uniform(0, 1, SIMULATIONS) # Probability of "The Moonshot" working
rl_terminal_value_success = np.random.triangular(100.0, 300.0, 800.0, SIMULATIONS) # If it works (New Computing Platform)
rl_terminal_value_fail = 0.0 # If it fails, it's worth zero (or shut down)

# RL WACC (Venture Risk)
rl_wacc = np.random.triangular(0.12, 0.15, 0.20, SIMULATIONS) 

# --- SHARED METRICS ---
shares_outstanding = 2.53 # Billion
net_cash = 15.6 # Cash - Debt (Positive)
tax_rate = 0.16

# 2. VECTORIZED CALCULATION

# A. FAMILY OF APPS VALUATION (5-Year DCF)
# ----------------------------------------
# Approximate 5-year annuity for cash flows
foa_avg_rev_5y = foa_rev_base * ((1 + foa_growth) ** 2.5) 
foa_nopat = foa_avg_rev_5y * foa_margin * (1 - tax_rate)
foa_discount_factor_annuity = (1 - (1 + foa_wacc)**-5) / foa_wacc
foa_pv_cashflows = foa_nopat * foa_discount_factor_annuity

# Terminal Value FOA
foa_rev_y5 = foa_rev_base * ((1 + foa_growth) ** 5)
foa_nopat_y5 = foa_rev_y5 * foa_margin * (1 - tax_rate)
foa_tv = foa_nopat_y5 * (1 + foa_terminal_g) / (foa_wacc - foa_terminal_g)
foa_pv_tv = foa_tv / ((1 + foa_wacc) ** 5)

foa_ev = foa_pv_cashflows + foa_pv_tv

# B. REALITY LABS VALUATION (Burn + Option)
# ----------------------------------------
# PV of the Burn (Cost to hold the option)
rl_pv_burn = rl_burn_annual * (1 - (1 + rl_wacc)**-rl_burn_years) / rl_wacc

# PV of the Payoff (Option Value)
# We define "Success" as probability > 0.6 (40% chance of success - optimistic but possible)
is_success = rl_success_prob > 0.6
rl_future_val = np.where(is_success, rl_terminal_value_success, rl_terminal_value_fail)
rl_pv_payoff = rl_future_val / ((1 + rl_wacc) ** rl_burn_years)

rl_ev = rl_pv_burn + rl_pv_payoff

# 3. TOTAL VALUATION FUSION
total_ev = foa_ev + rl_ev
equity_value = total_ev + net_cash
fair_value_per_share = equity_value / shares_outstanding

# 4. ANALYSIS & OUTPUT
p10 = np.percentile(fair_value_per_share, 10)
p50 = np.percentile(fair_value_per_share, 50)
p90 = np.percentile(fair_value_per_share, 90)
prob_profit = np.mean(fair_value_per_share > CURRENT_PRICE)

# Breakdown stats
foa_per_share = np.median(foa_ev) / shares_outstanding
rl_per_share = np.median(rl_ev) / shares_outstanding
cash_per_share = net_cash / shares_outstanding

print(f"🐺 ALPHAWOLF SOTP VALUATION: META PLATFORMS")
print(f"-------------------------------------------")
print(f"FOA Value (The Engine):  ${foa_per_share:.2f} / share")
print(f"RL Value (The Venture):  ${rl_per_share:.2f} / share (Likely Negative)")
print(f"Net Cash:                ${cash_per_share:.2f} / share")
print(f"-------------------------------------------")
print(f"TOTAL P50 FAIR VALUE:    ${p50:.2f}")
print(f"Current Price:           ${CURRENT_PRICE:.2f}")
print(f"-------------------------------------------")
print(f"Bear Case (P10):         ${p10:.2f}")
print(f"Bull Case (P90):         ${p90:.2f}")
print(f"Edge:                    {((p50 - CURRENT_PRICE)/CURRENT_PRICE)*100:.2f}%")

# Visualization
plt.figure(figsize=(12, 6))
sns.histplot(fair_value_per_share, bins=100, kde=True, color='#00A884', element="step")
plt.axvline(CURRENT_PRICE, color='red', linestyle='--', label=f'Spot: ${CURRENT_PRICE}')
plt.axvline(p50, color='gold', linestyle='-', label=f'Fair Value: ${p50:.0f}')
plt.title('Meta Platforms: Sum-of-the-Parts Simulation (FOA + RL)')
plt.xlabel('Fair Value per Share (USD)')
plt.legend()
plt.show()