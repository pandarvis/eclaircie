<script>
const VOIES = {
  andrew: { nom: `Andrew`,  desc: `Ce monde-ci. Le présent.` },
  commun: { nom: `Les étapes`, desc: `Le beat, sans son monde. Ni écrit, ni attribué.` },
  joel:   { nom: `Joël`,    desc: `La vie d'avant — et le lecteur ne le sait pas.` }
};

const ACTES = [
  { t: `Ouverture`,          c0: 0,  c1: 1 },
  { t: `Avant la disparition`, c0: 2,  c1: 3 },
  { t: `La disparition`,       c0: 4,  c1: 6 },
  { t: `Le monde comme terrain`, c0: 7, c1: 8 },
  { t: `Le registre`,          c0: 9,  c1: 13 },
  { t: `La fausse piste s'éteint`, c0: 14, c1: 16 },
  { t: `L'enlisement`,         c0: 17, c1: 23 },
  { t: `La remontée`,          c0: 24, c1: 27 },
  { t: `Le seuil franchi deux fois`, c0: 28, c1: 33 },
  { t: `Épilogue`,             c0: 34, c1: 36 }
];

/* le tronc : le beat generique, ni ecrit ni attribue.
   Il ne commence qu'au moment ou le recit peut se dedoubler. */
const ETAPES = [
  { c0: 5, c1: 5,  t: `Première visite au commissariat, pour discuter avec son acolyte` },
  { c0: 6, c1: 6,  t: `Retour chez le témoin` },
  { c0: 7, c1: 7,  t: `Sur le lieu de travail` },
  { c0: 8, c1: 8,  t: `Ceux qui connaissent le suspect` },
  { c0: 9, c1: 9,  t: `L'archive` },
  { c0: 10, c1: 10, t: `Les recherches, en parallèle` },
  { c0: 12, c1: 12, t: `L'homme qui était là ce jour-là` },
  { c0: 14, c1: 14, t: `Chez le suspect` },
  { c0: 16, c1: 16, t: `L'alibi se vérifie` },
  { c0: 17, c1: 18, t: `Nouvelle piste` },
  { c0: 19, c1: 21, t: `La fausse piste tombe — et on continue quand même` },
  { c0: 22, c1: 23, t: `« Lâche l'affaire »` },
  { c0: 24, c1: 26, t: `Seul — puis la solution` },
  { c0: 27, c1: 27, t: `On entre` },
  { c0: 28, c1: 29, t: `Le lieu de séquestration` },
  { c0: 30, c1: 30, t: `La poursuite` }
];

/* ==========================================================================
   LES LOTS — des chapitres qui font bloc
   Ce ne sont pas les actes : un acte range, un lot se lit d'un seul tenant.
   ========================================================================== */
const BLOCS = [
  { c0: 5,  c1: 16, t: `La première piste`,
    q: `Un suspect, un alibi — et douze chapitres pour rien.` },
  { c0: 17, c1: 21, t: `La seconde piste`,
    q: `Elle meurt sur une erreur administrative, et personne n'a rien fait de mal.` },
  { c0: 22, c1: 24, pic: true, t: `Le point culminant`,
    q: `Trois chapitres, une seule scène pour le lecteur — deux hommes, deux issues.` },
  { c0: 27, c1: 31, pic: true, vert: true, t: `La même scène, jouée deux fois`,
    q: `Il entre seul. D'un côté deux corps ; de l'autre, un garçon vivant.` }
];

