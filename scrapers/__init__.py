"""
Scrapers package initialization.
"""

from .web_scraper import WebScraper
from .social_scrapers import LinkedInScraper, FacebookScraper, TwitterScraper, InstagramScraper

__all__ = [
    'WebScraper',
    'LinkedInScraper',
    'FacebookScraper',
    'TwitterScraper',
    'InstagramScraper',
]
