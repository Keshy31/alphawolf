import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 🐺 ALPHA WOLF: MODULE 7 - THOUSAND PATHS SIMULATION
# Target: ASPI (ASP Isotopes Inc.)
# Objective: Quantify the "Binary" nature of the trade using Monte Carlo.

np.random.seed(42) # The Wolf's Code: Reproducibility
SIMULATIONS = 200000

# --- 1. INPUT DISTRIBUTIONS ---

# A. Medical/Tech Segment (The Factory) - Triangular Distribution
# Logic: Floor is scrap/IP ($250M), Base is current DCF ($415M), Bull is fast Si-28 adoption ($600M)
med_tech_val = np.random.triangular(250, 415, 600, SIMULATIONS)

# B. Nuclear/QLE Segment (The Option) - Discrete Distribution
# Logic: 30% Fail ($0), 40% Delay/Base ($400M), 30% Success ($1.5B)
# We add some noise to the non-zero outcomes to reflect execution variance (+/- 10%)
scenarios = [0, 400, 1500]
probs = [0.30, 0.40, 0.30]
nuclear_base = np.random.choice(scenarios, SIMULATIONS, p=probs)
# Add execution noise (normal dist) only where value > 0
noise = np.random.normal(1.0, 0.2, SIMULATIONS) # Mean 1.0, Std 10%
nuclear_val = nuclear_base * noise
# Ensure no negative values from noise
nuclear_val = np.maximum(nuclear_val, 0)

# C. Net Cash (The Buffer) - Triangular
# Logic: Burn could be worse ($80M) or better ($120M), Base ($105M)
net_cash_val = np.random.triangular(80, 105, 120, SIMULATIONS)

# D. Share Count (The Dilution) - Triangular
# Logic: Min (135M), Likely (145M - slight drift), Max (170M - heavy raise)
share_count = np.random.triangular(135, 145, 170, SIMULATIONS)

# --- 2. CALCULATE IMPLIED SHARE PRICE ---

# Total Equity Value
total_equity_val = med_tech_val + nuclear_val + net_cash_val

# Price Per Share
price_distribution = total_equity_val / share_count

# --- 3. STATISTICS & ANALYTICS ---

current_price = 7.60
mean_price = np.mean(price_distribution)
median_price = np.median(price_distribution)
p10 = np.percentile(price_distribution, 10) # Downside risk
p90 = np.percentile(price_distribution, 90) # Upside potential
prob_win = np.mean(price_distribution > current_price) # % Chance we make money

# --- 4. VISUALIZATION ---

plt.figure(figsize=(12, 6))
plt.hist(price_distribution, bins=100, color='#1f77b4', alpha=0.7, edgecolor='black', density=True)
plt.axvline(current_price, color='red', linestyle='dashed', linewidth=2, label=f'Spot Price (${current_price:.2f})')
plt.axvline(median_price, color='gold', linestyle='dashed', linewidth=2, label=f'Median Value (${median_price:.2f})')

plt.title(f'ASPI "Thousand Paths" Valuation Distribution (N={SIMULATIONS})', fontsize=14, fontweight='bold')
plt.xlabel('Implied Share Price ($)', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.xlim(0, 20) # Limit x-axis to focus on relevant range (ignore extreme tails for view)

# Annotate the peaks (The Trimodal Nature)
plt.text(2.5, 0.1, 'The "Rug Pull"\n(Tech Fail)', color='darkred', ha='center', fontsize=10, fontweight='bold')
plt.text(6.5, 0.15, 'The "Grind"\n(Delays)', color='orange', ha='center', fontsize=10, fontweight='bold')
plt.text(13.0, 0.05, 'The "Moonshot"\n(Success)', color='green', ha='center', fontsize=10, fontweight='bold')

filename = 'aspi_monte_carlo.png'
plt.savefig(filename)

print(f"Mean Price: ${mean_price:.2f}")
print(f"Median Price: ${median_price:.2f}")
print(f"P10 (Downside): ${p10:.2f}")
print(f"P90 (Upside): ${p90:.2f}")
print(f"Win Probability (Price > ${current_price}): {prob_win*100:.1f}%")