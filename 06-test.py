print("This line will be printed.")

import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Create a ChromeService object
#####service =  webdriver.ChromeService(executable_path="C:/Users/fh/Selenium/chromedriver/chromedriver-win64/chromedriver.exe")



service = Service(executable_path='C:/Users/fh/Selenium/chromedriver/chromedriver-win64/chromedriver.exe')
service = Service(port=9222)
options = Options()
options.binary_location = "C:/Users/fh/Selenium/chrome/chrome-win64/chrome.exe"
options.add_argument("--start-maximized")
options.add_argument("--user-data-dir=C:/Users/fh/Selenium/Chrome_Profile")
#options.add_argument("--disable-automation")
options.add_argument("disable-automation")
#options.add_argument("--enable-automation")
#options.add_argument("enable-automation")
#options.add_argument("--disable-infobars")
#options.excludeSwitches("enable-automation")
options.add_argument("disable-infobars")
options.add_argument("--disable-blink-features=AutomationControlled")
#options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])

#options.add_argument('incognito')
options.add_argument('disable-geolocation')
options.add_argument('ignore-certificate-errors')
options.add_argument('disable-popup-blocking')
options.add_argument('disable-web-security')
options.add_argument('--disable-infobars')
options.add_argument('disable-translate')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_experimental_option("detach", True)


#options.LeaveBrowserRunning = "True"

driver = webdriver.Chrome(options=options,service=service)

driver.set_page_load_timeout(30)


# Changing the property of the navigator value for webdriver to undefined 
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 


# Initializing a list with two Useragents 
useragentarray = [ 
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", 
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", 
] 
for i in range(len(useragentarray)): 
	# Setting user agent iteratively as Chrome 108 and 107 
	driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragentarray[i]}) 
	print(driver.execute_script("return navigator.userAgent;")) 


driver.get("https://www.google.com")
driver.get("https://www.dr.dk")

title = driver.title
print(title)
print(driver.window_handles)
print(driver.current_window_handle)
print(driver.current_url)


name = driver.name
print(name)


#driver.close()
#driver.quit()

print("Exiting the program...")
sys.exit(0)


driver = None
webdriver = None
Service = None
Options = None

del driver
del webdriver
del Service
del Options

print("Push Enter to continue.")
input()
