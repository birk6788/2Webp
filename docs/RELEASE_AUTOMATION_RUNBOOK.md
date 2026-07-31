# Windows release automation runbook

## Objectif

Construire et publier 2Webp pour Windows sans commandes manuelles fragiles, tout en conservant les logs lorsqu'un build échoue.

## Incidents rencontrés le 31 juillet 2026

### 1. GitHub CLI non authentifié

Symptôme :

```text
You are not logged into any GitHub hosts.
```

Cause : `gh` était installé mais aucun compte GitHub n'était authentifié localement.

Prévention : tous les scripts vérifient désormais `gh auth status` avant toute action et indiquent `gh auth login` si nécessaire.

### 2. Remote `origin` absent

Symptôme :

```text
error: No such remote 'origin'
```

Cause : `git remote get-url origin` écrivait sur stderr. Avec PowerShell en mode d'arrêt strict, l'absence normale du remote interrompait le script avant qu'il puisse l'ajouter.

Prévention : `publish-github.ps1` liste maintenant les remotes avec `git remote`, teste explicitement la présence de `origin`, puis l'ajoute ou met son URL à jour.

### 3. Dépôt GitHub déjà initialisé

Le dépôt distant contenait déjà un README. Le dépôt local complet devait rester l'historique de référence.

Prévention : récupération explicite de `origin/main`, puis push protégé par `--force-with-lease`. Le `--force` simple n'est utilisé que si aucune branche `main` distante n'existe réellement.

### 4. Interpréteurs Python différents

Symptôme : les dépendances étaient installées avec Python 3.13, mais le script de build utilisait `py`, qui sélectionnait Python 3.14. Pillow, PySide6 et PyInstaller semblaient alors absents.

Prévention : `build-release.ps1` résout une seule fois l'exécutable `python` fourni par `actions/setup-python`, vérifie les dépendances, puis utilise exactement cet interpréteur pour les tests et PyInstaller.

### 5. Commandes PowerShell multilignes mal concaténées

Symptôme :

```text
unknown flag: --log-failed30613946008
```

Cause : plusieurs blocs copiés à la suite ont fusionné un argument et un identifiant de run.

Prévention : ne plus demander une succession de commandes manuelles pour le diagnostic. Le script `scripts/test-windows-release.ps1` lance le workflow, retrouve son identifiant, attend la fin et affiche automatiquement les logs d'échec.

### 6. Run de diagnostic supprimé trop tôt

Symptôme :

```text
RUN=
failed to get run: HTTP 404: Not Found
```

Cause : le run échoué contenant les seuls logs utiles a été supprimé avant diagnostic.

Prévention : un run échoué ne doit jamais être supprimé avant résolution. Le nouveau script affiche explicitement que le run est conservé. Le nettoyage des anciens runs ne se fait qu'après un build vert et une Release vérifiée.

## Procédure de test

Depuis la racine du dépôt :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-windows-release.ps1
```

Le script :

1. vérifie GitHub CLI et l'authentification ;
2. lance `release-windows.yml` sur `main` ;
3. retrouve automatiquement le nouveau run ;
4. suit son exécution ;
5. affiche automatiquement les logs des étapes en échec ;
6. conserve toujours le run et ses logs.

## Règle de publication

1. Valider un build manuel vert sur `main`.
2. Vérifier les artefacts du workflow.
3. Créer ou déplacer le tag de version seulement après validation.
4. Laisser le push du tag déclencher la vraie GitHub Release.
5. Vérifier l'EXE portable, le ZIP, l'installateur et `SHA256SUMS.txt` avant de supprimer les anciens runs.
