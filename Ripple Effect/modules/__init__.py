# modules/__init__.py

# We use absolute imports (referencing the folder name)
from modules.rss_client import fetch_rss_news
from modules.processor import analyze_sentiment
from modules.correlation import find_correlations

# This tells Python which functions are 'public'
__all__ = ["fetch_rss_news", "analyze_sentiment", "find_correlations"]