CLS


$directoryPath = "$PSScriptRoot"

# Get a list of subdirectories in the specified directory
$subdirectories = Get-ChildItem -Path $directoryPath -Directory

# Loop through the subdirectories
foreach ($subdirectory in $subdirectories) {
    # You can add more code here to work with each subdirectory
    if ($($subdirectory.Name).Contains("python") -eq $true) {
        #Write-Host "Subdirectory Name: $($subdirectory.Name)"
        #Write-Host "Subdirectory Full Path: $($subdirectory.FullName)"    
        $PythonPath = $($subdirectory.FullName)
        break
    }
}

Write-Host PythonPath = $PythonPath

CLS
$folderPath = $PythonPath
$PythonEXE = $null

function FindPythonExe {
    param(
        [string]$path,
        [ref]$pythonExeRef
    )

    # Get all files in the current directory
    $files = Get-ChildItem -Path $path -File

    foreach ($file in $files) {
        if ($file.Name -eq "python.exe") {
            $pythonExeRef.Value = $file.FullName
            Write-Host "Found python.exe at $($file.FullName)"
            return $true
        }
    }

    # Recursively search subdirectories
    $subdirs = Get-ChildItem -Path $path -Directory
    foreach ($subdir in $subdirs) {
        $found = FindPythonExe -path $subdir.FullName -pythonExeRef $pythonExeRef
        if ($found) {
            return $true
        }
    }

    return $false
}

# Start the search from the root folder
$foundPython = FindPythonExe -path $folderPath -pythonExeRef ([ref]$PythonEXE)

if ($foundPython) {
	#Write-Host "Python.exe found at $($PythonEXE). Exiting..."
	Write-Host $($PythonEXE)
	Write-Host $PythonEXE
} else {
    Write-Host "Python.exe not found in the specified folder and its subdirectories."
    Pause
}

# DL.ps1
$scriptNameWithoutExtension = $MyInvocation.MyCommand.Name
$scriptBaseName = [System.IO.Path]::GetFileNameWithoutExtension($scriptNameWithoutExtension)
#Write-Host "The name of this script without the extension is: $scriptBaseName"

cls
& "$PythonEXE" ".\$scriptBaseName.py"




EXIT
