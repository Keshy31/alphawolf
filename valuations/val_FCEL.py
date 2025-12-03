import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def alphawolf_sotp_valuation():
    # 1. SETUP
    np.random.seed(42)
    SIMULATIONS = 50000
    SHARES_OUTSTANDING = 24.44e6  # 24.44 Million shares (Dec 2025)
    
    # 2. ASSET A: THE UTILITY (Backlog Discounting)
    # Total Backlog roughly $1.1B for Gen/Service. We model the realized profit value.
    # We assume this backlog unwinds over ~15 years.
    backlog_total = 1.12e9 
    
    # Margin Distribution (Triangular: Bear, Mode, Bull)
    utility_margin = np.random.triangular(0.20, 0.35, 0.45, SIMULATIONS)
    
    # Discount Rate (WACC) for Utility Assets (Lower than Corp WACC)
    utility_wacc = np.random.triangular(0.065, 0.075, 0.090, SIMULATIONS)
    
    # PV of Backlog Profit = (Backlog * Margin) / Discount_Adjustment
    # Simplified annuity approximation for 15 years
    annuity_factor = (1 - (1 + utility_wacc)**-15) / utility_wacc
    annual_revenue = backlog_total / 15
    pv_utility = (annual_revenue * utility_margin) * annuity_factor

    # 3. ASSET B: THE GROWTH ENGINE (Product Sales)
    # 2026 Sales Projections
    prod_sales_26 = np.random.triangular(100e6, 180e6, 250e6, SIMULATIONS)
    # EV/Sales Multiple
    prod_multiple = np.random.triangular(1.0, 2.5, 4.0, SIMULATIONS)
    
    val_growth = prod_sales_26 * prod_multiple

    # 4. ASSET C: THE MOONSHOT (Exxon/Carbon Capture)
    # Modeled as a binary event with varying payouts
    # 40% chance of $0 (Fail), 50% chance of $100M (Niche), 10% chance of $500M (Home Run)
    moonshot_outcomes = np.random.choice([0, 100e6, 500e6], size=SIMULATIONS, p=[0.4, 0.5, 0.1])
    val_moonshot = moonshot_outcomes

    # 5. LIABILITIES: THE "CORPORATE TAX" & DEBT
    # Net Debt position (approx)
    net_debt = 50e6 # Cash $237M - Debt/Leases ~280M (Estimated net)
    
    # Corporate Overhead Capitalized (The cost of running the HQ)
    # Burn $100M/year capitalized at 10% discount rate for 5 years
    corp_burn_annual = np.random.triangular(100e6, 120e6, 150e6, SIMULATIONS)
    pv_corp_drag = corp_burn_annual * ((1 - (1.10)**-5) / 0.10)

    # 6. TOTAL EQUITY VALUE
    # Sum of Parts - Debt - Corp Drag
    total_equity_value = pv_utility + val_growth + val_moonshot - net_debt - pv_corp_drag
    
    # Floor value at Liquidation (approx Cash - Liabilities)
    # We assume in worst case, tech has some salvage value, so floor at $2/share
    
    fair_value_per_share = total_equity_value / SHARES_OUTSTANDING

    # 7. OUTPUT GENERATION
    p10 = np.percentile(fair_value_per_share, 10)
    p50 = np.percentile(fair_value_per_share, 50)
    p90 = np.percentile(fair_value_per_share, 90)
    prob_profit = np.mean(fair_value_per_share > 6.71) # Assumed Spot Price

    print(f"--- ALPHAWOLF VALUATION OUTPUT ---")
    print(f"Spot Price Reference: $6.71")
    print(f"P10 (The 'Trap'):     ${p10:.2f}")
    print(f"P50 (Fair Value):     ${p50:.2f}")
    print(f"P90 (The 'Alpha'):    ${p90:.2f}")
    print(f"Probability > Spot:   {prob_profit:.2%}")
    print(f"----------------------------------")
    
    # Sensitivity Check
    print(f"Correlation (Value vs Product Sales): {np.corrcoef(fair_value_per_share, prod_sales_26)[0,1]:.2f}")
    print(f"Correlation (Value vs Moonshot):      {np.corrcoef(fair_value_per_share, val_moonshot)[0,1]:.2f}")

alphawolf_sotp_valuation()