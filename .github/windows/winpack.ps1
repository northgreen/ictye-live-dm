$work_path = $PWD.Path
Write-Output $work_path

Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.6/python-3.11.6-embed-amd64.zip" -OutFile "$work_path/python.zip"
mkdir $work_path/ictye-live-dm/bin
Expand-Archive -LiteralPath "$work_path/python.zip" -DestinationPath "$work_path/ictye-live-dm/bin"
Get-ChildItem $work_path
Get-ChildItem $work_path/ictye-live-dm/
tree /f $work_path
