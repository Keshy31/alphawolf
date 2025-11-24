# 🐺 AlphaWolf Valuation Methodology

## 🧠 Philosophy: System Dynamics for Capital

**Valuation is simply System Dynamics applied to finance.**

In engineering, you model systems with inputs (energy), resistance (friction), and outputs (work).
In finance, we model **Cash Flow Dynamics**:

*   **Input:** Capital Invested (Equity/Debt).
*   **Output:** Cash Flows (Dividends/FCF).
*   **Resistance:** The Discount Rate ($r$)—the risk/friction that degrades value over time.
*   **Time ($t$):** The duration of the system.

Our edge is **Probabilistic Modeling**. Single-point estimates (e.g., "The price target is $100") are fictions. The future is a probability distribution. We do not predict the future; we **map the probability surface** to find mispriced bets.

---

## 🔁 The AlphaWolf Protocol: 5 Steps to the Kill

To reproduce our valuation rigor, follow this standardized execution loop for every asset.

### Step 1: Calibration (Identify the Prey)
Before modeling, you must classify the asset. The asset's lifecycle determines the mathematical physics we apply.
*   **Action:** Determine the Asset Class (Start-up, Growth, Mature, Distressed).
*   **Output:** Selection of the primary model (The Weapon) from the *Decision Matrix* (see Section 4).

### Step 2: Dissection (Sum-of-the-Parts)
Corporations are rarely monoliths. They are collections of distinct machines.
*   **Action:** Break the company into its constituent engines.
    *   *Example:* A conglomerate = Stable Core (DCF) + High-Growth Venture (Real Option) + Real Estate (NAV).
*   **Principle:** Value each part using the model best suited for its specific physics, then sum them up.

### Step 3: The Engine (Mechanics)
For each part, build the deterministic logic.
*   **Governing Equation (DCF):**
    $$ \text{Value} = \sum_{t=1}^{n} \frac{\text{FCF}_t}{(1 + r)^t} + \frac{\text{Terminal Value}}{(1 + r)^n} $$
*   **Variables:**
    *   **FCF:** Distributable cash (EBIT - Tax + D&A - CapEx - Working Cap).
    *   **Discount Rate ($r$):** The hurdle rate (Risk-Free Rate + Beta * Equity Risk Premium).
    *   **Terminal Value:** The "Forever" value (Exit Multiple or Gordon Growth).

### Step 4: The Thousand Paths (Simulation)
We never use single numbers for uncertain inputs. We use **Probability Distributions**.
*   **Action:** Replace key assumptions (Growth, Margins, Multiples) with distributions (Triangular, Normal, Uniform).
*   **Execution:** Run 50,000+ Monte Carlo simulations.
*   **Result:** A histogram of outcomes, not a single price target.

### Step 5: Synthesis (The Kill)
Translate the math into a tradeable signal.
*   **Bear Case (P10):** The floor. If we buy here, it's hard to lose.
*   **Base Case (P50):** The median outcome.
*   **Bull Case (P90):** The blue-sky potential.
*   **Signal:** Compare P50 to Current Price. If $P50 > Price + Margin of Safety$, we hunt.

---

## 🛠️ The Arsenal: Models & Methods

We employ four primary "Weapons" depending on the target's nature.

### 1. The Standard DCF (The Time Machine)
*   **Use Case:** Mature, predictable companies (Phase 3).
*   **Mechanism:** Forecast 5-10 years of cash flows, discount them back.
*   **Key inputs:** WACC, Stable Growth Rate.

### 2. The Target/Shortcut DCF (The Sniper)
*   **Use Case:** Catalyst-driven stocks or "Story" stocks with a clear medium-term target (Phase 2).
*   **Mechanism:** Ignore the noisy short-term. Value the company at a specific future date (e.g., Year 3) based on management targets/capacity, then discount that *single* future value back to today.
*   **Formula:** $PV = \frac{\text{EBITDA}_{target} \times \text{Multiple}}{(1+r)^t}$
*   **Why:** Avoids "false precision" of modeling the messy ramp-up phase.

### 3. Real Options (The Quantum Bet)
*   **Use Case:** Pre-revenue, Biotech, Exploration Mining, "Moonshots" (Phase 1).
*   **Mechanism:** Binary outcomes. The asset is worth \$0 (Failure) or \$X Billion (Success).
*   **Formula:** $\text{Value} = (\text{Payoff} \times P_{success}) + (0 \times P_{fail})$.
*   **Why:** Averages lie. If a drug has a 10% chance of making \$10B, a DCF averaging that to \$1B is misleading. It's a binary option.

### 4. Relative Valuation (The Mirror)
*   **Use Case:** Sanity check for all models.
*   **Mechanism:** Compare Multiples (PE, EV/EBITDA, EV/Sales) to peers.
*   **Principle:** Intrinsic value (DCF) is what it *should* be worth. Relative value is what the market *is paying* for similar assets. The gap is the Alpha.

---

## 🎲 Distribution Dynamics

How to translate "feelings" into code (numpy distributions):

| Narrative Conviction | Distribution | Code |
| :--- | :--- | :--- |
| **"Management Guidance"** | **Triangular** | `np.random.triangular(low, mode, high)` |
| **"Natural Volatility"** | **Normal** | `np.random.normal(mean, std_dev)` |
| **"Total Uncertainty"** | **Uniform** | `np.random.uniform(low, high)` |
| **"Regime Change"** | **Binomial/Choice** | `np.random.choice([A, B], p=[0.7, 0.3])` |
| **"Fat Tails / Black Swans"** | **Lognormal** | `np.random.lognormal(mean, sigma)` |

---

## 🧭 The Decision Matrix: Damodaran's Map

Always align the model with the asset's lifecycle phase.

| Lifecycle Phase | Characteristics | Primary Weapon | Key Levers |
| :--- | :--- | :--- | :--- |
| **Phase 1: Start-up** | No Revenue, High Cash Burn, "Idea" | **Real Options** | TAM, Prob(Success) |
| **Phase 2: Growth** | High Revenue Growth, Negative Profit | **Target DCF (10Y)** | Rev Growth, Target Margin |
| **Phase 3: Mature** | Steady Growth (GDP+), Profitable | **Standard DCF** | WACC, Reinvestment |
| **Phase 4: Decline** | Falling Rev, High Debt, Distress | **Liquidation / Distressed DCF** | Asset Value, Burn Rate |
| **Special: Banks** | Money is the inventory | **Dividend Discount (DDM)** | ROE, Book Value |
| **Special: Resources** | Finite Life, Commodity Price risk | **NAV (Net Asset Value)** | Commodity Price, Reserves |
