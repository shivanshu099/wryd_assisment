from playwright.sync_api import sync_playwright
from urllib.parse import urljoin,urlparse
import os
import time

BASE_URL = "https://ursowyrd.notion.site/companywiki"
OUTPUT_FILE = "wryd_wiki.txt"


def expand_all_content(page):
    # Scroll multiple times (lazy loading)
    for _ in range(1):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1500)

    # Expand all toggle blocks
    closed_toggles = page.query_selector_all('div.notion-toggle-block')
    for block in closed_toggles:
        try:
            button = block.query_selector('div[role="button"]')
            if not button:
                    continue
            if button.get_attribute("aria-expanded") == "false":
                    button.click()
                    page.wait_for_timeout(300)
        except:
            pass

def scrape_full_site(base_url):
    visted=set()
    all_text=""
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=False)
        page=browser.new_page()
        page.goto(base_url,wait_until="domcontentloaded", timeout=60000)
        expand_all_content(page)
        time.sleep(10)
        links=page.eval_on_selector_all(
            "a",
            "elements=> elements.map(e=>e.href)"
        )
        domain=urlparse(base_url).netloc
        notion_links=set()
        for link in links:
            if not links:
                continue
            absolute_url=urljoin(base_url,link)
            parsed=urlparse(absolute_url)
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if parsed.netloc==domain:
                notion_links.add(clean_url)
        print(f"🔎 Found {len(notion_links)} Pages")
        for clean_urls in notion_links:
            if clean_urls in visted:
                continue
            print(f"📄 Scrapping :{clean_urls}")
            page.goto(clean_urls,wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(5000)
            expand_all_content(page)
            text=page.inner_text("body")
            all_text=all_text+f"\n\n---------Page: {clean_urls}---------------\n\n"
            all_text=all_text+text
            visted.add(clean_urls)
        browser.close()
    return all_text
content=scrape_full_site(BASE_URL)
with open(OUTPUT_FILE,"w",encoding="utf-8") as f:
    f.write(content)
print("☑️ Entire site text saved.........")























































