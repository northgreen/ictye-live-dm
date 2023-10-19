Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.6/python-3.11.6-embed-amd64.zip" -OutFile "$GITHUB_WORKSPACE/python.zip"
mkdir $GITHUB_WORKSPACE/ictye-live-dm/bin
Expand-Archive -LiteralPath "$GITHUB_WORKSPACE/python.zip" -DestinationPath "$GITHUB_WORKSPACE/ictye-live-dm/bin"
Get-ChildItem $GITHUB_WORKSPACE
Get-ChildItem $GITHUB_WORKSPACE/ictye-live-dm/
tree /f $GITHUB_WORKSPACE
