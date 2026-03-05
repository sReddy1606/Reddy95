from gnews import GNews

def fetch_rss_news(keyword, period='7d'):
    """
    Fetches news from Google News RSS.
    Returns an empty list if no results are found or if the connection fails.
    """
    try:
        # Initialize GNews with a specific period (e.g., '1d' or '7d')
        google_news = GNews(language='en', country='US', period=period, max_results=20)
        
        # Get news based on the keyword
        results = google_news.get_news(keyword)
        
        # Safety check: ensure we always return a list
        if results is None:
            return []
        return results
    except Exception as e:
        # Prints error to terminal for debugging, but keeps the app running
        print(f"RSS Fetch Error for {keyword}: {e}")
        return []