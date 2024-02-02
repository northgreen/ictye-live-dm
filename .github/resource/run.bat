@echo off
echo installing require
"./bin/python.exe" -m pip install -r ./requirements.txt

for /R ./plugin %%f in (requirements.txt) do (
if exist %%f (
        echo %%~dpf | findstr /I /V /C:"\\__pycache__\\" 1>nul
        if not errorlevel 1 (
            echo Installing packages from: %%f
            "./bin/python.exe" -m pip install -r  "%%f"
        )
    )
)

echo starting
"./bin/python.exe" ./
pause
