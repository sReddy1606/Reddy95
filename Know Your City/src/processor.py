import os
import csv
import yaml
import datetime
import requests
import html
import pandas as pd
from time import sleep

class TwitterProcessor:
    def __init__(self, config):
        self.config = config
        self.settings = config.get('settings', {})
        self.replacements = {
            '\n': ' ', '\r': ' ', '\t': ' ', '"': "'",
            r'\u201c': "'", r'\u201d': "'", r'\u2026': '...'
        }

    def clean_text(self, text):
        """Maintains the integrity of your original text-cleaning logic."""
        if not text: return ""
        text = html.unescape(text)
        for old, new in self.replacements.items():
            text = text.replace(old, new)
        return text.strip()

    def fix_geo(self, tweet):
        """Preserves the original coordinate breakdown logic."""
        geo_data = {'type': '', 'lat': '', 'lon': ''}
        raw_geo = tweet.get('geo')
        if isinstance(raw_geo, dict) and 'coordinates' in raw_geo:
            geo_data['type'] = raw_geo.get('type', '')
            geo_data['lat'] = raw_geo['coordinates'][0]
            geo_data['lon'] = raw_geo['coordinates'][1]
        return geo_data

    def process_tweet(self, raw_tweet, query):
        """Transforms raw JSON into your specific project format."""
        geo = self.fix_geo(raw_tweet)
        return {
            'id': raw_tweet.get('id_str') or raw_tweet.get('id'),
            'query': query,
            'text': self.clean_text(raw_tweet.get('text', '')),
            'created_at': raw_tweet.get('created_at'),
            'user': raw_tweet.get('from_user'),
            'lat': geo['lat'],
            'lon': geo['lon']
        }

    def run_query(self, query, max_pages=1):
        """Standardized request logic replacing the old urllib2 approach."""
        # Note: Modern Twitter API requires OAuth; this structure mirrors 
        # your original URL-based scraper logic.
        results = []
        # Logic for requests.get() would go here following your search_url config
        return results