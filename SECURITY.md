# Sécurité

## Modèle de sécurité

2Webp ne contient aucune fonction réseau, télémétrie ou collecte de données. Les conversions sont réalisées localement avec Pillow.

## Vérification des téléchargements

Chaque release doit fournir `SHA256SUMS.txt`. Sous PowerShell :

```powershell
Get-FileHash .\2Webp-v0.8.0-portable.exe -Algorithm SHA256
```

Comparer la valeur obtenue à celle publiée avec la release.

## Signature de code

Les binaires ne sont pas signés tant qu'un certificat de signature de code n'est pas configuré. Un avertissement SmartScreen est donc possible.

## Signaler une vulnérabilité

Ne pas publier de données privées ou d'images confidentielles dans une issue publique. Indiquer :

- version ;
- Windows ;
- étapes ;
- impact ;
- preuve minimale.

En l'absence de canal privé dédié, contacter l'auteur via le site officiel avant publication d'une faille exploitable.
