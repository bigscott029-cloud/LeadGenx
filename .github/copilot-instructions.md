# Lead Generation Engine - Project Instructions

## Project Overview
This is a Python-based lead scraping system designed to extract leads (emails, phone numbers, company names) from websites and social media platforms using free, open-source tools.

## Technology Stack
- **Language**: Python 3.9+
- **Core Libraries**: Scrapy, Selenium, BeautifulSoup
- **Data Processing**: Pandas
- **Scheduling**: APScheduler
- **Social Media Scrapers**: linkedin-scraper, facebook-scraper, snscrape

## Project Structure
```
Lead Gen Engine/
├── scrapers/              # Web and social media scrapers
│   ├── __init__.py
│   ├── web_scraper.py     # Scrapy-based web scraper
│   └── social_scrapers.py # LinkedIn, Facebook, Twitter scrapers
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── lead_extractor.py  # Email/phone/company extraction
│   ├── human_behavior.py  # Anti-detection mechanisms
│   ├── proxy_manager.py   # Proxy rotation
│   └── validators.py      # Data validation
├── tests/                 # Unit and integration tests
├── data/                  # Output CSV files and history
├── config.yaml            # Main configuration file
├── main.py                # Entry point
├── scheduler.py           # Scheduling logic
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
```

## Development Guidelines
- Use type hints in function signatures
- Add docstrings to all classes and functions
- Handle exceptions gracefully with logging
- Implement retry logic for network failures
- Maintain human-like behavior to avoid detection
- Log all scraping activities for compliance

## Testing
- Unit tests for lead extraction functions
- Integration tests for scrapers
- Validation of CSV output
- Performance testing on sample data

## Execution
1. Install dependencies: `pip install -r requirements.txt`
2. Update configuration in `config.yaml` as needed
3. Run the system: `python main.py`
4. Check output in `data/` directory

## Compliance Notes
- Respect robots.txt and platform ToS
- Implement reasonable delays between requests
- Log all activities
- Do not bypass authentication mechanisms
- Stop scraping if rate-limited or blocked
