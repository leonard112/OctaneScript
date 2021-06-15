!define PACKAGE_NAME "octanescript-installer"
!define VERSION "DEV" 

Name "OctaneScript ${VERSION}"
OutFile "${PACKAGE_NAME}.exe"
InstallDir "C:\Program Files\OctaneScript"
ShowInstDetails Show
ManifestDPIAware true

!include "MUI2.nsh"

!define MUI_ICON "octanescript-logo.ico"
!define MUI_UNICON "octanescript-logo.ico"
!define MUI_WELCOMEFINISHPAGE_BITMAP "octanescript-logo.bmp"
!define MUI_WELCOMEPAGE_TITLE_3LINES
!define MUI_WELCOMEPAGE_TEXT "$\nOctaneScript is a scripting language built using Python.$\n$\nNote that this language is not being developed for any customer or particular use. This lanauge is being developed for fun. Feel free to use this software for whatever you wish, but ensure that you review this software's license (MIT) if you consider using this software for anything more than exploration and learning."
!define MUI_FINISHPAGE_TITLE_3LINES
!define MUI_FINISHPAGE_TEXT "$\n$\n$\nOctaneScript has been installed on your computer.$\n$\nClick Finish to close Setup.$\n$\n$\n$\n$\n$\n$\n$\n$\nOctaneScript is maintained at:"
!define MUI_FINISHPAGE_LINK "https://github.com/leonard112/OctaneScript"
!define MUI_FINISHPAGE_LINK_LOCATION "https://github.com/leonard112/OctaneScript"
!define MUI_LICENSEPAGE_TEXT_TOP ""
!define MUI_LICENSEPAGE_TEXT_BOTTOM "$\nBy clicking $\"I Agree$\", you accept the terms of the license."
!define MUI_ABORTWARNING
!define MUI_UNABORTWARNING
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_UNFINISHPAGE_NOAUTOCLOSE

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"
 
Section
    SetOutPath $INSTDIR
	
	File "os.exe"
	File "LICENSE"
 
    WriteUninstaller "$INSTDIR\uninstall.exe"
	EnVar::AddValue "PATH" "$INSTDIR\"
	Pop $0
	DetailPrint "EnVar::AddValue returned=|$0|"
SectionEnd
 
Section "uninstall"
	Delete "$INSTDIR\os.exe"
	Delete "$INSTDIR\LICENSE"
	Delete "$INSTDIR\uninstall.exe"
    RMDir $INSTDIR
	EnVar::DeleteValue "PATH" "$INSTDIR\"
	Pop $0
	DetailPrint "EnVar::DeleteValue returned=|$0|"
SectionEnd