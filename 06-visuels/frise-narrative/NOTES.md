# Frise narrative — carnet

Fichier : [`frise-narrative.html`](frise-narrative.html) — s'ouvre dans un navigateur, autonome, aucune dépendance externe.

**Cinq onglets**, le document sert de référence de travail :

| Onglet | Contenu | Source |
|---|---|---|
| **La frise** | 18 mouvements, 4 actes, 3 voies, les âges à chaque étape | §13 + [`04-plan/`](../../04-plan/) |
| **Le décompte** | Le graphe des vies : chaque courbe descend puis devient plate au jardin | §7 + [`duree-et-calendrier.md`](../../04-plan/duree-et-calendrier.md) |
| **Les interdits** | Les 10, numérotation figée | [`les-interdits.md`](../../01-dossier/les-interdits.md) |
| **La ruche** | Le fonctionnement, en onze blocs | [`la-ruche.md`](../../02-univers/la-ruche.md) |
| **Les phrases** | §16 et les phrases nées en cours de travail | [`phrases-a-garder.md`](../../01-dossier/phrases-a-garder.md) |

*Les onglets documentaires sont des versions condensées : les fichiers du workspace restent la source de vérité. Quand un fichier change, penser à répercuter ici.*
Version en ligne : <https://claude.ai/code/artifact/278c6576-e781-4aad-86ff-135f9932ef11>

Source : section **13. LE PLAN** du [dossier de création](../../L-ECLAIRCIE-dossier-complet.md), corrigée par les décisions du 13 août 2026 (voir [`04-plan/incidences-2026-08-13.md`](../../04-plan/incidences-2026-08-13.md)).

---

## Le principe

Défilement horizontal. Trois voies parallèles courent d'un bout à l'autre du récit ; chaque mouvement du plan est posé sur la voie qu'il fait avancer.

| Voie | Couleur | Ce qu'elle porte |
|---|---|---|
| **Andrew** | acier | Le monde d'après. Son présent. |
| **L'enquête** | éclaircie (cyan pâle) | Les faits, les dates, les registres |
| **Joël** | ambre | Le monde d'avant. Son passé. |

**Erin n'a plus de voie.** L'histoire d'amour est suspendue (décision du 15 août 2026) ; ses quatre cartes — mouvements 5, 11-12, 21, 24 — ont été retirées, et la dernière page reste à écrire. Son nom d'éclaircie est noté dans [`les-ages-croises.md`](../../02-univers/les-ages-croises.md) pour le jour où elle reviendra.

> **La voie de Joël est presque vide : deux cartes sur dix-huit.**
> Ce n'est pas un défaut de la frise, c'est un constat. L'ancien plan en 24 mouvements ne contient pas les chapitres de la vie d'avant, que la nouvelle architecture réclame. Voir [`deux-histoires-en-une.md`](../../04-plan/deux-histoires-en-une.md).

### Ce que le découpage rend visible

- **Joël** ne compte que deux cartes. C'est le fil qui gouverne le livre, et il n'existe presque pas dans l'ancien plan. Tout le travail à venir est là.
- **L'enquête** occupe massivement l'acte II puis s'éteint net après le mouvement 17 : à partir du retournement, il n'y a plus rien à enquêter.
- **Andrew** n'intervient qu'aux extrémités : poser la règle (1, 2), puis la retourner en question morale (20).

### Parti pris graphique

La frise **s'éclaircit littéralement** de gauche à droite — un lavis pâle qui monte vers la fin, même geste que la capsule qui approche du terme. Les charnières verticales séparent les actes ; les stèles pleine hauteur portent les phrases à garder, posées à l'endroit où elles tombent dans le récit.

Navigation : molette, flèches ← →, glisser à la souris, ou clic sur un acte. Thème clair et sombre.

---

## État au 15 août 2026

- Les voies portent les deux hommes : **Andrew** (le monde d'après) et **Joël** (le monde d'avant), plus **L'enquête**.
- Stèle ajoutée avant le credo : **« Joël, non, attends ! »** — la seule fois du roman où son nom se dit.
- Le palier s'appelle **le jardin** — panneau d'ouverture, règle III.
- Le panneau d'ouverture porte une ligne sur le monde : c'est la Terre, les fleuves ont gardé leur nom, rien de ce qu'ont fait les hommes n'a été gardé.
- **Mouvement 1** : rien n'est annoncé à la cérémonie. Le corps dit l'âge, la salle l'estime à vue, le veilleur mesure après pour le registre.
- **Mouvements 5, 11-12, 21 et 24** : retirés avec la voie d'Erin. Le panneau de fin le dit — la dernière page reste à écrire.

---

## Arbitrages à revoir

> **La frise entière est à refondre.** Les 18 cartes viennent du plan du §13, qui ne connaît pas les deux histoires en une. Depuis, la forme du livre a changé : quelques semaines pour le corps du roman, un épilogue quinze ans plus tard, et une voie de Joël à remplir. C'est le chantier de la prochaine séance, et il demande que l'autrice reconstruise le séquencier.

En attendant, les points mineurs restés en suspens :

- [ ] **Mouvement 3** (« le chiffre qui monte ») rangé dans *L'enquête*. À revoir : ce n'est plus le moteur de l'intrigue mais une critique de fond (voir [`la-ruche.md`](../../02-univers/la-ruche.md)).
- [ ] **Mouvements 4 et 13** : la menace ambiante n'est pas encore portée sur les cartes.
- [ ] Faut-il une stèle pour la règle du jardin, ou le panneau d'ouverture suffit-il ?

## Pour mettre à jour

Les données du récit sont dans le tableau `COLS` en tête du `<script>`, une entrée par colonne (`beat`, `hinge`, `stele`, `panel`). Ajouter une voie = ajouter une entrée à `LANES` et une variable de couleur dans `:root`.
