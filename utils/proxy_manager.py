"""
Proxy manager module - Manage and rotate proxies.
"""

import logging
import requests
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class ProxyManager:
    """Manage proxy pools and rotation."""
    
    FREE_PROXY_SOURCES = [
        'https://www.free-proxy-list.net/',
        'https://free-proxy-list.com/',
    ]
    
    def __init__(self):
        """Initialize proxy manager."""
        self.proxies: List[str] = []
        self.current_index = 0
        self.failed_proxies: set = set()
    
    def fetch_free_proxies(self, source_url: str = None) -> List[str]:
        """
        Fetch free proxies from online sources.
        
        Args:
            source_url: Optional specific source URL
            
        Returns:
            List of proxy addresses
        """
        proxies = []
        
        try:
            # Note: This is a placeholder. Free proxy scraping requires
            # parsing HTML from proxy list websites.
            # In production, use libraries like:
            # - proxy-requests
            # - httpx with proxies
            # - Or maintain your own proxy list
            
            logger.warning("Free proxy fetching not implemented - use your own proxies")
            
        except Exception as e:
            logger.error(f"Error fetching free proxies: {e}")
        
        return proxies
    
    def add_proxy(self, proxy: str) -> None:
        """Add a proxy to the pool."""
        if proxy not in self.proxies and proxy not in self.failed_proxies:
            self.proxies.append(proxy)
            logger.info(f"Added proxy: {proxy}")
    
    def add_proxies(self, proxies: List[str]) -> None:
        """Add multiple proxies to the pool."""
        for proxy in proxies:
            self.add_proxy(proxy)
    
    def remove_proxy(self, proxy: str) -> None:
        """Remove a proxy from the pool."""
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            logger.info(f"Removed proxy: {proxy}")
    
    def mark_failed(self, proxy: str) -> None:
        """Mark a proxy as failed."""
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            self.failed_proxies.add(proxy)
            logger.warning(f"Marked proxy as failed: {proxy}")
    
    def get_next_proxy(self) -> Optional[str]:
        """Get next proxy in rotation."""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index % len(self.proxies)]
        self.current_index += 1
        
        return proxy
    
    def get_proxy_dict(self) -> Dict[str, str]:
        """Get proxy dictionary for requests library."""
        proxy = self.get_next_proxy()
        
        if not proxy:
            return {}
        
        return {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}',
        }
    
    def reset(self) -> None:
        """Reset proxy manager."""
        self.proxies.clear()
        self.failed_proxies.clear()
        self.current_index = 0
        logger.info("Proxy manager reset")
    
    def get_stats(self) -> Dict:
        """Get proxy pool statistics."""
        return {
            'total_proxies': len(self.proxies),
            'failed_proxies': len(self.failed_proxies),
            'current_index': self.current_index,
        }
