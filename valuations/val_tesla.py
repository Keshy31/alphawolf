import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 1. Setup
np.random.seed(42)
SIMULATIONS = 10000
SHARES_OUTSTANDING = 3.35  # Billion

# 2. Distributions (The Drivers)

# --- A. AUTOMOTIVE (The Anchor) ---
# Narrative: Margins are the battleground.
auto_rev = np.random.normal(90, 5, SIMULATIONS) # Revenue is relatively known ~$90B
auto_margin = np.random.triangular(0.08, 0.12, 0.17, SIMULATIONS) # Bear 8%, Base 12%, Bull 17%
auto_multiple = np.random.triangular(8, 12, 20, SIMULATIONS) # EV/EBIT. 8x (Ford) to 20x (Tech)

auto_ev = auto_rev * auto_margin * auto_multiple

# --- B. ENERGY (The Turbo) ---
# Narrative: High growth, but what is the terminal value?
energy_current_rev = np.random.normal(14, 1, SIMULATIONS) # Base
energy_growth = np.random.triangular(0.20, 0.35, 0.50, SIMULATIONS) # 20% to 50% CAGR
energy_years = 5
energy_terminal_margin = np.random.triangular(0.15, 0.20, 0.25, SIMULATIONS)
energy_wacc = np.random.triangular(0.09, 0.11, 0.13, SIMULATIONS)
energy_exit_multiple = np.random.triangular(15, 25, 40, SIMULATIONS)

# Calc Future Revenue & EBITDA
energy_future_rev = energy_current_rev * ((1 + energy_growth) ** energy_years)
energy_future_ebitda = energy_future_rev * energy_terminal_margin
energy_future_val = energy_future_ebitda * energy_exit_multiple
# Discount back
energy_ev = energy_future_val / ((1 + energy_wacc) ** energy_years)

# --- C. SERVICES (The Glue) ---
services_rev = np.random.normal(14, 1, SIMULATIONS)
services_multiple = np.random.triangular(2, 4, 6, SIMULATIONS) # Price-to-Sales
services_ev = services_rev * services_multiple

# --- D. AI / ROBOTAXI (The Option) ---
# Narrative: Binary Outcome. 
# Step 1: Does it work? (Probability)
ai_success_prob = np.random.uniform(0, 1, SIMULATIONS)
ai_success_threshold = 0.75 # 25% chance of success (AlphaWolf Assumption)

# Step 2: If it works, how big?
ai_tam = np.random.triangular(2000, 5000, 10000, SIMULATIONS) # $2T to $10T Market
ai_share = np.random.triangular(0.05, 0.15, 0.25, SIMULATIONS) # 5% to 25% Share
ai_margin = np.random.triangular(0.20, 0.40, 0.50, SIMULATIONS) # Software margins
ai_multiple = np.random.normal(20, 5, SIMULATIONS) # Mature Tech Multiple

ai_future_profit = ai_tam * ai_share * ai_margin
ai_future_val = ai_future_profit * ai_multiple

# Step 3: Discount it back (VC Rates)
ai_wacc_vc = np.random.normal(0.25, 0.05, SIMULATIONS) # 25% discount rate
ai_ev_success = ai_future_val / ((1 + ai_wacc_vc) ** 5)

# Step 4: Apply Binary Filter
ai_ev = np.where(ai_success_prob > ai_success_threshold, ai_ev_success, 0)

# --- E. AGGREGATION ---
net_cash = 34.0
total_equity_value = auto_ev + energy_ev + services_ev + ai_ev + net_cash
fair_value_dist = total_equity_value / SHARES_OUTSTANDING

# 3. Output Stats
p10 = np.percentile(fair_value_dist, 10)
p50 = np.percentile(fair_value_dist, 50)
p90 = np.percentile(fair_value_dist, 90)
current_price = 426.60
prob_alpha = np.mean(fair_value_dist > current_price)

print(f"P10: {p10}")
print(f"P50: {p50}")
print(f"P90: {p90}")
print(f"Prob Alpha: {prob_alpha}")

# 4. Visualization
plt.figure(figsize=(10, 6))
sns.histplot(fair_value_dist, bins=100, kde=True, color='#2c3e50', stat='density', alpha=0.6, edgecolor=None)
plt.axvline(x=p50, color='blue', linestyle='--', label=f'Fair Value (P50): ${p50:.2f}')
plt.axvline(x=current_price, color='red', linestyle='-', label=f'Current Price: ${current_price:.2f}')
plt.title(f'TSLA: AlphaWolf SOTP Monte Carlo (10,000 Paths)', fontsize=14)
plt.xlabel('Fair Value per Share ($)')
plt.ylabel('Density')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0, 1000) # Cap display to keep chart readable
plt.savefig('tsla_monte_carlo.png')