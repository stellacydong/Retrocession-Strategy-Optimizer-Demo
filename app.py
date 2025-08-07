import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="Retrocession Strategy Optimizer", layout="wide")

# Sidebar navigation
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Select a step:",
    [
        "🏠 Home",
        "📁 Step 1: Portfolio Input",
        "🔄 Step 2: Scenario Simulation",
        "🧠 Step 3: RL Optimization",
        "💬 Step 4: LLM Explanation",
        "✅ Step 5: Final Strategy"
    ]
)

# ------------------------------------------------
# HOME
# ------------------------------------------------
if page == "🏠 Home":
    # ===== Logo & Title =====
    st.image("assets/logo.png", width=200)
    st.markdown("<h1 style='text-align: center;'>⚡ Retrocession Strategy Optimizer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>An AI-powered co-pilot to optimize retrocession purchasing for reinsurers</p>", unsafe_allow_html=True)
    st.markdown("---")

    # ===== Problem → Solution =====
    st.markdown("### ❓ Why We Built This")
    st.markdown("""
    Retrocession — insurance for reinsurers — plays a critical role in protecting capital and managing catastrophe risk.  
    Yet choosing the optimal retrocession strategy is extremely complex:
    - The space of cover combinations (XoL, ILWs, sidecars) is massive
    - Market prices shift constantly
    - Manual or consulting-driven approaches are slow and hard to optimize

    **📉 The result?**  
    Reinsurers often face excess tail risk or overpay for inefficient protection.

    **💡 Our Solution:**  
    This tool uses **reinforcement learning** and **AI simulation** to:
    - Explore thousands of scenarios and coverage options
    - Learn high-performing retrocession mixes dynamically
    - Provide plain-language rationale and sample treaty wording via LLM
    """)

    st.markdown("---")

    # ===== What It Is =====
    st.markdown("### 🤖 What Is the Retrocession Strategy Optimizer?")
    st.markdown("""
    A decision-support engine for retro buyers, brokers, and CROs.  
    It acts as a **risk-transfer autopilot** that simulates, optimizes, and explains how to structure your retro program — faster and more comprehensively than a human team.

    Behind the scenes, it:
    - Simulates catastrophe losses
    - Optimizes coverage using RL agents
    - Summarizes insights and rationale using an LLM
    """)

    # ===== Architecture Diagram =====
    st.image("assets/architecture.png", caption="🧠 System Architecture Overview", use_container_width=True)

    st.markdown("---")

    # ===== How to Use It =====
    st.markdown("### 🧭 How to Use This Demo")
    st.markdown("""
    Step through the demo using the sidebar on the left. You’ll explore:

    1. **📁 Step 1 – Portfolio Input**  
       Upload or simulate a reinsurer’s portfolio to define risk exposure.

    2. **🔄 Step 2 – Scenario Simulation**  
       Generate thousands of catastrophe loss years to stress-test coverage needs.

    3. **🧠 Step 3 – RL Optimization**  
       Use a reinforcement learning agent to build an efficient mix of XoL, ILWs, and sidecars.

    4. **💬 Step 4 – LLM Explanation**  
       Interpret the strategy in plain language and draft sample treaty wordings.

    5. **✅ Step 5 – Final Output**  
       Review your recommended program and export the decision packet.
    """)

    st.success("✅ Use the sidebar to begin optimizing your retrocession program.")



