# L'ÉCLAIRCIE — atelier

Espace de travail du roman. Ce fichier décrit où va quoi.

> **L'irréparable est condamné, le réparable est pardonné, le meurtri est gracié.**

---

## Par où commencer

**[`06-visuels/atelier/atelier.html`](06-visuels/atelier/atelier.html)** — double-clic, ça s'ouvre dans le navigateur.
**C'est la source de vérité.** Les textes du livre, la frise, les notes datées, le lexique, les règles, les interdits, les personnages, les questions ouvertes, le plan de la ruche : tout y est, et tout y est à jour.

**Les fichiers Markdown du dossier sont les développements** — ce que l'atelier résume, eux le détaillent. *En cas de désaccord entre les deux, l'atelier a raison :* c'est lui qu'on met à jour à chaque décision.

---

## L'arborescence

| Dossier | Ce qu'on y met |
|---|---|
| `01-dossier/` | doctrine, interdits, arbitrages, et les paroles brutes de l'autrice |
| `02-univers/` | le système : la ruche, le jardin, le corps, le décompte, ce qui est jugé |
| `03-personnages/` | une fiche par personnage |
| `04-plan/` | l'architecture, le calendrier, le parcours de l'enquête, les faux raccords |
| `05-manuscrit/` | le texte : un PDF par chapitre, les brouillons en cours |
| `06-visuels/` | l'atelier, le plan de la ruche, les plans du jardin |
| `07-recherches/` | ce qui vient de dehors : références, notes de lecture |
| `08-références/` | les images passées par l'autrice |
| `99-archives/` | ce qu'on abandonne sans vouloir le perdre |

---

## Ce qui est écrit du roman

| | Chapitre | Mots | Scène |
|---|---|---|---|
| **Prologue** | [La cérémonie](05-manuscrit/chapitres/L-Eclaircie-Prologue.pdf) | 2 655 | `ouv` |
| **Chapitre premier** | [Une journée à la ruche](05-manuscrit/chapitres/L-Eclaircie-Chapitre-1.pdf) | 3 490 | `capsule` |
| **Épilogue** | [Épilogue](05-manuscrit/chapitres/L-Eclaircie-Epilogue.pdf) | 2 631 | `jardin-fin` |

**8 776 mots.** Trente-cinq scènes restent à écrire.

---

## Les documents à connaître

**[`01-dossier/les-interdits.md`](01-dossier/les-interdits.md)** — ⚠️ la liste de référence. Onze interdits, numérotation figée : on y renvoie par leur numéro.
**[`04-plan/deux-histoires-en-une.md`](04-plan/deux-histoires-en-une.md)** — ⚠️ l'architecture du roman. Deux enlèvements racontés comme un seul récit.
**[`04-plan/faux-raccords.md`](04-plan/faux-raccords.md)** — les dissonances semées pour qu'on comprenne, à la relecture, qu'on suivait deux hommes.
**[`01-dossier/paroles-brutes-2026-08-13-16.md`](01-dossier/paroles-brutes-2026-08-13-16.md)** — les mots de l'autrice, tels quels. Ne se réécrit jamais.
**[`L-ECLAIRCIE-dossier-complet.md`](L-ECLAIRCIE-dossier-complet.md)** — le dossier de création d'origine. **Périmé sur ses conclusions**, gardé pour ses `§` que tout le dossier cite.

---

## Conventions

- **On valide avant d'intégrer.** Toute modification du récit est discutée avant d'entrer dans la frise.
- **L'atelier se met à jour à chaque décision** — un atelier qui retarde d'une séance ne sert plus à rien.
- **On n'édite jamais `atelier.html` à la main :** on édite un morceau dans [`06-visuels/atelier/sources/`](06-visuels/atelier/sources/LISEZ-MOI.md), puis `sh fabriquer.sh`.
- **Nommer en clair**, sans accents ni espaces dans les noms de fichiers.
- **Dater les états de travail** quand plusieurs coexistent.
- **Ce qui est abandonné descend dans `99-archives/`**, jamais à la corbeille.

---

## L'historique

Tout est sous **git** : rien n'est jamais perdu, même supprimé.

```bash
git tag -l -n1
```

Les **étapes** sont marquées par des tags annotés. `v1` à `v10` suivent la construction du monde puis l'écriture ; **`v1.0`** marque le premier état livrable — trois textes, l'atelier complet — posé le 19 août 2026 juste avant le grand nettoyage.

Pour retrouver un fichier tel qu'il était :

```bash
git show v1.0:chemin/du/fichier.md
```
