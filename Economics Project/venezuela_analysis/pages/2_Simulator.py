import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import get_venezuela_simulation_data

# 1. Page Configuration
st.set_page_config(page_title="Economic Simulator", layout="wide")

def main():
    st.title("Economic Resilience Simulator")
    st.markdown("Testing the impact of policy and institutions on the Venezuelan 'U-Turn'.")

    # Load the specific Venezuelan simulation benchmarks
    gdp_index = get_venezuela_simulation_data()

    # Create Tabs for Interactivity and Academic Depth
    tab_sim, tab_math = st.tabs(["Run Simulation", "Formulaic Insights"])

    with tab_sim:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.header("Policy Parameters")
            # Meritocracy slider based on PDVSA professionalization research
            inst_quality = st.slider("Institutional Quality (0=Fragile, 1=Robust)", 0.0, 1.0, 0.25)
            # Global oil price shock
            oil_price = st.slider("Global Oil Price ($/bbl)", 20, 150, 70)
            # Social spending vs. Investment
            savings_rate = st.slider("Sovereign Fund Savings Rate (%)", 0, 80, 5)

        # --- SIMULATION LOGIC ---
        # Stability is a function of price tempered by institutional capacity
        # We use a non-linear formula to show how low institutions (I < 0.3) collapse under price shocks
        stability_index = (oil_price * inst_quality) / (1.01 - inst_quality)
        
        # Calculate "Recovery Potential" 
        # (Based on the 80% GDP loss benchmark from your data)
        years_to_recovery = 0
        if inst_quality > 0.5:
            # If institutions are good, calculate years to return to 2013 peak (100 pts)
            growth_rate = (inst_quality * 10) # Max 10% growth
            years_to_recovery = np.log(100 / gdp_index.iloc[-1]['Value']) / np.log(1 + (growth_rate/100))

        with col2:
            st.subheader("Simulated Outcome")
            st.metric("Economic Stability Score", f"{stability_index:.2f}")
            
            if stability_index < 35:
                st.error("🚨 **High Risk of State Collapse.** High correlation with Venezuela's 2014-2020 trajectory.")
            elif stability_index < 65:
                st.warning("⚠️ **Volatile Equilibrium.** Growth is entirely dependent on oil price spikes.")
            else:
                st.success("✅ **Institutional Resilience.** The economy can withstand price crashes (The Norway Model).")

            if years_to_recovery > 0:
                st.info(f"📅 **Recovery Projection:** At current settings, it would take approx. **{years_to_recovery:.1f} years** to return to the 2013 GDP peak.")

    with tab_math:
        st.markdown(r"""
        ### Mathematical Modeling of the Resource Curse
        
        Based on the research paper, the simulator uses the following logic to depict the **Venezuelan Condition**:

        **1. The Institutional Mitigation Factor:**
        We model stability ($S$) as a function of Price ($P$) and Institutional Meritocracy ($I$):
        $$S = \frac{P \times I}{1.01 - I}$$
        *Note: As $I$ approaches 0, the denominator creates a 'Fragility Trap' where no amount of oil wealth can stabilize the state.*

        **2. The Production Decay (Brain Drain):**
        Expected output $O$ is limited by the loss of technical expertise $\phi$:
        $$O_{actual} = O_{potential} \times (1 - \phi)^{t}$$
        *This explains why Venezuela's production fell from 3.4M to 0.4M bbl/d despite having the largest reserves.*
        """)

if __name__ == "__main__":
    main()