# L'atelier

**`atelier.html`** — ouvre-le d'un double-clic. Rien à installer, aucune connexion : tout est dans le fichier.

---

## Ce qu'il contient

| Écran | À quoi il sert |
|---|---|
| **Le parcours** | Le tableau des scènes, qui défile vers la droite. Trois voies : Andrew, le tronc commun, Joël. **Clique une scène** — son dossier d'écriture s'ouvre à droite : ce qui s'y passe, ce que la scène doit produire, ce qu'elle apprend du monde, les phrases à y placer, ce qu'il faut tenir, et ce qui reste à trancher. |
| **Les chapitres** | Glisse les scènes dans des chapitres pour construire le plan. Un clic suffit aussi. **Tout est gardé dans le navigateur** et s'exporte en fichier texte. |
| **Où l'ouvrir** | ⚠️ **Toujours le même fichier : `06-visuels/atelier/atelier.html`, dans le dossier du projet.** *Mets-le en favori et rafraîchis après chaque correction — il est refabriqué sur place.* ⛔ **N'ouvre pas les copies téléchargées** : le mode révision garde tes corrections par chemin de fichier, et une copie dans les téléchargements n'a pas le même chemin. *Tes corrections seraient là, mais pas où tu regardes.* |
| **La révision** | *Onglet Chapitres, bouton « réviser le texte ».* **Tu corriges le texte directement dans la page** — tu écris dans le paragraphe, la gouttière à gauche en ôte un ou en glisse un dessous. En bas, le compte de tes changements et **« enregistrer pour Claude »**. *Dis-moi ensuite « j'ai révisé » : je reprends le fichier et je le porte dans l'atelier.* ⚠️ **Enregistre avant de fermer l'onglet** — tant que le fichier n'est pas sorti, tes corrections ne vivent que dans ce navigateur. |
| **Les notes** | 300 notes — tout ce qui s'est dit du 13 au 20 août, dans l'ordre. Tes mots sont cités tels quels, et en dessous ce que la décision a produit. Cherchable, filtrable. |
| **Le glossaire** | *Onglet d'ouverture du Monde.* **Les trente-trois mots du monde, et cette liste EST la page de fin de volume du livre.** Ordre alphabétique, définitions d'un entre-deux : plus longues qu'une note de bas de page, plus courtes qu'une fiche. La source est [`02-univers/le-glossaire.md`](../../02-univers/le-glossaire.md) ; `05-manuscrit/glossaire.md` en est généré. |
| **La bible** | Le glossaire caché : vingt-cinq notions que le lecteur n’aura jamais — la dernière grâce, le marginal, l’affaire Sorel, le sismographe. **Ce n’est pas un carnet de réflexions.** |
| **Le jardin** | Le plan du jardin — **la fermette** : l'étendue, les bêtes, la mare qui ride, les chats qui se promènent et le trajet d'Andrew qu'on peut lancer. Tout se clique. |
| **Le monde** | Le glossaire, la bible, les règles, les onze interdits, le décompte des âges (avec son graphe), le calendrier, le dispositif des deux récits, et les faux raccords. |
| **Les gens** | Une fiche par personnage : ce qu'il faut avoir en tête avant d'écrire une scène où il entre. |
| **À trancher** | Les trous, les contradictions à répercuter, les questions en attente — et les phrases à garder. |

---

## Comment c'est fait

- **Un seul fichier**, sans dépendance ni appel réseau. Il se déplace, se copie, s'envoie.
- **Deux thèmes** : le bouton en bas du rail bascule sombre / clair. Le choix est retenu.
- **Au clavier** : `←` `→` passent d'une scène à l'autre, `Échap` ferme le dossier.
- **Ce qui est enregistré** dans le navigateur : le plan de chapitres et le thème. Rien d'autre, et rien ne sort de la machine.

## D'où viennent les données

Des fichiers du dossier — le parcours, les interdits, les fiches du monde et des personnages, les phrases —
et de la transcription intégrale des séances. Chaque scène porte sa source en bas de son dossier.

**Ce document était un miroir. Il est devenu la source.** *Le 19 août 2026 : les textes du livre,
les décisions datées, le lexique et les règles vivent désormais ici en premier, et les fichiers
Markdown du dossier sont en retard sur lui.* **En cas de désaccord, l'atelier a raison.**

---

## Comment on le modifie

**On n'édite jamais `atelier.html` à la main.** Sept cent mille caractères : on édite un des douze
morceaux de [`sources/`](sources/LISEZ-MOI.md), puis on refabrique.

```bash
cd sources && sh fabriquer.sh
```

Le script enchaîne la fabrication, un `node --check` sur tout le JavaScript, et
[`valide.js`](valide.js) — le contrôleur de cohérence : il compte les scènes, vérifie que chaque
lien pointe sur une scène qui existe, que chaque texte a sa fiche, et il refuse les mots bannis.

---

## Comment il se maintient

**Il se met à jour à chaque décision.** Une validation, une correction, une idée retenue : on corrige d'abord la fiche Markdown concernée, puis on répercute ici, on reconstruit, on vérifie dans le navigateur, on commite. *Un atelier qui retarde d'une séance ne sert plus à rien.*

**Les étapes sont marquées par des tags git.** `git tag -l -n1` les liste. Deux familles, et
elles ne se mélangent pas : **`etape-NN`** pour les jalons du récit, **`vX.Y.Z`** pour les
versions publiées.

| | |
|---|---|
| `etape-01` – `etape-04` | la mise en place du monde, du casting et du système |
| `etape-05` | l'atelier — le dossier devient un outil d'écriture |
| `etape-06` – `etape-07` | le lecteur ne quitte jamais ce monde-ci ; deux voies, une bande d'étapes |
| `etape-08` | l'épilogue écrit et validé |
| `etape-09` | le prologue existe |
| `etape-10` | **Une journée à la ruche** — le chapitre premier, seize passes |
| `avant-le-menage` | le filet posé avant le grand nettoyage du 19 août |
| **`v0.1.0`** | **la première version publiée** |

Pour retrouver une version : `git show etape-09:04-plan/le-parcours-de-l-enquete.md`
Pour comparer : `git diff etape-09 etape-10 -- 06-visuels/`

## Ce qu'il ne fait pas

Il ne porte pas les développements longs. Les documents de `01-dossier`, `02-univers`,
`03-personnages` et `04-plan` restent là pour ça — ce sont eux qui expliquent, lui qui tranche.