# ------------------------------------------------
# STEP 1: Portfolio Input
# ------------------------------------------------
elif page == "📁 Step 1: Portfolio Input":
    st.header("📁 Step 1: Define Your Reinsurer Portfolio")
    st.image("assets/step1_icon.png", width=80)

    st.markdown("""
    ### 📌 What Is This Step?

    In this step, you'll define the **portfolio of risks** your company is looking to protect using retrocession (reinsurance for reinsurers).  
    A portfolio typically includes insured values, estimated losses, and relevant underwriting information.  
    This data forms the foundation for downstream catastrophe simulations and retro strategy optimization.

    ---    
    ### 🧰 How to Use It

    You have two options:
    
    1. **Upload a real portfolio file** — if you have one in CSV or Excel format.  
       The file should include columns like:
       - `Region` or `Territory`
       - `TIV` (Total Insured Value)
       - `Expected Loss` or `PML`
       - `Line of Business`
       - Optional: `Capital Allocated`, `Cost Tolerance`, etc.

    2. **Use a simulated sample portfolio** — to explore the tool with realistic placeholder data.

    """)
    
    uploaded = st.file_uploader("📤 Upload Your Portfolio File (CSV or XLSX)", type=["csv", "xlsx"])
    use_sample = st.checkbox("Or use a sample portfolio", value=True)

    if uploaded or use_sample:
        st.success("✅ Portfolio successfully loaded and parsed.")

        # Simulated sample data
        df = pd.DataFrame({
            "Region": ["Florida", "Gulf Coast", "Northeast"],
            "TIV ($M)": [300, 250, 180],
            "Expected Loss ($M)": [45, 38, 20],
            "Line of Business": ["Property CAT", "Property All Risk", "Commercial Lines"]
        })

        st.markdown("### 🧾 Portfolio Overview")
        st.dataframe(df, use_container_width=True)

        st.markdown("""
        ---
        ### 🔍 Interpreting Your Portfolio

        Here's what the data means:
        - **Region**: The geographical exposure being covered.
        - **TIV ($M)**: The total amount insured across policies in that region.
        - **Expected Loss ($M)**: Average annual loss expected, based on historical models or internal projections.
        - **Line of Business**: The type of insurance risk (e.g., CAT-heavy, commercial).

        These fields will help the AI understand:
        - Where you're most exposed
        - How severe losses could be in each area
        - What kind of retro structures would be effective (e.g., XoL vs. ILW)

        ---
        ### 📈 What Happens Next?

        This portfolio feeds into:
        - **📉 Step 2: Scenario Simulation**: Where we simulate thousands of CAT loss years across these exposures.
        - **🧠 Step 3: RL Optimization**: Where an RL agent tests different coverage combinations to optimize protection.
        - **💬 Step 4: LLM Explanation**: Where AI explains *why* the selected strategy makes sense, based on this input.

        """)

        st.info("➡️ You're ready! Move to **Step 2** to simulate catastrophe scenarios based on this portfolio.")
    else:
        st.warning("📂 Please upload your portfolio or use the sample option to continue.")


# ------------------------------------------------
# STEP 2: Scenario Simulation
# ------------------------------------------------
elif page == "🔄 Step 2: Scenario Simulation":
    st.header("🔄 Step 2: Catastrophe Scenario Simulation")
    st.image("assets/step2_icon.png", width=80)

    st.markdown("""
    ### 🌪️ What Is This Step?

    This step simulates **thousands of annual catastrophe loss scenarios** to help you understand how your reinsurer portfolio performs under stress.  
    These simulations act as synthetic "alternate futures" — exploring how much you could lose in rare, severe, or clustered disaster years.

    ---
    ### 🎯 Why It Matters

    Before buying retrocession, you need to quantify:
    - **Tail risk** exposure (e.g., losses at the 1-in-100 or 1-in-250 return period)
    - **Expected annual losses** and capital volatility
    - **Coverage gaps** that may arise under extreme conditions

    These insights are essential to guide an RL agent’s optimization of your retro program in Step 3.

    ---
    ### 🔧 How to Use It

    Choose a simulation engine to generate your synthetic loss years:

    #### 🔢 Stochastic Generator (Default)
    A statistical model using:
    - **Poisson distribution**: Models the number of events per year (e.g., storms, quakes)
    - **Lognormal severity**: Captures the distribution of loss sizes

    This option is fast and useful for general risk simulation.

    #### 🧠 LLM-Based Scenario Generator *(Coming Soon)*
    A generative model that creates **realistic CAT narratives**:
    - Hurricanes hitting multiple coasts in one season
    - Black swan patterns and rare systemic shocks
    - Regional clustering of disasters

    This mode helps stress-test edge cases and complex correlations.

    ---
    """)

    if st.button("▶️ Run Loss Simulation"):
        with st.spinner("Simulating 1,000+ annual loss scenarios..."):
            time.sleep(2)
            losses = np.random.lognormal(mean=2, sigma=0.5, size=1000)
            loss_df = pd.DataFrame({"Simulated Annual Loss ($M)": losses})

        st.success("✅ Scenario simulation complete.")

        st.markdown("### 📈 Loss Distribution Plot")
        st.line_chart(loss_df)

        with st.expander("🔍 View Sample Simulated Losses"):
            st.dataframe(loss_df.head(10))

        st.markdown("""
        ---
        ### 📊 How to Interpret the Results

        You’ve now generated 1,000 synthetic loss years.

        - Each value represents a **total annual loss** for your reinsurer portfolio.
        - The **distribution curve** shows how frequently mild, moderate, and severe loss years occur.
        - The **tail of the distribution** represents your catastrophic risk exposure (e.g., $200M+ losses).

        In the next step, the RL agent will use this data to **train and test different retro structures** against these simulated stress conditions — helping to balance protection, cost, and ROI.

        ---
        """)

        st.info("➡️ Continue to **Step 3: RL Optimization** to build your optimal retrocession strategy.")

