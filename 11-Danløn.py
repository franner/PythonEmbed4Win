import subprocess
import requests
import pathlib
import os
import contextlib
from openpyxl import Workbook
from time import sleep

def is_chrome_running(debugging_port):
    """Check if Chrome is already running with debugging enabled."""
    try:
        requests.get(f'http://localhost:{debugging_port}/json/version', timeout=1)
        return True
    except requests.exceptions.RequestException:
        return False

def open_chrome():
    script_path = pathlib.Path(__file__).parent.resolve()
    chrome_dir = script_path / 'Chrome'
    chrome_executable = chrome_dir / 'chrome-win64' / 'chrome.exe'
    user_data_dir = script_path / 'Chrome_Profile'
    debugging_port = "9222"

    # Check if the remote debugging port is open
    if is_chrome_running(debugging_port):
        print("Chrome is already running with debugging enabled, quitting the function.")
        return

    print("Chrome is not running on the debugging port, opening Chrome.")
    command = [
        str(chrome_executable), 
            f"--remote-debugging-port={debugging_port}", 
            f"--user-data-dir={user_data_dir}", 
            "-test-type=gpu",
            "--start-maximized",
            "--no-sandbox",
            "--disable-software-rasterizer",
            "--disable-background-timers-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
            "--disable-infobars",
            "--disable-web-security",
            "--blink-settings=imagesEnabled=false",
            "--ignore-certificate-errors",
            "--disable-popup-blocking",
            "--disable-smooth-scrolling",
            "--max_old_space_size",
            "--disable-automation",
            "--disable-cache",
            f"http://localhost:{debugging_port}/json/version"
    ]
#           "--disable-background-timers-throttling",
#        "--disable-renderer-backgrounding",
#        "--disable-backgrounding-occluded-windows",
#        "--disable-infobars",
#        "--disable-web-security",
#        "--blink-settings=imagesEnabled=false",
#        "--ignore-certificate-errors",
#        "--disable-popup-blocking",
#        "--disable-smooth-scrolling",
#        "--max_old_space_size"
    #"--enable-automation",
    #"--disable-cache"
    subprocess.Popen(command)

    # Wait for Chrome to start and open the remote debugging port
    while not is_chrome_running(debugging_port):
        print("Waiting for Chrome to start...")
        sleep(1)  # Pause the script for a second before trying again

    response = requests.get(f'http://localhost:{debugging_port}/json/version')
    websocket_url = response.json()['webSocketDebuggerUrl']

    websocket_path = chrome_dir / 'websocket.txt'
    with contextlib.suppress(FileNotFoundError):
        with open(websocket_path, "w") as f:
            f.write(websocket_url)

