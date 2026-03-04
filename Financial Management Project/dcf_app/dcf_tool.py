import streamlit as st
import pandas as pd
import numpy as np

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================
st.set_page_config(page_title="Excelsoft DCF Valuation", layout="wide")

# ==========================================================
# SIDEBAR - GLOBAL ASSUMPTIONS
# ==========================================================
# We place high-level economic variables in the sidebar so the user
# can perform sensitivity analysis by toggling these at any time.
st.sidebar.header("📋 Master Inputs")

# Macro-economic & Market Inputs
rf = st.sidebar.number_input("Risk-free rate (Rf)", value=0.065, format="%.4f", help="Typically the yield on 10-year Govt Bonds.")
rm = st.sidebar.number_input("Market risk rate (Rm)", value=0.135, format="%.4f", help="Expected return of the market index.")
corp_tax = st.sidebar.slider("Corporate Tax Rate (%)", 0, 100, 25) / 100

# Terminal & Share Data
terminal_g = st.sidebar.slider("Terminal Growth (g) %", 0.0, 8.0, 6.0) / 100
shares_outstanding = st.sidebar.number_input("Shares Outstanding (Millions)", value=115.0842)

# ==========================================================
# DATA PREPARATION & CALCULATIONS
# ==========================================================

# --- 1. BETA CALCULATION ---
# We use peer company betas to find an 'Unlevered Beta' (Business Risk),
# then relever it based on Excelsoft's specific capital structure.
peer_data = [
    {'Company': 'MPS Ltd', 'Levered Beta': 0.54, 'D/E': 0.0206},
    {'Company': 'Ksolves India Limited', 'Levered Beta': 1.03, 'D/E': 0.0753},
    {'Company': 'Silver Touch Technologies Ltd', 'Levered Beta': 0.78, 'D/E': 0.2340},
    {'Company': 'Sasken Technologies Ltd', 'Levered Beta': 0.85, 'D/E': 0.0320},
    {'Company': 'InfoBeans Technologies Ltd', 'Levered Beta': 0.92, 'D/E': 0.0410},
    {'Company': 'Zensar Technologies Limited', 'Levered Beta': 1.15, 'D/E': 0.0285},
    {'Company': 'Sonata Software Limited', 'Levered Beta': 1.21, 'D/E': 0.4210},
    {'Company': 'Happiest Minds Technologies', 'Levered Beta': 1.08, 'D/E': 0.2830},
    {'Company': 'Coforge Limited', 'Levered Beta': 1.32, 'D/E': 0.1120},
    {'Company': 'Affle India', 'Levered Beta': 0.32, 'D/E': 0.0118},
    {'Company': 'Newgen Software', 'Levered Beta': 0.51, 'D/E': 0.0325}
]
df_peers = pd.DataFrame(peer_data)

# Hamada Formula for Unlevering: Bu = Bl / (1 + (1-T)*(D/E))
df_peers['Unlevered Beta'] = df_peers['Levered Beta'] / (1 + (1 - corp_tax) * df_peers['D/E'])
avg_unlevered_beta = df_peers['Unlevered Beta'].mean()

# Relevering: Bl = Bul*[(1 + (1-T)*(Target D/E))]
target_de = 0.05
levered_beta_usecase =avg_unlevered_beta*(1 + (1 - corp_tax) * target_de)

# --- 2. COST OF EQUITY & DEBT ---
# Cost of Equity via Capital Asset Pricing Model (CAPM)
re = rf + levered_beta_usecase * (rm - rf)

# Cost of Debt: Calculating interest burden over total debt obligations
total_debt = 62.77 + 265.89 + 22.64 # Sum of Non-current and Current liabilities
net_interest = 137.45 - 45.7
rd = net_interest / total_debt if total_debt > 0 else 0

# --- 3. WACC CALCULATION ---
# Using the specific derivation: E = 20D implies Weights are 20/21 (Equity) and 1/21 (Debt)
wacc = (20/21) * re + (1/21) * rd * (1 - corp_tax)

# --- 4. CASH FLOW ENGINE ---
# Calculating the Free Cash Flow to the Firm (FCFF) for the base year
revenue, op_cost, da = 2488.0, 1846.85, 98.64075
ebit = revenue - op_cost - da
ebitda=732.57
nwc_delta = 222.59 - 179.72 # Change in Net Working Capital
capex = -140.07
prov_delta = 305.65 - 315.52 # Change in Provisions

# FCFF = EBIT(1-T) + DA - Capex - Change in NWC
fcf_pre_tax = (ebit + da) - nwc_delta - capex - prov_delta
adapted_taxes = ebit * corp_tax
fcf_after_tax = fcf_pre_tax - adapted_taxes

# --- 5. MULTI-STAGE DCF PROJECTION ---
# Projecting 6 years of cash flows using explicit growth rates
g_rates = [0.18,0.16,0.14,0.11,0.08,0.06]
t_g=0.06
projected_fcfs = []
dcf_values = []
curr_fcf = fcf_after_tax

for i, g in enumerate(g_rates):
    if i<5:
        curr_fcf *= (1 + g) # Compounding growth
        projected_fcfs.append(curr_fcf)
        # Present Value = FCF / (1 + WACC)^t
        dcf_values.append(curr_fcf / (1 + wacc)**(i+1))
    elif i==5:
        curr_fcf *=(1+t_g) #terminal growth
        projected_fcfs.append(curr_fcf)
        # Present Value = FCF / (1 + WACC)^t
        dcf_values.append(0)
    

