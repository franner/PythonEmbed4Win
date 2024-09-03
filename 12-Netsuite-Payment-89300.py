
import pandas as pd
import itertools
import random
import csv
import pandas as pd
import ast
import time
import subprocess
import requests
import pathlib
import os
import contextlib
from openpyxl import Workbook
from time import sleep
from datetime import datetime


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
            return True
        except Exception as e:
            traceback.print_exc()
            print("Function click_selector Error")
            #input()
            clear_screen()
            return False

    async def click_selector_Force(self, selector):
        try:
            await self.page.click(selector, force=True)
            clear_screen()
            return True
        except Exception as e:
            traceback.print_exc()
            print("Function click_selector Error")
            #input()
            clear_screen()
            return False


    async def Wait_For_selector(self, selector):
        try:
            await self.page.wait_for_selector(selector, timeout=30000)
            return True
            clear_screen()
        except Exception as e:
            traceback.print_exc()
            print("Function Wait_For_selector Error")
            input()
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

    async def extract_table_data(page, selector):
        return await page.evaluate(f"""() => {{
            const table = document.querySelector('{selector}');
            const rows = Array.from(table.rows);
            return rows.map(row => 
                Array.from(row.cells).map(cell => cell.textContent || cell.innerText)
            );
        }}""")

    async def LoopSelector(self, selector, selectortwo):
        try:
            script_path = pathlib.Path(__file__).parent.resolve()
            File_xlsx = script_path / 'Netsuite.xlsx'
            File_Filtered_xlsx = script_path / 'Netsuite_Filtered.xlsx'
            CSV_File = script_path / '89300.csv'
            table_data = []
            table_data_all = []
            final_filtered_data = []
            filtered_data_for_Combinations = []
            Total_target_sum = 0

            # Use the selector to create a locator
            await self.page.wait_for_load_state("networkidle")
            locatorEndPage = self.page.locator('//*[@id="end_date"]')
            #await locatorEndPage.fill("01012021")
            await locatorEndPage.press('Tab')
            #await locatorEndPage.fill("16112023")
            locatorAccount = self.page.locator('//*[@id="inpt_account2"]')
            await locatorAccount.type("89300")
            await locatorAccount.press('Tab')
            time.sleep(5)
            
            self.page.wait_for_function("""
                    () => new Promise((resolve) => {
                        const observer = new MutationObserver((mutations, obs) => {
                            resolve(true);
                            obs.disconnect();
                        });
                        observer.observe(document.body, { childList: true, subtree: true });
                    })
                """)

            #input()
            await self.page.wait_for_load_state("networkidle")
            await self.page.wait_for_load_state("load")
            await self.page.wait_for_load_state("domcontentloaded")


            locator = self.page.locator('//*[@name="inpt_billrange"]')
            if await locator.is_visible():
                await locator.press('End')
            await self.page.wait_for_load_state("networkidle")
            locator_name = self.page.locator('//*[@name="inpt_billrange"]')
            LastLoopName = await locator_name.input_value()
            print(f"Name of last dropdownmenu: {LastLoopName}")
            if await locator.is_visible():
                await locator.press('Home')
            await self.page.wait_for_load_state("networkidle")
            locator_name = self.page.locator('//*[@name="inpt_billrange"]')
            Name = await locator_name.input_value()
            print(f"Name of first dropdownmenu: {Name}")
            print("wait....")

            i = 0
            LoopName = await locator.input_value()

            while True:
                #await self.page.wait_for_selector("#total")
