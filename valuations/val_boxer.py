import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 🐺 ALPHAWOLF CONFIGURATION
# -------------------------
SIMULATIONS = 50000        # The Scale (50k paths for smooth tails)
SEED = 2025                # Reproducibility (The Wolf's memory)
np.random.seed(SEED)

# 1️⃣ LIVE DATA SNAPSHOT (Boxer Retail Ltd - JSE: BOX)
# All figures in ZAR Millions unless per share
current_revenue = 42300.0  # FY25 Base
net_cash = 1100.0          # Net Cash Position (Module 4)
debt_adj = 500.0           # Debt adjustment (Conservative)
shares_out = 457.0         # Million Shares
spot_price = 73.42         # Current Market Price
tax_rate = 0.27            # SA Corporate Tax

# 2️⃣ PROBABILITY FIELDS (DISTRIBUTIONS)
# We use Triangular distributions for asymmetric risks (Skewed Downside)
# Format: (Min, Mode, Max)

# A. Revenue Growth (The Rollout)
# Bear: 8% (Saturation), Base: 13.5% (Target), Bull: 16% (Blue Sky)
growth_dist = np.random.triangular(0.08, 0.135, 0.16, SIMULATIONS)

# B. Operating Margin (The Kill Switch)
# Bear: 3.5% (Cost Pressure), Base: 4.8% (Recovery), Bull: 5.8% (Shoprite Levels)
margin_dist = np.random.triangular(0.035, 0.048, 0.058, SIMULATIONS)

# C. WACC (The Macro Risk)
# Normal Distribution: Mean 13.2%, Std Dev 1.5% (Volatile SA Bond Yields)
wacc_dist = np.random.normal(0.132, 0.015, SIMULATIONS)

# D. Terminal Growth (The Long Tail)
# Uniform: 4.0% to 6.0% (SA GDP + Inflation proxy)
term_growth_dist = np.random.uniform(0.04, 0.06, SIMULATIONS)

# E. Efficiency (Sales to Capital Ratio)
# How much revenue does R1 of capital generate? (Asset Turnover)
sales_to_cap_dist = np.random.normal(4.5, 0.5, SIMULATIONS)

# 3️⃣ THE ENGINE (VECTORIZED DCF)
# ------------------------------
print(f"🐺 Running {SIMULATIONS} simulations on [JSE: BOX]...")

# Initialize Arrays
projection_years = 5
fcf_matrix = np.zeros((SIMULATIONS, projection_years))
revenues = np.tile(current_revenue, SIMULATIONS)

# Loop through 5 years (Projecting paths)
for year in range(projection_years):
    # Grow Revenue
    revenues = revenues * (1 + growth_dist)
    
    # Calculate NOPAT (Net Operating Profit After Tax)
    ebit = revenues * margin_dist
    nopat = ebit * (1 - tax_rate)
    
    # Calculate Reinvestment (Growth / Sales-to-Capital)
    # Reinvestment needed to fund the revenue jump
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

# 4️⃣ TERMINAL VALUE CALCULATION
# TV = [FCFF_n+1 / (WACC - g)]
# Normalize Year 5 FCFF for steady state
final_nopat = (revenues * margin_dist) * (1 - tax_rate)
final_reinvestment = (final_nopat * term_growth_dist) / 0.20 # ROIC assumption for terminal
terminal_fcff = final_nopat - final_reinvestment

terminal_value = terminal_fcff / (wacc_dist - term_growth_dist)
pv_terminal = terminal_value / ((1 + wacc_dist) ** projection_years)

# 5️⃣ ENTERPRISE TO EQUITY BRIDGE
enterprise_value = pv_explicit + pv_terminal
equity_value = enterprise_value + net_cash - debt_adj
share_price_paths = equity_value / shares_out

# 6️⃣ STATISTICS & ALPHA EXTRACTION
# ------------------------------
p10 = np.percentile(share_price_paths, 10)
p50 = np.percentile(share_price_paths, 50)
p90 = np.percentile(share_price_paths, 90)
mean_val = np.mean(share_price_paths)
prob_win = np.sum(share_price_paths > spot_price) / SIMULATIONS * 100

# 7️⃣ REPORTING
print("-" * 50)
print(f"🐺 ALPHA STATE REPORT: BOXER RETAIL (BOX)")
print("-" * 50)
print(f"📍 Spot Price Ref:   R {spot_price:.2f}")
print(f"📊 Mean Value:       R {mean_val:.2f}")
print(f"📉 P10 (Bear Case):  R {p10:.2f}  (Risk of Ruin)")
print(f"⚖️ P50 (Base Case):  R {p50:.2f}  (The Median)")
print(f"📈 P90 (Bull Case):  R {p90:.2f}  (Blue Sky)")
print("-" * 50)
print(f"🎲 Probability Value > Spot: {prob_win:.1f}%")
print("-" * 50)

# Optional: Visualization (Histogram)
plt.figure(figsize=(10, 6))
plt.hist(share_price_paths, bins=100, color='#1f77b4', alpha=0.7, edgecolor='black')
plt.axvline(spot_price, color='red', linestyle='--', linewidth=2, label=f'Spot Price (R{spot_price})')
plt.axvline(p50, color='yellow', linestyle='-', linewidth=2, label=f'Fair Value (R{p50:.0f})')
plt.title('Thousand Paths: Boxer Retail Valuation Distribution', fontsize=14)
plt.xlabel('Implied Share Price (ZAR)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.show()