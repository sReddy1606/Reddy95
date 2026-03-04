import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
# Importing the specialized functions from your separate data_loader
from utils.data_loader import (
    fetch_venezuela_macro, 
    fetch_poverty_history, 
    get_oil_production_history, 
    get_global_comparison_data
)

# 1. Page Setup
st.set_page_config(
    page_title="Venezuela: Economic Trajectory",
    page_icon="🇻🇪",
    layout="wide"
)

def main():
    st.title("Venezuela: The Anatomy of a Resource Curse")
    st.markdown("Analyzing the impact of institutional decay on the world's largest oil reserves.")
    st.divider()

    # 2. Fetching the Data
    # This keeps the dashboard.py file clean and readable
    macro_df = fetch_venezuela_macro()
    poverty_df = fetch_poverty_history()
    oil_hist_df = get_oil_production_history()
    global_oil_df = get_global_comparison_data()

    # 3. Organizing the UI into Tabs
    tab1, tab2, tab3 = st.tabs(["📉 The Paradox", "🛢️ Oil Production", "🏚️ Poverty Analysis"])

    # --- TAB 1: Macroeconomic Paradox ---
    with tab1:
        st.subheader("GDP Decay vs. Inflationary Pressure")
        if not macro_df.empty:
            fig = go.Figure()
            # Primary Axis: GDP
            fig.add_trace(go.Scatter(x=macro_df.index, y=macro_df['GDP_Per_Capita'], 
                                   name="GDP/Capita (USD)", line=dict(color='blue', width=3)))
            # Secondary Axis: Inflation
            fig.add_trace(go.Scatter(x=macro_df.index, y=macro_df['Inflation_Rate'], 
                                   name="Inflation (%)", yaxis="y2", line=dict(color='red', dash='dot')))
            
            fig.update_layout(
                yaxis=dict(title="GDP per Capita (USD)"),
                yaxis2=dict(title="Inflation %", overlaying="y", side="right"),
                template="plotly_white",
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Could not load macroeconomic data from World Bank API.")

   # --- TAB 2: OIL PRODUCTION & RESERVES ---
    with tab2:
        st.header("🛢️ Oil Sector: The Efficiency Gap")
        
        # --- 1. GLOBAL COMPARISON (Reserves vs. Daily Output) ---
        st.subheader("Proven Reserves vs. Actual Extraction (2024)")
        # data_loader.get_global_comparison_data() provides the 2024/25 OPEC stats
        global_oil_df = get_global_comparison_data()
        
        fig_comp = go.Figure()

        # Bar Chart for the "Wealth" (Reserves)
        fig_comp.add_trace(go.Bar(
            x=global_oil_df['Country'], 
            y=global_oil_df['Reserves_Billion_Bbl'],
            name='Proven Reserves (Billion Barrels)', 
            marker_color='#DAA520' # Gold color to represent "potential wealth"
        ))

        # Line Chart for the "Reality" (Daily Production)
        fig_comp.add_trace(go.Scatter(
            x=global_oil_df['Country'], 
            y=global_oil_df['Production_MBPD'],
            name='Daily Production (Million BPD)', 
            yaxis="y2", 
            mode='lines+markers+text', 
            text=global_oil_df['Production_MBPD'],
            textposition="top center", 
            line=dict(color='red', width=3) # Red line to represent "actual output"
        ))
        
        fig_comp.update_layout(
            yaxis=dict(title="Proven Reserves (Billion Bbl)"),
            yaxis2=dict(title="Daily Production (Million BPD)", overlaying="y", side="right"),
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified"
        )
        st.plotly_chart(fig_comp, use_container_width=True)
        st.caption("**Thesis Point:** Despite holding ~6x more oil than the USA, Venezuela produces less than 5% of the US daily volume.")

        st.divider()

        # --- 2. HISTORICAL TIMELINE (1920-2024) ---
        st.subheader("A Century of Production Milestones")
        # data_loader.get_oil_production_history() provides labeled year-by-year data
        oil_hist_df = get_oil_production_history()
        
        fig_hist = px.line(
            oil_hist_df, 
            x='Year', 
            y='Production', 
            markers=True, 
            text='Label', # This adds the specific historical event names directly to the graph
            labels={'Production': 'Million Barrels Per Day'},
            title="Historical Production Peaks and Collapses"
        )
        
        fig_hist.update_traces(
            textposition="top left", 
            line=dict(width=3, color='#333333')
        )
        fig_hist.update_layout(template="plotly_white")
        st.plotly_chart(fig_hist, use_container_width=True)

    # --- TAB 3: Poverty Analysis ---
    with tab3:
        st.subheader("The Century-Long Poverty U-Turn")
        fig_pov = px.line(poverty_df, x='Year', y='Poverty_Rate', text='Context', markers=True)
        fig_pov.update_traces(textposition="top center", line=dict(color='orange', width=4))
        fig_pov.update_layout(yaxis_title="Poverty Rate (%)", template="plotly_white")
        st.plotly_chart(fig_pov, use_container_width=True)

if __name__ == "__main__":
    main()