#                print("click an item the we check the amount")
#                input()
#                NS_Amount_Field = await self.page.locator('//*[@id="total"]').inner_text()
#                print(f"Total Amount = {NS_Amount_Field}")
#                NS_Amount_Field = await self.page.locator('//*[@id="total').input_value()
#                NS_Amount_Field = convert_to_float(NS_Amount_Field)
#                print(f"Total Amount 2 = {NS_Amount_Field}")
#                input()

                time.sleep(2)
                await self.page.wait_for_selector(f"table#bill_splits")
                # Evaluate the script to extract table data

                # Format the JavaScript code string to include LoopName
                table_data_script = f"""() => {{
                    const table = document.querySelector('#bill_splits');
                    if (!table) return [];
                    const rows = Array.from(table.rows);
                    return rows.map((row, index) => {{
                        let rowWithNumberAndLoopName;
                        if (index === 0) {{
                            // Set the first row with headers
                            rowWithNumberAndLoopName = ['TableRowNumber', 'LoopName'];
                        }} else {{
                            // For other rows, set the first column as the row number and the second as LoopName's value
                            rowWithNumberAndLoopName = [index, "{LoopName}"];
                        }}
                        const cellData = Array.from(row.cells).map(cell => cell.textContent.trim());
                        return rowWithNumberAndLoopName.concat(cellData);
                    }});
                }}"""

                table_data = await self.page.evaluate(table_data_script)

                if table_data_all == []:
                    table_data_all = table_data
                else:
                    table_data_all = table_data_all + table_data[1:]

                if not LastLoopName != LoopName:
                    break

                if await locator.is_visible():
                    await locator.press('ArrowDown')
                    await self.page.wait_for_load_state("networkidle")
                    await self.page.wait_for_load_state("load")
                    await self.page.wait_for_load_state("domcontentloaded")
                    await self.page.wait_for_load_state()
                    LoopName = await locator.input_value()

            # Add "RowNumber" to the header
            table_data_all[0].insert(0, "RowNumber")
            # Add row numbers to each data row
            for index, row in enumerate(table_data_all[1:], start=1):
                row.insert(0, index)
            df = pd.DataFrame(table_data_all)
            df.to_excel(str(File_xlsx), index=False, header=False)  # Set index=False if you don't want the DataFrame index written to the file

            print(table_data_all)
            clear_screen()

            # Filter and append new data where ID equals '2'
            Filtered_data = filter_and_append_data(table_data_all, 'ID', 'V1733')
            Filtered_data = sort_data(Filtered_data, ['ID', 'Date Created'])
            Filtered_data = sort_data(Filtered_data, ['ID', 'Date Due'])
            if final_filtered_data == []:
                final_filtered_data = [table_data_all[0]]
            final_filtered_data = append_to_array(final_filtered_data, Filtered_data)

            Filtered_data = filter_and_append_data(table_data_all, 'ID', 'V2')
            Filtered_data = sort_data(Filtered_data, ['ID', 'Date Created'])
            Filtered_data = sort_data(Filtered_data, ['ID', 'Date Due'])
            if final_filtered_data == []:
                final_filtered_data = [table_data_all[0]]
            final_filtered_data = append_to_array(final_filtered_data, Filtered_data)

            # Step 1: Convert raw data to DataFrame
            final_filtered_data = pd.DataFrame(final_filtered_data[1:], columns=final_filtered_data[0])

            final_filtered_data['Date Due'] =  pd.to_datetime(final_filtered_data['Date Due'], format='%d/%m/%Y', errors='coerce')
            final_filtered_data['Date Created'] =  pd.to_datetime(final_filtered_data['Date Created'], format='%d/%m/%Y %H:%M', errors='coerce')
            final_filtered_data['Original Amount'] = final_filtered_data['Original Amount'].apply(convert_to_float)
            final_filtered_data['Amount Due'] = final_filtered_data['Amount Due'].apply(convert_to_float)

            print("final_filtered_data")
            print(final_filtered_data)
            #input()
            df = pd.DataFrame(final_filtered_data)
            df.to_excel(str(File_Filtered_xlsx), index=False, header=False)  # Set index=False if you don't want the DataFrame index written to the file
            print("Workbook saved...")
            balance = await self.page.locator('#balance').inner_text()
            print(f"Balance Amount = {balance}")
            balance = await self.page.locator('#balance').input_value()
            balance = convert_to_float(balance)
            print(f"Balance Amount = {balance}")


            NS_Amount_Field = await self.page.locator('#total').inner_text()
            NS_Amount_Field = await self.page.locator('#total').inner_text()
            print(f"Total Amount = {NS_Amount_Field}")
            NS_Amount_Field = await self.page.locator('#total').input_value()
            NS_Amount_Field = convert_to_float(NS_Amount_Field)
            print(f"Total Amount = {NS_Amount_Field}")

            if Total_target_sum == NS_Amount_Field:
                print("Total_target_sum == NS_Amount_Field")
            else:
                print("Total_target_sum == NS_Amount_Field are not equal!!! something is wrong")
                input()

            # List of encodings to try
            encodings_to_try = ['utf-8', 'latin-1', 'ISO-8859-1', 'cp1252']
            # Attempt to read the file with the specified encodings
            try:
                CSV = read_csv_with_encoding(CSV_File, encodings_to_try)
                print("File read successfully!")
            except ValueError as e:
                print(e)

            #search_value = "3394472,81"

            CSV['Balance'] = CSV['Balance'].apply(convert_to_float)
            CSV['Amount'] = CSV['Amount'].apply(convert_to_float)
            #CSV['Date'] = pd.to_datetime(CSV['Date'])
            CSV['Date'] = pd.to_datetime(CSV['Date'], format='%d.%m.%Y')
            #CSV['Date'] = CSV['Date'].to_datetime(CSV['Date'])
            #CSV['Interest from'] = CSV['Interest from'].to_datetime(CSV['Interest from'])
            CSV['Interest from'] = pd.to_datetime(CSV['Interest from'], format='%d.%m.%Y')

            #filtered_data = pd.DataFrame(array_from_csv[1:], columns=array_from_csv[0])
            filtered_data = CSV[CSV['Balance'] == balance]
            print("filtered_data array:")
            print(filtered_data.iloc[0, 0])
            print(CSV[CSV['Balance'] == balance].index)
            print(CSV.loc[CSV[CSV['Balance'] == balance].index])
            #input()
            print(f"Balance Amount = {balance}")
            print("CSV")
            print(CSV)
            clear_screen()
            #print("Filtered data...:")
            #print(filtered_data)
            #print(CSV[CSV['Balance'] == balance].index)
            index_list = int(CSV[CSV['Balance'] == balance].index[0]) if not CSV[CSV['Balance'] == balance].empty else None

            #CSV_above = CSV['Text'].tolist()[index_list]
            text_list = CSV['Text'].tolist()
            #text_value_list = text_list[index_list]
            print('before looping...')
            print('change date if necessary')
            input()
            for i in range(index_list-1, -1, -1):
                print(i)
                text_list = CSV['Text'].tolist()
                Amount_list = CSV['Amount'].tolist()
                Date_list = CSV['Date'].tolist()
                text_value_list = text_list[i]
                text_value_list = text_value_list.split(' ', 1)[0]
                Amount_value_list = Amount_list[i]
                Date_value_list = Date_list[i]
                # Format to 'd/m/Y'
                Date_value_list =  Date_value_list.strftime("%d/%m/%Y")
                print(f"text_value_list = {text_value_list}'")
                print(f"Amount_value_list = {Amount_value_list}")
                print(f"Date_value_list = {Date_value_list}")
                print("final_filtered_data")
                print(final_filtered_data)
                time.sleep(2)
                filtered_data_for_Combinations = filter_and_append_data(table_data_all, 'ID', f'{text_value_list}')
                #filtered_data_for_Combinations = CSV[CSV['ID'] == f"{text_value_list}"]
                print("filtered_data_for_Combinations")
                print(filtered_data_for_Combinations)
                #input()

                #input()
                #df = pd.DataFrame(filtered_data_for_Combinations, index=False, header=True)
                #df = pd.DataFrame(filtered_data_for_Combinations)
                df = pd.DataFrame(filtered_data_for_Combinations[1:], columns=filtered_data_for_Combinations[0])
                #df = df.sort_values(by=['Date Due'])
                #df = sort_data(df, ['ID', 'Date Due'])
                #df = pd.DataFrame(filtered_data_for_Combinations[0:], columns=filtered_data_for_Combinations[0])

                df.to_excel(str(File_Filtered_xlsx), index=False, header=False)  # Set index=False if you don't want the DataFrame index written to the file
                #target_sum = int(Amount_value_list)
                target_sum = convert_to_float(Amount_value_list*-1)
                target_sum = round(target_sum, 2) #Rounding to 2 decimals


                clear_screen()
                print(f"Target sum:{target_sum}")
                print(df.columns)
                #print(df.reset_index(inplace=True))
                #print(df["RowNumber"].to_numpy())
                #print(df.columns.tolist())
                print(df['Amount Due'])
                print(df['RowNumber'])
                df['Amount Due'] = df['Amount Due'].apply(convert_to_float)
                df['RowNumber'] = df['RowNumber'].apply(convert_to_float)

                clear_screen()
                print(f"df['Amount Due'] = {df['Amount Due']}")
                print(f"df['RowNumber'] = {df['RowNumber']}")
                print(f"target_sum = {target_sum}")


                combination_with_row_numbers = find_combination_with_row_number(df['Amount Due'], target_sum, df['RowNumber'])
                print("Combination with row numbers:")
                print(combination_with_row_numbers)
                #print(combination_with_row_numbers[0])
                #print(combination_with_row_numbers[1])
                
                # Looping through each combination
                # Extracting the first element (column1) from each tuple in the list
                column2_elements = [combination[1] for combination in combination_with_row_numbers]
                if column2_elements == []:
                    print("column2_elements is empty...")
                    input()
                for combination in column2_elements:

                    print("Column2 Element:", combination)
                    # Filter data based on the value in the 'RowNumber' column
                    Filtered_Combination = filter_and_append_data(table_data_all, 'RowNumber', combination)
                    Filtered_Combination_LoopName = pd.DataFrame(Filtered_Combination[1:], columns=Filtered_Combination[0])
                    Filtered_Combination_LoopName = Filtered_Combination_LoopName['LoopName']
                    Filtered_Combination_LoopName = Filtered_Combination_LoopName[0]
                    print("Filtered_Combination: ", Filtered_Combination)
                    Filtered_Combination_TableRowNumber = pd.DataFrame(Filtered_Combination[1:], columns=Filtered_Combination[0])
                    Filtered_Combination_TableRowNumber = Filtered_Combination_TableRowNumber['TableRowNumber']
                    Filtered_Combination_TableRowNumber = Filtered_Combination_TableRowNumber[0]
                    Filtered_Combination = filter_and_append_data(table_data_all, 'RowNumber', combination)
                    Filtered_Combination_RowNumber = pd.DataFrame(Filtered_Combination[1:], columns=Filtered_Combination[0])
                    Filtered_Combination_RowNumber = Filtered_Combination_RowNumber['RowNumber']
                    Filtered_Combination_RowNumber = Filtered_Combination_RowNumber[0]
                    print("Filtered_Combination_RowNumber: ", Filtered_Combination_RowNumber)
                    print("Filtered_Combination: ", Filtered_Combination)
                    #clear_screen()
                    #print("Filtered_Combination_LoopName: ", Filtered_Combination_LoopName)
                    #print("Filtered_Combination_TableRowNumber: ", Filtered_Combination_TableRowNumber)
                    #input()
                    #selector_TableRowNumber = f'#billapply{Filtered_Combination_TableRowNumber}_fs'
                    selector_TableRowNumber = f'#billapply{Filtered_Combination_RowNumber}_fs'
                    print("selector:", selector_TableRowNumber)
                    locator_Menu = self.page.locator('//*[@name="inpt_billrange"]')

                    locator_Menu = self.page.locator('//*[@name="inpt_billrange"]')
                    Filtered_Combination_LoopName = pd.DataFrame(Filtered_Combination[1:], columns=Filtered_Combination[0])
                    Filtered_Combination_LoopName = Filtered_Combination_LoopName['LoopName']
                    Filtered_Combination_LoopName = Filtered_Combination_LoopName[0]
                    DropDownMenu = await locator_Menu.input_value()

                    if DropDownMenu != Filtered_Combination_LoopName:
                        await locator_Menu.press('Home')

                    #await self.page.wait_for_load_state("networkidle")
                    while True:
                        while True:
                            locator_Menu = self.page.locator('//*[@name="inpt_billrange"]')
                            Filtered_Combination_LoopName = pd.DataFrame(Filtered_Combination[1:], columns=Filtered_Combination[0])
                            Filtered_Combination_LoopName = Filtered_Combination_LoopName['LoopName']
                            Filtered_Combination_LoopName = Filtered_Combination_LoopName[0]

                            DropDownMenu = await locator_Menu.input_value()

                            if DropDownMenu == Filtered_Combination_LoopName:
                                #locator_Menu.press('ArrowDown')
                                break
                            else:
                                await locator_Menu.press('ArrowDown')
                                await self.page.wait_for_load_state("networkidle")
                            print(f"DropDownMenu... {DropDownMenu}")
                            print(f"Filtered_Combination_LoopName... {Filtered_Combination_LoopName}")
                            #input()
                            
                        #new_class = await self.page.evaluate(f"document.querySelector('{selector_TableRowNumber}').className")
                        #if new_class == 'checkbox_ck':
                        #    break
                        
                        await self.page.wait_for_selector(f"{selector_TableRowNumber}")
                        #await self.page.click(f"{selector_TableRowNumber}", force=True)
                        Click = False
                        while Click == False:
                            Click = await self.click_selector_Force(f"{selector_TableRowNumber}")

                        #await self.page.click(f"{selector_TableRowNumber}")
                        break
                    #input()
                #input()

                NS_Amount_Field = await self.page.locator('#total').inner_text()
                NS_Amount_Field = await self.page.locator('#total').inner_text()
                print(f"Total Amount = {NS_Amount_Field}")
                NS_Amount_Field = await self.page.locator('#total').input_value()
                NS_Amount_Field = convert_to_float(NS_Amount_Field)
                print(f"Total Amount = {NS_Amount_Field}")
                Total_target_sum = Total_target_sum+target_sum
                Total_target_sum = round(Total_target_sum, 2)

                if Total_target_sum == NS_Amount_Field:
                    print("Total_target_sum == NS_Amount_Field")
                    #input()
                else:
                    
                    print(f"Total_target_sum {Total_target_sum} == NS_Amount_Field {NS_Amount_Field} are not equal!!! something is wrong with text_list = {text_list}")
                    input()

            #print("CSV Above")
            #print(text_value_list)
            #input()

        except Exception as e:
            traceback.print_exc()
            print("Function LoopSelector Error")
            input()
            clear_screen()

    async def playwright_close(self):
        try:
            if resource_type == "playwright":
                await self.playwright.stop()
            elif resource_type == "browser":
                await self.browser.close()
            elif resource_type == "page":
                await self.page.close()
            else:
                raise ValueError("Invalid resource type")
        except Exception as e:
            traceback.print_exc()
            print(f"Error closing {resource_type}: {e}")


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


