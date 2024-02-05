all:.\ictye-live-dm\start.exe

.\ictye-live-dm\start.exe:.\launcher\recours.res
	cl /std:c++20 /Zi /EHsc /nologo /Fe.\ictye-live-dm\start.exe .\launcher\start.cpp .\launcher\recours.res

.\launcher\recours.res:.\launcher\recours.rc
	rc /r .\launcher\recours.rc

clean:
	del .\launcher\start.obj .\ictye-live-dm\start.exe .\ictye-live-dm\*.pdb .\launcher\*.res .\ictye-live-dm\*.ilk