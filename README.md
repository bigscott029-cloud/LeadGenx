# Lead Generation Engine

A Python-based lead scraping system for extracting contact information from websites and social media platforms using free, open-source tools.

## Features

✨ **Multi-Source Scraping**
- General websites (Scrapy, BeautifulSoup)
- LinkedIn (public data)
- Facebook (public groups and pages)
- Twitter/X (public tweets)
- Instagram (public hashtag and caption scanning)

📊 **Lead Extraction**
- Email addresses with validation
- Phone numbers (multiple formats)
- Company names
- Contact forms and links
- Social media profiles

🎯 **Targeting Options**
- Keyword-based filtering (tech startups, HVAC services, web development, etc.)
- Niche-specific search terms
- Region-based search targeting for session-level focus
- Time-based filtering (recent posts within specified days)
- Multiple geographic and industry options

🔒 **Anti-Detection Features**
- Random delays between requests
- User agent rotation
- Proxy rotation support (free proxy integration)
- Rate limiting to avoid overwhelming servers
- Human-like browsing patterns

💾 **Data Management**
- CSV export format
- Automatic deduplication by email/phone/company
- Lead validation and filtering
- Historical tracking of extracted leads
- Structured output with metadata

⏰ **Scheduling**
- Daily, hourly, or interval-based runs
- APScheduler integration for automated execution
- Configurable start times and frequencies

📋 **Comprehensive Configuration**
- YAML-based configuration file
- Easy niche and keyword management
- Platform selection
- Time window customization
- Output settings

## Installation

### Prerequisites
- Python 3.9+
- pip

### Setup

1. **Clone/Create the project**
```bash
cd "Lead Gen Engine"
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Create environment variables**
```bash
cp .env.example .env
```
Then update `.env` with your `TELEGRAM_BOT_TOKEN`.

## Configuration

Edit `config.yaml` to customize:

### Niches
Add or modify target niches with specific keywords:
```yaml
niches:
  - name: "Tech Startups"
    keywords:
      - "web developer"
      - "hiring developer"
      - "software engineer"
```

### Platforms
Enable/disable scraping platforms:
```yaml
platforms:
  - name: "linkedin"
    enabled: true
  - name: "facebook"
    enabled: true
  - name: "twitter"
    enabled: true
  - name: "web"
    enabled: true
```

### Time Filters
Set how recent posts should be:
```yaml
time_filters:
  max_age_days: 7  # Include posts from last 7 days
```

### Extraction Settings
Configure what to extract:
```yaml
extraction:
  extract_emails: true
  extract_phones: true
  extract_company_names: true
  validate_emails: true
```

## Usage

### Run Once
```bash
python main.py
```

### Scheduled Runs
Modify the scheduler configuration in `main.py`:
```python
engine.start_scheduler(frequency_hours=24, start_time="08:00")
```

### Output
Leads are saved to `data/leads_YYYYMMDD_HHMMSS.csv` with columns:
- `email`
- `phone`
- `company_name`
- `social_handle`
- `region`
- `source_url`
- `source_platform` (web, linkedin, facebook, twitter, instagram)
- `post_link`
- `extracted_at` (timestamp)

## Telegram Bot

The Telegram bot provides remote control of the scraping session from your phone or desktop.

1. Create a `.env` file using `.env.example` and set `TELEGRAM_BOT_TOKEN`.
2. Run the bot with:
```bash
python bot.py
```
3. Commands:
   - `/start` — Start the bot and show available commands
   - `/help` — Show help text
   - `/status` — View current target, region, platforms, and lead limit
   - `/set_target <niche>` — Choose a niche from `config.yaml`
   - `/set_platforms <web,linkedin,facebook,twitter,instagram>` — Choose active platforms
   - `/set_region <region>` — Apply region targeting for this session
   - `/set_amount <number>` — Set the maximum number of leads for the next scrape
   - `/scrape` — Start a scraping job with current settings
   - `/download` — Download the latest generated CSV file

## Project Structure

```
Lead Gen Engine/
├── scrapers/
│   ├── __init__.py
│   ├── web_scraper.py          # Website scraping
│   └── social_scrapers.py      # Social media scrapers
├── utils/
│   ├── __init__.py
│   ├── lead_extractor.py       # Email/phone/company extraction
│   ├── human_behavior.py       # Anti-detection mechanisms
│   ├── validators.py           # Data validation & filtering
│   └── proxy_manager.py        # Proxy rotation (future)
├── tests/                      # Unit and integration tests
├── data/                       # Output CSV files
├── config.yaml                 # Configuration file
├── bot.py                      # Telegram bot orchestration
├── main.py                     # Entry point
├── scheduler.py                # Scheduling logic
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## Testing

### Run Tests
```bash
python -m pytest tests/
```

### Test Extraction
```python
from utils.lead_extractor import LeadExtractor

text = "Contact us at info@example.com or call (555) 123-4567"
emails = LeadExtractor.extract_emails(text)
phones = LeadExtractor.extract_phones(text)
```

## Compliance & Legal

⚠️ **Important Notes**

1. **Respect robots.txt** - Check and follow website robots.txt files
2. **Platform Terms of Service** - Ensure compliance with each platform's ToS
3. **Rate Limiting** - Use reasonable delays to avoid overwhelming servers
4. **No Authentication Bypass** - Do not bypass login or authentication
5. **Logging & Transparency** - All activities are logged for compliance
6. **Stop on Blocks** - Cease scraping immediately if detected or blocked
7. **Local Laws** - Verify compliance with local data protection laws (GDPR, CCPA, etc.)

The system is designed for ethical scraping of publicly available data only.

## Limitations

- Social media scrapers are framework foundations (API integration required for full functionality)
- Free proxies may be unreliable; consider using dedicated proxies for production
- Some platforms actively block scraping; verify ToS compliance before use
- JavaScript-heavy pages may require Selenium enhancement (currently supports basic JS rendering)

## Troubleshooting

### No leads extracted
- Check that platforms are enabled in config
- Verify keywords match actual content
- Check network connectivity
- Review logs in `scraper.log`

### Rate limiting / Blocks
- Increase delays in `human_behavior` config
- Use proxies with rotation
- Reduce concurrency/frequency
- Check target website's blocking policy

### Email validation errors
- Verify email format is correct
- Check spam keyword filters
- Review validation rules in `validators.py`

## Future Enhancements

- [ ] Advanced proxy management with rotating pools
- [ ] Selenium integration for heavy JavaScript sites
- [ ] Email verification API integration
- [ ] Contact form submission handling
- [ ] Advanced filtering and ML-based lead scoring
- [ ] Database storage (SQLite/PostgreSQL)
- [ ] Web API for remote execution
- [ ] Dashboard for monitoring

## Support

For issues or questions:
1. Check `scraper.log` for error details
2. Review configuration in `config.yaml`
3. Verify platform availability
4. Check network/proxy settings

## License

This project is provided as-is for educational and legitimate business purposes.

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style
- Tests are included
- Documentation is updated
- Ethical scraping practices are maintained

---

**Last Updated**: May 2026  
**Version**: 1.0.0