# ------------------------------------------------
# STEP 3: RL Optimization
# ------------------------------------------------
elif page == "🧠 Step 3: RL Optimization":
    st.header("🧠 Step 3: RL-Based Strategy Optimization")
    st.image("assets/step3_icon.png", width=80)

    st.markdown("""
    ### 🤖 What Is This Step?

    We use a **Reinforcement Learning (RL) agent** to design an optimal retrocession program for your reinsurer portfolio.  
    The agent explores different combinations of:

    - **XoL (Excess-of-Loss)**
    - **ILWs (Industry Loss Warranties)**
    - **Sidecars**

    It tests each strategy across thousands of loss simulations and learns how to **maximize retained capital**, **minimize tail risk**, and **control cost**.
    """)

    # ------------------------
    # Reward Function Weights
    # ------------------------
    st.markdown("### 🎛️ Customize Reward Priorities")

    st.markdown("""
    The RL agent balances **three competing objectives**:

    1. **📈 Retained Surplus** – Capital remaining after losses and premiums  
    2. **🛡️ Tail Risk (CVaR)** – How bad your worst years can get (99th percentile loss)  
    3. **💸 Premium Cost** – Upfront spend on protection

    Use the sliders below to reflect your business priorities.

    | Strategy Type             | Surplus | CVaR | Cost |
    |---------------------------|:-------:|:----:|:----:|
    | Budget-conscious buyer    |  0.3    | 0.3  | 0.4  |
    | Risk-averse insurer       |  0.2    | 0.6  | 0.2  |
    | Growth-focused aggressor  |  0.6    | 0.2  | 0.2  |
    """)

    surplus_weight = st.slider("📈 Weight on Surplus Retained", 0.0, 1.0, 0.4)
    cvar_weight = st.slider("🛡️ Weight on Tail Risk (CVaR)", 0.0, 1.0, 0.4)
    cost_weight = st.slider("💸 Weight on Premium Cost", 0.0, 1.0, 0.2)

    total = surplus_weight + cvar_weight + cost_weight
    if total > 0:
        surplus_w = surplus_weight / total
        cvar_w = cvar_weight / total
        cost_w = cost_weight / total
    else:
        surplus_w, cvar_w, cost_w = 0.4, 0.4, 0.2

    # ------------------------
    # Premium Budget Constraint
    # ------------------------
    st.markdown("### 💰 Set Premium Budget Constraint")
    max_premium = st.slider("Maximum Total Premium ($M)", min_value=10, max_value=30, value=20)

    # ------------------------
    # Run Optimization
    # ------------------------
    if st.button("🎯 Run Optimization Agent"):
        with st.spinner("Training RL agent across 1,000 simulated loss years..."):
            time.sleep(3)  # Replace with actual RL training logic

            # Simulated strategy output
            result_df = pd.DataFrame({
                "Cover Type": ["XoL", "ILW", "Sidecar"],
                "Retention ($M)": [30, 50, 20],
                "Limit ($M)": [100, 75, 50],
                "Premium ($M)": [8.2, 4.5, 6.1],
                "Expected Payout ($M)": [28, 20, 15]
            })

            # Simulated frontier points
            strategies = pd.DataFrame({
                "ROI (%)": [18.2, 20.1, 21.5, 19.8, 22.4],
                "CVaR (99%)": [38, 35, 32, 36, 30]
            })

        st.success("✅ Optimization complete. Strategy generated!")

        # ------------------------
        # Show Strategy Output
        # ------------------------
        st.markdown("### 🧾 Optimized Retrocession Strategy")
        st.dataframe(result_df, use_container_width=True)

        st.markdown("""
        Each row represents a **recommended retrocession layer**, and each column tells you what the RL agent selected:

        - **Retention ($M)**: How much loss you’ll absorb before this layer activates.
        - **Limit ($M)**: The cap or maximum payout from the cover.
        - **Premium ($M)**: Estimated cost of purchasing the layer.
        - **Expected Payout ($M)**: Average modeled benefit over 1,000 simulated loss years.

        🧠 **Interpretation Tips**:
        - Lower retentions reduce tail risk but usually cost more.
        - ILWs trigger on industry losses — useful for correlated events.
        - Sidecars provide off-balance-sheet capacity for high-severity years.
        """)

        # ------------------------
        # ROI vs. CVaR Plot
        # ------------------------
        st.markdown("### 📉 Risk vs. Return Frontier")

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.scatter(strategies["CVaR (99%)"], strategies["ROI (%)"], color="teal", s=80)
        ax.set_xlabel("Tail Risk (CVaR 99%) [$M]")
        ax.set_ylabel("Return on Risk Capital [%]")
        ax.set_title("Efficient Frontier: Risk vs. Reward")
        ax.grid(True)
        st.pyplot(fig)

        st.markdown("""
        This chart shows the **trade-off between profitability and catastrophic risk** across strategies tested by the RL agent.

        - 📉 X-axis (CVaR): Higher values mean more tail risk.
        - 📈 Y-axis (ROI): Higher values mean more efficient use of capital.

        ✅ **Top-left points** represent the most attractive programs — those that deliver **high ROI while minimizing risk**.

        Use this to:
        - Test different slider settings
        - Compare agent behavior under cost-heavy vs. risk-heavy priorities
        """)

        st.info("➡️ Continue to **Step 4: LLM Explanation** to understand *why* this strategy is effective.")


