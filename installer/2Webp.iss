#ifndef MyAppVersion
  #define MyAppVersion "0.8.0"
#endif

#define MyAppName "2Webp"
#define MyAppPublisher "Jean-Philippe Bloch"
#define MyAppURL "https://www.jpbloch.fr"
#define MyAppRepo "https://github.com/birk6788/2Webp"
#define MyAppExeName "2Webp.exe"

[Setup]
AppId={{D988893A-0F7B-4B97-A9D9-772B58D9C2F6}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppRepo}
AppUpdatesURL={#MyAppRepo}/releases
DefaultDirName={localappdata}\Programs\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=..\LICENSE
OutputDir=..\release
OutputBaseFilename=2Webp-v{#MyAppVersion}-setup
SetupIconFile=..\assets\brand\2Webp-taskbar-round.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "Créer un raccourci sur le Bureau"; GroupDescription: "Raccourcis :"; Flags: unchecked

[Files]
Source: "..\dist\onedir\2Webp\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\2Webp"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\2Webp"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Lancer 2Webp"; Flags: nowait postinstall skipifsilent
