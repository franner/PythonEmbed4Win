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

$folderPath = $PythonPath
$PipEXE = $null

function FindPipExe {
    param(
        [string]$path,
        [ref]$pipExeRef
    )

    # Get all files in the current directory
    $files = Get-ChildItem -Path $path -File

    foreach ($file in $files) {
        if ($file.Name -eq "pip3.exe") {
            $pipExeRef.Value = $file.FullName
            Write-Host "Found pip3.exe at $($file.FullName)"
            return $true
        }
    }

    # Recursively search subdirectories
    $subdirs = Get-ChildItem -Path $path -Directory
    foreach ($subdir in $subdirs) {
        $found = FindPipExe -path $subdir.FullName -pipExeRef $pipExeRef
        if ($found) {
            return $true
        }
    }

    return $false
}

# Start the search from the root folder
$foundPip = FindPipExe -path $folderPath -pipExeRef ([ref]$PipEXE)

if ($foundPip) {
	#Write-Host "Pip3.exe found at $($PipEXE). Exiting..."
	Write-Host $($PipEXE)
	Write-Host $PipEXE
} else {
    Write-Host "Pip3.exe not found in the specified folder and its subdirectories."
    Pause
}



	Write-Host "Python install Selenium through PIP"
#	"$($PythonEXE)" -m "$($PipEXE)" install selenium
cls
# Use Start-Process to execute the executable
#Start-Process -FilePath $($PythonEXE) -m $($PipEXE) install selenium

cls
#$($PipEXE) " -U install selenium"

#Start-Process -NoNewWindow -FilePath "$($PipEXE)" -ArgumentList "-U install selenium"

& "$($PipEXE)" -m pip install --upgrade pip
& "$($PipEXE)" install --upgrade pip
& "$($PipEXE)" install pip

& "$($PipEXE)" install selenium
& "$($PipEXE)" install --upgrade selenium


#& "$($PipEXE)" -U install selenium

& "$($PipEXE)" install pyppeteer
& "$($PipEXE)" install asyncio

& "$($PipEXE)" install requests
#& "$($PipEXE)" install json
& "$($PipEXE)" install pathlib
#& "$($PipEXE)" install os
#& "$($PipEXE)" install contextlib
& "$($PipEXE)" install websocket-client
& "$($PipEXE)" install websockets
& "$($PipEXE)" install pytest-playwright playwright -U
& "$($PipEXE)" install openpyxl
& "$($PipEXE)" install pandas
& "$($PipEXE)" install ast
& "$($PipEXE)" install csv
& "$($PipEXE)" install threading
& "$($PipEXE)" install multiprocessing 
& "$($PipEXE)" install itertools
& "$($PipEXE)" install datetime
& "$($PipEXE)" install numpy
& "$($PipEXE)" install numba
& "$($PipEXE)" install pyopencl

& "$($PipEXE)" install  --upgrade pyppeteer
& "$($PipEXE)" install  --upgrade asyncio

& "$($PipEXE)" install  --upgrade requests
#& "$($PipEXE)" install  --upgrade json
& "$($PipEXE)" install  --upgrade pathlib
#& "$($PipEXE)" install  --upgrade os
#& "$($PipEXE)" install  --upgrade contextlib
& "$($PipEXE)" install  --upgrade websocket-client
& "$($PipEXE)" install  --upgrade websockets
& "$($PipEXE)" install  --upgrade pytest-playwright playwright -U
& "$($PipEXE)" install  --upgrade pytest-playwright playwright
& "$($PipEXE)" install  --upgrade openpyxl
& "$($PipEXE)" install  --upgrade pandas
& "$($PipEXE)" install  --upgrade ast
& "$($PipEXE)" install  --upgrade csv
& "$($PipEXE)" install  --upgrade threading
& "$($PipEXE)" install  --upgrade multiprocessing 
& "$($PipEXE)" install  --upgrade itertools
& "$($PipEXE)" install  --upgrade datetime
& "$($PipEXE)" install  --upgrade numpy
& "$($PipEXE)" install  --upgrade numba
& "$($PipEXE)" install  --upgrade pyopencl

EXIT
