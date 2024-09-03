#[CmdletBinding()]
#param (
#    [Parameter(Mandatory = $True)]
#    [string]
#    $SeleniumOutputPath
#)

#     Write-Host "loading module"
Import-Module ".\MyFunctions.psm1"
Import-Module "$PSScriptRoot\MyFunctions.psm1"


###################################
#     test port                   #
#     tnc localhost -port 9222    #
#     tnc localhost -port 9222 | Select-Object -Property "TcpTestSucceeded" | Select-Object -Last 1 | select-string false
#     tnc localhost -port 9222 | Select-Object -Property "TcpTestSucceeded" | Select-Object -Last 1 | select-string true
###################################
$port = 9222



#$ChromePortTrue = tnc localhost -port $port | Select-Object -Property "TcpTestSucceeded" | Select-Object -Last 1 | select-string true
$ChromePortTrue = (Test-PortScan -Devices localhost -StartPort $port).open

#Write-Host "$ChromePortTrue =" $ChromePortTrue 


#if ($ChromePortTrue -eq $null){
if ($ChromePortTrue -eq $false){

     # Your working directory
     $WebdriverPath = $env:USERPROFILE + "\Chrome-Remote\Misc"
     $workingPath = $WebdriverPath

     # Add the working directory to the environment path.
     # This is required for the ChromeDriver to work.
          if (($env:Path -split ';') -notcontains $workingPath) {
              $env:Path += ";$workingPath"
          }

     # OPTION 1: Import Selenium to PowerShell using the Add-Type cmdlet.
     #Add-Type -Path "$($workingPath)\WebDriver.dll"
          Import-Module "$($workingPath)\WebDriver.dll"

     #Seettings for Chrome, profile
          $ChromePath = "--user-data-dir=$env:userprofile\Chrome-Remote"
          $ChromeOptions = New-Object OpenQA.Selenium.Chrome.ChromeOptions
          $ChromeOptions.AddArgument('start-maximized')
          $ChromeOptions.AddArgument('disable-automation')
          $ChromeOptions.AddArgument('disable-infobars')
          $ChromeOptions.AddArgument('--disable-blink-features=AutomationControlled')
#          $ChromeOptions.AddAdditionalCapability("useAutomationExtension", $false)
          $ChromeOptions.AddExcludedArgument("enable-automation")
          $ChromeOptions.LeaveBrowserRunning = $True
#          $ChromeOptions.excludeSwitches = "enable-automation"


          $ChromeOptions.AcceptInsecureCertificates = $True

          $PSScriptRoot+"\Download"
          $ChromeOptions.AddUserProfilePreference('download', @{'default_directory' = $PSScriptRoot+"\Download"; 'prompt_for_download' = $false;})
          $ChromeOptions.AddArgument($ChromePath)
          $ChromePath = "--remote-debugging-port=$port"
          $ChromeOptions.AddArgument($ChromePath)

          chromedriver.exe --version
#pause

#                New-Object OpenQA.Selenium.Chrome.ChromeDriver($ChromeOptions)
$ChromeWindow = New-Object OpenQA.Selenium.Chrome.ChromeDriver($ChromeOptions)
#$ChromeWindow.executeScript("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
}

exit