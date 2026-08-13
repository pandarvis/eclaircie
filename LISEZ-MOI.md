# L'ÉCLAIRCIE — atelier

Espace de travail du roman. Ce fichier décrit où va quoi.

> **L'irréparable est condamné, le réparable est pardonné, le meurtri est gracié.**

---

## Le point d'entrée

**[`L-ECLAIRCIE-dossier-complet.md`](L-ECLAIRCIE-dossier-complet.md)** — le dossier de création, à la racine.
C'est la source de vérité : univers, système, personnages, plan, règles d'écriture.
Tout le reste en découle. Il reste à la racine exprès : on ne le cherche pas.

---

## L'arborescence

| Dossier | Ce qu'on y met |
|---|---|
| `01-dossier/` | Annexes et développements du dossier maître — notes de doctrine, arbitrages, versions de travail d'une section |
| `02-univers/` | Le système : barème du décompte, chronologie du monde, lexique, institutions, géographie, ce que croient les veilleurs |
| `03-personnages/` | Une fiche par personnage. Le veilleur, elle, le garçon, les jumelles, les seconds rôles |
| `04-plan/` | Le plan et ses états successifs : séquencier, découpage en chapitres, arcs par personnage |
| `05-manuscrit/chapitres/` | Le texte. Un fichier par chapitre |
| `06-visuels/` | Tout ce qui se regarde : frises, schémas, cartes, moodboards |
| `07-recherches/` | Documentation, références, notes de lecture, ce qui vient de dehors |
| `99-archives/` | Ce qu'on abandonne sans vouloir le perdre. Rien ne se supprime, tout descend ici |

---

## Ce qui s'y trouve déjà

### `01-dossier/`
- **[`les-interdits.md`](01-dossier/les-interdits.md)** — ⚠️ **la liste de référence.** Les quatre interdits du §14, plus six dérivés. Numérotation figée : on y renvoie par leur numéro.
- **[`notes-en-vrac-2026-08-13.md`](01-dossier/notes-en-vrac-2026-08-13.md)** — dépôt brut d'une session d'idées, avec le statut de chacune et où elle a été développée.

### `02-univers/`
- **[`la-ruche.md`](02-univers/la-ruche.md)** — comment ça marche : l'Archiviste, la maturation, l'éclaircie, les travées, l'instrument qui mesure l'âge.
- **[`la-terre.md`](02-univers/la-terre.md)** — le monde est la Terre. Ce qui est identique, ce qui a été réécrit, et comment le montrer sans le dire.
- **[`ce-qui-est-juge.md`](02-univers/ce-qui-est-juge.md)** — ce qui est jugé, c'est la vie, pas la mort. Le barème du verdict.
- **[`les-ages-croises.md`](02-univers/les-ages-croises.md)** — le décompte du couple d'un monde à l'autre, et la règle des retrouvailles.
- **[`la-jalousie.md`](02-univers/la-jalousie.md)** — le mécontentement ordinaire, la violence, l'insécurité. Développement du §9.5.

### `03-personnages/`
**[`veilleur.md`](03-personnages/veilleur.md)** — fiche du protagoniste : sa mort, sa faute, la réplique, ce qui reste à trouver.

### `04-plan/`
**[`incidences-2026-08-13.md`](04-plan/incidences-2026-08-13.md)** — ce que les nouvelles idées changent, mouvement par mouvement.

### `06-visuels/frise-narrative/`

**[`frise-narrative.html`](06-visuels/frise-narrative/frise-narrative.html)** — la frise du récit, à ouvrir dans un navigateur.
Défilement horizontal, 24 mouvements, 4 actes, 4 voies narratives : *le monde*, *l'enquête*, *elle*, *le voile*.
La frise s'éclaircit de gauche à droite. Voir le [carnet du dossier](06-visuels/frise-narrative/NOTES.md).

Version en ligne : <https://claude.ai/code/artifact/278c6576-e781-4aad-86ff-135f9932ef11>

---

## Conventions

- **On valide avant d'intégrer.** Toute modification du récit est d'abord proposée et discutée. Elle n'entre dans la frise narrative qu'une fois validée. Les propositions en attente restent dans les fichiers de travail, marquées *à valider*.
- **Nommer en clair, sans accents ni espaces** dans les noms de fichiers : `veilleur.md`, `bareme-decompte.md`.
- **Dater les états de travail** quand plusieurs coexistent : `plan-2026-08-13.md`.
- **Le dossier maître ne se réécrit pas à la légère.** On travaille en annexe dans `01-dossier/`, puis on remonte ce qui est tranché.
- **Ce qui est abandonné descend dans `99-archives/`**, jamais à la corbeille.

---

## L'historique

L'atelier est sous **git**. Tout est versionné : chaque état du dossier est récupérable, et rien n'est jamais réellement perdu, même si un fichier est écrasé ou supprimé par erreur.

Les commandes utiles, à lancer depuis ce dossier :

```bash
git log --oneline
```

```bash
git status
```

Pour retrouver un fichier tel qu'il était à un état donné :

```bash
git show <numéro-de-commit>:chemin/du/fichier.md
```

Les **étapes marquantes** sont marquées par des tags (`v1`, `v2`…), qu'on pose quand un jalon du dossier est atteint. Pour les lister :

```bash
git tag -l -n1
```
