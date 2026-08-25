# Où on en est

*Point d'étape au 25 août 2026, en fin de journée. Ce fichier se réécrit à chaque
séance : il dit l'état du chantier, pas son histoire.*

---

## ✨ Le livre — `06-visuels/atelier/le-livre.html`

**Le roman se lit maintenant comme un livre : double page au format poche, la
couverture fermée au départ, les pages qui se tournent.** *99 pages, sept
chapitres, chacun sur une belle page — 5, 19, 39, 59, 71, 79, 87.* Le fichier
tient tout seul — couverture comprise, aucun appel réseau : il s'ouvre d'un
double-clic et se donne à lire.

🔒 **L'épilogue n'est pas dans le livre.** *Il est écrit, et il donne la fin.*

**Le livre se ferme sur une page « À suivre »**, sur une belle page et sans folio.
*Sans elle, on tourne la dernière page du chapitre sixième et on croit que le
fichier est incomplet.* Rien après : le contre-plat de fin ne se voit jamais dans
un vrai livre, la couverture se referme dessus.

**Pas de nom de chapitre : Prologue, Chapitre I, Chapitre II.** *Le manuscrit dit
« Chapitre premier » ; le livre compte en chiffres.* **Le titre d'un chapitre
annonce ce qui va se passer, et ici ça ne regarde personne.**

| | |
|---|---|
| tourner | les flèches du clavier, les deux boutons, `Espace`, **la corne en bas à droite** |
| enchaîner | maintenir la flèche : au-delà de 480 ms d'écart, ça n'anime plus |
| se repérer | folio en bas au centre, titre courant, épaisseur du bloc, réglette d’avancement |
| ne pas savoir | la réglette est une ligne nue : **un cran par chapitre, c’est un cran par longueur de chapitre** |
| retrouver | `S` ouvre le sommaire de n'importe où · la page se retient d'une séance à l'autre |
| adresser | `le-livre.html#p63` ouvre directement à la page 63 |
| au départ | un mot à côté de la couverture nomme les deux flèches — celles de l’écran et celles du clavier |
| le reste | `G` le glossaire (sans bouton) · `N` la lecture de nuit · `Échap` referme |

### La relecture d'août

| chapitre | blancs posés | autre | |
|---|---|---|---|
| Prologue | — | une phrase de trop retirée, un saut de page | 🔒 |
| Chapitre I | 13 | *l'écusson de la ruche* | 🔒 |
| Chapitre II | 28 | — | 🔒 |
| Chapitre III | 12 | *ce qu'il avait dit en sortant de sa capsule* · *un temps d'arrêt* | 🔒 |
| Chapitre IV | 8 | *Bonjour Julie* sans virgule | 🔒 |
| Chapitre V | 8 | *et le remarqua* · *coupé avant le nom* · *d'une fugue, elle ?* | 🔒 |
| Chapitre VI | 5 | *le panier raconté* · *ce qu'il ne sait pas, c'est quand* · **Andrew ne prononce jamais le mot** | 🔒 |

*Les blancs sont une demande de rythme, pas une correction de texte : le chapitre
deuxième en compte vingt-huit pour 274 paragraphes, soit une respiration toutes
les dix.*

### Deux marques de respiration

| dans la source | à l'écran |
|---|---|
| `[pause]` avec les trois points | une rupture de scène : `· · ·`, trois lignes de blanc |
| **`[pause]` avec rien dedans** | **un blanc d'une ligne**, sans marque — la scène ne se coupe pas, elle respire |

*On n'a pas inventé de genre pour ça : huit outils connaissent la liste des genres,
et celui qu'on oublie perd le blanc en silence.* **Une pause vide fait le travail,
et seule sa présentation change.**

### Les sauts de page demandés

**Un saut forcé s'ancre sur le texte, jamais sur un numéro de page** — la
pagination se recalcule à chaque correction, un numéro ne tiendrait pas une
journée. On nomme le début du paragraphe qui doit commencer une page, dans
`SAUTS` en tête de `fabriquer-le-livre.py`. ⚠️ **La fabrication s'arrête si le
passage a été réécrit** : on l'apprend tout de suite au lieu de perdre le saut en
silence. *Vérifié en le sabotant.*

