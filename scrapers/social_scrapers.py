"""
Social media scrapers module - Scrape LinkedIn, Facebook, Twitter for leads.
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class LinkedInScraper:
    """Scrape LinkedIn for leads (public data only)."""
    
    def __init__(self):
        """Initialize LinkedIn scraper."""
        logger.warning("LinkedIn scraper - Note: Scraping LinkedIn requires careful handling of ToS")
    
    def search_posts(self, keywords: List[str], days: int = 7) -> List[Dict]:
        """
        Search LinkedIn posts by keywords.
        
        Args:
            keywords: List of keywords to search
            days: Number of days back to search
            
        Returns:
            List of posts with extracted leads
        """
        # Placeholder for LinkedIn scraping
        # In production, use linkedin-scraper or LinkedIn API (requires credentials)
        logger.info(f"Searching LinkedIn for keywords: {keywords}")
        return []
    
    def extract_from_post(self, post_text: str, post_url: str) -> List[Dict]:
        """
        Extract leads from a LinkedIn post.
        
        Args:
            post_text: Post text content
            post_url: URL to the post
            
        Returns:
            List of extracted leads
        """
        from utils.lead_extractor import LeadExtractor, LeadNormalizer
        from utils.validators import DataValidator
        
        leads = []
        extractor = LeadExtractor()
        
        emails = extractor.extract_emails(post_text)
        phones = extractor.extract_phones(post_text)
        companies = extractor.extract_company_names(post_text)
        
        for email in set(emails):
            if DataValidator.is_valid_email(email):
                lead = {
                    'email': email,
                    'phone': '',
                    'company_name': '',
                    'source_url': post_url,
                    'source_platform': 'linkedin',
                    'post_link': post_url,
                    'extracted_at': datetime.now().isoformat(),
                }
                lead = LeadNormalizer.normalize_lead(lead)
                leads.append(lead)
        
        for phone in set(phones):
            if DataValidator.is_valid_phone(phone):
                lead = {
                    'email': '',
                    'phone': phone,
                    'company_name': '',
                    'source_url': post_url,
                    'source_platform': 'linkedin',
                    'post_link': post_url,
                    'extracted_at': datetime.now().isoformat(),
                }
                lead = LeadNormalizer.normalize_lead(lead)
                leads.append(lead)
        
        return leads


class FacebookScraper:
    """Scrape Facebook for leads (public data only)."""
    
    def __init__(self):
        """Initialize Facebook scraper."""
        logger.warning("Facebook scraper - Note: Scraping Facebook requires careful handling of ToS")
    
    def search_groups(self, keywords: List[str], days: int = 7) -> List[Dict]:
        """
        Search Facebook groups for leads.
        
        Args:
            keywords: List of keywords to search
            days: Number of days back to search
            
        Returns:
            List of posts with extracted leads
        """
        # Placeholder for Facebook group scraping
        logger.info(f"Searching Facebook groups for keywords: {keywords}")
        return []
    
    def search_pages(self, keywords: List[str], days: int = 7) -> List[Dict]:
        """
        Search Facebook pages for leads.
        
        Args:
            keywords: List of keywords to search
            days: Number of days back to search
            
        Returns:
            List of posts with extracted leads
        """
        # Placeholder for Facebook page scraping
        logger.info(f"Searching Facebook pages for keywords: {keywords}")
        return []
    
    def extract_from_post(self, post_text: str, post_url: str) -> List[Dict]:
        """
        Extract leads from a Facebook post.
        
        Args:
            post_text: Post text content
            post_url: URL to the post
            
        Returns:
            List of extracted leads
        """
        from utils.lead_extractor import LeadExtractor, LeadNormalizer
        from utils.validators import DataValidator
        
        leads = []
        extractor = LeadExtractor()
        
        emails = extractor.extract_emails(post_text)
        phones = extractor.extract_phones(post_text)
        
        for email in set(emails):
            if DataValidator.is_valid_email(email):
                lead = {
                    'email': email,
                    'phone': '',
                    'company_name': '',
                    'source_url': post_url,
                    'source_platform': 'facebook',
                    'post_link': post_url,
                    'extracted_at': datetime.now().isoformat(),
                }
                lead = LeadNormalizer.normalize_lead(lead)
                leads.append(lead)
        
        for phone in set(phones):
            if DataValidator.is_valid_phone(phone):
                lead = {
                    'email': '',
                    'phone': phone,
                    'company_name': '',
                    'source_url': post_url,
                    'source_platform': 'facebook',
                    'post_link': post_url,
                    'extracted_at': datetime.now().isoformat(),
                }
                lead = LeadNormalizer.normalize_lead(lead)
                leads.append(lead)
        
        return leads


class TwitterScraper:
    """Scrape Twitter/X for leads."""
    
    def __init__(self):
        """Initialize Twitter scraper."""
        logger.info("Twitter/X scraper initialized")
    
    def search_tweets(self, keywords: List[str], hashtags: List[str] = None, days: int = 7) -> List[Dict]:
        """
        Search Twitter for leads.
        
        Args:
            keywords: List of keywords to search
            hashtags: List of hashtags to search (e.g., #hiring)
            days: Number of days back to search
            
        Returns:
            List of tweets with extracted leads
        """
        # Placeholder for Twitter scraping
        # In production, use snscrape or Twitter API v2 (free tier available)
        logger.info(f"Searching Twitter for keywords: {keywords}, hashtags: {hashtags}")
        return []
    
    def extract_from_tweet(self, tweet_text: str, tweet_url: str) -> List[Dict]:
        """
        Extract leads from a tweet.
        
        Args:
            tweet_text: Tweet text content
            tweet_url: URL to the tweet
            
        Returns:
            List of extracted leads
        """
        from utils.lead_extractor import LeadExtractor, LeadNormalizer
        from utils.validators import DataValidator
        
        leads = []
        extractor = LeadExtractor()
        
        emails = extractor.extract_emails(tweet_text)
        phones = extractor.extract_phones(tweet_text)
        
        for email in set(emails):
            if DataValidator.is_valid_email(email):
                lead = {
                    'email': email,
                    'phone': '',
                    'company_name': '',
                    'source_url': tweet_url,
                    'source_platform': 'twitter',
                    'post_link': tweet_url,
                    'extracted_at': datetime.now().isoformat(),
                }
                lead = LeadNormalizer.normalize_lead(lead)
                leads.append(lead)
        
        for phone in set(phones):
            if DataValidator.is_valid_phone(phone):
                lead = {
                    'email': '',
                    'phone': phone,
                    'company_name': '',
                    'source_url': tweet_url,
                    'source_platform': 'twitter',
                    'post_link': tweet_url,
                    'extracted_at': datetime.now().isoformat(),
                }
                lead = LeadNormalizer.normalize_lead(lead)
                leads.append(lead)
        
        return leads


class InstagramScraper:
    """Scrape Instagram posts for leads using hashtag search."""

    def __init__(self):
        """Initialize Instagram scraper."""
        logger.info("Instagram scraper initialized")
        try:
            from instaloader import Instaloader
            self.loader = Instaloader(
                download_pictures=False,
                download_videos=False,
                save_metadata=False,
                compress_json=False,
                quiet=True,
            )
        except ImportError:
            self.loader = None
            logger.warning("Instaloader is not installed; Instagram scraping will be disabled.")

    def search_hashtags(self, hashtags: List[str], regions: List[str] = None, max_posts: int = 30) -> List[Dict]:
        """
        Search Instagram hashtags and extract leads.

        Args:
            hashtags: List of hashtags to search
            regions: Optional region filters to match in captions or locations
            max_posts: Maximum number of posts to scan per hashtag

        Returns:
            Extracted leads from Instagram posts
        """
        if not self.loader or not hashtags:
            return []

        leads = []
        from instaloader import Hashtag

        for hashtag in hashtags:
            try:
                tag = Hashtag.from_name(self.loader.context, hashtag.lstrip('#'))
                for index, post in enumerate(tag.get_posts()):
                    if index >= max_posts:
                        break

                    caption = post.caption or ''
                    owner_handle = getattr(post, 'owner_username', '') or ''
                    location_name = ''
                    if getattr(post, 'location', None):
                        location = post.location
                        location_name = getattr(location, 'name', '') if location else ''

                    region_text = ' '.join([caption, owner_handle, location_name]).lower()
                    if regions:
                        if not any(region.lower() in region_text for region in regions):
                            continue

                    post_url = f"https://www.instagram.com/p/{post.shortcode}/"
                    leads.extend(self.extract_from_post(
                        caption,
                        post_url,
                        social_handle=owner_handle,
                        region=', '.join(regions) if regions else ''
                    ))
            except Exception as e:
                logger.error(f"Error searching Instagram hashtag '{hashtag}': {e}")

        return leads

    def extract_from_post(
        self,
        post_text: str,
        post_url: str,
        social_handle: str = '',
        region: str = ''
    ) -> List[Dict]:
        """
        Extract leads from Instagram post content.

        Args:
            post_text: Post caption text
            post_url: URL to the post
            social_handle: Instagram username for the post
            region: Region tag or filter

        Returns:
            List of lead dictionaries
        """
        from utils.lead_extractor import LeadExtractor, LeadNormalizer
        from utils.validators import DataValidator

        leads = []
        extractor = LeadExtractor()
        emails = extractor.extract_emails(post_text)
        phones = extractor.extract_phones(post_text)
        companies = extractor.extract_company_names(post_text)

        for email in set(emails):
            if DataValidator.is_valid_email(email):
                lead = {
                    'email': email,
                    'phone': '',
                    'company_name': '',
                    'social_handle': social_handle,
                    'region': region,
                    'source_url': post_url,
                    'source_platform': 'instagram',
                    'post_link': post_url,
                    'extracted_at': datetime.now().isoformat(),
                }
                leads.append(LeadNormalizer.normalize_lead(lead))

        for phone in set(phones):
            if DataValidator.is_valid_phone(phone):
                lead = {
                    'email': '',
                    'phone': phone,
                    'company_name': '',
                    'social_handle': social_handle,
                    'region': region,
                    'source_url': post_url,
                    'source_platform': 'instagram',
                    'post_link': post_url,
                    'extracted_at': datetime.now().isoformat(),
                }
                leads.append(LeadNormalizer.normalize_lead(lead))

        for company in set(companies):
            if DataValidator.is_valid_company_name(company):
                lead = {
                    'email': '',
                    'phone': '',
                    'company_name': company,
                    'social_handle': social_handle,
                    'region': region,
                    'source_url': post_url,
                    'source_platform': 'instagram',
                    'post_link': post_url,
                    'extracted_at': datetime.now().isoformat(),
                }
                leads.append(LeadNormalizer.normalize_lead(lead))

        if not (emails or phones or companies) and social_handle:
            lead = {
                'email': '',
                'phone': '',
                'company_name': '',
                'social_handle': social_handle,
                'region': region,
                'source_url': post_url,
                'source_platform': 'instagram',
                'post_link': post_url,
                'extracted_at': datetime.now().isoformat(),
            }
            leads.append(LeadNormalizer.normalize_lead(lead))

        return leads
