import asyncio
from pyppeteer import connect
import pathlib
from pathlib import Path



async def main():
    CurrentScriptPath = pathlib.Path(__file__).parent.resolve()
    ChromePath = f"{CurrentScriptPath}\Chrome"
    WebSocket = f"{ChromePath}\websocket.txt"
    print(WebSocket)
    strWebSocket = Path(WebSocket).read_text()
    print(strWebSocket)
    browser = await connect(browserWSEndpoint=f"{strWebSocket}")
    # Now you can interact with the browser instance
    # For example, creating a new page:
    #page = await browser.newPage()
    page = (await browser.pages())[0]
    await page.goto('http://example.com')
    # ... Do more stuff with the page
    await page.screenshot({'path': 'example.png'})
#    await browser.close()

asyncio.get_event_loop().run_until_complete(main())