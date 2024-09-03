import subprocess
import requests
import pathlib
import os
import json
import contextlib

def open_chrome():
    CurrentScriptPath = pathlib.Path(__file__).parent.resolve()
    ChromePath = f"{CurrentScriptPath}/Chrome"
    chrome_path = f"{CurrentScriptPath}/chrome/chrome-win64/chrome.exe"
    user_data_dir = f"{CurrentScriptPath}/Chrome_Profile"
    debugging_port = "9222"

    # Check if the remote debugging port is open
    try:
        response = requests.get(f'http://localhost:{debugging_port}/json/version')
        # If the request is successful, Chrome is already running with debugging enabled
        print("Chrome is already running with debugging enabled, quitting the function.")
        return
    except requests.exceptions.RequestException:
        # If the request fails, Chrome is not running on the debugging port
        print("Chrome is not running on the debugging port, opening Chrome.")
        command = [chrome_path, f"--remote-debugging-port={debugging_port}", f"--user-data-dir={user_data_dir}", "-test-type=gpu", f"http://localhost:{debugging_port}/json/version"]
        process = subprocess.Popen(command)
        # Here you may want to add logic to wait and ensure Chrome starts properly
        # Make an HTTP GET request to the Chrome remote debugging endpoint
        response = requests.get('http://localhost:9222/json/version')
        data = response.json()

        # Extract the WebSocket debugger URL
        websocket_url = data['webSocketDebuggerUrl']
        #print(websocket_url)

        with contextlib.suppress(FileNotFoundError):
            os.remove(f"{ChromePath}/websocket.txt")


        # opening the file in write only mode
        f = open(f"{ChromePath}/websocket.txt", "w")
        # f is the File Handler
        f.write(websocket_url)

# Call the function
open_chrome()

