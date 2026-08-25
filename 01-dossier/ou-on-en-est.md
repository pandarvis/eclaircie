# Où on en est

*Point d'étape au 25 août 2026. Ce fichier se réécrit à chaque séance : il dit
l'état du chantier, pas son histoire.*

---

## ✨ Le livre — `06-visuels/atelier/le-livre.html`

**Le roman se lit maintenant comme un livre : double page au format poche, la
couverture fermée au départ, les pages qui se tournent.** *99 pages, sept
chapitres, chacun sur une belle page — 5, 19, 39, 59, 71, 79, 87.* Le fichier
tient tout seul — couverture comprise, aucun appel réseau : il s'ouvre d'un
double-clic et se donne à lire.

🔒 **L'épilogue n'est pas dans le livre.** *Il est écrit, et il donne la fin.*

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

**La dernière ligne d'un paragraphe coupé ne se justifie que si elle est déjà
presque pleine.** *Un paragraphe coupé par un changement de page continue de
l'autre côté, donc sa dernière ligne se justifie comme les autres — sauf quand la
règle anti-veuve raccourcit la coupe : six mots écartelés sur toute la mesure se
voient de l'autre bout de la pièce.*

---

## Le manuscrit — 19 067 mots

| # | Titre | Scène | Mots | État |
|---|---|---|---|---|
| — | Prologue — La cérémonie | `ouv` | 2 628 | 🔒 **relu et reverrouillé** |
| 1 | Une journée à la ruche | `capsule` | 3 747 | 🔒 **relu et reverrouillé** |
| 2 | L'aquarium | `s1` | 3 451 | ✅ validé |
| 3 | La tournée | `s2` | 1 834 | ✅ validé |
| 4 | La maison | `s3` | 1 245 | ✅ passe d'autrice appliquée |
| 5 | Le poste | `s4` | 1 165 | ✅ passe d'autrice appliquée |
| 6 | **Première investigation** | `s5` | 2 332 | ⚠️ **écrit aujourd'hui, relecture à froid demain** |
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

## Ce qui attend demain

⚠️ **La relecture à froid du chapitre 6.** *Il a été repris une trentaine de fois
aujourd'hui ; personne ne l'a lu d'une traite depuis.*

**Cinq chapitres sur huit ne sont pas verrouillés.** *Seuls le prologue, le chapitre 1
et l'épilogue le sont.* ❓ *Faut-il figer* La maison, Le poste *et* Première
investigation ?

⚠️ **Un seul verrou reste ouvert : l'épilogue.** *L'autrice dira quand le
reposer. Tant qu'il est ouvert, la fabrication ne protège plus ce texte contre
une modification involontaire.*
✅ *Prologue relu et reverrouillé le 25 août 2026 — 115 paragraphes.*
✅ *Chapitre premier relu et reverrouillé le 25 août 2026 — 187 paragraphes.*

⚠️ ***pédiatre* est mort le 20 août et vit encore dans 15 fichiers.** *Certaines
occurrences sont légitimes — les interdits doivent le nommer pour l'interdire. Les
autres non, et le mot de remplacement n'existe toujours pas.*

**Les fiches de personnages de la version bêta** — June, Julie, Paul — *sont de moi et
n'ont jamais été relues.*

**Sans réponse depuis plusieurs jours :** le nom du corps médical du jardin ; le nom du
rendez-vous de suivi ; la frontière entre chuchoteur et tuteur ; le nombre de travées.

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
| `poser-un-blanc.py` | pose ou ôte un blanc d'une ligne entre deux paragraphes ; refuse si l'ancre est absente, ambiguë, pas en fin de paragraphe, ou si le chapitre est verrouillé |

*Le sommaire de la version de lecture vérifie aussi que ses accroches choisies existent
mot pour mot dans le texte.*