def filter_and_append_data(original_data, header_to_filter, value_to_filter, new_data=None):
    # Find the index of the header
    header_index = original_data[0].index(header_to_filter)
    
    # Filter the original data
    filtered_data = [original_data[0]]  # include headers
    for row in original_data[1:]:
        if row[header_index] == value_to_filter:
            filtered_data.append(row)
    
    # If there's new data to append
    if new_data:
        for row in new_data[1:]:  # assuming new_data has the same headers
            if row[header_index] == value_to_filter:
                filtered_data.append(row)
    
    return filtered_data

def append_to_array(base_data, additional_data):
    """
    Appends additional data to the base data assuming both have the same headers.

    :param base_data: 2D list containing the base data including headers
    :param additional_data: 2D list containing the new data to be appended including headers
    :return: 2D list with the appended data
    """
    # Check if headers match
    if base_data[0] != additional_data[0]:
        raise ValueError("Headers do not match.")
    
    # Append the data excluding the header of the additional data
    return base_data + additional_data[1:]

def sort_data(data, sort_headers):
    """
    Sorts the 2D list data by multiple headers.

    :param data: 2D list containing the data including headers
    :param sort_headers: List of headers to sort by
    :return: 2D list with the sorted data
    """
    # Extract headers and rows
    headers = data[0]
    rows = data[1:]

    # Get indices of the headers to sort by
    sort_indices = [headers.index(header) for header in sort_headers]

    # Define a key function for sorting based on multiple columns
    def sort_key(row):
        # Return a tuple of values to sort by
        return tuple(row[index] for index in sort_indices)

    # Sort rows by the key
    sorted_rows = sorted(rows, key=sort_key)

    # Return sorted data including headers
    return [headers] + sorted_rows

