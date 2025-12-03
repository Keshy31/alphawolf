import numpy as np

# ALPHAWOLF v12 CORE ENGINE // GOOGL SOTP SIMULATION
np.random.seed(42)
SIMULATIONS = 50000

# 1. SETUP VARIABLES (The Distributions)
# Search EBIT (Mature, Stable-ish)
# Base: $145B | Bull: Ad Market Boom | Bear: Regulatory Crush
search_ebit = np.random.triangular(130, 145, 160, SIMULATIONS)
search_multiple = np.random.triangular(15, 18, 22, SIMULATIONS)

# Cloud Revenue (Hyper-Growth)
# Base: $75B | Bull: AI Explosion | Bear: Competition/Saturation
cloud_rev = np.random.triangular(65, 75, 95, SIMULATIONS)
cloud_multiple = np.random.triangular(8, 12, 15, SIMULATIONS) # EV/Sales

# Adjustments
net_cash = 98  # Billions (Fixed from Q3)
corp_drag = np.random.normal(150, 10, SIMULATIONS) # Capitalized Corp Overhead
shares_outstanding = 12.2 # Billion Shares

# 2. THE CALCULATION (Vectorized)
ev_search = search_ebit * search_multiple
ev_cloud = cloud_rev * cloud_multiple
total_ev = ev_search + ev_cloud + 20 # Adding Other Bets fixed option value

equity_value = total_ev + net_cash - corp_drag
price_per_share = equity_value / shares_outstanding

# 3. THE VERDICT
p10 = np.percentile(price_per_share, 10)
p50 = np.percentile(price_per_share, 50)
p90 = np.percentile(price_per_share, 90)
current_price = 320.00
prob_profit = np.mean(price_per_share > current_price) * 100

print(f"--- ALPHAWOLF SOTP OUTPUT ---")
print(f"P10 (Bear Case):   ${p10:.2f}")
print(f"P50 (Base Case):   ${p50:.2f} (Fair Value)")
print(f"P90 (Bull Case):   ${p90:.2f}")
print(f"Current Spot:      ${current_price:.2f}")
print(f"Probability of Alpha: {prob_profit:.1f}%")