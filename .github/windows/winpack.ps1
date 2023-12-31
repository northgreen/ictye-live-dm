$work_path = $PWD.Path
Write-Output $work_path

Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.6/python-3.11.6-embed-amd64.zip" -OutFile "$work_path/python.zip"
mkdir $work_path/ictye-live-dm/bin
Expand-Archive -LiteralPath "$work_path/python.zip" -DestinationPath "$work_path/ictye-live-dm/bin"
Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "$work_path/ictye-live-dm/bin/get-pip.py"
&"$work_path/ictye-live-dm/bin/python.exe" "$work_path/ictye-live-dm/bin/get-pip.py"


<#移除py311.pthimport site前的井号#>
$file_path = Join-Path $work_path "ictye-live-dm/bin/python311._pth"
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



Copy-Item .\.github\resource\run.bat .\ictye-live-dm\

Compress-Archive -Path $work_path/ictye-live-dm/* -DestinationPath $work_path/ictye-live-dm.zip

Write-Debug "打包完成"