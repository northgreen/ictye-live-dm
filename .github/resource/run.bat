@Set PATH=%~dp0:%~dp0Scripts:%PATH%
@Set root=%~dp0
@Set root=%root:\=\\%
@(Set /p=%root%) <NUL> %~dp0\lib\site-package\WindPy.pth
"./bin/python.exe" -m pip install -r ./requirements.txt
"./bin/python.exe" ./
pause
