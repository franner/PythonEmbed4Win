import subprocess

import pytest
import asyncio
import playwright
from playwright.async_api import async_playwright


try:
    # Run the playwright install command
    subprocess.run(["playwright", "install"], check=True)
except:
    print("Playwright is installed")
    
async def main():
    async with async_playwright() as p:
        # Connect to the running browser instance over CDP
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        # Get the first context. If there are no contexts, you may need to create one
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        # Get the first page. If there are no pages, you may need to create one
        page = context.pages[0] if context.pages else await context.new_page()
        # Navigate to a website
        await page.goto("http://google.com")
        # Perform other actions, e.g., take a screenshot
        ##await page.screenshot(path="example.png")
        # Click Gmail
        await page.click('//*[@id="gb"]/div/div[1]/div/div[1]/a');

        # Close the browser
        ##await page.close()
        ##await browser.close()

        
asyncio.run(main())