const SCENES = [
{
  id: `g-poste`, no: `Non écrite`, col: 5, row: `andrew`, acte: `La disparition`, gris: true,
  face: `s4`,
  titre: `Il rencontre Isaac`,
  statut: `ouvert`,
  resume: `**Andrew rend visite à Isaac au sujet de la disparition d'Eliott.** Le livre ne l'écrit pas — la carte est là à titre indicatif, pour qu'on sache où l'on en est.`,
  produit: `*Ça a lieu, le lecteur le suppose, et on ne le lui montre pas. La scène écrite, à cette étape, est celle de Joël.*`,
  monde: `—`, qui: [`andrew`,`isaac`],
  gardes: [`Si elle finit par s'écrire, elle ne doit rien apprendre que le chapitre de Joël n'ait déjà donné — sinon le lecteur a deux scènes et non une.`],
  src: `décision du 16 août 2026`
},
{
  id: `g-suspect`, no: `Non écrite`, col: 14, row: `andrew`, acte: `La fausse piste s'éteint`, gris: true,
  face: `s12`,
  titre: `Chez le marginal`,
  statut: `ouvert`,
  resume: `Le même beat, de ce côté-ci : ils vont voir l'homme de vingt-deux ans, celui des scènes 6, 7 et 9. **Le livre ne l'écrit pas.**`,
  produit: `*C'est ce qui rend la couture possible : le lecteur a entendu parler du marginal pendant trois scènes, il croit le rencontrer, et il rencontre un homme de l'autre monde.*`,
  monde: `—`, qui: [`andrew`,`isaac`,`marginal`],
  gardes: [`Elle ne doit jamais s'écrire. Deux visites chez deux suspects, et le lecteur a deux affaires.`],
  src: `décision du 16 août 2026`
},
{
  id: `g-alibi`, no: `Non écrite`, col: 16, row: `andrew`, acte: `La fausse piste s'éteint`, gris: true,
  face: `s13`,
  titre: `L'alibi du marginal tient`,
  statut: `ouvert`,
  resume: `Le même beat, de ce côté-ci. **Le livre ne l'écrit pas.**`,
  produit: `*Les deux pistes meurent en même temps, et le lecteur n'en enterre qu'une.*`,
  monde: `—`, qui: [`andrew`,`isaac`],
  gardes: [`Ne jamais l'écrire, pour la même raison.`],
  src: `décision du 16 août 2026`
},
{
  id: `g-temoin`, no: `Non écrite`, col: 6, row: `joel`, acte: `La disparition`, gris: true,
  face: `s5`,
  titre: `Retour chez leur mère`,
  statut: `ouvert`,
  resume: `**Décision de l'autrice, 16 août 2026 : le pendant de June, c'est leur mère.** Joël y retourne pour ce que le procès-verbal n'a pas retenu — l'état d'esprit, les habitudes, ce qui n'allait pas.`,
  produit: `**Le même beat, et une asymétrie que le monde produit tout seul.** D'un côté quelqu'un dont c'est le métier de s'occuper d'un arrivant ; de l'autre, quelqu'un qui n'a pas de métier du tout. *À garder en tête en écrivant June : elle est payée pour être là, et l'autre non.*`,
  monde: `—`, qui: [`joel`],
  gardes: [
    `**Rien à surveiller ici : la scène ne s'écrira pas.** La carte existe pour que l'autrice sache ce qui s'est passé de ce côté-là en écrivant celle d'en face. *Le mot « mère » peut donc y figurer — il ne sortira jamais dans le texte, puisqu'il n'y aura pas de texte.*`
  ],
  src: `décision du 16 août 2026 — 04-plan/le-parcours-de-l-enquete.md §5`
},
{
  id: `g-fac`, no: `Non écrite`, col: 7, row: `joel`, acte: `Le monde comme terrain`, gris: true,
  face: `s6`,
  titre: `Une sortie de fac`,
  statut: `ouvert`,
  resume: `**Le pendant du lieu de travail.** Une sortie de faculté ; le responsable est un surveillant ; les marginaux sont un groupe de lourds. **L'homme aime semer le désordre** — l'équivalent d'un casseur dans une manifestation.`,
  produit: `*Le même blasé, la même exclusion temporaire, le même effectif qu'on ne peut pas baisser. Un surveillant de fac et un responsable d'atelier disent exactement la même chose, et c'est ce qui permet de n'en écrire qu'un.*`,
  monde: `—`, qui: [`joel`],
  gardes: [`Le groupe n'a ni nom, ni sigle, ni chef — même règle que de l'autre côté.`,
           `Aucun mot ne doit ancrer l'endroit dans un seul des deux mondes : ni programme, ni diplôme, ni rien qui n'existerait pas ici.`],
  src: `décision du 16 août 2026`
},
{
  id: `g-archives`, no: `Non écrite`, col: 9, row: `joel`, acte: `Le registre`, gris: true,
  face: `s8`,
  titre: `Le service des archives`,
  statut: `ouvert`,
  resume: `**Le pendant de la ruche : le service des archives du commissariat.** Il y retourne, il tire des dossiers, il cherche une anomalie.`,
  produit: `🔴 **Et ça dissout le risque majeur du dossier.** Le §3.5 posait que les scènes de monde ne peuvent être que d'Andrew, donc que ses chapitres seraient chargés et ceux de Joël secs — *deux textures, et le dispositif se fissure.* **Un homme qui consulte des archives est le même partout.**`,
  monde: `—`, qui: [`joel`],
  gardes: [`C'est un lieu de travail ennuyeux des deux côtés. Ni ambiance, ni solennité.`],
  src: `décision du 16 août 2026`
},
{
  id: `g-liam`, no: `Non écrite`, col: 10, row: `joel`, acte: `Le registre`, gris: true,
  face: `s9`,
  titre: `Liam donne des infos`,
  statut: `ouvert`,
  resume: `**Le pendant du coup de téléphone.** C'est Liam qui renseigne : les altercations, ce qui a dérapé, les jours passés en cellule.`,
  produit: `*Une voix au bout d'un fil qui déroule un casier : impossible de dire de quel monde elle parle.*`,
  monde: `—`, qui: [`joel`],
  gardes: [`Le nom de Liam n'est jamais prononcé dans le texte, comme tous les noms de la vie d'avant. C'est un nom de bible.`],
  ouvert: [`✅ **C'est bien Liam, et il n'y a pas d'autre collègue.** *Le même homme porte donc la présentation d'Isaac, les renseignements du téléphone, et le cri de la fin — il gagne en épaisseur à chaque apparition, et c'est ce qui rend le dernier chapitre si dur.*`],
  src: `décision du 16 août 2026`
},
{
  id: `g-potes`, no: `Repère`, col: 8, row: `joel`, acte: `Le monde comme terrain`, gris: true,
  titre: `Les potes du type`,
  statut: `ouvert`,
  resume: `**Le pendant des autres travailleurs : les copains de l'homme.** Ils disent ce qu'ils pensent de lui, et ce qu'ils pensent d'elles.`,
  produit: `*Le grief se dit dans leur bouche et jamais dans celle du narrateur — exactement comme de l'autre côté, et pour la même raison.*`,
  monde: `—`, qui: [`joel`],
  gardes: [`Repère d'écriture. La scène ne s'écrira pas.`],
  src: `décision du 16 août 2026`
},
{
  id: `g-accident`, no: `Repère`, col: 11, row: `joel`, acte: `Le registre`, gris: true,
  titre: `L'accident`,
  statut: `ouvert`,
  resume: `**Ce que la cérémonie des vingt-six raconte, de l'autre côté : un accident.** Un groupe d'enfants et leurs accompagnants adultes.`,
  produit: `🔴 **Personne dans le livre ne le saura jamais, et le roman ne le dira à aucun moment.** *La carte existe pour l'autrice seule : elle donne un visage au chiffre que le lecteur, lui, devra deviner.* **Vingt-trois petits chiffres et trois adultes dans le même paquet ne se lisent que d'une façon.**`,
  monde: `—`, qui: [`joel`],
  gardes: [`Repère d'écriture. **Aucune scène, aucune ligne, aucune allusion.** C'est le seul endroit du dossier où l'on écrit la réponse à une question que le livre pose sans jamais y répondre.`,
           `Rien ne relie cet accident à l'affaire Sorel : ce n'est pas la même histoire, c'est le même monde.`],
  src: `décision du 16 août 2026`
},
{
  id: `g-ancien`, no: `Non écrite`, col: 12, row: `joel`, acte: `Le registre`, gris: true,
  face: `s11`,
  titre: `Chez un ancien policier`,
  statut: `ouvert`,
  resume: `**Le pendant du veilleur de l'époque au jardin.** Un ancien policier, chez lui, qui était présent le jour d'une manifestation qui a dégénéré.`,
  produit: `**Le parallèle est exact : des deux côtés, c'est l'homme qui était là et qui n'est plus en service.** *L'un a huit ans et vit au jardin, l'autre a pris sa retraite — et tous les deux racontent une matinée sans se rappeler leur carrière.*`,
  monde: `—`, qui: [`joel`],
  gardes: [`On va le voir chez lui, et il répond à des questions. Il n'explique rien de son propre chef.`],
  src: `décision du 16 août 2026`
},
{
  id: `g-coldcase`, no: `Repère`, col: 17, row: `joel`, acte: `L'enlisement`, gris: true,
  face: `s14a`,
  titre: `Un cold case qui n'en est pas un`,
  statut: `ouvert`,
  resume: `**Le pendant du départ de la seconde enquête.** Deux jeunes filles du même âge, disparues quelques années plus tôt, dans la même région. Un dossier ancien qui ressemble exactement à ce qu'il cherche : un précédent.`,
  produit: `**Et ça ne mène nulle part, pour la même raison qu'en face.** Les deux sont vivantes. *Le dossier n'a simplement jamais été classé correctement — une défaillance administrative, et rien d'autre.*`,
  clef: `🔴 **Ce que la symétrie produit, et personne ne l'écrira jamais.** Il court après deux filles qui vont très bien — *pendant que les deux qu'il cherche vraiment sont en train de mourir.* **Le lecteur ne peut pas le savoir ; l'autrice, si.**`,
  monde: `—`, qui: [`joel`],
  gardes: [`Repère d'écriture. La scène ne s'écrira pas — c'est le chapitre du creux, juste après, qui portera ce qu'il faut en garder.`,
           `**Ce qui en passe dans le texte ne compte jamais les disparues, ne les sexue pas et ne leur donne pas d'âge.** *Une vieille affaire mal classée : c'est tout ce que le lecteur doit pouvoir lire, et c'est ce qu'il rapportera au dossier de l'arrivant.*`],
  src: `décision du 16 août 2026`
},
{
  id: `g-piste`, no: `Non écrite`, col: 26, row: `joel`, acte: `La remontée`, gris: true,
  face: `s17c`,
  titre: `Il a trouvé une piste seul`,
  statut: `ouvert`,
  resume: `**Le pendant de la remontée.** Joël a fini par trouver une piste, seul, **après avoir perdu énormément de temps.**`,
  produit: `*Le même mouvement, et c'est là que tout se joue : l'un a perdu ses semaines pour rien, l'autre a perdu ses deux semaines et arrive à l'heure. **Le lecteur lit un seul homme qui repart.***`,
  monde: `—`, qui: [`joel`],
  gardes: [`Le temps perdu ne se chiffre pas et ne se commente pas. Il se sent au ton.`],
  src: `décision du 16 août 2026`
},
{
  id: `g-entre`, no: `Non écrite`, col: 27, row: `joel`, acte: `La remontée`, gris: true,
  face: `s18`,
  titre: `Il entre seul, sans attendre`,
  statut: `ouvert`,
  resume: `**Le pendant exact, et il est écrit à l'identique.** Il a appelé, il sait que l'autre arrive, il n'attend pas.`,
  produit: `**C'est le seuil que le lecteur franchit deux fois** — une seule descente lue, deux escaliers, et derrière la porte un mouroir d'un côté et une cave repeinte de l'autre.`,
  monde: `—`, qui: [`joel`],
  gardes: [`Les deux descentes ne se citent jamais. Aucun personnage ne remarque le contraste.`],
  src: `04-plan/le-meme-jour.md §5 quater`
},
{
  id: `ouv`, no: `Première page`, col: 0, row: `andrew`, acte: `Ouverture`,
  titre: `La cérémonie d'Eliott`,
  statut: `acquis`,
  resume: `🔴 **Deux capsules surgissent le même matin** — *une noyade ne laisse aucun délai de maturation* — et la cérémonie se monte dans la journée. **Un arrivant de dix ans, un arrivant de quarante.** *On a prévenu tard, donc il y a peu de monde.* La cérémonie se déroule normalement. **Il n'y a rien à signaler, et le texte ne signale rien.**`,
  produit: `Le système entier passe là, sans un mot d'explication. Le garçon parle avant qu'on lui demande quoi que ce soit, avec une terreur qu'on ne s'explique pas — c'est inquiétant, on passe outre, la cérémonie se termine.`,
  clef: `Debout à côté de l'homme, Eliott le dévisage. Quelque chose se ferme sur son visage, ça dure le temps que ça dure, et il enchaîne. Personne ne le remarque.`,
  monde: `La capsule, l'éclaircie, la travée, le relevé à l'instrument, le nom qu'on produit soi-même, le numéro qu'on inscrit. Rien n'est expliqué : tout est fait devant le lecteur.`,
  qui: [`andrew`,`eliott`,`quarante`],
  gardes: [
    `⛔ **Rien de ce que dit le garçon ne doit pouvoir se rattacher au jour de sa mort.** *L'autrice, 17 août 2026 :* **« je veux pas qu'on puisse faire un lien quelconque avec le jour de l'accident — ça gâche l'épilogue qui nous apprend ce qui s'est passé. »**

⛔ *Donc : pas d'eau, pas de « en bas », pas de « il est pas remonté », pas de « il faut aller le chercher ».* **Ce qu'il dit doit n'avoir aucun sens** — c'est ça qui fait peur, et c'est ça qui protège la dernière page.`,
    `✅ **Ce qu'il dit, et c'est arrêté :** *« Il faut vider mes poches. »* — **« Elles sont pleines. »** — puis, plus doucement, **« Je reviens bientôt. »** *Il est nu sous une serviette de cérémonie. Deux ou trois personnes regardent quand même s'il y a des poches dessus.*`,
    `✅ **Nora hésite un temps, un seul, et le referme aussitôt.** *Correction de l'autrice :* **elle est un professionnel, pas quelqu'un qui bafouille.** *Ce qui se voit, c'est le temps d'arrêt — pas la phrase répétée.*`,
    `🔴 **L'ordre du chapitre est fixé — l'autrice, 17 août 2026, et c'est le vrai gain du premier jet.** *Le garçon se voit dans le miroir, balaie la pièce, et la capsule d'à côté passe dans ce balayage sans y peser.* **Son regard tombe sur Andrew, on lui demande son nom, il répond.** *C'est le nom donné qui fait basculer Andrew sur la seconde capsule* — et c'est pendant qu'il a les deux mains dans la seconde capsule, **de dos**, que le garçon se met à parler. Sa collègue a déjà pris le relais derrière lui.`,
    `✅ **Et « on passe outre » cesse d'être une décision.** *C'est une position de corps :* **« Andrew ne se retourna pas. Il avait les deux mains dans la capsule de l'homme. »** *Rien à commenter, rien à justifier — il travaille.*`,
    `⛔ **La cérémonie des vingt-six ne s'évoque pas ici.** *Coupée du premier jet par l'autrice, 17 août 2026 :* **on y viendra avec la suite de l'enquête**, et pas en page une.`,
    `✅ **Les visiteurs ne sont pas froids, et c'est une naissance.** *Correction de l'autrice, 17 août 2026 :* silence cérémonieux jusqu'aux cadeaux, **puis du bruit pour la première fois** — on se penche pour voir, on commente, on se serre le bras sans se connaître, des « bienvenue » se reprennent de bouche en bouche. *La règle du monde tient quand même, mais elle passe après la joie :* **« Aucun d'eux ne les connaissait. Aucun ne les reverrait. Ça n'enlevait rien. »**`,
    `✅ **La salle, et rien de plus.** *Le complexe entier ne se décrit pas ici* — il est gardé pour la journée type à la ruche. **On ne voit que la salle six et ce qui s'y passe.**`,
    `✅ **L'image qui porte le lieu, en trois lignes :** la sculpture monte à mi-hauteur d'une colonne et s'arrête, la coulée prend le relais et continue jusqu'en haut. **« On ne savait pas laquelle des deux avait copié l'autre. »** *⛔ Pas de balcons, pas de catalogue d'ornements.*`,
    `⛔ **Aucune capsule pourrie dans le prologue, et pas une allusion.** *L'autrice, 17 août 2026.* **La première que le lecteur rencontre est celle de la journée à la ruche**, et elle doit le révulser sans qu'il ait été prévenu. *Une mention en page une lui retirerait tout.*`,
    `✅ **Le miroir — trouvaille de l'autrice, 17 août 2026.** *Le veilleur tend un miroir à l'arrivant pour qu'il fasse connaissance avec sa propre apparence.* **C'est un geste de protocole, au même titre que la couverture** : personne ne l'explique et personne ne s'en étonne.

✅ **Et ça rend possible la dernière page.** *À l'épilogue, Eliott dira de l'homme d'à côté : « j'ai vu ses yeux, tout pareils que les miens ».* **Il ne pouvait le dire que s'il venait de voir les siens.** — *À vérifier : si c'est Andrew qui tient le miroir, alors l'homme qui lui a montré son propre visage est celui à qui il racontera l'histoire six cents pages plus loin.*`,
    `La scène ne doit rien peser. Pas de gros plan, pas de phrase de narrateur sur ce regard, pas de retour dessus dans les pages suivantes.`,
    `🔴 **Le chiffre est annoncé, et c'est un changement du 17 août 2026.** *La foule estime à vue et se trompe — elle chuchote « douze », puis « treize »* — **puis le veilleur sort son instrument, fait le relevé et tranche pour tous :** « Capsule éclaircie, arrivant réactif. L'Archiviste lui a compté dix ans. » *La marge entre l'estimation et le nombre se referme à chaque cérémonie, et le livre s'en sert dès la première page.*`,
    `Puis ils sont affectés ailleurs et ne se revoient jamais. Aucune retrouvaille, aucun personnage qui rapproche les deux noms.`,
    `Il n'y a pas de capsule défaillante ce jour-là.`
  ],
  ouvert: [`Combien de lignes doit durer le dévisagement ? Trop peu ne s'imprime pas et le lecteur ne s'en souviendra pas à l'épilogue ; trop long, ça l'annonce.`,
           `✅ **Il s'appelle Nicolas** — *validé le 17 août 2026.* **Il apparaît deux fois, ici et scène 8**, et rien ne doit inviter à le rapprocher de celui d'Eliott.`,
           `⚠️ **La case des observations, à la toute fin.** *Il la regarde un moment, puis il range le carnet.* **C'est le seul endroit du chapitre qui pèse un gramme** — à garder ou à couper.`,
           `⚠️ **La phrase d'accueil entière est donnée ici** — *« Bienvenue à toi »* — alors qu'à sa propre cérémonie Andrew n'en attrapera que le début. **Gratuit si on la garde, mais il faut le vouloir.**`],
  lecture: `Première lecture : un gamin bizarre. Seconde lecture : il regarde quelqu'un qui lui fait éprouver une chose qu'il ne sait pas nommer.`,
  src: `04-plan/le-parcours-de-l-enquete.md — « Avant le parcours »`
},
{
  id: `s1`, no: `Scène 1`, col: 2, row: `andrew`, acte: `Avant la disparition`,
  titre: `Première visite chez June`,
  statut: `acquis`,
  resume: `Andrew vient voir le garçon, et ce n'est pas la première fois. June ouvre sans être surprise. Ils sortent — c'est devenu leur habitude : Andrew lui montre des endroits qu'il ne connaît pas. Au retour, ils longent l'école et le terrain d'endurance.`,
  produit: `🔴 **La « première visite » n'est pas la première, et c'est ce qui règle tout.** *Décision de l'autrice, 22 août 2026.* **June ouvre sans étonnement, elle interpelle Eliott, ils partent.** *Rien ne dit depuis quand il vient, personne ne le demande, et le mois qui sépare l'arrivée du garçon de sa disparition n'a plus à être justifié.*`,
  clef: `🔴 **Le chapitre s'ouvre sur ce qu'il n'a pas fait.** *Le prologue s'achève sur une case d'observations restée vide : il a vu Eliott imiter les gestes de Nicolas sans s'en rendre compte, la plume s'est attardée, et il n'a rien écrit.* **Ouverture proposée : « Il n'avait rien écrit dans la case. »** *Le manque est posé avant les présentations, donc les présentations servent à quelque chose.*

⛔ **Et le manque ne se comble jamais.** *Ni ici, ni plus tard. C'est le fil qui traverse les trois chapitres sans être nommé : un homme qui retourne voir un gosse parce qu'il n'a pas su remplir une case.*

⛔ **Ce qu'il rouvre est son carnet, jamais le registre.** *Correction de l'autrice, 22 août 2026 : le registre est une salle, la ronde au cœur de la ruche — on n'y feuillette pas une page.* **Et elle est réservée à la scène 8**, où Andrew y revient pour de bon. *Ici, il rouvre la poche de sa blouse, et c'est tout.*

⛔ **Et son trouble ne se nomme jamais.** *La fiche d'Andrew l'interdit : pas d'illumination, pas même atténuée — <em>il chasse l'idée</em>, <em>quelque chose lui échappe</em> sont faux.*

🔴 **Mais le geste seul ne suffisait pas, et l'autrice l'a repris le 22 août 2026 :** *« à un moment donné, ça l'interroge quoi, on peut pas appeler un chat un chien. »* **La sortie n'est pas de lui faire pressentir quelque chose : c'est de lui faire chercher un mot qu'il n'a pas.**

✅ **Ce qui manque à Andrew n'est pas la compréhension, c'est la case.** *Il sait ce qu'il a vu et il sait ce qu'est une observation : une capsule en retard, un instrument qui a sauté, une salle qu'on a changée.*

🔴 **Et le fait tient en une phrase — reprise de l'autrice, 22 août 2026 :** *« il l'a imité, l'autre s'est arrêté, ça a cassé l'action, fin de l'histoire. La question est, pourquoi il a cherché à l'imiter ? »* **C'est la question qui doit rester sur la page, pas le détail des gestes.**

✅ **D'où la chute : il n'y avait pas de case pour une question.** *La colonne attend un fait ; il n'a qu'un pourquoi.* ⛔ *Il ne conclut rien, il ne pressent rien : il remet le carnet dans sa poche et il va ouvrir sa salle.*

⛔ **Un veilleur prend une salle, pas une travée.** *J'avais écrit « il descendit prendre sa première travée » : le chapitre premier dit le contraire — les travées ont une salle en face, et c'est la salle qui revient au veilleur.* **Et rien ne le place à un étage : il ne descend nulle part.**`,
  garde_forme: `**Le déroulé, tel que l'autrice l'a posé :** ① il sonne, June ouvre sans surprise — description très brève ; ② Eliott, et c'est là que le lecteur le voit vraiment pour la première fois ; ③ ils sortent — **l'aquarium, décision du 22 août 2026, et ils entrent dedans** : 🔴 *et il doit être merveilleux, pas correct — reprise de l'autrice, 23 août 2026 : « il n'a jamais vu d'aquarium de sa vie, le truc le plus banal peut être quelque chose de merveilleux pour lui »*. **Le but est de donner au lecteur l'envie d'aller s'y promener** — *des bassins immenses, un qui passe au-dessus des têtes, la pénombre qui est là pour les poissons, des couleurs qu'on n'a pas l'habitude de voir ensemble, et des tailles qui impressionnent sans qu'on sache les nommer.* ✅ **Et on nomme les choses — reprise de l'autrice, 23 août 2026 :** *« autant directement dire que c'est une anémone, et ne pas passer par quatre chemins ».* **Anémone, corail, méduse, raie.** *La périphrase faisait précieux, et le vocabulaire des objets est commun aux deux mondes.*

🔴 **L'aquarium marche au don — décision de l'autrice, 23 août 2026.** *Un guichet à l'entrée, une pancarte qui propose des montants : la nourriture d'une semaine, l'entretien d'un bassin, les soigneurs.* **Rendre le lieu accessible à tous va de soi ; donner est un usage, pas une condition.** *— Il faut payer ? — Non. Et Andrew pose quand même de quoi pour deux dans la coupelle.* ⛔ **Le mot <em>quand même</em> porte tout le système, et rien ne l'explique.**

⛔ **Un bassin n'est pas une espèce.** *Reprise de l'autrice, 23 août 2026 : « les espèces sont rarement séparées dans un aquarium, tu peux avoir des tableaux très beaux avec beaucoup de couleurs ».* **Le premier bassin de la salle basse les mélange donc tous** — *corail, anémone, poissons-clowns, petits jaunes et le rond et plat au milieu.*

🔴 **Une pieuvre, et pas des axolotls — décision de l'autrice, 23 août 2026.** *Je lui avais signalé que l'axolotl était un second animal qui ne suit pas le cours ordinaire d'une vie, après les méduses ; elle l'a écarté.* **Il reste donc un seul de ces échos, et c'est le bon.**

*Un bras d'abord, qui se déroule le long d'une pierre et se colle dessus par en dessous. Puis tous les autres à la fois.* **— Il y en a combien ? — Huit.** *Et il les compte en la suivant.*

🔴 **La courbe du chapitre, arrêtée par l'autrice le 23 août 2026.** *Elle tient en quatre temps et elle commande l'ordre des bassins.*

**① Il s'ouvre devant le petit poisson** — *« Regardez celui-là »*, puis il chante pour lui seul. **② Il se referme aussitôt après**, sur sa propre fabulation : *une boîte en verre, un meuble, un tapis dessous* — *« vous me croyez pas », « c'est pareil », « tout le monde fait ça, on dit ah et après on parle d'autre chose »*, mains dans les poches. **③ La fermeture dure trois bassins** : *les herbes où Andrew dit « je te crois » sans qu'il le prenne, les axolotls qui lui arrachent deux mots, la raie sous laquelle il rechante à mi-voix — il va mieux, il ne parle toujours pas.* **④ Andrew le relance :** *« Il était de quelle couleur, le meuble ? »*

⛔ **Personne ne nomme ce qui vient de se passer.** *Un homme a demandé un détail à un garçon que personne n'écoute — c'est un réflexe d'enquêteur, et il ne sait pas qu'il en a un.* ✅ **C'est la réponse à « pourquoi il vous parle, à vous », et elle n'est jamais donnée.**

⚠️ **Et la fabulation porte sur le petit poisson, pas sur la raie.** *Repérage de l'autrice : personne n'a de raie dans son salon.*

⛔ **Les méduses sont écartées — décision de l'autrice, 23 août 2026.** *Le caméo était le sien : celle qu'on étudie chez nous peut inverser son cycle et recommencer.* **Mais elle fait quelques millimètres, ne se maintient qu'en laboratoire et n'est jamais présentée au public** — *il aurait fallu un bac à part et un verre grossissant pour la rendre plausible, et ça ne valait pas ce que ça coûtait.* ✅ *« Si un problème, on fait sauter les méduses, ça n'apporte rien de plus. »*

💡 **Les axolotls reprennent la place.** *Quatre, roses et pâles, posés sur du sable clair, qui ne font rien du tout. L'un d'eux ouvre la bouche, la referme, et en garde l'air content.* **— Il sourit. — On dirait.** *C'est le seul moment de complicité du chapitre.*

✅ **Et l'objection que j'avais faite tombe avec les méduses :** *l'axolotl était le second animal du chapitre à ne pas suivre le cours ordinaire d'une vie ; il est maintenant le seul.* ⛔ **Rien ne le dit, rien ne l'appuie.** ; ④ au retour, l'école et le gymnase, en passant — **et le contraste est le sujet du chapitre** : *un lieu où on l'emmène et où il entre, une cour où il n'entrera jamais.*

**Fin proposée :** *ils rentrent, Eliott passe la porte, Andrew reste une seconde devant.* **« Il ne compta pas les pas du retour »** — l'écho du chapitre premier dit qu'il est ailleurs sans dire où. ⛔ *Et le chapitre ne se ferme pas chez lui : le lecteur ne doit jamais voir où Andrew habite.*`,
  monde: `🔴 **Le quartier des berceuses, réglé par l'autrice le 22 août 2026 :** *des pavillons, chacun le sien, un carré d'herbe devant et une allée de gravier — pas des maisons serrées les unes contre les autres.* **Elles habitent du côté du jardin sans que toutes y soient accolées.** Le métier de berceuse vu de l'intérieur : quelqu'un qui a la charge de trois personnes. **Un aquarium, et ce que ce monde-là fait d'un lieu qu'on visite.** Et l'école, depuis la rue, en longeant la grille — **celle où Eliott n'ira jamais.**`,
  qui: [`andrew`,`eliott`,`june`,`paul-julie`],
  gardes: [
    `Ce n'est jamais une audition.`,
    `🔴 **June a trois arrivants à charge, et Eliott est le dernier arrivé.** *Décision de l'autrice, 22 août 2026 : Paul et Julie vivent là depuis plus longtemps que lui.* **Ça donne à June sa profondeur — elle n'est pas en peine avec un garçon, elle est en peine avec celui-là** — *et ça explique sans un mot pourquoi elle est soulagée que quelqu'un vienne.*`,
    `**Aucune phrase ne justifie ses visites** — ni du narrateur, ni de lui, ni d'un tiers. *On écrit qu'il y va.* ⛔ **S'il sait pourquoi il y va, le retournement final n'a plus rien à retourner.**`,
    `🔴 **La sortie, elle, est habillée — la visite ne l'est pas.** *Décision de l'autrice, 22 août 2026 : c'est devenu leur rituel, Andrew montre au garçon des endroits qu'il ne connaît pas.* **Le lecteur a donc une réponse à la question facile, ce qui l'empêche de poser la difficile.** ⛔ *Et June n'organise rien : elle n'a pas à proposer, c'est déjà une habitude.*`,
    `**June : visage un peu fermé, mais soulagée.** *Elle n'est pas au bout — elle a du mal à créer le lien avec Eliott, et ça la travaille.* **Une réplique suffit, dite sans y penser : « il vous parle, à vous. »** ✅ *Validée par l'autrice le 22 août 2026.*`,
    `⚠️ **Une seule colère, jamais comprise, et elle n'est pas ici.** *Elle est rapportée bien plus tard, quand Joël et Liam viennent l'interroger.* ⛔ **Pas de colères au pluriel : le motif est le reliquat corporel de la noyade, et le banaliser tôt le dépense.**`,
    `Rien de ce que dit Eliott ne doit être vérifiable ni se recouper avec ce qui remonte chez Andrew.`,
    `🔴 **Deux ou trois gestes qu'il ne devrait pas connaître, et pas un de plus.** *Décision de l'autrice, 22 août 2026.* **Des gestes, jamais des savoirs** — *un savoir se vérifie, un geste n'est qu'une bizarrerie d'enfant.* **Un seul ici — décision de l'autrice, 23 août 2026, reprise le même jour :** *il ne fredonne pas un air, il chante une vraie chanson, avec des mots dedans, et il en connaît la fin.* **Il y est question d'eau, ou de ce qu'il y a dessous.** ⛔ *Andrew ne la connaît pas et ne demande pas où il l'a apprise — il s'interroge, il ne relève pas.* ✅ **Et le garçon chante parce qu'il s'est enfin détendu ; rien ne le dit.** ⛔ **Le sifflet est à la tournée.**

⛔ **Et le carrefour saute.** *Le garçon quittait le trottoir sans regarder, Andrew le rattrapait par le col, et il disait « normalement ils me laissaient passer, ici ».* **Trois raisons de le retirer, données par l'autrice :** *il tombait comme un cheveu sur la soupe entre deux paragraphes ; il faisait redondance avec la boîte en verre sur le meuble, qui est plus forte ; et toutes les interactions gagnent à se passer dans l'aquarium.* ✅ *Il réglait au passage un manquement à l'interdit n° 5 — « pas de feu, pas de passage protégé, pas même un panneau » décrivait trois absences à la file.*

⛔ **Et la réplique du carrefour est abandonnée pour de bon — décision de l'autrice, 23 août 2026.** *Elle aurait fait une seconde fabulation développée dans le même chapitre que l'épicerie, et le lecteur n'aurait pas su laquelle retenir.* ✅ **L'épicerie se noie dans du banal, pas dans une phrase aussi marquante qu'elle** — *une ligne suffit à dire qu'il en a dit deux ou trois autres, sans les rapporter.*`,
    `🔴 **La chaussée, telle que l'autrice l'a réglée le 22 août 2026.** *Eliott descend sans regarder, Andrew le chope par le col, et le garçon dit :* **« normalement ils me laissaient passer ici. »** *Il a reconnu un endroit, et une priorité au piéton qui n'existe pas ici.* **Un geste, un incident, une phrase fausse — et rien à vérifier.**`,
    `⛔ **On ne rebaptise aucun objet et on n'en escamote aucun.** *Le monde a des voitures, des poteaux, des trottoirs, et ils portent leurs noms.* **Inventer un vocabulaire d'objets ferait exploser le glossaire et trahirait la couture dès le premier chapitre de Joël.** *Voir les interdits, « Et le vocabulaire des objets n'est pas un interdit non plus ».* ⛔ **L'idée du rond-point est écartée.**`,
    `🔴 **L'aquarium, réglé par l'autrice le 22 août 2026 — et il tient sur une réticence qui cède.** *Eliott boude le lieu au début, il n'est pas à l'aise ; Andrew insiste juste ce qu'il faut — tu ne seras pas déçu — et de toute façon il n'a pas prévu de vêtements de rechange.* **Puis c'est un gros whaou** : *des spécimens colorés, et un gamin qui s'excite pour la première fois du chapitre.*`,
    `🔴 **Et la réplique des vêtements de rechange fait tout le travail sans le savoir.** *Elle dit une seule chose au garçon : on ne va pas se baigner.* **Andrew désamorce une terreur dont il ignore tout, en parlant de linge.** ⛔ *Personne ne le relève, et surtout pas le narrateur.*`,
    `✅ **La chronologie est tranchée : le cours de natation n'a pas encore eu lieu.** *Décision de l'autrice, 22 août 2026.* **Sa peur de l'eau n'a donc encore été vue par personne** — *ni par June, ni par Andrew, ni par le lecteur.* **La réticence du début est lisible comme une mauvaise humeur de gamin, et c'est exactement ce qu'il faut.**`,
    `⛔ **Andrew ne relève ni l'air fredonné ni la chaussée.** *Pas un regard appuyé, pas une phrase de narrateur, pas un silence qui compte.* 🔴 **Il ne relève que le sifflet, à la tournée — décision de l'autrice, 22 août 2026** — *et c'est le seul des trois qui ne prouve rien.* **Voir la fiche de la tournée : c'est ce qui rend crédible son silence sur le reste.**`,
    `⛔ **L'école ne tourne jamais à la drôlerie.** *Un professeur de quinze ans, un homme de quatre-vingt-douze ans qui lève la main, surexcité, deux élèves repris par la maîtresse — et personne dans la rue ne s'arrête pour regarder.* **Le lecteur seul trouve la scène étrange, et il ne doit rien lire qui l'y invite.**`,
    `⛔ **Aucune insistance sur l'itinéraire.** *Pas de description de trajet, pas de rue nommée deux fois, rien qui ait l'air d'être posé pour servir.* **L'école est en travers du chemin, pas une étape.**`,
    `⛔ **Aucun personnage ne cherche où se mettre dans ce chapitre.** *L'autrice avait écrit « il ne savait pas vraiment où se mettre » à l'entrée du séjour ; c'est la première phrase de l'épilogue, mot pour mot ou presque : « Il n'y avait aucun endroit où se mettre. »* **L'image appartient à la dernière page du livre, où elle porte tout le chapitre.** *Ici, « Andrew resta debout, comme les autres fois » dit la même gêne et dit en plus l'habitude.*`,
    `🔴 **La saison est le printemps — décision de l'autrice, 22 août 2026.** *Le cerisier de June est plein à craquer ; il ne fait pas chaud, il fait beau.* **La raison est une contrainte, et elle vaut d'être retenue :** *j'avais placé la scène en plein été, et un lecteur de chez nous ne peut pas lire « il fait une chaleur » puis voir, au retour, une école en cours.* ⛔ **Personne ne parle du temps qu'il fait** — *June propose un verre d'eau sans invoquer la chaleur.*`,
    `🔴 **C'est ici que le mot jardin entre dans le livre, et il entre par une bouche.** *Repérage de l'autrice, 22 août 2026 : ni le prologue ni le chapitre premier ne le prononcent.* ⛔ **Donc pas de phrase de décor qui explique où habitent les berceuses** — *c'était le narrateur qui posait une règle du monde, et la règle 10 l'interdit.* **Andrew le dit à June, à propos de Paul, et tous les deux savent de quoi ils parlent :** *« Il est content d'aller au jardin ? »* **Le lecteur n'a rien à comprendre encore.**`,
    `✅ **Le métier de berceuse se dit clairement, en un paragraphe — décision de l'autrice, 22 août 2026.** *« Autant le dire clairement, comme on a pu dire à quoi servait un analyste et un préparateur. »* **Le chapitre premier a posé le précédent :** *le paragraphe sur l'analyste qui tranche et le préparateur qui cueille est du narrateur, et il tient.* 🔴 **Et il passe par ce qu'Andrew voit d'elle, pas par une définition.** *Reprise de l'autrice, 22 août 2026 : la première version en disait « trop et pas assez à la fois », et elle était abrupte.* **On part de la douceur — ce qu'il voit d'elle à chacune de ses visites — et le métier vient après.** *Prendre, accompagner, remettre : le même mouvement, toujours.*

⛔ **Ce qui n'est pas dit : ce qu'est le jardin.** *Elle passe la main à la grille, et le narrateur s'arrête là.*

✅ **Et « ni école ni tuteur » quitte ce paragraphe** — *décision de l'autrice : ça tombera tout seul au retour, quand ils longeront la grille de l'école.*`,
    `⛔ **Une seule inversion des âges par chapitre, et c'est Julie qui la porte.** *Question de l'autrice, 22 août 2026 : j'avais écrit « vingt-deux ans, à peu près, et berceuse depuis plus longtemps que ça », et Julie dit la même chose deux paragraphes plus loin.* **La sienne est plus forte** — *un corps de dix ans qui pique un ourlet sans épingle, et onze ans de métier derrière ; ça se voit avant d'être dit.* **La phrase de June s'arrête donc à « et berceuse ».**

✅ *Et son expérience se dit quand même, mais par elle et sans malice : « Moi, c'est le quatrième. On s'y fait. »*`,
    `⛔ **Eliott ne va pas à l'école, et il n'a jamais commencé de cours accélérés.** *La fiche disait le contraire : c'était faux, corrigé le 22 août 2026.* **À son âge, c'est le berceur qui instruit** — *June lui apprend ce qu'il faut, et elle ne passe la main que pour ce qu'elle ne peut pas donner elle-même, comme la natation.* **Les cours du soir et les tuteurs sont pour les arrivants de cinquante à soixante-dix ans.**`,
    `⛔ **Le paragraphe de l'école ne dit pas ce qu'il reste à vivre.** *Repérage de l'autrice, 23 août 2026 : « L'école accueillait ceux qui arrivaient avec encore toute une vie devant eux » est horrible si on ne connaît pas encore le système.* **Trois lignes après « parce que je suis trop petit », le lecteur ferait le calcul : plus on arrive haut, plus on a de temps — donc ce garçon-là n'en a presque pas.**

⛔ **Ce n'est pas le chapitre qui doit apprendre ça, et personne n'a de raison de le dire ici.** *La phrase devient « L'école prenait ceux qui arrivaient tout en haut » : l'information passe, la sentence tombe.*`,
    `⛔ **Aucun âge précis à l'école — décision de l'autrice, 23 août 2026.** *On voit que la maîtresse est bien plus jeune que ceux qui l'écoutent, et c'est tout ce qu'on écrit.* **L'homme du troisième rang n'a plus quatre-vingt-douze ans, il lève la main.**

✅ **Et les deux qui papotent gagnent leur malice :** *une main devant la bouche, reprises sans qu'elle se retourne ni hausse le ton, et elles se taisent le temps qu'il faut avant de recommencer plus bas.*

⛔ **La fenêtre est au ras du trottoir.** *Je l'avais mise au premier étage : on ne voit rien d'une classe depuis la rue si elle est en hauteur.* ✅ **Et le terrain n'est pas ailleurs :** *toujours derrière la même grille, les salles laissent la place à un terrain avec des lignes peintes au sol.*

⛔ **Les coureurs ont tous le même âge.** *La phrase qui comparait le plus jeune d'entre eux au professeur saute : à l'école, ils sont de la même tranche, sinon ils seraient aux cours du soir.*

🔴 **Le partage des trois régimes, arrêté le 23 août 2026 :** *l'école prend ceux qui arrivent vers quatre-vingts ou quatre-vingt-dix ans et dure des années ; ceux d'autour de cinquante ou soixante entrent tout de suite dans la vie active, avec des cours décalés le soir et un tuteur au cas par cas ; et pour les plus jeunes, c'est un berceur du premier jour au dernier.* ✅ **Le glossaire a été mis à jour dans le même mouvement.**`,
    `🔴 **Et c'est ce qui donne la réplique de l'école — donnée par l'autrice le 22 août 2026.** *Devant la grille, au retour :* **« C'est donc à ça que ça ressemble, l'école ? June m'a dit que je ne pourrais jamais y aller parce que je suis trop petit. »** *Le renversement se fait tout seul : ici l'école est pour les vieux, et les petits n'y ont pas droit.* ⛔ **Personne ne le lui explique et le narrateur n'y touche pas.**`
  ],
  phrases: [{ t: `normalement ils me laissaient passer ici`,
             n: `✅ **Donnée par l'autrice le 22 août 2026.** *Dite après qu'Andrew l'a rattrapé par le col, sur un ton d'évidence — il ne se justifie pas, il constate.* **Elle invoque une règle, pas un objet** : une priorité au piéton qui n'existe pas ici, et que personne ne songe à lui expliquer.\n\n⛔ **Elle ne se vérifie pas et ne se recoupe avec rien.** *C'est une fabulation de plus, de la même famille que le magasin de chaussures — et Andrew ne la relève pas.*` },
            { t: `il vous parle, à vous`, n: `✅ **Validée par l'autrice le 22 août 2026.** *Dite sans y penser, sur le pas de la porte.* **Elle ne dit pas pourquoi il vient — elle dit pourquoi elle le laisse.** *Ce sont deux questions différentes, et seule la seconde a le droit d'une réponse.*` }],
  ouvert: [`⚠️ **Combien de lieux du rituel sont montrés.** *L'aquarium occupe déjà toute l'aller ; un second lieu ferait visite guidée.*`,
           `✅ **La répartition des gestes est tranchée le 22 août 2026.** *L'air fredonné et la chaussée ici ; le sifflet à la tournée.* **Raison de l'autrice : à la seconde visite, il n'est pas en état de fredonner — il est agacé.**`],
  src: `04-plan/le-parcours-de-l-enquete.md §2 — 03-personnages/eliott.md §4 bis — décisions du 22 août 2026`
},

{
  id: `s2`, no: `Scène 2`, col: 3, row: `andrew`, acte: `Avant la disparition`,
  titre: `La tournée`,
  statut: `acquis`, pivot: true,
  resume: `Il y est retourné plusieurs fois — une ellipse le dit en deux lignes. Cette fois-là, il le rejoint sur sa tournée : Eliott a le visage fermé, agacé. Le portage vu de son point de vue. Au retour chez la berceuse, le garçon dit au revoir et se sauve à l'intérieur ; Andrew reste sur le pas de la porte avec June.`,
  produit: `🔴 **June est anxieuse, et elle échoue pour la première fois — décision de l'autrice, 23 août 2026.** *Elle en a eu six avant lui, il y en a eu des difficiles, ça s'est toujours arrangé.* **Là, non.** *Il est poli, il aide, il répond ce qu'il faut pour qu'on arrête de demander — et au bout d'un mois elle ne saurait pas dire ce qu'il aime.*

⛔ **Elle ne se plaint pas : elle donne un résultat.** *« Je crois qu'il n'a pas envie de me connaître. Et c'est mon métier. C'est exactement mon métier. »*

✅ **Ils s'asseyent sur les marches.** *Andrew ne franchit toujours pas la porte, mais la conversation a le temps de se faire.*

🔴 **La blessure n'est plus montrée : elle est rapportée, et une porte s'est refermée entre les deux.** *Décision de l'autrice, 22 août 2026.* **On voit un visage fermé sans savoir pourquoi, le gamin file, et on apprend la raison une fois qu'il n'est plus là.** *Le lecteur recompose la journée à rebours, et Andrew reste dehors avec une chose qu'il n'a pas vue arriver.*`,
  clef: `🔴 **Le ton d'Eliott sur toute la tournée : à cran, et pas contre Andrew.** *Indication de l'autrice, 23 août 2026 : « un peu comme un futur ado, un truc le gonfle et il est à cran sur tout ».* **Ça se voit partout et ça ne vise personne** — *il ne remercie pas la femme à la lettre, il donne un coup de pied dans un caillou qui ne part pas, il répond sec à des questions qui n'attaquent rien.*

✅ **Et l'épicerie n'est plus un entêtement, c'est une contrariété de plus.** *Il s'arrête, il regarde la devanture, il inspire un coup — puis :* **« Bon. C'est pas grave, j'ai rien à y livrer de toute façon. »** *Et il repart sans y jeter un œil.* ⛔ **Il ne défend pas sa version, il la lâche** — *ce qui la rend beaucoup plus difficile à ranger dans le délire.*

🔴 **Ce que le garçon cache derrière ce qu'il dit — décision de l'autrice, 23 août 2026.** *Il tourne autour du pot, et ce qu'il sort est un sentiment d'injustice : on ne lui a pas demandé ce qu'il voulait faire, on lui a donné le portage.* **Le métier des autres a l'air plus vrai que le sien.** *Il en veut au monde de ne pas l'avoir consulté — et il projette là-dessus ce qu'il ne dit pas.*

⛔ **Ce qu'il ne dit pas : ce qui se passe vraiment au travail.** *Le lecteur ne l'apprendra qu'au chapitre suivant, quand June racontera qu'il est rentré avec les genoux en sang.* **Ici il ne lâche qu'une phrase, et elle a l'air de rien :** *« ils le disent pas aux autres, ils le disent à moi ».*

✅ **Et Andrew croit tenir le problème.** *Il le dit à June — personne ne lui a demandé ce qu'il voulait faire — et il garde pour lui la réserve : ça n'explique pas le premier jour.*

🔴 **C'est June qui dit le mot, et la question des deux bouches est tranchée.** *Décision de l'autrice, 22 août 2026 : elle rapporte qu'Eliott lui a dit que les autres le traitaient de porteur de voiles au boulot.* **Elle parle aussi de ses difficultés à elle** — le garçon ne va pas bien, il se referme, et elle n'arrive pas à créer le lien.

⛔ **Elle n'en fait jamais une hypothèse.** *C'est une phrase qui s'arrête, pas un relais d'information — elle bute sur un mot et passe à autre chose.*`,
  garde_forme: `🔴 **Ce chapitre a le droit d'être court, et c'est même ce qu'on lui demande.** *Constat de l'autrice, 23 août 2026 : « le suivant n'a quasiment rien en comparaison, on va sans doute pas passer autant de temps dans la ville avec le travail ».* **Le prologue fait 2 644 mots, le chapitre premier 3 765, le deuxième 3 442** — *et la tournée n'a pas de lieu à faire découvrir, elle a une nouvelle à faire tomber.*

✅ **Les chapitres doivent raccourcir à mesure que ça se resserre.** *Deux longs pour installer le monde et le lien, puis la tournée, puis la place vide qui sera plus courte encore.* **L'accélération se sent d'autant mieux qu'on vient de passer trois mille mots dans un aquarium.** ⛔ *Rien à rallonger pour équilibrer.*

**Le déroulé, tel que l'autrice l'a posé :** ① l'ellipse — *« il y retourna le mardi suivant, et le mardi d'après »* — qui donne le mois entier et la récurrence en deux lignes ; ② Eliott sur sa tournée, visage fermé ; ③ le métier de portage de son point de vue ; ④ retour chez la berceuse, il sonne, dit au revoir, se sauve ; ⑤ Andrew et June sur le pas de la porte.

**Fin proposée :** *le mot en dernière réplique, puis un geste et rien d'autre —* **il regarde la fenêtre du haut, elle est fermée.** *Le lecteur enchaîne parce qu'il vient d'apprendre une chose que le gamin ne sait pas qu'on a dite.*`,
  monde: `⛔ **Le palier ne s'explique pas dans ce chapitre — décision de l'autrice, 23 août 2026.** *Ni la mécanique, ni le temps qu'il reste à un arrivant de dix ans, ni ce que ça fait grincer chez ceux qui ont trimé.* **C'est Henri qui l'apprendra au lecteur**, scène 6, socialement, par un homme qui tient un effectif.

✅ **Ce qui est permis ici, et rien de plus — décision de l'autrice, 23 août 2026 :** *Andrew peut nous apprendre, par son métier, ce qu'il a déjà constaté des variantes d'espérance de vie, sans entrer dans le détail.* **Il constate, il n'explique pas.**

✅ **Et la conséquence pratique est validée telle quelle :** *« on la fait à pied, faute d'avoir le temps devant soi pour apprendre à conduire »* — *modèle pris au glossaire, à l'entrée Portage.* ⛔ **Aucun chiffre. Et Andrew ne calcule jamais un âge, ni à voix haute ni dans sa tête.**

**Le portage, le métier d'Eliott** — l'équivalent d'un petit postier — vu en marchant, par celui qui le fait. *Et c'est par June que le lecteur apprend ce qu'est un porteur de voiles, sans qu'aucun narrateur ne l'explique.*`,
  qui: [`andrew`,`eliott`,`june`,`paul-julie`],
  gardes: [
    `🔴 **Le mot arrive par le bas, pas par le haut.** *Décision de l'autrice, 20 août 2026 :* **porteur de voiles est une croyance, et le mot n'est pas tendre** — *on l'emploie couramment pour dire de quelqu'un qu'il raconte n'importe quoi, et on en traite les gens.* **C'est comme ça que le lecteur l'apprend : entendu, pas expliqué.**`,
    `Personne ne le confirme. Une gêne n'est pas une fissure — c'est ce qui la rend compatible avec l'interdit n° 4.`,
    `Il n'est jamais repris, pas même quand le garçon disparaît.`,
    `**Ce que dit le garçon ne mène nulle part, et c'est la règle.** *Rien de ce qui sort de sa bouche ne se vérifiera jamais* — ni ici, ni plus tard, ni à la relecture. **L'hypothèse « il fabulait » doit rester debout jusqu'à la dernière page.**`,
    `🔴 **C'est ici que tombe la phrase de l'épicerie.** *Décision de l'autrice, 22 août 2026 : dans la tournée, dehors, en marchant, noyée parmi d'autres.* **Il peut buguer dessus.** ⛔ *Et rien ne la distingue des autres : c'est une fabulation de plus, et elle est fausse comme les autres.*`,
    `🔴 **Andrew ne dépasse pas le seuil, et c'est une progression sur trois chapitres.** *Décision de l'autrice, 23 août 2026.* **Au deuxième il entre et reste debout au milieu de la pièce ; ici il ne franchit pas la porte ; à la place vide, elle s'ouvre avant qu'il ait frappé et il n'entre pas du tout.** *De plus en plus près de la porte, de moins en moins dedans.*

⛔ **Rien de la maison ne se redécrit** — *il n'y met pas les pieds, et c'est ce qui permet de revenir au même endroit deux chapitres de suite sans que ça pèse.* ✅ **Le vide de la scène suivante ne se sent que si la place était pleine.**`,
    `⚠️ **La tournée se fabrique ici, et elle sert encore — autrement.** *Andrew la refera seul à la scène 17 c, comme la dernière fois qu'il l'a vu dans ce contexte de sortie.* **Les lieux doivent donc être sur la page, nommés banalement, comme du décor qu'on traverse** — sinon le lecteur ne peut pas revenir en arrière et retrouver l'endroit.`,
    `⛔ **Aucune insistance sur l'itinéraire.** *Rien qui ait l'air d'être posé pour servir.*`,
    `⛔ **L'école n'est plus ici.** *Elle est passée à la visite précédente, avec la découverte — décision du 22 août 2026.*`,
    `🔴 **Le sifflet tombe ici, et il a un motif.** *Décision de l'autrice, 22 août 2026 : en marchant, Eliott aperçoit Julie — l'une des deux autres arrivantes de chez June — et la siffle entre ses doigts pour l'interpeller.* **— Tu vas où ? — June m'a demandé de récupérer du lait !** *Deux répliques, et on repart.*`,
    `🔴 **Et c'est le seul geste qu'Andrew relève de tout le livre.** *Décision de l'autrice, 22 août 2026 : il s'en étonne — personne ne fait ça ici pour appeler quelqu'un.* **Il demande, Eliott ne sait pas répondre, et on passe.** ⛔ *Il n'en fait rien : pas de note, pas de retour, pas une pensée plus loin.*`,
    `✅ **Pourquoi ce geste-là et pas un autre : c'est le seul des trois qui ne prouve rien.** *Un sifflement ne se vérifie pas, ne se recoupe pas, ne mène nulle part — quelqu'un d'ici pourrait l'apprendre demain.* 🔴 **Et ça achète une chose précieuse : le lecteur voit qu'Andrew est capable de tiquer.** *Alors quand il ne tique pas sur la phrase de l'épicerie, ce n'est plus le narrateur qui triche — c'est lui qui n'a rien vu.* **Son silence sur le reste devient crédible parce qu'il a parlé une fois.**`,
    `⚠️ **L'homme qui remarque ce qui ne compte pas et manque ce qui compte.** *C'est sa faille écrite en une scène de dix lignes, et personne ne la nomme.*`,
    `✅ **Et ça évite un Eliott d'un seul bloc.** *Il est fermé tout le chapitre, sauf cinq secondes : il hèle quelqu'un, il se déride, il se referme.* ⛔ **Personne ne commente le sifflement** — c'est un geste utilitaire, il glisse pour ça.`,
    `⚠️ **La maisonnée de June entre par la fenêtre, sans exposition.** *Un berceur peut avoir plusieurs arrivants à charge — l'épilogue le dit déjà : parfois trois pour un, parfois plus.* ⛔ **Aucun mot de parenté, aucune fratrie :** *ils vivent au même endroit, c'est tout ce qu'on en sait.*`,
    `⛔ **Le chapitre ne se ferme pas chez Andrew.** *Le lecteur ne doit jamais voir où il habite : la scène 17 b en dépend.*`
  ],
  phrases: [{ t: `Un porteur de voiles de cet âge… je n'en avais jamais vu.`, n: `Exemple donné par l'autrice, à garder tel quel.` },
            { t: `Mais si, il y avait un magasin de chaussures ici, pas une épicerie.`,
              n: `✅ **Validée le 16 août 2026, et c'est elle qui reviendra.** Dite dehors, en marchant, devant l'épicerie, au milieu des autres. *Rien ne la distingue : c'est une fabulation de plus, et elle est fausse comme les autres.*

**Le sens des deux commerces, à tenir partout :** le **magasin de chaussures est de l'autre monde** — c'est ce dont Eliott se souvient ; **l'épicerie est d'ici**, c'est ce qu'il a sous les yeux et qu'il refuse.

**Elle ne donne aucun indice, elle donne une destination.** À la scène 17 c, Andrew s'en souviendra et entrera dans cette épicerie — non pas parce qu'il cherche quelque chose, mais parce qu'un gamin en avait parlé et qu'il n'a plus que ça. *C'est un geste de deuil, pas d'enquête.*

**Et c'est là que le livre se retourne :** ce que le garçon racontait lui a valu de n'être cru par personne, et ça l'a blessé. **Ce sont ces mêmes mots, faux, moqués, qui amèneront Andrew au bon endroit.** *Rien n'est vérifié pour autant : l'épicerie est bien une épicerie. Il avait tort, et il sauve tout.*` }],
  ouvert: [`💡 **L'ellipse peut porter autre chose qu'un compte de visites.** *Piste de l'autrice, 22 août 2026 : une remarque en passant sur le moment où Eliott a accepté de le tutoyer.* **Deux lignes d'ellipse qui disent un mois de familiarité, sans raconter une seule des visites.**`,
           `⚠️ **Ce que le lecteur entend de la conversation avec June.** *Tout, ou seulement la fin ? Andrew est sur le pas de la porte, et ce genre de conversation commence toujours avant qu'on l'écoute.*`,
           `✅ **Ils ont un nom et ils restent : Paul et Julie.** *Décision de l'autrice, 22 août 2026 — c'est Julie qu'il siffle.* **Ils reparaissent une fois, quand Joël et Liam viennent chez June, et plus jamais après** — *sinon l'enquête aurait un trou : on n'interroge pas une maison sans interroger ceux qui y vivent.* ⛔ **Ultra-secondaires, et ils le restent.** ⚠️ *Leurs âges sont à fixer.*`,
           `**Où le lecteur apprend ce qu'est un porteur de voiles s'il ne l'apprend pas d'elle.** *Une seconde occurrence ailleurs ferait du mot une notion, et la gêne disparaîtrait avec.*`],
  src: `04-plan/le-parcours-de-l-enquete.md §2 — 03-personnages/june.md §2 bis — décisions du 22 août 2026`
},

{
  id: `capsule`, no: `Chapitre premier`, ecrit: true, col: 1, row: `andrew`, acte: `Ouverture`,
  titre: `Une journée à la ruche`,
  statut: `acquis`,
  resume: `Ce n'est pas une scène, c'est une journée de travail. Combinaisons, raclette, seaux, odeur. Andrew n'y touche pas : ce n'est plus son tour. Il regarde un plus récent se faire bizuter, et il ne trouve rien à en dire. Puis la journée continue, parce que c'est une journée.`,
  produit: `⛔ **À ce stade du livre, on ne se dit pas « bien fait pour sa gueule » — on trouve juste ça révulsant.** *Une description crade et nauséabonde, et rien d'autre : le lecteur ne sait pas qu'il y avait quelqu'un dedans, et personne ne le lui dit.*

**« Bien fait pour sa gueule » arrive six cents pages plus loin**, à l'instant où Andrew connecte et où le lecteur connecte avec lui. *C'est là seulement qu'il a quelque chose à juger — et ce qu'il aura à juger, c'est sa propre satisfaction.*`,
  clef: `🔴 **C'est ici qu'on forge la formule, et elle ne servira qu'une seconde fois.** *Une phrase exacte, à vocabulaire précis et successif, qui décrit l'odeur de la capsule pourrie.* **Modèle donné par l'autrice, image trouvée le 19 août 2026 :** *« une odeur, insipide, et prenante au nez, comme le fond d'un vase de fleurs qu'on aurait oublié tout un été. »* — **une odeur que tout le monde a déjà eue dans le nez, qui n'a rien à elle, et qu'on ne peut pas rattacher à un corps.**

**Elle n'apparaît nulle part ailleurs dans le livre que dans ce chapitre et à la seconde cérémonie.** Pas une variation, pas un synonyme : *les mêmes mots, dans le même ordre.* **C'est le seul fil qui relie deux chapitres séparés de six cents pages** — si l'un des deux bouge, l'autre bouge en même temps.`,
  clefFin: `⛔ **Et l'ancienne formule du prologue est supprimée.** *La pierre mouillée et le fond légèrement sucré ne sont plus nulle part* — c'était mon invention et elle ne servait à rien. **Le prologue n'a donc plus à porter d'odeur** : il est libre de ce côté-là.`,
  garde_forme: `**Une journée, pas une scène.** Une carte « Andrew regarde un nettoyage » n'a aucune raison d'exister au milieu de la disparition d'Eliott ; une journée de travail, si. Et le nettoyage doit être un incident d'exploitation, pas une épreuve morale — alors la forme dit déjà ce que le contenu dit.

Le déroulé : ① l'arrivée, le tableau des travées, le tour de rôle ; ② une éclaircie ordinaire, réussie, avec l'odeur propre ; ③ le creux du milieu de journée, les conversations ; ④ la travée qui n'a pas éclairci ; ⑤ le registre, en fin de journée — la première fois que le lecteur voit ce que c'est ; ⑥ il sort.`,
  garde_bis: `✅ **Le chapitre a changé de place : il suit le prologue.** *Décision de l'autrice, 19 août 2026.* Il n'est donc plus pris en sandwich entre la douceur et le vide — **il est collé à la cérémonie propre**, et c'est ce qui fait le plus mal : *le lecteur vient de voir un rite tenu au millimètre, et il tombe sur ce que le même lieu produit quand ça rate.*\n\n✅ **Et la frise suit, le 19 août 2026 :** *la case passe en colonne 1, juste après le prologue, et l'acte d'ouverture compte désormais deux chapitres.* **Les deux visites chez June glissent d'un cran.**`,
  monde: `Le tour de rôle, le bizutage, l'ancienneté qui se lit à l'envers sur les visages : la sale besogne va aux derniers arrivés, c'est-à-dire à ceux qui ont l'air les plus vieux.`,
  qui: [`andrew`],
  gardes: [
    `**Reprendre les mots du prologue, pas d'autres.** C'est la répétition littérale qui fera le raccord, pas une comparaison. Et personne ne dit que c'est la même odeur.`,
    `Le nettoyage est un incident d'exploitation. Personne ne s'attendrit, personne ne s'interroge.`,
    `⛔ **La capsule pourrie n'a rien à voir avec Eliott** : un autre jour, une autre travée. *Et ce n'est plus un souvenir depuis que le chapitre a changé de place — c'est une matinée ordinaire, un mois avant qu'il ne rencontre le garçon.*`,
    `Les capsules sans éclaircie se multiplient depuis quelques années et personne ne sait pourquoi. Deux occurrences dans le livre, pas davantage, et jamais un personnage qui pointe la courbe.`,
    `⛔ **Le chapitre ne montre pas le logement d'Andrew.** Il commence quand il arrive, il s'arrête quand il sort. La scène 17 b en dépend : c'est un chapitre chez Joël que le lecteur doit prendre pour une fin de journée d'Andrew, et il ne le prendra que s'il n'a jamais vu où Andrew habite.`,
    `**Ce n'est pas une visite guidée.** On suit quelqu'un qui travaille, pas quelqu'un qui explique.`,
    `**Court.** Une journée type, tôt dans un livre, est le genre de chapitre qui enlise. **Deux mille mots**, et il tient parce qu'il finit sur une odeur.`,
    `✅ **Le chapitre s'arrête avant la cérémonie.** *Le lecteur sait déjà ce qui s'y passe — il vient de la voir en entier.* La formule est une meilleure dernière ligne qu'un rite rejoué.`,
    `✅ **L'inversion des âges se pose chez les préparateurs, et le bizutage la confirme.** *Refusée dans la description d'Andrew — trop frontale — elle tombe sur un homme de soixante-douze ans qui s'émerveille devant sa première capsule.* **« Personne ne trouva ça remarquable. Dans ce service, les plus anciens du métier étaient aussi ceux qui avaient l'air les plus jeunes. Ça se comprenait très bien. »** ⛔ *Et le pourquoi ne vient jamais.*`
  ],
  ouvert: [`⚠️ Sur quoi le chapitre se ferme. Une piste : il se dit qu'il passera voir Eliott, et il remet à demain — la journée ordinaire devient alors l'alibi qui le poursuivra tout le livre. C'est peut-être trop appuyé : une simple sortie, sans rien dire, suffirait.`,
           `✅ **Pas le prologue.** Le prologue occupe déjà ce champ lexical avec la version propre — et la version propre doit venir en premier, sinon la version gâtée n'a rien à corrompre.`],
    src: `L-ECLAIRCIE-dossier-complet.md §8 — décision du 16 août 2026`
},
{
  id: `s3`, no: `Scène 3`, col: 4, row: `andrew`, acte: `La disparition`,
  titre: `Troisième visite — la place est vide`,
  statut: `acquis`, pivot: true,
  resume: `Andrew vient croyant trouver le garçon. June est déjà allée voir la police, et elle lui apprend qu'il n'est pas rentré de son travail.`,
  produit: `Il ne reçoit pas la nouvelle : il tombe dessus, sur un pas de porte, en venant pour autre chose. Il n'a rien à déclencher et rien à conseiller — tout a déjà été fait, dans l'ordre, par quelqu'un dont le rôle s'arrête là.`,
  clef: `🔴 **Et c'est ici que le nom d'Isaac entre dans le livre — par la bouche de June.** Elle dit avoir parlé à un certain Isaac ; Andrew répond que c'est un bon ami, et qu'il va aller lui parler. *Le lecteur attend donc de le rencontrer au chapitre suivant. Il rencontrera quelqu'un d'autre.*`,
  garde_forme: `**Ouverture proposée : « La porte s'ouvrit avant qu'il ait frappé. »** *Elle guettait.* **Trois mots plus tard le lecteur a compris qu'il se passe quelque chose, et Andrew, lui, n'a encore rien compris.** *C'est la troisième fois qu'une porte s'ouvre dans ces chapitres, et c'est la première où elle s'ouvre trop tôt.*

**Fin : le nom.** *C'est le hook le plus important des quatre — il fabrique l'attente que le chapitre suivant va trahir pendant six cents pages.*`,
  monde: `Rien de neuf, et c'est voulu. La scène est un vide.`,
  qui: [`andrew`,`june`],
  gardes: [
    `June ne vient trouver personne et ne signale rien à Andrew. Elle n'est pas un relais d'information : elle est un lieu où la nouvelle attend.`,
    `Si une seule de ses répliques a l'air d'appeler Andrew à faire quelque chose, la séquence bascule.`,
    `⛔ **Le chapitre ne se ferme pas chez Andrew.** *Le lecteur ne doit jamais voir où il habite : la scène 17 b en dépend.*`
  ],
  ouvert: [`✅ **La contradiction du mois est levée.** *Décision du 22 août 2026 : la première visite montrée n'est pas la première, et l'ellipse de la tournée porte le reste.* **Les visites tiennent donc sur le mois sans qu'aucune phrase ait à le dire.**`],
  src: `04-plan/le-parcours-de-l-enquete.md §2 — décisions du 22 août 2026`
},

{
  id: `s4`, no: `Scène 4`, col: 5, row: `joel`, acte: `La disparition`,
  face: `g-poste`,
  titre: `Première visite au commissariat`,
  statut: `acquis`, pivot: true,
  resume: `Il pousse la porte d'un poste de police et parle à quelqu'un de l'affaire. On lui donne des faits, et rien d'autre : des trajets, des horaires, un déroulé de journée. **Jamais un état d'esprit.** *C'est le premier chapitre de la vie d'avant, et le lecteur ne le sait pas.*`,
  produit: `🔴 **Décision de l'autrice, 16 août 2026 : c'est là que le récit se dédouble, et la scène est de Joël.** *Le lecteur croit assister à la rencontre d'Andrew et d'Isaac, dont on vient de lui parler.* **Il assiste en réalité à une conversation entre Joël et son collègue, et il ne le saura qu'à la dernière page.**`,
  clef: `**Et c'est ici que le lecteur se fabrique Isaac.** La silhouette, la voix, la façon de tenir un bureau, l'humeur : tout ce qu'il croira savoir d'Isaac vient de cet homme-là. *Le suspect était déjà une couture ; l'allié en est une aussi.*`,
  lecture: `Il vient d'entendre June parler d'un certain Isaac et Andrew répondre que c'est un bon ami. **Il ouvre le chapitre suivant en s'attendant à le rencontrer, et il rencontre quelqu'un d'autre.**`,
  monde: `Rien, et c'est la condition. Un poste de police se ressemble partout — c'est l'infrastructure même du dispositif.`,
  qui: [`joel`,`liam`],
  gardes: [
    `**Aucun nom, ni celui de l'homme, ni celui de Joël.** Le lecteur apportera « Isaac » tout seul, et personne dans le texte ne le prononcera.`,
    `Aucun marqueur de monde : pas de travée, pas de registre, pas d'arrivant, pas un mot de parenté.`,
    `Les victimes ne sont ni comptées, ni sexuées, ni décrites.`,
    `**Rien de ce qui décrit l'homme ne doit contredire Isaac plus tard.** Ni l'âge, ni l'apparence, ni un détail de bureau. *La contrainte est lourde, et elle vaut pour tous les chapitres où il reparaîtra.*`,
    `🔴 **On ne discute jamais de l'enlèvement.** Ni ici ni ailleurs : pas de rappel des faits, pas de résumé de l'affaire, pas une phrase qui dise ce qui est arrivé et à qui. **On parle d'une affaire en cours, comme le font des gens qui la connaissent déjà.** *C'est ce qui rend le chapitre superposable à celui d'Andrew, et c'est la règle la plus stricte de toute la voie de Joël.*`,
    `L'affaire a un nom — **l'affaire Sorel** — et c'est tout ce qu'on en saura. Un nom de famille, catégorie de mot qu'Andrew ne pourra même pas identifier comme un nom. *Il peut revenir cent fois sans jamais rien apprendre.*`
  ],
  pourquoi: [
    `**Le procès-verbal ne retient pas les états.** C'est ce qui manque au dossier, et c'est ce qui pousse à retourner chez le témoin — le beat suivant tient par ce vide, dans les deux mondes.`,
    `**Et le cri final change de nature.** Si le lecteur a passé le livre à croire que ce collègue est Isaac, alors c'est Isaac qu'il entend crier *« Joël, attends ! »*. *Le dernier chapitre s'écroule sur lui d'un cran de plus.*`
  ],
  ouvert: [`✅ **Il n'y a plus de carte « L'affaire Sorel ».** *Décision de l'autrice, 16 août 2026 : cet encart n'existait pas vraiment, il est regroupé ici.* **Aucun chapitre n'établit l'affaire** — elle est déjà là quand on entre dedans, comme dans la vie.`,
           `⚠️ **La fiche de Liam est périmée.** Elle le donne pour « pas un personnage, une voix derrière lui ». **Il porte désormais la présentation de l'allié**, donc il existe, il a une manière, une façon de parler. *À réécrire — c'est la conséquence la plus lourde de cette décision.*`,
           `Combien de fois il reparaît côté Joël avant la poursuite.`],
  src: `04-plan/le-parcours-de-l-enquete.md §2 — décision du 16 août 2026`
},
{
  id: `s5`, no: `Scène 5`, col: 6, row: `andrew`, acte: `La disparition`,
  face: `g-temoin`,
  titre: `Retour chez June, avec Isaac`,
  statut: `acquis`,
  resume: `Elle raconte comment ça se passe et l'état d'esprit du garçon : il peut être adorable puis devenir d'un coup hyper agressif. Il a une peur bleue de l'eau et a refusé les premiers cours de natation. Et la veille, il est rentré avec les genoux en sang et la lèvre fendue.`,
  produit: `C'est la scène qui produit la direction du lendemain, et elle la produit par une inquiétude, pas par un indice. Il a dit être tombé ; elle est certaine que quelque chose n'allait pas au travail.`,
  monde: `Les cours de natation donnés aux arrivants — un détail d'intégration ordinaire qui devient, pour le lecteur de la dernière page, une chose difficile à relire.`,
  qui: [`andrew`,`isaac`,`june`],
  gardes: [
    `Sa terreur de l'eau ne s'explique pas, ne se commente pas, et ne revient pas comme motif.`,
    `June restitue sans rien ajouter. Elle ne conclut jamais rien.`,
    `🔴 **Paul et Julie sont présents tous les deux.** *Décision de l'autrice, 22 août 2026 : on n'interroge pas une maison sans interroger ceux qui y vivent.* ⛔ **Ils ne savent rien** — *ils vivaient avec lui, ils ne l'ont pas suivi au travail, et ce qu'ils disent ne fait avancer personne.* **C'est leur dernière apparition du livre.**`,
    `🔴 **June seule parle de son comportement et du cours de natation.** *Décision de l'autrice, 22 août 2026 : la parole utile est à elle, et à personne d'autre dans cette maison.* ⛔ **Et leur non-savoir doit être actif :** *on leur demande forcément s'il leur a parlé de quelque chose — ils répondent, et leur réponse ne sert à rien.* **Un témoin présent qui n'apporte rien doit avoir l'air de n'avoir rien, pas d'être escamoté.**`,
    `🔴 **La colère est unique, et c'est ici qu'on l'apprend.** *Décision de l'autrice, 22 août 2026 : une seule fois, jamais comprise, jamais expliquée.* ⛔ **Aucune colère au pluriel dans les chapitres d'avant** — *June s'y inquiète qu'il n'aille pas bien, refermé, en difficulté, et rien de plus.* **Le motif est le reliquat corporel de la noyade : le banaliser tôt le dépense.**`
  ],
  phrases: [{ t: `il s'est mis dans une colère noire, ça ne lui ressemblait pas`, n: `Formulation de l'autrice, à garder.` }],
  double: `Beat doublable : deux fois la même pièce, deux fois la même question, et une seule fois où il en tire quelque chose.`,
  src: `04-plan/le-parcours-de-l-enquete.md §2 — §5`
},

/* ---------- LE MONDE COMME TERRAIN ---------- */
{
  id: `s6`, no: `Scène 6`, col: 7, row: `andrew`, acte: `Le monde comme terrain`,
  face: `g-fac`,
  titre: `Sur son lieu de travail`,
  statut: `acquis`,
  resume: `Le portage — une tournée, et c'est elle qui fait passer Eliott dans les rues d'ici. **Henri**, le responsable, donne sa version : la veille, Eliott était impliqué dans une bagarre avec un homme de vingt-deux ans. Il l'a congédié sur-le-champ, après plusieurs sommations, quand l'homme est devenu insultant et haineux.`,
  produit: `L'économie de ce monde : qui travaille, à quelles conditions, et ce qu'on tolère pour tenir un effectif. Le responsable semble blasé, comme si ce n'était pas la première fois — des marginaux, il y en a partout, il faut vivre avec en limitant les débordements.`,
  monde: `Le travail des jeunes arrivants, l'exclusion temporaire, le seuil de tolérance d'une société qui a besoin de ses effectifs.`,
  qui: [`marginal`,`andrew`,`isaac`],
  gardes: [
    `🔴 **Le responsable a un nom : Henri.** *Décision de l'autrice, 22 août 2026.*`,
    `🔴 **Henri tient une entreprise de livraison, pas un service pour jeunes arrivants.** *Précision de l'autrice, 23 août 2026.* **Il emploie de tout, parce qu'il faut de la condition physique pour livrer certaines choses** — *le portage n'est que le petit nom de ce qu'on confie aux plus bas : les menus colis, les lettres, ce qui se porte à pied.* ⛔ **Sans ça, on ne croiserait pas de marginaux chez lui, et la scène suivante n'aurait pas lieu d'être.**`,
    `🔴 **Et c'est là que le grief prend un visage.** *L'homme de vingt-deux ans est un arrivant venu avec un grand nombre : il trime depuis des années dans cette maison.* **Il a vu entrer un garçon de dix ans qui n'en a plus que six devant lui et à qui l'on donne tout.** ⛔ *Personne ne met les deux côte à côte dans le texte — c'est le lecteur qui les rapproche, et il le fera d'autant mieux qu'il vient de passer un chapitre entier avec le garçon.*`,
    `🔴 **C'est ici que le lecteur apprend combien de temps il reste à un jeune arrivant — décision de l'autrice, 23 août 2026.** *Première des trois marches, et la seule qui soit froide.*

**Henri a une raison de le dire, et c'est la seule bonne :** *il tient un effectif et il explique pourquoi il emploie ces gens-là.* **Un jeune arrivant ne fera jamais d'études : il n'a pas le temps devant lui.** ⛔ *Il parle de main-d'œuvre, jamais d'Eliott — c'est le lecteur qui fait la soustraction, et il la fait après coup.*

✅ **Et la scène suivante en dépend :** *le grief des marginaux — l'accès sans mérite — ne se comprend que si on sait ce que les jeunes arrivants ont et n'ont pas.* **Sans cette marche-là, la scène 7 ne tient pas debout.**`,
    `⛔ **Ce qui ne se dit pas ici : ce qu'est le jardin, et ce qu'il y a au bout.** *Deux autres marches s'en chargent — la scène 11, où Andrew y va et voit le lieu, et la scène 14 c, où une berceuse tient un tout-petit sur le point de disparaître.* **Trois marches, chacune plus profonde, et aucune n'explique.**`,
    `Le responsable ne formule jamais la doctrine. Il est blasé, il a un effectif à tenir, c'est tout.`,
    `Sa position sur les jeunes arrivants doit rester neutre — ni tendresse, ni mépris.`
  ],
  phrases: [{ t: `On les fait travailler pour que le reste du monde le supporte.`, n: `Retenue par l'autrice comme réplique d'Henri, quand on lui demande pourquoi la sortie du marginal ne lui fait pas plus d'effet que ça.` }],
  ouvert: [`Le prénom de l'homme de vingt-deux ans. Un nom d'éclaircie. Il traverse huit scènes sans être nommé.`,
           `Ce que le portage porte exactement, à qui, et sur quel périmètre.`],
  src: `04-plan/le-parcours-de-l-enquete.md §2`
},
{
  id: `s7`, no: `Scène 7`, col: 8, row: `andrew`, acte: `Le monde comme terrain`,
  titre: `Les autres travailleurs`,
  statut: `acquis`,
  resume: `Isaac interroge des amis du marginal absent. C'est là que leur point de vue tombe : l'accès sans mérite, les marches qu'ils ont faites et que d'autres n'ont pas faites, l'argument de la santé qui est vrai et vérifiable.`,
  produit: `Le grief se dit dans leur bouche et jamais dans celle du narrateur. Les deux camps ont raison, le livre ne tranche pas, personne ne les corrige.`,
  monde: `La jalousie ordinaire, entière, dans la bouche de ceux qui la portent. Pas un mouvement, pas un nom, pas un porte-parole : des gens à qui on a beaucoup demandé et qui font une remarque.`,
  qui: [`isaac`,`andrew`],
  gardes: [
    `Ne jamais leur donner tort par un chiffre.`,
    `Ne jamais mettre les deux arguments dans la même bouche.`,
    `Ne jamais laisser Andrew formuler le nœud budgétaire. Il écoute, il s'en va, il pense à autre chose.`,
    `Personne ne corrigera jamais leur sophisme — le corriger reviendrait à dire que naître vieux coûte cher, et cela, personne ne le dira.`
  ],
  phrases: [{ t: `les petits princes pourris du jardin`, n: `L'insulte du milieu. « Petits princes » pour l'accès sans mérite, « pourris » au sens de gâtés, « du jardin » pour le lieu où eux n'iront que très tard et pour très peu de temps.` },
            { t: `libérer plus tôt`, n: `La formule du courant respectable. Il ne dit jamais « tuons-les » : il le dit avec des chiffres, dans des salles, devant des gens qui hochent la tête.` }],
  ouvert: [`Où et combien de fois l'insulte se dit. Une fois en passant puis une fois qui glace, ou une seule occurrence ?`],
  src: `02-univers/la-jalousie.md — 04-plan/le-parcours-de-l-enquete.md §2`
},

/* ---------- LE REGISTRE ---------- */
{
  id: `s8`, no: `Scène 8`, col: 9, row: `andrew`, acte: `Le registre`,
  face: `g-archives`,
  titre: `Retour à la ruche — le registre`,
  statut: `acquis`, pivot: true,
  resume: `Andrew enquête sur plusieurs lignes. D'abord celle de l'homme : un arrivant de quatre-vingt-onze ans. Puis la cérémonie d'éclaircie d'Eliott. Ce que la journée porte, à son heure, ce sont deux arrivées : Eliott, dix ans, et un arrivant de quarante ans. Il ne s'y arrête pas une seconde.`,
  produit: `C'est le cas témoin du livre. Le lecteur apprend ici que deux arrivées le même jour signifient une seule mort — sur un cas parfaitement innocent, dans une scène occupée à tout autre chose. Une leçon qu'on reçoit sans savoir qu'on la reçoit, parce qu'elle ne sert à rien sur le moment.`,
  clef: `Il s'en servira bien plus tard, sur la ligne de la paire : même structure, même journée partagée — plus une capsule qui n'éclaircit pas. Il n'aura besoin d'aucune explication.`,
  monde: `Ce qu'un veilleur peut lire, et ce que le registre note : la travée, la date, l'âge relevé, le nom, le numéro. Et le rapport de capsule : nickel, belle forme, belle couleur, survenue assez vite, pas de développement — une capsule non préméditée.`,
  qui: [`andrew`],
  gardes: [
    `Andrew ne fait jamais le lien. Il entend, à la fin, une histoire d'eau et de courant, et il ne va pas vérifier qui d'autre est arrivé ce jour-là. Personne ne le fait à sa place.`,
    `Aucune phrase du texte ne rapproche jamais les deux arrivées. Pas un personnage qui compte, pas un narrateur qui rappelle la cérémonie, pas une reprise du regard de la première page.`,
    `Il n'y a pas de capsule défaillante ce jour-là. Le bizutage est un souvenir d'un autre jour, ailleurs.`,
    `Le registre est infaillible et il le reste. S'il peut se tromper, le mouvement où Andrew lit sa propre ligne s'effondre.`
  ],
  lecture: `Rien n'a été caché, rien n'a été déplacé, tout était écrit en clair — et ça ne ressemblait à rien. C'est le lecteur qui se souvient de l'homme debout à côté du petit, à la première page.`,
  ouvert: [`Le motif d'Andrew pour aller au registre. Piste : il y va parce que c'est le seul terrain où il est le meilleur — c'est déjà son défaut à l'œuvre.`],
  src: `04-plan/le-parcours-de-l-enquete.md §2, §3.3`
},
{
  id: `s9`, no: `Scène 9`, col: 10, row: `andrew`, acte: `Le registre`,
  face: `g-liam`,
  titre: `Au téléphone, en parallèle`,
  statut: `acquis`,
  resume: `Isaac a fait des recherches sur l'homme. Andrew partage ses infos ; Isaac détaille sa vie. Plusieurs altercations, dont certaines ont dérapé. Et il a fait quelques jours « au silence » — la cellule temporaire — après avoir tenté, avec un groupe d'autres marginaux, d'empêcher l'entrée au jardin d'un groupe d'arrivants de six ans.`,
  produit: `Deux choses d'un coup, et aucune n'est expliquée : un régime pénal qui existe et qui a un nom, et un homme dont l'hostilité a déjà pris la forme d'un acte public.`,
  monde: `« Au silence ». Le mot ne s'explique pas, il se comprend au premier emploi par le contexte, et il dit quelque chose du monde sans que personne ait à le commenter.`,
  qui: [`isaac`,`andrew`,`marginal`],
  gardes: [`Le mot « au silence » n'est jamais défini. Il s'emploie.`],
  ouvert: [`« Au silence » est à porter au lexique — aucun fichier de lexique n'existe encore dans le dossier.`],
  src: `04-plan/le-parcours-de-l-enquete.md §2, §3.6`
},
{
  id: `s10`, no: `Scène 10`, col: 11, row: `andrew`, acte: `Le registre`,
  titre: `Vingt-six arrivants simultanés`,
  statut: `acquis`, pivot: true,
  resume: `Andrew, le registre encore sous le nez, évalue le groupe : vingt-trois arrivants de six ans, un de quarante-quatre, un de trente-neuf, un dernier de soixante et un. Vingt-six arrivants simultanés. Une cérémonie assez grandiose.`,
  produit: `C'est le sismographe, et c'est peut-être le plus fort effet gratuit du livre. Vingt-trois petits chiffres dans le même paquet ne se lisent que d'une façon : quelque chose, de l'autre côté, a tué vingt-trois très jeunes d'un coup.`,
  clef: `Personne ne peut le savoir ici. Le veilleur de l'époque y a vu une matinée chargée, l'administration un problème d'enregistrement, le service un manque de berceurs. Andrew y voit un fait exceptionnel qu'il note et qu'il range. Aucun de ces regards n'est faux, et aucun ne s'approche de ce qui s'est passé.`,
  monde: `Ce qu'est une ruche sans que personne le sache : un sismographe. Trente capsules qui mûrissent le même jour signalent un tremblement de terre, une guerre, un naufrage.`,
  qui: [`andrew`],
  gardes: [
    `✅ **C'était une cérémonie compliquée et atypique, et ça se voit.** *Précision de l'autrice, 17 août 2026 :* **peu de monde dans le public, et pas assez de berceuses** pour les arrivants qu'il fallait porter. *Rien ne s'est mal passé ; tout a été difficile.*`,
    `✅ **Et leur entrée au jardin l'a été aussi.** *Un énorme groupe arrivé en même temps, en plus de ceux qui étaient prévus.* **Cette promotion-là a mis le système en difficulté aux deux bouts — à l'arrivée, puis huit ans plus tard à la grille.**`,
    `La seule chose à faire est de ne rien faire. Pas de personnage qui s'étonne trop longtemps, pas de phrase qui pèse, pas de retour dessus plus tard.`,
    `Il ne faut surtout pas l'expliquer. L'expliquer le détruirait, et rien ne le remplacerait.`
  ],
  lecture: `Le lecteur fait le calcul seul, dans une scène qui parle d'autre chose, au milieu d'une enquête sur un homme innocent.`,
  src: `04-plan/le-parcours-de-l-enquete.md §2, §3.2`
},
{
  id: `s11`, no: `Scène 11`, col: 12, row: `andrew`, acte: `Le registre`,
  face: `g-ancien`,
  titre: `Au jardin — le veilleur de l'époque`,
  statut: `acquis`,
  resume: `Andrew et Isaac s'y donnent rendez-vous. Le veilleur qui s'était chargé de la cérémonie est désormais au jardin, âgé de huit ans. Il décrit la cérémonie et les réactions du public. Il n'y avait pas assez de berceurs ce jour-là ; la cérémonie a même pris du retard, l'administration ayant dû les enregistrer un à un.`,
  produit: `Le fonctionnement du jardin, et l'attitude presque destructrice des marginaux dans un lieu d'innocence et de paix. Le marginal faisait partie du public : le transfert s'étant passé le jour même, il a enflammé ses camarades pour aller mettre le bazar à l'entrée du jardin.`,
  clef: `Un veilleur de l'époque désormais à huit ans se souvient d'une matinée sans se souvenir de sa carrière. C'est gratuit et c'est terrible, à condition de ne jamais le commenter.`,
  monde: `Le jardin : le dernier lieu de vie, huit ans et en dessous, dans les mêmes pièces. La mémoire qui s'allège en descendant. Le fait qu'on puisse aller poser une question à quelqu'un qui ne travaille plus.`,
  qui: [`andrew`,`isaac`],
  gardes: [
    `Ne jamais commenter la mémoire du veilleur de l'époque.`,
    `Le monde ne se livre jamais en description : quelqu'un répond à une question qu'on lui a posée. Il parle des berceurs parce qu'on l'interroge sur un retard.`,
    `Test : si l'on peut retirer la question sans perdre l'information, la scène est une description déguisée et elle est à réécrire.`
  ],
  ouvert: [`Le basculement direct au jardin des vingt-trois arrivants de six ans a été confirmé le 16 août 2026 : on est au jardin dès qu'on a huit ans ou moins, quel que soit le sens de la trajectoire. **La scène ne bouge pas.**`],
  src: `04-plan/le-parcours-de-l-enquete.md §2 — 02-univers/le-jardin.md`
},
{
  id: `ceremonie2`, no: `Entre 12 et 13`, col: 15, row: `andrew`, acte: `La fausse piste s'éteint`,
  titre: `Sa cérémonie, vue de l'intérieur`,
  statut: `acquis`, pivot: true,
  resume: `Sa propre arrivée, dix ans plus tôt. **Il se réveille comme d'un sommeil profond**, aveuglé par la lumière, les voix lui parviennent étouffées. Une paire dont la salle s'émerveille, un veilleur qui note tout. Puis on s'adresse à lui : *« Quel sera ton prénom ? Comment veux-tu qu'on t'appelle pour te désigner ? »*`,
  produit: `Le livre contient deux descriptions de cérémonie, toutes deux d'Andrew : celle où il accueille — le prologue, le professionnel au travail — et celle où il est accueilli, par quelqu'un qui n'a aucun mot pour ce qu'il voit. **Le même rite depuis les deux bouts, et c'est le dispositif d'ensemble à l'échelle d'un chapitre.**`,
  clef: `**Elle s'intercale entre les deux scènes de Joël, et c'est quelque chose dans le discours de l'homme qui donne prétexte à se souvenir.** Décision de l'autrice, 16 août 2026. *Le lecteur croit lire une seule pensée continue : un homme sort d'un pas de porte et une chose qu'on vient de lui dire lui rappelle son propre premier jour. Il y a deux hommes, deux mondes, et il ne le saura pas.*`,
  monde: `La cérémonie vue par quelqu'un qui ne sait rien. Et, sans que personne le sache, la journée des quatre capsules : la paire, lui, et une quatrième qui n'éclaircit pas.`,
  qui: [`andrew`,`chrissy`],
  gardes: [
    `✅ **Il n'a pas eu une petite cérémonie : il a eu celle de la paire.** *Précision de l'autrice, 17 août 2026.* **Les capsules des jumelles avaient mis longtemps à mûrir — le temps exact de leur agonie dans l'autre monde — et leur cérémonie était prévue de longue date**, donc annoncée, donc suivie. *Moins d'une heure avant, la capsule d'Andrew surgit ; le veilleur de l'époque la note et décide de grouper.* **Un poste de plus, et c'est tout** — monter une seconde cérémonie aurait bloqué deux salles pour rien.`,
    `⛔ **Et il n'y a rien de cruel là-dedans, contrairement à ce qu'on pourrait écrire.** *Le public ne vient pas pour quelqu'un en particulier : il vient pour célébrer une arrivée, et aucun lien ne se fait entre lui et les arrivants.* **Personne ne pense « zut, il y en a un troisième »** — ceux qui sont là constatent qu'il y en a un de plus, et c'est tout. *La seule chose vraie, et elle est banale : sans les jumelles, il y aurait eu moins de monde. Une question d'avoir prévenu plus tôt ou pas.*`,
    `Il ne comprend rien et ne doit rien comprendre.`,
    `🔴 **C'est ici, et seulement ici, que la paire est posée.** La salle s'émerveille : « elles sont pareilles », « première fois que j'en vois », « j'en ai déjà vu il y a quelques années ». *Rien de plus — mais assez pour que le lecteur emporte deux visages identiques dont il ne fera rien.* **C'est à cette scène qu'il se raccrochera devant les corps, six cents pages plus loin.**`,
    `**La quatrième capsule doit être là et ne rien peser.** Un veilleur s'occupe des arrivants pendant qu'un autre racle, plus loin, pour que l'infamie de la chose n'entrave pas la cérémonie. *Un chifoumi silencieux s'est joué entre eux ce matin-là, et personne ne le racontera jamais.* Ce qu'Andrew en attrape est une odeur, mentionnée par quelqu'un au loin, et rien de plus.`,
    `⚠️ **Le récit doit montrer qu'il n'entend pas.** Une bouche qui bouge, des mots qui ne se forment pas, une phrase d'accueil dont il ne retient que les deux premiers mots. **C'est la condition pour que la seconde version, au chapitre F, soit un blanc qu'on comble et non une information qu'on avait gardée sous le coude.**`,
    `De la phrase d'ouverture, il n'attrape que *« Bienvenue à tous »*. La suite se perd, et le lecteur voit qu'elle se perd.`,
    `Aucun personnage ne rapproche jamais les trois arrivées. Le lecteur seul aura vu la pièce.`
  ],
  pourquoi: [
    `**Le souvenir est convoqué, pas déposé.** Ailleurs, ce chapitre arriverait parce que l'autrice en a besoin là. Ici il arrive parce que quelque chose l'a appelé — *c'est toute la différence entre un plan et un livre.*`,
    `**La transition devient elle-même une pièce du dispositif.** Le lecteur sort d'un chapitre de la vie d'avant et entre dans un souvenir du monde d'ici, sans voir la couture, parce que c'est lui qui la fait. Il croit suivre une seule pensée continue.`,
    `**Elle sépare deux chapitres de Joël.** Sans elle, les scènes 12 et 13 s'enchaînent et le lecteur passe trois chapitres d'affilée dans la vie d'avant — c'est long, et c'est le moment le plus fragile du livre.`,
    `**Elle tombe juste avant le travail sur le registre.** La paire, les trois capsules et la quatrième qui n'éclaircit pas sont fraîches quand Andrew y retourne à la scène 14, et elles le seront encore à la toute fin.`,
    `**Et ça change la nature du temps 5.** Quand il lit sa ligne, le lecteur ne reçoit pas une explication : il se souvient d'une pièce où il était. *Un souvenir frappe plus fort qu'une révélation.*`
  ],
  contre: `**Ce que ce placement coûte, et il faut le savoir :** la paire n'apparaît plus tôt dans le livre, mais au milieu — et dans une scène chargée, pas en décor. *Le risque est que le lecteur rapproche trop vite les deux corps identiques du chapitre B de la paire qu'il vient de voir naître.* **Ce qui l'en empêche est l'interdit n° 1 :** il ignore que les arrivées répondent à des morts, donc il n'a pas la marche à monter. **Mais la marche existe, et elle est plus courte qu'avant.**`,
  ouvert: [`✅ **Ce chapitre est repris une seconde fois, au chapitre F**, après la mort de Joël — plus bref, moins tourné vers lui, et cette fois il entend la phrase entière. *Les deux récits doivent être vérifiables l'un contre l'autre : rien dans le second qui ne pouvait être manqué dans le premier.*`,
           `⚠️ **Ce que l'homme dit qui donne prétexte au souvenir.** Il est du monde d'avant, donc Andrew ne l'entend pas : **le déclenchement ne vaut que pour le lecteur.** Pistes d'équivoque, à trancher — *« ça fait dix ans que ça dure »* (le chiffre exact de son arrivée) ; *« on est arrivés en même temps, lui et moi »* (embauchés la même semaine là-bas, trois capsules le même matin ici) ; *« vous croyez que je me souviens de ce que j'ai dit il y a dix ans ? »*`,
           `⚠️ **Contrainte de loyauté, et elle est absolue.** Le texte ne doit **jamais** placer Andrew chez l'homme. Pas de « en repartant de chez lui », pas de voiture qu'on referme, pas de porte dans le dos. *On l'ouvre ailleurs — à la ruche, dans un couloir, devant un lavabo — et le lecteur fait le raccord tout seul. Rien n'est caché : quelque chose n'est simplement pas dit.*`,
           `✅ **La paire est posée ici, et nulle part ailleurs.** *La carte « la paire, en passant » est supprimée : elle ne manquait pas, elle refaisait ce que cette scène fait déjà.* **Et le chapitre F ne la reprendra pas** — il ne donne que ce qu'Andrew avait omis.`,
           `✅ **La réplique du ratio ne tombe pas ici.** *Elle part à la découverte du jardin, dans la bouche du pédiatre — décision de l'autrice, 16 août 2026.*`],
  src: `04-plan/deux-histoires-en-une.md §7 — 04-plan/le-meme-jour.md §1`
},
{
  id: `s12`, no: `Scène 12`, col: 14, row: `joel`, acte: `La fausse piste s'éteint`,
  face: `g-suspect`,
  titre: `Chez l'homme`,
  statut: `acquis`, pivot: true,
  resume: `Joël rend visite à un homme qui aurait harcelé les deux filles. Il est là, il ne veut pas leur parler, il les envoie promener — et il donne un alibi comme on jette une porte, sans rien démontrer, parce qu'il n'a pas à se justifier devant des gens qui n'ont rien contre lui.`,
  produit: `🔴 **Décision du 16 août 2026 : la scène est de Joël, et le lecteur croit écouter un marginal du monde d'Andrew.** *Le suspect que le lecteur s'est fabriqué depuis la scène 6 n'existe pas : il est cousu de deux hommes qui ne se sont jamais rencontrés et qui ne vivent pas dans le même monde.*`,
  clef: `**L'équivoque, et c'est le mot qui tient toute la scène : « des propos déplacés ».** Le responsable du monde d'Andrew, scène 6, parlait de propos haineux ; ici on dit déplacés, et le lecteur y lit un euphémisme pour la même chose. **C'étaient des propos sexistes tenus à deux filles de dix-huit ans.** Un seul mot, deux lectures, aucune des deux invraisemblable.`,
  lecture: `Il a entendu parler du marginal aux scènes 6, 7 et 9 sans jamais le voir. Il le voit ici. Il ne remarquera pas que ce n'est pas le même homme, parce qu'il n'a aucune raison de le remarquer — et parce que les deux tiennent exactement le même discours.`,
  monde: `Rien, et c'est la condition. Un homme en colère sur un pas de porte est le même dans les deux mondes.`,
  qui: [`joel`],
  gardes: [
    `**Aucun nom de famille, et le sien n'est jamais donné.** On dit l'homme, il, le type de l'entrepôt.`,
    `**Les deux filles ne sont jamais évoquées** — ni comptées, ni sexuées, ni décrites. Il ne dit jamais « elles ».`,
    `**Aucun marqueur d'âge sur lui.** Le lecteur doit pouvoir le superposer à l'homme de vingt-deux ans de la scène 6 sans que rien ne résiste.`,
    `Aucun marqueur de monde : pas de travée, pas de registre, pas d'arrivant, pas un mot de parenté.`,
    `Ça tourne laid sans tourner violent. Personne ne lève la main, et le narrateur ne juge pas.`,
    `Le grief reste réel, jamais caricatural, et on ne demande jamais d'y adhérer.`
  ],
  phrases: [
    { t: `On lui a reproché des propos déplacés.`, n: `**Le pivot de la scène.** Le mot doit tomber sans être souligné, et personne ne demande lesquels.` },
    { t: `Vous en seriez venus aux mains.`, n: `Formulation de l'autrice. Une bagarre au travail : même phrase, même sens, deux mondes.` },
    { t: `J'ai dit ce que tout le monde pense, et c'est moi qu'on montre du doigt.`, n: `Proposition. Se lit comme le grief des jaloux, et c'est un homme qui a insulté deux filles.` },
    { t: `J'ai perdu ma place pour trois mots.`, n: `Proposition. Il se croit la victime, et c'est ce qui le rend détestable et innocent en même temps.` }
  ],
  pourquoi: [
    `**Son mobile, proposé :** il travaillait au même endroit qu'elles. Il a dit des choses. On l'a écarté — muté, congédié, peu importe — et depuis il considère qu'on lui a pris sa place pour rien. *Ce n'est pas un prédateur, c'est un homme qui s'estime lésé, et il n'a rien fait d'autre que parler.*`,
    `**Son alibi, proposé :** il travaillait. Un poste, des horaires pointés, trois personnes qui l'ont vu. **Il ne le démontre pas** — il le jette, et c'est ce qui le rend crédible : un innocent n'apporte pas de preuves, il s'agace.`,
    `*Les deux tiennent dans les deux mondes sans une retouche, et c'est la seule chose à vérifier avant d'écrire quoi que ce soit d'autre.*`
  ],
  ouvert: [`**Et la scène 13 ?** L'alibi qui se confirme suit-il du côté de Joël, ou repasse-t-il chez Andrew ? *Du même côté, la piste naît et meurt dans le même monde, ce qui est plus propre. Chez Andrew, l'enquête d'ici enterre une piste d'ailleurs, et personne ne le saura jamais.*`],
  src: `04-plan/le-parcours-de-l-enquete.md §2, §4.4 — décision du 16 août 2026`
},
{
  id: `s13`, no: `Scène 13`, col: 16, row: `joel`, acte: `La fausse piste s'éteint`,
  face: `g-alibi`,
  titre: `L'alibi tient`,
  statut: `acquis`,
  resume: `Joël repart interroger quelqu'un, ailleurs, pour vérifier ce que l'homme a dit. Ça tient. La piste s'éteint sans coupable, sans explication et sans éclat.`,
  produit: `🔴 **Décision du 16 août 2026 : la scène est de Joël, comme la précédente.** Le lecteur croit toujours suivre Andrew, et croit qu'on vérifie l'alibi du marginal. *La piste naît et meurt dans le même monde — celui que le lecteur ne sait pas lire.*`,
  clef: `Celui qui crie n'est pas celui qui fait. L'homme a un alibi parce qu'il est bruyant : il crie, il est connu pour crier, tout le monde peut dire où il était. **Et ça vaut deux fois, puisqu'il y a deux hommes** — le vrai coupable, lui, est silencieux, et il est à l'exact opposé du milieu qu'on soupçonne.`,
  monde: `Rien, et il ne faut rien y mettre. C'est une scène de vérification : un lieu, quelqu'un qu'on interroge, une réponse qui ne bouge pas. Elle doit pouvoir se dérouler dans n'importe lequel des deux mondes sans qu'un mot change.`,
  qui: [`joel`],
  gardes: [
    `Mêmes contraintes que la scène 12 : aucun nom, aucun âge, aucun marqueur de monde, aucun mot de parenté, et les victimes jamais évoquées.`,
    `**Le lieu doit exister des deux côtés.** Un dépôt, un poste de nuit, une salle de pause, un comptoir. Rien qui n'appartienne qu'à un seul monde.`,
    `L'alibi tient franchement. Pas de doute résiduel, pas de témoin fuyant, pas de « mais » : une piste qui agonise fait perdre le lecteur, une piste qui meurt le libère.`,
    `Le milieu de la jalousie reste une fausse piste et rien de plus. Le grief garde toute sa place, mais il ne mène plus à personne.`
  ],
  lecture: `**Rien de ce que la piste a coûté n'est perdu pour lui** : il a l'économie du monde, le grief, la ruche, le régime pénal, la cérémonie des vingt-six, le jardin — et, sans le savoir, il vient de passer trois chapitres dans la vie d'avant.`,
  src: `04-plan/le-parcours-de-l-enquete.md §2, §3.1, §4.4 — décision du 16 août 2026`
},

/* ---------- L'ENLISEMENT ---------- */
{
  id: `s14a`, no: `Scène 14 · a`, col: 17, row: `andrew`,
  face: `g-coldcase`, acte: `L'enlisement`,
  titre: `Le départ de la seconde enquête`,
  statut: `acquis`, pivot: true,
  resume: `Andrew retourne au registre et **tombe sur un jeune arrivant dont plus rien n'est écrit après une certaine date.** La ligne est là, parfaite ; ensuite, les traces s'arrêtent. Il va demander la suite à l'administratif — **et on la lui refuse.**`,
  produit: `Andrew apprend qu'il existe une partie de ce monde qu'un veilleur n'a pas le droit de voir — et il l'apprend **avec le lecteur**, ce qui n'arrive nulle part ailleurs dans le livre.`,
  clef: `**Le registre ne s'est pas trompé : il n'a jamais eu à savoir.** Il ne note que les arrivées ; ce qui vient après est ailleurs, dans les dossiers du suivi. Et ceux du jardin sont sous secret médical.`,
  monde: `Le second registre, celui du suivi. Le secret médical du jardin. Et le fait qu'un veilleur ne soit pas au-dessus de tout.`,
  qui: [`andrew`,`isaac`],
  garde_forme: `**Ce n'est pas un mur, c'est un guichet.** Le secrétariat accepte de donner **le nom de le pédiatre qui a suivi l'arrivant et ce qu'il fait maintenant** — il exerce au jardin — **et refuse d'en dire davantage.** *Personne n'a rien décidé : on l'a renvoyé ailleurs, et le renvoi est l'information.* **La loi du monde ne s'énonce jamais, elle se heurte.**`,
  gardes: [
    `🔴 **Le registre ne peut pas être faux, et il ne l'est pas.** L'erreur est dans les dossiers d'après — le suivi, les affectations, tenus par des gens. *Si le registre devient discutable, le mouvement où Andrew lit sa propre ligne s'effondre.*`,
    `Pas un paragraphe sur le secret médical, pas un personnage qui expose le fonctionnement du jardin. **Quelqu'un répond non à une question, et c'est tout.**`,
    `**Test :** si l'on peut retirer la question sans perdre l'information, la scène est une description déguisée et elle est à réécrire.`,
    `Il y va parce que c'est son terrain, et Isaac le suit parce qu'Andrew est l'homme du registre. **Ce n'est pas une intuition qu'Isaac suit, c'est une compétence.**`
  ],
  ouvert: [`⚠️ **Quelle est l'erreur administrative, exactement.** *Un transfert non consigné, une fiche jamais rouverte, un service qui a changé de nom : assez banal pour qu'on n'en veuille à personne, assez net pour avoir coûté deux semaines.*`],
  src: `04-plan/le-parcours-de-l-enquete.md §4 ter.1, §4 ter.2 — décision du 16 août 2026`
},
{
  id: `s14-appel`, no: `Scène 14 · a bis`, col: 18, row: `andrew`, acte: `L'enlisement`,
  titre: `Il appelle Isaac`,
  statut: `acquis`,
  resume: `Il a une piste, un nom, un lieu. **Il prévient Isaac et ils se donnent rendez-vous au jardin.**`,
  produit: `Rien d'autre qu'un raccord, et c'est ce qu'il faut : *il a quelque chose, il appelle son ami, ils se retrouvent là-bas.* **La scène doit être plate.**`,
  clef: `🔴 **C'est le premier de deux coups de fil, et le second est celui qui compte.** *À la scène 17 c, il appellera de nouveau — et cette fois il dira « c'était là sous nos yeux ».* **Si celui-ci a le moindre relief, l'autre perd le sien.**`,
  garde_bis: `**Il ne sait pas qu'il a besoin d'un policier.** Il appelle Isaac parce que c'est ce qu'il fait, depuis des années, sur des affaires qui n'ont rien à voir. *Ce n'est qu'au jardin qu'une porte s'ouvrira pour une raison qu'aucun des deux n'aura prévue.*`,
  monde: `Rien.`,
  qui: [`andrew`,`isaac`],
  gardes: [
    `**Aucun enthousiasme.** Il ne pense pas tenir quelque chose ; il pense avoir un nom et une adresse, et ça se dit en trois phrases.`,
    `Isaac ne discute pas et ne pose pas de question. *Il vient parce qu'Andrew est l'homme du registre — et ça, c'est déjà écrit.*`,
    `Ni l'un ni l'autre ne formule que le secret médical vient de leur fermer une porte. **Ils vont voir quelqu'un, c'est tout.**`
  ],
  ouvert: [`Est-ce un chapitre, ou la dernière page du précédent ? *Trois phrases suffisent peut-être, et le blanc fait le reste.*`],
  src: `décision du 16 août 2026`
},
{
  id: `s14b`, no: `Scène 14 · b`, col: 19, row: `andrew`, acte: `L'enlisement`,
  titre: `L'entretien en marchant`,
  statut: `acquis`, pivot: true,
  resume: `Ils vont voir le pédiatre au jardin. **Il est un peu sur la réserve — puis il comprend qu'il a affaire à un policier, et il coopère normalement.** Il est très occupé : il leur propose de le suivre pendant qu'il répond. **Ils traversent le jardin en marchant à côté de lui.**`,
  produit: `**Et c'est comme ça que le lecteur voit le jardin : de biais, en marchant, pendant qu'on parle d'autre chose.** *Personne ne visite, personne n'explique — on suit quelqu'un qui travaille et qui répond en même temps.* Au bout : l'erreur administrative, et quelqu'un de trois ans qui va très bien.`,
  clef: `Le mur était un dossier, jamais une porte. **L'anticlimax est total, et il est humain : personne n'a rien fait de mal.** Ni victime, ni négligence, ni mauvaise volonté — une administration qui protège quelqu'un, et quelqu'un qui n'avait aucun besoin d'être cherché.`,
  monde: `Le bas de la courbe, vu une fois, en entier. **À trois ans la parole est partie depuis longtemps** : ils ont cherché deux semaines quelqu'un qui n'avait jamais disparu, et qui n'aurait pas pu répondre même s'il l'avait été. *Et Andrew voit, sans le formuler, ce qu'Eliott va devenir.*`,
  garde_forme: `**Le dispositif de la scène est la marche.** Il avance, ils suivent, il répond entre deux portes. *C'est ce qui autorise à montrer le jardin sans jamais le décrire : ce qu'on voit passe dans le champ, on ne s'y arrête pas.* **Sauf une fois — et c'est la scène suivante.**`,
  qui: [`andrew`,`isaac`,`pediatre`],
  gardes: [
    `**Il ne s'excuse pas et ne se justifie pas.** Il applique une règle, puis il en applique une autre quand un policier est là.`,
    `Aucun personnage ne formule l'ironie de la piste morte. Elle est dans le fait, pas dans une réplique.`,
    `Il ne parle jamais de l'âge d'un enfant du jardin ni du jour où sa descente a commencé. **C'est la seule chose qu'il ne dira pas, même à un policier.**`,
    `Le lecteur, lui, a la fiche complète d'Eliott en tête. **C'est le seul endroit du livre où l'épilogue est visible en avance, et il l'est par accident.**`,
    `⚠️ **L'anomalie : elle pleure, et elle s'excuse.** *On a dit que les berceurs devaient être des professionnels ; celle-ci ne l'est pas tout à fait.* Le pédiatre le relève, avec compassion et sans s'arrêter de travailler — « allons, allons, pourquoi pleurez-vous ? » — et elle répond « je… heu… pardon ». **Personne n'y voit un défaut, et ce n'en est pas un : c'est trop d'amour, pas trop peu.**`,
    `⛔ **Aucune description d'elle, et c'est vital.** Ni visage, ni âge, ni allure — *trois hommes regardent un bébé, pas une femme.* **Elle n'existe dans cette scène que par ce qu'elle dit et par la façon dont elle le dit** : une voix qui s'excuse d'exister. *Le lecteur non plus ne doit pas pouvoir la reconnaître de vue.*`,
    `**Et ses larmes ne s'expliquent jamais.** *Est-ce qu'elle pleure cet enfant-ci, ou celui qu'elle a pris, ou ce qu'elle est en train de devenir ?* **Le livre ne le dira pas, pas même à la fin.**`,
    `🔴 **C'est ici que tombe la réplique du ratio.** *Décision de l'autrice, 16 août 2026 : elle vient des données techniques que le pédiatre a en main.* — **« Ils mettent trois fois plus longtemps à descendre, en plus. »** *Sans commentaire, sans personne pour relever, et on parle d'autre chose à la phrase suivante.* **C'est la seule fois du livre où le lecteur peut se tromper d'arithmétique** : sans elle il calcule 1:1 et trouve huit au lieu de quinze.`,
    `**Et elle ne contredit pas son secret.** *Il ne dit l'âge de personne et ne date aucune descente* — il énonce une propriété du barème, comme un médecin cite une posologie. **C'est justement parce qu'il la trouve banale que le lecteur la garde.**`,
    `✅ **Un berceur, un homme, croisé en passant.** *Décision de l'autrice, 16 août 2026.* Le métier est mixte — le lexique dit « le berceur, la berceuse » — et le livre ne le montrait nulle part. **Il ne fait rien de particulier et personne ne le remarque :** il traverse, il porte quelque chose, il dit bonjour. *S'il devient un personnage, la correction se voit ; s'il n'est qu'un passant, elle s'installe.*`
  ],
  ouvert: [`Validée provisoirement le 16 août 2026 — l'autrice veut y revenir.`],
  src: `04-plan/le-parcours-de-l-enquete.md §4 ter.2 bis — décision du 16 août 2026`
},
{
  id: `s14c`, no: `Scène 14 · c`, col: 20, row: `andrew`, acte: `L'enlisement`,
  titre: `La salle, en passant`,
  statut: `acquis`, pivot: true,
  resume: `Ils passent devant une salle. **Dedans, une berceuse en tête à tête avec un tout-petit sur le point de disparaître.** Andrew s'arrête. Le pédiatre sait que c'est rare de voir ça quand on est extérieur au jardin : **il laisse passer.**`,
  produit: `**C'est la seule fois du livre où le monde est entièrement bon avec quelqu'un.** Partout ailleurs, quelqu'un est mal accompagné, mal cru, mal regardé, ou pas regardé du tout. Ici, non — il n'y a rien à reprocher à personne, et c'est la seule page dont on puisse le dire.`,
  clef: `**Une scène presque de mère et d'enfant, dans une grâce et un amour profonds.** *Et le mot est impossible à écrire, ce qui oblige à le faire tenir entièrement dans les gestes.*`,
  clefFin: `⚠️ **Et c'est elle.** La berceuse de cette scène est celle qui détient Eliott. *Le lecteur passe la plus belle page du livre à la regarder, et il l'aime.* Pendant ce temps, le garçon qu'elle a pris est enfermé quelque part.

**Ce qu'Andrew emporte, c'est une voix.** Son attention est sur le bébé, et la scène doit l'y garder : il ne voit pas son visage, il ne la décrit pas, il ne la regarde pas. *Mais elle parle — et c'est ce timbre-là, et rien d'autre, qui reviendra à la scène 17 c.*`,
  garde_forme: `🔴 **Le temps se dilate, et c'est le dispositif de la scène.** Trois personnes s'arrêtent — Andrew, Isaac, le pédiatre — et regardent. *On a donc tout le temps de décrire : les gestes, ce qui passe sur les visages, le rythme.* **On raconte une scène hors du temps pendant que trois personnes debout la regardent, et personne ne dit rien.**`,
  garde_bis: `**Ce n'est pas seulement du métier.** Un berceur est payé, comme une assistante maternelle est payée — *et il donne aussi de la tendresse et de l'amour.* **Porter quelqu'un jusqu'à zéro est le dernier acte d'amour qu'il puisse donner.** Et cet amour est un reliquat : elle avait déjà cette vocation là-bas. *Rien de tout cela ne se dit jamais dans le texte.*`,
  monde: `Jusqu'où va le métier de berceuse : jusqu'au dernier jour, littéralement, en portant. **Le lecteur n'a plus besoin qu'on le lui dise, il vient de le voir.** *Et ça charge rétroactivement June, sans qu'une ligne le formule.*`,
  qui: [`berceuse`,`andrew`,`isaac`,`pediatre`],
  gardes: [
    `**Aucun pathos sur la page.** Une position à trouver, un poids à répartir, un rythme à tenir. *L'émotion est entièrement dans ce que le lecteur sait du métier, et pas une ligne ne la dit.*`,
    `**Aucune explication.** Rien n'annonce que ça commence et rien ne signale que c'est fini. Personne ne commente en repartant.`,
    `**Elle reste anonyme : un geste, une silhouette, pas un portrait.** Pas de visage, pas de nom, pas de réplique.`,
    `**Ne rien faire de plus.** Pas de personnage qui s'attarde après, pas de retour dessus plus tard, pas de résonance ménagée avec l'épilogue.`
  ],
  phrases: [{ t: `Elle le berçait au rythme de la chaîne autour de son cou, symbole de sa foi.`, n: `**Le détail qui plante tout, et c'est un objet — pas un visage.** *Décision de l'autrice, 16 août 2026.* Il résout la contrainte d'anonymat au lieu de la contredire : **on ne décrit pas quelqu'un, on décrit une chose qu'il porte.** Et il rime avec la dernière image de la scène 19.` }],
  ouvert: [`✅ **Et si c'était elle — le livre ne le dira jamais.** *Décision de l'autrice, 16 août 2026 : le doute plane et ne se referme pas.* Le lecteur se souviendra peut-être, à l'arrestation, d'avoir vu quelqu'un porter un mourant avec une tendresse parfaite. **Si c'est elle, la scène cesse d'être une belle parenthèse : c'est son mobile, joué devant nous, à l'instant où on la retire du monde.** *Et si ce n'est pas elle, la scène garde tout son sens. Rien ne dépend de la réponse — c'est ce qui permet de ne jamais la donner.*`,
           `Chante-t-elle ? *S'il y a un chant, il ne doit être ni nommé ni décrit comme un rituel — le risque est de fabriquer une cérémonie là où il n'y a qu'un geste.*`,
           `Ce que devient le corps, après. *La scène peut s'arrêter avant.*`],
  src: `02-univers/le-jardin.md §6 — 03-personnages/la-berceuse.md §7 — décision du 16 août 2026`
},
{
  id: `j3`, no: `Scène 14 · d`, col: 21, row: `joel`, acte: `L'enlisement`,
  titre: `Il continue quand même`,
  statut: `acquis`,
  resume: `🔴 **Décision de l'autrice, 16 août 2026.** On le voit acculé. **C'était évidemment une fausse piste.** Une scène de lassitude, énervé d'avoir perdu du temps. *Et pourtant : il pense que ça vaut le coup de continuer.* **Il décide de retourner au commissariat pour parler avec son ami.**`,
  produit: `🔴 **C'est aussi le creux, et le creux n'avait pas besoin de deux chapitres.** *La carte « Il n'a plus rien », qui s'intercalait à la 14 · a bis, est supprimée le 16 août 2026 : cette scène-ci la remplace.* **Les deux semaines perdues d'Andrew et les semaines perdues de Joël sont les mêmes semaines** — et les deux enquêtes s'enlisent en parallèle sans qu'aucun effet d'écriture n'ait à les rapprocher : *une enquête qui piétine se ressemble partout.*

**Le raccord le plus large du livre.** Le lecteur regarde un homme décider d'aller au commissariat — et le chapitre suivant montre Andrew au commissariat. *Il n'a pas à supposer quoi que ce soit : il a vu la décision, il voit l'arrivée, il coud.* **La décision appartient à Joël, l'arrivée appartient à Andrew, et rien dans le texte ne ment.**`,
  lecture: `**C'est la portion du livre où il est le plus incapable de distinguer les deux hommes**, et c'est voulu. \n\n**Ce que croit le lecteur :** Andrew sort du jardin, l'erreur administrative lui a mangé deux semaines, il est vidé, il rentre, il rumine — et il se dit que non, il ne lâche pas, et qu'il va aller voir Isaac. *La scène suivante lui donne raison.* **Ce qui se passe vraiment :** un autre homme, un autre monde, un autre ami.`,
  clef: `🔴 **Et c'est ce qui rend la scène 15 a beaucoup plus dure.** *Le lecteur vient de regarder quelqu'un décider que ça valait le coup* — et à la page suivante, on lui dit de lâcher l'affaire. **La gifle n'est possible que si la main s'est levée dans le chapitre d'avant.**`,
  garde_forme: `**Aucune phrase de décision.** Pas de « il ne lâcherait pas », pas de mâchoire serrée, pas de résolution formulée. *Ça se voit à ce qu'il fait : il ne rentre pas chez lui, il reprend la voiture, il regarde l'heure et il y va quand même.*`,
  garde_bis: `**L'énervement est celui du temps perdu, pas celui de l'échec.** Il n'en veut pas à l'affaire, il en veut aux jours. *Et le livre sait, lui, que pendant ces jours-là les deux qu'il cherche vraiment sont en train de mourir — mais aucune phrase ne le dit ici.*`,
  monde: `Rien, et c'est volontaire. Un bureau, une route, une fin de journée. **La deuxième portion du livre où il n'y a aucun monde à expliquer** — et c'est exactement ce qui la rend indépartageable.`,
  qui: [`joel`],
  gardes: [
    `🔴 **Il ne nomme pas son ami.** *« L'autre », « lui », « son collègue » — jamais le prénom.* **C'est la seule condition du raccord** : un nom qui n'est pas Isaac casse tout, et un nom qui est Isaac serait un mensonge.`,
    `⚠️ **À vérifier contre les autres chapitres de Joël.** *Si Liam y est nommé couramment, ne pas le nommer ici devient une anomalie repérable à la première lecture.* **Alors il faut que l'absence de nom soit la règle dans toute la branche, pas une exception dans ce chapitre-là.**`,
    `La fatigue est physique et banale. Elle se dit par des choses : la faim qui est passée, la lumière du tableau de bord, une porte qu'on ferme trop fort.`,
    `**Il ne récapitule pas l'affaire.** Pas de bilan mental, pas de liste de ce qu'il a éliminé. *Le lecteur en sait déjà assez — et un récapitulatif obligerait à nommer des choses qui n'existent que d'un côté.*`,
    `Ni chiffre, ni date, ni lieu identifiable. **Le chapitre doit pouvoir se lire dans les deux mondes sans qu'un seul mot ait à être repris.**`,
    `🔴 **On ne compte jamais.** Ni les disparues de l'affaire, ni celles du vieux dossier. *Le lecteur doit pouvoir lire « une vieille affaire mal classée » et la rapporter au dossier de l'arrivant dont les traces s'arrêtent.*`,
    `**Ne pas égayer le creux.** Pas de rebondissement, pas de demi-indice, pas de scène de monde pour tenir le lecteur. *Ce qui tient le chapitre, c'est qu'il décide de continuer à la fin — et rien d'autre.*`
  ],
  ouvert: [`🔴 **Quelle était la fausse piste, exactement.** *Une piste, héritée de la carte supprimée : un vieux dossier mal classé qui ressemblait à un précédent, et où tout le monde va bien.* **Exactement comme en face** — et pendant ces semaines-là, les deux qu'il cherche vraiment sont en train de mourir.`,
           `✅ **Le lendemain matin.** *Décision de l'autrice, 16 août 2026 : la nuit laisse au lecteur le temps de bien s'installer dans son erreur.* **Le chapitre se ferme donc le soir, sur la décision et pas sur le trajet** — et la scène 15 a s'ouvre sur un homme déjà au commissariat. *Personne ne raconte la nuit, et c'est dans ce blanc-là que le lecteur change d'homme sans le savoir.*`],
  src: `décision du 16 août 2026`
},
{
  id: `s15a`, no: `Scène 15 · a`, col: 22, row: `andrew`, acte: `L'enlisement`,
  face: `s15b`,
  titre: `Au commissariat`,
  statut: `acquis`, pivot: true,
  resume: `Andrew insiste. Il insiste encore. Il parle de reprendre le registre, de vérifier des lignes, de recouper des dates. **Il voit la motivation d'Isaac le lâcher et il panique un peu, sans contrôle** — il essaie de lui donner un coup de fouet. Isaac tranche sèchement. Fin de chapitre.`,
  produit: `🔴 **Décision du 16 août 2026 — et c'est ici que le lecteur est explicitement du côté d'Andrew.** Aucune ambiguïté, aucun doute : on est dans ce monde-ci, avec ces deux hommes-là. *C'est ce qui rend le chapitre suivant impossible à soupçonner.*`,
  clef: `**Sa panique est du métier retourné contre lui.** Ce qu'il propose pour relancer, c'est de vérifier des documents — le registre, des lignes, des dates. **Il n'a rien d'autre à offrir, parce que c'est tout ce qu'il sait faire**, et Isaac, lui, sait que ça ne vaut rien à ce stade.`,
  monde: `Le registre revient dans sa bouche comme une solution, une fois de plus. Personne ne relève.`,
  qui: [`andrew`,`isaac`],
  gardes: [
    `Sa panique ne se nomme pas. Pas de « il paniquait », pas de cœur qui s'emballe : ça se voit à ce qu'il propose, et au fait qu'il le propose deux fois.`,
    `Isaac n'est ni las ni lâche. **Il a raison**, et il le dit comme on dit une chose désagréable qu'on a déjà pesée.`,
    `✅ **Et c'est ici qu'il s'en va, pas dans un chapitre à lui.** *La scène 16 est supprimée le 16 août 2026 : Isaac se retirait deux fois.* **Ce n'est pas le délai, c'est la crédibilité** — il a suivi l'homme du registre dans un mur, et il ne se laissera pas emmener une seconde fois. *Son départ est entièrement juste et entièrement la faute d'Andrew.*`,
    `Ne jamais faire d'Isaac un lâche, ni un tiède, ni un fonctionnaire. **Ne jamais lui faire dire qu'il a été trompé — il ne l'a pas été.** *La scène ne se joue pas entre un bon et un mauvais : elle se joue entre la raison et l'entêtement, et le livre ne donne tort ni à l'un ni à l'autre.*`,
    `Le chapitre se ferme sur la réplique. Pas de réaction d'Andrew, pas de ligne de narrateur derrière.`
  ],
  phrases: [{ t: `Lâche l'affaire, Andrew… tu comprends pas, on a perdu trop de temps ; on court déjà après un cadavre !`, n: `Formulation de l'autrice. **Le prénom est capital** : il ancre le chapitre sans discussion possible dans le monde d'ici — et c'est précisément ce qui autorise le chapitre suivant.` }],
  src: `04-plan/le-meme-jour.md §5.3, §5.5 — décision du 16 août 2026`
},
{
  id: `s15b`, no: `Scène 15 · b`, col: 23, row: `joel`, acte: `L'enlisement`,
  face: `s15a`,
  titre: `« Lâche l'affaire »`,
  statut: `acquis`, pivot: true,
  resume: `Le ton est monté. On se répond, on hausse la voix, quelqu'un répète ce qu'il a déjà dit. **Puis il regarde les dossiers, et il n'y touche plus.** Le chapitre se ferme sur un abandon.`,
  produit: `🔴 **Le chapitre suivant, et on a changé de monde sans que le lecteur le sache.** Il croit lire la suite de la dispute : même pièce, mêmes hommes, ton qui monte d'un cran. *Ce sont deux disputes, dans deux mondes, à dix ans d'écart — et c'est la coupe de chapitre qui fait tout le travail.*`,
  clef: `**« Je te le répète » est la charnière, et c'est une équivoque parfaite.** Chez Joël, elle renvoie à ce qui a déjà été dit dans sa propre conversation. Pour le lecteur, elle renvoie au chapitre d'avant. **Les deux lectures sont exactes, et aucune n'est un mensonge.**`,
  lecture: `Il vient de voir Isaac dire à Andrew de lâcher. Il lit la suite. Il n'y a pas de suite — *et il aura fabriqué lui-même la scène la plus importante du dispositif.* **Et il croit voir un homme abandonner**, ce qui rend le chapitre d'après plus fort qu'il n'a le droit de l'être.`,
  monde: `Rien, et surtout rien. Un commissariat se ressemble partout, une engueulade entre deux collègues aussi : c'est exactement ce qui rend la méprise possible.`,
  qui: [`joel`],
  gardes: [
    `**Aucun prénom.** Le chapitre précédent a dit « Andrew » ; celui-ci ne dit personne, et le lecteur reporte le nom tout seul.`,
    `Aucun marqueur de monde : pas de travée, pas de registre, pas d'arrivant, pas un mot de parenté.`,
    `Aucune des deux victimes n'est comptée, décrite ni sexuée. Le lecteur doit pouvoir y lire un garçon de dix ans.`,
    `**Les deux chapitres ne se citent jamais l'un l'autre**, et rien dans celui-ci ne rappelle celui-là. C'est le lecteur qui raccorde ; s'il est aidé, il voit la couture.`
  ],
  phrases: [
    { t: `Comment tu peux sortir ça ? Tant qu'on a rien retrouvé, on peut rien avancer.`, n: `Formulation de l'autrice. Joël se défend — et la phrase vaut mot pour mot pour un garçon disparu.` },
    { t: `Je te le répète, lâche l'affaire ! À l'heure qu'il est, les vers ont sûrement commencé leur travail !`, n: `Formulation de l'autrice. **« Je te le répète » est le mot qui coud les deux chapitres.** Il ne doit être ni souligné, ni commenté, ni relevé par personne.` }
  ],
  ouvert: [`**Ce que devient « c'est déjà ce qu'on m'a dit ».** La réplique qui échappait à Andrew n'a plus de place ici : le dispositif ne passe plus par un écho dans sa tête, il passe par une coupe de chapitre. *À supprimer, ou à replacer ailleurs — mais pas ici, où elle ferait doublon avec un procédé plus fort.*`],
  src: `04-plan/le-meme-jour.md §5.3, §5.3 bis, §5.5 — décision du 16 août 2026`
},
{
  id: `s15c`, no: `Scène 15 · c`, col: 24, row: `andrew`, acte: `La remontée`,
  face: `s17b`,
  titre: `Il passe outre, et il n'en tire rien`,
  statut: `trou`, pivot: true,
  resume: `**Décision de l'autrice, 16 août 2026 : ce chapitre en absorbe deux.** *L'ancienne scène 17 a — « il se fait des nœuds au cerveau » — n'existe plus séparément.* **Quelque chose a retenu son attention dans le dossier**, pendant la conversation houleuse au commissariat. Il décide d'y réfléchir au calme. *Là où l'autre s'est arrêté net, celui-ci ne s'arrête pas.* **Puis il y passe la journée, seul, et ça ne donne rien.**`,
  produit: `**Le lecteur a lu une seule scène :** un homme sommé d'arrêter, qui désespère, qui regarde ses dossiers — puis qui décide de continuer quand même. **Il y avait deux hommes.** *Le premier s'est arrêté et il a perdu deux filles ; le second a continué et il retrouvera le garçon vivant.*`,
  clef: `*C'est le §4 bis.3 rendu invisible : l'obéissance puis le refus, le même geste à deux issues, livré en trois coupes de chapitre et sans une phrase pour le signaler.* **Le lecteur croit assister à une hésitation. Il assiste à une bifurcation.**`,
  clefFin: `✅ **Et c'est ce chapitre qui apprend au lecteur qu'Isaac est parti — par une absence.** *La scène 16, où Isaac lâchait l'affaire, est supprimée : il se retirait déjà en fermant la 15 a.* **Plus de second homme dans les scènes, plus de véhicule, plus de poste où entrer sans s'annoncer.** *Aucune phrase ne dit qu'il est parti. On s'en aperçoit.*`,
  garde_forme: `⛔ **Ce qu'il a remarqué ne doit rien donner.** *C'est la condition de toute la séquence :* le chapitre ouvre sur quelque chose qui ressemble à une piste, y passe des heures — et se ferme sur rien. **Sans ça, l'idée arrivée en tête de chapitre pré-annonce la solution, et les trois chapitres suivants n'ont plus rien à découvrir.**

**La forme suit :** ① il note la chose, sans y croire, dans une pièce où on lui crie dessus ; ② il se la garde ; ③ il y consacre sa journée ; ④ il n'en tire rien ; ⑤ **le chapitre se ferme sur une fin de journée** — pour que le suivant se lise comme un soir, et le troisième comme un lendemain.`,
  lecture: `Il ne peut pas savoir qu'il vient de voir la différence entre les deux vies du même homme. *Il la verra à la relecture, et il n'y aura toujours rien à corriger : personne n'a menti.* **Et il sort du chapitre en croyant que cet homme-là est fini** — ce qui est exactement l'état qu'il faut pour lire le chapitre suivant de travers.`,
  monde: `Rien de neuf, et ce n'est pas le moment d'en mettre.`,
  qui: [`andrew`],
  gardes: [
    `**Aucun personnage ne rapproche les trois chapitres**, ni sur le moment ni plus tard.`,
    `Andrew ne comprend rien à ce qui vient de se passer. Pas d'illumination, pas de déjà-vu formulé.`,
    `Ce qu'il a remarqué ne doit contenir aucune information venue de l'autre monde. **Rien ne traverse.**`,
    `**Il ne devient pas meilleur enquêteur : il devient un homme seul qui continue.** *Pas de progrès — c'est la condition pour que le chapitre suivant se lise comme une pause méritée.*`,
    `⛔ **Aucun retour en arrière sur le départ d'Isaac.** Pas de « depuis qu'il était seul », pas de coup de fil qu'on ne passe plus, pas de souvenir de la dispute. *L'ellipse ne tient que si personne ne la comble.*`,
    `✅ **Et personne ne dit ce que ça lui coûte.** *Passer outre, c'est perdre Isaac* — mais le chapitre ne le formule pas, ne l'anticipe pas, et ne se ferme pas sur un adieu.`
  ],
  pourquoi: [
    `**Ce qui a été écarté le 16 août 2026 :** on lui demandait de signer quelque chose qui clôt le dossier — un formulaire, un classement, une restitution — **et il ne le faisait pas.** *C'était son défaut retourné pour la première fois : l'homme qui croit les documents et pas les gens refuse un document.* **Écarté parce qu'un refus est un geste, et qu'un geste se remarque** — or ce déclenchement-ci doit être le plus petit des trois.`,
    `**Écarté aussi, plus sec :** il n'y a pas d'élément du tout, Isaac se détourne et Andrew ne bouge pas. *Ça marchait, mais ça ne donnait rien à la relecture — et surtout ça laissait la journée suivante sans objet.*`
  ],
  ouvert: [`⚠️ **Qu'est-ce qui a retenu son attention, exactement.** *Trou neuf, petit mais réel.* **Trois contraintes :** ça doit se voir dans un dossier qu'il a sous les yeux pendant qu'on lui crie dessus ; ça ne doit lui donner aucune direction ; **et ça doit pouvoir ne rien donner sans que le lecteur se sente floué.**`,
           `⚠️ **Trois déclenchements se suivent** — celui-ci, le reliquat qui lui rend le geste, et la phrase d'Eliott qui lui donne le lieu. *Deux, c'est une remontée ; trois, c'est une machine.* **Celui-ci doit rester le plus petit : il décide seulement qu'il ne s'arrête pas.**`],
  src: `04-plan/le-parcours-de-l-enquete.md §4 bis, §4 bis.3 — décision du 16 août 2026`
},
{
  id: `s17b`, no: `Scène 17 · b`, col: 25, row: `joel`, acte: `La remontée`,
  face: `s15c`,
  titre: `Il rentre chez lui`,
  statut: `acquis`, pivot: true,
  resume: `Il est rentré chez lui, dépité. Il s'affale sur son canapé. Il fait des choses banales. **C'est un abandon complet.**`,
  produit: `🔴 **Et le lecteur ne doit surtout pas le lire comme tel.** Pour lui, on est toujours chez Andrew : une fin de journée éreintante, une pause après tous ces nœuds au cerveau. *Un homme qui souffle, rien de plus.* **C'est le chapitre le plus dangereux du livre à écrire, parce qu'il doit être deux choses opposées à la fois sans qu'un seul mot penche d'un côté.**`,
  clef: `**Ce que Joël fait ici, c'est renoncer. Ce que le lecteur voit, c'est quelqu'un qui se repose.** La seule différence entre les deux est dans ce qui suit — et le lecteur croira que ce qui suit, c'est le même homme qui repart.`,
  lecture: `Il aura vu un homme s'obstiner, puis souffler, puis trouver. Trois chapitres, un seul arc. **Il y a deux hommes, et l'un des deux ne s'est jamais relevé.**`,
  monde: `⚠️ **Un intérieur est l'endroit du livre où un monde se trahit le plus vite.** Rien chez lui ne doit être impossible chez Andrew : pas d'image de quelqu'un, pas d'objet qui suppose une histoire, rien qui vienne d'avant. *Corollaire de plan : mieux vaut que le lecteur n'ait jamais vu le logement d'Andrew avant ce chapitre — sinon il compare.*`,
  qui: [`joel`],
  gardes: [
    `**Aucune phrase de renoncement.** Pas de « il n'y retournerait pas », pas de dossier qu'on repousse, pas de décision. Il rentre, il s'assoit, il fait des gestes.`,
    `**Et aucune phrase de repos non plus.** Pas de « il avait besoin de souffler », pas de fatigue commentée. Le narrateur ne qualifie rien : il décrit des gestes, et le lecteur choisit — il choisira mal.`,
    `Aucun nom, aucun marqueur de monde, aucun mot de parenté.`,
    `**Ne rien y faire arriver.** Pas d'appel, pas de pensée qui relance, pas de détail qui reviendra plus tard. Une page où il ne se passe rien, et c'est tout le travail.`
  ],
  pourquoi: [
    `**C'est l'endroit du livre où poser un faux raccord de corps.** Une scène domestique donne le rasage, le miroir, la main qui prend un verre, la façon de s'asseoir. *Le dossier cherchait une scène où la cicatrice puisse se voir sans qu'on montre un visage : elle est là.*`,
    `**Et ça absorbe la carte « Joël retourne à ses notes », qui n'a plus lieu d'être.** L'ancien mécanisme voulait qu'Andrew regarde un homme reprendre un dossier lâché ; la doctrine du 16 août l'interdit — Andrew ne regarde rien, c'est le lecteur qui attribue. *Le retour de Joël à l'affaire se fait donc hors champ, entre ce chapitre et la planque, et le livre n'a jamais eu besoin de le montrer.*`
  ],
  src: `04-plan/le-parcours-de-l-enquete.md §4 bis.2 — décision du 16 août 2026`
},
{
  id: `s17c`, no: `Scène 17 · c`, col: 26, row: `andrew`, acte: `La remontée`,
  face: `g-piste`,
  titre: `Il a trouvé`,
  statut: `trou`, pivot: true,
  resume: `Il refait la promenade qu'il avait faite avec le garçon, comme un homme qui suit un fantôme. Une phrase lui revient — *« il y avait un magasin de chaussures ici, pas une épicerie »* — et il entre dans l'épicerie. Il flâne dans les rayons, il passe en caisse. **La femme devant lui est nerveuse. Elle fait tomber sa monnaie.**`,
  clefFin: `✅ **Et sa culpabilité reste exacte, sans qu'aucune phrase n'ait à être retrouvée.** *Ce n'est pas qu'il a manqué un indice : il est resté trois mètres devant elle et il ne l'a pas regardée.* **Il regardait le bébé.** *L'homme qui lit les documents et pas les gens était dans la même pièce que la coupable, et il n'a emporté qu'un timbre de voix.* **C'est la faute d'avant refaite à l'identique, dans la même vie, avec le même geste — et sans qu'il puisse le savoir.**`,
  produit: `**C'est sa peur d'être reconnue qui la fait reconnaître.** *Elle sait qui il est : elle l'a vu au jardin avec le policier.* Andrew, lui, serait passé à côté — il n'avait pas retenu son visage. **Elle lâche sa monnaie parce qu'elle l'a vu, et c'est en ramassant la monnaie qu'il l'entend.** *Elle fabrique elle-même ce qu'elle redoute.*`,
  clef: `**Il ne déduit rien de toute la scène : elle fait tout le travail.** Elle s'excuse trop vite, elle se retourne, et le lendemain elle le conduit à l'enfant sans savoir qu'elle est suivie. *Le chapitre s'appelle « Il a trouvé » et il n'y a pas une déduction dedans — seulement de l'entêtement, le même exactement qu'à la scène 15 a où il avait tort.*`,
  garde_forme: `**Le déroulé.** ① il marche, la phrase du gamin lui revient, il entre dans l'épicerie — *sans rien chercher : le magasin ne contient rien* ; ② il flâne, il passe en caisse ; ③ la femme devant lui laisse tomber sa monnaie et **s'excuse auprès du caissier** — *« heu… pardon… »* — pendant qu'il s'accroupit pour l'aider ; ④ leurs regards se croisent — **un micro-blanc**, et elle essaie de le contenir ; ⑤ elle finit de payer maladroitement et sort en trombe ; ⑥ il retourne au jardin : **on lui donne un nom, pas une adresse** ; ⑦ le lendemain, il la prend en filature ; ⑧ elle le mène droit au lieu, elle en repart, il appelle.

*Coupure de chapitre possible après ⑥ : le refus d'adresse ferme bien, et « le lendemain » rouvre.*`,
  garde_bis: `⚠️ **Andrew relit deux fois la même scène sans le savoir.** *Au jardin, le pédiatre relevait ses larmes et elle bredouillait pardon ; ici, c'est au caissier qu'elle s'excuse d'avoir lâché sa monnaie.* **Deux fois quelqu'un derrière un comptoir, deux fois la même femme qui s'excuse d'exister — et il n'est l'interlocuteur ni de l'une ni de l'autre.**

*Il ne reconnaît pas un visage : il reconnaît un timbre, et il n'est même pas celui à qui on parle.* **Ce qu'il entend, il l'entend par-dessus l'épaule de quelqu'un d'autre — exactement comme la première fois.**`,
  lecture: `Le lecteur a passé la plus belle page du livre à la regarder bercer un tout-petit, **et il l'aimait.** *À la relecture, « je… heu… pardon » n'est plus une femme qui s'excuse de pleurer.*`,
  monde: `Le jardin donne un nom et refuse une adresse. **Rien d'hostile, rien de dramatique** — la même administration qu'à la scène 14 b, qui protège des gens et le fait bien.`,
  qui: [`andrew`,`isaac`],
  gardes: [
    `**Aucune phrase du genre « il la reconnut ».** *Il ne la reconnaît jamais complètement, pas même en la suivant.* Il a une voix, une attitude, et rien d'autre — et il y va quand même.`,
    `Elle ne parle pas. **Deux mots dans tout le chapitre**, et ce sont ceux qu'elle a dits au jardin.`,
    `⛔ **Il ne la reconnaît pas — c'est sa voix qui la reconnaît, et ça l'interpelle, rien de plus.** *Aucun soupçon dans le magasin : il aide quelqu'un à ramasser de la monnaie, c'est tout ce qu'il croit faire.* **Une écharde, pas une piste.** *Et c'est la façon dont elle sort qui, une minute plus tard, transforme l'écharde en question.*`,
    `**Le micro-blanc ne s'écrit pas comme un suspense.** *Une seconde de trop, un regard qui ne se détourne pas assez vite, et elle qui se remet à compter sa monnaie.* Le narrateur n'en fait aucun cas.`,
    `**La filature ne doit rien avoir de spectaculaire.** Un homme seul, sans voiture, qui attend dans une rue et qui marche derrière quelqu'un. *S'il y a du suspense, il vient de ce qu'on sait déjà, jamais de la mise en scène.*`,
    `« C'était là sous nos yeux » est dit une fois, au téléphone, et personne ne le relève. Ça ne doit jamais être expliqué.`,
    `**L'hypothèse « le gamin fabulait » reste debout jusqu'à la dernière page.** Rien de ce qu'Eliott a dit n'est confirmé par cette scène : c'est une femme qui s'excuse mal, pas une phrase qui se vérifie.`
  ],
  pourquoi: [
    `**Trouvaille de l'autrice, 16 août 2026 — et elle rachète la scène 14 c**, qui était la plus belle du livre et ne servait à rien. *Elle y pleurait, le pédiatre le relevait doucement, elle bredouillait pardon.* **C'était de l'amour ; ça devient une pièce.**`,
    `**L'asymétrie est le moteur.** *Elle le reconnaît, lui ne la reconnaît pas.* Elle réagit à une reconnaissance qui n'a pas eu lieu — **et c'est cette réaction-là qui la déclenche.** *Sans son affolement, il passait son chemin.*`,
    `**Et ce sont les mots du gamin qui l'amènent là — sans être un indice.** *Il entre dans l'épicerie parce qu'un garçon en avait parlé et qu'il n'a plus que ça : un geste de deuil, pas d'enquête.* **Ce que ce gosse racontait lui a valu de n'être cru par personne, et ça l'a blessé.** *Ce sont ces mêmes mots, faux, moqués, qui amènent Andrew au bon endroit — et l'épicerie est bien une épicerie. Il avait tort, et il sauve tout.*`,
    `**Le hasard n'achète qu'un soupçon.** *Elle fait ses courses dans le quartier où elle travaille, il entre dans un magasin pour une raison qui lui appartient — personne n'a besoin d'une coïncidence.* **Et tout ce qui suit est du travail :** retourner au jardin, obtenir un nom, se faire refuser l'adresse, attendre un jour, marcher derrière quelqu'un.`,
    `⛔ **Écarté : ils se rentrent dedans dans la rue.** *Ça reposait entièrement sur un hasard, et ça ne donnait à Andrew que deux secondes pour tiquer.* **La caisse lui en donne trente**, à genoux, à côté d'elle, pendant qu'elle parle.`,
    `**Et il ne trouve toujours rien lui-même : c'est elle qui le conduit.** *Ne sachant pas qu'elle est suivie, elle va là où il faut aller.* **L'homme qui croit les documents et pas les gens est sauvé en suivant quelqu'un.**`,
    `⛔ **Écartées, notées pour ne pas y revenir :** la voiture qu'il n'a pas ; la voisine qui dit bonjour ; le nom prononcé et laissé tomber ; le gamin qui décrivait un intérieur ; **la fenêtre, la lumière qui s'éteint et le cadenas.** *Cette dernière marchait, mais elle obligeait le lieu à être sa maison — et elle donnait la scène à un homme qui déduit.*`
  ],
  ouvert: [`✅ **La réplique d'Eliott saute — décision du 16 août 2026.** *Elle ne servait plus, et ce qu'elle emportait est remplacé par mieux :* **l'indice à retrouver n'est plus une phrase, c'est une personne.** Le lecteur a passé la plus belle page du livre à la regarder. *Il n'avait pas à la déchiffrer : il avait juste à la voir, et il ne l'a pas vue non plus.*`,
           `⚠️ **Où il la suit — sa maison, ou ailleurs.** *Ailleurs est plus fort : plus rien à déduire, il voit l'endroit.* **Et ça libère « c'était là sous nos yeux » de la géographie** — la phrase ne parle plus d'un lieu, elle parle d'elle. *Ils sont restés trois mètres devant elle pendant qu'elle berçait un enfant.*`,
           `⚠️ **Est-ce que ça tient en un chapitre ou en deux.** *Le refus d'adresse au jardin ferme très bien, et « le lendemain » rouvre.*`],
  phrases: [{ t: `c'était là sous nos yeux`, n: `⚠️ **Et depuis le 16 août 2026, elle ne parle plus d'un lieu : elle parle d'elle.** *Ils sont restés trois mètres devant elle, au jardin, pendant qu'elle berçait un enfant — et ils cherchaient le garçon qu'elle avait pris.* **C'est le sens le plus littéral que la phrase puisse avoir, et personne ne l'entend.**

**Second coup de fil du livre, et le premier était plat exprès** — voir la scène 14 · a bis. Réplique d'Andrew à Isaac, au téléphone, au moment de donner l'adresse. C'est une réplique de policier, elle a le droit d'être banale — c'est le lecteur qui saura qu'elle est littérale. Les berceuses habitent à côté du jardin ; elle vit à quelques pas de chez June ; Andrew est passé devant sa porte à chacune de ses trois visites.

✅ **Et depuis le 16 août 2026, elle est littérale trois fois.** *Il est passé devant. Il est passé devant avec le gamin. Et le gamin a parlé à cet endroit-là.* **C'est la seule réplique du livre qui dise exactement ce qu'elle dit, au moment où personne ne peut l'entendre** — Isaac la prend pour une formule de flic, et le lecteur se dit « mais oui, bien sûr ».` }],
  pourquoi: [
    `✅ **Trouvé le 16 août 2026 — et c'est l'autrice qui l'a trouvé.** *Le trou n'était pas « qu'est-ce qu'Eliott a dit » : c'était « comment Andrew y revient ».* **Il refait la tournée.** *Celle de la scène 2 — décision de l'autrice, 22 août 2026 : la sortie n'est plus une promenade de quartier mais la tournée de portage du garçon, la dernière fois qu'il l'a vu dans ce contexte-là.* **Comme un homme qui suit un fantôme.** Il déambule, et un mot lui revient. Puis une intuition.`,
    `**Pourquoi ça tient, alors que rien d'autre ne tenait :** *le trajet n'est pas le sien, c'est celui d'Eliott.* **Ses pieds n'ont donc pas à choisir cette rue-là : le gamin l'a choisie pour lui, il y a des semaines.** *Aucun hasard à couvrir, aucune attention à diriger — il suit un itinéraire qui existe déjà.*`,
    `**Et les mots sont accrochés au trottoir.** *Regarder la scène de la tournée : « mais si, il y avait un magasin de chaussures ici, pas une épicerie » — c'est une phrase qu'on ne peut dire que devant quelque chose.* **Le gamin commentait ce qu'il passait, comme font les gamins ; Andrew marchait à côté et écoutait à moitié.** *Chaque bout de rue porte donc ce qui s'y est dit, et il suffit de le refaire pour que ça revienne.* **Ce n'est pas un procédé : c'est comme ça que la mémoire fonctionne.**`,
    `**Devant une porte, la chose qu'il avait rangée dans le délire est debout devant lui.** *Et « c'était là sous nos yeux » devient exact au sens propre :* **il est passé là avec le garçon, et le garçon a parlé à cet endroit précis.**`,
    `**C'est son défaut retourné, enfin.** *L'homme qui croit les documents relit le monde — et le seul document qu'il consulte ce jour-là est une promenade.* **Il n'est pas revenu chercher un indice : il a arrêté de travailler, et la chose est arrivée.** *Personne ne le formule.*`,
    `⛔ **Trois pistes écartées le 16 août 2026, à ne pas refaire.** *① La voiture :* Andrew n'en a pas, il était déjà à pied les trois premières fois. *② Il s'arrête devant chez June et lit une porte :* **un homme planté devant une porte regarde ses pieds, pas la maison d'en face** — rien ne dirige son attention. *③ June parle d'Eliott et le nom tombe :* **ça marche, mais c'est elle qui trouve et lui qui reçoit**, et le chapitre s'appelle « Il a trouvé ».`,
    `⚠️ **Ce que ça exige de la scène 2, et c'est une dépendance dure.** *La promenade doit être sur la page, marchée, avec les phrases dedans* — sinon le lecteur ne peut pas revenir en arrière et retrouver l'endroit. **Elle y est déjà : « puis ils sortent faire un tour — c'est dehors, en marchant, que le garçon dit ce qu'il dit ».** *Il faut seulement que les lieux y soient nommés, banalement, comme du décor qu'on traverse.*`
  ],
  ouvert: [`⚠️ **Ce qui le fait tiquer — proposition du 16 août 2026.** Le gamin avait décrit l'intérieur de cette maison. Debout devant la porte, Andrew perçoit la chose qu'il avait décrite — et comprend qu'elle est là.

Ce n'est pas un pressentiment, c'est un fait : Eliott a décrit une pièce où il n'avait aucune raison d'être entré. Ça suffit pour entrer sans attendre, et ça n'a besoin d'aucun autre argument.`,
           `**Et c'est la seule erreur de tri de tout le livre.** Le métier d'Andrew est de démêler ce qu'un jeune arrivant invente de ce qu'il a vu. Le gamin décrivait des lieux qui n'existent pas — un boulanger là où il y a un magasin de chaussures — alors quand il a décrit une cuisine, c'est parti au même endroit. *Il n'a pas manqué un indice caché : il a mal trié une phrase, une seule fois, et c'était celle-là.*`,
           `**Ce que ça donne pour la suite, sans qu'un mot l'explique :** si le gamin connaissait cet intérieur, c'est qu'une porte s'était déjà ouverte pour lui. *Un enfant qui ne trouve sa place nulle part avait un endroit où on le laissait entrer.* **Personne ne l'a emmené de force la première fois** — et c'est ce qui rend la suite bien pire.`,
           `⚠️ **Il reste à choisir le [X] — la chose que le gamin décrit.** Trois conditions : ça se dit en trois mots par un enfant ; c'est trop banal pour qu'on le note ; **et ça se perçoit depuis la rue au second passage.** *De préférence par l'oreille — alors Andrew comprend qu'il l'entendait déjà les trois fois d'avant, et « c'était là sous nos yeux » devient vrai une quatrième fois.* Un oiseau, une radio qu'on laisse allumée, un chien.`,
           `⛔ **Écarté : le nom.** *La coupable était nommée par le gamin, et Andrew ne l'avait pas entendu.* **La faute était plus cruelle — « il a eu le nom et il l'a laissé tomber par terre » — mais un nom prononcé ne dit pas que l'enfant est à l'intérieur.** *Une description d'intérieur, si.*`,
           `⛔ **Écarté : la voisine qui dit bonjour.** *Trop faible.* **On n'entre pas chez quelqu'un parce qu'il a salué un enfant dans la rue** — c'était un pressentiment déguisé en indice.`,
           `**Il ne peut pas avoir décrit la cave : il n'y était jamais allé.** *Ce qu'il décrit est une pièce ordinaire — celle où l'on fait entrer quelqu'un une fois, pour cinq minutes.*`],
  src: `04-plan/le-parcours-de-l-enquete.md §4, §4.3, §4 ter.4, §4 ter.6`
},
{
  id: `s18`, no: `Scène 18`, col: 27, row: `andrew`, acte: `La remontée`,
  face: `g-entre`,
  titre: `Il entre seul, sans attendre`,
  statut: `acquis`, pivot: true,
  resume: `Il a appelé, il sait que l'autre arrive, et il n'attend pas. Ce n'est pas du courage et ce n'est pas de l'imprudence : c'est exactement la faute d'avant refaite à l'envers. On lui a dit d'arrêter de creuser une fois, et il a obéi. Cette fois, personne ne l'arrête parce que personne n'est là.`,
  produit: `Le seuil. Fin de chapitre : l'air est lourd, il descend, et on referme.`,
  clef: `Ce n'est pas une planque, c'est une maison ordinaire, dans une rue, comme les autres. La porte qu'il ouvre donne sur une cave.`,
  monde: `Rien.`,
  qui: [`andrew`,`joel`],
  gardes: [`Les deux descentes ne se citent jamais. Le lecteur descend deux fois le même escalier et ouvre deux fois la même porte.`],
  double: `C'est le seuil que le lecteur franchit deux fois — et le seul endroit du livre où le procédé produit son effet par la différence et non par la ressemblance.`,
  src: `04-plan/le-parcours-de-l-enquete.md §2 — 04-plan/le-meme-jour.md §5 quater`
},

/* ---------- LE SEUIL FRANCHI DEUX FOIS ---------- */
{
  id: `corps`, no: `Chapitre B`, col: 28, row: `joel`, acte: `Le seuil franchi deux fois`,
  face: `s19a`,
  titre: `Les corps`,
  statut: `acquis`, pivot: true,
  resume: `On décrit un premier corps, et on croit que c'est le garçon. Puis un second, plus loin. Deux corps identiques, encore roses de l'afflux sanguin, mortes depuis moins d'une heure.`,
  produit: `Le trouble. Le lecteur peut se dire « la paire du début, qu'est-ce qu'elles font là ? » — c'est admis, c'est même souhaitable. Ce n'est pas encore la bascule : c'est une pièce de trop dans les mains, sans case où la ranger.`,
  clef: `Le chemin émotionnel est à trois temps là où les références en ont deux : l'angoisse (c'est peut-être lui), le soulagement (ce n'est pas lui), l'horreur (ce sont elles, et on ne savait même pas qu'on pouvait les perdre).`,
  monde: `Rien.`,
  qui: [`joel`,`liam`,`chrissy`],
  gardes: [
    `Ne pas couper la description. Elle doit durer, et elle doit être précise : c'est le carburant de l'espoir. Un corps abîmé à ce point n'est plus reconnaissable — plus la description avance, plus on peut se dire « ça ne lui ressemble pas ».`,
    `Aucun signe d'identité pendant la description. Rien qui nomme, rien qui prouve.`,
    `Faire réagir le témoin avant de montrer la preuve.`,
    `Finir court. Une phrase sans emphase, à la dernière ligne du chapitre. C'est le contraste de longueur qui frappe.`,
    `Le soulagement du temps 2 doit être réel, tenir une phrase ou deux, avant d'être retourné.`,
    `Les chapitres de la vie d'avant ne nomment personne : la phrase de chute ne peut pas porter de prénom. Elle devra tomber sur autre chose. Une heure. Une chaleur. Un fait.`
  ],
  clefFin: `On peut défigurer un visage. On ne peut pas défigurer une ressemblance. Ce qui clôt la scène n'est pas « c'est elle », mais que les deux corps sont les mêmes. La description peut être aussi atroce qu'on veut, l'espoir survivra tant que chaque corps est pris séparément — il meurt à la seconde où on les regarde ensemble.`,
  refs: [
    { t: `The Walking Dead — Carol et sa fille, la grange`, d: `La grange s'ouvre. On y a cherché quelqu'un pendant toute une saison. Ce qui en sort sort un par un, et on continue d'espérer jusqu'au dernier. Une paire de chaussures qu'on reconnaît, puis une démarche qui n'est plus humaine, puis une silhouette. Et le corps de celui qui regarde cède avant qu'on nous montre le visage.` },
    { t: `Franck Thilliez — « Il était deux fois », Gabriel et Julie`, d: `Tout un chapitre de description atroce. Le ressenti et le désespoir du personnage sont décrits avant la sentence : on croit encore à un soulagement. La phrase tombe à la toute fin, brève, presque administrative.` }
  ],
  refNote: `Ce qu'elles ont en commun : la scène porte le lecteur jusqu'au bout dans l'espoir que ce ne soit pas elle. L'espoir n'est pas retiré à l'avance — on n'a pas été préparé, on a été accompagné. Et la description longue et atroce est précisément ce qui le fait tenir : elle horrifie, et elle protège l'espoir.`,
  ouvert: [`L'espoir doit avoir été payé : la grange ne fonctionne que parce qu'on a cherché toute une saison. Il faut donc que la recherche ait du poids avant.`],
  src: `07-recherches/references-de-scenes.md — 04-plan/le-meme-jour.md`
},
{
  id: `s19a`, no: `Chapitre C`, col: 29, row: `andrew`, acte: `Le seuil franchi deux fois`,
  face: `corps`,
  titre: `Le même lieu, l'autre issue`,
  statut: `acquis`, pivot: true,
  resume: `Le chapitre recommence. Même arrivée, même pesanteur — et Eliott est vivant. Isaac les rejoint. **Andrew sent pourtant une présence derrière eux. Une silhouette apparaît. Fin de chapitre.**`,
  produit: `C'est la bascule du roman. Le lecteur comprend qu'il y a deux histoires — et il ne la reçoit ni d'une phrase ni d'un personnage : **il la reçoit de la forme du livre, qui se dédouble sous ses yeux.**`,
  clef: `🔴 **Et le chapitre se ferme sur la silhouette, ce qui arme tout le reste.** Le lecteur y voit le ravisseur pris sur le fait, et il attend la course. *Il l'aura — mais pas dans ce monde-ci.*`,
  lecture: `Il croit lire la fin d'une traque. Il lit la fin de deux traques, et une seule des deux va se terminer par une course.`,
  monde: `La cave réaménagée : elle a peint, elle a meublé, elle a choisi. Ce n'est pas de la négligence retournée en gentillesse — **c'est de la préparation.** Du temps, des courses, des décisions prises une par une, des semaines avant. Ça dit qu'elle comptait rester.`,
  qui: [`andrew`,`eliott`,`isaac`,`berceuse`],
  gardes: [
    `**La silhouette n'est décrite par rien.** Ni vêtement, ni taille, ni âge, ni sexe. *Le mot « silhouette » est féminin en français, ce qui protège gratuitement les deux lectures : on peut écrire « la silhouette » des deux côtés sans qu'un accord trahisse quoi que ce soit.*`,
    `**Rien ne dit qu'elle bouge.** Elle apparaît, et le chapitre s'arrête. C'est le lecteur qui la fera courir.`,
    `« Une chambre d'enfant » ne peut pas s'écrire, et aucune tournure de remplacement ne doit venir la doubler. Il faudra décrire les couleurs, la taille des meubles, une hauteur de table, un lit court. **Le lecteur nommera lui-même, et ça frappera plus fort.**`,
    `Aucun personnage ne remarque le contraste avec l'autre cave.`
  ],
  ouvert: [`Combien de lignes tient la silhouette avant la coupe. *Trop, et on la décrit ; trop peu, et le lecteur ne la charge pas assez pour vouloir la poursuivre.*`],
  src: `04-plan/le-parcours-de-l-enquete.md §2, §4 ter.5 — décision du 16 août 2026`
},
{
  id: `poursuite`, no: `Chapitre D`, col: 30, row: `joel`, acte: `Le seuil franchi deux fois`,
  face: `s19c`,
  titre: `La poursuite`,
  statut: `acquis`, pivot: true,
  resume: `**La silhouette prend la fuite.** Sans réfléchir, il s'élance. Une rage, la colère, l'envie de tuer. « Joël, attends ! » La poursuite en voiture, l'accident. Il meurt en même temps que l'assassin.`,
  produit: `🔴 **Le cri tombe désormais au milieu d'une course que le lecteur a entièrement investie comme celle d'Andrew.** Il vient de voir la silhouette apparaître dans la cave d'ici ; il lit la suite. *Le nom ne révèle pas le dispositif : il révèle l'identité, et il arrive quand le lecteur est le moins capable de s'en défendre.*`,
  clef: `**Le nom arrive attaché à un refus d'obéir.** La seule fois du roman où l'on entend son nom est la seule fois où quelqu'un essaie de l'arrêter et où il n'écoute pas. Son partenaire crie *attends* — le mot exact auquel il a cédé des semaines plus tôt, et qui est toute sa faute. **Son identité et sa faute sont données dans le même souffle, et en miroir.**`,
  lecture: `Il croit qu'Andrew court après la ravisseuse. **Personne ne court, de ce côté-ci** — et il l'apprendra au chapitre suivant, sans qu'une ligne le lui dise.`,
  monde: `Rien.`,
  qui: [`joel`,`liam`],
  gardes: [
    `✅ **Ils meurent tous les deux dans le carambolage — l'autrice, 17 août 2026.** *Le tueur emboutit quelqu'un, Joël emboutit le tueur.* **En face il y a un poids lourd, qui ne bouge presque pas.** La voiture du tueur s'encastre dedans, celle de Joël suit bêtement. *Le tueur se retrouve pris en sandwich entre le camion et la voiture de police, et Joël fait un choc frontal en rentrant dans la sienne.*`,
    `⛔ **Deux morts, deux capsules, et c'est de là que tout part.** *Une mort brutale ne laisse aucun délai de maturation :* **les deux capsules arrivent le jour même.** Celle de Joël éclaircira — et deviendra Andrew. **Celle du tueur n'éclaircira pas.**`,
    `**Le chauffeur du poids lourd n'a presque pas bougé.** *Il n'y a donc pas de troisième capsule*, et rien à expliquer de ce côté-là.`,
    `**Le chapitre s'ouvre sur la fuite, pas sur un lieu.** Aucune reprise du décor de la cave, aucun raccord visuel avec le chapitre précédent : c'est le lecteur qui raccorde, et s'il est aidé, il voit la couture.`,
    `Un nom donné par le narrateur est une information ; un nom crié par un personnage est du bruit. **Le narrateur ne le prononce jamais, pas même là.**`,
    `Le mot « attends » n'est ni répété, ni souligné, ni mis en italique.`,
    `Il ne meurt pas en sauvant quelqu'un. Sa poursuite ne sert à rien, personne ne la lui demande, aucun personnage ne commente sa mort.`,
    `Il ne veut pas l'arrêter, il veut le tuer — comme si les deux filles avaient pu être les siennes. **C'est la seule fois du livre où il n'est plus lui-même.**`
  ],
  phrases: [{ t: `Joël, attends !`, n: `Crié par son collègue. **Unique occurrence de son nom dans tout le roman**, et le dernier endroit possible du livre : le dispositif tient sur la totalité du volume, pas sur les neuf dixièmes.` }],
  src: `04-plan/deux-histoires-en-une.md §2.2, §2.2.2, §2.2.3 — décision du 16 août 2026`
},
{
  id: `s19c`, no: `Chapitre E`, col: 31, row: `andrew`, acte: `Le seuil franchi deux fois`,
  face: `poursuite`,
  titre: `Elle n'a pas fui`,
  statut: `acquis`, pivot: true,
  resume: `On revient chez Andrew. **Il réalise sa propre mort.** Il observe, dubitatif, la berceuse qui a compris qu'elle était prise sur le fait. **Elle n'a pas tenté de s'enfuir.** Elle semblait juste profondément triste. **Elle tritura son collier, hésitante, avant d'enfin tendre ses deux mains en avant pour le passage des menottes.**`,
  produit: `🔴 **Et le lecteur comprend, sans qu'une ligne le lui dise, que personne n'a couru de ce côté-ci.** La course qu'il vient de lire n'appartenait pas à cette cave. *Il n'a pas été trompé : on ne lui a jamais dit que la silhouette fuyait — il l'a supposé.*`,
  clef: `**Elle n'a pas fui, et c'est ce qui la referme.** Elle ne voulait pas le tuer, elle voulait le garder ; on ne fuit pas quand on n'a nulle part où aller et rien à sauver. *Sa tristesse n'est pas du remords : c'est la fin de la seule chose qu'elle avait.*`,
  lecture: `Deux images se superposent chez lui pour toujours : un homme qui court et meurt, et une femme qui ne bouge pas. **Il n'aura jamais les mots pour dire que c'est la même seconde.**`,
  monde: `Rien de neuf. C'est le premier endroit du livre où le reliquat frappe en pleine scène, et personne ne le remarque.`,
  qui: [`andrew`,`berceuse`,`isaac`,`eliott`],
  gardes: [
    `**Il ne comprend rien.** Il voit sa propre mort et il n'a aucun nom pour ça — pas de « c'était lui », pas de « il se reconnut ». Le corps sait, pas lui.`,
    `**Il n'apprend jamais qu'il s'est appelé Joël.** Le nom n'existe que pour le lecteur.`,
    `Elle ne s'explique pas, personne ne formule son motif à sa place, et le livre n'a pas de scène qui rende son geste intelligible.`,
    `**Elle ne doit jamais s'écrire comme une démente qu'on range et qu'on oublie.** Sa tristesse est celle de quelqu'un à qui on reprend quelque chose, et elle ne se commente pas.`,
    `Aucun personnage ne rapproche jamais sa présence ancienne et son arrestation. Pas de « elle était là depuis le début ».`,
    `🔴 **Le collier est la seule chose qui relie les deux scènes, et personne ne le relève.** *C'est le lecteur qui l'a vu bercer à son rythme, six cents pages plus tôt.* **Il ne doit être ni nommé comme un signe, ni décrit deux fois de la même façon.**`
  ],
  ouvert: [`Ce qu'elle dit, ou ne dit pas, au moment de l'arrestation. *Le silence est la version la plus dure ; une seule phrase est la plus risquée.*`,
           `Le livre lui donne-t-il un nom ? Trois canaux possibles, et il n'en faut qu'un.`,
           `⚠️ **Ce qu'Andrew fait de sa stupeur dans les pages qui suivent.** Il vient de voir mourir un homme qui était lui ; le livre ne peut ni l'expliquer ni l'ignorer. *C'est la seule zone du dénouement qui reste à régler.*`],
  src: `04-plan/le-parcours-de-l-enquete.md §2 — 03-personnages/la-berceuse.md — décision du 16 août 2026`
},
{
  id: `ceremonie3`, no: `Chapitre F`, col: 32, row: `andrew`, acte: `Le seuil franchi deux fois`,
  titre: `La cérémonie, une seconde fois`,
  statut: `acquis`, pivot: true,
  resume: `🔴 **Elle ne redécrit rien.** *Décision de l'autrice, 16 août 2026 : ce chapitre ne rejoue pas la cérémonie — il donne uniquement ce qu'Andrew avait omis.* **Ce qu'il croyait ne pas avoir entendu :** la phrase d'ouverture en entier — *« la cérémonie du jour nous offre trois arrivants au lieu de deux ; le troisième nous ayant surpris par son éclaircissement inopiné ».* **Et ce qu'il croyait ne pas avoir senti :** l'odeur, dans les mots exacts du chapitre de la capsule pourrie — **et la réplique qui dit d'où elle venait.** *Un veilleur était entré avec sa tenue de travail, il venait de nettoyer une capsule qui n'avait pas éclairci, et quelqu'un le lui a fait remarquer :* « tu aurais pu enfiler une autre tenue, quand même. » **Personne ne s'en est offusqué, la cérémonie a continué, et un homme de vingt ans plus jeune ne l'a même pas entendu.**`,
  produit: `🔴 **C'est son défaut qui se rejoue une dernière fois, et c'est la seule fois où le lecteur le voit se produire en direct.** L'information était dans sa tête depuis dix ans. Il ne l'a pas manquée : **il ne l'a pas écoutée** — exactement comme il n'a pas écouté un arrivant de dix ans qui lui parlait.`,
  clef: `**Et ce n'est pas une tricherie, parce que le monde a déjà expliqué pourquoi il n'entendait pas.** Un arrivant sort embrumé, aveuglé, les voix lui parviennent étouffées : *le premier récit montrait déjà une bouche qui bougeait sans qu'il attrape les mots.* **Le texte n'a rien caché — il a rendu une perception, et elle était fidèle.**`,
  lecture: `Il ne reçoit aucun fait nouveau : il reçoit un fait ancien, à sa place. *Et il peut relire les deux versions et vérifier que la seconde ne contient rien que la première ait escamoté.*`,
  monde: `🔴 **Et c'est ici qu'on comprend ce qu'est une capsule qui n'éclaircit pas.** *Décision de l'autrice, 16 août 2026 : la chose n'a pas de scène à elle — elle se noie dans ce second récit.* Le lecteur avait entendu parler d'une odeur, au loin ; il sait maintenant ce qu'il y avait au bout de l'allée, et pourquoi on raclait pendant que les autres se nommaient. **Personne ne le lui dit : il le pose lui-même.**

**Deux autres choses, et aucune n'est expliquée.** Les capsules de la paire étaient attendues ; la sienne, non. *Une vie qui s'éteint lentement fait mûrir lentement ; une mort soudaine fait mûrir vite.* Et l'odeur, au loin : un veilleur s'occupait des arrivants pendant qu'un autre raclait, pour que l'infamie de la quatrième capsule n'entrave pas la cérémonie.`,
  qui: [`andrew`,`chrissy`],
  gardes: [
    `🔴 **Le chapitre se ferme sur l'odeur, et c'est sa dernière ligne.** *Structure donnée par l'autrice, 17 août 2026 :* la réplique — « tu aurais pu changer de tenue ! » — **puis « et là il la remarqua, cette odeur, insipide et prenante au nez, comme si… »** *et la formule reprise mot pour mot.* **Le lecteur ne peut que s'en souvenir : elle n'existe qu'à deux endroits dans tout le livre.**`,
    `**Le premier récit doit montrer qu'il n'entend pas.** Des voix étouffées, une bouche qui bouge, des mots qui ne se forment pas. *Sans ça, la seconde version ressemble à une information qu'on avait gardée sous le coude ; avec ça, elle est un blanc que le lecteur avait sous les yeux.*`,
    `**Personne ne commente.** Il ne dit pas « je me souviens maintenant », le narrateur ne signale pas que la version a changé, et aucune phrase ne rapproche les deux récits.`,
    `🔴 **Ne rien reprendre de ce que le premier récit a déjà donné.** Ni la salle, ni la paire, ni le froid, ni le nom qu'on lui demande. *Le chapitre est court parce qu'il ne contient que deux choses — et c'est sa brièveté qui dit, sans un mot, qu'on n'y cherche plus la même chose.*`,
    `Il ne comprend toujours rien. Il a un fait de plus et pas une conclusion.`,
    `**L'odeur reste une odeur.** Personne ne dit ce qui la produisait, et surtout pas lui.`
  ],
  phrases: [
    { t: `Bienvenue à tous.`, n: `Ouverture du premier récit, et tout ce qu'il en attrape.` },
    { t: `Bienvenue à tous. La cérémonie du jour nous offre trois arrivants au lieu de deux, le troisième nous ayant surpris par son éclaircissement inopiné.`, n: `**La même phrase, entendue en entier.** Formulation de l'autrice. *Elle dit, sans que personne puisse le lire ainsi, que deux morts étaient prévisibles et qu'une ne l'était pas.*` },
    { t: `Quel sera ton prénom ? Comment veux-tu qu'on t'appelle pour te désigner ?`, n: `Formulation de l'autrice, identique dans les deux récits — c'est elle qui prouve au lecteur que c'est bien la même scène.` }
  ],
  pourquoi: [
    `**Le souvenir vient avant le registre, et il le motive.** Un homme qu'un reliquat vient de frapper ne va pas d'abord aux archives : quelque chose remonte, et c'est ce quelque chose qui l'envoie vérifier. *Le dossier cherchait depuis longtemps une raison qu'Andrew ait d'aller au registre. Elle est là, et elle arrive à la fin.*`,
    `**Le souvenir n'établit rien, le registre établit tout.** L'un rouvre, l'autre prouve. Les intervertir donnerait une preuve avant une question, et il ne resterait plus qu'à commenter.`,
    `**Et le doute vit un chapitre de plus.** Un souvenir ne se vérifie pas ; l'hypothèse « il fabule » sort de cette scène aussi solide qu'elle y est entrée.`
  ],
  ouvert: [`✅ **Les deux autres étaient attendues — décision de l'autrice, et la déduction est donc voulue.** Leur vie s'est éteinte lentement quand la sienne s'est arrêtée net : *elles ont agonisé pendant que Joël les cherchait, et la ruche faisait mûrir leurs capsules pendant ce temps-là.* **Personne dans le livre ne peut le formuler ; le lecteur a la règle depuis le premier chapitre.** À l'écriture : ne jamais appuyer. Le mot *inopiné* suffit, et le contraste se fait tout seul.`,
           `La longueur du second récit. *Plus bref que le premier — c'est ce qui signale, sans un mot, qu'on n'y cherche plus la même chose.*`,
           `⚠️ **Ce que devient la scène révulsante du dossier maître.** Le §8 demandait une description crue d'une capsule sans éclaircie, faite pour dégoûter avant qu'on ait à juger. *En noyant la chose ici, la compréhension devient froide et rétrospective — ce qui est plus juste, mais la révulsion n'a plus de logement.* **À trancher : on l'abandonne, ou elle se replace ailleurs, tôt, dans une journée de service ordinaire.**`],
  src: `04-plan/deux-histoires-en-une.md §7 — 02-univers/la-ruche.md — décision du 16 août 2026`
},
{
  id: `registre-fin`, no: `Temps 5`, col: 33, row: `andrew`, acte: `Le seuil franchi deux fois`,
  titre: `La ligne de registre`,
  statut: `acquis`,
  resume: `🔴 **Il ne vient pas vérifier un détail : il vient vérifier sa propre mort.** *Il a réalisé, au chapitre précédent, que la silhouette n'avait pas bougé — et donc qu'il avait vu comment il était mort.* Il entre dans la salle du registre, seul, et il cherche le jour de son arrivée. **Il trouve sa ligne, et celle de la paire à côté.** *Puis il se demande si l'autre s'en est tiré* — et un souvenir de vingt ans lui répond.`,
  produit: `La ligne ne révèle rien de neuf : elle confirme, et elle confirme par un document. C'est le bon ordre — **le lecteur devine, puis on lui prouve.** Il ne découvre rien, il vérifie. *Et la scène cesse d'être gratuite : le chapitre précédent lui a donné une raison d'ouvrir le registre.*`,
  clef: `Il a déjà vu la figure une fois, propre, gratuite, sans conséquence, à la scène 8 : deux arrivées le même jour signifient une seule mort. Il sait ce qu'elle veut dire avant qu'on la lui remontre.`,
  monde: `Le numéro, qu'il faut avoir fait passer plusieurs fois sous les yeux du lecteur avant, en n'ayant jamais rien voulu dire — un comptoir, un formulaire, une convocation.`,
  qui: [`andrew`],
  gardes: [
    `✅ **Pourquoi il y va, et l'autrice l'a corrigé le 17 août 2026 : il sait comment il est mort.** *Au chapitre de la poursuite, le lecteur voit le carambolage. Au chapitre suivant, Andrew réalise que la silhouette n'a pas bougé* — **et il comprend qu'il a vu sa propre mort.** C'est ça qui l'amène ici, et pas un détail de cérémonie.`,
    `✅ **Et c'est en vérifiant qu'il se pose la vraie question : est-ce que cette enflure a pu s'échapper ?** *Il a la stèle sous les yeux, il a sa ligne, il a celle de la paire à côté — et il n'y a rien pour l'autre.* **Alors l'intuition vient, et elle vient d'un souvenir de vingt ans :** un veilleur entré en tenue de travail, et quelqu'un qui lui dit *« tu aurais pu enfiler une autre tenue, quand même ».*
  **Il connecte. Il sait que l'autre n'est jamais arrivé.**`,
    `🔴 **Il a tout compris à sa propre mort — correction de l'autrice, 17 août 2026.** *Ce n'est pas un fait qu'il attrape, c'est sa vie.* **Il s'appelait Joël.** Il a ressenti dans son reliquat cette colère aveuglante, il a senti qu'il aurait pu tuer pour ces deux filles. **Il sait tout de sa ligne.**`,
    `✅ **Et les reliquats lui viennent ici par flashs, en surimpression.** *Deux images données par l'autrice, à garder :* **le visage de June qui disparaît au moment où elle lui dit qu'Eliott a disparu, remplacé par celui d'une parfaite inconnue qui dit qu'elle s'inquiète.** Et **son regard qui se pose sur la photo d'identité d'Eliott dans un dossier — dédoublée, et devant une photo de famille des deux jumelles.**`,
    `**C'est le faux-raccord rendu littéral, une seule fois, à la fin.** *Tout le livre a superposé deux vies sans le montrer ; ici la superposition se voit* — et elle se voit dans la tête d'un seul homme, dans une pièce où personne n'entre.`,
    `⛔ **Ce qu'il n'a pas, et qu'il n'aura pas ici : l'homme d'à côté à la cérémonie d'Eliott.** *Cette réponse-là, c'est Eliott qui la lui apportera, six ans plus tard, et sans savoir ce qu'il donne.*`,
    `⛔ **Rien de tout ça ne s'écrit en clair.** *Pas de récapitulatif, pas de phrase qui pose la conclusion, pas de narrateur qui confirme.* **Des images qui se remplacent, et un homme debout devant une stèle.**`,
    `Le registre est infaillible. C'est une lecture, pas une hypothèse.`,
    `Trop peu de numéros semés avant, et la reconnaissance ne repose sur rien ; trop appuyé, on annonce la scène.`,
    `Il n'apprend jamais qu'il s'est appelé Joël. Le nom d'avant n'existe que pour le lecteur.`
  ],
  ouvert: [`Le nombre exact d'occurrences du numéro avant cette scène, et sa forme.`],
  pourquoi: [`**Et on s'arrête là. Ellipse.** Le registre confirme son souvenir, et le chapitre se ferme sans qu'il en tire quoi que ce soit. *L'arc d'Andrew se termine ici — tout ce qui suit appartient au garçon.*`,
    `**C'est plus subtil que de lui donner une quête.** Une scène où il irait chercher des réponses ferait de la dernière page son affaire à lui ; l'ellipse le laisse avec ce qu'il a, c'est-à-dire rien. **Il lui reste deux choses à faire, et aucune des deux n'est pour lui.**`],
  src: `04-plan/deux-histoires-en-une.md §1 bis, §2.6 — 04-plan/le-meme-jour.md §3, §3 bis`
},

/* ---------- ÉPILOGUE ---------- */
{
  id: `excuses`, no: `Épilogue`, col: 34, row: `andrew`, acte: `Épilogue`,
  titre: `Les excuses`,
  statut: `acquis`,
  resume: `Il pousse leur porte un après-midi ordinaire. Deux arrivantes d'une quinzaine d'années qui ne le connaissent pas. Elles ont presque l'âge des corps qu'il a trouvés — trois ans d'écart, rien de plus. Il s'excuse pour un monde dont elles n'ont aucun souvenir.`,
  produit: `Il n'obtient ni absolution ni incompréhension : il obtient de la politesse. La culpabilité de ne pas avoir été capable de les retrouver à temps, et le soulagement de voir que l'équilibre leur a offert une seconde chance — et rien de tout cela ne peut se dire.`,
  monde: `À quinze ans elles ont tous les mots, elles répondent, elles comprennent. Quand il prononce un des deux noms, une seule se retourne.`,
  qui: [`andrew`,`chrissy`],
  gardes: [
    `La scène ne commente rien, ne compare pas, ne rappelle pas le chiffre.`,
    `Leurs prénoms de la vie d'avant ne sont jamais donnés — ni au lecteur, ni à un personnage, ni au dossier. C'est un blanc et il reste blanc.`,
    `« Jumelles » et « sœurs » sont réservés à la vie d'avant, jamais dans une scène d'ici.`
  ],
  src: `03-personnages/chrissy-et-tania.md`
},
{
  id: `confession`, no: `Épilogue · 2 sur 2`, col: 36, row: `andrew`, acte: `Épilogue`,
  titre: `En tête à tête`,
  statut: `acquis`, pivot: true,
  resume: `June vient de partir. **Un blanc — on ne sait pas qui va parler le premier, et c'est le garçon.** Il le remercie de son aide, puis plus largement : *de l'avoir cru.* Et parce qu'il sait qu'avec celui-là on ne se moquera pas, il raconte une dernière chose.`,
  produit: `**L'arc d'Andrew s'est terminé au chapitre du registre. Celui-ci n'a plus qu'un objectif : rassurer Eliott.** *Il s'apprête à entrer dans un lieu d'innocence, et c'est le meilleur qui pouvait lui arriver.* **Rien n'est une révélation — le lecteur sait déjà tout.** Ce qu'il reçoit ici, ce n'est pas une information, c'est une phrase.`,
  clef: `**C'est parce qu'il a été cru qu'il parle.** *Il réalise qu'Andrew a toujours été de son côté, et c'est ça qui le décide* — pas une confiance générale, mais le souvenir précis d'un homme qui ne s'est jamais moqué. **Le seul cadeau que ce livre fasse à quelqu'un, c'est celui-là, et il arrive à la dernière page.**`,
  clefFin: `**Sa fin dans l'autre monde est irrévocablement triste, à en pleurer. Mais l'amour reste.** *C'est tout le contraste que la scène doit tenir : le récit est atroce et le garçon va bien.*`,
  garde_forme: `**Il n'énonce rien : il décrit des sensations qu'il n'arrive pas à formuler.** *Il n'a ni le mot rivière avant l'école, ni le mot noyade, ni le mot père — il a des impressions et il les rend telles quelles.* **Et ce ne sont pas que celles de l'accident** : il y a aussi une odeur, un regard plein d'amour. *Une vie ne se souvient pas d'une seule minute.*

**Le déroulé.** ① le blanc, et c'est lui qui le rompt ; ② il remercie — de l'avoir cru ; ③ *« tu n'as jamais eu cette impression, toi, de rêver en plein jour ? »* ; ④ les fragments, dans le désordre, sans hiérarchie ; ⑤ **ses deux questions**, qui sont les vraies ; ⑥ ce qu'Andrew trouve à répondre.`,
  lecture: `Il a devant lui quelqu'un d'enthousiaste qui va vivre heureux, et il vient d'entendre comment il est mort. **Les deux sont vrais en même temps, et c'est la seule chose que le livre demande de tenir dans la main en le refermant.**`,
  monde: `La parole est intacte à huit ans. Et la dernière grâce, qui ne doit jamais être confirmée : on suppose que les reliquats s'en vont une fois au jardin, et *ça se dit comme on parle des fantômes.*`,
  qui: [`eliott`,`andrew`],
  gardes: [
    `**Personne ne traduit, personne ne commente, personne n'a l'air de comprendre.** Pas de narrateur qui éclaire, pas d'interlocuteur qui hoche la tête, pas de silence appuyé, pas de phrase juste après qui pèse.`,
    `**Il ne dira jamais « papa » ni « père ».** Les mots n'existent pas, il ne les a jamais eus, et il ne peut donc pas même sentir qu'ils lui manquent.`,
    `**Andrew ne fait jamais le lien** avec la ligne du registre, et il ne va jamais vérifier qui d'autre est arrivé le jour du garçon.`,
    `**Aucun mot ne doit être plus grand que lui.** Il a huit ans, il a du vocabulaire d'école, et il bute. *Ce qui glace, c'est qu'il raconte ça calmement, comme une chose finie, sans se plaindre et sans chercher à émouvoir.*`,
    `⚠️ **Les fragments ne sont pas tous noirs.** *Il se rappelle une odeur, un regard plein d'amour.* **Sinon la scène devient un récit d'accident, et ce n'en est pas un : c'est ce qui reste d'une vie entière.**`,
    `Un seul personnage qui aurait l'air de saisir, et la réplique cesse d'être une trouvaille pour devenir un aveu.`,
    `⛔ **Aucune résonance chez Andrew, et surtout pas une paix.** *Son arc s'est fermé au chapitre du registre — décision de l'autrice, 16 août 2026 : la scène d'avant sert déjà à ça, et le refaire ici la doublerait.* **Il donne un exemple à un gamin, ça ne lui coûte rien et ça ne lui rend rien.** *S'il était ému par ce qu'il vient de dire, il serait un homme qui sait à moitié — et c'est le lecteur, pas lui, qui doit recevoir la phrase.*`
  ],
  phrases: [
    { t: `Tu n'as jamais eu cette impression, toi ? De rêver en plein jour ?`, n: `**L'ouverture, et c'est une question, pas une confidence.** *Formulation de l'autrice.* Il ne dit pas « je vais te raconter » : il demande si l'autre connaît ça, comme on vérifie qu'on ne va pas être seul.` },
    { t: `J'ai senti le sol se dérober sous mes pieds alors que je ne bougeais même pas.`, n: `*Formulation de l'autrice, à retravailler.* Une sensation sans son objet : il n'a pas le mot pour ce qui l'a emporté.` },
    { t: `J'avais les yeux ouverts et je pouvais sentir l'eau dans ma bouche.`, n: `*Formulation de l'autrice, à retravailler.* **Aucun mot de noyade, jamais.**` },
    { t: `Je n'ai jamais vu de rivière. Je ne savais même pas ce que c'était, un courant, avant de l'apprendre à l'école. Et pourtant j'ai rêvé que je tombais dedans.`, n: `**La pièce maîtresse : il constate lui-même que ça n'a aucun sens.** *Formulation de l'autrice.* C'est ce qui rend la fabulation invérifiable et bouleversante à la fois — **il donne l'argument contre lui-même**, et l'interdit n° 4 tient sans effort.` },
    { t: `L'arrivant qui était à côté de moi à ma cérémonie, j'ai rêvé de lui aussi. Il me tendait la main et je n'arrivais pas à l'attraper. Nos mains glissaient trop.`, n: `**Et c'est l'homme de la première page.** *Formulation de l'autrice.* Le lecteur se souvient de celui qui était debout à côté du petit, et il restera seul avec.` },
    { t: `Je ne sais pas pourquoi, mais j'avais très peur. Autant pour moi que pour lui, alors que je ne le connaissais même pas.`, n: `*Formulation de l'autrice.* **Il avait peur pour quelqu'un qu'il ne connaissait pas** — et c'est la seule façon de dire « mon père » quand le mot n'existe pas.` },
    { t: `Il m'aimait beaucoup, un sentiment fort, très fort. J'avais l'impression qu'il était moi et que moi j'étais lui. Comme si je l'aimais encore plus fort que lui !`, n: `**La phrase qui ferme les fragments.** Il a le sentiment entier et il n'a pas le nom, alors il le décrit par l'identité et par la confusion des deux personnes — *c'est exactement ainsi qu'on décrirait un père si l'on n'avait jamais eu le concept.* Elle ne coûte rien à l'interdit n° 4 : un sentiment ne se confirme ni ne se réfute.` },
    { t: `Et maintenant, je fais quoi avec ça ? Tu crois que les autres vont se moquer de moi ici aussi ?`, n: `⚠️ **La vraie question du livre, posée par un enfant de huit ans à la dernière page.** *Que faire des voiles ?* **Personne n'y a jamais répondu, ni le dossier ni le monde** — et c'est un gamin qui pose la question, à quelqu'un qui n'a pas la réponse.` },
    { t: `Est-ce que tu viendras me voir, au jardin ?`, n: `**Et c'est celle-là qui compte pour lui.** *Elle est petite, et elle est la seule à laquelle Andrew peut répondre oui.*` },
    { t: `J'ai connu quelqu'un qui se posait beaucoup de questions, lui aussi.`, n: `⚠️ **La réponse d'Andrew, et elle n'est pas une réponse.** *Il ne sait pas quoi faire des voiles — personne ne le sait — alors il donne un exemple au lieu d'une solution.* **Il parle sincèrement de quelqu'un qu'il croit avoir connu.** Les mots exacts restent à trouver ; ce qu'ils doivent porter : *c'était survivable.*` },
    { t: `— Il s'appelait comment ?`, n: `⛔ **Et la question reste sans réponse. Décision de l'autrice, 16 août 2026 : le prénom ne revient pas sur la table.** *Le seul nom que le livre n'a jamais dit est demandé à voix haute, par un enfant, à la dernière page — et rien ne vient.*

**Ce qui vient à la place, c'est la réponse à l'autre question :** oui, il viendra le voir au jardin. *Le garçon prend la réponse qu'il voulait, et personne ne s'aperçoit du trou.* **C'est le lecteur qui met le nom, comme il a mis tout le reste depuis six cents pages.**` }
  ],
  pourquoi: [
    `✅ **Le prénom ne se dit pas — décision de l'autrice, 16 août 2026.** *Il y fait référence sans le savoir, et ça ne lui fait rien.* **Il parle sincèrement de quelqu'un qu'il croit avoir connu**, il ne ment pas et il ne confesse rien : il console un enfant avec sa propre vie racontée comme celle d'un autre. *C'est le dernier faux-raccord du livre, et le seul qu'un personnage produise à voix haute sans le percevoir.*`,
    `⛔ **Écarté : « il s'appelait Joël ».** *Prononcé, le nom confirme* — même dit par quelqu'un qui ne sait pas ce qu'il dit. **Le livre n'a jamais rien confirmé en six cents pages ; il ne va pas commencer à la dernière ligne.** *Et la question posée sans réponse est plus forte que la réponse : c'est le seul nom que le livre n'a jamais dit, demandé à voix haute par un enfant, et rien ne vient.*`,
    `⛔ **Et surtout, s'il sait qu'il parle de lui, la fin s'écroule.** *Il devient un homme qui savait, sa culpabilité cesse d'être tragique pour devenir délibérée*, et « il ne peut pas le savoir » — qui tenait tout le dernier tiers — devient faux rétroactivement.`,
    `**Ça explique enfin pourquoi il l'a cru.** *Non pas parce qu'il sait qu'il est un porteur de voiles* — il ne le sait pas, il n'a jamais nommé la chose — **mais parce que quelque chose en lui a reconnu ça sans pouvoir le dire.** Il n'a jamais traité une seule de ses visites comme une audition, et le livre n'a jamais expliqué pourquoi.`,
    `**Et ça se raccorde à la seconde cérémonie**, où il retrouve ce qu'il croyait ne pas avoir entendu et ce qu'il croyait ne pas avoir senti. *Il a déjà des fragments qu'il ne sait pas ranger. Un prénom en est un de plus.*`
  ],
    ouvert: [`✅ **Le livre se ferme sur trois phrases après la réplique du garçon — validé le 17 août 2026.** *Ils passent la grille, on la tire derrière eux ; les cris continuent exactement comme avant ; le banc n'est plus froid.* **La dernière note passe du garçon à Andrew, et c'est voulu :** la tristesse doit aller quelque part et elle n'a pas le droit d'aller sur Eliott.`,
           `✅ **La question des voiles ne reçoit pas de réponse.** *« Et maintenant je fais quoi avec ça ? »* — **Andrew n'en a pas, et c'est ce qu'il faut :** il ne répond pas à la question, il répond à l'enfant. *Un exemple au lieu d'une solution — et ça s'arrête là : il n'en tire rien pour lui.*`,
           `Andrew réagit-il visiblement ? *Le moins possible, et probablement rien du tout.*`,
           `Combien de répliques autour de la phrase acquise. **Elle doit être la dernière, donc rien après.**`],
  src: `01-dossier/les-interdits.md n° 11 — 01-dossier/phrases-a-garder.md`
},
{
  id: `jardin-fin`, no: `Épilogue · 1 sur 2`, col: 35, row: `andrew`, acte: `Épilogue`,
  titre: `L'entrée au jardin`,
  statut: `acquis`, pivot: true,
  resume: `**Une rentrée scolaire, et c'est exactement le registre.** De petits groupes attendent sur l'allée, près d'une grille, chacun avec son berceur. Les petits se regardent, certains ont déjà un copain, d'autres ne lâchent pas une jupe ; les adultes échangent des banalités. Puis la grille s'ouvre.`,
  produit: `✅ **Les deux cartes de l'épilogue ne font qu'un seul chapitre — décision de l'autrice, 16 août 2026.** *Écrit, et lisible dans l'onglet Chapitres.* Elles restent séparées ici parce que ce sont deux beats distincts à suivre, mais le texte ne se coupe pas entre les deux : on passe de la grille au banc sans blanc.

**Le lecteur ne doit pas se sentir triste du sort d'Eliott.** *Il va vivre heureux au jardin, et il est même très enthousiaste.* Il dépose ce qui le faisait souffrir et il entre dans l'insouciance : **c'est une fin qui n'est pas une mort.** Le registre de la rentrée le garantit tout seul — on ne pleure pas à une rentrée, on a le ventre serré et on y va.`,
  clef: `**Et c'est le seul rite du livre qu'on n'a pas encore vu.** Le roman ouvre sur une arrivée à la ruche et se ferme sur une arrivée au jardin : *le même geste aux deux bouts d'une vie, et le lecteur reçoit le second en sachant tout ce que le premier ne disait pas.*`,
  garde_forme: `**Le déroulé, tel que l'autrice l'a posé.** ① l'allée le long de l'enceinte, des groupes disséminés près d'une grille ; ② l'attente — la curiosité entre petits, les banalités entre adultes ; ③ **Andrew est déjà là et regarde de loin** ; ④ June l'aperçoit et l'invite à les rejoindre ; ⑤ la grille s'ouvre, le responsable de zone sort avec ses berceurs, les autres commencent à entrer ; ⑥ **June demande à celle qui lui succède quelques instants avant qu'on referme, et on les lui accorde** ; ⑦ ses adieux ; ⑧ elle salue Andrew et s'en va.

*C'est cette permission demandée à la ⑥ qui rend possible tout le chapitre suivant : les deux restent dehors, sur l'allée, pendant que le reste du monde est déjà entré.*`,
  garde_bis: `**Les adieux de June sont professionnels, et l'émotion se sent quand même.** *Le pincement au cœur d'une assistante maternelle qui voit partir le petit qu'elle gardait* — elle ne pleure pas, elle ne s'attarde pas, mais ce n'est pas une formalité de service. **C'est la fin d'une durée**, et c'est le premier des deux adieux d'une vie ; le second, celui de zéro, appartiendra à la femme à qui elle passe la main.`,
  monde: `**Le seul endroit du livre où l'on voit le jardin comme institution.** L'enceinte crème vue de la ville, l'allée-parc qui la longe, les grilles multiples — et de l'autre côté une seconde ville dont on n'apercevra rien dans ce chapitre, parce qu'on reste dehors. *Le personnel est nombreux et spécialisé : responsable d'accueil, de zone, de dortoir, de section.*`,
  qui: [`eliott`,`andrew`,`june`],
  gardes: [
    `**Personne ne lui dit dans quoi il entre.** Ni June, ni Andrew, ni un berceur.`,
    `**Aucun pathos, et surtout aucune pitié.** Le registre est celui d'une rentrée : on s'installe, on est content, on regarde autour, on a un peu peur et ça passe.`,
    `Ce n'est ni une mort ni une perte de la parole. **La parole est intacte à huit ans** et le restera des années.`,
    `**June a vingt-deux ans et elle l'a gardé six ans.** Elle ne pleure pas et elle ne s'attarde pas — et ça se voit quand même.`,
    `Le relais se fait sans cérémonie. Personne ne dit qu'on se relaie ; on voit seulement qu'une autre est là.`,
    `⛔ **Ne nommer aucune salle par ce qu'elle développe.** *Ni éveil, ni apprentissage : ces mots supposent une direction que ce monde ne prend pas.* On dit la salle des tapis, le gymnase, les salles de jeu.`,
    `⛔ **Le mot est interdit et les fresques le contournent.** On les décrit — peintes à hauteur de main, des proportions qui ne tiennent pas, des soleils qui ont un visage — *et on ne dit jamais qui les a faites.*`,
    `Le livre ne confirme jamais que les reliquats s'en vont là-dedans.`
  ],
  ouvert: [`⚠️ **Trois raccords à reprendre dans la dernière page**, écrite avant celle-ci : *les portes de chaque côté* et *la lumière qui venait du fond et qui n'avait pas de source visible* décrivent un couloir intérieur — or ils sont dehors. **Et la porte qui bat derrière eux doit devenir une grille**, ou une portière sur le parking du centre pédiatrique.`,
           `Ce que June lui dit exactement en partant. *« Le meilleur » est le sens ; les mots sont à trouver, et ils doivent tenir en une ligne.*`,
           `✅ **On reste dehors — décision de l'autrice, 16 août 2026.** *Le lecteur n'a plus aucune raison d'entrer.* **La cartographie du jardin se donne à la scène 14 b**, quand elle sert à l'enquête : de biais, en marchant à côté d'un pédiatre pressé. *Ici on n'en voit que ce qui passe par une grille ouverte, et la description de l'enceinte elle-même appartient à la 14 b.*`],
    src: `02-univers/le-jardin.md — décision du 16 août 2026`
}
];

