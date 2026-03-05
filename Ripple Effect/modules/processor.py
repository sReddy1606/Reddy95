from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER Sentiment tool
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Calculates if a headline is Positive, Negative, or Neutral.
    """
    if not text:
        return {"label": "Neutral", "score": 0.0}
        
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
        
    return {"label": label, "score": round(compound, 2)}