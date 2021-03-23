!define PACKAGE_NAME "octanescript-installer"
!define VERSION "DEV" 

Name "OctaneScript ${VERSION}"
OutFile "${PACKAGE_NAME}.exe"
InstallDir "C:\Program Files\OctaneScript"
ShowInstDetails Show

!include "MUI2.nsh"
!define MUI_ICON "../images/octanescript_logo.ico"
!define MUI_UNICON "../images/octanescript_logo.ico"
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "OctaneScript"
!define MUI_LICENSEPAGE_TEXT_TOP "LICENSE INFORMATION"
!define MUI_LICENSEPAGE_TEXT_BOTTOM "Please review the license if you are considering using this software for anything more than exploration and learning."
!define MUI_LICENSEPAGE_BUTTON "Next"
!insertmacro MUI_PAGE_LICENSE "../src/dist/LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
 
Section
    SetOutPath $INSTDIR
	
	File "os.exe"
	File "LICENSE"
 
    WriteUninstaller "$INSTDIR\uninstall.exe"
	
SectionEnd
 
Section "uninstall"
    Delete "$INSTDIR\uninstall.exe"
    RMDir $INSTDIR
SectionEnd
