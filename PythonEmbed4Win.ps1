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
Expand-Archive -Path $destinationPath -DestinationPath "$PSScriptRoot\python-embed" -Force

# Step 6: Remove the zip file after extraction
Remove-Item $destinationPath

# Step 7: Set up environment variables (optional)
$pythonPath = "$PSScriptRoot\python-embed"
$env:Path = "$pythonPath;$env:Path"

# Step 8: Test the Python installation
Write-Host "Testing Python installation..."
& "$pythonPath\python.exe" -V

Write-Host "Python $latestVersion setup complete!"
