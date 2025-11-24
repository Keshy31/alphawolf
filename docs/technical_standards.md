# 🐺 AlphaWolf Technical Standards

To maintain "Jane Street Rigor" with "Renaissance Storytelling," all technical artifacts must adhere to the Wolf's Code.

## 1. Code Hygiene

### The Stack
*   **Core Math:** `numpy` (Vectorized operations only. No slow for-loops for simulations).
*   **Data Structure:** `pandas` (For time-series or tabular data handling, though numpy arrays preferred for raw sim speed).
*   **Visualization:** `matplotlib.pyplot`, `seaborn`.

### Reproducibility
Every simulation MUST be reproducible.
```python
import numpy as np
# The Wolf's Code: Reproducibility
np.random.seed(42)
SIMULATIONS = 50000 # Minimum for robust tails
```

### Windows Compatibility
Ensure standard output handles UTF-8 characters (like 🐺) on Windows.
```python
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## 2. Visualization Style

All plots must follow the AlphaWolf visual identity: **Dark, Professional, Sharp.**

### Color Palette
*   **Histogram:** `#2c3e50` (Dark Slate Blue)
*   **Current Price (Reference):** `red` (Dashed Line)
*   **Median (P50):** `gold` (Solid Line) - The Anchor
*   **Bear Case (P10):** `maroon` (Dotted Line) - The Risk
*   **Bull Case (P90):** `green` (Dotted Line) - The Reward

### Plot Structure
```python
plt.figure(figsize=(12, 6))
sns.histplot(data, bins=100, kde=True, color='#2c3e50', stat='density', alpha=0.6)
plt.title('TICKER "Thousand Paths" Valuation', fontsize=16, fontweight='bold', color='#1a1a1a')
plt.xlabel('Fair Value Per Share', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.savefig('ticker_valuation.png')
```

## 3. Output Format

The bot reads stdout to generate the final report. Logs must be regex-friendly.

### Required Output Block
At the end of every script, print the key stats in this exact format:
```text
🐺 SIMULATION REPORT [N=50000]
Current Price: R 123.45
------------------------------
Mean Fair Value:   R 140.00
Median Fair Value: R 138.50
P10 (Bear Case):   R 110.00
P90 (Bull Case):   R 180.00
------------------------------
PROBABILITY OF PROFIT: 65.4%
Expected Upside (Mean): 13.4%
```

## 4. Modeling Conventions

### Variable Naming
*   Use `snake_case` for variables.
*   Use `ALL_CAPS` for constants (`SIMULATIONS`, `SHARES_OUT`).
*   Suffix distributions with their type or unit if ambiguous (`margin_dist`, `price_zar`).

### Distribution Selection
*   **Triangular (`np.random.triangular`):** Use when you have a specific Bear/Base/Bull view (e.g., Management Guidance).
*   **Normal (`np.random.normal`):** Use for natural phenomena (FX rates, Commodity prices, generic volatility).
*   **Uniform (`np.random.uniform`):** Use for maximum uncertainty within a range (e.g., "Burn rate is between 50 and 100").
*   **Binomial (`np.random.binomial`):** Use for regime switches (e.g., "Success/Fail" masks).

