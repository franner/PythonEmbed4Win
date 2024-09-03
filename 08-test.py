import os
import subprocess
import platform
import subprocess
import asyncio
import traceback
from playwright.async_api import async_playwright


def clear_screen():
    # Check if the operating system is Windows
    if platform.system().lower() == "windows":
        # Clear screen command for Windows
        subprocess.run(["cls"], shell=True)
    else:
        # Clear screen command for Unix/Linux/Mac
        subprocess.run(["clear"], shell=True)


class PlaywrightManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    @staticmethod
    def install_playwright():
        try:
            # Run the playwright install command
            subprocess.run(["playwright", "install"], check=True)
            clear_screen()
        except Exception as e:
            print(f"An error occurred while installing Playwright: {e}")
            clear_screen()
    
    async def setup(self):
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.connect_over_cdp("http://localhost:9222")
            # Get the first context or create one if none exist
            self.context = self.browser.contexts[0] if self.browser.contexts else await self.browser.new_context()
            # Get the first page or create one if none exist
            self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
            clear_screen()
        except Exception as e:
            traceback.print_exc()
            print("Setup Finished Error")
            #input()
            clear_screen()


    async def go_to(self, url):
        try:
            await self.page.goto(url)
            clear_screen()
        except Exception as e:
            traceback.print_exc()
            print("Function go_to Error")
            #input()
            clear_screen()


    async def click_selector(self, selector):
        try:
            await self.page.click(selector)
            clear_screen()
        except Exception as e:
            traceback.print_exc()
            print("Function click_selector Error")
            #input()
            clear_screen()


    async def Wait_For_selector(self, selector):
        try:
            await self.page.wait_for_selector(selector, timeout=100)
            return True
            clear_screen()
        except Exception as e:
            traceback.print_exc()
            print("Function Wait_For_selector Error")
            #input()
            return False
            clear_screen()

    async def wait_and_click(self, selector):
        try:
            # Wait for the selector to be present within the given timeout
            await self.page.wait_for_selector(selector, timeout=1000)  # 1 seconds timeout
            clear_screen()  # Assuming clear_screen is a previously defined function
            bCondition = True
        except Exception as e:
            traceback.print_exc()
            print(f"Error in wait_and_click with selector {selector}: {e}")
            #input()  # Uncomment this if you want to wait for user input before continuing
            clear_screen()
            bCondition = False
        if bCondition == True:
            # If the selector is found, click on it
            await self.page.click(selector)
        

    async def playwright_close(self):
        try:
            await self.playwright.stop()
            clear_screen()
        except Exception as e:
            traceback.print_exc()
            print("Function playwright_close Error")
            #input()
            clear_screen()


    async def browser_close(self):
        try:
            await self.browser.close()
            clear_screen()
        except Exception as e:
            traceback.print_exc()
            print("Function browser_close Error")
            #input()
            clear_screen()


    async def page_close(self):
        try:
            await self.page.close()
            clear_screen()
        except Exception as e:
            traceback.print_exc()
            print("Function page_close Error")
            #input()
            clear_screen()




# Using the PlaywrightManager
async def main():
    PlaywrightManager.install_playwright()
    manager = PlaywrightManager()
    await manager.setup()
    await manager.go_to("http://google.com")

    xpath = '//*[@id="L2AGLb"]'
    await manager.wait_and_click(xpath)

    xpath = '//*[@id="gb"]/div/div[1]/div/div[1]/a'
    await manager.wait_and_click(xpath)
    #await manager.page_close()
    #await manager.browser_close()
    await manager.playwright_close()
    try:
        print("main Finished")
    except Exception as e:
            traceback.print_exc()
            #input()
asyncio.run(main())