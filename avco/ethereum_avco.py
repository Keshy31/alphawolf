import pandas as pd
import numpy as np

# Load the file again
filename = '5685614742285959814_0001.csv'
df = pd.read_csv(filename)

# Filter for ETH
df_eth = df[df['Currency'] == 'ETH'].copy()
df_eth['Timestamp (UTC)'] = pd.to_datetime(df_eth['Timestamp (UTC)'])
df_eth = df_eth.sort_values('Timestamp (UTC)')

# Logic for AVCO
current_holdings = 0.0
total_cost_basis = 0.0
transaction_history = []

for index, row in df_eth.iterrows():
    delta = row['Balance delta']
    value_zar = row['Value amount']
    desc = row['Description']
    timestamp = row['Timestamp (UTC)']
    
    is_inflow = delta > 0
    
    # State before
    prev_holdings = current_holdings
    prev_cost_basis = total_cost_basis
    prev_avg_cost = 0.0 if prev_holdings == 0 else prev_cost_basis / prev_holdings
    
    step_pnl = 0.0
    action_type = ""
    price_per_unit = 0.0
    
    if is_inflow:
        action_type = "Buy/Receive"
        # Logic: New Cost = Old Cost + Value of Inflow
        current_holdings += delta
        total_cost_basis += value_zar
        price_per_unit = value_zar / delta if delta != 0 else 0
        
    else: # Outflow
        action_type = "Sell/Send"
        abs_delta = abs(delta)
        price_per_unit = value_zar / abs_delta if abs_delta != 0 else 0
        
        if prev_holdings > 0:
            # Cost of the specific amount leaving based on weighted average
            cost_of_exit = abs_delta * prev_avg_cost
            
            # Reduce total cost basis
            total_cost_basis -= cost_of_exit
            
            # Realized PnL (only relevant if it's a sell vs transfer, but strictly mathematically:
            # PnL = Proceeds - Cost Basis. If it's a transfer, Proceeds usually 0 or N/A, 
            # but here 'Value amount' is often the ZAR equivalent. 
            # If Description says "Sold", it's a taxable event.
            if "Sold" in desc:
                 step_pnl = value_zar - cost_of_exit
            
            current_holdings += delta 
        else:
            # Negative balance case (data anomaly or margin), just track delta
            current_holdings += delta
            
    # Update average cost
    # If holdings drop to near zero, reset or keep last known? 
    # Usually if 0, cost basis is 0.
    if current_holdings <= 0.00000001: # Epsilon for float errors
        curr_avg_cost = 0.0
        total_cost_basis = 0.0 # Reset if empty
    else:
        curr_avg_cost = total_cost_basis / current_holdings
    
    transaction_history.append({
        'Timestamp': timestamp,
        'Action': action_type,
        'Description': desc,
        'Quantity_ETH': delta,
        'Transaction_Price_ZAR': price_per_unit,
        'Transaction_Value_ZAR': value_zar,
        'Realized_PnL_ZAR': step_pnl if step_pnl != 0 else np.nan,
        'Total_Holdings_ETH': current_holdings,
        'Total_Cost_Basis_ZAR': total_cost_basis,
        'Blended_Cost_Per_ETH_ZAR': curr_avg_cost
    })

# Create DataFrame
avco_df = pd.DataFrame(transaction_history)

# Save to CSV
output_filename = 'ETH_AVCO_History.csv'
avco_df.to_csv(output_filename, index=False)

print(f"File saved as {output_filename}")
print(avco_df.tail())