| chapitre | le paragraphe qui ouvre une page |
|---|---|
| Prologue | *Après le nom, le pichet.* — demandé le 25 août 2026 |

---

**La pagination est calculée dans une géométrie logique fixe, puis le livre est
mis à l'échelle de la fenêtre.** *C'est ce qui permet d'avoir un livre qui remplit
n'importe quel écran sans qu'un seul numéro de page change.* Changer un chiffre de
`GEO` dans `fabriquer-le-livre.py` repagine tout le livre.

**Le glossaire est éteint par défaut, et il n'a plus de bouton** — seule la touche
`G` l'allume. La fiche se pose à côté du livre, sur le bureau, sans recouvrir une
ligne ; sur une fenêtre étroite elle se range en bas et mange le pied de la page.

### La page roule

**Une feuille plate qui tourne autour d'un axe reste une planche.** *Aucun réglage
d'animation ne rattrape ça : il fallait qu'elle soit réellement courbe.*

La page est découpée en **quatorze lames articulées** les unes aux autres. À chaque
image, la rotation totale se répartit entre elles : une part va à la charnière, le
reste se concentre sous **une bosse qui voyage du bord libre vers la reliure**.
C'est ce voyage qui fait le roulement. Chaque lame s'assombrit selon l'angle
qu'elle présente à la lumière — et c'est ce dégradé, plus que la géométrie, qui
donne le relief.

**500 ms.** Les réglages sont en tête du moteur : `NLAME`, `BOSSE`, `SIG`.

⚠️ **L'ombrage se calcule en sin², pas en 1 − |cos|.** *Les deux courbes ont la
même forme, mais `|cos|` fait un angle vif à 90° — en plein dans le moment où la
page tourne le plus vite. On voyait la cassure.* **Ne pas y retoucher sans
retracer la courbe.**

⚠️ **Les lames s'empilent, elles ne se juxtaposent pas.** *Deux lames voisines qui
se touchent exactement sont rasterisées séparément : au pixel de la couture,
chacune ne couvre que la moitié et un quart du fond passe au travers.* Chaque
lame déborde donc d'un pixel sur sa voisine, **et ce débordement passe derrière
elle** — ce qui fuit par la couture est alors le même texte au même endroit.
L'empilement tient à un décalage de profondeur de 0,12 px par lame. *Ordre, du
fond vers l'œil : face k, son voile, face k+1, son voile.*

⚠️ **L'ombre court en dégradé, pas par lame.** *Une lame est une facette plate ;
une seule valeur d'ombre par lame se lit comme quatorze bandes dès que la feuille
s'incline.* Chaque voile va de l'ombre de son bord d'entrée à celle de son bord
de sortie — et la sortie de l'une est l'entrée de la suivante.

### La page respire

**26 lignes, interligne à 1,62, marges élargies.** *La page était juste — 28
lignes de poche — et étouffante : un poche s'imprime pour être lu à bout de bras,
un écran se lit de face.* La justification ne bouge pas : 54 signes par ligne.

⚠️ **Une coupe de paragraphe ne se signale que d'une façon : sa dernière ligne
est justifiée, donc pleine.** *Sinon le lecteur tourne la page et trouve une
phrase qui commence en minuscule, sans alinéa — et sur une réplique, sans tiret.*

Deux règles, dans cet ordre :
1. **On recule d'une ligne entière** — celle qui devient la dernière appartient au
   flux naturel du paragraphe, donc elle est pleine.
2. **Si c'est impossible, on ne coupe pas.** *Un préfixe de deux lignes ne peut pas
   reculer sans laisser une orpheline ; le paragraphe entier passe à la page
   suivante.*

*Prix : deux ou trois lignes de blanc sur six pages. Un livre en a partout ; une
phrase coupée qui ne se voit pas, non.* Mesuré sur le livre entier : **11 coupes,
toutes à 100 % de remplissage, toutes justifiées.**

