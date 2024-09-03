##from selenium import webdriver
##from selenium.webdriver.chrome.service import Service
##from selenium.webdriver.chrome.options import Options

##chrome_options = Options()
##chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
###chrome_options.setBinary("C:/Users/fh/Selenium/chrome/chrome-win64/chrome.exe")

##service = Service("C:/Users/fh/Selenium/chromedriver/chromedriver-win64/chromedriver.exe")  # Update this path
###service = Service("executable_path=C:/Users/fh/Selenium/chrome/chrome-win64/chrome.exe")  # Update this path
##driver = webdriver.Chrome(service=service, options=chrome_options)
##driver.get("https://www.dr.dk")  # Opens the website
##print(driver.title)  # Prints the title of the page


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome("C:/Users/fh/Selenium/chromedriver/chromedriver-win64/chromedriver.exe", options=chrome_options)
