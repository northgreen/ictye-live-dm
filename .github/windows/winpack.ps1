$work_path = $PWD.Path
Write-Output $work_path

<#下载python#>
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.6/python-3.11.6-embed-amd64.zip" -OutFile "$work_path/python.zip"
mkdir $work_path/src/bin
Expand-Archive -LiteralPath "$work_path/python.zip" -DestinationPath "$work_path/ictye-live-Danmku/bin"
Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "$work_path/ictye-live-Danmku/bin/get-pip.py"
&"$work_path/ictye-live-Danmku/bin/python.exe" "$work_path/ictye-live-Danmku/bin/get-pip.py"

<#配置内置python环境#>
<#移除py311.pthimport site前的井号#>
$file_path = Join-Path $work_path "ictye-live-Danmku/bin/python311._pth"
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

<#构建启动器#>
Copy-Item $work_path\icon.ico $work_path\launcher
nmake
mkdir $work_path\src\plugin


Copy-Item $work_path\.github\resource\run.bat $work_path\src\

<#打包压缩包#>
Compress-Archive -Path $work_path/src/* -DestinationPath $work_path/ictye-live-Danmku.zip

Write-Debug "打包完成"