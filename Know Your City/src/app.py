import streamlit as st
import pandas as pd
import yaml
from processor import TwitterProcessor

st.set_page_config(page_title="Twitter Scraper V2", layout="wide")

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

st.title("🎓 Master's Project: Twitter Scraper V2")
st.markdown("Modernized interface for legacy data collection.")

# Sidebar Config
st.sidebar.header("Configuration")
settings_file = st.sidebar.file_uploader("Upload settings.yaml", type=['yaml', 'yml'])

if settings_file:
    config = yaml.safe_load(settings_file)
    processor = TwitterProcessor(config)
    
    query_input = st.text_input("Enter Queries (comma separated)", "science, tech")
    pages = st.slider("Max Pages", 1, 10, 1)

    if st.button("Run Scraper"):
        queries = [q.strip() for q in query_input.split(',')]
        all_data = []
        
        progress = st.progress(0)
        for idx, q in enumerate(queries):
            st.write(f"Collecting: {q}...")
            # Using the Processor from processor.py
            data = processor.run_query(q, max_pages=pages)
            all_data.extend(data)
            progress.progress((idx + 1) / len(queries))

        if all_data:
            df = pd.DataFrame(all_data)
            st.success("Scrape Complete!")
            st.dataframe(df)
            
            # CSV Download (Maintains CSV requirement)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "results.csv", "text/csv")
else:
    st.info("Please upload your settings.yaml in the sidebar to begin.")