import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# SYSTEM: ALPHAWOLF CORE ENGINE
# TARGET: SIBANYE-STILLWATER (JSE: SSW)
# DATE: DEC 3, 2025

def run_simulation():
    np.random.seed(42)
    SIMULATIONS = 10000
    
    # --- VARIABLES (The Drivers) ---
    # 1. Commodity Prices (ZAR Basket normalization factor)
    # Triangular: Bear (R24k), Base (R30k), Bull (R38k)
    basket_price_zar = np.random.triangular(24000, 30000, 38000, SIMULATIONS)
    
    # 2. Production Volumes (Millions of oz 4E)
    # Normal Dist: Mean 3.2Moz, StdDev 0.15Moz (Operational risk)
    production_vol = np.random.normal(3.2, 0.15, SIMULATIONS)
    
    # 3. All-in Sustaining Cost (AISC) Margin %
    # Dependent on US restructure success.
    # Uniform distribution between 12% (fail) and 25% (success)
    margin_percent = np.random.uniform(0.12, 0.25, SIMULATIONS)
    
    # 4. Valuation Multiple (EV/EBITDA)
    # Market sentiment factor
    multiple = np.random.triangular(3.0, 4.5, 6.5, SIMULATIONS)
    
    # --- CALCULATION ENGINE ---
    # Revenue Proxy (simplified linear relationship to basket)
    # Base Revenue at R30k basket ~ R135bn. 
    revenue = (basket_price_zar / 30000) * 135000 # R millions
    
    ebitda = revenue * margin_percent
    
    # Enterprise Value
    ev = ebitda * multiple
    
    # Equity Value (EV - Net Debt)
    # Net Debt fixed at R25bn (Current state)
    net_debt = 25000 
    equity_value_total = ev - net_debt
    
    # Share Count (Millions)
    shares = 2830
    fair_value_per_share = equity_value_total / shares
    
    # Filter out negative equity values (Bankruptcy risk)
    fair_value_per_share = np.maximum(fair_value_per_share, 0)

    # --- OUTPUTS ---
    p10 = np.percentile(fair_value_per_share, 10)
    p50 = np.percentile(fair_value_per_share, 50)
    p90 = np.percentile(fair_value_per_share, 90)
    
    current_price = 56.82
    prob_profit = np.mean(fair_value_per_share > current_price) * 100
    
    print(f"--- ALPHAWOLF MONTE CARLO RESULTS (n={SIMULATIONS}) ---")
    print(f"P10 (Downside Risk):  R{p10:.2f}")
    print(f"P50 (Fair Value):     R{p50:.2f}")
    print(f"P90 (Upside Tail):    R{p90:.2f}")
    print(f"Current Spot:         R{current_price}")
    print(f"Probability of Profit: {prob_profit:.1f}%")
    print(f"Estimated Edge:       {((p50 - current_price)/current_price)*100:.1f}%")

run_simulation()