from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_correlations(target_item, history_list):
    """
    Compares today's news against historical news to find causal links.
    Returns the top 10 matches.
    """
    if not history_list or len(history_list) < 2:
        return []

    # Combine title and description for better matching
    target_text = f"{target_item['title']} {target_item.get('description', '')}"
    pool_texts = [f"{item['title']} {item.get('description', '')}" for item in history_list]

    # Create TF-IDF vectors (ignores common words like 'the', 'and')
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([target_text] + pool_texts)
    
    # Calculate similarity scores
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    results = []
    for i, score in enumerate(scores):
        # Ignore exact matches (score > 0.98) and unrelated noise (score < 0.1)
        if 0.1 < score < 0.98:
            results.append({
                "title": history_list[i]['title'],
                "date": history_list[i]['published date'],
                "score": round(float(score) * 100, 1)
            })
            
    # Sort by highest relevance and take top 10
    return sorted(results, key=lambda x: x['score'], reverse=True)[:10]