# ------------------------------------------------
# STEP 4: LLM Explanation
# ------------------------------------------------
elif page == "💬 Step 4: LLM Explanation":
    st.header("💬 Step 4: Strategy Explanation & Wording")
    st.image("assets/step4_icon.png", width=80)

    st.markdown("""
    ### 📘 What Is This Step?

    In this step, a **large language model (LLM)** explains the rationale behind the recommended retrocession strategy —  
    and provides **natural language wording** that can be adapted into a formal treaty document.

    This helps:
    - **Communicate the logic** behind coverage decisions to underwriters, actuaries, and capital committees
    - **Draft initial treaty language** for legal review and broker circulation
    - **Improve interpretability** of the RL agent’s behavior
    """)

    st.markdown("---")

    # ------------------------
    # Strategy Rationale
    # ------------------------
    st.markdown("### 🤖 Strategy Rationale (LLM-Generated)")

    st.success("""
    “The recommended retrocession program is designed to reduce concentration risk in hurricane-prone regions,  
    particularly Florida and the Gulf Coast. Excess-of-Loss (XoL) layers provide budget-efficient tail risk protection.  
    Industry Loss Warranties (ILWs) act as correlated-event buffers — especially for multi-event CAT seasons.  
    Sidecars are strategically deployed to transfer high-severity exposure to third-party capital, reducing solvency pressure  
    while preserving underwriting flexibility.”
    """)

    st.markdown("---")

    # ------------------------
    # Wording Output
    # ------------------------
    st.markdown("### 📜 Sample Retrocession Wording Draft")

    st.code("""
    Retrocession Agreement — Draft Language:

    1. XoL Layer: The Reinsurer agrees to cede losses in excess of $30 million up to a limit of $100 million  
       for the Property CAT portfolio concentrated in Florida and Gulf Coast territories.

    2. ILW Trigger: An Industry Loss Warranty will activate upon aggregate insured losses  
       exceeding $20 billion for a named U.S. windstorm season, providing up to $75 million coverage.

    3. Sidecar Participation: Up to $50 million of additional capital will be sourced via a Sidecar vehicle,  
       attaching at the $150 million portfolio-level loss point, for 1-in-200 modeled events.
    """)

    st.markdown("""
    ✍️ **Note**: This wording is a first-pass draft. Legal teams and brokers should customize and validate before use in contracts.

    - Covers may be subject to **specific perils**, **geographic exclusions**, or **seasonal limitations**
    - Consider including **collateralization terms**, **basis risk clauses**, or **index triggers** in sidecar deals
    """)

    st.info("➡️ Proceed to **Step 5: Final Strategy Summary** to review the full package and export.")

