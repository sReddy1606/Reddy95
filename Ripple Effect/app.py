import streamlit as st
# Direct imports from the files to avoid circular dependency
from modules.rss_client import fetch_rss_news
from modules.processor import analyze_sentiment
from modules.correlation import find_correlations

st.set_page_config(page_title="Ripple Effect Tracker", layout="wide")

# Session State to handle page navigation
if 'view' not in st.session_state:
    st.session_state.view = 'list'
if 'selected_news' not in st.session_state:
    st.session_state.selected_news = None

# --- VIEW 1: TODAY'S NEWS ---
if st.session_state.view == 'list':
    st.title("Today's News Pulse")
    query = st.text_input("Enter Topic to Scan:", "Global Economy")
    
    if query:
        with st.spinner("Scanning today's headlines..."):
            today_news = fetch_rss_news(query, period='1d')
            
            if not today_news:
                st.warning("No recent news found. Try a broader keyword.")
            else:
                for idx, news in enumerate(today_news):
                    sent = analyze_sentiment(news['title'])
                    color = "green" if sent['label'] == "Positive" else "red" if sent['label'] == "Negative" else "gray"
                    
                    col1, col2, col3 = st.columns([6, 2, 2])
                    with col1:
                        st.markdown(f"**{news['title']}**")
                    with col2:
                        st.markdown(f":{color}[{sent['label']} ({sent['score']})]")
                    with col3:
                        if st.button("Trace Origins 🔍", key=f"btn_{idx}"):
                            st.session_state.selected_news = news
                            st.session_state.view = 'details'
                            st.rerun() # Refresh to show details page
                    st.divider()

# --- VIEW 2: CAUSAL DRILL-DOWN ---
elif st.session_state.view == 'details':
    target = st.session_state.selected_news
    
    if st.button("⬅️ Back to List"):
        st.session_state.view = 'list'
        st.rerun()

    st.header("Causal Investigation")
    st.info(f"**Target News:** {target['title']}")
    
    with st.spinner("Finding historical influencers (Last 7 Days)..."):
        # We search using a few keywords from the title to find related history
        history_query = " ".join(target['title'].split()[:3])
        history_pool = fetch_rss_news(history_query, period='7d')
        
        links = find_correlations(target, history_pool)
        
        if not links:
            st.write("No strong historical correlations found.")
        else:
            for item in links:
                c1, c2 = st.columns([8, 2])
                with c1:
                    st.write(f"**{item['title']}**")
                    st.caption(f"Date: {item['date']}")
                with c2:
                    st.metric("Relevance", f"{item['score']}%")
                st.divider()