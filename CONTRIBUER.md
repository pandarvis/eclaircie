# Comment on travaille sur ce dépôt

*Gitflow, adapté à un roman. Deux branches permanentes, des branches de travail éphémères.*

---

## Les deux branches permanentes

| Branche | Ce qu'elle contient |
|---|---|
| **`main`** | uniquement des états publiés, chacun portant un tag `vX.Y.Z`. On n'y commite jamais directement |
| **`develop`** | le travail en cours, toujours cohérent : l'atelier s'y fabrique et le contrôleur y passe |

## Les branches de travail

| Préfixe | Pour quoi | Part de | Retourne dans |
|---|---|---|---|
| `feature/` | une scène, un chapitre, un document, un outil | `develop` | `develop` |
| `release/` | la préparation d'une version : relectures, PDF, numéros | `develop` | `main` **et** `develop` |
| `hotfix/` | une correction qui ne peut pas attendre la prochaine version | `main` | `main` **et** `develop` |

**Nommer en clair, sans accents :** `feature/chapitre-2-le-registre`,
`feature/plan-du-jardin`, `release/0.2.0`.

## Le cycle

```bash
git switch develop && git pull
git switch -c feature/chapitre-2-le-registre
```

On écrit. On commite souvent, avec des messages qui disent ce que la décision change et
pourquoi — *pas* ce que le fichier contient.

```bash
cd 06-visuels/atelier/sources && sh fabriquer.sh
```

**Une branche ne se fusionne pas si le contrôleur ne passe pas.** `fabriquer.sh` enchaîne la
fabrication, la vérification de syntaxe et `valide.js`. Un brouillon de texte se contrôle en
plus avec `controler-un-texte.py`.

```bash
git switch develop
git merge --no-ff feature/chapitre-2-le-registre
git branch -d feature/chapitre-2-le-registre
```

`--no-ff` garde la trace de la branche dans l'historique : on voit ce qui a été fait
ensemble, et on peut le défaire d'un bloc.

## Publier une version

```bash
git switch -c release/0.2.0 develop
```

Sur la branche de release : les relectures, les PDF régénérés, les compteurs mis à jour dans
les `LISEZ-MOI`. Rien de neuf ne s'y écrit.

```bash
git switch main && git merge --no-ff release/0.2.0
git tag -a v0.2.0 -m "..."
git switch develop && git merge --no-ff release/0.2.0
git branch -d release/0.2.0
git push origin main develop --follow-tags
```

## Les tags

Deux familles, et elles ne se mélangent pas.

- **`etape-NN`** — les jalons du récit. `etape-10` est *Une journée à la ruche*.
  Ils ne suivent aucune numérotation de version et ne se comparent pas entre familles.
- **`vX.Y.Z`** — les versions publiées, sur `main` uniquement.
  `0.Y.Z` tant que le roman n'est pas fini.

## Ce qui ne se commite jamais

`check.js`, `combo.js`, les pages d'impression intermédiaires, les sondes de vérification.
Tout est dans `.gitignore` — et tout se régénère.

## La règle qui prime sur les autres

**On valide avec l'autrice avant d'intégrer.** Une branche peut contenir dix propositions ;
aucune n'entre dans `develop` sans son accord, et rien ne touche à la frise narrative sans
qu'elle l'ait dit.
