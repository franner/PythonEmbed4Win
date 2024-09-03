$ProgressPreference = 'SilentlyContinue'

[Net.ServicePointManager]::SecurityProtocol = "tls12, tls11, tls"

Write-Host Folder: "./PythonEmbed4Win.ps1"
Write-Host Downloading...


Invoke-WebRequest -Uri "https://raw.githubusercontent.com/franner/PythonEmbed4Win/main/PythonEmbed4Win.ps1" -OutFile "PythonEmbed4Win.ps1"
.\PythonEmbed4Win.ps1

Exit