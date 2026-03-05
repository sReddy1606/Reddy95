# Ripple Effect: Causal News Tracker

A feasibility prototype designed to investigate the relationship between current news events (The Effect) and historical news context (The Inception). This tool uses **NLP (Natural Language Processing)** and **Vector Similarity** to identify potential causal links.

## The Core Theory
The project operates on the hypothesis that news events do not happen in isolation. By analyzing today's headlines against a 7-day historical window using **TF-IDF vectorization**, we can mathematically quantify the "relevance" of past events to current triggers.

---

## Features
- **Real-Time Extraction:** Fetches live news data using the Google News RSS feed (no API key required).
- **Sentiment Analysis:** Utilizes the **VADER** algorithm to score the emotional tone of headlines.
- **Causal Drill-Down:** Allows users to select a "Trigger" headline and trace its origins.
- **Correlation Engine:** Uses **Scikit-Learn** to calculate the Cosine Similarity between past and present news fingerprints.

---

## Project Structure
```text
Ripple_Effect/
├── app.py                  # Streamlit Frontend & State Management
├── requirements.txt        # Python Dependencies
├── Dockerfile              # Containerization Blueprint
├── .dockerignore           # Build Optimization
└── modules/                # Core Logic Package
    ├── __init__.py         # Package Handshake
    ├── rss_client.py       # News Data Layer
    ├── processor.py        # Sentiment Logic
    └── correlation.py      # TF-IDF Similarity Math