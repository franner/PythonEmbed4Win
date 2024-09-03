import subprocess
import pathlib
CurrentScriptPath = pathlib.Path(__file__).parent.resolve()
ChromePath = f"{CurrentScriptPath}/Chrome"
#print(ChromePath)

chrome_path = f"{CurrentScriptPath}/chrome/chrome-win64/chrome.exe"
user_data_dir = f"{CurrentScriptPath}/Chrome_Profile"
debugging_port = "9222"

command = [chrome_path, f"--remote-debugging-port={debugging_port}", f"--user-data-dir={user_data_dir}",f"-test-type=gpu",f"http://localhost:{debugging_port}/json/version"]

#command = [chrome_path, f"--remote-debugging-port={debugging_port}", f"--user-data-dir={user_data_dir}",f"--auto-open-devtools-for-tabs","https://www.example.com"]

process = subprocess.Popen(command)


import requests
import json

# Make an HTTP GET request to the Chrome remote debugging endpoint
response = requests.get('http://localhost:9222/json/version')
data = response.json()

# Extract the WebSocket debugger URL
websocket_url = data['webSocketDebuggerUrl']
#print(websocket_url)




import contextlib
import os

with contextlib.suppress(FileNotFoundError):
    os.remove(f"{ChromePath}/websocket.txt")


# opening the file in write only mode
f = open(f"{ChromePath}/websocket.txt", "w")
# f is the File Handler
f.write(websocket_url)
