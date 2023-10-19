$work_path = $PWD.Path
Write-Output $work_path

Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.6/python-3.11.6-embed-amd64.zip" -OutFile "$work_path/python.zip"
mkdir $work_path/ictye-live-dm/bin
Expand-Archive -LiteralPath "$work_path/python.zip" -DestinationPath "$work_path/ictye-live-dm/bin"
&"$work_path/ictye-live-dm/bin/python.exe" "$work_path/ictye-live-dm/bin/get-pip.py"

$file_path = Join-Path $work_path "ictye-live-dm/bin/python38._pth"
$lines = Get-Content -Path $file_path
$updatedLines = @()

foreach ($line in $lines) {
    if ($line.Trim().StartsWith("#") -and $line.Contains("import site")) {
        $updatedLines += $line.TrimStart("#")
    } else {
        $updatedLines += $line
    }
}

$updatedLines | Set-Content -Path $file_path



Write-Output @Set PATH=%%~dp0:%%~dp0Scripts:%%PATH%% > $work_path/ictye-live-dm/run.bat 
Write-Output @Set root=%%~dp0 >> $work_path/ictye-live-dm/run.bat
Write-Output @Set root=%%root:\=\\%% >> $work_path/ictye-live-dm/run.bat
Write-Output @(Set /p=%%root%%) `<NUL`> %%~dp0\lib\site-package\WindPy.pth >> $work_path/ictye-live-dm/run.bat
Write-Output ./bin/python.exe -m ./ >> $work_path/ictye-live-dm/run.bat

Compress-Archive -Path $work_path/ictye-live-dm/* -DestinationPath $GITHUB_WORKSPACE/ictye-live-dm.zip

Get-ChildItem $work_path
Get-ChildItem $work_path/ictye-live-dm/
tree /f $work_path