def read_csv_with_encoding(file_path, encodings):
    for encoding in encodings:
        try:
            # Attempt to read the CSV file with the current encoding
            return pd.read_csv(file_path, encoding=encoding, sep=';')
        except UnicodeDecodeError:
            # If a UnicodeDecodeError occurs, move to the next encoding
            continue
    raise ValueError(f"None of the encodings worked for file: {file_path}")

def convert_to_float(val):
    try:
        # Try converting directly (handles cases without separators)
        return float(val)
    except ValueError:
        # Handle European format (dot as thousand separator, comma as decimal)
        if ',' in val:
            return float(val.replace('.', '').replace(',', '.'))
        # Handle US format (comma as thousand separator, dot as decimal)
        else:
            return float(val.replace(',', ''))


def meet_in_middle_n_way(arr, target, n):
    # Function to compute all possible sums for a part
    def compute_sums(part):
        return {sum(comb) for r in range(len(part) + 1) for comb in itertools.combinations(part, r)}

    # Divide the array into n parts
    length = len(arr)
    parts = [arr[i*length // n: (i+1)*length // n] for i in range(n)]

    # Compute all possible sums for each part
    all_sums = [compute_sums(part) for part in parts]

    # Function to combine sums from different parts
    def combine_sums(all_sums, depth=0, current_sum=0):
        if depth == n:
            return current_sum == target
        for sum_part in all_sums[depth]:
            if combine_sums(all_sums, depth + 1, current_sum + sum_part):
                return True
        return False

    return combine_sums(all_sums)

def check_continuous_subsets(nums, target, row_numbers):
    target = round(target, 2)  # Ensure target is rounded to avoid floating point precision issues

    # Iterate through each starting point in the list
    for i in range(len(nums)):
        current_sum = 0.0
        combination = []

        # Iterate to sum continuous subsets starting from index i
        for j in range(i, len(nums)):
            num = round(nums[j], 2)
            current_sum = round(current_sum + num, 2)

            combination.append((num, row_numbers[j]))

            # Check if the current sum matches the target
            if current_sum == target:
                return combination
            elif current_sum > target:
                break  # Stop if the sum exceeds the target

    return None  # Return None if no continuous subset sums up to the target

def find_combination_with_row_number(nums, target, row_numbers):
    target = round(target, 2)  # Ensure target is rounded to avoid floating point precision issues

    # First, check for continuous subsets that might sum up to the target
    continuous_subset = check_continuous_subsets(nums, target, row_numbers)
    if continuous_subset is not None:
        return continuous_subset

    # Initialize a dictionary to store the combinations leading to each sum
    sum_combinations = {0: []}  # Base case: the sum 0 is reached with no numbers

    for i, num in enumerate(nums):
        num = round(num, 2)  # Round each number to ensure precision
        current_row_number = row_numbers[i]

        # Create a list of sums to update to avoid changing the dictionary during iteration
        sums_to_update = []
        for prev_sum, combo in sum_combinations.items():
            new_sum = round(prev_sum + num, 2)  # Calculate new sum and round it

            # Check if this sum is a new one and less than or equal to target
            if new_sum <= target and new_sum not in sum_combinations:
                sums_to_update.append((new_sum, combo + [(num, current_row_number)]))

                # If new sum equals the target, immediately return the combination
                if new_sum == target:
                    return combo + [(num, current_row_number)]

        # Update sum_combinations with new sums and combinations
        for new_sum, new_combo in sums_to_update:
            sum_combinations[new_sum] = new_combo

    return sum_combinations.get(target)  # Return the combination for the target sum, if it exists

# Using the PlaywrightManager
async def main():
    PlaywrightManager.install_playwright()
    manager = PlaywrightManager()
    await manager.setup()

    await manager.go_to("https://4667410.app.netsuite.com/app/center/card.nl?sc=-29")
    title = await manager.title()
    print(f"The title of the page is: '{title}'")
    main_string = f"{title}"
    substring = "NetSuite Login"

    if substring.lower() in main_string.lower():
        print(f"'{substring}' is found in '{main_string}' (case-insensitive).")
        print(f"We are not logged in.")
        await manager.wait_and_click('//*[@id="login-submit"]')
    else:
        print(f"'{substring}' is not found in '{main_string}' (case-insensitive).")
        print(f"We are already logged in!")

    await manager.go_to("https://4667410.app.netsuite.com/app/accounting/transactions/vendpymts.nl?")
    await manager.LoopSelector('.dropdownDiv','.dropdownDiv.div')

    await manager.playwright_close()
    try:
        print("main Finished")
    except Exception as e:
            traceback.print_exc()
            #input()


asyncio.run(main())