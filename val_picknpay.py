import numpy as np

# Wolf's Parameters
n_sims = 100000
current_price = 25.78

# 1. Asset 1: The Anchor (Boxer Stake)
# Boxer Price Volatility (Normal Dist, 25% vol)
boxer_price_shock = np.random.normal(1.0, 0.40, n_sims)
boxer_base_value_per_share = 29.20 # PIK's share of Boxer
boxer_value_sim = boxer_base_value_per_share * boxer_price_shock

# 2. Asset 2: The Cash (Fixed)
net_cash_per_share = 5.45

# 3. Asset 3: The Gamble (Core Turnaround DCF)
# Terminal Margin (Triangular: Min 0%, Mode 1.5%, Max 3.5%)
core_margin_sim = np.random.triangular(0.00, 0.015, 0.035, n_sims)
# Revenue Base (R60bn) * Margin * Multiple (6x EV/EBITDA implied for distressed retail)
# Simplified DCF proxy: Value of Core = (Rev * Margin * Multiple) / Shares
multiple = np.random.choice([5.0, 6.5, 8.0], n_sims, p=[0.3, 0.5, 0.2])
core_value_sim = (60e9 * core_margin_sim * multiple) / 745e6 # 745m shares

# 4. The Friction (HoldCo Discount)
# Discount applied to the TOTAL sum (Triangular: 5% to 25%, Mode 15%)
holdco_discount = np.random.triangular(0.05, 0.15, 0.25, n_sims)

# Total Value Calculation
gross_value = boxer_value_sim + net_cash_per_share + core_value_sim
final_value = gross_value * (1 - holdco_discount)

# Metrics
upside_prob = np.mean(final_value > current_price)
doubler_prob = np.mean(final_value > (current_price * 1.5))
downside_risk = np.percentile(final_value, 10) # P10
target_value = np.median(final_value) # P50

print(f"P10 (Bear): {downside_risk:.2f}")
print(f"P50 (Base): {target_value:.2f}")
print(f"P90 (Bull): {np.percentile(final_value, 90):.2f}")
print(f"Prob of Profit: {upside_prob * 100:.1f}%")