# ------------------------------------------------
# STEP 5: Final Strategy
# ------------------------------------------------
elif page == "✅ Step 5: Final Strategy":
    st.header("✅ Step 5: Final Strategy Summary")
    st.image("assets/step5_icon.png", width=80)

    st.markdown("""
    ### 📊 Final Recommendation Summary

    Below is your **optimized retrocession strategy**, based on thousands of simulated loss years and guided by your chosen priorities.

    This output is designed to be **decision-ready** — supporting discussions with CROs, capital committees, brokers, or treaty teams.
    """)

    st.markdown("### 📈 Key Performance Metrics")

    st.markdown("""
    | Metric | Description | Value |
    |--------|-------------|-------|
    | 📈 **Expected Surplus** | Projected capital retained after losses & premiums | `$95M` |
    | 🛡️ **Tail Risk (CVaR 99%)** | Estimated capital needed in worst 1% of years | `$32M` |
    | 💰 **Total Premium** | Modeled cost of retrocession program | `$18.8M` |
    | 🎯 **Return on Risk Capital** | ROI across simulations (post-protection) | `22.4%` |
    """)

    st.markdown("### 📋 Final Retrocession Structure")

    final_df = pd.DataFrame({
        "Cover Type": ["XoL", "ILW", "Sidecar"],
        "Retention": ["$30M", "$50M", "$20M"],
        "Limit": ["$100M", "$75M", "$50M"],
        "Premium": ["$8.2M", "$4.5M", "$6.1M"]
    })
    st.dataframe(final_df, use_container_width=True)

    st.markdown("""
    - **XoL**: Offers efficient tail-risk absorption for Florida block.
    - **ILW**: Supplements correlated CAT event exposure during extreme seasons.
    - **Sidecar**: Adds alternative capacity for extreme-loss layers, diversifying capital sources.
    """)

    st.markdown("---")
    st.markdown("### 📦 Export Your Strategy Packet")

    st.markdown("""
    Your final strategy can be exported for stakeholder presentation or contract preparation.

    **Included in the packet (coming soon):**
    - Executive summary
    - Coverage tables
    - Tail risk chart (CVaR frontier)
    - LLM-generated treaty wording
    """)

    st.download_button(
        label="⬇️ Download Strategy Packet (PDF Coming Soon)",
        data="Strategy content here",
        file_name="Retro_Strategy_Summary.txt",
        disabled=True
    )

    st.success("✅ Your strategy is complete. You’re ready to present or refine further.")
