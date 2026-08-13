# Frise narrative — carnet

Fichier : [`frise-narrative.html`](frise-narrative.html) — s'ouvre dans un navigateur, autonome, aucune dépendance externe.
Version en ligne : <https://claude.ai/code/artifact/278c6576-e781-4aad-86ff-135f9932ef11>

Source : section **13. LE PLAN** du [dossier de création](../../L-ECLAIRCIE-dossier-complet.md), corrigée par les décisions du 13 août 2026 (voir [`04-plan/incidences-2026-08-13.md`](../../04-plan/incidences-2026-08-13.md)).

---

## Le principe

Défilement horizontal. Quatre voies parallèles courent d'un bout à l'autre du récit ; chaque mouvement du plan est posé sur la voie qu'il fait avancer.

| Voie | Couleur | Ce qu'elle porte | Mouvements |
|---|---|---|---|
| **Le monde** | acier | Le rite, la règle, la doctrine | 1, 2, 20 |
| **L'enquête** | éclaircie (cyan pâle) | Les faits, les dates, les registres | 3, 4, 6-9, 13, 14, 15, 16, 17 |
| **La fille** | rose sourd | Le décompte, le visage, l'échec | 5, 11-12, 21, 24 |
| **Le voile** | ambre | L'ancien monde qui remonte | fin d'acte I, 10, 18, 19, 22, 23 |

Pas de cinquième voie : le garçon et les jumelles découlent de l'enquête, ils n'ont pas de fil propre.

### Ce que le découpage rend visible

- **Le voile** s'allume une fois en fin d'acte I, disparaît, revient au mouvement 10 — puis prend tout l'acte III. C'est le fil qui gouverne le livre et il est presque muet pendant la moitié du texte.
- **La fille** ne compte que quatre points, très espacés. C'est le rythme juste pour une histoire d'amour qui ne peut pas se dire.
- **L'enquête** occupe massivement l'acte II puis s'éteint net après le mouvement 17 : à partir du retournement, il n'y a plus rien à enquêter.
- **Le monde** n'intervient qu'aux extrémités : poser la règle (1, 2), puis la retourner en question morale (20).

### Parti pris graphique

La frise **s'éclaircit littéralement** de gauche à droite — un lavis pâle qui monte vers la fin, même geste que la capsule qui approche du terme. Les charnières verticales séparent les actes ; les stèles pleine hauteur portent les phrases à garder, posées à l'endroit où elles tombent dans le récit.

Navigation : molette, flèches ← →, glisser à la souris, ou clic sur un acte. Thème clair et sombre.

---

## État au 13 août 2026

Intégré depuis la première version :

- La voie **Elle** devient **La fille** ; la voie **Le voile** est glosée « l'ancien monde qui remonte ».
- Le palier s'appelle **le jardin** — panneau d'ouverture, règle III.
- Le panneau d'ouverture porte une ligne sur le monde : c'est la Terre, les fleuves ont gardé leur nom, rien de ce qu'ont fait les hommes n'a été gardé.
- **Mouvement 1** : rien n'est annoncé à la cérémonie. Le corps dit l'âge, la salle l'estime à vue, le veilleur mesure après pour le registre.
- **Mouvements 11-12** : plus de compte à rebours. Il croise la fille avec une facilité qui devrait l'alerter.
- **Mouvement 21** : ne s'appelle plus « L'année ». Devient **Ce qui ne se dira pas** — il ne peut rien lui avouer, il essaie autrement, elle en fait un ami. Le lien met les gens sur le même chemin, il n'oblige à rien.
- **Mouvement 24** et **panneau de fin** : il se dit qu'il la reverra dans l'autre monde. Elle n'a aucun moyen de comprendre ce qu'il se dit, et le livre ne le confirme jamais.

---

## Arbitrages à revoir

- [ ] **Conflit à trancher, hérité du dossier maître.** Le veilleur n'est en poste que depuis huit ans au début du livre. Le §12 le dit « vétéran du métier » et le mouvement 20 parlait de « ce qu'il racle depuis vingt ans ». J'ai retiré les vingt ans de la carte 20, mais « vu de l'intérieur » au mouvement 1 remplace provisoirement « professionnel blasé » : à confirmer.
- [ ] **Mouvement 3** (« le chiffre qui monte ») rangé dans *L'enquête* plutôt que dans *Le monde*, parce que c'est le déclencheur.
- [ ] **Fin d'acte I** transformée en carte autonome sur la voie *Le voile*. Dans le plan c'est une ligne de bloc-note ; ici c'est le premier point du fil qui portera tout le livre.
- [ ] Les mouvements 6-9 et 11-12 sont groupés comme dans le plan. À éclater si le découpage en chapitres se précise.
- [ ] **Mouvements 4 et 13** : la menace ambiante (voir [`la-jalousie.md`](../../02-univers/la-jalousie.md)) n'est pas encore portée sur les cartes. En attente.
- [ ] Faut-il une stèle pour la règle du jardin, ou le panneau d'ouverture suffit-il ?

## Pour mettre à jour

Les données du récit sont dans le tableau `COLS` en tête du `<script>`, une entrée par colonne (`beat`, `hinge`, `stele`, `panel`). Ajouter une voie = ajouter une entrée à `LANES` et une variable de couleur dans `:root`.
