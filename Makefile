all:.\ictye-live-dm\start.exe

.\ictye-live-dm\start.exe:.\launcher\recours.res
	cl /std:c++20 /Zi /EHsc /nologo /Fe.\ictye-live-dm\start.exe .\launcher\start.cpp .\launcher\recours.res

.\launcher\recours.res:.\launcher\recours.rc
	rc /r .\launcher\recours.rc
.\ictye-live-dm\src\ictye_live_dm\GUI\Ui_MainWindow.py:
	.\venv\Scripts\active.bat
	pyuic5  .\ictye-live-dm\src\QT-GUI\main.ui -o .\ictye-live-dm\src\ictye_live_dm\GUI\Ui_MainWindow.py

clean:
	del .\launcher\start.obj .\ictye-live-dm\start.exe .\ictye-live-dm\*.pdb .\launcher\*.res .\ictye-live-dm\*.ilk