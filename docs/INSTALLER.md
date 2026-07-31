# Installateur Windows

L'installateur utilise Inno Setup 6 et le script `installer/2Webp.iss`.

## Comportement

- installation par utilisateur dans `%LOCALAPPDATA%\Programs\2Webp` ;
- pas de privilèges administrateur obligatoires ;
- raccourci menu Démarrer ;
- raccourci bureau optionnel ;
- désinstallation standard Windows ;
- conservation des préférences dans `%APPDATA%\2Webp` lors d'une désinstallation.

## Compilation manuelle

```powershell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" `
  "/DMyAppVersion=0.8.0" `
  ".\installer\2Webp.iss"
```

## Signature

Aucune signature de code n'est actuellement configurée. L'installateur et l'exécutable peuvent donc déclencher SmartScreen.
