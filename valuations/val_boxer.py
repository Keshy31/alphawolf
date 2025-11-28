import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import io

# 🐺 ALPHAWOLF: BOXER RETAIL (Standard DCF)
# Target: JSE: BOX
# Objective: Standard DCF for High-Growth Retailer

# --- 0. SYSTEM SETUP ---
# Force UTF-8 for stdout (Windows support)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# The Wolf's Code: Reproducibility
np.random.seed(42)
SIMULATIONS = 50000

# --- 1. SETTING THE SCENE (CONSTANTS) ---
# All figures in ZAR Millions unless per share
CURRENT_REVENUE = 42300.0  # FY25 Base
NET_CASH = 1100.0          # Net Cash Position
DEBT_ADJ = 500.0           # Debt adjustment (Conservative)
SHARES_OUT = 457.0         # Million Shares
CURRENT_PRICE = 73.42      # Current Market Price
TAX_RATE = 0.27            # SA Corporate Tax

# --- 2. INPUT DISTRIBUTIONS (THE ASSUMPTIONS) ---

# A. Revenue Growth (The Rollout)
# Bear: 8% (Saturation), Base: 13.5% (Target), Bull: 16% (Blue Sky)
growth_dist = np.random.triangular(0.08, 0.135, 0.16, SIMULATIONS)

# B. Operating Margin (The Kill Switch)
# Bear: 3.5% (Cost Pressure), Base: 4.8% (Recovery), Bull: 5.8% (Shoprite Levels)
margin_dist = np.random.triangular(0.035, 0.048, 0.058, SIMULATIONS)

# C. WACC (The Macro Risk)
# Normal Distribution: Mean 13.2%, Std Dev 1.5%
wacc_dist = np.random.normal(0.132, 0.015, SIMULATIONS)

# D. Terminal Growth (The Long Tail)
# Uniform: 4.0% to 6.0% (SA GDP + Inflation proxy)
term_growth_dist = np.random.uniform(0.04, 0.06, SIMULATIONS)

# E. Efficiency (Sales to Capital Ratio)
sales_to_cap_dist = np.random.normal(4.5, 0.5, SIMULATIONS)

# --- 3. THE ENGINE (VECTORIZED DCF) ---
print(f"🐺 Running {SIMULATIONS} simulations on [JSE: BOX]...")

# Initialize Arrays
projection_years = 5
fcf_matrix = np.zeros((SIMULATIONS, projection_years))
revenues = np.tile(CURRENT_REVENUE, SIMULATIONS)

# Loop through 5 years (Projecting paths)
for year in range(projection_years):
    # Grow Revenue
    revenues = revenues * (1 + growth_dist)
    
    # Calculate NOPAT
    ebit = revenues * margin_dist
    nopat = ebit * (1 - TAX_RATE)
    
    # Calculate Reinvestment
    rev_change = revenues - (revenues / (1 + growth_dist))
    reinvestment = rev_change / sales_to_cap_dist
    
    # Free Cash Flow to Firm (FCFF)
    fcff = nopat - reinvestment
    
    # Discount Factors
    discount_factors = (1 + wacc_dist) ** (year + 1)
    
    # Store PV of FCFF
    fcf_matrix[:, year] = fcff / discount_factors

# Sum PV of Explicit Period
pv_explicit = np.sum(fcf_matrix, axis=1)

# --- 4. TERMINAL VALUE ---
# Normalize Year 5 FCFF for steady state
final_nopat = (revenues * margin_dist) * (1 - TAX_RATE)
final_reinvestment = (final_nopat * term_growth_dist) / 0.20 # ROIC assumption for terminal
terminal_fcff = final_nopat - final_reinvestment

terminal_value = terminal_fcff / (wacc_dist - term_growth_dist)
pv_terminal = terminal_value / ((1 + wacc_dist) ** projection_years)

# --- 5. ENTERPRISE TO EQUITY BRIDGE ---
enterprise_value = pv_explicit + pv_terminal
equity_value = enterprise_value + NET_CASH - DEBT_ADJ
fair_value_per_share = equity_value / SHARES_OUT

# --- 6. ANALYZE THE KILL (STATISTICS) ---
mean_val = np.mean(fair_value_per_share)
p10 = np.percentile(fair_value_per_share, 10) # Bear
p50 = np.median(fair_value_per_share)         # Base
p90 = np.percentile(fair_value_per_share, 90) # Bull
prob_profit = np.mean(fair_value_per_share > CURRENT_PRICE)
upside_mean = (mean_val - CURRENT_PRICE) / CURRENT_PRICE

# --- 7. REPORT (STDOUT) ---
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

# --- 8. VISUALIZATION ---
plt.figure(figsize=(12, 6))
sns.histplot(fair_value_per_share, bins=100, kde=True, color='#2c3e50', stat='density', alpha=0.6)

# Annotations
plt.axvline(CURRENT_PRICE, color='red', linestyle='--', linewidth=2, label=f'Price (R{CURRENT_PRICE})')
plt.axvline(p50, color='gold', linestyle='-', linewidth=2, label=f'Median (R{p50:.2f})')
plt.axvline(p10, color='maroon', linestyle=':', linewidth=2, label=f'P10 Bear (R{p10:.2f})')
plt.axvline(p90, color='green', linestyle=':', linewidth=2, label=f'P90 Bull (R{p90:.2f})')

plt.title('Boxer Retail: Valuation Distribution', fontsize=16, fontweight='bold', color='#1a1a1a')
plt.xlabel('Fair Value Per Share (ZAR)', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Save
plt.savefig('val_boxer_dist.png')