---

## Le manuscrit — 19 067 mots

| # | Titre | Scène | Mots | État |
|---|---|---|---|---|
| — | Prologue — La cérémonie | `ouv` | 2 628 | 🔒 **relu et reverrouillé** |
| 1 | Une journée à la ruche | `capsule` | 3 747 | 🔒 **relu et reverrouillé** |
| 2 | L'aquarium | `s1` | 3 451 | 🔒 **relu et verrouillé** |
| 3 | La tournée | `s2` | 1 834 | 🔒 **relu et verrouillé** |
| 4 | La maison | `s3` | 1 245 | 🔒 **relu et verrouillé** |
| 5 | Le poste | `s4` | 1 165 | 🔒 **relu et verrouillé** |
| 6 | **Première investigation** | `s5` | 2 371 | 🔒 **relu et verrouillé** |
| — | Épilogue | `jardin-fin` | 2 631 | 🔒 verrouillé |

**`lecture.html` contient les huit chapitres** (282 ko), sommaire compris. Il se
construit désormais tout seul depuis la liste des chapitres lisibles — il ne peut
plus se périmer.

---

## Ce qui a été décidé aujourd'hui

### La mise en forme

**L'alinéa OU le blanc, jamais les deux.** *Le retrait dit déjà « nouveau
paragraphe » ; le blanc le redisait par-dessus.* Corrigé dans
[`p3-style.html`](../06-visuels/atelier/sources/p3-style.html) — donc dans
l'atelier **et** dans la version de lecture. Le blanc est rendu à ce qu'il sait
faire seul : marquer une rupture de scène.

**La typographie française se pose au rendu, jamais dans la source.** *652 espaces
insécables devant les `; : ! ?` et dans les guillemets.* **Le texte n'a pas
bougé d'un caractère** — trois chapitres sont verrouillés par empreinte, et ce
n'est pas au fabricant de corriger l'autrice.

### Les règles de langue

**Le mot *peau* n'est interdit que pour les capsules.** *La règle du 19 août visait
les capsules pourries — « rien ne doit laisser croire qu'il y a quelqu'un dedans ».*
`valide.js` ne bloque plus, il signale quand le mot voisine une capsule.

**On s'adresse aux gens selon leur vécu, pas selon leur apparence.** *Julie et Eliott
ont dix ans ; Andrew la vouvoie et le tutoie.* **Ce n'est pas une politesse, c'est une
information** — écrit dans [`la-ruche.md`](../02-univers/la-ruche.md).

**Un interdit interdit ce qu'il nomme, pas le champ lexical autour.** *En cas de doute :
écrire, puis signaler la tension. Jamais contourner en silence.* Voir
[`les-interdits.md`](les-interdits.md), « Comment lire ces interdits ».

**Le carnet est à Andrew, le calepin à Isaac et au lieutenant.** *Un objet que deux
personnages manipulent change de nom, pas de propriétaire —* [`le-style.md`](le-style.md) § 8 bis.

### Le dispositif

**Le nom de Liam ne s'écrit jamais** — pas plus que celui de Joël. `valide.js` refuse
de fabriquer si l'un apparaît dans un chapitre dont la scène est du côté de Joël.

**Le lieutenant du chapitre 5 est celui qui ordonnera de lâcher l'affaire, et celui qui
criera *attends* à la poursuite.** *Un ami, un supérieur et un témoin, dans cet ordre.*

**Une seule dissonance de langue au chapitre 5** — *J'en mettrais ma main au feu*,
née de l'ordalie. *Plus* en mon temps, *et les deux photographies, qui portent sur le
nombre.*

**Le jour du tri** — *deux fois par semaine les porteurs ne sortent pas* — enferme
l'affaire dans le dépôt et rend la visite chez Henri obligatoire.

---

## Comment se mène une relecture

**Deux passes.** *La rapide dit les blancs — le rythme, les respirations, les
changements de sujet. La minutieuse suit, pour les ajustements de texte.*
**On ne mélange pas les deux** : chercher les mots en même temps que le souffle
fait perdre les deux.

