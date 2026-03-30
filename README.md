# 📺 TV Guide Multi-Channel Scraper

> Scrape TV show schedules from 68+ channels and export to a single clean JSON file. Built for recurring monthly use.

## Features

- ✅ Scrapes any number of channel URLs
- ✅ Outputs single consolidated JSON (weekday + weekend split)
- ✅ Handles JS-heavy sites (Playwright mode available)
- ✅ Configurable delay between requests (polite scraping)
- ✅ Error handling per channel (one failure won't stop the rest)
- ✅ Monthly cron-ready

## Install

```bash
pip install requests beautifulsoup4
```

## Usage

```bash
# Basic usage
python3 tv_guide_scraper.py --config channels.json --output schedule.json

# Demo mode (test without config)
python3 tv_guide_scraper.py --demo
```

## Channel Config Format

```json
[
  {"name": "NBC", "url": "https://example.com/nbc/schedule"},
  {"name": "ABC", "url": "https://example.com/abc/schedule", "weekend_same_as_weekday": false}
]
```

## Output Format

```json
{
  "generated_at": "2026-03-31T02:00:00",
  "total_channels": 68,
  "successful": 67,
  "channels": [
    {
      "channel": "NBC",
      "weekday": [{"time": "8:00 PM", "title": "Show Name"}],
      "weekend": [{"time": "7:00 PM", "title": "Weekend Show"}]
    }
  ]
}
```

## Custom Work

Need this customized for your specific sites? **DM me on Freelancer or Reddit.**
- Custom selectors for your specific channel websites
- 68-channel setup & testing: **$35**
- Monthly delivery service: **$35/month**
- Playwright/JS-heavy sites extra: **+$10**

## License

MIT — free to use, modify, distribute.

---

💡 *Built by K Two. Available for custom Python/automation work.*  
📧 Contact via [Freelancer](https://www.freelancer.com) | [Reddit u/ktwo_dev]
