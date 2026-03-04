import streamlit as st
import time
import os

# 1. Page Configuration
st.set_page_config(page_title="Venezuela: Oil Reserve, Economic Collapse & Resource-Curse Dynamics", layout="wide")

def main():
    # --- TITLE SECTION ---
    # Centered and Grand Title using HTML
    st.markdown("<h1 style='text-align: center; font-size: 50px;'>THE ANATOMY OF A RESOURCE CURSE</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555;'>Institutional Decay and the Paradox of Plenty in Venezuela</h3>", unsafe_allow_html=True)
    st.divider()

    # --- DYNAMIC REVOLVING GALLERY ---
    if 'slide_idx' not in st.session_state:
        st.session_state.slide_idx = 0

    col_l, col_img, col_r = st.columns([1, 2, 1])
    
    with col_img:
        # Define the two rotating images and captions
        slides = [
            {"img": "assets/venezuela_oil_map.png", "cap": "A volatile State."},
            {"img": "assets/End_pic.png", "cap": "The Social Reality: Institutional Decoupling and Poverty."}
        ]
        
        current = slides[st.session_state.slide_idx % len(slides)]
        
        # Display logic
        if os.path.exists(current["img"]):
            st.image(current["img"], use_container_width=True)
        else:
            st.info(f"IMAGE NOT FOUND: Please place '{current['img']}' in your project folder.")
            
        st.markdown(f"<p style='text-align: center; font-style: italic;'>{current['cap']}</p>", unsafe_allow_html=True)

    # --- EXECUTIVE SUMMARY ---
    st.header("Executive Summary")
    st.write("""
    This research investigates the singular economic collapse of Venezuela, a nation that transitioned from being the 
    wealthiest in Latin America to a state of systemic humanitarian crisis. Unlike traditional market-driven recessions, 
    Venezuela’s trajectory serves as a definitive case study in how the mismanagement of resource windfalls, coupled with 
    the deliberate dismantling of meritocratic institutions, creates a 'Fragility Trap' that is resilient even to high oil prices.
    """)

    # --- RESEARCH QUESTION (The centerpiece) ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; border-top: 2px solid #eee; border-bottom: 2px solid #eee; padding: 40px;'>
            <h1 style='font-weight: bold; font-size: 38px;'>
            "To what extent did the politicization of extractive institutions, rather than global market volatility, 
            drive the decoupling of Venezuela's oil wealth from its national economic stability?"
            </h1>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- HYPOTHESIS ---
    st.info("""
    **Hypothesis:** The Venezuelan collapse was not an inevitable consequence of the 2014 oil price crash, but the 
    predictable outcome of 'Institutional Hollow-out.' We posit that the erosion of technical autonomy within PDVSA 
    and the adoption of pro-cyclical fiscal policies rendered the state incapable of absorbing external shocks.
    """)

    # --- CURRENT RESEARCH ABSTRACT ---
    st.markdown("### 📄 Research Abstract")
    st.write("""
    This study examines the paradox of plenty in Venezuela. Despite possessing over 300 billion barrels of 
    proven reserves, the state has suffered an unprecedented -80% GDP contraction. The research identifies 
    three primary transmission mechanisms: Dutch Disease, Rent-Seeking Behavior, and Institutional Politicization. 
    It argues that institutional quality is the true long-term driver of economic survival in petro-states.
    """)

    st.divider()

    # --- CORE FRAMEWORKS & QUOTES ---
    
    st.markdown("<h2 style='text-align: center;'>Core Theoretical Frameworks</h2>", unsafe_allow_html=True)
    st.divider()

    # I. The Resource Curse
    st.markdown("<h3 style='text-align: center;'>I. The Resource Curse</h3>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; padding: 0px 50px 20px 50px;'>
            <p style='font-style: italic; font-size: 18px; color: #444;'>
                "Resource-abundant economies tend to grow more slowly than resource-scarce economies... 
                the abundance of natural resources leads to short-sightedness among policy-makers."
            </p>
            <p>— <b>Richard Auty (1993)</b></p>
        </div>
    """, unsafe_allow_html=True)



    # II. Dutch Disease Dynamics
    st.markdown("<h3 style='text-align: center;'>II. Dutch Disease Dynamics</h3>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; padding: 0px 50px 20px 50px;'>
            <p style='font-style: italic; font-size: 18px; color: #444;'>
                "A phenomenon whereby a boom in one traded goods sector (oil) squeezes profitability in 
                other traded goods sectors... by placing upward pressure on the exchange rate."
            </p>
            <p>— <b>Corden & Neary (1982)</b></p>
        </div>
    """, unsafe_allow_html=True)



    # III. Institutional Failure
    st.markdown("<h3 style='text-align: center;'>III. Institutional Failure</h3>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; padding: 0px 50px 20px 50px;'>
            <p style='font-style: italic; font-size: 18px; color: #444;'>
                "Extractive economic institutions are designed to extract incomes and wealth from 
                one subset of society to benefit a different subset."
            </p>
            <p>— <b>Acemoglu & Robinson (2012)</b></p>
        </div>
    """, unsafe_allow_html=True)
    

    # LOGIC TO REVOLVE IMAGES (Updated every 10 seconds)
    time.sleep(10)
    st.session_state.slide_idx += 1
    st.rerun()

if __name__ == "__main__":
    main()