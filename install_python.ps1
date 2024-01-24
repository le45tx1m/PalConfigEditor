
$ErrorActionPreference = "Stop"

$DxUrl = "https://www.python.org/ftp/python/3.11.0/python-3.11.0rc1.exe"
$DxOutput = "C:\Program Files\PalServer\pythoninstall.exe"
Invoke-WebRequest -Uri $DxUrl -OutFile $DxOutput
Write-Host "Installing python.exe..."
Start-Process -FilePath $DxOutput -Args '/quiet InstallAllUsers=1 PrependPath=1 Include_test=0' -Wait
Remove-Item -Path $DxOutput

pip install Flask
pip install psutil
python app.py