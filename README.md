# L'Éclaircie

*Un roman en cours d'écriture, et l'atelier qui sert à l'écrire.*

> **L'irréparable est condamné, le réparable est pardonné, le meurtri est gracié.**

---

**Écrit à ce jour : 8 776 mots** — le prologue, le chapitre premier, l'épilogue.
Trente-cinq scènes restent à écrire.

| | | |
|---|---|---:|
| **Prologue** | [La cérémonie](05-manuscrit/chapitres/L-Eclaircie-Prologue.pdf) | 2 655 mots |
| **Chapitre premier** | [Une journée à la ruche](05-manuscrit/chapitres/L-Eclaircie-Chapitre-1.pdf) | 3 490 mots |
| **Épilogue** | [Épilogue](05-manuscrit/chapitres/L-Eclaircie-Epilogue.pdf) | 2 631 mots |

---

## L'atelier

**[`06-visuels/atelier/atelier.html`](06-visuels/atelier/atelier.html)** — un seul fichier,
aucune dépendance, aucun appel réseau. Il s'ouvre d'un double-clic et contient tout : la
frise des scènes, les textes, les notes datées, le lexique, les règles, les interdits, le
glossaire, les personnages, les questions ouvertes et le plan de la ruche.

**C'est la source de vérité du projet.** Les fichiers Markdown sont les développements —
en cas de désaccord, l'atelier a raison.

Il ne s'édite jamais à la main : on modifie un des douze morceaux de
[`06-visuels/atelier/sources/`](06-visuels/atelier/sources/), puis

```bash
cd 06-visuels/atelier/sources && sh fabriquer.sh
```

qui refabrique, vérifie la syntaxe et fait passer le contrôleur de cohérence.

## Où va quoi

| | |
|---|---|
| [`LISEZ-MOI.md`](LISEZ-MOI.md) | **le point d'entrée détaillé** |
| [`CONTRIBUER.md`](CONTRIBUER.md) | comment on travaille : gitflow, contrôles, la règle qui prime |
| [`01-dossier/le-style.md`](01-dossier/le-style.md) | le style du livre, établi en mesurant les textes |
| [`05-manuscrit/`](05-manuscrit/) | le texte, un PDF par chapitre, et le glossaire de fin de volume |
| [`06-visuels/`](06-visuels/) | l'atelier, le plan de la ruche, les trois plans du jardin |
| `02-univers/` · `03-personnages/` · `04-plan/` | le monde, les gens, l'architecture du récit |

## Les outils

| | |
|---|---|
| `valide.js` | contrôle la cohérence de l'atelier : scènes, liens, textes, mots proscrits |
| `analyse-style.py` | mesure les textes : temps, longueurs de phrase, répétitions, ambiguïtés |
| `controler-un-texte.py` | passe un brouillon au même contrôle |
| `verifier-le-plan-du-jardin.py` | vérifie par le calcul qu'aucun bâtiment ne déborde du mur |

---

*Écrit par Élodie. Rien du récit n'est figé : elle valide, l'atelier suit.*
