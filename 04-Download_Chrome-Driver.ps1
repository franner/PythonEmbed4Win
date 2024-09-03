cls
$ProgressPreference = 'SilentlyContinue'

[Net.ServicePointManager]::SecurityProtocol = "tls12, tls11, tls"


Invoke-WebRequest 'https://googlechromelabs.github.io/chrome-for-testing/' -OutFile './chrome-for-testing.txt'
$text = Select-String -Pattern "win64" -Path './chrome-for-testing.txt' | Select-String -Pattern "http"  | Select-String -Pattern ".zip"
$text = [regex]::Matches($text, '(stable.*?beta)') | ForEach-Object { $_.Groups[0].Value }
$text = [regex]::Matches($text, '(http[^/]+.*)') | ForEach-Object { $_.Groups[0].Value }
$text = [regex]::Matches($text, '(http[^/]+.*chromedriver-win64.zip)') | ForEach-Object { $_.Groups[0].Value }
$text = [regex]::Matches($text, '((http)(?!.*http).*)') | ForEach-Object { $_.Groups[0].Value }
cls

Write-Host $text 
Write-Host Folder: ./chromedriver-win64.zip
Write-Host Downloading...

Invoke-WebRequest $text -OutFile './chromedriver-win64.zip'

cls
Write-Host Extracting './chromedriver-win64.zip' to ".\chromedriver"
Expand-Archive './chromedriver-win64.zip' -DestinationPath ".\chromedriver"


Exit