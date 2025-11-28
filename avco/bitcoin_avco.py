import pandas as pd
import numpy as np

# Configuration
CURRENT_BTC_PRICE_ZAR = 1499166.14
filename = '1142728405724743374_0001.csv'

# Load
df = pd.read_csv(filename)
# Filter for BTC
df_btc = df[df['Currency'].isin(['XBT', 'BTC'])].copy()
df_btc['Timestamp (UTC)'] = pd.to_datetime(df_btc['Timestamp (UTC)'])
df_btc = df_btc.sort_values('Timestamp (UTC)')

# State
pool_coins = 0.0
pool_total_cost = 0.0
pool_avg_cost = 0.0
exchange_balance = 0.0
external_balance = 0.0

transaction_history = []

for index, row in df_btc.iterrows():
    delta = row['Balance delta']
    value_zar = row['Value amount']
    desc = str(row['Description']) # Keep case for regex if needed, but lower is easier
    desc_lower = desc.lower()
    timestamp = row['Timestamp (UTC)']
    abs_delta = abs(delta)
    
    action = "Unknown"
    notes = ""
    
    # ---------------------------------------------------------
    # LOGIC CORE
    # ---------------------------------------------------------
    
    if delta > 0:
        # === INFLOWS (BTC Balance Increases) ===
        exchange_balance += abs_delta
        
        # 1. Plain Buy with Fiat ("Bought BTC... @ price")
        if "bought" in desc_lower and "btc" in desc_lower and "eth" not in desc_lower and "ltc" not in desc_lower and "bch" not in desc_lower and "xrp" not in desc_lower and "sol" not in desc_lower:
            action = "Buy (Fiat)"
            pool_coins += abs_delta
            pool_total_cost += value_zar
            
        # 2. Crypto-to-Crypto Buy ("Sold ETH... for BTC") -> effectively Buying BTC
        elif "sold" in desc_lower and "for btc" in desc_lower:
            action = "Buy (Crypto Swap)"
            # We treat this as buying BTC using the ZAR value of the altcoin sold
            pool_coins += abs_delta
            pool_total_cost += value_zar
            notes = "Swapped Altcoin for BTC"
            
        # 3. Receive (Transfer)
        elif "received" in desc_lower:
            action = "Receive (Transfer)"
            if external_balance >= abs_delta:
                external_balance -= abs_delta
            else:
                # Phantom deposit handling
                excess = abs_delta - max(0, external_balance)
                external_balance = 0.0
                if excess > 0:
                    action = "Receive + Deposit (Adjustment)"
                    pool_coins += excess
                    # Cost basis for excess? Market value at time.
                    price = value_zar / abs_delta if abs_delta > 0 else 0
                    pool_total_cost += (excess * price)
                    notes = f"Found {excess:.6f} BTC extra"
                    
        else:
            # Fallback for weird descriptions (often direct deposits/mining/unknown)
            # Default to Buy/Deposit
            action = "Deposit/Buy (Other)"
            pool_coins += abs_delta
            pool_total_cost += value_zar

    else:
        # === OUTFLOWS (BTC Balance Decreases) ===
        exchange_balance -= abs_delta
        
        # 1. Plain Sell to Fiat ("Sold... for R...")
        if "sold" in desc_lower and "for r" in desc_lower:
             action = "Sell (Fiat)"
             if pool_coins > 0:
                 cost_part = abs_delta * pool_avg_cost
                 pool_total_cost -= cost_part
                 pool_coins -= abs_delta
                 
        # 2. Crypto-to-Crypto Sell ("Bought ETH... for BTC") -> Spending BTC
        elif "bought" in desc_lower and "for btc" in desc_lower:
            action = "Sell (Crypto Swap)"
            # We are spending BTC to buy another coin.
            # This is a DISPOSAL of BTC.
            if pool_coins > 0:
                 cost_part = abs_delta * pool_avg_cost
                 pool_total_cost -= cost_part
                 pool_coins -= abs_delta
            notes = "Spent BTC to buy Altcoin"

        # 3. Transfers / Fees
        elif "fee" in desc_lower:
            action = "Fee (Sell)"
            # Fees are realized losses/expenses. We reduce the pool.
            # Usually treated as a 'spend' (disposal).
            if pool_coins > 0:
                 cost_part = abs_delta * pool_avg_cost
                 pool_total_cost -= cost_part
                 pool_coins -= abs_delta

        elif "sent" in desc_lower or "kesh" in desc_lower or "emptying" in desc_lower:
            action = "Send (Transfer)"
            external_balance += abs_delta
            # Pool Coins UNCHANGED (still owned)
            
        else:
            # Catch-all for ambiguous outflows. 
            # If it says 'Sold' but not handled above?
            if "sold" in desc_lower:
                action = "Sell (Other)"
                if pool_coins > 0:
                    cost_part = abs_delta * pool_avg_cost
                    pool_total_cost -= cost_part
                    pool_coins -= abs_delta
            else:
                # Assume Transfer for unknown withdrawals
                action = "Send (Unclassified)"
                external_balance += abs_delta

    # Update Average
    if pool_coins > 1e-9:
        pool_avg_cost = pool_total_cost / pool_coins
    else:
        pool_avg_cost = 0.0
        pool_total_cost = 0.0

    transaction_history.append({
        'Timestamp': timestamp,
        'Raw_Desc': desc,
        'Action': action,
        'Delta': delta,
        'Value_ZAR': value_zar,
        'Pool_Coins': pool_coins,
        'Pool_Avg_Cost': pool_avg_cost,
        'Exchange_Bal': exchange_balance,
        'External_Bal': external_balance,
        'Notes': notes
    })

# Output
res_df = pd.DataFrame(transaction_history)

# Filter for Crypto-Crypto examples to show user
swaps = res_df[res_df['Action'].str.contains("Swap")]

print("Crypto-Crypto Transactions Found:")
print(swaps[['Timestamp', 'Action', 'Raw_Desc', 'Delta', 'Value_ZAR']].head())

print("\nFinal State:")
print(f"Exchange Bal: {exchange_balance:.8f}")
print(f"External Bal (Hacked): {external_balance:.8f}")
print(f"Pool Avg Cost: {pool_avg_cost:.2f}")

# Save for user
res_df.to_csv("BTC_Audit_Detailed.csv", index=False)