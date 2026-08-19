# Le site de lecture — conception

*Publier* L'Éclaircie *en ligne : un site qui prolonge le livre au lieu de le commenter.*

> Statut : **conception validée**, rien n'est encore construit.
> Décidé le 19 août 2026. Aucune ligne n'entre dans `develop` sans l'accord de l'autrice.

---

## 1. L'intention

Un site qui donne le roman à lire, et qui met en scène la lecture — la lumière, le
rythme, la matière du monde — sans jamais passer devant le texte.

Le roman est bâti sur un tour : deux enlèvements racontés comme un seul récit, et le
lecteur ne comprend qu'à la fin qu'il suivait deux hommes. Le site **joue ce tour avec
le livre**. Il a deux états.

| État | Ce que le lecteur voit |
|---|---|
| **Première lecture** | une seule lumière, un seul monde, aucune couleur de voie, aucune trace du montage |
| **Seconde lecture** | les mêmes pages, les deux voies séparées, les faux raccords allumés, le plan dédoublé |

La seconde lecture ne s'ouvre qu'une fois l'épilogue atteint. **L'expérience du site
*est* la relecture** — ce que le livre demande déjà de son lecteur.

## 2. Les décisions

| Question | Décision | Pourquoi |
|---|---|---|
| Pour qui | privé d'abord, public le jour venu | l'écriture est loin d'être finie : 8 776 mots, 35 scènes à écrire |
| Le tour | le site le joue, il ne l'explique pas | seule option qui fait du site un prolongement ; et les bêta-lecteurs servent justement à vérifier qu'il fonctionne |
| Où il vit | `09-site/`, dans ce dépôt | le site lit les sources de l'atelier au build : le livre et le site ne peuvent pas diverger |
| Sur quoi on lit | grand écran d'abord, responsive comme plancher | l'ambition est visuelle |
| Qui lit | personne — pas de comptes | phrase de passe partagée, progression dans le navigateur |
| Avec quoi | Astro 6.3 | le site est d'abord un livre : il doit s'afficher avant qu'on ait fini de cligner |

## 3. Comment la donnée arrive

Les sources de l'atelier ne sont pas des modules : ce sont des `<script>` qui déclarent
des globales — `TEXTES`, `VOIES`, `ACTES`, `ETAPES`, `LEXIQUE`. **On ne les convertit
pas.** L'atelier tient à son fichier unique sans dépendance ; le site s'adapte, pas
l'inverse.

`09-site/extraire.mjs` reprend le procédé que `fabriquer.sh` emploie déjà pour
`valide.js` : il concatène les modules de données, retire les balises, les évalue dans
un bac à sable `node:vm`, et écrit du JSON dans `09-site/donnees/`. Il tourne avant
chaque build, et le JSON produit ne se commite pas.

### Le contrat de données

L'extraction **échoue** si la forme attendue a changé : un champ disparu, un texte qui
pointe une scène inconnue, une voie qui n'existe plus. Le message dit en français quoi
réparer.

Le même contrôle s'accroche à `fabriquer.sh`, à côté de `valide.js`. L'autrice
l'apprend donc **en écrivant**, pas trois jours plus tard à un déploiement raté.

> Elle écrit librement *dans* les données — c'est son texte. Ce qui est sous contrat,
> c'est la *forme*, pas le contenu.

## 4. Les pièces

| Pièce | Rôle | Dépend de |
|---|---|---|
| `extraire.mjs` | sources de l'atelier → JSON ; garde le contrat | les sources |
| `lecture/` | le livre : une page par texte, HTML statique, typographie | le JSON |
| `ambiance/` | la lumière qui suit la scène — île persistante | la position de lecture |
| `progression` | le seul objet qui sait où en est le lecteur | `localStorage` |
| `seconde-lecture/` | l'état révélé | `progression` |
| `porte/` | la phrase de passe de la phase privée | une variable d'environnement |

`progression` est isolée exprès. Le jour où l'on voudra des liens nominatifs par
bêta-lecteur — et savoir où chacun décroche —, c'est cette pièce-là qu'on remplace, et
rien d'autre ne bouge.

## 5. L'ambiance

Contrainte qui trie toutes les idées : **les scènes d'Andrew se passent dans la ruche,
celles de Joël dans la vie d'avant.** Tout élément d'ambiance propre à un monde trahit
le tour. Les registres admis en première lecture sont ceux que les deux mondes
partagent.

| Registre | Première lecture | Seconde lecture |
|---|---|---|
| la lumière — la page a une heure | oui | oui, et elle diverge |
| le souffle — typographie et rythme suivent la tension | oui | oui |
| la matière — végétation, coulants, colonnes | non | oui |
| le lieu — le plan, la salle en cours | non | oui, dédoublé |
| le décompte — la frise, les huit jours | non | oui, à deux branches |

Ce qui est interdit en première lecture n'est pas perdu : **c'est le matériau de la
seconde.**