# --- 6. TERMINAL VALUE ---
# Gordon Growth Method: TV = [FCF_n * (1+g)] / (WACC - g)
sum_dcf = sum(dcf_values)
terminal_val = projected_fcfs[-1] / (wacc - terminal_g) if (wacc - terminal_g) != 0 else 0
discounted_tv = terminal_val / (1 + wacc)**6

# --- 7. FINAL VALUATION BRIDGE ---
total_debt_book_value=181.79
ev = sum_dcf + discounted_tv
equity_value = ev - total_debt_book_value
intrinsic_value = equity_value / shares_outstanding

# ==========================================================
# USER INTERFACE - TABS
# ==========================================================
st.title("Technologies Valuation Dashboard")

# Creating the 6-Tab Navigation Structure
t1, t2, t3, t4, t5, t6 = st.tabs([
    "Beta Calc", "Re & Rd", "WACC", "Entity Model", "Terminal Value", "Price Per Share"
])

# --- TAB 1: BETA ---
with t1:
    st.subheader("Step 1: Unlevering & Relevering Beta")
    st.markdown("We determine Excelsoft's Beta by looking at comparable software firms.")
    st.table(df_peers.style.format(precision=4))
    
    c1, c2 = st.columns(2)
    c1.metric("Avg Unlevered Beta (Bu)", round(avg_unlevered_beta, 4))
    c2.metric("Target Levered Beta (β)", round(levered_beta_usecase, 4))
    
    st.latex(r"\beta_{Unlevered} = \frac{\beta_{Levered}}{1 + (1 - T) \times (D/E)}")
    st.info(f"Target D/E: {target_de} | Relevered for financial risk.")

# --- TAB 2: RE & RD ---
with t2:
    st.subheader("Step 2: Cost of Equity & Debt")
    col_re, col_rd = st.columns(2)
    with col_re:
        st.write("**CAPM (Cost of Equity)**")
        st.latex(r"R_e = R_f + \beta(R_m - R_f)")
        st.metric("Re", f"{round(re*100, 2)}%")
    with col_rd:
        st.write("**Cost of Debt (Pre-Tax)**")
        st.latex(r"R_d = \frac{Net Interest}{Total Debt}")
        st.metric("Rd", f"{round(rd*100, 2)}%")
    
    st.write("**Detailed Debt Components (FY25)**")
    st.table(pd.DataFrame({
        "Interest Component": ["Interest Income","Interest paid","Combined Total"],
        "Value": [137.45,-45.7,net_interest]
    }))
    st.table(pd.DataFrame({
        "Debt Component": ["Borrowings-Non-current liabilities ","Lease liabilities-Non-current liabilities ", "Borrowings-current liabilities ", "Lease liabilities-current liabilities ", "Combined Total"],
        "Value": [0,62.77, 265.89, 22.64, total_debt]
    }))

# --- TAB 3: WACC ---
with t3:
    st.subheader("Step 3: Weighted Average Cost of Capital")
    st.markdown("Based on the target capital structure $E = 20D$.")
    st.latex(r"WACC = \left(\frac{E}{V} \times R_e\right) + \left(\frac{D}{V} \times R_d \times (1 - T_c)\right)")
    st.metric("Calculated WACC", f"{round(wacc*100, 2)}%")

# --- TAB 4: ENTITY MODEL ---
with t4:
    st.subheader("Step 4: Cash Flow Build-up (Base Year)")
    cf_data = {
        "Metric": ["EBIT", "D&A", "EBITDA", "Change in NWC", "CAPEX", "Change in Provisions", "Pre-Tax FCF", "Taxes", "FCFF (After-Tax)"],
        "Value": [ebit, da, ebitda, nwc_delta, capex, prov_delta, fcf_pre_tax, adapted_taxes, fcf_after_tax]
    }
    st.table(pd.DataFrame(cf_data).style.format({"Value": "{:,.2f}"}))

# --- TAB 5: TERMINAL VALUE ---
with t5:
    st.subheader("Step 5: 6-Year Projection & Terminal Value")
    proj_df = pd.DataFrame({
        "Year": [f"Year {i}" for i in range(1,7)],
        "Growth Rate": [f"{round(g*100, 0)}%" for g in g_rates],
        "FCFF": projected_fcfs,
        "Discounted CF (PV)": dcf_values
    })
    st.table(proj_df.style.format({"FCFF": "{:,.2f}", "Discounted CF (PV)": "{:,.2f}"}))
    
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Sum of PVs (Stage 1)", f"{round(sum_dcf, 2)}")
    c2.metric("Terminal Value (Stage 2)", f"{round(terminal_val, 2)}")
    c3.metric("PV of Terminal Value", f"{round(discounted_tv, 2)}")

# --- TAB 6: PRICE PER SHARE ---
with t6:
    st.subheader("Step 6: Equity Valuation & Price")
    # Enterprise Value (EV) = PV of Stage 1 + PV of Terminal Value
    final_results = {
        "Valuation Component": ["Enterprise Value (NPV)", "(-) Total Net Debt", "(=) Equity Value", "(÷) Shares Outstanding", "Intrinsic Value Per Share"],
        "Amount": [f"{round(ev, 2)}",f"{round(total_debt, 2)}" ,f"{round(equity_value, 2)}" , shares_outstanding, f"₹ {round(intrinsic_value, 2)}"]
    }
    st.table(pd.DataFrame(final_results))
    
    st.success(f"### The estimated intrinsic value is ₹ {round(intrinsic_value, 2)} per share.")