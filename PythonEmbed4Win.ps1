# Script to download and setup the latest Python embeddable package for Windows x64

# Step 1: Determine the latest Python version from the official website
$pythonUrl = "https://www.python.org/ftp/python/"
$latestVersionHtml = Invoke-WebRequest -Uri $pythonUrl -UseBasicParsing | Select-Object -ExpandProperty Content

# Parse out the latest version number, assuming the format is consistent
$versionPattern = [regex]::Matches($latestVersionHtml, "\d+\.\d+\.\d+")
$latestVersion = $versionPattern | ForEach-Object { $_.Value } | Sort-Object -Descending | Select-Object -First 1

# Step 2: Construct the URL to the latest Python embeddable package
$embedUrl = "$pythonUrl$latestVersion/python-$latestVersion-embed-amd64.zip"

# Step 3: Define the destination for the download
$destinationPath = "$PSScriptRoot\python-$latestVersion-embed-amd64.zip"

# Step 4: Download the Python embeddable package
Write-Host "Downloading Python $latestVersion embeddable package from $embedUrl..."
Invoke-WebRequest -Uri $embedUrl -OutFile $destinationPath

# Step 5: Extract the zip file
Write-Host "Extracting the package..."
$extractPath = "$PSScriptRoot\python-embed"
Expand-Archive -Path $destinationPath -DestinationPath $extractPath -Force

# Step 6: Wait for extraction to complete
Start-Sleep -Seconds 5  # Adjust the sleep duration as necessary

# Step 7: Remove the zip file after extraction
Remove-Item $destinationPath

# Step 8: Locate and modify the ._pth file to enable pip installation
$pypathFile = Get-ChildItem -Path $extractPath -Filter "*._pth" | Select-Object -First 1

if ($pypathFile) {
    Write-Host "Modifying $($pypathFile.Name) to enable site-packages and pip..."
    (Get-Content -Path $pypathFile.FullName) | ForEach-Object { $_ -replace '#import site', 'import site' } | Set-Content -Path $pypathFile.FullName
} else {
    Write-Host "Error: Could not find the Python ._pth file. Aborting."
    exit 1
}

# Step 9: Download get-pip.py script
$pipUrl = "https://bootstrap.pypa.io/get-pip.py"
$pipScriptPath = "$PSScriptRoot\get-pip.py"

Write-Host "Downloading get-pip.py from $pipUrl..."
Invoke-WebRequest -Uri $pipUrl -OutFile $pipScriptPath

# Step 10: Install pip
Write-Host "Installing pip..."
& "$extractPath\python.exe" $pipScriptPath

# Step 11: Clean up
Write-Host "Cleaning up..."
Remove-Item $pipScriptPath

# Step 12: Verify pip installation
$pipExePath = "$extractPath\Scripts\pip.exe"
if (Test-Path $pipExePath) {
    Write-Host "pip successfully installed!"
    & "$pipExePath" --version
} else {
    Write-Host "pip installation failed."
    exit 1
}

# Step 13: Test the Python installation
Write-Host "Testing Python installation..."
& "$extractPath\python.exe" -V

Write-Host "Python $latestVersion and pip setup complete!"