/* liens du tableau : [de, vers, classe] */
const LIENS = [
  [`ouv`,`capsule`,`a`],
  [`capsule`,`s1`,``], [`s1`,`s2`,``], [`s2`,`s3`,``],
  
  [`s3`,`s4`,``], [`s4`,`s5`,``], [`s5`,`s6`,``], [`s6`,`s7`,``],
  [`s7`,`s8`,`a`], [`s8`,`s9`,`a`], [`s9`,`s10`,`a`], [`s10`,`s11`,`a`],
  [`s11`,`s12`,`j`], [`s12`,`ceremonie2`,`a`], [`ceremonie2`,`s13`,`j`], [`s13`,`s14a`,`a`],
  [`s14a`,`s14-appel`,`a`], [`s14-appel`,`s14b`,`a`], [`s14b`,`s14c`,`a`], [`s14c`,`j3`,`j`], [`j3`,`s15a`,`a`], [`s15a`,`s15b`,`j`],
  [`s15b`,`s15c`,`a`], [`s15c`,`s17b`,`j`], [`s17b`,`s17c`,`a`],
  [`s17c`,`s18`,``],
  [`s18`,`corps`,`j`], [`corps`,`s19a`,`a`],
  [`s19a`,`poursuite`,`j`], [`poursuite`,`s19c`,`a`], [`s19c`,`ceremonie3`,`a`], [`ceremonie3`,`registre-fin`,`a`],
  [`registre-fin`,`excuses`,`a`], [`excuses`,`jardin-fin`,`a`], [`jardin-fin`,`confession`,`a`]
];