Le vocabulaire s'enrichira par passes, en voyant. **La première passe porte la lumière
seule** — c'est le registre le plus sûr et déjà le plus fort.

L'heure de chaque texte vit dans une petite table **côté site**, pas dans les données de
l'atelier : le site ne demande jamais à l'autrice d'annoter son texte pour lui.

## 6. La pile visuelle

Ni Astro ni aucun framework ne dessine ni n'anime : le SVG et l'animation vivent dans
le navigateur. Principe retenu — **du natif partout où le navigateur sait faire, une
librairie seulement là où il ne sait pas.**

| Pour quoi | Avec quoi |
|---|---|
| l'ossature | Astro 6.3 |
| passer d'une page à l'autre sans rupture | transitions de vue natives, `<ClientRouter />` de `astro:transitions` |
| l'ambiance qui ne se réinitialise jamais | `transition:persist` sur l'île d'ambiance |
| ce qui s'anime en défilant | animations liées au défilement, en CSS |
| la révélation, le plan qui se dédouble | Motion, seulement là |
| les dessins | SVG écrit à la main, animé en CSS |

`transition:persist` est la pièce qui compte : la lumière **survit à la navigation** et
continue de tourner d'un chapitre au suivant, au lieu de repartir de zéro à chaque page.

Le site hérite de la langue visuelle de l'atelier — jetons CSS, thème clair et sombre,
serif pour le texte, sans-serif pour l'interface — mais **pas de ses couleurs de voie**
en première lecture.

## 7. Deux garde-fous

### Le texte se lit même si tout le reste tombe

L'ambiance est une couche par-dessus du HTML qui se suffit à lui-même. JavaScript
coupé, build d'ambiance cassé, navigateur ancien : **on lit le roman.** Non négociable.

### Rien ne fuite

Le vrai risque du projet, c'est qu'une régression laisse échapper le montage sans que
personne le remarque. Donc un contrôle automatique : on construit les pages de première
lecture et **on échoue si un nom de voie, un identifiant de voie ou une couleur de voie
apparaît dans le HTML livré.**

Pas dans le code — dans ce que le lecteur reçoit. C'est la seule invariante vérifiable
sur un site qui contient les deux états du livre.

## 8. La frontière entre les deux sessions

Deux personnes travaillent dans ce dépôt avec leur propre assistant, et les sessions ne
se parlent pas. La frontière s'écrit.

| Fichier | Contenu |
|---|---|
| `CLAUDE.md` à la racine | la loi commune, reprise de `CONTRIBUER.md` : on valide avec l'autrice avant d'intégrer ; gitflow `develop` / `feature/` ; l'atelier est la source de vérité ; on n'édite jamais `atelier.html` à la main. Plus la frontière : la session d'écriture ne descend pas dans `09-site/`, la session du site ne touche pas au manuscrit |
| `09-site/CLAUDE.md` | les règles du site seul, lues seulement quand on travaille dedans |

**Le fichier explique pourquoi ; le contrôle garantit que.** Une consigne en prose, un
agent peut la contourner sans le vouloir. Un contrôle qui échoue, non. Les deux, donc.

## 9. Le déploiement

Projet Vercel enraciné sur `09-site/`. `develop` donne des aperçus, `main` la
production.

**La protection par mot de passe native de Vercel est réservée au plan payant.** Sur le
plan gratuit, on fait une porte maison : une phrase de passe, un cookie, plus
`noindex`. Assez pour « pas public », pas pour « secret ». Le jour de la publication,
on retire la porte — c'est un interrupteur, pas une refonte.

## 10. Hors périmètre

Comptes et inscriptions. Télémétrie de lecture. Commentaires et annotations. Version
imprimable — les PDF existent déjà. Traduction. Application mobile. Moteur de recherche
plein texte.

## 11. À trancher avec l'autrice

1. **L'épilogue est déjà écrit.** Un bêta-lecteur qui arrive aujourd'hui peut le lire au
   deuxième clic, se gâcher le livre et déverrouiller la seconde lecture d'un roman
   qu'il n'a pas lu. Décision de récit, pas de technique.
2. **Le site montre un livre inachevé** — trois textes sur trente-huit. Qu'est-ce qu'on
   affiche à la place de ce qui manque ? Rien, un sommaire grisé, un état d'avancement ?
3. **La mise en scène est une lecture de son texte.** Elle valide l'ambiance.
4. Le nom de domaine.

## 12. Par où on commence

La conception tient en un document, la construction non. Première tranche — **un livre
qui se lit, en ligne, derrière une porte** :

1. `extraire.mjs` et le contrat de données, accroché à `fabriquer.sh`
2. les deux `CLAUDE.md` et la frontière
3. les pages de lecture : les trois textes, la typographie, le sommaire
4. la porte et le déploiement Vercel
5. le contrôle anti-fuite

L'ambiance, la progression et la seconde lecture viennent ensuite, chacune sur sa
tranche. Rien de ce qui précède ne les empêche : la lumière est une couche à poser, et
`progression` est déjà prévue comme une pièce à part.
