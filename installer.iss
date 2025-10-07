[Setup]
AppName=Av-PDF
AppVersion=1.2
DefaultDirName={pf}\Av-PDF
DefaultGroupName=Av-PDF
OutputDir=dist-installer
OutputBaseFilename=Av-PDF-Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=dist\Av-PDF\_internal\icono.ico
UninstallDisplayIcon={app}\_internal\icono.ico


[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
; Ejecutable principal
Source: "dist\Av-PDF\Av-PDF.exe"; DestDir: "{app}"; Flags: ignoreversion

; Iconos e imágenes
Source: "dist\Av-PDF\_internal\icono.ico"; DestDir: "{app}\_internal"; Flags: ignoreversion
Source: "dist\Av-PDF\_internal\icono_16.png"; DestDir: "{app}"; Flags: ignoreversion

; Carpeta _internal que contiene todo lo demás (pyd, recursos, dlls, etc.)
Source: "dist\Av-PDF\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Acceso directo escritorio
Name: "{commondesktop}\Av-PDF"; Filename: "{app}\Av-PDF.exe"; WorkingDir: "{app}"

; Acceso directo menú inicio
Name: "{group}\Av-PDF"; Filename: "{app}\Av-PDF.exe"

[Registry]
; Asociar Av-PDF como opción en "Abrir con"
Root: HKCR; Subkey: "Applications\Av-PDF.exe\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Av-PDF.exe"" ""%1"""
Root: HKCR; Subkey: "Applications\Av-PDF.exe"; ValueType: string; ValueName: "FriendlyAppName"; ValueData: "Av-PDF"
Root: HKCR; Subkey: "Applications\Av-PDF.exe\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\_internal\icono.ico"
Root: HKCR; Subkey: ".pdf\OpenWithProgids"; ValueType: none; ValueName: "Applications\Av-PDF.exe"; Flags: uninsdeletevalue

; Limpieza completa al desinstalar
Root: HKCR; Subkey: "Applications\Av-PDF.exe\DefaultIcon"; Flags: deletekey
Root: HKCR; Subkey: "Applications\Av-PDF.exe"; Flags: deletekey uninsdeletekeyifempty

; OPCIONAL: Para hacer Av-PDF el visor predeterminado de PDFs (descomenta si deseas usarlo)
;Root: HKCR; Subkey: ".pdf"; ValueType: string; ValueName: ""; ValueData: "AvPDFFile"; Flags: uninsdeletevalue
;Root: HKCR; Subkey: "AvPDFFile"; ValueType: string; ValueName: ""; ValueData: "Documento Av-PDF"
;Root: HKCR; Subkey: "AvPDFFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\_internal\icono.ico"
;Root: HKCR; Subkey: "AvPDFFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Av-PDF.exe"" ""%1"""

; Registro adicional para asegurar visibilidad en "Abrir con"
Root: HKCU; Subkey: "Software\Classes\Applications\Av-PDF.exe\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Av-PDF.exe"" ""%1"""
Root: HKCU; Subkey: "Software\Classes\Applications\Av-PDF.exe"; ValueType: string; ValueName: "FriendlyAppName"; ValueData: "Av-PDF"
Root: HKCU; Subkey: "Software\Classes\Applications\Av-PDF.exe\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\_internal\icono.ico"
Root: HKCU; Subkey: "Software\Classes\.pdf\OpenWithProgids"; ValueType: none; ValueName: "Applications\Av-PDF.exe"; Flags: uninsdeletevalue


[Run]
Filename: "{app}\Av-PDF.exe"; Description: "Iniciar Av-PDF"; Flags: nowait postinstall skipifsilent