⚠️ **Le verrou d'un chapitre veut dire que les DEUX passes sont faites.** *Il ne se
pose pas après la passe rapide.* Un chapitre verrouillé est relu, pas seulement rythmé.

**Le vocabulaire est fixé :** *« un blanc »* pour une ligne de respiration,
*« une pause »* pour la rupture de scène en trois points. Voir
`poser-un-blanc.py`, qui refuse de travailler sur une ancre douteuse.

**Et chaque chapitre se ferme par son verrou** dès qu'il est validé.

---

## Le manuscrit est relu

✅ **Les huit textes sont relus, validés et verrouillés.** *La grande passe du 25 août
2026 : une lecture rapide pour le rythme — 74 blancs posés — puis les corrections
d'écriture, chapitre par chapitre.* La fabrication vérifie leur empreinte et refuse de
tourner si l'un d'eux bouge.

✅ *Prologue relu et verrouillé le 25 août 2026 — 115 paragraphes.*
✅ *Chapitre premier relu et verrouillé le 25 août 2026 — 187 paragraphes.*
✅ *Chapitre deuxième relu et verrouillé le 25 août 2026 — 274 paragraphes.*
✅ *Chapitre troisième relu et verrouillé le 25 août 2026 — 194 paragraphes.*
✅ *Chapitre quatrième relu et verrouillé le 25 août 2026 — 138 paragraphes.*
✅ *Chapitre cinquième relu et verrouillé le 25 août 2026 — 106 paragraphes.*
✅ *Chapitre sixième relu et verrouillé le 25 août 2026 — 214 paragraphes.*
✅ *Épilogue validé et verrouillé le 25 août 2026 — 118 paragraphes.*

### Ce qui attend

**Les fiches de personnages de la version bêta** — June, Julie, Paul — *sont de moi et
n'ont jamais été relues.*

### Ajourné jusqu'à la description du jardin

⛔ **Ne pas le rappeler avant d'y être.** *L'autrice tranchera sur place, et le répéter
à chaque point d'étape ne fait que du bruit.*

*Le remplaçant de* pédiatre *(mort le 20 août, encore dans 15 fichiers) ; le nom du corps
médical du jardin ; le nom du rendez-vous de suivi ; la frontière entre chuchoteur et
tuteur ; le nombre de travées.*

---

## Les outils, et ce qu'ils refusent

*Tout passe par `06-visuels/atelier/sources/fabriquer.sh`, qui doit imprimer
**FABRICATION OK**. Ne jamais le filtrer par `grep` ou `tail` : le code de sortie du
filtre masque celui du script.*

| Outil | Ce qu'il fait |
|---|---|
| `valide.js` | refuse de fabriquer si un chapitre manque de `note`, `tenu` ou `ouvre`, s'il emploie un mot interdit, ou si un nom de la vie d'avant apparaît côté Joël |
| `glossaire.py` | régénère `p7-monde.js` ; la fabrication refuse de tourner s'il est en retard |
| `verrouiller-les-textes.py` | `--verifier` · `--poser [id…]` · `--ouvrir <id>` |
| `relire.py` | correcteur mécanique : signale, ne corrige jamais |
| `citations.py` | vérifie que ce que les fiches citent existe encore dans le texte |
| `reprendre-la-revision.py` | reprend un fichier corrigé par l'autrice, réouvre et repose le verrou |
| `fabriquer-le-livre.py` | fabrique `le-livre.html` ; il tourne à chaque fabrication, le livre ne peut pas prendre de retard sur le texte |
| `poser-un-blanc.py` | pose ou ôte un blanc d'une ligne **entre deux paragraphes nommés** — la fin de l'un, le début de l'autre ; refuse si une ancre est absente, ambiguë, pas en fin de paragraphe, s'il y a déjà un blanc, ou si le chapitre est verrouillé |

*Le sommaire de la version de lecture vérifie aussi que ses accroches choisies existent
mot pour mot dans le texte.*
