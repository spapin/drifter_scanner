[Setup]
AppName=Drifter Scanner
AppVersion=0.1.0
AppPublisher=spapin
AppPublisherURL=https://github.com/spapin/drifter_scanner
DefaultDirName={autopf}\Drifter Scanner
DefaultGroupName=Drifter Scanner
UninstallDisplayIcon={app}\drifter-scanner.exe
OutputBaseFilename=DrifterScannerSetup
SetupIconFile=drifter_scanner\resources\WCBR_logo.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible

[Files]
Source: "dist\drifter-scanner.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Drifter Scanner"; Filename: "{app}\drifter-scanner.exe"
Name: "{group}\Uninstall Drifter Scanner"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Drifter Scanner"; Filename: "{app}\drifter-scanner.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"
