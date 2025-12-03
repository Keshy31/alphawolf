import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Setup
np.random.seed(42)
SIMULATIONS = 50000

# --- INPUTS BASED ON CONFIRMED FACTS (Q3 2025) ---
shares_outstanding = 91.0e6  # 91 Million Shares
cash_balance = 1.93e9        # $1.93 Billion (Q3 Report)
burn_discount = 0.85         # Market discounts cash by ~15% for future burn

# --- COMPONENT A: THE FLOOR (Risk-Adjusted Cash) ---
# We value the cash pile, but discount it because they are burning it.
cash_value_per_share = np.full(SIMULATIONS, (cash_balance * burn_discount) / shares_outstanding)

# --- COMPONENT B: THE ENGINE (CASGEVY REALITY) ---
# Instead of % of 35k TAM, we model "Peak Annual Infusions" globally.
# Bear: 500 (Niche product) | Base: 1200 (Blockbuster) | Bull: 2000 (Standard of Care)
peak_patients_dist = np.random.triangular(500, 1200, 2000, SIMULATIONS)

# Net Price (Vertex reported ~$1.8M realized approx)
price_dist = np.random.triangular(1.6e6, 1.8e6, 2.0e6, SIMULATIONS)

# Vertex Profit Margin (EBIT margin on the drug)
# Gene therapy margins are high (80% gross), but commercial costs are heavy initially.
# We assume steady state net margin of 55%.
margin_dist = np.random.normal(0.55, 0.05, SIMULATIONS)

# CRSP Profit Share (Contractual 40%)
profit_share = 0.40

# Revenue & Earnings Calculation
peak_revenue = peak_patients_dist * price_dist
peak_earnings_crsp = peak_revenue * margin_dist * profit_share

# Valuation Multiple (Exit P/E for a mature biotech)
# Lowered to 12x-15x as growth slows at peak
exit_multiple_dist = np.random.triangular(10, 13, 16, SIMULATIONS)

# Discount Rate (WACC) - Higher risk (12.5%) due to slow launch
wacc_dist = np.random.triangular(0.11, 0.125, 0.14, SIMULATIONS)
discount_years = 5 # Discounting back from 2030 Peak
discount_factor = (1 + wacc_dist) ** -discount_years

# PV of Commercial Stream
engine_value_total = (peak_earnings_crsp * exit_multiple_dist) * discount_factor
engine_value_per_share = engine_value_total / shares_outstanding

# --- COMPONENT C: THE CALL OPTION (Pipeline) ---
# Conservative valuation of Diabetes/Oncology (Values entire pipeline at ~$500M)
pipeline_val_total = np.random.triangular(200e6, 500e6, 1.0e9, SIMULATIONS)
pipeline_val_per_share = pipeline_val_total / shares_outstanding

# 3. Aggregation
fair_value_dist = cash_value_per_share + engine_value_per_share + pipeline_val_per_share

# 4. The Verdict
p10 = np.percentile(fair_value_dist, 10)
p50 = np.percentile(fair_value_dist, 50)
p90 = np.percentile(fair_value_dist, 90)
current_price = 55.00 

prob_profit = np.mean(fair_value_dist > current_price)
edge = (p50 - current_price) / current_price

print(f"--- ALPHAWOLF RECALIBRATED: THE SKEPTICAL MODEL ---")
print(f"Current Price Reference: ${current_price:.2f}")
print(f"P10 (Bear Case - 'Stalled Launch'): ${p10:.2f}")
print(f"P50 (Base Case - 'Rational Scale'): ${p50:.2f}")
print(f"P90 (Bull Case - 'Optimized'):      ${p90:.2f}")
print(f"Probability of Alpha: {prob_profit:.1%}")
print(f"True Edge: {edge:.1%}")