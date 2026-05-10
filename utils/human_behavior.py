"""
Human behavior module - Implement anti-detection mechanisms.
"""

import random
import time
from typing import List
import logging

logger = logging.getLogger(__name__)


class HumanBehavior:
    """Implement human-like behavior to avoid detection."""
    
    # Common browser user agents
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    ]
    
    # Common referrers
    REFERRERS = [
        'https://www.google.com/',
        'https://www.bing.com/',
        'https://duckduckgo.com/',
        'https://www.linkedin.com/',
        'https://www.facebook.com/',
        'https://twitter.com/',
        'https://www.reddit.com/',
    ]
    
    @staticmethod
    def random_delay(min_seconds: float = 2, max_seconds: float = 8) -> None:
        """
        Add random delay between requests to mimic human behavior.
        
        Args:
            min_seconds: Minimum delay in seconds
            max_seconds: Maximum delay in seconds
        """
        delay = random.uniform(min_seconds, max_seconds)
        logger.debug(f"Waiting {delay:.2f} seconds before next request...")
        time.sleep(delay)
    
    @staticmethod
    def get_random_user_agent() -> str:
        """Get a random user agent string."""
        return random.choice(HumanBehavior.USER_AGENTS)
    
    @staticmethod
    def get_random_referrer() -> str:
        """Get a random referrer."""
        return random.choice(HumanBehavior.REFERRERS)
    
    @staticmethod
    def get_headers() -> dict:
        """Get headers that mimic a real browser."""
        return {
            'User-Agent': HumanBehavior.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': HumanBehavior.get_random_referrer(),
        }
    
    @staticmethod
    def scroll_pause() -> None:
        """Simulate human scrolling pause."""
        pause_time = random.uniform(0.5, 2.0)
        time.sleep(pause_time)
    
    @staticmethod
    def typing_pause() -> None:
        """Simulate human typing pause."""
        pause_time = random.uniform(0.1, 0.3)
        time.sleep(pause_time)
    
    @staticmethod
    def random_click_delay() -> None:
        """Simulate delay before clicking."""
        delay = random.uniform(0.3, 1.5)
        time.sleep(delay)


class ProxyRotator:
    """Manage proxy rotation."""
    
    # Free proxy sources (user can add their own)
    FREE_PROXIES = [
        # Note: These are placeholders. In production, fetch from free proxy lists
        # Examples: free-proxy-list.net, proxy-list.download, etc.
    ]
    
    def __init__(self, proxies: List[str] = None):
        """
        Initialize proxy rotator.
        
        Args:
            proxies: List of proxy URLs to rotate through
        """
        self.proxies = proxies or self.FREE_PROXIES
        self.current_index = 0
    
    def get_next_proxy(self) -> dict:
        """
        Get next proxy in rotation.
        
        Returns:
            Dictionary with proxy configuration for requests library
        """
        if not self.proxies:
            return {}
        
        proxy = self.proxies[self.current_index % len(self.proxies)]
        self.current_index += 1
        
        logger.debug(f"Using proxy: {proxy}")
        
        return {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}',
        }
    
    def add_proxy(self, proxy: str) -> None:
        """Add a proxy to the rotation."""
        if proxy not in self.proxies:
            self.proxies.append(proxy)
            logger.info(f"Added proxy: {proxy}")
    
    def remove_proxy(self, proxy: str) -> None:
        """Remove a proxy from rotation."""
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            logger.warning(f"Removed proxy: {proxy}")
    
    def get_all_proxies(self) -> List[str]:
        """Get list of all proxies."""
        return self.proxies.copy()


class RateLimiter:
    """Rate limiting to avoid overwhelming servers."""
    
    def __init__(self, requests_per_second: float = 1.0):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_second: Number of requests allowed per second
        """
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0
    
    def wait_if_needed(self) -> None:
        """Wait if necessary to maintain rate limit."""
        now = time.time()
        time_since_last = now - self.last_request_time
        
        if time_since_last < self.min_interval:
            wait_time = self.min_interval - time_since_last
            logger.debug(f"Rate limiting: waiting {wait_time:.2f} seconds")
            time.sleep(wait_time)
        
        self.last_request_time = time.time()
