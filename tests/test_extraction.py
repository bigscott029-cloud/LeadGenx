"""
Unit tests for lead extraction and validation.
"""

import pytest
from utils.lead_extractor import LeadExtractor, LeadNormalizer
from utils.validators import DataValidator, DeduplicateManager


class TestLeadExtractor:
    """Test lead extraction functionality."""
    
    def test_extract_emails(self):
        """Test email extraction."""
        text = "Contact us at info@example.com or sales@company.org"
        emails = LeadExtractor.extract_emails(text)
        
        assert len(emails) == 2
        assert 'info@example.com' in [e.lower() for e in emails]
        assert 'sales@company.org' in [e.lower() for e in emails]
    
    def test_extract_invalid_emails(self):
        """Test that invalid emails are filtered."""
        text = "Contact noreply@example.com or invalid@"
        emails = LeadExtractor.extract_emails(text)
        
        assert 'noreply@example.com' not in [e.lower() for e in emails]
        assert len([e for e in emails if '@' in e]) == len(emails)
    
    def test_extract_phones(self):
        """Test phone number extraction."""
        text = "Call us at (555) 123-4567 or +1-800-555-1234"
        phones = LeadExtractor.extract_phones(text)
        
        assert len(phones) >= 1
        assert any('555' in phone for phone in phones)
    
    def test_extract_company_names(self):
        """Test company name extraction."""
        text = "We are Google Inc and Apple Corporation, both tech companies"
        companies = LeadExtractor.extract_company_names(text)
        
        assert len(companies) >= 1
    
    def test_extract_from_html(self):
        """Test extraction from HTML."""
        html = "<p>Email: test@example.com</p><p>Phone: 555-1234567</p>"
        result = LeadExtractor.extract_from_html(html)
        
        assert 'emails' in result
        assert 'phones' in result
        assert 'companies' in result


class TestLeadNormalizer:
    """Test lead normalization."""
    
    def test_normalize_phone(self):
        """Test phone normalization."""
        phone = "(555) 123-4567"
        normalized = LeadNormalizer.normalize_phone(phone)
        
        assert '+1' in normalized or '555' in normalized
    
    def test_normalize_email(self):
        """Test email normalization."""
        email = "INFO@EXAMPLE.COM"
        normalized = LeadNormalizer.normalize_email(email)
        
        assert normalized == 'info@example.com'


class TestDataValidator:
    """Test data validation."""
    
    def test_is_valid_email(self):
        """Test email validation."""
        assert DataValidator.is_valid_email('test@example.com') == True
        assert DataValidator.is_valid_email('invalid-email') == False
        assert DataValidator.is_valid_email('') == False
    
    def test_is_valid_phone(self):
        """Test phone validation."""
        assert DataValidator.is_valid_phone('(555) 123-4567') == True
        assert DataValidator.is_valid_phone('555') == False
        assert DataValidator.is_valid_phone('') == False
    
    def test_is_valid_company_name(self):
        """Test company name validation."""
        assert DataValidator.is_valid_company_name('Apple Inc') == True
        assert DataValidator.is_valid_company_name('click here') == False
        assert DataValidator.is_valid_company_name('') == False
    
    def test_is_spam_lead(self):
        """Test spam detection."""
        assert DataValidator.is_spam_lead('test@viagra.com') == True
        assert DataValidator.is_spam_lead('info@example.com') == False


class TestDeduplicateManager:
    """Test deduplication."""
    
    def test_add_and_check_duplicate(self):
        """Test duplicate detection."""
        manager = DeduplicateManager()
        
        # First entry should not be duplicate
        assert manager.is_duplicate(email='test@example.com') == False
        
        # Same email should be duplicate
        assert manager.is_duplicate(email='test@example.com') == True
    
    def test_multiple_fields(self):
        """Test deduplication with multiple fields."""
        manager = DeduplicateManager()
        
        # First entry
        assert manager.is_duplicate(email='test@example.com', phone='5551234567') == False
        
        # Different email, same phone
        assert manager.is_duplicate(email='other@example.com', phone='5551234567') == True


class TestIntegration:
    """Integration tests."""
    
    def test_extract_and_validate_lead(self):
        """Test extracting and validating a lead."""
        text = "Contact John at john@example.com or call (555) 987-6543 at ABC Corp"
        
        emails = LeadExtractor.extract_emails(text)
        phones = LeadExtractor.extract_phones(text)
        
        assert len(emails) > 0
        assert len(phones) > 0
        
        # Validate
        for email in emails:
            assert DataValidator.is_valid_email(email)
        
        for phone in phones:
            assert DataValidator.is_valid_phone(phone)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