# Call the function
open_chrome()





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
            # Wait for the page to be fully loaded, including network being idle
            await page.wait_for_load_state("networkidle")
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


    async def type(self, selector, text):
        try:
            await self.page.wait_for_selector(selector, timeout=1000)  # 1 seconds timeout
            clear_screen()  # Assuming clear_screen is a previously defined function
            bCondition = True
        except Exception as e:
            traceback.print_exc()
            print(f"Error in Type with selector {selector} and text {text}: {e}")
            #input()  # Uncomment this if you want to wait for user input before continuing
            clear_screen()
            bCondition = False
        if bCondition == True:
            # If the selector is found, click on it
            await self.page.click(selector)
            await self.page.fill(selector, text)

    async def hover(self, selector):
        try:
            # Use the selector to create a locator
            locator = self.page.locator(selector)
            await locator.scroll_into_view_if_needed()
            clear_screen()
        except Exception as e:
            traceback.print_exc()
            print("Function hover Error")
            input()
            clear_screen()

    async def title(self):
        try:
            # Use the selector to create a locator
            title = await self.page.title();
            clear_screen()
            return title
        except Exception as e:
            traceback.print_exc()
            print("Function title Error")
            input()
            clear_screen()


    async def setvalue(self, selector, text):
        try:
            # Use the selector to create a locator
            #locator = self.page.locator(selector)
            await self.page.wait_for_selector(selector, state='attached')
            locator = self.page.locator(selector)
            await locator.select_option(label=text)
            #select_option: value, label, index
            # Fetch all options
            #await locator.select_option(value='Enabled')
            #await locator.select_option(label='Enabled')
            #input()
            clear_screen()
        except Exception as e:
            traceback.print_exc()
            print("Function hover Error")
            input()
            clear_screen()

    async def LoopSelector(self, selector, selectortwo):
        try:
            script_path = pathlib.Path(__file__).parent.resolve()
            File_xlsx = script_path / 'example.xlsx'

            # Use the selector to create a locator
            #locator = self.page.locator(selector)
            #await self.page.wait_for_selector(selector, state='attached')
            await self.page.wait_for_selector(selector, timeout=20000)
            await self.page.wait_for_load_state("networkidle")
            #options_locator = self.page.locator('select#MEDARBEJDER_SELECTOR option')
            locator = self.page.locator(selector)
            options_locator = self.page.locator(f'{selectortwo}')
            count = await options_locator.count()
            #await options_locator.select_option(value="199")
            #await locator.select_option(value="220")
            #await locator.select_option(index=213)
            await locator.press('Home')
            print("wait....")
            input()
            print(f"{count}")
            print("wait....")
            input()
            i = 1

            wb = Workbook()
            ws = wb.active
            for index in range(1,count+1):
                await self.page.wait_for_load_state("networkidle")
                locator_name = self.page.locator('//*[@id="stam.navn"]')
                Name = await locator_name.input_value()
                locator_name = self.page.locator('//*[@id="stam.lonNummer"]')
                MedarbejderNr = await locator_name.input_value()
                locator_name = self.page.locator('//*[@id="stam.ansatDato"]')
                ansatDato = await locator_name.input_value()
                ansatDato = ansatDato.replace('.', '-')
                locator_name = self.page.locator('//*[@id="stam.fratraadtDato"]')
                fratraadtDato = await locator_name.input_value()
                fratraadtDato = fratraadtDato.replace('.', '-')
                print(index)
                print(Name)
                print(MedarbejderNr)
                print(ansatDato)
                print(fratraadtDato)
                #input()  # Waits for user input before continuing. Remove if not needed.
                await locator.select_option(index=index)

                # Create a workbook and select the active worksheet

                ws.append([Name, MedarbejderNr, ansatDato, fratraadtDato])
                wb.save(File_xlsx)


            print("wait....")
            input()
            clear_screen()
        except Exception as e:
            traceback.print_exc()
            print("Function LoopSelector Error")
            input()
            clear_screen()

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

    await manager.go_to("https://app.danlon.dk/app/overblik?")
    title = await manager.title()
    print(f"The title of the page is: '{title}'")

    main_string = f"{title}"
    substring = "Log ind"

    if substring.lower() in main_string.lower():
        print(f"'{substring}' is found in '{main_string}' (case-insensitive).")
        print(f"We are not logged in.")
        await manager.wait_and_click('//*[@id="coiPage-1"]/div[2]/div[1]/button[3]')
        await manager.wait_and_click('//*[@id="kc-login"]')
    else:
        print(f"'{substring}' is not found in '{main_string}' (case-insensitive).")
        print(f"We are already logged in!")

    await manager.go_to("https://app.danlon.dk/app/medarbejder/generelt?")
    await manager.setvalue('//*[@id="LONPERIODE_MED_ARKIVEREDE_SELECTOR"]','Arkiverede')
    #await manager.LoopSelector('//*[@id="MEDARBEJDER_SELECTOR"]')
    #await manager.LoopSelector('#MEDARBEJDER_SELECTOR')
    await manager.LoopSelector('//*[@id="MEDARBEJDER_SELECTOR"]','select#MEDARBEJDER_SELECTOR option')
    #'select' //*[@id="LONPERIODE_MED_ARKIVEREDE_SELECTOR"]





    await manager.playwright_close()
    try:
        print("main Finished")
    except Exception as e:
            traceback.print_exc()
            #input()


asyncio.run(main())