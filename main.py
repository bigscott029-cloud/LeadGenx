"""
Main entry point - Lead scraping orchestrator.
"""

import logging
import sys
import csv
from datetime import datetime
from pathlib import Path
import yaml
from typing import List, Dict, Optional

from scrapers.web_scraper import WebScraper
from scrapers.social_scrapers import LinkedInScraper, FacebookScraper, TwitterScraper, InstagramScraper
from utils.validators import DeduplicateManager, DataValidator
from scheduler import ScrapingScheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LeadScrappingEngine:
    """Main lead scraping orchestrator."""
    
    def __init__(self, config_file: str = 'config.yaml'):
        """
        Initialize the scraping engine.
        
        Args:
            config_file: Path to configuration file
        """
        self.config = self._load_config(config_file)
        self.dedup_manager = DeduplicateManager()
        self.scheduler = ScrapingScheduler()
        self.all_leads = []
    
    def _load_config(self, config_file: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_file}")
            return config
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_file}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            sys.exit(1)
    
    def _get_keywords_for_niche(self, niche_name: str) -> List[str]:
        """Get keywords for a specific niche."""
        for niche in self.config.get('niches', []):
            if niche.get('name') == niche_name:
                return niche.get('keywords', [])
        return []
    
    def _get_region_filter(self, regions: Optional[List[str]] = None) -> List[str]:
        """Get configured region filter values."""
        region_filter = regions if regions is not None else self.config.get('region_filter', [])
        if isinstance(region_filter, str):
            region_filter = [region_filter]
        return [region.strip() for region in region_filter if region]

    def _get_default_platforms(self) -> List[str]:
        return [
            platform.strip().lower()
            for platform in self.config.get('bot', {}).get('default_platforms', ['web', 'linkedin', 'facebook', 'twitter', 'instagram'])
        ]

    def scrape_web(self, niche: str = None, regions: List[str] = None, max_urls: int = 10) -> List[Dict]:
        """
        Scrape general websites for leads.
        
        Args:
            niche: Specific niche to target
            regions: Optional list of regions to filter query terms
            max_urls: Maximum result URLs to scrape
            
        Returns:
            List of extracted leads
        """
        logger.info("Starting web scraping...")
        
        scraper = WebScraper(rate_limit=1.0)
        web_leads = []
        try:
            keywords = self._get_keywords_for_niche(niche) if niche else []
            region_terms = self._get_region_filter(regions)
            web_leads = scraper.scrape_search_queries(keywords, region_terms, max_results=max_urls)
            logger.info(f"Found {len(web_leads)} leads from web search")
            return web_leads
        finally:
            scraper.close()

    def scrape_instagram(self, niche: str = None, regions: List[str] = None, max_posts: int = 30) -> List[Dict]:
        """
        Scrape Instagram for leads.
        """
        logger.info("Starting Instagram scraping...")
        scraper = InstagramScraper()
        instagram_leads = []

        try:
            platform_config = next(
                (platform for platform in self.config.get('platforms', []) if platform.get('name') == 'instagram'),
                {}
            )
            hashtags = platform_config.get('hashtags', []) or []
            if niche:
                hashtags.extend(self._get_keywords_for_niche(niche))
            hashtags = list(dict.fromkeys([tag.strip().lstrip('#') for tag in hashtags if tag]))
            region_terms = self._get_region_filter(regions)
            instagram_leads = scraper.search_hashtags(hashtags, regions=region_terms, max_posts=max_posts)
            logger.info(f"Found {len(instagram_leads)} leads from Instagram")
            return instagram_leads
        except Exception as e:
            logger.error(f"Error scraping Instagram: {e}")
            return []
    
    def scrape_linkedin(self) -> List[Dict]:
        """Scrape LinkedIn for leads."""
        logger.info("Starting LinkedIn scraping...")
        
        scraper = LinkedInScraper()
        linkedin_leads = []
        
        try:
            for niche in self.config.get('niches', []):
                keywords = niche.get('keywords', [])
                days = self.config.get('time_filters', {}).get('max_age_days', 7)
                
                posts = scraper.search_posts(keywords, days)
                
                for post in posts:
                    # Extract leads from post
                    leads = scraper.extract_from_post(
                        post.get('text', ''),
                        post.get('url', '')
                    )
                    linkedin_leads.extend(leads)
            
            logger.info(f"Found {len(linkedin_leads)} leads from LinkedIn")
            return linkedin_leads
            
        except Exception as e:
            logger.error(f"Error scraping LinkedIn: {e}")
            return []
    
    def scrape_facebook(self) -> List[Dict]:
        """Scrape Facebook for leads."""
        logger.info("Starting Facebook scraping...")
        
        scraper = FacebookScraper()
        facebook_leads = []
        
        try:
            for niche in self.config.get('niches', []):
                keywords = niche.get('keywords', [])
                days = self.config.get('time_filters', {}).get('max_age_days', 7)
                
                # Search Facebook groups
                group_posts = scraper.search_groups(keywords, days)
                for post in group_posts:
                    leads = scraper.extract_from_post(
                        post.get('text', ''),
                        post.get('url', '')
                    )
                    facebook_leads.extend(leads)
                
                # Search Facebook pages
                page_posts = scraper.search_pages(keywords, days)
                for post in page_posts:
                    leads = scraper.extract_from_post(
                        post.get('text', ''),
                        post.get('url', '')
                    )
                    facebook_leads.extend(leads)
            
            logger.info(f"Found {len(facebook_leads)} leads from Facebook")
            return facebook_leads
            
        except Exception as e:
            logger.error(f"Error scraping Facebook: {e}")
            return []
    
    def scrape_twitter(self) -> List[Dict]:
        """Scrape Twitter for leads."""
        logger.info("Starting Twitter scraping...")
        
        scraper = TwitterScraper()
        twitter_leads = []
        
        try:
            for niche in self.config.get('niches', []):
                keywords = niche.get('keywords', [])
                days = self.config.get('time_filters', {}).get('max_age_days', 7)
                
                tweets = scraper.search_tweets(keywords, days=days)
                
                for tweet in tweets:
                    leads = scraper.extract_from_tweet(
                        tweet.get('text', ''),
                        tweet.get('url', '')
                    )
                    twitter_leads.extend(leads)
            
            logger.info(f"Found {len(twitter_leads)} leads from Twitter")
            return twitter_leads
            
        except Exception as e:
            logger.error(f"Error scraping Twitter: {e}")
            return []
    
    def run_scraping(
        self,
        platforms: List[str] = None,
        niche: str = None,
        regions: List[str] = None,
        max_leads: int = None
    ) -> List[Dict]:
        """
        Run scraping on specified platforms.
        
        Args:
            platforms: List of platforms to scrape
            niche: Niche name to target
            regions: Optional list of regions to filter searches
            max_leads: Optional maximum number of leads to return
            
        Returns:
            List of all extracted leads
        """
        platforms = platforms or self._get_default_platforms()
        platforms = [platform.strip().lower() for platform in platforms if platform]
        all_leads = []
        region_terms = self._get_region_filter(regions)
        limit = max_leads or self.config.get('bot', {}).get('default_amount')

        logger.info(f"Starting scraping on platforms: {platforms}")

        if 'web' in platforms:
            web_limit = self.config.get('output', {}).get('search_limit', 15)
            all_leads.extend(self.scrape_web(niche=niche, regions=region_terms, max_urls=web_limit))

        if 'linkedin' in platforms:
            all_leads.extend(self.scrape_linkedin())

        if 'facebook' in platforms:
            all_leads.extend(self.scrape_facebook())

        if 'twitter' in platforms:
            all_leads.extend(self.scrape_twitter())

        if 'instagram' in platforms:
            instagram_platform = next(
                (platform for platform in self.config.get('platforms', []) if platform.get('name') == 'instagram'),
                {}
            )
            instagram_limit = instagram_platform.get('max_posts', 30)
            all_leads.extend(self.scrape_instagram(niche=niche, regions=region_terms, max_posts=instagram_limit))

        filtered_leads = DataValidator.filter_leads(all_leads, require_email=False)

        if limit is not None:
            filtered_leads = filtered_leads[:limit]

        logger.info(f"Total leads collected: {len(all_leads)}")
        logger.info(f"Leads after filtering: {len(filtered_leads)}")

        self.all_leads = filtered_leads
        return filtered_leads
    
    def save_leads(self, output_filename: str = None) -> str:
        """
        Save extracted leads to CSV.
        
        Args:
            output_filename: Output filename (optional)
            
        Returns:
            Path to saved file
        """
        if not self.all_leads:
            logger.warning("No leads to save")
            return None
        
        # Generate filename if not provided
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"leads_{timestamp}.csv"
        
        # Create data directory if it doesn't exist
        data_dir = self.config.get('output', {}).get('output_dir', 'data')
        Path(data_dir).mkdir(exist_ok=True)
        
        filepath = Path(data_dir) / output_filename
        
        fieldnames = [
            'email',
            'phone',
            'company_name',
            'social_handle',
            'region',
            'source_url',
            'source_platform',
            'post_link',
            'extracted_at',
        ]

        with filepath.open('w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(self.all_leads)

        logger.info(f"Leads saved to: {filepath}")
        
        return str(filepath)
    
    def start_scheduler(self, frequency_hours: int = 24, start_time: str = "08:00") -> None:
        """
        Start the scheduler for periodic runs.
        
        Args:
            frequency_hours: Hours between runs
            start_time: Time to start in HH:MM format
        """
        hour, minute = map(int, start_time.split(':'))
        
        def scraping_job():
            logger.info("Executing scheduled scraping job...")
            leads = self.run_scraping()
            self.save_leads()
            logger.info(f"Scheduled job completed. Found {len(leads)} leads")
        
        self.scheduler.schedule_daily(scraping_job, hour=hour, minute=minute)
        self.scheduler.start()
    
    def stop_scheduler(self) -> None:
        """Stop the scheduler."""
        self.scheduler.stop()


def main():
    """Main entry point."""
    logger.info("Lead Scraping Engine starting...")
    
    # Initialize engine
    engine = LeadScrappingEngine('config.yaml')
    
    # Run scraping on all platforms
    leads = engine.run_scraping()
    
    # Save results
    if leads:
        filepath = engine.save_leads()
        logger.info(f"✓ Successfully saved {len(leads)} leads to {filepath}")
    else:
        logger.warning("⚠ No leads extracted")
    
    logger.info("Lead Scraping Engine completed")


if __name__ == '__main__':
    main()
