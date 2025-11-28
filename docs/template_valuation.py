import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import io

# 🐺 ALPHAWOLF v9 CORE ENGINE
# ---------------------------------------------------------
# STANDARDS:
# 1. Reproducibility: Seed 42
# 2. Vectorization: numpy only
# 3. Output: Strict Regex-friendly block
# ---------------------------------------------------------

# --- 0. SYSTEM SETUP ---
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

np.random.seed(42)
SIMULATIONS = 50000

# --- 1. THE HUNT PARAMETERS (USER INPUTS) ---
# [USER: UPDATE THESE BEFORE RUNNING]
TICKER = "XYZ"
CURRENT_PRICE = 123.45
SHARES_OUT = 100.0  # Million

# --- 2. THE NARRATIVE (DISTRIBUTIONS) ---
# "Damodaran's Razor": Select the right distribution for the story.

# REVENUE GROWTH (Triangular: Management Guidance)
# Bear: 5% | Base: 10% | Bull: 15%
growth_dist = np.random.triangular(0.05, 0.10, 0.15, SIMULATIONS)

# OPERATING MARGIN (Normal: Historical Volatility)
# Mean: 20% | StdDev: 2%
margin_dist = np.random.normal(0.20, 0.02, SIMULATIONS)

# EXIT MULTIPLE (Uniform: Valuation Uncertainty)
# Range: 10x to 14x
multiple_dist = np.random.uniform(10, 14, SIMULATIONS)

# WACC (Normal: Interest Rate Risk)
wacc_dist = np.random.normal(0.10, 0.005, SIMULATIONS)

# --- 3. THE ENGINE (VECTORIZED DCF) ---
# Base Year Data
base_revenue = 1000.0  # Million

# Future Year 1 (Simplified for Template - Expand for N-Stage)
# FCF = Rev * Margin * (1 - Tax) - Reinvestment
# For 'Target DCF', we project to Year N and discount back.
YEARS_TO_TARGET = 5

future_revenue = base_revenue * ((1 + growth_dist) ** YEARS_TO_TARGET)
future_ebitda = future_revenue * margin_dist
future_ev = future_ebitda * multiple_dist

# Discounting to Present
discount_factor = (1 + wacc_dist) ** YEARS_TO_TARGET
pv_enterprise_value = future_ev / discount_factor

# Bridge to Equity
net_debt = 200.0  # Million
equity_value = pv_enterprise_value - net_debt
fair_value_dist = equity_value / SHARES_OUT

# --- 4. THE SYNTHESIS (STATISTICS) ---
mean_val = np.mean(fair_value_dist)
p10 = np.percentile(fair_value_dist, 10)  # Bear Case
p50 = np.median(fair_value_dist)          # Base Case
p90 = np.percentile(fair_value_dist, 90)  # Bull Case

# The Wolf's Edge: Probability of Profit
# % of simulations where Fair Value > Current Price
prob_profit = np.mean(fair_value_dist > CURRENT_PRICE)

# Expected Return (Kelly Input)
upside_mean = (mean_val - CURRENT_PRICE) / CURRENT_PRICE

# --- 5. VISUALIZATION (THE MAP) ---
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

# Main Histogram
sns.histplot(fair_value_dist, bins=100, kde=True, 
             color='#2c3e50', stat='density', alpha=0.6, edgecolor=None)

# The Key Levels
plt.axvline(CURRENT_PRICE, color='red', linestyle='--', linewidth=2.5, label=f'Price: {CURRENT_PRICE:,.2f}')
plt.axvline(p50, color='gold', linestyle='-', linewidth=2.5, label=f'Median (P50): {p50:,.2f}')
plt.axvline(p10, color='maroon', linestyle=':', linewidth=2, label=f'Bear (P10): {p10:,.2f}')
plt.axvline(p90, color='green', linestyle=':', linewidth=2, label=f'Bull (P90): {p90:,.2f}')

plt.title(f'🐺 ALPHAWOLF v9: {TICKER} Valuation Distribution', fontsize=14, fontweight='bold', color='#1a1a1a')
plt.xlabel('Intrinsic Value Per Share', fontsize=11)
plt.ylabel('Probability Density', fontsize=11)
plt.legend(loc='upper right')
plt.grid(axis='y', alpha=0.3)

# Save high-res
plt.savefig(f'{TICKER}_wolf_valuation.png', dpi=150)

# --- 6. THE REPORT (REGEX FRIENDLY OUTPUT) ---
# This block is parsed by the Chatbot to generate the Final Alpha Call
print(f"\n🐺 SIMULATION REPORT [N={SIMULATIONS}]")
print(f"Target: {TICKER}")
print(f"Current Price: {CURRENT_PRICE:,.2f}")
print("-" * 30)
print(f"Mean Fair Value:   {mean_val:,.2f}")
print(f"Median Fair Value: {p50:,.2f}")
print(f"P10 (Bear Case):   {p10:,.2f}")
print(f"P90 (Bull Case):   {p90:,.2f}")
print("-" * 30)
print(f"PROBABILITY OF PROFIT: {prob_profit:.1%}")
print(f"Expected Upside (Mean): {upside_mean:.1%}")
print("-" * 30)