Unicode True

!include MUI2.nsh

Name "ictye-live-dm"
OutFile "ictye-live-dm-installer-x86_64.exe"
InstallDir "$PROGRAMFILES\ictye-live-dm"
Icon "ictye-live-dm\icon.ico"

Var StartMenuFolder

!insertmacro MUI_LANGUAGE "SimpChinese"


;协议
!define MUI_LICENSEPAGE_TEXT_TOP "请阅读并同意此许可（写点废话不行嘛。。。。。。）"
!define MUI_LICENSEPAGE_BUTTON "下一步"
!define MUI_LICENSEPAGE_TEXT_BOTTOM "确保仔细阅读，同意此协议然后下一步喵"
!define MUI_LICENSEPAGE_RADIOBUTTONS
!define MUI_LICENSEPAGE_RADIOBUTTONS_TEXT_ACCEPT "同意"
!define MUI_LICENSEPAGE_RADIOBUTTONS_TEXT_DECLINE "我拒绝签字"
!insertmacro MUI_PAGE_LICENSE "LICENSE"

;开始菜单选单
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\ictye-live-dm" 
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!define MUI_ABORTWARNING
!define MUI_FINISHPAGE_NOAUTOCLOSE

RequestExecutionLevel admin

Section "MainSection" SEC01

    SetOutPath "$INSTDIR"
    File /r "ictye-live-dm\*.*"

    WriteUninstaller "$INSTDIR\uninstall.exe"

    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ictye-live-dm" "DisplayName" "ictye-live-dm"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ictye-live-dm" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ictye-live-dm" "DisplayName" "ictye-live-dm"

    SetShellVarContext current
    CreateShortCut "$DESKTOP\ictye-live-dm.lnk" "$INSTDIR\start.exe" 
    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    CreateShortCut "$SMPROGRAMS\$StartMenuFolder\ictye-live-dm.lnk" "$INSTDIR\start.exe"
SectionEnd

Section "Uninstall"

    Delete "$INSTDIR\uninstall.exe"
    RMDir /r "$INSTDIR"

    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ictye-live-dm"
    DeleteRegKey HKLM "Software\ictye-live-dm"

    Delete "$SMPROGRAMS\$StartMenuFolder\ictye-live-dm.lnk"
    Delete "$DESKTOP\ictye-live-dm.lnk"

    RMDir "$SMPROGRAMS\$StartMenuFolder"

    StrCpy $0 $APPDATA
    RMDir /r "$0/ictye-live-dm"

SectionEnd
