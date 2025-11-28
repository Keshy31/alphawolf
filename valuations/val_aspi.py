import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 🐺 ALPHA WOLF: MODULE 7 - THOUSAND PATHS SIMULATION (RE-CALIBRATED)
# Target: ASP Isotopes Inc. (ASPI)
# Objective: Run a Damodaran-style Sum-of-Parts Monte Carlo to quantify value distribution.

# --- 1. SETTING THE SCENE (PARAMETERS) ---
SIMULATIONS = 50000
np.random.seed(42) # The Wolf's Code: Reproducibility

# --- 2. PART A: THE FACTORY (Medical & Si-28) ---
# wolf_note: Industrial ramps are binary. We model two regimes.

# Regime 1: "Execution Success" (70% Prob) - Plants open on time.
# Guidance: Q3 Update $50M-$70M. We assume slight upside for pricing power.
rev_success = np.random.triangular(50, 65, 85, SIMULATIONS)

# Regime 2: "Construction Delay" (30% Prob) - 6-month slip.
# Revenue is limited to legacy/pilot capacity ($15M-$25M).
rev_delay = np.random.uniform(15, 25, SIMULATIONS)

# Create the Regime Mask (1 = Success, 0 = Delay)
# We assume a 70% success rate based on current shipment proofs.
regime_mask = np.random.binomial(1, 0.70, SIMULATIONS)

# Combine Revenues based on Regime
revenue_2027 = (rev_success * regime_mask) + (rev_delay * (1 - regime_mask))

# Stress-Tested Margins
# If Delayed (Regime 0), margins crash due to fixed costs (10%).
# If Success (Regime 1), margins are healthy but volatile (25%-35%).
margin_success = np.random.normal(0.30, 0.05, SIMULATIONS)
margin_delay = np.random.normal(0.10, 0.05, SIMULATIONS) # Fixed cost drag
margins = (margin_success * regime_mask) + (margin_delay * (1 - regime_mask))

# Valuation Multiple (EV/EBITDA)
# We apply a penalty multiple to the "Delay" scenario (market loses faith).
multiple_success = np.random.uniform(14, 18, SIMULATIONS) # Growth premium
multiple_delay = np.random.uniform(8, 12, SIMULATIONS) # "Show me" penalty
multiples = (multiple_success * regime_mask) + (multiple_delay * (1 - regime_mask))

# Discount Rate (WACC for Commercial Stage)
# 15% reflects the execution risk of a small cap.
discount_rate = 0.15
years_to_discount = 2 # 2027 back to 2025

# CALCULATE FACTORY VALUE (Present Value)
ebitda_2027 = revenue_2027 * margins
factory_ev_future = ebitda_2027 * multiples
factory_pv = factory_ev_future / ((1 + discount_rate) ** years_to_discount)

# --- 3. PART B: THE OPTION (Nuclear / QLE) ---
# Logic: A Probability-Weighted Asset.
# Scenarios based on S-1 Filing & TerraPower status.

# Define Scenarios & Probabilities
# 1. Failure (15%): IPO pulled, tech fails. Value = $0.
# 2. Base/Delay (50%): IPO happens, but modest val ($400M-$600M).
# 3. Bull/Win (35%): IPO hot, HALEU critical ($1.0B-$1.4B).
scenarios = ['Cold', 'Base', 'Bull']
probs = [0.40, 0.40, 0.20]

# Generate the Scenario Indices
scenario_indices = np.random.choice(len(scenarios), SIMULATIONS, p=probs)

# Assign Values based on Scenarios (with some variance within scenarios)
nuclear_vals = np.zeros(SIMULATIONS)

# Apply values
# Fail case is just 0 (plus maybe some small scrap value noise, but let's keep it clean at 0)
nuclear_vals[scenario_indices == 0] = np.random.normal(400, 20, np.sum(scenario_indices == 0))

# Base Case: Normal dist around $500M
nuclear_vals[scenario_indices == 1] = np.random.triangular(600, 750, 900, np.sum(scenario_indices == 1))

# Bull Case: Normal dist around $1.2B
nuclear_vals[scenario_indices == 2] = np.random.normal(1200, 200, np.sum(scenario_indices == 2))

# --- 4. PART C: THE FOUNDATION (Cash & Shares) ---
# Net Cash (Cash - Debt).
# Logic: $405M Cash - $165M Debt = $240M Base.
# Add uncertainty for burn rate over next 12 months (-$50M to -$100M).
starting_cash = 378
debt = 66

# Burn varies by regime
# Success = High Burn (Building) / Delay = Med Burn (Stalled)
burn_success = np.random.uniform(80, 120, SIMULATIONS)
burn_delay = np.random.uniform(50, 80, SIMULATIONS)
burn_rate = (burn_success * regime_mask) + (burn_delay * (1 - regime_mask))

net_cash_final = starting_cash - debt - burn_rate

# Share Count (Dilution Risk)
# Base 145M. Risk of further dilution to fund QLE if IPO delays.
shares = np.random.triangular(102, 105, 108, SIMULATIONS)

# --- 5. THE FUSION (Price Per Share) ---
total_equity_value = factory_pv + nuclear_vals + net_cash_final
price_per_share = total_equity_value / shares

# --- 6. STATISTICS & VISUALIZATION ---
mean_price = np.mean(price_per_share)
p10 = np.percentile(price_per_share, 10)
p50 = np.median(price_per_share)
p90 = np.percentile(price_per_share, 90)
current_price = 5.97 # Reference Price

# Plotting
plt.figure(figsize=(12, 6))
sns.histplot(price_per_share, bins=100, kde=True, color='#2c3e50', stat='density', alpha=0.6)

# Annotations
plt.axvline(current_price, color='red', linestyle='--', linewidth=2, label=f'Current Price (${current_price})')
plt.axvline(p50, color='gold', linestyle='-', linewidth=2, label=f'Median Value (${p50:.2f})')
plt.axvline(p10, color='maroon', linestyle=':', linewidth=2, label=f'P10 Downside (${p10:.2f})')
plt.axvline(p90, color='green', linestyle=':', linewidth=2, label=f'P90 Upside (${p90:.2f})')

plt.title('ASPI "Thousand Paths" SOTP Valuation (Post-Q3 Update)', fontsize=16, fontweight='bold', color='#1a1a1a')
plt.xlabel('Fair Value Per Share ($)', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.xlim(0, 18)

# Save
plt.savefig('aspi_sotp_monte_carlo.png')

# Output Stats
print(f"Mean Fair Value: ${mean_price:.2f}")
print(f"Median Fair Value: ${p50:.2f}")
print(f"P10 (Bear Case): ${p10:.2f}")
print(f"P90 (Bull Case): ${p90:.2f}")
print(f"Probability Value > ${current_price}: {np.mean(price_per_share > current_price)*100:.1f}%")