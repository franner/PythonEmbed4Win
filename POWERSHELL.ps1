# Script to download and install the latest stable ZIP version of PowerShell for Windows

# Step 1: Determine the latest stable version from the GitHub releases page
$releasesUrl = "https://api.github.com/repos/PowerShell/PowerShell/releases/latest"
$latestRelease = Invoke-RestMethod -Uri $releasesUrl -UseBasicParsing
$latestVersion = $latestRelease.tag_name.TrimStart('v')

# Step 2: Construct the URL to the latest PowerShell ZIP package for Windows x64
$zipAsset = $latestRelease.assets | Where-Object { $_.name -match "win-x64.zip$" }
$zipUrl = $zipAsset.browser_download_url

# Step 3: Define the destination for the download
$destinationPath = "$PSScriptRoot\PowerShell-$latestVersion-win-x64.zip"

# Step 4: Download the PowerShell ZIP package
Write-Host "Downloading PowerShell $latestVersion ZIP package from $zipUrl..."
Invoke-WebRequest -Uri $zipUrl -OutFile $destinationPath

# Step 5: Define the extraction path (same folder as the .ps1 script, under a subfolder 'Powershell')
$extractPath = "$PSScriptRoot\Powershell"

# Create the extraction directory if it doesn't exist
if (-not (Test-Path $extractPath)) {
    New-Item -Path $extractPath -ItemType Directory
}

# Step 6: Extract the ZIP file
Write-Host "Extracting PowerShell $latestVersion..."
Expand-Archive -Path $destinationPath -DestinationPath $extractPath -Force

# Step 7: Clean up the ZIP file after extraction
Remove-Item $destinationPath

# Step 8: Verify the installation
$pwshExe = "$extractPath\pwsh.exe"
if (Test-Path $pwshExe) {
    Write-Host "Verifying the PowerShell installation..."
    $installedVersion = & "$pwshExe" -Version
    Write-Host "PowerShell $installedVersion installed successfully!"
} else {
    Write-Host "PowerShell installation failed!"
}
