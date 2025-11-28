import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. CONFIGURE THE HUNT (Assumptions) ---
N_SIMS = 50000
np.random.seed(42) # For the Wolf's reproducibility

# A. The Crown Jewel (Cartier/VCA)
# Logic: Base EBITDA €5.32bn with slight operational variance.
# Multiple: Triangular distribution skewing towards higher quality.
jewellery_ebitda = np.random.normal(5320, 150, N_SIMS) # € Millions
jewellery_multiple = np.random.triangular(18, 22, 28, N_SIMS)

# B. The Distressed Asset (Watchmakers)
# Logic: PERT distribution. Sticky low base (€260m), small chance of zero, decent chance of recovery.
# Note: Using Beta distribution scaled to range to approximate PERT
def pert(min_val, mode_val, max_val, n):
    alpha = 1 + 4 * (mode_val - min_val) / (max_val - min_val)
    beta = 1 + 4 * (max_val - mode_val) / (max_val - min_val)
    return min_val + np.random.beta(alpha, beta, n) * (max_val - min_val)

watch_ebitda = pert(150, 260, 800, N_SIMS) # € Millions (Widened max for recovery option)
watch_multiple = np.random.uniform(8, 12, N_SIMS) # Distressed to Normal Luxury

# C. The "Other" & Corp Costs
other_value = 1300 # €1.3bn Fixed (Immaterial)
corp_drag_value = np.random.normal(-7500, 500, N_SIMS) # Capitalized Head Office Costs
net_cash = 6500 # €6.5bn Cash Pile (Fortress)

# D. The Tax (Holding Discount)
# Logic: Market penalizes structure. Uniform 5% to 15% discount.
holding_discount = np.random.uniform(0.05, 0.15, N_SIMS)

# E. The Currency (The Rand Hedge)
# Logic: Mean 20.50 (Drift), StdDev 1.5 (High Volatility)
eur_zar = np.random.normal(20.50, 1.5, N_SIMS)

# --- 2. RUN THE SIMULATION (The Calculation) ---

# Step 1: Gross Enterprise Value (Sum of Parts)
ev_gross = (jewellery_ebitda * jewellery_multiple) + (watch_ebitda * watch_multiple) + other_value + corp_drag_value

# Step 2: Equity Value (EUR)
# Add Cash, Apply Holding Discount
equity_value_eur = (ev_gross + net_cash) * (1 - holding_discount)

# Step 3: Per Share Value (EUR -> ZAR)
SHARES_OUT = 570 # Million
fair_value_eur_per_share = equity_value_eur / SHARES_OUT
fair_value_zar = fair_value_eur_per_share * eur_zar

# --- 3. ANALYZE THE KILL ---
current_price = 3635.53
upside = (fair_value_zar - current_price) / current_price
prob_profit = np.mean(fair_value_zar > current_price)

# Output Stats
print(f"🐺 SIMULATION REPORT [N={N_SIMS}]")
print(f"Current Price: R {current_price:,.2f}")
print("-" * 30)
print(f"Mean Fair Value:   R {np.mean(fair_value_zar):,.2f}")
print(f"Median Fair Value: R {np.median(fair_value_zar):,.2f}")
print(f"P10 (Bear Case):   R {np.percentile(fair_value_zar, 10):,.2f}")
print(f"P90 (Bull Case):   R {np.percentile(fair_value_zar, 90):,.2f}")
print("-" * 30)
print(f"PROBABILITY OF PROFIT: {prob_profit:.1%}")
print(f"Expected Upside (Mean): {np.mean(upside):.1%}")