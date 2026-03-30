#!/usr/bin/env python3
"""
tv_guide_scraper.py - Multi-channel TV Guide Scraper
Scrapes TV show schedules from multiple channels and outputs a single JSON file.

Usage:
    python3 tv_guide_scraper.py --config channels.json --output schedule.json
    python3 tv_guide_scraper.py --demo  # Run with 3 sample channels

Author: K Two | Contact for custom work: see README
License: MIT
"""

import json
import argparse
import logging
import time
import sys
from datetime import datetime
from typing import Dict, List, Optional

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Install deps: pip install requests beautifulsoup4")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}


def scrape_channel(channel: Dict) -> Dict:
    """Scrape a single channel's schedule. Returns structured data."""
    name = channel.get('name', 'Unknown')
    url = channel.get('url', '')
    result = {
        'channel': name,
        'url': url,
        'scraped_at': datetime.utcnow().isoformat(),
        'weekday': [],
        'weekend': [],
        'error': None
    }

    if not url:
        result['error'] = 'No URL provided'
        return result

    try:
        log.info(f"Scraping {name}: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Generic schedule extraction - finds time+title patterns
        shows = []
        # Try common schedule table patterns
        for row in soup.select('tr, .schedule-item, .program-item, [class*="schedule"], [class*="program"]'):
            time_el = row.select_one('[class*="time"], td:first-child, .time')
            title_el = row.select_one('[class*="title"], [class*="name"], td:nth-child(2), .title')
            if time_el and title_el:
                t = time_el.get_text(strip=True)
                title = title_el.get_text(strip=True)
                if t and title and len(title) > 1:
                    shows.append({'time': t, 'title': title})

        # Fallback: look for time-like patterns near text
        if not shows:
            import re
            text_blocks = soup.find_all(string=re.compile(r'\d{1,2}:\d{2}'))
            for block in text_blocks[:50]:
                parent = block.parent
                if parent:
                    shows.append({
                        'time': re.search(r'\d{1,2}:\d{2}(?:\s*[AP]M)?', block).group(),
                        'title': parent.get_text(strip=True)[:80]
                    })

        # Split weekday/weekend based on channel config
        result['weekday'] = shows
        result['weekend'] = channel.get('weekend_same_as_weekday', True) and shows or []
        log.info(f"  → Found {len(shows)} shows")

    except Exception as e:
        result['error'] = str(e)
        log.error(f"  → Error: {e}")

    return result


def run_demo():
    """Demo mode with 3 sample public TV guide URLs."""
    demo_channels = [
        {'name': 'Demo Channel 1', 'url': 'https://www.tvguide.com/listings/', 'weekend_same_as_weekday': True},
    ]
    results = [scrape_channel(c) for c in demo_channels]
    print(json.dumps(results, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description='Multi-channel TV Guide Scraper')
    parser.add_argument('--config', default='channels.json', help='JSON file with channel list')
    parser.add_argument('--output', default='schedule.json', help='Output JSON file')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    try:
        with open(args.config) as f:
            channels = json.load(f)
    except FileNotFoundError:
        log.error(f"Config file not found: {args.config}")
        log.info("Create channels.json with: [{\"name\": \"Channel1\", \"url\": \"https://...\"}]")
        sys.exit(1)

    log.info(f"Scraping {len(channels)} channels...")
    results = []
    for i, channel in enumerate(channels):
        result = scrape_channel(channel)
        results.append(result)
        if i < len(channels) - 1:
            time.sleep(args.delay)

    output = {
        'generated_at': datetime.utcnow().isoformat(),
        'total_channels': len(results),
        'successful': sum(1 for r in results if not r.get('error')),
        'channels': results
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    log.info(f"Done! Output: {args.output} ({output['successful']}/{output['total_channels']} successful)")


if __name__ == '__main__':
    main()
