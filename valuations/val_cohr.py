import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# SYSTEM IDENTITY: ALPHAWOLF CORE ENGINE
np.random.seed(42)
SIMULATIONS = 10000

# --- INPUTS ---
# Shares Outstanding (Millions)
SHARES_OUT = 157.0
# Net Debt (Total Debt - Cash) ($M) - Q1 FY26 Est.
NET_DEBT = 2800.0 
# Tax Rate
TAX_RATE = 0.21
# WACC Distribution (Triangular: Min, Mode, Max)
wacc_dist = np.random.triangular(0.085, 0.098, 0.110, SIMULATIONS)

# --- SEGMENT 1: NETWORKING (THE ROCKET) ---
# Revenue Base (Last TTM approx split)
rev_net_base = 4200.0 
# Growth Rates (Next 5 Years)
g_net_dist = np.random.triangular(0.12, 0.22, 0.35, SIMULATIONS)
# Target Operating Margin
margin_net_dist = np.random.triangular(0.18, 0.24, 0.28, SIMULATIONS)

# --- SEGMENT 2: INDUSTRIAL (THE ANCHOR) ---
# Revenue Base
rev_ind_base = 1800.0
# Growth Rates
g_ind_dist = np.random.triangular(-0.02, 0.03, 0.06, SIMULATIONS)
# Target Operating Margin
margin_ind_dist = np.random.triangular(0.10, 0.15, 0.18, SIMULATIONS)

# --- CALCULATION ENGINE (VECTORIZED) ---
# 5-Year Projection
# We simplify to a 5-year DCF + Terminal Value for speed
discount_factors = np.array([(1 + wacc_dist) ** -t for t in range(1, 6)])

# Initialize Cash Flow arrays
fcf_total = np.zeros(SIMULATIONS)

# Loop 5 years (Projecting FCFF)
curr_rev_net = np.full(SIMULATIONS, rev_net_base)
curr_rev_ind = np.full(SIMULATIONS, rev_ind_base)

for t in range(5):
    # Grow Revenue
    curr_rev_net *= (1 + g_net_dist)
    curr_rev_ind *= (1 + g_ind_dist)
    
    # Calc EBIT
    ebit_net = curr_rev_net * margin_net_dist
    ebit_ind = curr_rev_ind * margin_ind_dist
    total_ebit = ebit_net + ebit_ind
    
    # NOPAT (Net Operating Profit After Tax)
    nopat = total_ebit * (1 - TAX_RATE)
    
    # Reinvestment (Simplified: ~35% of NOPAT needed for growth blended)
    reinvestment = nopat * 0.35
    
    # FCFF
    fcff = nopat - reinvestment
    
    # Discount to PV
    fcf_total += fcff / ((1 + wacc_dist) ** (t + 1))

# Terminal Value (Gordon Growth)
# Blended Terminal Growth ~3.5%
tv_growth = 0.035
terminal_cash_flow = (curr_rev_net * margin_net_dist + curr_rev_ind * margin_ind_dist) * (1 - TAX_RATE) * 0.65 # Assume stable reinvestment
terminal_value = terminal_cash_flow * (1 + tv_growth) / (wacc_dist - tv_growth)
pv_terminal_value = terminal_value / ((1 + wacc_dist) ** 5)

# Enterprise Value
ev = fcf_total + pv_terminal_value

# Equity Value
equity_value = ev - NET_DEBT
price_per_share = equity_value / SHARES_OUT

# --- OUTPUT ---
p10 = np.percentile(price_per_share, 10)
p50 = np.percentile(price_per_share, 50)
p90 = np.percentile(price_per_share, 90)

print(f"ALPHAWOLF VALUATION // COHR")
print(f"Current Market Price: ~$164.26")
print(f"---")
print(f"P10 (Bear): ${p10:.2f}")
print(f"P50 (Base): ${p50:.2f}")
print(f"P90 (Bull): ${p90:.2f}")
print(f"Probability of Upside: {np.mean(price_per_share > 164.26) * 100:.1f}%")

# Plotting (Simulated for visual context in text response)
plt.figure(figsize=(12, 6))
sns.histplot(price_per_share, color='#2c3e50', kde=True)
plt.title('COHR: Valuation Distribution', fontsize=16, fontweight='bold', color='#1a1a1a')
plt.xlabel('Fair Value Per Share', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.savefig('val_cohr_dist.png')