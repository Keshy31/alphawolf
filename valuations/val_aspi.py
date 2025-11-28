import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import io

# 🐺 ALPHA WOLF: MODULE 7 - ASPI (Real Options)
# Target: ASP Isotopes Inc. (ASPI)
# Objective: Sum-of-Parts Monte Carlo (Factory + Nuclear Option)

# --- 0. SYSTEM SETUP ---
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

np.random.seed(42)
SIMULATIONS = 50000

# --- 1. SETTING THE SCENE (PARAMETERS) ---
CURRENT_PRICE = 5.97 # Reference Price USD

# --- 2. PART A: THE FACTORY (Medical & Si-28) ---
# wolf_note: Industrial ramps are binary. We model two regimes.

# Regime 1: "Execution Success" (70% Prob)
rev_success = np.random.triangular(50, 65, 85, SIMULATIONS)

# Regime 2: "Construction Delay" (30% Prob)
rev_delay = np.random.uniform(15, 25, SIMULATIONS)

# Create the Regime Mask (1 = Success, 0 = Delay)
regime_mask = np.random.binomial(1, 0.70, SIMULATIONS)

# Combine Revenues
revenue_2027 = (rev_success * regime_mask) + (rev_delay * (1 - regime_mask))

# Stress-Tested Margins
margin_success = np.random.normal(0.30, 0.05, SIMULATIONS)
margin_delay = np.random.normal(0.10, 0.05, SIMULATIONS)
margins = (margin_success * regime_mask) + (margin_delay * (1 - regime_mask))

# Valuation Multiple (EV/EBITDA)
multiple_success = np.random.uniform(14, 18, SIMULATIONS)
multiple_delay = np.random.uniform(8, 12, SIMULATIONS)
multiples = (multiple_success * regime_mask) + (multiple_delay * (1 - regime_mask))

# Discount Rate
discount_rate = 0.15
years_to_discount = 2

# CALCULATE FACTORY VALUE
ebitda_2027 = revenue_2027 * margins
factory_ev_future = ebitda_2027 * multiples
factory_pv = factory_ev_future / ((1 + discount_rate) ** years_to_discount)

# --- 3. PART B: THE OPTION (Nuclear / QLE) ---
# Scenarios based on S-1 Filing
# 1. Failure (40%): Value = $0 (Scrap)
# 2. Base (40%): $400M-$600M
# 3. Bull (20%): $1.0B-$1.4B

scenarios = ['Cold', 'Base', 'Bull']
probs = [0.40, 0.40, 0.20]
scenario_indices = np.random.choice(len(scenarios), SIMULATIONS, p=probs)

nuclear_vals = np.zeros(SIMULATIONS)
nuclear_vals[scenario_indices == 1] = np.random.triangular(600, 750, 900, np.sum(scenario_indices == 1))
nuclear_vals[scenario_indices == 2] = np.random.normal(1200, 200, np.sum(scenario_indices == 2))

# --- 4. PART C: THE FOUNDATION (Cash & Shares) ---
starting_cash = 378
debt = 66

# Burn varies by regime
burn_success = np.random.uniform(80, 120, SIMULATIONS)
burn_delay = np.random.uniform(50, 80, SIMULATIONS)
burn_rate = (burn_success * regime_mask) + (burn_delay * (1 - regime_mask))

net_cash_final = starting_cash - debt - burn_rate

# Share Count (Dilution Risk)
shares = np.random.triangular(102, 105, 108, SIMULATIONS)

# --- 5. THE FUSION (Price Per Share) ---
total_equity_value = factory_pv + nuclear_vals + net_cash_final
fair_value_per_share = total_equity_value / shares

# --- 6. STATISTICS & ALPHA EXTRACTION ---
mean_val = np.mean(fair_value_per_share)
p10 = np.percentile(fair_value_per_share, 10)
p50 = np.median(fair_value_per_share)
p90 = np.percentile(fair_value_per_share, 90)
prob_profit = np.mean(fair_value_per_share > CURRENT_PRICE)
upside_mean = (mean_val - CURRENT_PRICE) / CURRENT_PRICE

# --- 7. REPORT (STDOUT) ---
print(f"🐺 SIMULATION REPORT [N={SIMULATIONS}]")
print(f"Current Price: $ {CURRENT_PRICE:.2f}")
print("-" * 30)
print(f"Mean Fair Value:   $ {mean_val:.2f}")
print(f"Median Fair Value: $ {p50:.2f}")
print(f"P10 (Bear Case):   $ {p10:.2f}")
print(f"P90 (Bull Case):   $ {p90:.2f}")
print("-" * 30)
print(f"PROBABILITY OF PROFIT: {prob_profit:.1%}")
print(f"Expected Upside (Mean): {upside_mean:.1%}")

# --- 8. VISUALIZATION ---
plt.figure(figsize=(12, 6))
sns.histplot(fair_value_per_share, bins=100, kde=True, color='#2c3e50', stat='density', alpha=0.6)

# Annotations
plt.axvline(CURRENT_PRICE, color='red', linestyle='--', linewidth=2, label=f'Price (${CURRENT_PRICE})')
plt.axvline(p50, color='gold', linestyle='-', linewidth=2, label=f'Median (${p50:.2f})')
plt.axvline(p10, color='maroon', linestyle=':', linewidth=2, label=f'P10 Bear (${p10:.2f})')
plt.axvline(p90, color='green', linestyle=':', linewidth=2, label=f'P90 Bull (${p90:.2f})')

plt.title('ASPI: Real Options Valuation Distribution', fontsize=16, fontweight='bold', color='#1a1a1a')
plt.xlabel('Fair Value Per Share ($)', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.xlim(0, 18)

# Save
plt.savefig('val_aspi_dist.png')
