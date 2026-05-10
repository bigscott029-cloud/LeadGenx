"""
Validators module - Data validation utilities.
"""

import re
from typing import Dict, List


class DataValidator:
    """Validate extracted lead data."""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Check if email format is valid."""
        if not email:
            return False
        
        # Simple email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Check if phone number format is valid."""
        if not phone:
            return False
        
        # Remove non-digits
        digits = re.sub(r'\D', '', phone)
        
        # Valid if has 10+ digits
        return len(digits) >= 10
    
    @staticmethod
    def is_valid_company_name(company: str) -> bool:
        """Check if company name is valid."""
        if not company or len(company) < 2:
            return False
        
        # Check for common invalid patterns
        invalid_patterns = ['click here', 'contact', 'email', 'phone', 'address']
        company_lower = company.lower()
        
        if any(pattern in company_lower for pattern in invalid_patterns):
            return False
        
        return True
    
    @staticmethod
    def is_spam_lead(email: str = None, company: str = None) -> bool:
        """Detect potential spam leads."""
        spam_keywords = [
            'viagra', 'casino', 'lottery', 'bitcoin', 'crypto', 'forex',
            'dating', 'adult', 'xxx', 'spam', 'test', 'example'
        ]
        
        text = (email or '') + ' ' + (company or '')
        text_lower = text.lower()
        
        for keyword in spam_keywords:
            if keyword in text_lower:
                return True
        
        return False
    
    @staticmethod
    def validate_lead_object(lead: Dict) -> Dict[str, bool]:
        """
        Validate all fields in a lead object.
        
        Returns:
            Dictionary with validation results for each field
        """
        return {
            'email_valid': DataValidator.is_valid_email(lead.get('email', '')),
            'phone_valid': DataValidator.is_valid_phone(lead.get('phone', '')),
            'company_valid': DataValidator.is_valid_company_name(lead.get('company_name', '')),
            'is_spam': DataValidator.is_spam_lead(
                lead.get('email', ''),
                lead.get('company_name', '')
            ),
        }
    
    @staticmethod
    def filter_leads(leads: List[Dict], require_email: bool = False) -> List[Dict]:
        """
        Filter out invalid leads.
        
        Args:
            leads: List of lead dictionaries
            require_email: If True, only keep leads with valid emails
            
        Returns:
            Filtered list of valid leads
        """
        valid_leads = []
        
        for lead in leads:
            # Skip spam
            if DataValidator.is_spam_lead(lead.get('email'), lead.get('company_name')):
                continue
            
            # Check minimum requirements
            has_email = DataValidator.is_valid_email(lead.get('email', ''))
            has_phone = DataValidator.is_valid_phone(lead.get('phone', ''))
            has_company = DataValidator.is_valid_company_name(lead.get('company_name', ''))
            has_handle = bool(lead.get('social_handle', '').strip())
            
            if require_email:
                if has_email:
                    valid_leads.append(lead)
            else:
                if has_email or has_phone or has_company or has_handle:
                    valid_leads.append(lead)
        
        return valid_leads


class DeduplicateManager:
    """Manage lead deduplication."""
    
    def __init__(self):
        """Initialize deduplication manager."""
        self.seen = set()
    
    def add_fingerprint(self, email: str = '', phone: str = '', company: str = '') -> str:
        """
        Create a fingerprint for a lead.
        
        Args:
            email: Email address
            phone: Phone number
            company: Company name
            
        Returns:
            Fingerprint string
        """
        # Use email as primary key, then phone, then company
        key = email.lower().strip() if email else ''
        key = key or (phone if phone else '')
        key = key or (company.lower().strip() if company else '')
        
        return key
    
    def is_duplicate(self, email: str = '', phone: str = '', company: str = '') -> bool:
        """
        Check if a lead is a duplicate.
        
        Returns:
            True if duplicate, False otherwise
        """
        fingerprint = self.add_fingerprint(email, phone, company)
        
        if not fingerprint:
            return False
        
        if fingerprint in self.seen:
            return True
        
        self.seen.add(fingerprint)
        return False
    
    def clear(self) -> None:
        """Clear the deduplication cache."""
        self.seen.clear()
    
    def get_count(self) -> int:
        """Get count of unique leads seen."""
        return len(self.seen)
