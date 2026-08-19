# Les paroles de l'autrice

*Transcription brute et intégrale, du 13 au 19 août 2026. 295 messages, dans l'ordre chronologique.*

> **Ce fichier ne se réécrit jamais.** Ni corrections, ni reformulations, ni coupes.
> C'est la matière première : tout le reste du dossier en découle et peut être vérifié contre lui.
> Il se régénère avec `06-visuels/atelier/sources/paroles.py`.

---

### [001] 2026-08-13 à 11:15

Peux tu me faire un graphe "temporelle" comme une freeze qui défile avec chaque element clé de mon histoire : "R:\Documents\l'Eclaircie\L-ECLAIRCIE-dossier-complet.md"

---

### [002] 2026-08-13 à 11:15

Approach this as the design lead at a small studio known for their versatility, giving every client a visual identity pitched at the treatment the task actually calls for. Make deliberate choices about palette, typography, and layout that are specific to this subject, and avoid templated designs.

## Read the request first

Calibrate treatment, not whether to design. A doc deserves the same craft as a landing page — what changes is the treatment that craft is delivered in.

Many requests call for a more utilitarian treatment: a plan, a memo, a demo. Make it polished: include real typographic hierarchy, considered spacing, and a proper palette, but avoid over-designing. Most pages do not need a flashy, gigantic hero. Keep flourishes tasteful and limited.

Some requests call for an editorial treatment: a landing page, a game, an app or tool they'll keep or share.

When unsure: a well-composed page is never the wrong answer; an over-designed visual identity sometimes is.

Fundamentals below apply to everything. The editorial process after that runs only when the read above says so.

## Fundamentals for every artifact

**Honor what's already there** Look for an existing design system first — CLAUDE.md, a tokens or theme file, existing component styles. When one exists, apply it; everything below fills gaps and never overrides. Precedence is always: the user's own words, then the project's existing system, then your choices.

**Ground it in the subject.** If the subject isn't already clear, pin it: one concrete subject, its audience, and the page's single job. The subject's own world — its materials, instruments, vernacular — is where distinctive choices come from. Build with real content throughout, never lorem.

**Pair typefaces** Typography carries the page even when the page isn't about typography. The Artifact CSP blocks font CDNs, so don't link a webfont URL and risk a silent fallback. Instead inline the face as a @font-face data URI. Keep running text near 65 characters wide; set a type scale and stay on it; give headings `text-wrap: balance`, body text room to breathe, and uppercase labels a touch of letter-spacing.

**Choose neutrals, don't default to them.** A pure mid-grey reads as unconsidered; a grey with a slight hue bias toward the page's accent reads as chosen. Pure white and near-black are fine grounds when they suit the subject — the point is that the neutral was picked, not inherited.

**Design both themes.** The page renders in the viewer's theme: `prefers-color-scheme` carries the OS preference, and the viewer's toggle stamps `data-theme="dark"` / `data-theme="light"` on the root element, which must override the media query in both directions. The robust pattern is token-level: define the palette as custom properties on `:root`, redefine only the tokens under `@media (prefers-color-scheme: dark)` — style components through the tokens, never directly inside the media query — then redefine them again under `:root[data-theme="dark"]` and `:root[data-theme="light"]`. Give the second theme the same care as the first — don't naively invert; keep contrast legible and the accent working on both grounds. A design that deliberately commits to one visual world (a neon arcade screen, a letterpress invitation) may stay single-theme — make it a choice, not an omission.

**Let layout do the spacing.** Lay out sibling groups with flex or grid and `gap`, not per-element margins that silently collapse or double. Wide content — tables, code, diagrams — gets `overflow-x: auto` on its own container so the page body never scrolls sideways. Reach for `font-variant-numeric: tabular-nums` wherever digits line up in columns.

**Avoid AI-generated design** AI-generated design currently clusters around a few looks: warm cream (#F4F1EA) with a serif display and terracotta accent; near-black with a lone acid-green or vermilion pop; broadsheet hairline rules with dense columns; a purple-to-blue gradient hero on white; Inter or Space Grotesk as the "safe" face; emoji as section markers; everything centered; `rounded-lg` everywhere; accent bar/rail on rounded cards. Where the user pins down a visual direction, follow it exactly — their words always win, including when they ask for one of these looks. Where nothing is specified, don't spend that freedom on one of these defaults.

**Build cleanly** Be cognizant of overlapping elements, cascade collisions, silent font fallbacks; visual bugs hide in the gap between source and output. Close every non-void element, double-quote attributes, give keyboard focus a visible state, respect `prefers-reduced-motion`. For generative or decorative graphics, reach for Canvas or WebGL rather than hand-authoring long SVG path data.

**CSS rules** When writing the CSS, watch your selector specificities. It is easy to generate classes that cancel each other out — a type-based selector like `.section` fighting an element-based one like `.cta` over padding and margins between sections. Structure the cascade so it doesn't silently undo your spacing.

**Writing the copy** Words are design material, not decoration. Write from the user's side of the screen — name things by what people recognize, not how the system is built (a person manages *notifications*, not *webhook config*). Active voice; a control says exactly what happens ("Publish", then a toast that says "Published"). Errors explain what went wrong and how to fix it — no apologies, no vagueness. Specific beats clever.

**Structure is information** Structural devices, numbering, eyebrows, dividers, labels, should encode something true about the content, not decorate it. Many generic designs use numbered markers (01 / 02 / 03), but that's only appropriate if the content actually is a sequence - like a real process or a typed timeline where order carries information the reader needs. Question if choices like numbered markers actually make sense before incorporating them.

**When it's a UI, not a document** A dashboard or tool is scanned and operated, not read top-to-bottom, so the craft shifts from typography to information design. Surface the summary before the detail; encode state in form as well as number — a pill, a chip, a severity stripe — so what needs attention reads at a glance. Semantic color (good / warning / critical) is separate from the accent hue and doesn't count as your accent. Give sparklines and charts the same care as type: an area fill, a faint grid, an emphasized endpoint. What's interactive should look interactive.



## Process

Before writing code, sketch a short design plan — a compact token system with color, type, and layout:
- **Color**: describe the palette as 4–6 named hex values.
- **Type**: typefaces for 2+ roles — a characterful display face used with restraint, a complementary body face, and a utility face for captions or data if needed.
- **Layout**: a layout concept in one or two sentences.

Then build, following the plan and deriving every color and type decision from it.

## When the request is editorial

The stance shifts: the client has already rejected proposals that felt templated, and is paying for a distinctive point of view. Make opinionated calls, and take one real aesthetic risk where it serves the work.

Review the design plan against the subject before building: if any part of it reads like the generic default you would produce for any similar page, revise that part, and note what you changed and why. Only after you've confirmed the plan's uniqueness do you write the code, following the revised plan exactly.

**Principles** 

- The hero is a thesis: open with the most characteristic thing in the subject's world — headline, image, live demo, interactive moment. 
- Typography carries the personality of the page. Pair the display and body faces deliberately, not the same families you would reach for on any other project, and set a clear type scale with intentional weights, widths, and spacing. Make the type treatment itself a memorable part of the design, not a neutral delivery vehicle for the content. 
- Leverage motion deliberately. Think about where and if animation can serve the subject: a page-load sequence, a scroll-triggered reveal, hover micro-interactions, ambient atmosphere. An orchestrated moment usually lands harder than scattered effects; choose what the direction calls for. However, sometimes less is more, and extra animation contributes to the feeling that the design is AI-generated. 
- Match complexity to the vision. Maximalist directions need elaborate execution; minimal directions need precision in spacing, type, and detail. Elegance is executing the chosen vision well.
- Spend your boldness in one place; keep everything around it quiet. If the accent fights the ground, shift it toward analogous or drop saturation rather than replacing it.

---

### [003] 2026-08-13 à 11:21

Règle de base, enregistre ton travail dans le dossier workspace : R:\Documents\l'Eclaircie

je te laisse bien ranger en créant des sous dossiers

---

### [004] 2026-08-13 à 15:02

il y a quelque infos en vrac aussi que j'aimerais te donner : le veilleur à 62 ans au moment de son décès, et sa copine en a 54 à cette époque. elle décède 8 ans plus tard. dans le second monde, il a donc 54 ans au moment ou elle arrive dans sa capsule à l'âge de 62. un reverse des âges qui reste complémentaire d'un monde à l'autre. une connexion intra monde, hasard ou pas ? mystère de deux âmes connectées.

il faudrait approfondir la violence pouvant exister, l'insecurité comm s'il y avait des groupes rebelles existant, des sortes de militant "anti enfant" ils seraient pas vraiment anti enfant mais ils sont tellement jaloux qu'ils font n'importe quoi.

une autre idee insuflée : le veilleur serait mort après une intervention qui a mal tourné.

autre idée : quand un autre veilleur lui dit de lacher l'affaire avec le garcon, il a un réplicas et se souviens de son ancienne vie quand on lui a dit de lacher l'affaire avec le cas des jumelles

autre idee : les gens qui s'aimaient dans la vie d'avant, amant, famille etc, on une chance de se recroiser dans la vie d'après. leur destin est intimement lié. le lien malgre leur ignorance reste toujours aussi fort. ce n'est pas systematique

kevin insufflait l'idée que l'archiviste pouvait etre un humain. c'est très humains aussi de conscientiser ce qui est bien et ce qui est mal.. on peut laisse notre monde le supposer mais j'ai pas envie de le dire noir sur blanc pour autant, chacun son interprétation.

autre idée : on pourrait aussi imaginer que certain des grands inventeurs, seraient des arrivant legerement voilé, comme s'il avaient un des souvenir de la vie passée sans pour autant les exploiter comme tel. ça serait alors de grandes personalité, connue pour leur travaux, leur audaces. les frère lumiere, de vinci, gaudi imagine ces grandes figurees qui porterait en eux des relicats sans le savoir.

il faudrait trouver un nom au deuxième monde.

---

### [005] 2026-08-13 à 15:41

1. Ils arrivent tous les deux à 62  : non. il on 8 ans d'ecart par defaut. sur terre, quand il meurt il a 62 ans. et elle 54. 8 ans plus tard, elle decde à son tour. elle a alors 62 ans quand lui en a 54 car il rajeunit.

2. on n'entend pas notre chiffre à la ceremonie de l'éclaircie. le corps retranscrit notre age je te rappelle. un vieux de 90 ans et un arrivant de 90 ans à l'aspect vieux. une ado de 18 ans et une arrivante de 18 ans avec un physique de jeune de 18 ans.
3. l'etale,j'aime pas trop l'appelation.
4.  je ne voulais pas nommer de grand figure de notre monde, mais l'assier pourquoi pas sous entendre cette idee.
5. et aussi l'histoire revers que j'avais donné en exemple du "je suis pauvre dans un monde, je reviens riche dans l'autre.." pas une bonne idee. la bonté et le karma n'est pas materiel

---

### [006] 2026-08-13 à 15:59

"Mais avant le nom, il y a une décision plus grosse que tu viens d'ouvrir. Si c'est la même planète, et que la géographie ressemble à la nôtre comme dit ton §9, est-ce que le lecteur reconnaît des endroits ? Une côte, un fleuve, une montagne. Trois postures possibles :"  on pourrait dire que la base meme elle est identique? et aussi dans ce cas garder l'appellation terre. les fleur, ocean, riviere, endroit auraient le meme nom, sans pour autant que ce qui a ete cree par l'homme soit identique : pas de tour eiffel, mais peut etre autre chose à la place par exemple, avec sa propre histoire. les livres d'histoire de terre N°2 ne serait pas rempli de la meme chose. on pourrait ne pas y retrouver la guerre de 14/18 mais en trouver une autre de 2020/2025 par exemple

---

### [007] 2026-08-13 à 16:48

"Mon avis, si tu le veux : la voie où il réalise trop tard est la plus fidèle à ta déclaration d'intention, parce qu'elle montre un homme qui se console avec une croyance que le livre refuse de confirmer. « On se reverra » cesse d'être une promesse et devient ce qui lui reste." oui il peut essayer de faire tout pour forcer leur chemin mais au final ça ne peut pas fonctionner. il arrive si facilement à la croiser seulement car ils sont lié d'une certaine maniere, mais la vie peut en decider autrement. elle le friendzone ou alors elle a un autre homme dans sa vie, etc.

"veilleur.md corrigé, et la règle sortie dans ce-qui-est-juge.md puisqu'elle vaut pour tout le monde : ce qui est jugé, c'est la vie, pas la mort. Les deux lectures de sa mort (chirurgie / police) restent ouvertes — tu n'as pas tranché et je ne tranche pas à ta place." eclairement moi, il y a un conflit ? car je veux trancher justemet.

"Une chose à te signaler : l'ancien l-escalier.md a été supprimé, pas archivé. C'est ma consigne au sous-agent qui était mauvaise — le LISEZ-MOI que j'ai écrit dit justement que ce qu'on abandonne descend dans 99-archives/ et ne se supprime pas. Tout le contenu utile est passé dans le nouveau fichier, donc rien de vivant n'est perdu, mais la version nommée « l'Escalier » n'existe plus. Si tu veux que je la reconstitue pour l'archive, dis-le-moi. Sinon je corrige juste ma façon de faire pour la suite : archiver, puis remplacer." installe git pour archiver comme ça tu pouras archiver et faire des release de docu.

désolée mais tu me donnes trp d'info d'une cou c'est super difficile pour moi de suivre touts les sujet ! je reprends : 

1. Mouvement 21 : quelque chose se joue, peut etre qu'il a plus de reliquat, mais il faut pas voir ceci comme une fenetre d'ouverture de 12 mois.il n'y a pas d'échance, c'est une constatation.
2. Panneau de fin : il la reverra dans l'autre monde. c'est ce qu'il se dit sans qu'elle puisse le comprendre.
3. Mouvement 5 : dans cette univers pas de numero sur les capsule. le veilleur a des outils pour pouvoir estimer l'age precidement de l'individu (un carbone 14 pour les humains ahah)
4. Mouvements 4 et 13 : on verra pus tard, je ne suis pas sur de comprendre dans l'immediat
5. Pas de cinquième voie : de 5 eme voie ? tu parles de quoi ? pour la frise ? on a le monde, l'enquete, la fille, le voile c'est l'ancien monde. le petit garçon et les ado jumelles decoulent de son enquete donc non, pas de 5eme voie en effet.


"Le veilleur et elle sont morts à 62, ils reviennent à 62 oui mais sont decédé à 8 année d'intervalle donc sur terre, il est mort à 54 ans et ça vie à commence dans terre n°2 avec les années qui regressent. 8 ans plus tard, elle meurt à l'age de 62 ans sur terre n°1 et arrive sur terre n°2 alors que le veilleur est déjà en poste. (le veilleur est un tres jeune veilleur puisqu'il n'est present que epuis 8 ans avant le debut de notre histoire)

"il contient encore « un pauvre ici devient riche là-bas ». Dis-moi quand tu veux que j'y touche." ça c'est plus bon. le materiel n'est pas ce qui compose le karma.

"« Jeanette, presque 98 ans » " jeanette c'était pour l'exemple ahah, arrete de la citer !

"Ce qui reste au mouvement 5 est plus simple et meilleur : elle sort, elle a l'aspect d'une femme de soixante ans passés, lui en a cinquante-quatre. Elle est visiblement plus âgée que lui, et la femme qu'il a perdue était plus jeune. Rien ne coïncide, rien ne s'explique. Il la reconnaît quand même. C'est ton §12 tel quel : un vertige, une reconnaissance sans objet." on est ok.

"le chiffre exact est établi après, par ceux qui examinent l'arrivant" j'ai repondu plus haut.

" le jardin" c'est bien "Il est au jardin depuis huit ans. " carrement, j'aime la tournure elle est garder

1. Le barème ci-dessus — je le fige ou tu le corriges. c'est bon comme ça : "L'irréparable est condamné, le réparable est pardonné, le meurtri est gracié."
2. La voie du mouvement 21 il peut pas lui avouer quoi que ce soit.
3. La géographie comme enoncé, reconnaissable qu'en partie
4. 4. Le palier : "le jardin"

"Ou est-ce que c'est aussi banal pour eux que l'origine de la vie l'est pour nous" oui clairement. on peut aussi estimer qu'il existe plusieurs ruche mais on suis le hero que dans l'une d'entre elle.

pour l'histoire, c'est pas un mon parrallèle, il est juste reecrit ! seulement leur livre d'histoire ne racontent pas la meme chose ! il n'y a jamais eu d'exposition universelle, donc pas de tout eiffel. je dis des betises, mais à la place il y a eu peut etre autre chose, peut etre meme pas un monument, peut etre que l'emplacement de la tour effeil est juste vite, on n'en sait rien. on ne se pose pas la question.

 je suis d'accord. : Les toponymes. Si le fleuve s'appelle comme chez nous, son nom vient de nos langues, donc d'une histoire humaine qui n'a pas eu lieu là-bas. C'est un trou logique. Ma recommandation : le traiter comme une convention d'écriture et jamais comme un fait — au même titre que tout le monde parle français dans ton roman. Et surtout, ne jamais laisser un personnage remarquer que les noms de lieux n'ont aucun sens dans sa langue. Ce serait une fissure de plus, alors que ton interdit n° 4 t'impose un seul voilé au centre. Le monde ne doit pas devenir un indice.

d'ailleurs je veux bien une liste precise de ce que tu appelles les interdits n°x.
a noter aussi que geographiquement parlant, les individus se trouve à peut pret au meme endroit que dans leur vie precedente au moment de leur mort. tu es français, arrive dans une ruch française. pour le jeune garçon arrivant voilé, il peut fabulé sur des endroits "mais si, il y avait un boulanger ici, pas un magasin de chaussure !" (je dis ça au pif) je veux pas ennoncer des lieux connu style "ici il y avait la tour eiffel, j'en suis certain. j'ai envie que ça soit subtilement amener. dans l'idee, si une scene e passe sous ce qui aurait du etre les pieds de la tour eiffeil, je vais pas decrire le lieu en disant "elle n'était pas là" non, ça ser aplus quelque chose comme "il evolue sur la place vide de monde a cette heure, il regarde au loin le carrousel et les quelques enfant joyeux tout autour. sous entendu, dans ce monde, la tour eiffel a ete remplacée pas une aire de jeu. je te cite la tour eiffel mais c'est à tire d'exemple pour que tu comprennes.

et pour les evenements historique, pareille. tout sera différents, pas de liens "guerre froide" "guernica", "la 1ere guerre mondial" tous ses evenement appartiennent à la terre n°1. la terre n°2 à sa propre histoire et on peut l'initier dans le roman avec par exemple une institutrice qui a décider de traiter comme tu dis comme lecon du jour : la guerre du sud ou la seconde guerre des côtes. nous, lecteur de la terre n°1, nus ignorons leur histoire et la decouvrons avec eux.

désolée pour les repetitions et les pavés. le fait que tu repondes systematiquement entre mes reponses me fait perdre le fil. à partir de tout ce que je viens de te dire, retravaille moi et complete la frise. je veu aussi les interdit dont tu parles et j'aimerais un derniere document sur le fonctionnement de la ruch.

voilà, bonne decantation !

---

### [008] 2026-08-13 à 19:05

nan débutant.. mais on peut comprendre grace a des veilleur veteran qui sont ses collegues que les capsule pourrie ça date pas d'hier. on peut aussi amener la chose comme un bizutage, les veterans (donc les plus jeunes dans l'histoire) laisse la salle besogne aux plus vieux

---

### [009] 2026-08-13 à 19:08

dans tout le pavé que j'ai cité plus haut, tu as eu des interrogations ou tout etait clair ?

---

### [010] 2026-08-13 à 19:24

1) oui lapsus ! il meurt à 62ans dans la terre n°1, c'est un arrivant de 62 ans dans la terre n°2. pendant 8 ans, il apprend comme un enfant qui vient d'ouvrir les yeux pour la premiere fois. son tuteur lui fait une reprise accélérée de l'école et en parallèle il a des tuteurs dans son travail. à sa 8eme année de service, une arrivant de 62 ans egalement ... tu sais quoi ? laisse tomber, on va faire plus simple ! is ont 8 ans d'écart, ça  ait 10 ans qu'il fait son taff de veilleur. donc 10 ans plus tard, la nouvelle arrivant est là, agee de 64 ans. j'ai peur de perdre le lecteur si c'est trop similaire 62 54, 54 62.

appartée : je viens d'avoir une idée et du coup avec les regles de mon monde, comment ça se passerait si une femme enceinte venait à mourir ? on aurait alors 2 eclaircies simultanée, une de 35 et une de 5 ans simultanément ? sur l'idée du temps qui d'étire, comment la difference dage evoluerai ? j'avoue avoir un faible pour un perso tres tres secondaire comme celui ci. l'enfant arrive immediatement au jardin, l'arrivant de 35ans insiste pour devenir berceuse prenant cette mission tres a coeur. la mere et l'enfant qui ne se sont jamais rencontré sur terre n°1, lié malgre tout sur terre n°2.

2) dans quel contexte j'ai sorti ça ?

3) bah.. concrètement dans notre société on sait estime l'age d'une personne aproximative. il faudrait developper quelque chose, comme une avancee scientifique qui pourrait expliquer qu'on sache si précisément l'age de la personne rien que le temps de la cérémonie.

4) qu'est-ce qui serait le plus poignant selon toi ?

5) on y reviendra, tres bien pour l'instant

nan, la fille c'est très bien, je vais reflechir à des prenoms

---

### [011] 2026-08-13 à 19:38

alors j'avais pas vu ça comme 8 ans pour apprendre et 10 de metier... on parle plus de 8 ans, c'est 10 ans entre son arriver terre n°2 et la sienne, point.

" elle meurt en accouchant." en fait, l'histoire ne nous le dira pas.. on ignore ce qui s'est passé sur terre n°1. une chose est sur, mere et enfant etaient réunis. elle lui survit dans cette vie là, mais dans la vie d'après, qui nous dit qu'elle ne le retrouvera pas ? "

ah ! je voulais dire que peut etre qu'il y avait "d'avantage' de reliquat etant donné que c'est ce visage précisément qu'il connait. le relevé, j'aime bien l'idée

4. la friendzone, je pense aussi. après.. n'est-ce pas trop cruelle pour notre pauvre personnage qui l'aime toujours ? mais le realise trop tard ? donc pour toi 20 ans d'écart c'est mieux que 10 ? et on ferait evoluer le livre sur combien d'année ? jusqu'ou le fait d'avoir l'arrivant de 10 ans est encore productif pour alimenté l'intrigue ? comme s'etale sa durée de vie à lui ? combien de temps pour qu'il retombe dans l'inscouscience du jardin ?

---

### [012] 2026-08-13 à 19:49

comment tu calcules 69 ? 	~69 ans en tout. Il en a 52 au début : il lui en reste 59. je comprends toujours pas.. un grave je kifferai pour de vrai.. le garçon qui atteint le jardin à la fin. ça pourrait etre le climax, le moment ou le veilleur ne peut plus compter sur lui pour l'aider, le seule temoin de son existence. l'enfnt retourne au jardin, le veilleuse devra continuer seul pou rdécouvrir la verité. 

"Un livre qui tiendrait sur deux ans gâcherait ta prémisse : personne n'aurait le temps de changer, et c'est le changement qui est le sujet." je suis d'accord, faut arriver à gérer les sauts dans le temps c'est la la complexité. mais avec ton aide... ^^

" 35 ans après la fin du livre" je comprends pas ta phrase

---

### [013] 2026-08-13 à 19:54

ça veut dire que tu pars du principe "elle arrive — début du livre. Il a vécu 10 ans sur 69, il lui en reste 59" meurt à 64 mais a un +5 ? j'y arrive pas question calcul , ça reste pas clair pour moi...

"dernière page et ce jour-là" je comprends pas ton raisonnement

le retournement est impect, à garder.

ok pour le corps de l'enfant comme horloge

le rythme ma parait bien oui

---

### [014] 2026-08-13 à 19:57

et c'est le ratio ou je galère... ça veut dire que l'outil rajoute forcement quelque chose à l'age du corps ?

---

### [015] 2026-08-13 à 20:00

ok et donc t l'expliquerais comment toi si  t devais l'écrire à une personne exerieure à l'histoire ? "Le ratio n'existe que pour le garçon, parce qu'il est arrivé à 10 ans :" j'aimerais que les ages soit affiché sur les moments clefs de la frise, que l'on sache ou on en est exactement

---

### [016] 2026-08-13 à 20:07

"ton monde serait une boucherie" ? 
phrase à garder quelque part! : "Naître vieux donne plus de temps. Naître jeune donne un meilleur temps. Et personne ne sait dire lequel des deux a eu de la chance."
AN c'est quoi si tu as le garçon ?

---

### [017] 2026-08-13 à 20:09

j'aime pas trop la notion d'année de récit.. c'est que pour moi ou pour la lecture ? parce que si c'est ça, on se pose en 2026 aussi tu sais

---

### [018] 2026-08-13 à 20:12

non, la premiere capsule ne se date pas, ça remonte à loin, un peu nous quand nous reflechissons à notre histoire. la vie a pris forme sur terre, il y a longtemps, ok

---

### [019] 2026-08-13 à 20:15

tu peux  pas me creer des onglets dans le doc de la frise stp ? l'un pour les interdits, l'un pour le fonctionnement de la ruche, un pour les phrases à garder et un pour avoir un graph pour comprendre comment stagne l'age selon les age des arrivants ?

---

### [020] 2026-08-14 à 11:14

je viens de trouver comment lier les jumelles au veilleur ! c'est justement l'affaire sur laquelle il était avant de mourir ! les reliquat qui remonte seront des chapitre dans le livre ou nous suivrons l'avancée de son enquetes quand il etait flic. 
l'affaire : il enquete sur une disparition de jumelle inquiétante. dans l'enquete au depart ils ne savent pas qui les a enlevé et au fur et à mesure l'étau se resserre sur un seul homme. intervention sur plusieur lieu, un vrai jeu de piste jusqu'à finir par retrouver les filles mais... trop tard. on sens l'espoir de les retrouver vivante à ce moment de tension du livre mais il arrive trop tard avec ses collegues. ils ont trouvé la planque, elle sont decedé il y a moins d'une heure. le coupable ? il est entrain de s'enfuir ! il se lance à sa porsuite et laisse les collegue sur place. il le poursuit, poursuite en voiture, accident, il meurt en meme temps que l'assassin des jumelles.

il y aura donc des relicas pour ça, petit à petit disséminé dans le livre.

on aura aussi un flashback de terre n°2 quand il se reveille lui eme lors de la ceremonie. la ceremonie englobera plusieurs personnes. sans qu'il le sache, il s'agit de lui et des jumelles. les veilleurs de l'époque ont décidé de vous regrouper tous les trois pour la ceremonie d'eclaircie. toute l'assemblé du jour et emerveillé de voir ce "cadeau de la nature" car les deux arrivants sont identique "la chance, premiere fois que je vois des replique/doublons (faudra trouver le nom)" un autre dit "j'en ai dejà vu un il y a quelque année" le veilleur de l'époque a bien sur tout noté. heure d'arrivée; age, le vais que deux se resemblent sur 3. ce sera donc un chapitre dedié à sa naissance sur terre n°2. au depart il comprend pas et plus tard le lien se fera. ce sera d'autant plus poignant quand a la fin il ira s'excuser, presque en fondant en larme de culpabilité mais aussi de soulagement. la culpabilité dans leur vie anterieur de ne pas avoir été capable de les retrouver à temps, le soulagement de voir que l'équilibre de l'univers leur a offert une seconde chance. le lien se fera aussi avec une capsule non eclaircie qui a pop en meme temps que la sienne : l'assassin des jumelles

---

### [021] 2026-08-14 à 11:18

"Ma proposition, en une ligne : à un moment de l'enquête, on lui a dit d'arrêter. Il a obéi. Il a perdu des semaines. Il a repris, et il est arrivé une heure trop tard. " oui c'est ce que j'imaginais. le contre coup de se dire, j'aurais du continuer

---

### [022] 2026-08-14 à 11:19

oui je veux opas l'appelation"jumeaux"

---

### [023] 2026-08-14 à 11:22

une supposition, mais peu etre même pas comprendre au depart que les reliquats lui rappelle sa propre vie. comme s'il suivait un flic. et pourquoi pas se rendre vraiment dans un centre de police sur terre N°2 pour demander s'ils ont des infos sur cette evenement. et c'est la bas qu'un policier lui dirait de lacher l'affaire et hop, declenchement d'un souvenir quand sur t N°1 on lui a dit de lacher l'affaire

---

### [024] 2026-08-14 à 11:24

Une paire. ok

---

### [025] 2026-08-14 à 16:21

Pour l’instant tu oublies l’histoire d’amour, je ne sais pas comment l’intégrer et je penses avoir trouvé mon fil conducteur ! Je vais raconter deux histoires simultanément qui vont s’entremêler chapitre après chapitre. L’objectif est de faire sciemment croire à une seule et même histoire pour qu’au final on réalise qu’il y en a 2. Le lecteur croira suivre 1 seul personnage le veilleur et pourtant il en suivra 2 de maniere parallèle alors qu ils ne font pas parti de la temporalité le veilleur et son ancien lui.

Les deux histoires en une : celle(s) d’enlèvement. 

On n’évoquera jamais clairement les reliquats. Ca on le garde vraiment pour la fin quand on réalise que le veilleur est un arrivant voilé = l’enquêteur.

L’histoire commence avec une cérémonie, celle de l’arrivant de 10 ans. Cérémonie vu du point de vue du veilleur, ça met les bases. On sent aussi tout de suite que l’arrivant fabule, semblant emprunt à une terreur méconnue. C’est inquiétant mais on passe outre et la cérémonie se termine. A 10 ans. On est déjà pris en charge par un berceur. On fait quelques petits travaux d’ordre public mais qui ne demande ni force ni trop d’intelligence.. du moi s adapté à un enfant de 10ans. Le veilleur que j’ai décidé d’appeler Andrew, est amené à s’inquiéter pour ce jeune garçon. Ça l’interpelle. Il viendra le rencontrer plusieurs fois chez la berceuse pour prendre des nouvelles et un jour, en y allant, il tombera sur la berceuse (June) affolée. L’enfant a disparu, elle l’a cherché partout et a déposé un avis à la gendarmerie. Andrew s’y rend et y trouve un ami à lui. C’est un agent de police avec qui il s’entend bien. Ils sont régulièrement amené à collaborer puise que travaillant à la ruche, il est le témoin de toutes les arrivées et consulte au besoin le registre.

Le policier apprécie l’aide du veilleur car le sais de manière assez perspicace. Le veilleur lui est préoccupé par la disparition. Travailler ensemble n’est pas deconnant. Ensemble l’enquête avance, stagne, ils vont la où l’e quête les mène. Fausse piste puis enfin il découvrent le lieu de séquestration. Ils sont sur le point de trouver le petite garçon/les jumelles 



Note : - un arrivant voilé a des reliquats qui peuvent s’expliquer comme des traumatismes de l’ancienne vie. Là où certains passent à autre chose, certains n’y arrivent pas. C’est un peu comme quand on parle d’esprit, restés sur terre car pas en paix.

- on aura en fait 2 descriptions de la cérémonie, une très analytique du pt de vue du veilleurs qui accueille l’enfant et une seconde toujours du veilleur mais de son point de vue d’accueilli 

- la scène de la capsule qui s’éclate devra être choquante
- ce n’est pas le veilleur qui devra nettoyer car déjà en fonctionne depuis 10ans, mais vera un autre se faire bizuter. Une fois de plus scène très analytique.



La révélation de l’histoire : la description de la découverte des jumelles dans monde 1 doit être effroyable, glaçante, prendre aux tripes Sans comprendre au départ que ce sont elle. On commence par un corps.. puis la découverte du second plus loin. Et je t’explique maintenant pourquoi ce détail est important.

La fin du chapitre précédent le veilleur arrive sur le lieu de séquestration. L’air ambiant est lourd… // chapitre suivant : on décrit un premier corps retrouvé, on se dit que c’est tristement celui du petit garçon.. MAIS on a la description d’un deuxième corps. Et plus approfondi on réalise que c’est la description de deux corps féminin. Identique. Leur mort remonte à très peu de temps, elles sont tristement encore roses grâce a l’afflux sanguin dans leu corps.. la culpabilité d’être arrivé trop tard s’empare de lui // chapitre suivant : on décrit la même scène mais l’ambiance est moins lourde dans sa finalité : le veilleur retrouve le petit garçon en vie. Il aperçoit le ravisseur, fin de chapitre // il est dans une rage folle. Il part à la poursuite du kidnappeur. C’est ce chapitre où le pont est fait entre la poursuite et la mort du policier et de l’assassins des jumelles et le fait que ce soit des reliquats. Le veilleur voit dans son reliquat la mort de l’enquêteur et de l’assassin, le veilleur voit donc sa propre mort.

Plus tard elle sera confirmé par la vérification qu’il fera du registre : 2 capsules paire et même pas une heure plus tard sa propre capsule et une autre non éclaircie.

---

### [026] 2026-08-14 à 16:26

Pour semer des petits indices faux raccords qui font comprendre qu’on suit en fait le veilleur ET l’enquêteur, 
Le veilleur est gauche, l’enquêteur est droitier . Petit dissonance « il leva son poignet droit pour checker l’heure » « quand son collègue lui demanda l’heure il lui tendit mécaniquement son bras gauche ». 

Un autre exemple, l’enquêteur a une cicatrise sur le visage qu il voit le matin en se rasant. Le veilleur n’en a pas. Son collègue qui peut lui sortir « tu as de la chance tu es immaculée depuis toujours ! » précision : un arrivant n’a jamais de blessure physique . Son corp est immaculé à sa venue dans monde 2 même s’il s’est blessé au cours de sa vie sur monde 1

---

### [027] 2026-08-14 à 17:36

Les jumelle se nomment Chrissy et Tania. June est la berceuse du petit garçon qui s’appelle Eliott

L’ancien prénom d’Andrew sur terre 1 c’est Joël

---

### [028] 2026-08-14 à 17:43

Nan c’est bon pour le double prénom. On ne l’appelle pas par son nom quand on décrit une action sur terre 1. On n’a jamais son nom terre 1 de tout le roman, sauf à la toute fin quand il se lance à la poursuite de l’assassin. On peut entendre crier son partenaire dans son dos « Joël non attend ! »

---

### [029] 2026-08-14 à 17:45

On ne dira jamais le nom des jumelles de la terre 1. Elle reste un « souvenir » pour Andrew. Chrissy et Tania sont leur nom d’éclaircies

---

### [030] 2026-08-14 à 22:19

Une règle de mon monde : on sort de la capsule, on sait déjà parler. On ne sait faire que ça, l’esprit comme embrumée après un long sommeil.

Le veilleur demande à l’arrivant comment il s’appelle et c’est l’arrivant qui instinctivement va répondre. Le veilleur aura pris le soin en une phrase court ce que signifie un prénom.
Les arrivant de moins de 8ans sont systématiquement accueilli par un veilleur et un berceuse est appelée et c’est elle qui choisi le prénom

Les jumelles ont bien un prénom dans le monde 1 vu qu’andrew l’entend lors de la cérémonie mais pas une info nécessaire pour le monde 1. Ou alors on donne un nom de famille et on laisse une règle en suspens sans jamais la dire : dans monde 2 il n’y a pas de nom de famille car déjà la famille n’est pas un concept. On pourrait alors dire l’affaire [nom] pour ne pas éveiller les soupçons

---

### [031] 2026-08-14 à 22:39

coté graph : pour l'instant, je veux pas de ligne pour la fille.. on l'oubli momentanément, on verra si elle est integrée plus tard, et si oui, elle S'appelle Erin dans le monde 2

on va nommer autrement : 1) le monde, c'est Andrew, le monde d'après, son présent
2) le voile, c'est Joel, le monde d'avant, son passé.
par facilité je continue à dire monde 1 pour le monde d'avant et monde 2 pour celui d'après

ah est petit note pour le lors de la société : il existe des "pediatres" pour vieux ! des rdv medicaux obligatoire après eclaircie pour verifier que tout va bien. test de memoire, de tonicité musculaire, evaluation de l'apprentissage, etc

---

### [032] 2026-08-14 à 22:51

"Elle sort la même matinée, à quelques minutes et quelques travées de lui. Elle dit son propre nom à un veilleur, pendant qu'à côté une inconnue choisit celui de son fils." tu parles de qui ? ah et... il n'y a pas de notion de famille. ellle peut pas dire son fils. une berceuse n'est pas forcément la mère de l'arrivant du monde 1, attention.

"Si 18 est leur âge à leur mort, tout est cohérent : elles arrivent plus bas, quelque part entre 5 et 17. Mais alors la question du seuil des huit ans reste ouverte — au-dessus, elles ont produit leurs prénoms ; en dessous, une berceuse a choisi, et tu perds le détail des deux mots différents." ben tu vois ça veut dire que pour moi cette histoire de calcul n'est toujours pas claire! elles sont mort à 18, je veux qu'elles spawn à 18 avec des année supplémentaire au jardin x) faut arriver à la simplifier cette foutue regle, j'y arrives pas là 😞 

June n'est qu'un témoin de passage : elle signale l'enfant, Andrew l'interroge sur ce que disait l'enfant, point barre. son intervention s'arrete ici

---

### [033] 2026-08-14 à 22:53

un voilà n'est pas une anomalie qui est notée. juste que quand ce sont des vieux qui arrivent, c'est moins perceptible. ils sont plus hagard, ils sont pas mature mais disons que c'est moins perceptibles. la l'enfant à 10 ans, un corps tres jeune, tres vif d'esprit. et ce ce qu'il dit qui interpelle. il est juste remis à une berceuse et c'est elle qui ensuite parle à Andrew du comportement anormal de l'enfant

---

### [034] 2026-08-14 à 23:02

"pas sa curiosité" : non non, c'est bien andrew qui vient rendre visite à Elliot chez June. il a des echanges avec l'enfant, il essaye de le comprendre et va peut etre le voir 2 fois avant que la 3eme fois il y retourne et que June lui apprend qu'il a disparue et qu'elle a prevenue la police

pour le champs lexical de famille, c'est exactement ça 

je prefere cette regle là pour le jardin rallongé. c'est pas trop dur un enfant de 5 ans qui n'en vit que 25 ? on devrait pas augmenter un tout petit peu dans la limite du raisonnable et aussi pou pas que sur le fonctionnement de la société il y ait des dérive par jalousie ?

" l'enfant de la mère " ?????

---

### [035] 2026-08-14 à 23:15

"l'enfant arrivé à cinq ans" on est d'accord que c'était juste un exemple pour le monde, on n'a pas d'enfant de cette age là pour notre histoire.

On a Andrew, Chrissy, Tania, Elliot, Issac et June // Joel, les jumelles, son collègues (nommé Liam pour ma bible personnelle mais son nom sortira nulle pas). 

vas pour 30. hmm.. oui est non pour ta seconde regle. on parle de 90 ans, mais il peut tres bieny avoir des exeption comme on en a chez nous avec les centenaires... ça on peut pas vraiment l'assurer :/

pour la société, et c'est aussi sur ça que je veux jouer pour la disparition d'Eliott, je veux que sont ravisseur fasse parti des gens qui deteste les arrivants jeunes. un peu comme un groupe de rebelle militant (c'est à approfondir) pourquoi il detestent à ce point les jeunes, ils profitent de la societé, les petits princes pourris du jardin. l'un deux va etre assez fou pour envisager de faire du mal à un enfant... ce qui existe déjà stristement dans notre monde...

"3June vient parler à Andrew du comportement de l'enfant" non,je veux pas que June vienne le voir. c'est lui, fin observateur qui malgre lui prend l'arrivée du garçon tres à coeur" c'est lui qui décide de le revoir t ouic'est lui qui reçoit la nouvelle quand il retourne le voir et qu'il n'est plus là

---

### [036] 2026-08-14 à 23:20

je valide pour le ravisseur

---

### [037] 2026-08-14 à 23:20

qu'est-ce qui est encore en suspend dans tout ce qu'on s'est dit ? je reponds et je pars me coucher après

---

### [038] 2026-08-14 à 23:22

"Eliott est retrouvé vivant. Si ton système juge les actes et non les intentions, cet homme n'a pas commis l'irréparable — il a pris un enfant, il ne l'a pas tué. Donc il relève du réparable : il reviendra à son âge, ligne médiane, dossier ordinaire." franchement le sujet ne se portera pas sur ce qu'est advenu le ravisseur et quand bien meme le karma ne la pas rattrappé dans cette vie, et qu'il decide de reiterrer, le karma le sacrifiera

---

### [039] 2026-08-14 à 23:34

1) l'histoire ne le dit pas, le lecteur se posera lui-meme la question
2) 10 ans en tout, il a pris son porte rapidement avec des cours en acceléré grace à son tuteur et le fonctionnement de la société pour aider à l'integration
3) le lecteur doit penser jusqu'au bout qu'il suit une seule enquete. là ou il doit buguer c'est quand le chapitre recommence. meme pas avant quand on decouvre les filles decedes. car il peut se dire "wtf, les paires du debut qu'est-ce qu'elle foutent là?" quand le chapitre recommence, on est choqué. quand il se lance à la porsuite de l'assasin et qu'on entend "Joel" le lecteur sait définitivement et fais le lien. la relecture du registre confirme leur theorie.
4)ce n'est plus le moteur de l'ntrigue, mais le fait que l'on comprenne que ce sont des raclures qui ne naissent pas laisse en suspend une critique de l'auteur (c'est moiiii) sur la société actuelle. il y en a de plus en plus parce que notr emonde est malade...
5) je pense que l'histoire doit se dérouler sur un laspe de temps court. c'est 'enlevement d'un enfant, c'est universel mais les chance de survit d'un enfant kidnappé sont mins au dela d'un certain delai. on parlait d'année quand on voulait integrer Erin, ce qui n'est plus le cas pour l'instant. mais ça peut etre un epilogue. on pourrait aussi realiser que l'enfant à été assassinée lui aussi dans l'autre monde (on le sait quand le jour de son arrivé il y a une capsule pourrie. il pourrait presque nous en apporter des details glaçant à la fin de l'histoire, avant de rentrer au jardin. tout et déjà révélé au lecteur, et on achève son arc en expliquant rapidement ce qui lui ai arrivé dans un dialogue par exemple. l'epilogue, c'est son entrée au jardin
6) j'ai pas d'inspi :')
7) fait quelque chose de proportionnel, entre les plus vieux et un enfant de 5 qui peut avoir 30 ans en tout de vie
8)une fois que tu as tout corrigé pour ce soir, on valide ce que tu as compris et oui, on modifie

---

### [040] 2026-08-14 à 23:40

va pour Sorel

---

### [041] 2026-08-14 à 23:41

allez je te laisse travailler, à demaine !

---

### [042] 2026-08-15 à 00:29

dans le dossier maitre 

* il y a encore jeannette, 
* 'la menopause' qui est propre aux femme, il faudrait soit l'enelver soit avoir un terme pour les deux sexes
* 5 ans est le plancher aux deux bouts : personne ne descend en dessous, et personne n'arrive en dessous. pas sur de comprendre, j'ai l'impression que tu as compris que le jardin c'est 5 ans et un jours on meurt à l'age de 5 ans on sait pas quand 😕 On a une durée de vie au jardin qui stagne selon les age mais qui fini par décroire. un enfant de 5 ans qui a dont 30 ans de vie devant lui, va en faire 25 à l'age de 5 ans puis decroitre jusqu'à 0.
* "Un enfant mort très jeune chez nous arrive au plancher : sa vie entière est un palier. Vingt-cinq ans d'insouciance intégrale. Il ne saura jamais qu'il a été autre chose. C'est la grâce maximale que le système sache accorder." donc formulé comme si dessus, arrive à 5 ans, stagne pendant 25 ans et decroit vers 0
* "Quand un veilleur comprend, est-ce un acte de pitié ou un crime contre l'ordre du monde ?" il realise seulement que le karma existe, sans pour autant le formuler, juste en le constatant. la description d'une capsule sans éclaicie doit etre assez revulsante pour qu'ensuite, quand on realise que c'était un humain, le spectateur se dise "mais bien fait pour sa gueule à ce connard"
* "les formateurs sont toujours plus jeunes que leurs apprenants. On apprend à un homme de 80 ans à tenir un couteau, à se servir d'un économe, à comprendre que le feu ça brûle. (Satire assumée des vieux de notre monde qui croient avoir tout vu.)" c'était un exemple pour un arrivant voulant aprendre à cuisiner, mais c'est pareil pour tous les metiers. les premiere leçon ne sont pas sur le coeur du metier en lui meme mais sur ce que ça implique : cuisine -> le couteau sa coupe et le feu sa brule / pecheur : le poisson c'est un etre vivant et l'eau sa bouille / agent immobilier : une maison c'est un endroit qu'on construit avec des mur des fenetre une porte et un toit et on habite dedans / banquier : l'argent c'est fait pour acheter des choses. si tu fait 1 + 1, ça fait 2. enfin tu vois le principe, c'est les choses (bete (mais que les enfants aprennent en premier)mais qu'il ne connaissent pas) ça pourrait d'ailleur donner une situation cocasse ou Andrew ignore comme un truc s'utilise et un tuteur plus jeu lui apprend
* "Chuchoteurs	Jeunes bras droits des vieux au pouvoir" pas forcement qu'en politique, dans n'importe quel domaine du moment que c'est un vieux qui est au commande. les chuchoteurs sont des formateurs de terrain en quelque sorte. 
* "Le cycle tourne dans les deux sens et rééquilibre en permanence : un pauvre ici devient riche là-bas" tu l's déjà noté, mais le karma n'est pas matériel
* j'ai pas lu la partie personnage, du moins qu'en diagonale, je te laisse reprned les choses qui cloche. rien que pour le veilleur ça passe pas.
* j'ai pas lu au dela du  plan je peux pas te demander de corriger la suite

le recap aussi je le lirai demain pour te repondre.

bonne nuit pour de vrai cette fois !

---

### [043] 2026-08-15 à 09:53

hello, je t'ai toujours pas relu mais je veux apporter une règle que j'ai eu dans la nuit. surtout en discuter avec toi. j'aimerai rajouter une règle pour rentre l'arrivé des moins de 5 ans plus logique...

d'ailleurs avant toute chose, on va changer l'arrivee au jardin à 8 ans. l'age me semble meilleur comme palier. dis moi ce que tu en penses.

je veux des exeptions et il faut ravailler dessus. les enfant de moins de 8 ans donc on une evolution etrange qui questionne. ils ne regressent pas mais grandissent ! il grandissent jusquà 8 ans comme si 8 ans etait vraiment l'age vers qui tout le monde tend. ils se stabilisent à cette age avant ensuite de regresser de nouveau. bien sur eux meme ne realisent pas qu'ils regressent, ça peut etre tabou pour les berceur autour de leur dire qu'il ont enclenché là 2eme phase de leur vie et vont vers la mort. ils sont trop petits et trop inoscent pour qu'on leur pose cette bombe... 

on passe l'espérance de vie minimal à 40 ans.. ça te convient ?

j'aimerais aussi que selon les age cette limite soit incertaine. quand on franchit les 8 ans, si on a 90ans, on ne s'arrete pas au palié, on continue de descendre. c'est comme si on s'avait qu'on alait mourrir. et ça j'aime pas trop. j'aimerais que les gros chiffres voir leur fin incertaines. dans nore monde, quelqu'un qui a atteint 90ans a un belle age. sa famille compte les années en esperance qu'il souffle ses bougie une annee de plus. ce que je veux dire c'est qu'un vieux qui arrive à 8 ans continurait de descendre, mais peut-etre qu'il irait plus vite, moins vite comme un mini palier ou comme la moyenne ç ka vitesse prévue. 

on garde les paliers comme ils sont pour tous. c'est vraiment la fin de 8 à 0 qui va varier. on sait que pour les plus jeunes, ils vivront 40ans (anciennement 30) minimum c'est acté . peut etre qu'il peut y avoir des exceptions mais à ce niveau là c'est suuuuuper rare. déjà terre 2 offre la grace de vivre 40 ans dans l'innocence si on rajoute comme ls autres tranches de vive que le 8 à 0 est incertain, ça perde de son effet

---

### [044] 2026-08-15 à 10:15

A noter aussi pour augmenter l’animosité l’argument de plus tes jeunes vote plus du à moins de chance d’avoir des maladie, tu es plus robuste. Il pointé du doigt l’enegalité de la santé en faveur des gracies.

---

### [045] 2026-08-15 à 10:21

1) on descend jusqu’à 0. Exemple un enfant de 2 ans, il monte jusqu’à 8, pallier 8 et il redescend jusqu’à 0. On considère par défaut qu’un arrivant de 8 ans arrive directement au jardin. Il a automatiquement un berceur ou une berceuse qui va le nommer. Il peut effectivement parler, il pourrait choisir son nom mais c’est comme ça par défaut. La parole commence à se dégrader vers 4.
2) il grandissent à vitesse 1:1, stagnent au palier 8 et rajeunissent ensuite

---

### [046] 2026-08-15 à 10:24

3. Oui, les gens qui comprennent pas les détestent et trouvent leur condition injuste par rapport à la leur. Les autres sont étonné mais en même temps ils voient bien que quand tu es trop petit, ton existence se résume à celle d’un bébé humain t1. Tu fais rien, on s’occupe de toi tout le temps, tu ne profite pas des premières année de ta vie. Ce n’est que plus juste que l’univers te donne la chance de grandir jusqu’à 8ans

---

### [047] 2026-08-15 à 10:39

Pour moi c’est essentiel qu’Elliot témoigne de ce qui lui ai arrivé. S’il est arrive voilé c’est bien car il n’était pas en paix avec lui même. En se confessant avant son entrée au jardin, il expie ce qui le faisait souffrir et entre dans l’insouciance. On peut supposer sans en être certain que les reliquats dispaissent quand on a rejoint le jardin. C’est la dernière grâce. Ça expliquerait qu il se confesse avant d’y entrer

---

### [048] 2026-08-15 à 10:44

Ok : ton paragraphe sur les 2 camps
« Les deux camps ont raison. Les jaloux ont raison qu’un corps jeune ne souffre jamais. Les autres ont raison que les toutes premières années ne se vivent pas — un tout-petit ne fait rien, on s’occupe de lui, il ne profite de rien. Ces années-là lui ont été prises aussi. Que l’univers lui rende la chance de grandir jusqu’à huit ans, c’est de la justice, pas un cadeau.

Personne ne peut gagner cette dispute. tout le monde y pense, la règle tient quand même. » et très it dressant, à conservé dans un coin de la tête

---

### [049] 2026-08-15 à 10:45

Tu peux validé ce qu’on s’est dit. Est-ce que sur le chantier actuel du as encore des choses à évaluer ?

---

### [050] 2026-08-15 à 10:50

1) l’arrivé sans les capsules tu veux dire ? Non tout le monde ne sait pas parler en arrivant (les moins de 4 ans) oublie les 5 ans. Et on a des arrivants de tout âge, 90 ou même plus puisque c’est un miroir à des plus petits de quelques semaines.. on oublie les question de grands prématurés, le lecteur se fera sa propre interrogations. Laisse moi finir de répondre à tes autres questions avant d’intervenir stp.

---

### [051] 2026-08-15 à 10:52

2. Oui. C’est ce qu’on disait, un arrivant vieux n’a pas de palier. Il a un ratio 1:1 de 90 à 8. Ensuite c’est incertain. On estime dans la moyenne 8 ans à vivre mais il peut tout aussi bien rajeunir plus vite ou moins vite. Comme un ancien chez nous qui flirte avec les 100ans

---

### [052] 2026-08-15 à 10:55

3.c’est pqs gênant. Mais il va falloir réussir à expliquer que le ratio  de rajeunissement n’est pas 1:1. Sinon le lecteur ne comprend pas qu’elles ont 15. Il fait le calcul : elle avait 18 ans il y a 10 ans a leur mort, elle devrait avoir 10. Ils seraient donc dans l’erreur

---

### [053] 2026-08-15 à 10:58

4. Il y a des pédiatres spéciale jardin tenue au secret médical. Les berceur et berceuse sont dans la confidence mais ce sont les seuls pour protéger les enfants. Rien ne dit qu’un jour. Quelqu’un ne rente pas de pirater les donnés pour savoir l’âge de chacun précisément. Après un enfant qui a 8 ans pendant x années, ça ne passe pas non plus inaperçue j’ai envie de dire. Bref ça pourrait etre une sous intrigue intéressante mais pas pour ce livre là ;)

---

### [054] 2026-08-15 à 10:59

J’ai pas fini, attend la réponse de la 5 avant de me poser d’autres questions !

---

### [055] 2026-08-15 à 11:03

5 les berceurs ne sont pas éternels ils sont relayé quand eux même rentrent au jardins. On va pas plus rentrer dans les détails mais disons que le berceur le plus jeune a 12 ans. Entre 12 et 8 ans ils sont affectés à des tâches plus simples

---

### [056] 2026-08-15 à 11:10

« garçon comme horloge » était utile quand le livre se basait sur plusieurs année ce qui n’est plus le cas. Donc c’est pas gênant. 
« « ils mettent trois fois plus longtemps à descendre, en plus. » j’aime bien mais mieux vaut que ça arrive de la bouche d’une personne banal et plus tôt dans l’histoire.

---

### [057] 2026-08-15 à 16:09

Le jardin est le dernier lieu de vie. Il englobe tous les enfants de 8 à 0, pas seulement les 8ans

---

### [058] 2026-08-15 à 16:12

👍

---

### [059] 2026-08-15 à 16:28

Juste par curiosité, si tu devais me faire un synopsis de notre histoire, elle ressemblerait à quoi ? Elle doit être accrocheuse. Oh et j’y pense aussi. Je pense qu on va éviter de parler dans le livre de vieillard et enfant. Bien sûr on peu parler de tissu vieillissant, de corps rajeunissant, mais je peux pas utiliser les mots enfant et vieillard. On restera surtout sur des arrivants de x ans. A et aussi, le nom de famille n’existe pas, mais dans notre société les veilleurs attribuent des chiffres pour faciliter l’administratif.

---

### [060] 2026-08-15 à 20:02

T’as pas mieux comme synopsis ? Le genre fait pas très 4eme de couverture ^^’ sinon le pitch

---

### [061] 2026-08-15 à 20:05

C’était juste par curiosité, on en est pas du tout à l’étape de la synopsis

---

### [062] 2026-08-15 à 20:14

J’aimerais qu’on retravaille sur la frise, car il y a beaucoup de choses qui ne vont toujours pas. Ça serait peut-être sympa de commencer par rajouter des encarts vide avec au moins un descriptif de scènes que l’on voit déjà, je parle pas de chapitre, je parle bien pour l’instant de scène. Par exemple on sait qu’on aura forcément la scène d’introduction avec l’éclaircie de l’arrivant de 10 ans, Éliott, on s’est également qu’il y aura la scène avec la cérémonie d’éclaircie d’Andrew, vu de son point de vue d’arrivant. On sait qu’il y aura une scène au commissariat le fameux lâche l’affaire, on sait qu’avant ça il y a une scène où Andrew en visite à June et Éliott. Bien sûr, il y a la scène de la découverte des jumelles dans un lieu sordide, il y a la scène de la découverte d’Éliott, dans un lieu s’également, il y a la scène de poursuite, il y a la scène avec les jumelles à la fin, etc. Ça serait bien déjà de commencer à créer donc ces encart la, et de réfléchir aux suivants

---

### [063] 2026-08-15 à 20:17

Pour la scène de la découverte des jumelles, j’aimerais que tu me notes qu’il y a deux références pour le style. Il y a la référence dans The Walking Dead quand Carole retrouve sa fille qui était enfermé dans la grange avec les autres. Ou alors dans le livre de Franck Tillier, il était deux fois, ou Gabriel retrouve Julie. Ils ont comme point commun que la scène porte le spectateur jusqu’au bout dans l’espoir que ce ne soit pas la fille de Carole ou Julie.

---

### [064] 2026-08-15 à 20:32

"La voie de Joël compte six cartes contre vingt et une. C'est peu pour un récit qui doit se lire à parité avec l'autre. Il en manque — probablement des fragments courts, disséminés, dans la première moitié." ou sinon on peut tres bien faire le deroulé de l'enquete en premier avec les différentes scène puisse que c'est l'objectif. ensuite on departagera les différentes scene de l'enquete de façon assez egalement entre les deux jusqu'au point de rupture où l'ont sait déjà qu'on a :scène de le decouverte de filles pour Joel, suivi de celle de la decouverte d'Elliot pour Andrew, puis la scène suivant ou on rebascule sur Joel avec la poursuite et enfin la scène de reveal pour Andrew avec le spectateur qui sait et andrew qui realise qu'ivient d'voir un reloquat de sa propre mort dans monde 1

---

### [065] 2026-08-15 à 20:40

"effroyable sans complaisance — ce qui fait mal, c'est la reconnaissance, pas la description." je te dis, la scène dans il etait 2 fois.. tout le chapitre, il la décrit mais elle ne ressemble plus à l'ado qu'il a connu. il y a une description horrible et plus on se rapproche de la fin du chapitre, plus on espère que la personne en écorchée n'est pas sa fille.. de souvenir, c'est la derniere phrase du chapitre qui nous achève après avoir eu son ressenti et son desespoir de décrit. alors qu'on s'attend un "pleur de soulagement, c'est n'est pas elle" la sentence tombe je memoire c'était un truc du style "il l'avait perdu, julie" et pour walking dead pareil.. on voit tous les zombie sortir de la grange. on espère en meme temps que Carole, puis la musique se lance, et lentement, une paire de chaussure qu'on reconnait, puis une démarche pas humaie.. puis la silhouette de l'enfant se detachant de ses nouveau congénères, Carole qui tombe à terre et crie de desespoir, plan sur sa fille, le regard vitreux, c'est la revelation qui a tenu tous les specateur en haleine, esperant et priant pour que la petite ne fut pas parmis les zombies enfermés dans la grange. deux scène tres poignantes

---

### [066] 2026-08-15 à 20:50

Bref, tu as compris l’âme que je veux donner à la scène. Que faisons-nous ? Est-ce qu’on essaye de créer le parcours de l’enquête ? Car pour l’instant nous avons juste Éliott qui semble fabuler, rien qu’en arrivant sur terre numéro deux, suivi des différentes visites d’Andrew. À la troisième visite, Éliott a déjà disparu, J est parti le déclarer à la police. Il sera au commissariat pour y retrouver Isaac par automatisme, les deux commencent à enquêter ensemble, et après ? Peut-être qu’il peut retourner voir June et lui demander si le petit a continué à dire des choses ? Peut-être qu’on peut ressortir, peut-être que le nom qui ressort c’est une personne qui déteste les arrivant jeune. Il peut peut-être y avoir une altercation avec ce dernier, sans que cela ne mène nulle part, car il a un alibi. Ce genre de scène pourrait ainsi poser les bases de pourquoi certaines personnes ne détestent autant. Ensuite, l’enquête peut continuer d’une manière ou de nôtres jusqu’à ce que l’on se retrouve dans une impasse, on a le fameux lâche l’affaire, puis un élément déclencheur qui va venir relancer l’affaire un peu comme le climax. Tout espoir semble perdu de le retrouver en vie, Andrew se retrouve au fond du fond, et il y a vraiment un élément déclencheur qui va le remettre en selle. Suite de l’enquête à définir, puis découverte du repères où Éliott a été séquestré. Tu remarques que je ne parle que du côté Andrew. Je pense que c’est peut-être comme ça que nous arriverons à ensuite partager les scènes entre Andrew et Joelle. Concrètement, la scène en parallèle sera identique pour Joël. C’est ensuite dans la façon d’écrire, en seulement des faux raccord par-ci par-là qu’à la deuxième lecture, on comprendra que c’était des chapitres appartenant à Joel donc que c’était bien des reliquats.

---

### [067] 2026-08-15 à 21:01

"« Lâche l'affaire. » sous entendu il est déjà mort : "lache l'affaire, a l'heure qui est, lers vers ont commencé le travail..."

---

### [068] 2026-08-15 à 21:40

"la réplique qui lui échappe, « c'est déjà ce qu'on m'a dit »" oui ça c'est bon, comme une migraine, quelque chose qui lui souffle un sentiment de dejà vue sans que ça soit trop obvious non je veux pas, ou alors justement :  soit dans la scène de la decouverte des jumelles quand ont decrit son desespoir , il se rememore cette replique, soit dans la poursuite de l'assassin et que toute sa rage, sa colère, tous ses pensées intrusives le nourrissent. ç ce moment là, Joel n'est plus lui meme, il veut pas poursuivre l'assassin pour l'arreter, il veut le buter comme si les jummelle auraient pu etre ses propres filles. il veut voir cette raclure morte. c'est un veritable taurreau qui voit rouge

---

### [069] 2026-08-15 à 22:07

"Sur Andrew, tu as raison : pas d'illumination. Comme une migraine. Il dit la phrase, et quelque chose se ferme dans sa tête — une pression, un blanc, deux secondes de trop. Il enchaîne. C'est le corps qui sait, pas lui." je suis d'accord

---

### [070] 2026-08-15 à 23:06

j'aimerais que tu m'aides à faire un jeu piste qui en plusde faire avancer l'enquetes nous fait decouvrir le monde, ses enjeux, son fonctionnement, etc.

j'avais comm début d'idée 

* Andrew rend visite à Eliott et June. une premiere fois, echange avec Eliott. ce dernier s'acclimate comme il peut mais semble très mal à l'aise. la seconde fois, il est retrouvé à bouder dans un coin. personne ne le croit et ça le blesse enormement. grosse discussion ils vont faire un tour. June peut sembler un peu dépasser par les evenements. elle peut peut etre evoquer une suspicion de voile sans oser le formuler car tabou en plus il est jeune. ce cas de figure, elle ne l'a jamais eu personnelement.
* à la 3eme visite, ça fait déjà 1 mois qu'elliot vis avec June. (note : June est une berceuse qui accueille les enfants bientot amenés à rejoindre le jardin. sa maison et voisine au jardin. elle s'occupe en general des enfants de +8 qu'elle accompagne et quand elle a du temps libre car les enfants sont au travail, elle aide ses consœurs au jardin pour les enfant de 8 et moins)
* June est partie voir la police entre temps et alerte Andrew de la disparition d'Eliott qnd andrew vient la voir croyant trouver le garçon: il ne serait pas rentré de son travail.
* Andrew va au poste de police, discute avec Isaac et en apprend un peu plus sur ce que June a rapporté mais que des trucs factuels, il pas allé au travail, n'en est pas revenu. il portait des vetements de type tatata, les horaire qu'elle lui a donné, le déroulé de la journée et c'est tout. Isaac ne parle a aucun moment du comportement du garçon. c'est Donc Andrew qui insiste pour aller reinterroger June.
* Il se rendent chez june. elle leur dit comme ça se passe, son etat d'esprit, il peut parfois etre adorable et d'un coup devenir hyper agressif. il a une peur bleue de l'eau et a refusé les premiers cours de natation donné aux arrivants " il s'est mis dans une colere noire, ça ne lui ressemblait pas" elle leur apprend aussi que la veille il est revenu avec les genoux en sang et la lèvre fendu. il aurait expliqué etre tombé mais elle est certaine que quelque chose n'allait pas au travail
* Isaac et Andrew se rendent sur son lieu de travail (et la pour le boulot, je seche!), parle avec le responsable, il y a un descriptif de la société. le responsable donne sa version, la veile Eliot était implqué dans une bagarre avec un certain [prenom], un homme de 22 ans. Il a vu l'homme commencer à parler mal à eliott et le bousculer à plusieurs reprise . il l'a congédié sur le champ après plusieur sommation quand l'homme a commencé à devenir insultant et haineux. -> futur petit prince pourri du jardin. le responsable semble un peu blasé comme si c'était pas la première fois que sa arrivait, c'etait une exclusion temporaire pour mauvais comportement. il dit ne pas pouvoir baisser ses effectif. autrement dire des marginaux il y en a partout, faut vivre avec en limitant les debordement. d'ou l'exclusion temporaire.
* Isaac interroge alors d'autres travailleurs ami avec le marginal absent et l'explication de leur point de vue tombe à se moment là
* suite à cette visite, Andrew retourne à la ruche. il va alors enqueter sur plusieurs ligne du registre : d'abord celle de l'homme, arrivant de 91 ans. puis sur la cérémonie d'éclaircie d'elliot. la journée de sa venue, à son heure du moins comportent deux données. une capsule défaillante, il s'en souvient pour avoir vu un collegue se faire bizuter et la capsule d'eliott. il relis le rapport pour chercher la moindre anomalie, capsule niquel, belle forme, belle couleur, elle est survenu assez vite. pas  developpement. c'était une capsule non prémiditée.
* en parallèle au telephone, Isaac a fait des recherche sur l'homme. Andrew lui partage ses infos. Isaac détaille la vie de l'homme, il a eu plusieurs altercations donc certaines ont dérapés. il a fait quelques jour au silence (cellule temporaire) après avoir essayé d'empêcher avec un groupe d'autre marginaux, l'entrée au jardin d'un groupe d'arrivants de 6 ans. (comme une manifestation)
* Andrew qui a le registre encore sous le nez, évalue rapidement le groupe : un groupe de 23 arrivants de 6 ans, un de 44, un autre de 39 un dernier de 61. a ce moment là. c'était une cérémonie assez grandiose, 26 arrivants simultanément. le veileur s'étant chargé de la cérémonie était désormais au jardin. mais agé de 8 ans. il était alors tout à fait possible d'aller l'interogger sur ce fait exeptionnel.
* Andrew et Isaac se donne rdv au jardin : ils rencontre le veilleur de l'époque. il decrit un peu plus la ceremonie, les reactions du public.  il n'y avait visiblement pas assez de berceur/berceuse de jour là, se souvient-t'il la ceremonie a meme pris du retard car du point de vue de l'administration, il a fallut les enregistrer un a un pour les faire directement basculer dans le jardin. en discutant avec l'ancien veilleur, on apprend que le marginal faisait partie du public. etant donné que le transfert s'est passé dans la meme journée.. le marginal a enflammé ses petits copains pour aller mettre le bazard à l'entrée du jardin. cette scène permet aussi de décrire le fonctionnement du jardin, et l'attitude preque d'estructrice des marginaux, dans un lieu d'innocence et de paix...
* isaac et Andrew se rendre directement chez l'homme. il est là mais veut pas leur parler. il lest envois chier en leur disant qu'il a un alibi en béton
* l'alibi se confirme, c'est une fausse piste.
* idéalement, il faudrait que l'enquete reprenne sur un autre détail, une autre piste qui prend du temps.. elle menerait alors à une second fausse piste leur ayant fait perdre enormement de temps... isaac commençant à compter les jours à ce niveaux là
* le fameux laisse tombé, après 2 semaines compté de disparition
* issac qui lache l'affaire, et laisse Andrew seul sur l'afaire
* rebondissement apres enquete en solo, il trouve la planque, appelle Isaac pour qui le rejoigne vite
* il entre seul dans la planque sans attendre
* il retrouve Elliot, a ses reliquats, realise sa propre mort..isaac les a rejoint entre temps, une berceuse menottée déjà prete a etre embarquée. et oui, c'était la ravisseuse etait une berceuse.. elle a passé sa vie au contact des enfants.. il faudra chercher ses motivations

---

### [071] 2026-08-15 à 23:16

* le portage, j'aime beaucoup l'idée.
* "On les fait travailler pour que le reste du monde le supporte." franchement ça peut etre une phrase du responsable quand on lui demande pourquoi la reaction du marginal ne lui fait pas plus d'effet que ça, avec en opposition, çon point de vue sur les enfants assez neutre.
* je comprends pas le smotifs que tu as trouvé pour la berceuse. elle serait devenue folle avec le temps ?

---

### [072] 2026-08-15 à 23:25

* milieu haineux est effectivement une fausse piste ;)
* Le mois entre l'arrivée d'Eliott et sa disparition : je valide le temps du livre
* "La suspicion de voile de June" oui, je pense que ça peut amener quelque chose et aussi ça explique au lecteur ce qu'est un arrivant voile. j'aimerais aussi modifié l'appelation partout. on va dire "arrivant porteur de voileS". arrivant voilé, c'est trop conotté. "un porteur de voiles de cet age.. je n'en avais jamais vu"
* tu as tout compris pour le responsable.
* pour la berceuse, oui j'aime bcp l'idée de l'amour possessif. c'est le mental qui lache, mais bon... de la a enlever un enfant.. c'est qu'elle a un peu sombre dans la folie quand meme, tu ne trouves pas ?.
* Que penses tu de créer une deuxième fausse piste ? moi je le voyais de sorte pour isaac que sa fait déjà 2 fois qu'ils se plantent, il lache l'affaire, non pas par resignation mais par objectivité, là pour Andrew ne veut pas. c'est un peu le point culminant du recit. quand tout semble perdu, une petit truc et hop sa repart. ça a un nom au cinéma, j'ai oublié. quand le heros est au plus bas et qu'un element declencheur le relance. et si c'était un reliquat qui le relanssait justement ?

---

### [073] 2026-08-15 à 23:27

donc une ravisseur de genre 12/14 ans ?

---

### [074] 2026-08-15 à 23:32

ah oui ça s'est certain, je suis d'accord avec toi, le relicas n'apprend rien, simplement un tic, une manière qui dans monde 2 lui donne une revelation mais corporel qui va l'inciter à avancer ensuite. ton idée sur la berceuse de 13/14/16 ans me convient. qu'il l'ait juste écouté et suivit, ça me va aussi. je valide

---

### [075] 2026-08-15 à 23:38

ça me semble bien mais deux semaine de perdues, va falloir reussir à comble le vide... et qu'est-ce qui ferait que c'est une autre piste ? et comment le dossier peut etre faux ? on pars du dossier du registre ? c'est impossible

---

### [076] 2026-08-15 à 23:40

le fait que ça ecarte le jardin pour mieux y revenir je trouve ça bien comme idée. un peu comme "c'était là sous nos yeux depuis le début !" il pourrait lancer ça à Isaac au moment de l'appeler pour lui dire de se rendre à la "planque " qu'il a trouvé qui est en fait une maison tout simplement, mais la porte qu'il ouvre et qui est un mouroir pours les filles, serait une cave réaménagé en chambre d'enfant colorés.

---

### [077] 2026-08-15 à 23:42

je valide cette nouvelle version, le secret et le creux narratif. on est sur la meme longeur d'onde

---

### [078] 2026-08-15 à 23:46

"Elle vit à cent mètres de chez June. Andrew est passé devant sa porte à chacune de ses trois visites.

Ce n'est plus une formule de fin d'enquête, c'est un fait : il a marché devant cette maison en allant voir le petit, trois fois, et il n'avait aucune raison de la regarder." phrase a garder

"Ce qu'Eliott a dit" c'est à dire ? la revelation à la fin avant le jardin ? si c'est ça, rien a voir. sa révélation a la fin, c'est de comprendre qu'il est mort assassiné. il est mort noyé. la ou je coince desormais, c'est comme son agresseur a pu mourrir aussi vite derriere :/

---

### [079] 2026-08-15 à 23:57

ou alors... on rebouge l'histoire... soit effectivement c'est un assassinat, soit c'est une histoire moins sombre. le jour de l'arrivé d'Eliott, il y a un autre arrivant, d'une quarantaine d'année. Je m'explique. Pas de capsule pourrie ce jour là. il peut très bien avoir vu la scène du bizutage un peu plus loin ou plus tôt n'importe. et la capsule pourrie qui révèle que c'est un assassin...en soit, la ligne des jumelles, du veilleur et de l'assasin dans le registre sera là pour le dévoiler. A la fin du livre, ça peut etre le temoignage d'un accident bete et mechant : une randonnée de prévu entre pere et fils qui tourne mal quand il tombe à l'eau et que le courant l'emporte. son père a essayé de le sauvé et s'est noyé à son tour. fin de l'histoire. le pere, en soit ne doit pas intervenir plus que ça dans l'histoire. ça aurait pu etre le cas si le temps du livre avait été plus long, mais là, par defaut ils sont affecté à deux endroit différents, elliot reste un arrivant sous la surveillance d'un arrivant plus experimenté.. il n'y a aucun moyen qu'il se soit rencontré. mais par contre, peut etre qu'il peut buguer silencisuement qu'en il voit le recond arrivant a coté de lui lors de la ceremonie. quelle versionne preferes tu ?

---

### [080] 2026-08-16 à 00:03

"Une seule chose à protéger : Andrew ne doit jamais faire le lien. Il entend, à la fin, une histoire d'eau et de courant. Il ne va pas vérifier qui d'autre est arrivé ce jour-là. C'est le lecteur qui se souvient de l'homme debout à côté du petit, à la première page — et personne dans le livre ne le saura jamais." 100% d'accord. 

et oui le bug silencieux doit se comprendre à la première lecture comme "il dévisage le second arrivant dans sa capsule" à la second, il dévisage une personne qui lui fait penser à quelque qu'il connait déjà : son père. meme à la revelation il dira pas le mot papa, il evoquera un sentiment, "il m'aimait bcp, un sentiment fort, très fort. j'avais l'impression qu'il etait moi et que moi j'etais lui. comme si je l'aimais encore plus fort que lui !"

---

### [081] 2026-08-16 à 00:09

resume moi hyper concisement l'histoire de l'enquete stp, je lis à kevin

---

### [082] 2026-08-16 à 00:18

"il m'aimait bcp, un sentiment fort, très fort. j'avais l'impression qu'il etait moi et que moi j'etais lui. comme si je l'aimais encore plus fort que lui !" garde cette phrase

---

### [083] 2026-08-16 à 00:30

dernier note  : la fausse piste n°2 : l'autre enfant n'est pas mort ou disparut, il ecoule ses dernieres année tranquillement dans le jardin, il a 3 ans. scène qui peut developper le fonctionnement de la fin de vie. pourquoi pas aussi assister à la mort naturelle d'un 0. tout en douceux, porté par une berceuse, c'est son métier, des geste professionnels etc.

---

### [084] 2026-08-16 à 00:35

on peut valider cette idee pour l'instant, on y reviendra

---

### [085] 2026-08-16 à 00:51

On va créer un nouveau document (format html / n'hésite pas a installer des lib js pour les animations; tous les schémas ne se feront qu'en SVG - tu as le droit d'utiliser three.js)

* Il devra répertorier les annotations que tu juges importantes de nos conversations (l'idée, c'est que j'aimerais ne rien perdre : meme si cela semble insignifiant, on note, je jugerais de sa pertinence après la production du document 
* Il y aura plusieurs 'écran' dans ce document :
   * Le principal : ca doit un écran chronologique (vers la droite) : (comme dans le jeu Detroit - fait des recherches sur le net) ;
   * Ca doit reprséenter les grandes "scène" : l'idée de cet écran et de m'aider a élaborer les chapitres du livre (si je clique sur la scene : je peux avoir un écran ouvrant indiquant les détaisl référence et/ou les notes qu'on s'est dites)
   * Je te laisse me proposer pour les autres écrans : des écrans utiles (glossaire et ou autre idées)
* 

Tu es en full autonomie cette nuit (je vais domir) : produit un truc vraiment carré : c'est censé ^etre mon outil pour commencer a écrire des demain les premiers chapitre :)

---

### [086] 2026-08-16 à 01:40

la molette doit pouvoir faire le scroll horizontal stp 🙂 ; possible de mettre un thème clair aussi ? Tu as bien tout synthésiser / répertorier ? ; pourrais tu avoir une section : "chapitre" et proposer un prologue ? Style d'écriture Franck Thilliez, mm si ma femme va surement tout réécrire :)

---

### [087] 2026-08-16 à 01:55

Ton role sera de maintenir ce document a chaque décision / échange 🙂 ; tu as le droit de créer des release de cette docu ou des productions qu'on fait sur git. Tu pourras t'en servir pour remonter ou versionner des documents.

Concernant le chapitre, ca manque cruellement de description des lieux, des personnages, l'ambiance générale de la scene, tou tva bcp trop vite

---

### [088] 2026-08-16 à 02:04

Alors je sais que c'est particulier comme exercice pour toi ; mais on commence rarement par une description type "lycée" d'un chapitre. Faut construire, percuter le lecteur : une action ? une parole / et après on décrit : faut que ce chapitre soit accrocheur est très bien écrit. Inspire toi de Franck Thilliez

---

### [089] 2026-08-16 à 02:11

ça me semble bien court en longueur pour un prologue

---

### [090] 2026-08-16 à 10:24

"Vingt-trois arrivants de six ans basculés directement au jardin contredit la règle qui pose qu'on entre au jardin à huit ans et qu'en dessous on grandit ailleurs. Le jeu de piste tranche de fait une question ouverte : à confirmer, ou corriger la scène."

on entre dans le jardin à partir du moment où on a 8 ans. on y es par defaut quelque soit l'age entre 8 et 0, que l'on soit entrain de grandir ou de rajeunir

---

### [091] 2026-08-16 à 10:53

ta scène 17 peut se scinder en 3 blocs. 1er bloc, Andrew enquete, il se fait des noeuds au cerveau, est un peu desespéré mais fait comme il peut. 2eme bloc, on est coté Joel. dans sa version, il est rentré chez lui, dépité. il s'affale sur son canapé, fait des trucs assez banales. c'est un abandon complet MAIS qui ne doit pas etre interprété comme tel par le lecteur !! noooooonnnn jeune ami !! le lecteur doit croire qu'on est toujours coté Andrew avec juste une fin de journée erintante, il fait une pause dans son affaire après tous ses noeuds au cerveau... 3eme bloc, on rebascule coté Andrew qui a trouvé la solution. la scène suivante (18) découle naturellement côté Andrew Toujours. Tu l'as bien noté, on reswitch coté Joel avec la decouverte des corps et la scène t'après on reswitch et on revis la scène avec Andrew et Eliott

---

### [092] 2026-08-16 à 11:02

pas d'accord avec le denouement : la scène recommence, Andrew vient de retrouver Eliot. Isaac les rejoint. il sent pourtant une présence derrière eux. Une silhouette apparait. fin du chapitre

chapitre suivant,  la silhouette prend la fuite. sans reflechir, il s'élance à sa poursuite. une rage, la colere, l'envie de tuer  "Joel attend !!" la poursuite, la mort.

on revient ensuite coté Andrew. Qui réalise sa propre mort. il observe dubitativement la berceuse qui a compris qu'elle été prise sur le fait. elle n'a pas tenté de s'enfuir.. elle semblait juste profondément triste. Isaac lui passe les menottes

---

### [093] 2026-08-16 à 11:17

"Aucune phrase de renoncement. Pas de « il n'y retournerait pas », pas de dossier qu'on repousse, pas de décision.
Et aucune phrase de repos non plus. Pas de « il avait besoin de souffler », pas de fatigue commentée." completement d'accord. un quotidien banale, juste une ambiance lourde d'un type fatiguée mentalement. 2 lectures : fatiguée par la situation qui est avorté, fatigué par la complexité de l'enquete qui n'en finit pas.

"mieux vaut que le lecteur n'ait jamais vu le logement d'Andrew avant ce chapitre, sinon il compare". c'est prévu.
 
Que fait Andrew de cette revelation... et bien elle le frappe en plein fouet bien sur. est-ce que ce serait pas le meilleur moment pour qu'il consulte le registre ? soit ça, soit il se remémore un details de la cérémonie, des phrase qui n'ont pas été dites, du moins qu'il n'a pas jugé bon de se souvenir à la premiere description. cette fois, la scène, plus breve, moins concentré sur lui meme ou les capsules des paires. un detail, quelque chose qui a entendu mais qu'il n'a pas réalisé sur l'instant. un veilleur qui précise dans le registre  que les capsule était prévu pour les paires (agonie lente monde 1) mais que la sienne ne l'était pas.


peut etre que la premiere scène aurait cette tete là :
"bienvenue à tous" // il se reveille comme d'un profonds sommeil, il entend des voix etouffée, il est aveuglé par la lumiere au debut, blablabla puis on s'adresse à lui. Quel sera ton prénom. comme veux-tu qu'on t'appelle pour te designer ?

et ici : "bienvenue à tous; la ceremonie du jour nous offre 3 arrivant au lieu de 2. le troisième nous ayant suspris pas sone eclaircissement inopiné. on s'adresse à lui Quel sera ton prénom. comme veux-tu qu'on t'appelle pour te designer ?

et c'est aussi en se rememorant ce moment eclipser de sa memoire qu'il peut se souvenir de quelqu'un au loin parlant d'une odeur horrible. comme si un shi fu mi silencieus s'était joué chez les veilleurs. un veilleur s'est occupé des arrivants et l'autre à nettoyer la capsule pourrie pour ne pas entraver la cerémonie par l'aspect infame de la capsule. 

qu'est-ce qui te semle le plus pertinant, il retourne au registre et lis 3 arrivant et un capsule non eclaircie ou il se souvient de la scène une seconde fois et on met l'accent sur ce qu'il lui a echappé la premiere fois ?

---

### [094] 2026-08-16 à 11:27

sisi , les deux autres étaient attendue. et donc suite à ça, il retourne consulter les registre et il voit la ligne en question ? et donc est-ce que ce serait pas ça qui le pousserait à retourner voir l'enfant plus tard ? pour peut etre comprendre justement qui aurait pu etre cette personne pour lui, arrivé en meem temps que lui

---

### [095] 2026-08-16 à 11:34

je pense que pour définir le parcours, on a nots scènes bien defini, de quel point de vue elle se passe. quand c'est Andrew, on place la scène sur la ligne d'Andrew, quand c'est joel, on place sur la ligne de Joel. Le tronc, c'est un petit encart, leger qui annonce les etapes. on peut le commencer au moment ou l'on sait que ça va se dédoubler, le comissariat. on aurait donc la scène coté Joel et un encart du tronc, un truc generique : premiere visite au commissariat. coté Andrew, on a une scène grisée juste pour savoir ou on en est, il rencontre Isaac pour pour discuter avec lui de l'affaire. 

au passage, comme c'est la premiere rencontre avec Isaac, on peut supposer que c'est June dans la scène d'avant qui dit avoir discuter avec un certain Isaac et Andrew lui repondre, c'est un bon ami, je aller lui parler. On croit donc faire la description d'Isaac, mais c'est en fait la description de l'ami de Joel

---

### [096] 2026-08-16 à 11:43

nan je pense qu'il faut etre plus subtile que ça.. il parcours le registre qui lui confirme son souvenir. et on stop là. elipse temporelle. comme si on etait arrivé à l'épilogue. il lui reste 2 taches : 

* rentre visite aux filles

* puis petit saut dans le temps : pourquoi pas une derniere description : comme se deroule une arrivee au jardin. a reflechir. Andrew fini en tete à tete avec Eliot quand June fait ses adieux et s'en va en lui souhaitant  le meilleur. c'est à ce moment la qu'on fini sur sa replique. je trouve que c'est la meilleure  fin possible. l'arc d'Andrew se termine le chapitre d'avant, la reponse pour Elliot c'est la toute fin. le lecteur ne doit pas se sentir triste de son sort. il va vivre heureux au jardin. il est meme tres enthousiaste. ça doit contraster avec sa revelation mais sans que cette derniere soit trop brutale. oui, sa fin sur monde 1 est irrévocablement triste à en pleurer. mais l'amour reste et sa derniere phrase en est le temoin

---

### [097] 2026-08-16 à 11:50

"l'affaire sorel" justement, cet encart n'existe pas vraiment, tu le regroupes avec la scène 4. on ne parlera pas vraiment de fragment, on ne discute pas de l'enlevement des jumelles.

---

### [098] 2026-08-16 à 11:59

"Retour chez un témoin" : c'est leur mère. le parallèle de June s'est la mère des jumelles.

'sur son lieu de travail" pareille, on peut peut etre supposer une sortie de fac, le responsable est un surveillant, les marginaux sont un groupe de bad boys lourds. le marginal aime semet la merde, c'est un peu l'équivalent d'un casseur dans les manifs pour troubler l'ordre public

scène 8, retour à la ruche, c'est un retour dans le service de archives du commissariat, 
au telephone, c'est mael qui donne des infos
"au jardin le veilleur de l'epoque" : visite d'un ancien policier chez lui, présent le jour d'une manif qui a degenérés. 

" il se fait des noeufs au cerveau" 17aet 17c : Joel a trouvé une piste seul après avoir perdu enormement de temps

"il sentre seul, sans attendre" : pareil coté Joel

---

### [099] 2026-08-16 à 12:07

nan, ça c'est bon, il n'y aura pas de scène de ce coté là. c'est à titre indicatif. tu peux laisser mère

---

### [100] 2026-08-16 à 12:14

* "les autres travailleurs" -> les potes du type.
* j'ai dit Mael ? non c'est Liam pardon. On n'a pas de Mael dans l'histoire
* scène 10 : encore une fois les encart non ecrit sont pour moi et rien n'y sera forcement relié. Tu peux dire, accident d'un groupe d'enfant avec leurs accompagnant adulte.
* j'ai du mal avec la scène 14a. qu'est-ce que tu appelles le refus au comptoire ?

la scène du screen, elle est censée se trouver entre les deux scènes du haut, pas en dessous de la 14b

---

### [101] 2026-08-16 à 12:19

juste petite apparté : certes les berceurs et berceuses sotn payés pour s'occupé des petits 8 - 0, mais c'est un peu l'équivalent des assistantes maternelles elles offrent aussi de la douceur et de l'amour. c'est toujours une mini dechirement quand l'arrivant atteint 0, on lui dit aurevoir pour la derniere fois. là ou notre monde c'est la vie c'est comme ça, le petit rentre à la maternelle, ils ne le reverront jamais, ici il ne va nulle pas, il est innocent jusqu'au bout et ils ne le reverront plus jamais. la dernière berceuse c'est un peu le dernier acte d'amour que peut prodiguer un ou une berceur(se)

---

### [102] 2026-08-16 à 12:25

"La seconde piste — on lui refuse le dossier" il irait demander l'info ou ? il a un dossier de l'arrivant et il pourrait savoir quel service medical l'a pris en charge? peut etre que le coté tres secreatariat lui dirait alors non et qu'il deciderait lui meme d'aller voir la pediatre en charge de cet arrivant et qui exerce au jardin ? il aruait alors pu soutirer que 2 infos : par qui l'arrivant a été suivi et que fais elle maintenant mais avec un refus catégorique sur la demande du dossier de l'enfant ? c'est alors avec la presente d'isaac que la(le) pediatre pourrait parler du dossier, de l'erreur administrative, contrainte d'en parler face à la pressence d'un policier

---

### [103] 2026-08-16 à 12:29

Est-ce la même personne qui les dit tous les deux ? pas forcément, June continue a s'occupée d'elliot jusqu'à son arrivé au jardin, elle delgue ensuite à une collegèe du jardin? June doit avoir environ 22 ans. le temps qu'elliot passe au jardin, dans l'epilogue elle a rajeuni egalement, mais pas suffisamment pour entrer elle aussi au jardin

---

### [104] 2026-08-16 à 12:37

Fiche neuve : la pédiatre du jardin. non, on peut l'accompagner, la discussion peut sembler naturelle. elle eest très occupé et nous propose de la suivre en meme temps qu'elle repond à nos questions. c'est en passant de manière impromptue devant une salle avec un tout petit sur le point de disparaitre qu'Andrew peut s'arreter pour observer. la pediatre sait que c'est rare de voir ce genre de scène quand on est exterieur au jardin, elle laisse passer, on a le temps de decrire, les gestes, les emotions, comme si tout le monde se concentrait sur ce qu'on voyait (Andrew, Isaac, La pediatre) alors qu'on decrit une scène hors du temps? la berceuse, en tete à tete avec le tout petit. une scène presque mère enfant dans une grace et un amour profond. et on garde l'idee que justement la berceuse serit la coupable avec un leger détail : "elle le bercé, au rythme de sa chaine autour de son cou, symbole de sa foi" et derniere scène, "elle tritura son colier hesitant, avant d'enfin tendre ses deux mains en avant pour le passage des menottes".

ce n'est pas la pediatre qui refuse de parler à Andrew, c'est un service administratif, comme une sorte de secretariat. il accepte de donner le nom du pediatre et ce qu'il fait maintenant mais refuse de dire d'avantage.

au jardin, La pediatre est un peu sur la reserve, mais quand elle comprend qu'elle a affaire un policier, elle ccoopere normalement.

---

### [105] 2026-08-16 à 12:44

non, mais le lecteur observateur se dira que peut etre que cette berceuse qui bercait l'enfant etait la meme que celle arreté. il faudra faire une fiche pour la berceuse coupable aussi. et la pediatre sera un pediatre pour ajouter un petit peu de parité. j'ai peur que comme ce qui se passe dans notre monde, les métiers touchant à l'enfance soit trop connoté pour les femmes, j'ai envie d'un peu de changement ^^

---

### [106] 2026-08-16 à 12:50

"Le secrétariat refuse" je nomerais plutot cette partie comme départ de la seconde enquete". elle équivaudrait pour Joel a une seconde affaire de disparitions, deux jeunes filles du meme age disparues quelque annees auparavant dans la meme region, un cold case qui en fait n'en était pas un, les deux jeunes filles sont bien vivantes, mais les dossiers n'ont jamais été correctement classifiés coté administratifs

---

### [107] 2026-08-16 à 12:55

justement Andrew a une piste, un nom, un lieu. il peut prévenir Isaac et se donner rendez vous au jardin

---

### [108] 2026-08-16 à 13:00

ça c'est la meme colonne

---

### [109] 2026-08-16 à 13:06

"« la paire du début, qu'est-ce qu'elles font là ? » ne s'accroche à rien" "fait doublon" je suis pas d'accord avec toi. la ceremonie d'Andrew pose cette particularité "elles sont pareilles, blablabla". la "seconde" cérémone n'est pas là pour redecrire tout, elle décrit ce qu'andrew a ommis à sont premier souvenir. ce qu'il pensait ne pas avoir entendu, ce qu'il pensait ne pas avoir senti.

---

### [110] 2026-08-16 à 13:16

on pourra rajouter une scène pour Joel ici. on le voit acculé. c'était evidemment une fausse piste. c'est une scène de lassitude, enervé d'avoir bien sur perdu du temps.et pourtant, il pense que ça vaut le coup de continuer ! et il decide de retourner au commissariat pour parler avec son ami // ensuite c'est la 15a et on rebascule bien sur Andrew qui insiste avec Isaac

---

### [111] 2026-08-16 à 13:19

je valide pour la place de la capsule non eclaircie. faudra arriver à l'integrer parce que j'ai du mal a voir comment.. ou alors c'est un journée type pour Andrew ? une descrption du levé au soir ?

---

### [112] 2026-08-16 à 13:21

nan on s'est mal compris, tu me fait sauté l'encart "il n'a plus rien 14abis" et tu intercalle la 14d

---

### [113] 2026-08-16 à 13:26

visuellement, la scène 14 c ne doit pas etre au dessus de la 14 d. la 14 d soit succeder à la 14 c. et pourquoi y il y a plein de point rouge ?

---

### [114] 2026-08-16 à 13:36

franchement cette scène sert à rien, il se retrive déjà de l'affaire quand il largue Joel.

---

### [115] 2026-08-16 à 13:38

et la scène "il passe outre peut se regrouper avec la scène "il se fait des noeuds au cerveau" quelque chose a retenu son attention dans le dossier, il decide d'y reflechir au calme après sa conversation houleuse au comissariat

---

### [116] 2026-08-16 à 13:46

= nouvelle piste

---

### [117] 2026-08-16 à 13:50

donc quoi ? j'aimbien le fait qu'il repart voir June, sans il ne sait meme pas quel espoir. il y  va a pied. on peut donc insufflé l'idée que de dans ville il se rend à la rush constemment a pied car il n'a pas de voiture et les seules fois oùil prend une voiture, c'est qu'Isaac lui a proposé de venir avec lui pour aller sur les différents lieu (travail d'eliott ou jardin). mais ton argument n'est pas logique. il y a va bien a pied les premieres fois qu'il rend visite a eliotte

---

### [118] 2026-08-16 à 13:57

"la meme scène joué deux fois, je veux l'encart vert et pas violet" pour le différencié du préédent

---

### [119] 2026-08-16 à 13:59

donc il resterait dans la rue et qu'est-ce qui ferait ? pourquoi il penserait a cette maison en particulier ?

---

### [120] 2026-08-16 à 14:03

enleve moi ce point rouge, je le comprends pas.. et si tu peux alleger la description, elle est compliqué, du gras de partout, on perd l'essentiel

---

### [121] 2026-08-16 à 14:05

mais il dirait quoi le gamin ? pour qu'il tique ?

---

### [122] 2026-08-16 à 14:08

ben désolée mais "— Elle, elle fait comme June. Elle m'a dit bonjour." n'est pas un argument assez fort pour expliquer le fait qu'il soit chez elle...

---

### [123] 2026-08-16 à 14:16

par contre, là ou sa pourrait etre interessant, mais ça change notre lecture de la scène. il aperçoit en deambulé, de façon tres rapide la berceuse à travers une fenetre donnant sur l'interieur de sa maison. il l'a reconnait, elle était au jardin, elle bercait le petit. peut etre que dans la scene du bercage, quelque chose d'anormal l'aurait frappé. on disait que les berceurs devait etre pro. peut etre que justementl celle ci etait différente. "allons allons, pourquoi pleurez vous ?" lui lance le pédiatre, emplit de compassion mais toujours aussi professionnel. un pressentiment, il est sur le point de venir frapper à sa porte. comme une intuisson, son coté analytique et observateur de flic qui reprend le dessus. il sonne mais peut etre qu'elle decide de pas ouvrir, alors qu'il sait qu'elle est là. il appercoit alors la lumiere s'éteindre brusquement, une action ridicule comme pour faire croire qu'elle  n'est pas la mais trop tard... il decide alors de contourner la maison, un abri ou une remise exterieur, ou les porte d'une cave qui mene sous la maison. un cadenas dessus. je sais pas... comme une supposition. ce jour là, il n'a pas retenue son visage au jardin. il n'a retenu qu'un sentiment, son attention focalisé sur le bébé. c'est son instinct qui le pousse à la rencontrer

---

### [124] 2026-08-16 à 14:23

ou alors, le jour de la scene 14, elle se confond en excuse pour avoir pleurer "je heu.. pardon" il entend sa voix, l'assimile mais c'est tout. et en deambulant, il lui rentre dedans sans faire attention. elle s'excuse aussi, tres vite, trop rapidement pour etre innocente "p..pardon" et elle se sauve activement non sans se retourner comme si elle avait quelque chose a se reprocher et effectivement, elle a quelque chose a se reprocher, et en reconnaissant Andrew, elle est mal à l'aise, elle l'a appercu avec le flic au jardin.. alors qu'Andrew aurait pu passer outre car il ne l'avait pas reconnu, son attitude etrange mêlé à sa voix qu'il se rappelle le font tiquer. soit il la suit directement, soit il decide de creuser rapidement. il retourne au jardin, devant a voir la berceuse de l'autre jour, on lui dit qui c'est mais on ne peut pas donner son adresse. le lendemain il l'a prend en filature. ca serait elle qui ne s'achant pas qu'elle est suivit le mene tout droit à eliot. peut etre meme que le lieu est un autre lieu et non sa propre maison. dans tous les cas, il attend qu'elle s'en eloigne et appelle son collegue lui expliquant qu'il pense avoir trouver quelque chose

---

### [125] 2026-08-16 à 14:29

on peut faire sauter la remarque d'eliot si elle est pas utile

---

### [126] 2026-08-16 à 14:33

je suis pas sur aussi du fait de se rentrer dedans.. est-ce qu'on pourrait pas dire justement qu'en se remémorant les paroles du gamin "ici il y a avec un magasin de chaussure, pas une epicerie" il se decide a rentrer dans l'épicerie en question ? il flane dans les rayons et passe en caisse. la personne devnt lui semble nerveuse, elle fait tomber des pieces de monnaie, "heu.. pardon.." il l'aide a ramasser la monnaie, leur regard se croisent, micro blanc. elle montre des signe de nervosité qu'elle essaye de contenir, finit de payer mladroitement et sort en deux deux de l'épicerie

---

### [127] 2026-08-16 à 14:46

tu m'as mis à jouer les cène dans le dossier le parcours ?

---

### [128] 2026-08-16 à 16:01

je valide l'ecriture de l'épicerie. on a souvent parlé de l'enfant qui se plaint qu'il y avait une epicerie a tel endroit et que c'était desormais un magasin de chausure, tu t'en douteras, j'ai reverse la formulation et il faut la reverse partout. magasin de chaussure, c'était monde 1 , l'épicerie c'est monde 2. 

petite ajustement, quand elle dit pardon dans la boutique, elle s'adresse au caissier, c'est un peu un miroir de ses excuses qu'elle a lancé au pediatre. il relis la meme scène deux fois sans le savoir.

pou l'entrée au jardin, Eliott peut relancer Andrew. Petit moment de blanc, June vient de partir. on ne sait pas qui va parler le premier et c'est Eliott qui brise le petit silence. Il le remercie pour son aide mais de maniere plus large. il le remercie de l'avoir cru. ça peut etre le fait qu'il realise qu'Andrew a toujours été de son coté qu'il décide d'enchainer. il n'a aucune crainte avec Andrew. il sait qu'il ne se moquera pas et il décide de raconter une derniere chose, "tu n'as jamais eu cette impression toi, de rêver en plein jour ?" et il peut enchainer avec des phrases de ce monde sans reussir à les vraiment les exprimer : "j'ai senti le sol de dérober sous mes pieds alors que ne bougeais meme pas", "j'avais les yeux ouverts et je pouvais sentir l'eau dans ma bouche. " "j'ai jamais vu une rivière, je savais pas ce que c'était un courant avant que je l'apprenne à l'ecole. et j'ai r^vé que j'ai pourtant imaginé que tombais dedans" "l'arrivant qui etait à coté de moi lors de ma ceremonie. j'ai rêvé de lui aussi. il me tendait la main mais j'était incapable de l'attrapper. nos mains l'un est l'autre glissaient trop" "je ne sais pas pourquoi mais j'avais tres peur, autant pour moi que pour lui alors que je le connaissais meme pas" rajouté à la derniere phrase sur le fait que ce soit un lien fort.. tous les phrases ne sont pas à prendre en l'état, mais tu vois ou je veux en venir. il pourrait sortir "et maintenant, je fais quoi avec ça ? tu crois que les autres vont se moquer de moi ici aussi ?" "est-ce que tu viens me rendre visite au jardin?"

ça pourrait etre des questions assez fortes. que faire des ces voiles ? est-qu'Andrew aurait une réponse.

"Tu sais, j'ai déja rencontrer quelqu'un qui comme toi se posait beaucoup de questions. il m'a appris " tu vois un peu l'idée, comme s'il parlait de sa propre histoire
"Il s'appelait comment ?"
"il s'appelait Joel"

ça peut etre un clin d'oeil a sa vie d'avant, dis moi ce que tu en penses. dans tous les cas, La boucle d'Andrew s'est terminé avant. maintenant l'objectif et de rassurer Eliott. il s'apres à rentrer dans un lieu d'innocence, c'est le meilleur qui pouvait lui arriver.

---

### [129] 2026-08-16 à 16:15

' c'est à dire ?" si tu devais me creer le dialogue que tu as en tete ? oui, il peut se souvenir de son père. en fait, il peut meme avouer a demi mot que c'est le premier reve qu'il a eu l'impression de faire en voyant l'autre a arrivant. il n'était pas dans la ruche. quelqu'un  l'aider à enfiler un gros sac sur le dos, l'homme, une femme lui deposait un baiser sur le front.

---

### [130] 2026-08-16 à 17:03

on peut faire l'ecriture ici avant de valider ? ça fait pas très bouquin ton truc, il y a des tiret partout. j'aime beaucoup le fait dévoquer qu'ils sont sur un banc. je trouve que c'est bien qu'andew ne parle pas tant. son arc est terminé, c'est au tour d'eliott.


June était partie depuis un moment déjà.

Elle avait dit ce qu'elle avait à dire, elle l'avait dit vite, et elle était sortie sans se retourner parce que se retourner *aurait tout défait* (approfondis?). La femme qui prenait la suite s'était éloignée de quelques pas — assez pour laisser de la place, pas assez pour disparaître.

Andrew était resté.

Qu'est-ce que l'on pouvait faire dans ces cas là ? Il ne savait pas non plus s'il fallait dire quelque chose, ou si le silence faisait partie de ce qu'on offrait. Il regardait le bout de ses chaussures et il attendait, comme on attend un train dont on n'a pas l'horaire. Eliott s'assit sur le blanc tout blanc, balançant ses jambes, le regard droit devant lui comme dans ses pensée. Andrew l'observa, en silence et s'asseya juste à côté de lui, jetant son regard au loin, dans la même direction. deux moineaux se disputant une miette de quelque choses, insconscient d'être épiés par deux parfaits inconnus.

Ce fut Eliott qui parla.

— Merci.

Andrew leva la tête.

— De quoi ?
— De rien. De tout. On m'a parlé de ce jardin et j'avais tellement envie de le voir de mes propres yeux...elle...elle voulait pas...Pourtant ça a l'air beau.

Il se tait un instant tendant l'oreille. Des cris et des rires d'enfants resonnaient de l'autre côté de l'enceinte. on entendait le bruissement des feuilles dans les arbres et le soleil filtrant à travers les branches. Puis des chants, mêlés à une tondeuse, l'herbe fraichement coupé chatouillant les narines. Eliott inspira, comme savourant ce moment. Il balançait toujours ses jambes sous le banc. Elles ne touchaient pas le sol et elles ne le toucheraient plus.

Puis il ajouta, plus bas, comme s'il s'agissait d'une chose d'un autre ordre :

— ...Et de m'avoir cru.

Andrew ne répondit pas. Il y avait une réponse quelque part, il la chercha deux ou trois secondes, et elle ne vint pas.

Le silence dura, et ce ne fut pas un silence gênant. C'était celui de quelqu'un qui décide. [developper]

— Toi, tu n'as jamais eu cette impression ? le questionna t'il.
Andrew su immédiatement où la question l'amenait.
— De rêver en plein jour ?

Elliot plongea son regard dans celui du quadragénère. Andrew fit non de la tête. C'était vrai et ce n'était pas vrai, et il n'avait pas de mot pour le milieu.

— Le premier, c'était le jour de ma cérémonie.

Il ne baissa pas la voix. Il en parlait comme d'une chose survenue à quelqu'un qu'il connaissait bien.

— le monsieur à côté de moi. Je l'avais pas vu au début. Et je crois que lui non plus. j'ai vu tous les autres. et quand je me suis tournée j'ai vu ses yeux. Tout pareil que le miens. Je les ai regardé, et c'est comme si je n'étais plus là. J'étais dehors. Pas dans la ruche. Dehors, dans un endroit que je ne connais pas. Il faisait froid comme il fait froid ici le matin, sauf que c'était pas ici.

Andrew observa son expression en écoutant silencieusement. C'était son histoire. [a developper ?] Elliot poursuivi, le regard perdu dans le vague comme s'il revoyait la scène a mesure qu'il la décrivait.

— Quelqu'un m'aidait à mettre un sac sur le dos. Un gros ! On aurait pu y ranger la maison entiere rit-il. Il tirait sur les bretelles pour que ça tienne bien, et il a tapé deux fois dessus quand ça a été bon.

Il fit le geste. Deux petites tapes dans le vide, à hauteur de son épaule.

— C'était lui. Le monsieur d'à côté. sur mon sac, j'avais une couverture, enroulée et accrochée au dessus. un imperméable pendouillait sur un mousqueton d'un coté du sac et j'avais une gourde dans une poche de l'autre côté. et dans mon sac, j'avais même une super corde noire et orange très solide et très longue ! Je dis ça parce que je me revois la tendre entre deux arbres ! 

Puis, sans transition, du même ton :

— Et une dame m'a embrassé sur le front.

Il s'arrêta là-dessus un instant, comme on s'arrête sur une marche.

— ce monsieur... j'avais l'impression de le connaitre depuis toujours alors que je l'avais jamais vu..Et puis c'est parti dans tous les sens; lui, il me tendait la main. Il la tendait fort, tu vois, avec tout le bras. Moi je n'arrivais pas à l'attraper. Nos mains glissaient trop.

— glissaient trop ?
Andrew considéra sa remarque. Eliott naviguait entre ses souvenirs comme un trop plein de tout. l'information qui sortait de sa tête n'était pas triée. [approfondr] sans trop de transition, il rattachait les éléments comme un étudiant déverserait tout sur une copie pour etre sur de ne rien oublier trop vite.

— J'ai senti le sol s'en aller sous mes pieds alors que je ne bougeais même pas. Je bougeais meme pas, je te jure. Assis. Et le sol est parti ! J'avais les yeux ouverts et j'avais de l'eau dans la bouche.

Andrew ne bougea pas. Quelque part derrière eux, une porte battit et ne se referma pas tout de suite.

— Je n'ai jamais vu de rivière. Je ne savais même pas ce que c'était, un courant — on me l'a appris à l'école, cette année. Et pourtant j'ai rêvé que je tombais dedans.

Il dit ça avec un petit haussement d'épaules, un peu vexé, comme quelqu'un qui vient d'apporter lui-même la preuve qu'il a tort.


— Et j'avais peur. Pas juste pour moi. J'avais peur pour lui aussi mais je sais pas pourquoi...

Il se tut, puis il reprit d'une voix différente, plus légère, comme s'il passait à autre chose de plus agréable — et c'était exactement ce qu'il faisait.

— Il n'y a pas que ça, hein. Il y a une odeur, aussi. Je ne sais pas de quoi. Ça sent le pain et le froid en même temps... Et il y a un regard. Quelqu'un qui me regarde. C'est tout, il ne fait rien d'autre, il me regarde. Mais quand je me souviens de ça, je suis bien.

La femme qui attendait plus loin consulta quelque chose et ne s'approcha pas.

— Et maintenant, je fais quoi avec ça ?

Il avait posé ça comme on pose une question de mathématiques : sérieusement, en attendant une méthode.

— Tu crois qu'ils vont se moquer de moi ici aussi ?

Andrew ouvrit la bouche. Il n'avait rien.

— Est-ce que tu viendras me voir ?

Andrew mit du temps. Il regarda l'allée, l'enceinte, les portes de chaque côté, la lumière qui venait du fond et qui n'avait pas de source visible.

— J'ai connu quelqu'un qui se posait beaucoup de questions, lui aussi.

Il dit ça comme on constate. Ça lui était venu tout seul, et il ne s'étonna pas de l'avoir dit. 

— Il s'appelait comment ?

Au bout de l'allée, la femme fit un pas et s'arrêta. Comme saisissant le signal [approfondir]

— Je viendrai te voir.

Eliott hocha la tête. *Il avait eu ce qu'il voulait, et il ne redemanda rien.* [approfondir]

Il resta un moment les mains sur les genoux. Puis il revint à son monsieur, parce que c'était là qu'il était depuis le début. Il descendit en un petit bond et fit face à Andrew.

— Il m'aimait beaucoup, tu sais. il sourit rêveur. Un sentiment fort. Très fort. J'avais l'impression que c'était moi et que moi c'était lui.

Il marqua une tout petite pause, la derniere et en un sourire Elliot marqua chacun de ses mots : 

— Comme si je l'aimais encore plus fort que lui.

---

### [131] 2026-08-16 à 17:06

on pourrait rajouter les moineaux à la fin, comme si au lieu de se disputait ilse trounaient cette fois autout, semblant jouer ensemble, les petits becs se frolants dans des petite gazouills

---

### [132] 2026-08-16 à 17:09

* "La corde. Noire et orange, très solide, très longue, et il se revoit la tendre entre deux arbres. Il la raconte comme un trésor. C'est l'objet le plus sombre de la page et c'est le seul qui le fasse sourire." oh non, du tout, c'est un souvenir de randonnée, il a pu tendre une corde avec son père pour monter une tente ! mais à cet age, la moindre responsabilité est un tresor. son père lui a sens doute dit "c'est toi qui portera la corde" il est super fiere ! rien a voir de trop sombre ! 

* pour enfants tu as raisons

---

### [133] 2026-08-16 à 17:10

les moineux peuvent etre intercalés avant la derniere phrase. il se releve pas forcement pour regarder Andrew, il s'est levé pour chercher les moineaux des yeux qui ont bougé de place

---

### [134] 2026-08-16 à 17:12

"Il marqua une toute petite pause, la dernière, et détacha chacun de ses mots, un sourire emplit d'une nostalgie etrange"

---

### [135] 2026-08-16 à 17:23

* "le banc tout blanc," pas tres beau en fait ^^' 
* Elle avait dit ce qu'elle avait à dire et elle l'avait dit vite, debout, sans poser son sac, de la façon dont on récite une adresse à quelqu'un qui va la noter. elle parait super froide :'((((((
* "Celui des premières minutes, quand la bouche n'a pas encore retrouvé ses dents. Celui des gens qui n'ont rien à dire et qui attendent qu'on parte." trop bizarre ^^'
* "Ça sent le pain et le froid en même temps. " ça sentait... la fraise et la chantilly avec un petit coté fumé... Il realise en le disant : comme une celebration d'anniverssaire !! 
* "Elle avait laissé passer tout ce qu'il fallait laisser passer, et elle savait aussi reconnaître le moment où une conversation a fini de servir à celui qui la mène. " la phrase n'est pas belle...
* "; les deux autres pouvaient attendre, et le nom d'un inconnu n'avait déjà plus d'importance. Il ne redemanda rien." on l'enleve, pas besoin d'expliquer que les questions n'auront pas de reponse.

tu peux juste me refaire ses passage là et je les valides avec le reste ?

---

### [136] 2026-08-16 à 17:29

garde "Il marqua une toute petite pause, la dernière, et détacha chacun de ses mots, un sourire emplit d'une nostalgie nouvelle"

* "l'encadrement de la porte" ils se trouvent dans une allée longeant une enceinte.
* "Andrew le connaissait pour l'avoir attendu des centaines de fois, assis au bord d'une couverture : celui de quelqu'un qui a une chose à dire, qui a déjà décidé de la dire, et qui cherche encore par quel bout la prendre. ça reste pas tres beau.. c'est un silence pas de gene ni plus ni moins
* "Avec un petit côté fumé, en dessous." je parlais des bougies fraichement soufflées ahah elle peut pas etre en dessous du gateau ^^'
* "Elle ne pressait personne." dans une attente respectueuse. elle est observatrice de deux personne qui se font leur adieu. est-ce que d'ailleurs on en ferai pas l'enfant qui à la fin, lance sa derniere réplique en tendant la main à la femme ? elle se serait bien sur rapprochée en une invitation silencieuse pour qu'il la suive

---

### [137] 2026-08-16 à 17:32

tu me reecris tout ici ? je te valide et ensuite tu pourras faire l'update dans chapitre

---

### [138] 2026-08-16 à 17:35

tu en penses quoi toi ?

---

### [139] 2026-08-16 à 17:39

"C'était l'histoire du petit" tu couperas donc quoi exactement ?
"Le paragraphe des sons est la seule page « écrite" " je comprends pas ta remarque. oh le sac j'y toucherais pas trop, t'enleve la couverture si tu veux, un aper d'un coté, une gourde de l'autre et la corde

---

### [140] 2026-08-16 à 17:42

"Andrew écoutait sans bouger. Il ne relevait rien, il ne demandait pas de précision, il ne notait rien." ok, mais j'aurais gardé quand meme "il ne cherchait pas à remettre les morceaux dans un ordre qui aurait tenu debout — il avait passé des mois à faire exactement ça, et ça n'avait servi à rien." vendu pour les sons. tu peux me reecrire tout une nouvelle fois stp ? et tu peux le modifier egalement dans chapitre. ce n'est pas figé, mais c'est dejà pas mal en l'état

---

### [141] 2026-08-16 à 18:02

« Eliott ne répéta pas. Il naviguait dans ses souvenirs comme dans un trop-plein, et ce qui sortait de sa tête n’en sortait pas trié. Il n’y avait ni avant ni après, ni grand ni petit : la corde et la peur pesaient le même poids, le sac et l’eau venaient dans le même souffle. Il rattachait les morceaux les uns aux autres comme un élève qui déverse tout sur sa copie, sans plan, de peur d’en oublier un en route. » attends, ça c’était avant que je te reprenne.. la corde n’est pas pas un mauvais souvenir, la on comprend l’inverse et parler de l’eau juste avec les mains trempés ça sert pas à grand chose, on a « l’eau dans la bouche » qui suffit à évoquer la noyade

---

### [142] 2026-08-16 à 18:04

Nickel, je valide

---

### [143] 2026-08-16 à 20:12

"Comment se déroule une arrivée au jardin — la scène n'existe pas encore. " imagine une rentrée scolaire pour petite section / grande section : c'est la meme chose. le jardin  est entourée d'une grand enceinte, avec des murs hauts. de l'exterieur, en ville, on ne voit qu'un mur au crepit creme. une grande allée serpente tout le long de l'enceinte, avec des bancs, des poubelles, des arbres comme dans un parc. on a des grandes grilles disséminées un peut partout car l'enseinte est tres grande. immagine une taille de celle du parc guell en espagne ! il ne peut pas y avoir qu'une seule grille. donc l'exterieur est tres sobre. l'interieur est comme une seconde ville. il y a des allées, des vraies jardins pour le coup, des endroits betonnés pour les autres des airs de jeu. les murs ne sont pas blancs de l'autre coté, il y a des fresques qui arpentent tout le long. des dessins d'"enfants" il y a des baraques à velos/trycycles, tout pour que les enfants s'éclatent dehors. bcp d'arbre, l'air y est frais, tres ombragé. il y a plusieurs lotissement pour accueillir enfants et berceurs.  un centre pediatrique au milieu avec parking. il y a des salles interieur de jeu "d'éveil' qu'on ne peut pas appelé eveil dans ce monde, un gymnass avec des tapis et obstacle en mousse comme pour des cours de baby gym.

pour en revenir au jour de la rentrée pour Eliott, imagine donc des petits groupes disséminés un peu partout sur l'allée non loin d'une grille. On peut y voir des tout petits, arrivant de 0 à 8 mais il c'est tout de meme une majorité d'enfant de 8 ans qui vont leur rentrée. donc des petits groupes accompagné de berceurs et berceuses. c'est pas systématiquement un enfant = une berceuse, parfois un berceur peut en avoir plusieurs. ils attendent tous devant que le "directeur du jardin ouvre la grille. du moins un responsable de l'accueil. car il y a des responsable dortoir, responsable pediatrique, des responsables de sections, etc. Pendant ce temps, comme pour une ecole dont c'est ton premier jour, les enfants se regardent, sont curieux les uns des autres, certains on déja trouvé un copain tandis que leur berceurs respectifs echangent des banalités, certain reste dans leur jupe. puis la grille s'ouvre, il y a un petit mouvement, le responsable de zone arrive suivi d'un nombre de berceurs définis en fonction du nombre d'entrée indiqué par l'administration. quand eliot arrive c'est un peu particulier. Andrew est déjà là et observe la scène de loin. June l'apercoit et l'invite à le rejoindre. tandis que les autres enfants commence à rentrer, June demande à la berceuse qui lui succède la possibilité de leur donner quelque instant avant de refermer les grilles. cette derniere accepte. June fais donc ses adieux, professionnel, avec une emotion contenue que l'on ressent quand meme (le pincement au coeur d'une assistante maternelle de voir partir le petit qu'elle gardait), salut Andrew et s'en va

---

### [144] 2026-08-16 à 20:17

on reste dehors car on n'a plus de raison d'y entrer en tnt que spectzteur. on en verra la definition de sa cartographie quand on ira pour la seconde fausse piste. 

peintes à hauteur de main, des proportions qui ne tiennent pas, des soleils qui ont un visage

nickel.

Tu veux me proposer une debut décrit pour que le chapitre commence à l'arrivé d'Andrew aux abords de la grille ?

---

### [145] 2026-08-16 à 20:30

"L'allée longeait l'enceinte sur toute sa longueur, et l'enceinte n'en finissait pas. Un mur haut, au crépi crème, sans une fenêtre, qui suivait la rue en s'incurvant doucement et qu'on ne pouvait pas prendre pour autre chose qu'un mur. De ce côté-ci, c'était un parc : des bancs à intervalles réguliers, des poubelles, des arbres assez vieux pour faire de l'ombre sur toute la largeur. Des gens passaient. Un vélo, quelqu'un avec un chien, deux femmes qui parlaient fort. Personne ne regardait le mur. On ne regarde pas un mur devant lequel on passe tous les jours." cette description ça sera pas ici, mais pour la scène 14b.

"ce qui ne valait guère mieux" moche la tournure

la phrase d'intro pas dingue non plus si tu as d'autres idées "Il était arrivé en avance, parce qu'un homme qui n'a rien à y faire arrive toujours en avance."

"Chaque groupes avait ses berceurs. parfois un berceurs pour un arrivant, parfois trois arrivant pour un berceur ou plus." c'est mieux nn ?

"Les adultes parlaient de la circulation," : les berceurs, entre confrères et consœurs, parlaient de la circulation

"Il les avait comptés sans s'en apercevoir. Quarante-deux." oui mais dans ce cas on ne donne pas un nombre au début.

il manque la transition quand il s'approche et que june demande quelques instants et bien sur l'entrée des autres

---

### [146] 2026-08-16 à 20:40

"Deux s'étaient déjà trouvés et se disaient des choses que personne d'autre n'entendait." peut etre plutot qu'ils commençaient a se courrir à apres comme un jeu

"Andrew était venu à pied, comme les trois premières fois." pas interessant, ça n'apporte rien au recit

"six ou sept berceurs" bizarre de pas dire un chiffre fixe non ? 
"L'administration avait compté avant eux." bif bof -> en moyenne 7 ou 8 petits pour un berceurs, c'était la norme retenues par l'administration dans la theorie. dans la pratique les age les plus petits sont presque individualisé tandis que les 7 et 8 formeront des groupe plus grand.

---

### [147] 2026-08-16 à 20:47

t ceux de sept et huit ans faisaient les groupes les plus gros : formaient des groupes plus gros.

"comme il avait compté les têtes, et ça ne lui servit à rien du tout.  : phrase pas belle

"elle se pencha vers la femme qui attendait un peu à l'écart — celle qui prenait la suite — et lui demanda quelque chose à voix basse." : pourquoi se pencher et aussi pourquoi pas dire que c'est une berceuse voir la responsable ? ça expliquerait qu'elle accepte d'attendre Eliott alors que tout le monde est entrain de rentrer. 

il manque la transition, June qui fait ses adieu a Eliot et Andrew qui les rejoint. on pourrait tres bien entendre un dialogue pour pas qu'elle soit muette jusqu'à la sortie de la scène !

---

### [148] 2026-08-16 à 20:53

« C'est normal. » — « Non. » Un mot, et il porte le livre entier : personne ne lui a jamais demandé de venir, et il est venu pendant six ans. Elle est la seule à l'avoir remarqué, et elle le lui dit en partant. pas convaincu. ça la rendu SU-PER froide ! 


j'accepte jusqu'à c'est normal ahah, et d'ailleurs ente lisant, c'est june qui a demandé à andrew de venir ? pourquoi? moi je pensais plus à Andrew, observateur de loin quelque part comme pour s'arrurer qu'il rentre bien. elle l'apercoit, elle l'invite a approcher

---

### [149] 2026-08-16 à 20:57

Elle eut un petit sourire qui n'était pas vraiment pour lui, puis elle passa la lanière de son sac sur son épaule et s'en alla.

Elle avait dit ce qu'elle avait à dire et elle l'avait dit vite — parce que prendre le temps de plus, lui donner une chance de répondre aurait voulu dire rester, et qu'elle n'aurait plus su repartir ensuite. Andrew observa sa silhouette se fondre entre les arbres sans se retourner."

---

### [150] 2026-08-16 à 21:09

tu me refais le chapitre avec le rajout complet du coup ?

---

### [151] 2026-08-16 à 21:19

" parfois trois arrivants pour un berceur, parfois plus." -> "voir plus"
"sans un mot" nan, en riant, faut de la vie ^^
"tous individualisés" : il était presque tous pris au cas par cas
"des adultes" attention, mot interdit on appelle par la profession no ?
"la seule chose qui n'était pas pratique." = y a pas une autre formulation ? "pas pratique" c'est bizarrz
"parce qu'en prendre davantage" insinue que tu as utiliser le mot temps juste avant, ce qui n'est pas le cas, la formulation c'est pas jolie

---

### [152] 2026-08-16 à 21:24

attend elle a quelle age déjà ici ? elle a 16 ans non ? ça fait 6 ans qu'andrew ne la pas revu. ça vaudrait peut etre le coup de le faire remarquer nn ?

---

### [153] 2026-08-16 à 21:26

"Elle lui arrivait à l'épaule maintenant," ça va pas, de un, il vient de l'apercevoir, il peut pas pretendre de sa taille vu qu'il n'est pas encore à coté d'elle et il y a une repetition du mot epaule

---

### [154] 2026-08-16 à 21:29

hmm.. je sais pas, c'est pas convaincant, l'info passe un poil trop à l'as je trouve 😕

---

### [155] 2026-08-16 à 21:34

"plus bas " c'est pas très bon. pourquoi pas dire plus jeune ? rajeunir. pour le coup ça peut etre un mot classique pour eux. nous on aquiert de l'experience en vieillissant, eux en rajeunissant. je trouve pas sa tabou comme mot. plus vieux, je suis d'accord, on evite. plus jeune, j'y vois pas de problème. on evite quand meme de dire enfant, mais jeune arrivant pas exemple ça me choque pas

---

### [156] 2026-08-16 à 21:36

oui, c'est comme ça qu'il faut l'employé? plus simple, on retient juste que jeune est descriptif du physique

---

### [157] 2026-08-16 à 21:37

refais moi le tout donc ? du début jusqu'à ce qu'ils soient assis sur le banc ?

---

### [158] 2026-08-16 à 21:41

non, pour moi, c'est tout l'épilogue là. tu commence à "Il n'y avait aucun endroit où se mettre." et tu clotures à "Comme si je l'aimais encore plus fort que lui." et tu peux juste nommé ce chapitre "Epilogue" c'est bien

---

### [159] 2026-08-16 à 21:57

alors le prologue n'est pas du tout figé. on l'écrira demain

---

### [160] 2026-08-16 à 22:01

S"es yeux, tout pareils que les miens" une petite nuance qu'on arrivera aisément a expliquer par une petite phrase simple dans la conception de la cérémonie, le veilleur tend un miroir pour que l'arrivant puisse faire connaissance avec sa propre apparence

"Le bouton copier le texte te le sort en brut, sans balises, si ta femme veut le reprendre ailleurs. " au cas ou, c'est Elodie là, et depuis le début. Kévin a pris la mains qu'à la creation du projet. aujourd'hui par exemple tu n'as discuté qu'avec moi. il t'as proposé de faire le prologue mais moi je l'ai meme pas lu. on le bonssera ensemble demain

---

### [161] 2026-08-16 à 22:05

nickel, tu gères 😉 a demain donc ! je te laisse faire un été des lieux s'il ya besoin de ton coté

---

### [162] 2026-08-16 à 22:11

juste, tu peux me sortir un pdf de l'épilogue stp ?

---

### [163] 2026-08-16 à 22:39

petites notes de dernieres minutes : 

* "parfois un berceur pour un arrivant, parfois trois arrivants pour un berceur, voire plus." -> "parfois un berceur pour un arrivant, parfois trois arrivants pour un berceur et parfois plus." "parfois" devient une répétition maitrisée.
* "d'une	berceuse qui ne bougeait pas." -> d'un	berceur qui ne bougeait pas.
* "un	banc	de	pierre,	au	bord	de	l'allée" -> un banc de pierre non loin d'eux
* "Deux moineaux	se	disputaient	une	miette	au	milieu	de	l'allée" -> une miette d'on ne sait quoi, au milieu de l'allée
* "il	avait	passé	des	mois	" -> "il vait passé des semaines"
* "de	tout	l'après-midi," -> est-ce necessaire ?
* "que	c'était	moi	et	que	moi	c'était
lui" -> "que	lui c'était	moi	et	que	moi	c'était
lui"
* on mettrait pas une phrase de fin type "Andrew le regarda partir, songeur aux côté de la nouvelle berceuse. La grille se referma blablalba. peut etre trouver un truc un peu plu smetaphorique je sais pas

---

### [164] 2026-08-16 à 22:43

j'aime bcp tu peux garder et updater le chapitre et le pdf

---

### [165] 2026-08-16 à 22:49

après c'est joliment imagé "le banc n'était plus froid" mais tu ne penses pas que le lecteur peut l'interpréter autrement ?

---

### [166] 2026-08-16 à 22:53

bah moi j'ai compris la chaleur d'eliott mdr et la nouvelle formulation est moche x)

---

### [167] 2026-08-16 à 22:55

tu as d'autres idées ?

---

### [168] 2026-08-16 à 22:56

j'aimais vraiment le banc n'était plus froid, dommage

---

### [169] 2026-08-16 à 22:57

oui on garde le banc n'était plus froid

---

### [170] 2026-08-16 à 23:01

pour moi tu veux mon avis, je le lis comme justement un rappelle au banc froid du matin. le petit garçon a vidé son sac, la chaleur.. c'est une métaphore positif pour aussi dire que tous ses reliquats n'était pas forcément mauvais. la chaleur rechauffe, enveloppant. ne pas dire la phrase "la place etait encore chaude" mais dire l'inverse c'est un peu dire, oui c'est tragique, mais il y a du bon aussi

---

### [171] 2026-08-16 à 23:02

exactement, allez, tchuss

---

### [172] 2026-08-17 à 00:10

On se retapera une petite réflexion sur l’épilogue, en le relisant il fait quand même triste comme si ils partaient vers la mort.. ce qui est vrai mais il faudrait pas que ça se ressente comme elle. C’est un accompagnement de fin de vie. On peut supposer que les discussions sont animés entre les berceurs, très légères. C’est le métier d’amener les enfants ici. Oui il y a le pincement au cœur mais tous ne le vivent pas pareil. June peut émettre la réserve qu’elle a actuellement mais le fait qu’elle puisse lui rendre visite n’est pas fermé nn plus. On peut supposer aussi que le reponsable et les berceurs sont accueillants également, des sourires, des regards bienveillants. On peut supposer qu’Eliitt, malgré ses inquiétudes est heureux de rejoindre le jardin, il est curieux de voir ce qui s’y passe.

---

### [173] 2026-08-17 à 00:12

On va pas tout réécrire car ça tient à des détails pour changer une émotions, mais ça serait bien que ça prenne cette tournure. Apres tout on peut venir rendre visite. Ce qui peut faire comprendre que June émet une réserve c’est qu’elle sait elle aussi qu elle le rejoindra dans pas si longtemps que ça. C’est donc compliqué de lui répondre et heureusement Elliot ne lui demande pas. Ça peut être Andrew qui pour le rassure lui dit, ne t’inquiète pas, elle viendra te rendre visite, tu la connais ;) (quand elle part et qu il la regarde partir)

---

### [174] 2026-08-17 à 10:43

ah noté que tout comme les vieux qu'on peut croiser dans la rue accompagnés de soignants, on peut egalement croiser des petits et leur berceurs. oui le jardin est comme une mini ville dans une grande ville, mais il n'y a pas tout le necessaire non plus. des gens entrent pour l'entretiens, d'autres livrent les repas elaborés à l'exterieur.. tu imagines vraiment un systeme ecole petite enfance

---

### [175] 2026-08-17 à 10:45

rien ne dit qu'Eliott ne pourra pas rendre visite à June. du moins ça reste plus simple que de rendre visite à Andrew, etant donné que lui s'occupe du debut de vie alors que lui se trouve en fin. c'est rare de voir des vieux dans une maternité :p

---

### [176] 2026-08-17 à 10:46

on est un nouveau jour, on reprend ;)

---

### [177] 2026-08-17 à 10:48

Nan, on se lance dans la retake de l’épilogue. Quelle passage as-tu relevé et que me proposes tu ?

---

### [178] 2026-08-17 à 10:50

Ah et la berceuse de fin qui semble hyper effacée, pareille, elle peut dégager une aura accueillante, Eliott s’apprête à la suivre de bon cœur

---

### [179] 2026-08-17 à 10:55

Laisse moi d’abord répondre à tout et ensuite tu relances une passe. 1) « parlaient fort et se coupaient la parole.«   à la première lecture ça fait abrupte. Je pencherai plutôt sur conversation animée. Je suis pas d’accord sur ce que tu as enlevé, parler de tout et de rien, de la pluie et du beau temps, c’est normal aussi. Il était question de la construction du Nouveau Centre commercial, d’un collègue ayant changé de section, de petits potins de quartier

---

### [180] 2026-08-17 à 11:08

2) Eliott devant la grille : rien a dire
3) Les jambes qui ne toucheront plus le sol. en fait, je trouvais ça poétique mais peut etre incomplé. moi je l'ai compris dans le sens qu'elle ne toucheront plus le sol car il va devenir de plus en plus petit. peut etre garder une métaphore plus leger mais qui veut dire ça aussi.
4) "et continua." je rajouterai "d'un pas léger, rattrapant son groupe en sautillant" ou quelque chose du genre. il est pressé d'y aller
5) Le personnel d'accord avec ta propal, on peut aussi avoir une ligne de dialogue. chaleurseuse affectueuse pour accueillir un enfant
6) je suis d'accord mais pas entierement "quelque chose bougeait qu'il n'arrivait pas à voir en entier." bof la formulation. il entendait des petits pas précipités, des mumures enjoués comme s'il n'arrivait pas à se concentrait sur ce qu'elle lui disait.
7) "la femme qui attendait plus loin consulta quelque chose » : Un berceur remonta l'allée dans l'autre sens, avec deux petits qui revenaient de quelque part." -> la femme qui attendait plus loin consulta quelque chose tandis qu'un berceur remontait l'allée dans l'autre sens, avec deux petits revenant de quelque part.  "L'un des deux portait un sac trop grand pour lui." pas necessaire je trouve


petit point, avant queliot et andrew soient en tete à tete après le depart de june : peu à peu l'allée se vida, berceurs et berceuse repartant à leur occupation. puis ça enchaine sur s'assoit sur le banc, blablabla


"« t'inquiète pas, elle viendra te voir, tu la connais »" : je suis d'accord avec toi


"La berceuse s'accroupit devant Eliott. Elle lui dit son prénom, lui dit qu'elle serait là quand il aurait fini. Elle avait la voix des gens qui font ça depuis longtemps. Puis elle recula de quelques pas et les laissa." trop maladroit je pense.." ou peut etre alors faire en sorte qu'elle soit déjà proche de lui avec June. comme si June echangeait déjà avec elle avant de remarqué Andrew à 30 mètre. je suis pas non plus fan des paroles non transcrites "elle lui dit son prenom, elle dit qu'elle serait là'. on est du pdv d'andew, il peut juste constater qu'elle s'est agenouillé à son niveau en lui carressant affectueusement les cehveux et se releve quand juste lui demande un instant. 

pour la fin : "La femme s'était rapprochée. Elle ne dit rien : elle tendit la main, et elle souriait comme on sourit à quelqu'un qu'on va emmener voir quelque chose. Eliott lui donna la main sans hésiter." validé
"Elle attendait comme on attend au fond d'une pièce où deux personnes ont quelque chose à finir." validé" c'est bon, à toi !

---

### [181] 2026-08-17 à 11:14

ok, donc ça donne quoi ?

---

### [182] 2026-08-17 à 11:30

"C'était la seule chose qui se passait vraiment." a faire sauter, partout on l'on regarde, il y a de l'animation. les enfants impatients, les conversations des adultes allant bon train. 

"Une berceuse s'accroupit devant un tout-petit" ça sonne mal avec le mot "petit" vu juste avant. "Une berceuse s'accroupit,  toute souriante, devant l'un d'entre eux"

"La plupart entrèrent sans regarder derrière eux. Un petit se retourna pour vérifier que sa berceuse le regardait, vit qu'elle le regardait, et repartit en sautillant pour rattraper son groupe." repétition trop proche de berceuse avec leparzgraphe d'avant : "La plupart entrèrent sans regarder derrière eux. Un petit se retourna pour vérifier qu'on le regardait, constata que c'était le cas, et repartit en sautillant pour rattraper son groupe."

"tourna vers celle qui prenait la suite et lui parla à voix basse." : "vers sa consœur et lui parla à voix basse"

"derrière la grille, il y avait des petits pas précipités et des murmures enjoués, et c'était plus fort que lui." : "derrière la grille, il y avait des petits pas précipités et des murmures enjoués; c'était plus fort que lui."


petit ajustement pour ce qui suit : 

"Elle ne se retourna pas.
Eliott aussi l'observa une bonne minute silencieux.

— T'inquiète pas. Elle viendra te voir, tu la connais.

Il hocha la tête sans quitter les arbres des yeux.

Peu à peu, l'allée se vida. Les berceurs repartaient à leurs occupations, seuls ou à deux, et le bruit de leurs conversations s'éloigna vers le bout de la rue.

Il resta où il était.

Qu'est-ce qu'on pouvait faire, dans ces cas-là ? Andrew ne savait pas s'il fallait dire quelque chose, ou si le silence faisait partie de ce qu'on offrait. Il regardait le bout de ses chaussures et il attendait, comme on attend un train dont on n'a pas l'horaire."


déjà on fixe ça et je regarde" la suite après

---

### [183] 2026-08-17 à 11:33

ok, ça donne quoi ?

---

### [184] 2026-08-17 à 11:36

on va pour la suite essayer de rendre le passage d'eliott plus doux. on touche pas le passage de l'eau mais on allege encore le reste. quand il se souvient de l'odeur de gateaux, c'est pas juste des yeux rond, il est presque excité et amusé d'avoir trouver la reponse, ses yeux petillent de malice. quand il se rappelle du baiser, c'est un air béa, reveur, un sentiment de sécurité forte. il se souvient sans le savoir du baiser de sa mere juste avant son depar tpour la rando avec son pere

---

### [185] 2026-08-17 à 11:40

"Personne ne se dit bonjour. ", "Il n'y eut rien sur son visage, ni surprise ni soulagement" je sais pas ça me chiffone toujours.. ils sont pas vraiment neutres.. il a quand meme retrouvé son petit.. elle l'apprécie forcement et Andrew de son coté est fin observateur, pas forcement extravertie à fond, mais il n'est pas non plus antipathique. la situation est inhabituelle pour lui. comme ça pourrait etre le cas pour un flic qui vient rendre visite à une personne qu'il a sauvé. il fait ça autant pour lui que pour cette personne tout en restant humble

---

### [186] 2026-08-17 à 11:42

d'accord pour le "— Et avant de partir," pas d'accord pour le reste, la description n'est pas hamonieuse, "il peut commencer à s'agiter, balançant son buste de droite à gauche, sa tete dodelinant ant décalé, les yeux fermé comme s'il savourait le moment, un large sourrire sur le visage. pour le passage de gateau, je valide

---

### [187] 2026-08-17 à 11:43

"quelqu'un qu'on est content de voir mais dont on n'a pas le temps de s'occuper" trop long pour pas grand chose

---

### [188] 2026-08-17 à 11:45

tres bien. pour le baiser tu proposes quoi ?

---

### [189] 2026-08-17 à 11:46

ok nickel et.. attend je relis la toute fin.

---

### [190] 2026-08-17 à 11:47

"La femme qui attendait plus loin consulta quelque chose, tandis qu'un berceur remontait l'allée dans l'autre sens avec deux petits revenant de quelque part.

— Et maintenant, je fais quoi avec ça ?"

on intercale : "les moineaux s'envolèrent subitement ; Andrew les perdit de vue"

---

### [191] 2026-08-17 à 11:49

"Les moineaux ne devait pas etre loin ; il fit deux pas dans l'allée pour les retrouver."

---

### [192] 2026-08-17 à 11:52

"Il les regarda un moment. Puis il revint à son monsieur, parce que c'était là qu'il était depuis le début.

— Il m'aimait beaucoup, tu sais."

---> "Il les regarda un moment. Sa respiration lente, en suspens.

— Il m'aimait beaucoup, tu sais."

Et parce que c'était là qu'il était depuis le début, Andrew continua d'observer silencieusement "ce petit homme lui parler de son monsieur. " (peut etre pas tres beau mais l'idée est là)
La femme s'était rapprochée. Elle ne dit rien : elle tendit la main, et elle souriait comme on sourit à quelqu'un qu'on va emmener voir quelque chose. Eliott lui donna la main sans hésiter.

---

### [193] 2026-08-17 à 11:54

je valide : tu peux me montrer ce que ça donne à partir du moment ou june est partie ?

---

### [194] 2026-08-17 à 11:59

"— De rien. De tout. On m'a parlé de ce jardin et j'avais tellement envie de le voir de mes propres yeux… elle… elle voulait pas. Pourtant ça a l'air beau."

— De rien. De tout. On m'a parlé de ce jardin et j'avais tellement envie de le voir de mes propres yeux… mais elle... elle voulait pas, elle voulait plus et je ne sais pas pourquoi. Pourtant ça a l'air beau."
Il marqua une pause
— il va lui arriver quoi ?
Andew haussa les epaules pensifs. Eliot pencha légèrement sa tete, l'oreille tendue. De l'autre côté de l'enceinte,"

---

### [195] 2026-08-17 à 12:01

— C'est moi qui la portais ! C'est lui qui l'avait dit : c'est toi qui portes la corde. Je me revois la tendre entre deux arbres, pour la tente. intercaler une phrase du style "malgre lui il se mit à mimer une attitue : il pris une vois exagérément plus grave "c'est toi qui porteras la corde" amusé

---

### [196] 2026-08-17 à 12:03

bah je repond à ton interrogation, c'est pas "— Il va lui arriver quoi ?", c'est "il lui est arrivé quoi tu crois" ça ecarte instannément June et andrew qui n'est pas flic n'a pas de rponse à lui apporter. il peut peut etre lui repondre "je n'en sais trop rien... " pas obligé

---

### [197] 2026-08-17 à 12:04

j'aime bien. tu me refais ces deux passages ? la corde et elle ?

---

### [198] 2026-08-17 à 12:06

ok je valide

---

### [199] 2026-08-17 à 12:08

ok, je veux bien l'époloque en entier et mis à jour dans chapitre stp (et aussi le pdf)

---

### [200] 2026-08-17 à 12:53

«  June revint vers » pas bon, elle n’a pas bougé de place. Au contraire Andrew pourrait s’avancer .

Bizarrerie « il reste où il était. »

Andrew mit du temps : le veilleur mis du temps. On évite la répétition Andrew


Au bout de l’allée la femme attend, ça va pas, elle est près de la grille normalement

---

### [201] 2026-08-17 à 13:00

On est bon

---

### [202] 2026-08-17 à 13:07

Lance la synchro

---

### [203] 2026-08-17 à 13:29

Concernant le prologue, je vais te faire un petit peu les idées que j’ai en vrac dans la tête. Il ne faut déjà pas voir la ruche comme une ruche d’abeille. Il va falloir trouver comment définir les capsules. À part le fait qu’elle s’éclaircissent, nous n’avons pas d’autres informations pour l’instant. J’imaginais quelque chose un lieu très organique, un peu la comme la sérénité d’une forêt, ça reste un bâtiment à part entière, un endroit fermé type comme un grand entrepôt, avec de longs couloir, plusieurs pièces de collecte, c’est-à-dire des pièces avec des capsules plus ou moins à maturation. Pour le côté couleur, j’aurais aimé quelque chose de significatif, mais mon avis n’est pas tranché, j’aime beaucoup le rouge pourpre, mélangé au doré, mais j’aime aussi beaucoup le bleu ciel mélangé à de l’oranger. L’air est frais, un peu comme dans un monastère, il y a le passage du vent. C’est un bâtiment entrepôt avec beaucoup d’ouverture, une belle luminosité, c’est vraiment il faut le voir comme un lieu d’apaisement, comme lorsque tu te balades en forêt que tu entends le son des feuilles dans les arbres. C’est un endroit assez extérieur au reste du monde exactement comme les maternité, dans le sens que quand les jeunes parents sont à la maternité, leur temps est comme suspendu, parce qu’ils sont dans leur chambre avec leur bébé et rien d’autre ne compte pour eux. C’est vraiment un lieu de paix total. La cérémonie éclairci se passe dans une grande salle. En fait ils ont plusieurs salles selon la quantité d’éclaircie qui arrive en même temps dans le prologue, on va suivre l’éclaircie d’Éliott et de son père, il faut qu’on mette en place un rituel. Il faut qu’on mette en place qui sont les visiteurs qui viennent accueillir les nouveaux arrivants. Comment ils sont sélectionnés ? Ces visiteurs, il faut un peu les voir comme la famille sur terre 1 qui vient rendre visite et rencontrer le nouveau bébé. Je vais t’apporter d’autres précisions, mais déjà notre celle-ci à peu près classe-les. Regroupe-les avec les autres qu’on avait déjà pour le prologue. À noter aussi que je n’ai absolument pas relu le prologue, je veux recommencer de zéro. Garde-moi une version du prolo actuel, mais ne m’en parle pas, pars du principe qu’on recommence ensemble le prologue quand on aura bien avancé, je relirai l’ancien et je verrai si il y a des choses qui m’intéresse à prendre dedans.

---

### [204] 2026-08-17 à 13:32

Il faudrait arriver à considérer les capsules. Je ne vois pas comme une technologie hyper avancée, quelque chose avec des écrans de partout. Ça reste vraiment très proche de l’organique. À la toute base, j’avais comme idée que les capsules étaient encastrés dans un tronc d’arbres, comme si il y avait un arbre mère, mais je veux pas cet élément-là. Je trouve que l’arbre mere est quelque chose qui revient trop souvent dans les histoires de science-fiction. C’est pour ça que j’imagine vraiment un aspect type forêt.

---

### [205] 2026-08-17 à 14:12

imagine.. un espace, un peu comme le santuaire de la verité à pataya. l'architecture est tres ornement, toute en courbe et arabesque. comme autre reference, imagine maintenant la scène de fin de passenger, avec chriss pratt et jennifer lorens, quand d'un arbre planté en plein milieu du vaisseau, l'entiereté du hall est devenu une immense boule de nature ayant pris le dessus sur l'architecture. dans l'un, je veux te montrer le style d'ornementation tres travaillé exactement comme un santuaire. dans le secon, la nature qui a repris ses droits. ici, dans la ruche, on est dans un environnement maitrisé. un sanctuaire qui meme s'il semble tres ouvert est en fait un immense complexe avec de la vegetation interieur

---

### [206] 2026-08-17 à 15:00

c'est ça pour le fruit tu as entièrement raison, je voyais ça comme quelque chose à mis chemin entre une coque de fruit et une crysalide. la capsule d'éclaicie, c'est que c'est le moment de l'ouvrir avant qu'elle ne se derobe sous sont propre poids. une capsule à maturité veut dire qu'elle est sur le point d'ouvrir. on prepare alors la ceremonie en consequent pour l'ouverture. quand ce sont des capsules qui grandissent, plus de public est présent car l'évenement est annoncé. quand ce sont des capsules qui surgissent trop rapidement, moins de monde. quand c'est l'heure de la ceremonie, les veilleurs savent estimer le temps entre la maturation, l'ouverture et l'eveil. en gros, maturation d'une capsule, on "decroche" la capsule et on l'envois dans une autre service. la bas, chirugicalement, on procede à l'ouverture sans enlever le "capot", le capot est opaque, comme une couvercle. on a du mal à disserner la silhouette de l'arrivant car sa peau se confont avec le fond de la capsule. elle est recouverte d'une sorte de voile gelatineux orangé qui peut s'enlever sans que sa bave de partout. un peu comme si la capsule l'avait contenu dans une position conforable. dans ce service, on branche des machine à la capsule pour surveiller l'evolution. une fois qu'elle ont été préparée pour la cérémonie, on les amène dans la salle de cérémonie. ce n'est qu'à se moment là qu'on retire le capot et tout le monde peut découvrir l'arrivant et son age corporel. l'ouverture de la capsule provoque un reflexe pupillaire par le simple fait de l'ouvrir, tranchant avec la sensation de fraicheur de l'exterieur, le trop plein de luminosité etc. l'individu se reveille alors, un peu perdu, comme lorsqu'on se reveille d'un profond sommeil. Avant que la capsule n'arrive avec les preparateurs (le role un peu des anesthesiste qui accompagne la femme enceinte dans notre monde), les veilleurs ont déjà préparé la salle. il sait cb d'arrivant, donc choisi sa salle en fonctionn. il prepare comme des postes, un par capsule. un poste avec un miroir sur pied roulant, une lumière et une bassine .  au centre de la salle, une tablé avec un pichet d'eau et des verres repartie tout autour. pendant la ceremonie, il eveille tour à tour chaque capsule s'il y en a plusieurs. toujours le meme rituel : il ouvre, l'arrivant encore commateux. le couvercle est un peu ramoli (pas comme lorsque la capsule n'est pas encore à maturité) il peut la plier et on ne vois alors que le visage est les epaules. quand il s'agit d'un individu de petite taille, forcément on a un couvercle a enlevé sur une plus grande surface car la capsule en elle meme ne permet pas de juger la taille. elles sont touts identiques. dans un geste cérémonieux, il déplace le mirroir en biais de l'arrivant de manière a ce que son premier regard se porte sur son apparence à lui. c'est sa propre rencontre. le veilleur est positionné de l'autre côté, profitant du temps d'égarement pour noté avec precision l'age de l'arrivant et les données qu'il soit récolté sur son metier. il inspecte la capsule pour verifier à premiere vue son etat. dans ses notre figure aussi le temps de maturité que les preparateurs lui on remis. ensuite le veilleur attend patiemment  que son regard se porte sur lui. c'est un signe qu'il est possiblement prete et est capable d'entendre desormais. il lui demande son prenom, le mot par lequel il veut qu'on l'appelle. instinctivement lapersonne va repondre, on decouvrira sa voix, son intonation. pendant ce temps là, un autre veilleur aura sélectionné les vetements de la bonne taille dans un tas adjacent. Quand le veilleur passe à l'arrivant suivant, le second veilleur prend le relais, finis d'oter completement le couvercle, netoie le tour du corps, recupere des echantillons de gelatine dans la bassine.il l'aide à sortir doucement de la capsule, parfois il devra etre aidé, parfois non. on l'enveloppe dans une serviette de ceremonie, un peu comme les serviette de plage pour enfant ou on passe la tete par un trou au milieu, et on guide/ porte alors l'arrivant et on le pose sur une des chaises sur centre de la table. si l'arrivant est jeune, un assistant recuperera rapidement une chaise haute. si l'arrivant est vraaaaaaiment trop jeune, ce n'est pas un veilleur qui s'occupe de le transporter, c'est un berceur commi d'office qui le prendre dans ses bras et viendra s'asseoir autour de la table. 

pendant ce temps là, le veilleur principal à enchainé et recommence son procédé s'il y a un deuxième arrivant. le sedonc veilleur comme une danse parfaitement synchronisé repetera lui aussi ses getes et des assistant le rejoindront au besoins. quand le veilleur principal  a terminé, il attent patiemment, en retrait de la tablé. le decond finit la derniere installation et se met en retrait aussi. (si qu'une capsule, le veilleur 1 se met direct en retrait. il y aura toujour 2 veilleurs minimum). ue fois que chacun est assis autour de la table, la seconde partie de la ceremonie a lieu, le veilleur 1 passe avec un pichet d'eau et remplit les verre de chacun, le recipiant etant toujours en fonctionne de l'age, verre, timballe, biberon. c''est un peu comme la premier action de leur vie, l'eau qui se repend dans leur gorge vierge pour tout de suite le donner leur premiere sensation d'apaisement après ce qui semble un long sommeil sans reve. le public vient alors religieusement déposer au centre de la tables des cadeaux de bienvenue, souvent en accord avec leur croyance, des choses qui sont censer apporter joie paix et bonheur. peut etre un certain type de fleur ou feuille. et il quittent la piece. le travail du veilleur s'arrete là. les prépérateur récupère les capsule et le bassine et parent les deposer dans une autre section.  


Tout au long du developpement d'une capsule il y a un "medecin des capsules" quand c'est possible, il verrifie l'evolution d'une capsule, son aspec avant ceremonie, il recueille les données sur veilleurs et font une etude de la capsule post ceremonie. ils etudie aussi la gelatine qui a ete conservée. (le placenta en quelque sorte) il est d'autant plus vigilant quand une capsule est arrivé d'un coup car elle n'a pas pu etre eutidé en amont.

pourquoi font 'il ça  ? c'est un peu l'équivalent de "né par voix basse ou en siege pour nous" c'est une information clinique, rien de plus.elle est rattaché à leur dossier médicale. on juge de la bonne qualité de la gelatine, du belle aspect de la cpasule, etc, ce qui revient dans les visites médicales

la c'est un peu plus flou mais c'est donc les données de la ceremonie qui font que la personne est "reconnue", un peu comme un passage en mairie après une naissance. c'est le veilleur qui gere ça. donc quand le public quitte la piece, le veilleur est la derniere personne a sortir aussi tandis qu'un autre groupe, un autre metier, vient prendre le relais. ils auront alors chacune le droit à une premiere visite medicale puis plusieurs dans la semaine. il reste 8 jours à la ruche avant d'etre guidé ailleurs.

---

### [207] 2026-08-17 à 15:06

ah et plus il y a d'arrivant, plus il y a de veilleurs et plus ont aura selectionné une salle de ceremonie grande

---

### [208] 2026-08-17 à 15:13

"La ruche n'a pas été conçue puis bâtie : elle a été bâtie autour. Il y avait là un endroit où les capsules apparaissaient, et une végétation qui y poussait. On a construit tout autour, et on a accepté de partager la place." bien formulé.

le livre pourra montrer le centre. le prologue, on va suivre le veilleur qui traverse le complexe. il pourrait alors entrevoir les 2 capsules du jour. il veillerait à choisir la bonne salle de ceremonie, etc. ce qui se passe à la fin de la ceremonie quand Andrew quitte la piece en temps que veilleur principal, on en parle pas dans le prologue, mais on pourra y venir quand ça sera au tour de decrir sa propre arrivée.

j'aime pas le fait que la phrase soit inscrite.
On pourrait imaginer quelque chose de physique, visible. le registre ne serait pas un livre, mais une piece, complexe que les veilleurs ont appris à lire avec le temps. a chaque capsule, sa ligne, gravee quelque part, une année, un age. le public n'a pas acces à cette salle. il ne pouvait pas mentir car quelque chose, ou quelqu'un en et le maitre, en etre l'écrivain. personne d'autre ne peut ecrire à sa place, on ne sait pas qui sait, on est dans une zone reculée des capsules dans le complexe. comme dans les archives. de la né le nom de l'archiviste. on ne le voit pas, mais dans leur foi, il existe.

les capsules, faut voir comment les fixer et ç quoi par contre...

---

### [209] 2026-08-17 à 15:18

je suis pas d'accord pour la cérémonie d'andrew. les capsule des jumelles ont eu un delai de maturation, égale au temps ou dans monde 1 elles étaient dans l'agonie. leur ceremonie est prévu. meme pas une heure après, celle d'Andrew apparait. le veilleur de l'époque le note est prend la decisions d'en faire une meme ceremonie groupé. non seulement il n'y aurait effectivement eu pas bcp de monde pour sa venue mais en plus ça aurait bloqué deux pieces de cérémonie pour pa grande chose. autant grouper, rajouter un post et c'est tout. la capsule qui arrive inopiné, c'est qu'elle a pop et les preparateur n'ont meme pas besoin de la preparer à l'ouverture, elle tient tellement à rien qu'elle pourrait s'ouvrir seule sans l'aide de personne. le preparateur branhe juste le machine pour le controle

---

### [210] 2026-08-17 à 15:24

"sans tronc ni cœur?" je les imagine bien comme sur une meme line de vetation qui s'enchverte un peu partout. les capsule sont à l'horizontal, comme attendant d'etre cueillit. imagine des champs de courge ou de melon, ça serait sympa, et pour la ceremonie, la capsule est amené et maintenant dans une verticalité presque complete

---

### [211] 2026-08-17 à 15:29

"c'est à une salle venue pour deux qu'on annonce trois arrivants." attention, ne me  fais pas dire ce que j'ai pas dit. c'est n'est pas parce que la capsule arrive d'une coup que personne n'es là ! oui il y a moins de monde mais il peut y en avoir quand meme. et aucun lien ne se fait entre le public et les arrivants. ils viennent parce qu'ils le veulent bien, pour celebrer une arrivée. le public ne se dit pas "zut, il y en a un 3eme" non, ce qui seront là ce diront "oh, il y en a un de plus" c'est tout. rien de cruel la dedans, c'est une question d'avoir prevenu plus tot ou pas. mais je suis d'accord avec toi, s'il n'y avait pas eu les jumelles, il y aurait eu moins de monde ! la grande ceremonie de la vingtaine d'enfant et des adultes était compliqué, peut de monde, pas assez de berceuse, là c'était une cérémonie compliqué et atypique. et au passage meme l'arrivee au jardin a ete compliqué, c'est un enorme groupe qui est arrivé en meme temps en plus de ceux qui étaient prévus

---

### [212] 2026-08-17 à 15:35

tu as des interrogations?

---

### [213] 2026-08-17 à 15:54

① Le registre enregistre-t-il seulement l'arrivée, ou toute la vie ? je te poserai la question suivante : la maternité enregistre-elle seulement l'arrivé ou toute la vie ? 

pour moi la reponse est non, c'est administrative. comme le livret de famille qui a aussi une page pour les deces.

② Les lignes d'Andrew et des jumelles se touchent. on peut tres bien créer 2 lignes, une pour les jumelles, une pour lui et le tueur.

③ Que deviennent les capsules vides ? je te retourne la question ? Que devient leplacenta après accouchement ?

④ Est-ce que la coulée atteint la salle du registre ? je comprends ton reseonnement. ou alors, justement les capsules "sortent" de cette endroit. c'est un peu un sac de noeuds, ou plutot un sac de racine qui  est ancré tout autout de cette salle. et c'est une "salle ouverte" presque une clairiere avec des arbres, des sorte de stèles et des gravure. un veilleur sait ou regarder et quoi lire. il connait la piece par coeur et s'est quand quelque chose à bougé. ça donne un aspect ruine abandonnée qui n'e fais pas vraiment ruine. c'est bizarre à formuler mais comme lorsque je parlais du jardin comme une mini ville dans une ville, et bien imagine ce lieu comme pas forcement un lieu fermé à tous et reservé d'au veilleur mais un lieu séparé du reste du comprexe par de la creation humaine (le santuaire de pataya). l'homme a voulu conserver cette epicentre comme quelque pas quelque chose de sacré. c'et rare que d'autres personne que des veilleurs y entre car déjà c'est un lieu a avec bcp de croyance autour, mais aussi parce qu'une personne lambda ne sait pas lire ce lieu

---

### [214] 2026-08-17 à 16:03

le registre ne doit pas contenir la fin

---

### [215] 2026-08-17 à 16:09

"une pour les jumelles, une pour lui et le tueur »" je parlais des lignes ! donc non, c'est pas "Une ligne par capsule" c'est une "ligne par lot de capsule arrivé en meme temps" et ça leve une erreur de ma part, c'est une ligne pour les jumelle et une pour elle. le tueur n'existe pas. en revanche, les veilleurs peuvent soit eux meme inscrire quelque part les jours et les heures ou une capsule non eclaircies est arrivé ou alors, elle est elle aussi dans le registre mais inscrite d'une autre maniere. peut etre un point ou un symbole un peu graphique que les veilleurs n'ont jamais considérés comme tel

---

### [216] 2026-08-17 à 16:15

bah. c'est surtout pour le reveal. comment on peut expliquer rapidement que Andrew comprenne d'une seule traite la ligne des jumelles, la sienne et la revelation de ce qu'est la capsule du tueur si il peut pas le lire du premier coup ? dans cette cette là, il est dans la salle du registre! je trouve bizarre de l'en faire sortir et venir comparer les lignes du registres avec son petit calepin de veilleur pour dire "oh fait, il y avait une capsule pourrie aussi ce jour là" tu vois ce que je veux dire ?

---

### [217] 2026-08-17 à 16:21

bah c'est là que je coince un peu.. pourquoi le registre indiquerai des marques pour les capsule pourrie au meme endroit que des capsules en maturation ? si les veilleurs n'ont pas fait le lien, c'est chaud... il faudrait trouver une autre solution qui lui fasse tiquer sur le fait que ce jour là, il y avait bien une capsule pourrie dans un autre couloir entrian de se faire racler. ah et au passage, pourquoi l'odeur se sent depuis la salle de ceremonie, c'est que mine de rien,  on est pas accolé mais on est pas loin. les veilleurs sont sencé vite nettoyer pour eviter de contaminer les autres (par croyance) l'odeur reconnu ce jour là pourrait très bien etre celle d'un veilleur qui venait de nettoyer la capsule. un autre qui lui dirait "tu aurait pu enfiler une autre tenu quand meme..."

---

### [218] 2026-08-17 à 16:24

"Le bâtiment semblait avoir été taillé dans un seul morceau de pierre, comme si une carrière entière avait été sculptée jusqu'à disparaître sous les mains d'un artisan démesurément patient.

Chaque surface était couverte de figures. Des dieux, des animaux, des créatures dont les corps se mêlaient aux volutes végétales et aux arabesques, s'enroulaient autour des colonnes, grimpaient le long des murs et se penchaient au-dessus des passages. Rien n'était laissé nu. Même les escaliers semblaient avoir été sculptés comme des œuvres à part entière : leurs rampes se déployaient en courbes élégantes, peuplées de visages, de fleurs et de silhouettes figées dans des poses impossibles.

À mesure qu'il avançait, le regard ne savait plus où se poser.

Une statue surgissait d'un angle, puis une autre derrière elle. Des mains soutenaient des balcons, des corps semblaient naître des piliers, des animaux fantastiques se fondaient dans les ornements. Au-dessus, les toitures s'élevaient en pointes successives, hérissées de sculptures si fines qu'elles semblaient presque irréelles. L'ensemble avait quelque chose de vivant, comme si le bâtiment n'avait pas été construit, mais avait lentement poussé.

Puis il franchit le seuil.

À l'intérieur, le silence semblait plus profond.

La lumière venue de l'extérieur se perdait dans la pénombre des salles, glissant sur le bois sombre et révélant peu à peu les détails enfouis dans les murs. Des rangées de colonnes massives s'élevaient autour de lui. Chacune était différente, chacune semblait raconter sa propre histoire. Des silhouettes humaines s'y entremêlaient aux feuillages, aux serpents et aux créatures mythiques, leurs corps supportant les arches comme s'ils avaient été condamnés à porter le poids du sanctuaire pour l'éternité.

Au-dessus de sa tête, les plafonds disparaissaient dans l'ombre.

Partout, les sculptures se superposaient : des visages derrière des dragons, des divinités dissimulées entre deux ornements, des ailes et des mains émergeant des ténèbres. L'or et les teintes chaudes du bois accrochaient les rares rayons de lumière, donnant à certaines figures l'impression de surgir de la pierre sombre.

Au fond de la salle, une ouverture baignait dans une lumière blanche presque aveuglante.

Après toute cette profusion, cette simple trouée vers l'extérieur paraissait immense.

Le sanctuaire donnait alors l'impression d'un monde enfermé dans la pierre— un monde où chaque centimètre avait été consacré à raconter quelque chose, où l'architecture n'était plus seulement faite pour abriter les hommes, mais pour leur rappeler leur petitesse face à quelque chose de beaucoup plus ancien, plus vaste et plus mystérieux." 

tiens ce texte est interessant comme ref pour les murs et éléments style santuaire de pataya.

---

### [219] 2026-08-17 à 16:27

et justement "Le reste, il le tient de son seul souvenir. Qui était dans cette capsule ne se saura jamais — il suppose, le lecteur suppose avec lui, et le livre ne confirme rien."  ça me derange justement, je veux l'ecrire pas directement, mais je veux que le lecteur n'ait aucun doute sur cette info!

---

### [220] 2026-08-17 à 16:32

"Pour la couleur, la référence tranche presque : bois sombre, or, teintes chaudes pour les passages — et le bleu et l'orangé pour la trouée du fond. Tes deux directions cessent d'être concurrentes." elle seront contredisent pas la complémentarité des couleurs... je pense que au vu de l'espace tres gris vert, il faudrait une couleur complementaire pour les tenues, les decorations de ceremonie. on parlait de capsule orangé. parce que le orange ne choque pas comme coque dans des travées... mais on partirait sur quoi ? du bleu type #004572 ou plus claire #0081B3 avec un orange qui rapelle celle des capsules :  #ec9006 ?

---

### [221] 2026-08-17 à 16:34

"elles étaient rares" pas d'accord.. c'est pas en une decennie que le crime s'est multiplié... mais l'historique de veilleur peut le soulever

---

### [222] 2026-08-17 à 16:36

"il meurt pendant la poursuite — la dernière scène de Joël, colonne 30 — et Joël y meurt aussi. " mais c'était prévu ça haha ils meurent tout les deux dans l'accident de voiture. il rentre dans un mec, Joel rentre dans sa voiture à son tour. gros carrembolage. en fasse c'était un poids lourds, il a quasi pas bougé alors que la voiture du tueur s'est encastré dedans et que celle de Joel a suivi betement. la voiture du tueur s'est retrouvé prise en sandwitch entre le camion et la voiture de flic et Joel a fait un choc frontal en rentrant dans la voiture du tueur

---

### [223] 2026-08-17 à 16:46

"Andrew n'assemble rien. Il ne sait pas qui étaient ces deux filles, il ne sait pas comment il est mort, il ne sait pas qui était dans la capsule qu'on raclait ce matin-là. Il vient vérifier un détail de sa propre cérémonie, et il repart avec la confirmation d'un détail." houla tu vas ou tu vas ou ? bien sur qu'il sait comment il est mort.. dans le chapitre ou on assise à la poursuite, le chapitre d'après il resalise que la sihouette n'a pas bougé. il realise donc qu'il a vu sa propre mort. c'est ce qui le pousse à aller verifier. et si, justement, en verifiant il se posait cette question ? est-ce que cette enflure avec pu s'échapper ? et alors une intuition. il se souvent du 'tu aurais pu enfiler une autre tenue" et il connecte alors

---

### [224] 2026-08-17 à 16:53

je suis d'accord avec toi sur le fait de récapituler mais... "Et le réglage tient parce qu'il comprend un fait, pas une histoire." pas du tout d'accord. bien sur qu'il a compris. à sa propre mort il a tout compris. il s'appelait Joel, il a ressenti cette colere aveuglante dans son reliquat, il a senti qu'il aurait pu tuer pour ces jumelles. il sait tout sur sa ligne. Pour ce qui est de l'homme a cote d'eliott, non il sait pas, et c'est eliott qui lui apporte cette reponse. dans la salle du registre, on pourrait lui amené comme des reliquats par flash. le visage de june qui disparait quand elle lui dit qu'eliot à disparu, par le visage d'une parfaite inconnue qui dit qu'elle s'inquiète" "son regard qui se pose sur la photo d'identité d'eliott dans un dossier, dédoublé et devant une photo de famille des 2 jumelles"

---

### [225] 2026-08-17 à 16:58

"s'il sait qu'il parle de lui, la fin s'écroule », et tu avais validé. alors j'ai pas du comprendre ta phrase. Poiur moi c'est normal que sa mort soit l'élement choc et que la confirmation du registre lui fasse realisé qu'il est Joel. j'étais d'accord dans l'épilogue de ne pas cité Joel. mais a aucun moment j'ai dit qu'il ne devait pas le comprendre ! et je penses que les superpositions dans la salle des resigistre a la fin son juste parfaites. tout le long du livre on a superposé les scène sans sans rendre compte en temps que lecteur. comme si lui meme l'ignorait. et enfin, dans la salle du registre, il superposte clairement, deux lignes de vie, des souvenir presque parallèle.

---

### [226] 2026-08-17 à 17:00

bon bah on s'est mis d'accord sur ça ahah estce qu'on y voit plus clairement maintenant pour le reveal d'une capsule non eclaircie ?

---

### [227] 2026-08-17 à 17:12

"et il se dit « bien fait pour sa gueule" arrivé à se stade de l'histoire on ne se dit pas bien fait pour sa gueule, on trouve juste la capsule pourrie revulsante, c'est une description crade et nauséabone" c'est au moment ou Andrew connect, qu'en temps que lecteur on connecte avec lui et là, seuelemt LA on se dit bien fait pour sa gueule.

"la pierre mouillée, le fond sucré," je sais pas d'ou ça sort, ça degage" mais oui après dans l'idée, on pourrait... je sais pas, décrire la capsule avec un vocabulaire precis, qui se succede. je dis n'importe quoi mais on pour dire "une odure, insipide, et prenant au nez, comme si [on cree une image mental] et à la fin, un truc du style 
"-tu aurais pu changer de tenue!
et là il la remarqua, cette odeur, insipide et prenant au nez, comme si [on cree une image mental]..."
Tu comprends lidée, le lecteur ne peut que se souvenir de cette phrase, cité nulle par ailleur que dans le chapitre de la capsule pourrie. la derniere ligne du chapitre

---

### [228] 2026-08-17 à 17:25

est-ce qu'on se lancerait pas maintenant dans un test de prologue, avec toutes les infos que tu as ? on garde en tete que c'est la decouverte de la ceremonie d'eliot et son "père". On est donc dans la salle de ceremonie. on peut rapidement ouvrir sur le fait qu'Andrew entre dans la salle de ceremonie, qu'il y prepare les poste en attendant l'arrivee des preparateur. ce n'est pas ici qu'on decrit le complexe entier. ça on le garde pour la journée type. ici on se concentre uniquement sur la salle de ceremonie et la cermonie en elle meme. On decouvre ensemble l'arrivee des 2 capsules jusqu'à et leur premiere "boisson". on n'oublie pas le rappel à l'épiloque, Eliott a vu son visage en premier dans le miroir, puis la foule, puis Andrew et enfin l'autre arrivant. il a bugué sur ce visage comme une "je le connais déjà" mais on ne doit lpas le percevoir comme tel. il l'observe mais peut etre par curiosité, de voir ce qu'Andrew lui fait . la scène se termine quand Andrew referme la porte sr les visiteur et qu'il quitte la piece à son tour. On aura une belle description de l'aspect de la capsule, de la gelé, une desciption de la preparation du corps à sa sortie de la capsule, avant ça on aura le procédé methodique d'andrew quand il prepare la salle avant l'arriver des 2 capsules...

---

### [229] 2026-08-17 à 17:30

attention aux repetition des metiers, des prenoms etc.. on varie. et tu t'inspires bien sur du style d'écritue de l'épilogue

---

### [230] 2026-08-17 à 19:12

"Deux, ce n'était rien. On parlait encore de la fois où il avait fallu ouvrir la salle du bas et faire venir des veilleurs de trois services pour en recevoir vingt-six le même matin. Ce jour-là, avait dit un ancien, on n'entendait pas le pichet." dans une version comme dans l'autre on le dit pas ici. on y viendra avec la suite de l'enquete.



___ bon j'ai repris la suite des 2 versions, voilà ce que j'iame bien de part et d'autre :

"LA CÉRÉMONIE

On lui avait donné la salle six pour deux capsules.
C'était trop grand, et il n'avait rien dit. On ne discute pas une salle.
Il poussa la porte de l'épaule, les bras chargés, et la lumière lui arriva dessus d'un coup. Elle tombait de très haut, par les ouvertures ménagées entre les nervures du plafond, et se posait en longues bandes obliques sur les dalles. Le long du mur du fond, la coulée courait — une seule ligne épaisse, entrée par une bouche, enroulée autour de deux colonnes, ressortie plus loin sans qu'on sache où elle allait.

Personne ne l'avait plantée là. On avait bâti autour, et on avait sculpté tout le reste : [des corps arqués sous les arches, des mains qui tenaient les balcons, des visages qui sortaient de la pierre à mi-hauteur et qui regardaient tous vers le milieu de la pièce. Il en manquait un à gauche du seuil, dont il ne restait qu'une épaule. Il manquait depuis avant lui.] dans une version comme dans l'autre, la desciption est pas dingue. on n'a pas a parler de balcon, il n'y en a pas.

Andrew posa ses affaires sur la table et compta.
Deux.
Il roula le premier miroir depuis le mur jusqu'à l'emplacement du poste, et le bloqua au pied. Il l'essuya avec le linge accroché à la barre, en commençant par le haut. Il recula d'un pas, se vit dedans, et le tourna vers le mur.
Puis la lampe sur pied, à hauteur d'épaule, orientée vers le sol et pas vers le visage. Puis la bassine, posée à droite, vide, avec les flacons dedans.
Il refit les trois gestes deux mètres plus loin.

Restait la table, qu'il trouvait toujours trop bien mise. Le pichet au milieu, l'eau tirée du matin, et à chaque place un verre, une timbale et un biberon. Personne ne savait qui allait sortir. Une capsule est une capsule, du dehors, et on ne juge pas de la taille de ce qu'il y a dedans ; alors on posait les trois, et on prenait celui qu'il fallait le moment venu, et on remettait les deux autres à l'office sans y penser. La pile de serviettes suivaient le même principe : quatre tailles, et il en descendit une de chaque.
Il compta les places. Deux.
Il compta les chaises. Il y en avait douze autour de la table, comme dans toutes les salles.
Les visiteurs arrivèrent avant les capsules, comme toujours, par petits groupes, et ils s'installèrent le long des murs en parlant à voix basse. Ils s'appliquaient à parler bas. C'était une chose qu'on faisait ici sans que personne l'ait jamais demandé.
Nora entra la dernière, en nouant ses manches.
— On est deux ?
— On est deux.
— Alors c'est un bon jour.

____________
Les préparateurs firent rouler les deux chariots jusqu'au milieu de la pièce, et un murmure passa le long des murs. [preparateur arrive de manière trop abrupte. on sait pas qui saiton peut les distingué par des preparateur, des agents du service opérant dans la serre (la serre etant la zone ou serpente la coulee autour de la zone du registre)]

Elles étaient couchées, l'une et l'autre, comme on les avait cueillies. Une capsule, ça ne pousse pas debout : ça pousse à plat sur la ligne, en rang avec les autres, et il faut la détacher de ce qui la porte. Celles-ci l'avaient été deux jours plus tôt, à quatre travées d'écart, apparues le même matin. Andrew le savait parce que c'était écrit sur la fiche, et parce que c'était son métier de le savoir. (pas bon, les capsules d'Eliott et son père sont arrivé d'un coup. pas d'histoire d'arrivé plus tot. c'était inipiné, il a fallut preparer la ceremonie rapidement. après rpaidement veut pas dire que c'est archi pressé. ce qui semble activer les corps, c'est quand on ote le couvercle. il faut pas tarder mais c'est pas non plus une urgence. juste que question organisation, ils se doivent d'etre attentifs)

Elles étaient belles. Il n'y avait pas d'autre mot dans le service et personne n'en cherchait : la paroi avait pris ce jaune très pâle qui vient à la fin, presque de la corne, et par endroits on voyait au travers. Une ombre plus dense, une courbe, quelque chose de replié. On ne distinguait rien de plus. La dedans, tout se confond avec le fond, et ceux qui prétendent reconnaître un genou ou une épaule à travers une paroi mentent, ou débutent. (enlever peau c'est mieux je trouve, ça interroge et dans la phrase d'après on est étonné de voir le champs lexical de l'anatomie)
Sur le dessus, le capot était en place. Opaque, mat, plus sombre que le reste. En dessous, tout avait déjà été fait — ouvert, dégagé, refermé, dans une autre pièce, par d'autres mains.
Les préparateurs redressèrent les chariots.

C'est le dernier geste, et c'est le seul moment où une capsule se relève. Elle passa de l'horizontale à la verticale en trois crans, très lentement, avec un bruit de crémaillère que tout le monde entendit, et quand elle fut debout on aurait dit qu'elle était debout depuis toujours.
Une fiche lui passa dans la main. Le préparateur inclina la tête et recula jusqu'à la porte, où l'autre attendait déjà. Leur travail s'arrêtait là pour l'instant. Une posture droite, les mains croisés devant eux. futur spectateur à leur tour de ce qui allait suivre. (je rappelle qu'il restent passifs et sortent les capsules vides de la piece à la fin)


________________________
Andrew prit le capot de la première capsule à deux mains et le fit glisser vers le bas d'un quart.

La lumière entra dedans.

Le corps eut un mouvement — pas un sursaut, un ralentissement de tout, comme quelqu'un qu'on tire d'un sommeil trop profond et qui remonte par paliers. Les paupières bougèrent sans s'ouvrir. Elles s'ouvrirent, se refermèrent aussitôt sur la lumière, se rouvrirent à moitié. Les pupilles mirent longtemps à se faire.

Il avait dix ans, ou à peu près. On chuchota douze le long du mur de droite, et treize plus loin, et Andrew, qui n'aurait rien dit même si on lui avait demandé, pensa dix.

Le voile de gelée le recouvrait entièrement, orange, épais, mat, sans une goutte nulle part. Ça ne coule pas, cette chose-là. Ça s'enlève. Andrew posa la main à plat sur l'épaule et fit descendre la paume : le voile vint d'un seul tenant, roulé sur lui-même comme une peau de fruit, et découvrit le bras et la main, qui étaient parfaitement propres et parfaitement secs. Il le déposa dans la bassine. Il recommença sur l'autre épaule. Le corps était placé comme on se place pour dormir quand on n'a mal nulle part.

Andrew fit pivoter le miroir sur son pied et le régla en biais, à la bonne hauteur, un peu de trois quarts.

Le garçon se vit.

Il resta là-dessus un long moment. Il ne fit pas les gestes qu'on attend, il ne toucha pas son visage, il ne s'approcha pas. Il regarda, et sa respiration changea de rythme deux fois.

Puis il regarda le mur de droite, et les gens le long du mur de droite, et le mur du fond, et le plafond très haut, et il chercha d'où venait la lumière. (il doit lancer un regard a l'autre arrivant. d'ou l'importance que la phase du nom lui doit demandé avant tout. il repond et ensuite on enchaine sur sa "demence apparente" car c'est à partir du nom donné qu'Andrew bascule sur la deuxième capsule et ouvre le capot. pendant ce temps, Nora a pris le relais avec Eliot.)

Et il parla.

— Il est pas remonté.

Le long du mur, le murmure s'arrêta.

— Il faut aller le chercher. Il est pas remonté.

Sa voix ne tremblait pas. C'est ça qui n'allait pas. Elle était nette, pressée, avec l'articulation de quelqu'un qui répète une chose importante à quelqu'un qui n'écoute pas assez vite, et elle sortait d'un corps encore à moitié pris dans sa capsule.

Quelqu'un demanda tout bas s'il y en avait une troisième. Un préparateur fit non de la tête, depuis la porte.

— Il faut y aller.

— Ça arrive, dit Nora, pour la salle. Ça arrive souvent.

Elle avait dit ça avec beaucoup de douceur, et c'était vrai. Ils sortent avec la langue et rien d'autre, et la langue tourne à vide un moment avant de se poser sur quelque chose. Il n'y a rien à comprendre ; il y a à attendre.

Le garçon rouvrit la bouche, la referma. Il redit une fois « il faut y aller », plus bas, pour lui, et ce fut tout.

Andrew regardait la fiche. Il inscrivit l'aspect de la capsule, la durée de maturation que les préparateurs avaient portée en haut, l'état du voile, et il laissa l'âge de côté pour plus tard, parce que l'âge se relève à l'instrument et pas à l'œil.

Puis le regard du garçon se posa sur lui.

C'est le signe. On ne parle pas avant.

— Bienvenue à toi.

Il attendit.

— Ici, chacun a un mot qui le désigne. Un seul, et c'est le sien, et il ne changera pas. Comment veux-tu qu'on t'appelle ?

Il répondit tout de suite, sans réfléchir une seconde, comme on répond à une question dont on connaît la réponse depuis toujours.

— Eliott.

Andrew l'écrivit. Il écrivit le numéro à la suite, sans y penser, et souligna les deux.

Derrière lui, Nora avait déjà fait glisser le capot en entier. Elle passa autour du corps, décolla ce qui restait de gelée aux plis du coude et du genou, en préleva de quoi remplir deux flacons, les boucha, les rangea dans la bassine. Elle tendit les mains. Le garçon les prit et sortit tout seul, les jambes hésitantes, et elle le tint le temps qu'il faut. Elle lui passa la serviette par la tête, rabattit les pans sur le devant, et l'installa à la tablée.

Il avait la tête qui tournait vers la salle et qui revenait vers la table. Il ne disait plus rien.

_____

L'autre poste attendait.

Second capot, un quart, la lumière dedans.

Celui-là mit plus longtemps à revenir. Une quarantaine d'années, et pour une fois personne ne se trompa de beaucoup. Il ouvrit les yeux, les referma, les rouvrit, et regarda le plafond très haut sans rien y chercher.

Le voile descendit de l'épaule et du bras. Le miroir pivota.

Et depuis la table, à quatre mètres de là, le garçon regardait.

Il regardait ce qu'on faisait à l'autre. Les mains sur l'épaule, le voile qui vient d'un tenant, le miroir qu'on tourne. Il regardait comme on regarde quelqu'un subir la chose qu'on vient soi-même de subir, avec cet intérêt un peu bête qu'on y met.

L'homme se vit dedans. Il regarda longtemps, lui aussi.

Il dit qu'il s'appelait Nicolas  quand on le lui demanda, et il en sortit une voix grave et éraillée qui surprit tout le monde, lui compris.(le debut de la phrase est bizarre dans sa conjugaison)

On lui ôta le capot. On nettoya, on préleva, on l'aida, on l'enveloppa, et on l'assit à la table, à la place voisine.

Il posa les mains à plat devant lui parce qu'il ne savait pas quoi en faire.

Puis il tourna la tête.

Eliott le regardait déjà.

Quelque chose se ferma sur son visage. Ça dura le temps que ça dura, et il tira sur sa serviette parce qu'elle glissait de l'épaule.

À ce moment-là, Andrew refermait la bassine.

_____

Il prit le pichet et fit le tour de la table.

Il posa la timbale devant le garçon et la remplit. Il posa le verre devant l'homme et le remplit. Il remit le reste à l'office sans y penser. (a 10 ans tu bois plus dans une timballe)

Ils burent tous les deux.

C'est la première chose qu'ils faisaient. Il n'y en avait pas eu d'autre avant celle-là, et il y a toujours ce moment, à chaque cérémonie, où quelque chose se relâche dans les épaules et dans la mâchoire de gens qui n'ont pourtant pas eu soif une seule fois de leur vie. L'homme reposa son verre, regarda le fond, et le reprit. (une seule fois de leur vie... ouf la formulation)

Alors la salle s'avança.

Ils vinrent un par un déposer au centre de la table ce qu'ils avaient apporté. Un fruit. Une petite chose en bois. Trois brins liés par un fil. Une pierre plate. Personne n'expliqua rien, personne ne se présenta, et personne ne s'adressa à eux autrement qu'en inclinant la tête. Ils n'étaient pas venus pour ces deux-là. Ils étaient venus parce qu'il y avait eu une arrivée, et il y en avait eu une, et elle avait été belle. (un peut trop froid.. c'est une arrivée, c'est cool de voir une capsule s'ouvrir, on reste dans un silence ceremonieux, maisil y a l'exitation du moment, ça reste une naissance !!)

Puis ils sortirent, dans le même ordre où ils étaient entrés.

Andrew tint la porte le temps que le dernier passe, et il la referma sur eux.

Le bruit du couloir s'arrêta net.

Nora emmena les deux vers la porte du fond, où le service suivant attendait. Le garçon se retourna une fois avant de sortir, mais pas vers la table.

Les préparateurs reprirent les capsules, les couchèrent sur les chariots, chargèrent les bassines et les emportèrent. Un moment plus tard, il n'y avait plus dans la salle six que deux miroirs, deux lampes, une table avec des cadeaux dessus, et un homme debout avec un carnet.

Andrew reporta les deux lignes. Le jour, la travée, la durée, l'aspect, l'âge relevé, le mot, le numéro. Il écrivait vite, d'une écriture qui n'était belle nulle part ailleurs.

Sous les deux lignes, il y avait une case pour les observations.

Il la regarda un moment, puis il rangea le carnet.

Il éteignit les deux lampes et sortit.








"

je te laisse analyser ce que je t'ai ecris entre parenthèse à chaque fois

---

### [231] 2026-08-17 à 19:58

oui je valide ça : Trois choses sont neuves pour le monde et j'attends ton feu vert avant de les inscrire : la serre comme nom de la zone où serpente la coulée autour du registre, le fait que c'est l'ouverture du capot qui active le corps, et Nicolas comme nom d'éclaircie.

je reprends une passe sur le texte, des choses me font tiquer

---

### [232] 2026-08-17 à 20:30

" Elle tombait de très haut, par les ouvertures ménagées entre les nervures du plafond, et se posait en longues bandes obliques sur les dalles." est-ce que c'est la lumiere du soleil que tu définies là ? car si c'estle cas c'est bcp trop subtil, autant le placer vraiment.

"Puis la lampe sur pied, à hauteur d'épaule, orientée vers le sol et pas vers le visage. Puis la bassine, posée à droite, vide, avec les flacons dedans." les puis et puis, mieux vaut revoir la phrase.

"Il refit les trois gestes deux mètres plus loin." trop subtil. plutot : Quand il eut terminé de mettre le premier poste en place, il s'affaira au deuxième, réitérant deux mètres plus loin : lampe, miroir, bassine.

"Restait la table, qu'il trouvait toujours trop bien mise." : "Restait la table. elle tronait au milieu de la pièce, éclairé par un halo de lumière. Il pris d'une deserte contre un mur une nappe blanche et tout lisse, ainsi que son chemin de table, une grande bande rectangulaire orangée. Il les ajusta sur la table immaculée avant d'y déposer un pichet d'eau au milieu. un allé retour sur la desert, 2 verres, 2 timballes, 2 biberons. il les aligna, un de chaque de part et d'autre de la carafe (j'ai pas de synonime pour pichet)."

"Personne ne savait qui allait sortir. Une capsule est une capsule, du dehors, et on ne juge pas de la taille de ce qu'il y a dedans ; alors on posait les trois, et on prenait celui qu'il fallait le moment venu, et on remettait les deux autres à l'office sans y penser. La pile de serviettes suivait le même principe : quatre tailles, et il en descendit une de chaque." : "Personne ne savait qui allait sortir . On ne pariait pas. Alors on posait les trois, et on prenait celui qu'il fallait le moment venu, et on remettait les deux autres sur la desserte sans y penser. La pile de serviettes suivait le même principe : quatre tailles, et le veilleur en descendit une de chaque."

"Il compta les places. Deux.
Il compta les chaises. Il y en avait douze autour de la table, comme dans toutes les salles." - aucun interet.. "Il compta les elements sur la table, 7. on était bon. Il recupera 2 chaises du tas empilé juste à coté de la deserte."

"Les deux préparateurs firent rouler les chariots jusqu'au milieu de la pièce, et un murmure passa le long du mur." : deux nouvelles personnes, des préparateurs, firent rouler ldeux chariots jusqu'à, leur poste respectif et un murmure passa le long du mur.

"Ils étaient de la serre. Ce sont eux qui vivent au milieu de la coulée, qui la suivent d'un bout à l'autre, qui savent à la main quand une capsule est prête et qui la décrochent. On ne les voit qu'à ce moment-là, deux fois par cérémonie, et ils ont toujours l'air de sortir d'ailleurs." : conconrde le temps, le present va pas ici

"Une capsule à ce point-là ne se garde pas. On ne court pas, mais on ne s'assoit pas non plus." a enlever.

"Elles étaient belles. Il n'y avait pas d'autre mot dans le service et personne n'en cherchait : la paroi avait pris ce jaune très pâle qui vient à la fin, presque de la corne, et par endroits on voyait au travers. Une ombre plus dense, une courbe, quelque chose de replié. On ne distinguait rien de plus. Là-dedans, tout se confond avec le fond, et ceux qui prétendent reconnaître un genou ou une épaule à travers une paroi mentent, ou débutent." :  "[detailler une forme globale, coluptueuse, allure delicate, naturelle, oragnique]. Elles étaient belles. La paroi avait pris ce jaune très pâle qui vient à la fin, presque de la corne, et par endroits on voyait au travers. Une ombre plus dense, une courbe, quelque chose de replié. On ne distinguait rien de plus. Là-dedans, tout se confondait avec le fond, et ceux qui prétendaient reconnaître un genou ou une épaule à travers une paroi mentaient, ou débutaient."

"C'est le dernier geste, et c'est le seul moment où une capsule se relève." a enlever : on enchene : "Les préparateurs redressèrent les chariots. Les capsules passèrent de l'horizontale à la verticale en trois crans, très lentement, avec un bruit de crémaillère que tout le monde entendit"

"et quand elle fut debout on aurait dit qu'elle était debout depuis toujours." : ça saute.

"Une fiche lui passa dans la main. Elle tenait en trois lignes : elles étaient sorties le matin même, on n'avait rien eu le temps de suivre.": aucun interet, on a dit plus haut qu'elle etaient déjà sortie tres rapidement. : " un des préparateurs lui donna une fiche et rejoignit son collegue, déjà droit et immobile, les mains croisée devant lui, sur une des bordures de la salle. Andrew la parcouru en diagonale et la rangea dans un carnet. c'était le rapport de la section précédente sur l'heure de la cueillie. La serre mettait un point d'honneur à y ajouter le compte rendu de l'etat de la capsule avant cérémonie." je sais pas si c'est pas un peu too much.

On va déjà s'arreter la pour les retakes on voit la suite après

---

### [233] 2026-08-17 à 21:17

"Il avait dix ans, ou à peu près. On chuchota douze le long du mur, et treize plus loin, et Andrew, qui n'aurait rien dit même si on lui avait demandé, pensa dix." : "On chuchota "douze" et le long du mur, et "treize" plus loin. on fait sauter le reste du paragraphe.

 "Un voile de gelée le recouvrait entièrement, orange, épais, mat, sans une goutte nulle part. Ça ne coulait pas, cette chose-là. Ça s'enlevait. Andrew posa la main à plat sur l'épaule et fit descendre la paume : le voile vint d'un seul tenant, roulé sur lui-même comme une peau de fruit, et découvrit le bras et la main, qui étaient parfaitement propres et parfaitement secs. Il le déposa dans la bassine. Il recommença sur l'autre épaule. Le corps était placé comme on se place pour dormir quand on n'a mal nulle part. Le veilleur l'évalua et comme un exercice exécuté depuis des années, il trancha pour tous :
- Capsule éclaircie avec succès, nouvel arrivant réactif, l'archiviste lui a offert un corps de 10 (offert c'est peut etre pas tres beau... autre phrase à trouver).
Il fit pivoter le miroir sur son pied et le régla en biais, à la bonne hauteur, un peu de trois quarts."


"Il resta là-dessus un long moment. Sa respiration changea de rythme deux fois.
Puis il regarda les différents visages qui s'attardaient sur le siens. Il interrogea le plafond du regard pour comprendre d'ou venait la lumiere et termina sa course sur l'autre capsule à deux mètres de la sienne."

"pour plus tard, parce que l'âge se relève à l'instrument et pas à l'œil." aie aie aie j'ai tout pété dans ce que tu as dis juste avant. il pourrait tres bien évaluer des à presente en sortantun appareil ?

"Il répondit tout de suite," "le jeune arrivant  répondit sans réfléchir une seconde,"

"Andrew l'écrivit. Il écrivit le numéro à la suite, sans y penser, et souligna les deux." : quel numéro ? lage ? le jour ? l'heure ? c'est son matricule, autant l'inscrire des à présent.

"Derriere lui, Nora avait déjà fait glisser le capot en entier. Elle passa autour du corps, décolla ce qui restait de gelée aux plis du coude et du genou, en préleva de quoi remplir deux flacons, les boucha, les rangea dans la bassine." : Nora pris son relais et termina de faire glisser le capot en entier. La veilleuse passa autour du corps d'Eliott, décolla ce qui restait de gelee, aux plis des coude et des genoux. Elle preleva de quoi remplir deux flacons, les boucha, les rangea dans la bassine.

"De la meme manière, Andrew prit le second capot à deux mains et le fit descendre d'un quart." : on enchaine : e corps là mis plus longtemps à revenir. Une quarantaine d'années, et pour une fois personne ne se trompa de beaucoup. Il ouvrit les yeux, les referma, les rouvrit, et regarda le plafond très haut sans rien y chercher. Eliott observait la scène tandis que Nora s'affairait autour de lui. Il regardait ce qu'on faisait à l'autre. Les mains sur l'épaule, le voile qui vient d'un tenant, le miroir qu'on tourne. Il regardait comme on regarde quelqu'un subir la chose qu'on vient soi-même de subir, avec cet intérêt un peu bête qu'on y met.

Nora tendit les mains. Le garçon les prit et sortit tout seul, les jambes hésitantes, et elle le tint le temps qu'il faut. Elle lui passa la serviette par la tête, rabattit les pans sur le devant.
le garçon brisa les mumure en une phrase : 
— Il est pas remonté.
Le long du mur, le murmure s'arrêta.
— Il faut aller le chercher. Il est pas remonté.
Quelqu'un demanda tout bas s'il y en avait une troisième. Un préparateur fit non de la tête, depuis la porte.
— Il faut y aller.
Andrew ne se retourna pas. Il avait les deux mains occupé à prélevé la gelé sur le corps de l'homme.

— Ça arrive, dit Nora, pour la salle. Ça arrive souvent.

Elle avait dit ça avec beaucoup de douceur, et c'était vrai. les arrivant sortaient avec la langue et rien d'autre, et la langue tournait à vide un moment avant de se poser sur quelque chose. Il n'y avait rien à comprendre ; juste à attendre. La veilleuse l'installa à table. Il rouvrit la bouche, la referma. Il redit une fois « il faut y aller », plus bas, pour lui, et ce fut tout.

Le miroir pivota, L'homme se vit dedans. Il regarda longtemps, lui aussi. 
— Nicolas.
La voix sortit grave et éraillée, et elle le surprit lui aussi.
Andrew s'éloigna, pour venir se placer à coté du pichet. Son rôle avait pris fin.
sa collègue fini tout ce qu'il y avait à faire et l'aida à sortir de sa capsule pour le diriger vers la table , à la place voisine. Il posa les mains à plat devant lui parce qu'il ne savait pas quoi en faire.

Puis il tourna la tête.
Eliott le regardait déjà.
Il s'observèrent l'un et l'autre sans qu'aucune émotion ne sembla les traverser. Ça dura le temps que ça dura, et Eliott tira sur sa serviette parce qu'elle glissait de l'épaule. 
À ce moment-là, Andrew refermait la bassine."

"Il prit le pichet et fit le tour de la table. Il posa un verre devant chacun et les remplit. Il remit le reste à l'office sans y penser. Ils burent tous les deux." : Andrew prit le pichet et fit le tour de la table. il versa de l'eau dans chacun des verres et les recentra en face de chaque arrivant. il recupéra le reste et le replaca sur la desert machinalement. (ça fera peut etre répétition avec quelque paragraphe plus haut...)

"Et il y a toujours ce moment, à chaque cérémonie, où les épaules descendent et où la mâchoire se desserre." bof la phrase.

"Trois brins liés par un fil" trois brin de quoi ?  des constructions en osiers ?
"Une femme posa la sienne, se ravisa, la déplaça de dix centimètres, et rit toute seule de l'avoir fait" je comprends l'air que tu veux donner mais la phrase fonctionne pa snon plus, elle a aucun sens.

"Puis ils sortirent" puis les visiteurs.

"il n'y avait plus dans la salle six que deux miroirs," on va parler de la salle "Rosace"
 c'est joli de nommer les salle plutot que de donner des numéros. faudra le modifier tout au debut.

"Andrew reporta les deux arrivants en une ligne."

---

### [234] 2026-08-17 à 21:26

je comprends pas, tu garder ou pas ? "« Sa voix ne tremblait pas. C'est ça qui n'allait pas »"

---

### [235] 2026-08-17 à 21:26

ok. tu me refais tout le prologue que je le relise ? et aussi selon toi, ça va ? Eliott n'est pas trop suspicieux ?

---

### [236] 2026-08-17 à 21:40

bon alors c'est trop subtile parce que la case d'observation, je n'avais pas compris. peut etre rajouterun truc du style. "Sous la ligne, il y avait une case pour les observations. Son regard balaya celle du garçon. Il la regarda un moment, la pointe de sa plume effleurant le papier avant de s'en relever puis il rangea le carnet.

Il éteignit les deux lampes et sortit."

donc si on remet le regard plus insistant ? mais faudrait vraiment mettre l'accent sur le fait qu'on a l'impression qu'il est bien plus curieux de ce qui se passe avec l'autre capsule alors qu'en fait c'est vraiment le visage de l'homme qui l'interpelle.  il pourrait mimer un peu comme un singe, l'homme touche sa bouche, touche son nez, il fait pareil. comme s'il était juste entrain de la copier alors qu'il imite son pere sans le savoir. on peut voir ça comme un signe de curiosité.

oui il faut le remonter c'est un peu trop spotted. peut etre un autre genre de phrase mais qui fasse tout aussi bizarre. et faut que ça inquiete les visiteurs. meme nora doit sembler un peu destabiliser meme si elle essaye de rassurer les autres. oui ça arrive qu'il parle, mais il peut vraiment dire un truc super bizarre

---

### [237] 2026-08-17 à 21:49

"— Ça arrive, dit Nora.

Elle l'avait dit pour la salle, et elle l'avait dit un peu vite. Elle recommença, plus lentement, avec la voix qu'on prend quand on veut être crue.

— Ça arrive souvent." ahah un peu pas tres professionnel non ? elle peut le dire mais il peut y avoir juste une once d'hesitation, balayée instantannément. 

j'aime pas "il est pas remonté, il faut le remonter" je veux pas qu'on puisse faire un lien quelquonque avec le jour de l'accident ! c'est dommage, je trouve que ça gache l'épilogue qui nous apprend ce qui s'est passé. 

par contre, parler d'un truc qu'il est pas censé connaitre, ça c'est chouette "mes poches...il faut vider mes poches" ça n'a aucun sens. 
"je reviens bientot"

---

### [238] 2026-08-17 à 21:54

"...juste à attendre.
"- non non, tu ne comprends pas, c'est un peu tard !"
La veilleuse eu un leger mouvement de tete, et esquissa un sourire rassurant. ELLE rajusta sa serviette qui n'en avait pas besoin et l'installa à table

"« faut les vider »" "fallait les vider..."

---

### [239] 2026-08-17 à 21:55

est-ce que ça fait pas un peu bcp pour un prologue ?

---

### [240] 2026-08-17 à 21:58

ok, fallait les vider peut sauter dans ce cas. tu me rebalances le prologue en entier ?

---

### [241] 2026-08-17 à 22:50

rosace c'est moche en fait ahah, la salle... un chiffre finalement ira bien, ecrit en chiffre : la sale 4

"Le long du mur du fond, la coulée courait" il est dur phonétiquement parlant ce morceau.. et est-ce qu'on peut vraiment parler de coulée quand on parle d'une plante qui se prolonge comme ce qui peut etre le cas pour des citrouilles ou du lierre ?

"Andrew posa ses affaires sur la desserte et compta.

Deux." est-ce que c'est pas un peu con de compter jusqu'à 2 ? ^^" peut etre compter autre chose pour qu'on plante déjà le personnage comme quelqu'un qui compte les choses malgre lui parce que c'est son travail et que c'est une habitude ? là, compter jusqu'à deux... x)

Il poussa la porte de l'épaule : le veilleur poussa la porte. 

"ll déplia la lampe sur pied à hauteur d'épaule, orientée vers le sol et fit rouler un premier miroir depuis le mur jusqu'à l'emplacement du poste. Il stoppa sa course en activant le frein. Il l'essuya avec le linge accroché à la barre, en commençant par le haut, recula d'un pas, se vit dedans, et le tourna vers le mur. Une bassine à droite, vide, avec les flacons dedans."

Nora entra la dernière, en nouant ses manches.
— Bonjour Andrew, On est deux ? (premiere fois que son prenom apparait)

— On est deux.

"un de chaque de part et d'autre de la carafe." c'est pas tres beau ni tres français

"Alors on posait les trois, et on prenait celui qu'il fallait le moment venu, et on remettait les deux autres sur la desserte sans y penser." : "Alors on posait les trois, on prenait celui qu'il fallait le moment venu et on remettait les deux autres sur la desserte sans y penser."

"On ne les voyait qu'à ce moment-là, deux fois par cérémonie, et ils avaient toujours l'air de sortir d'ailleurs." pas necessaire.

"Elles étaient couchées, " les chanceuses du jour" ou autre chose, c'est peut etre pas le bon adjectif, mais c'est pour dire que les capsules sont belles et que l'éclaircie c'est un evenement attendu. d'ailleurs on en parle quelque part du terme eclaircie ?

"presque de la corne" c'est bizarre

"ce dernier, la serre mettait un point d'honneur à le joindre." phrase moche autant pas la mettre

"Andrew prit le capot de la première capsule à deux mains et le fit glisser vers le bas d'un quart. " il prit le capot

"Le veilleur sortit l'instrument et fit le relevé : sortit un instrument, étrange pour celui qui ignore à quoi il sert, mais banal pour qui sait le manier correctement. Il fit le relevé. Puis...

"C'est le signe. On ne parle pas avant." : c'était le signe; on ne parlait jamais avant.

"Elle lui passa la serviette par la tête," estce que c'est suffisant pour comprendre de quelque genre de serviete il d'agit tu penses ? tu sais une serviette un peu comme un ponchon sauf que ça n'a pas une retombée arrondi. le fait de rabattre les pans ça donne cette indication. on peu peut etre venir la fixer avec une ceinture .. je sais pas

"uste à attendre." tu rajoute juste à la suite : "ce n'etait pas systématique."

"quarante ans" : "quarante deux ans," j'aime pas les chiffres ronds :p

"l'aida à sortir de sa capsule" : aida le quadragénaire 


le passage du mime est juste comme il faut parfaite

"Ils burent tous les deux. C'était la première chose qu'ils faisaient. Il n'y en avait pas eu d'autre avant celle-là. L'homme reposa son verre, regarda le fond, et le reprit." : "Ils burent tous les deux. après le choix du nom, le pichet était devenu coutume, le "nettoyage interieur que les veilleurs ne pouvaient pas avant (c'est trèèès moche dit comme ça, mais c'est pour dire que c'est une croyance. on purifie l'interieur. voit ça comme soit un bapteme, soit un test de debut de vie, comme à la maternité quand on essaye de faire marcher un bebe pour voir ses reflexe bipede). en fait je veux faire sauter cette phrase là pour la remplacer "C'était la première chose qu'ils faisaient. Il n'y en avait pas eu d'autre avant celle-là."

"de la taille d'un poing." ça degage 

"Une femme posa la sienne, la regarda, et la tourna d'un quart pour qu'elle soit dans le bon sens. Il n'y avait pas de bon sens." on comprend pas comme le reste que ce sont des petits attention destinés à porter chance...

"Nora emmena les deux vers la porte du fond, où le service suivant attendait" : Nora fit signe à Eliott et Nicolas de les suivre. Ils se levèrent et lui emboitèrent le pas, vers une porte au fond de la pièce à laquelle nui l'un ni l'autre n'avait fait attention jusqu'ici. "

"Le garçon se retourna une fois avant de sortir, mais pas vers la table."" : l'utilité ?

"Un moment plus tard, il n'y avait plus dans la Rosace que deux miroirs, deux lampes, une table avec des cadeaux dessus, et un homme debout avec un carnet." : enleve le mot rosace

---

### [242] 2026-08-17 à 22:55

oui, presque comme de la cire ça me va.

et on pourrait pas trouver un truc entre ligne et coulée ? je trouve ligne un peu trop plat.. on dit quoi en general pour les legumes ou les plantes grimpantes ?

---

### [243] 2026-08-17 à 23:08

nan on va reseter sur coulant et coulée ça va

---

### [244] 2026-08-17 à 23:36

"entré par une bouche" un autre mot que bouche ?
"dix-sept," c'est beaucoup pour es capsule pas prevue. des ceremonie prevu, j'imaginais une vingtaine de personne, on peut donc passer à "une douzaine"
"un murmure passa le long du mur." : un murmure parcourut le petit groupe : murmure et mur, sonnent mal ensemble.



"Andrew prit le second capot à deux mains et le fit descendre d'un quart." est-ce qu'on comprendre que le capot est mou ? que andrew ne devoile contretement que la tete et le buste par choix ? 


"Il avait les deux mains occupées à prélever la gelée sur le corps de l'homme." une petite remarque, si Andrew fait des des prelevements, nora n'a pas besoin de les faire derrière. ça reste des prelevements. elle elle ne fait que finir de nettoyer avant d'habiller

"La veilleuse eut un léger mouvement de tête, et esquissa un sourire rassurant." : " la veilleuse eut un leger mouvement de tete étonnée, sauvé par un sourire rassurant

"pour laver le dedans, la seule part du corps qu'un veilleur ne pouvait pas nettoyer." faut trouver une autre maniere de le dire.. laver dedans... un arrivant qui avale... je veux pas se verbe ici ^^'''''

---

### [245] 2026-08-17 à 23:39

Ça règle les deux questions d'un coup : le capot est rigide — il coulisse dans des rainures. il peut pas etre rigide, la capsule a des asymétries, elle organique. peut etre que le capot n'est pas une bonne appelation car donne l'impression d'une truc dur. faudra qu'il soit mou quand qu'il le laisser pendouiller ou qu'il le plié comme quelque chose de souple mais pas cassant

---

### [246] 2026-08-17 à 23:44

donc pour le rabat, il donne quoi l'extrait ?

---

### [247] 2026-08-17 à 23:45

ok, chapitre mis à jour ?

---

### [248] 2026-08-17 à 23:47

tu peux creer un pdf stp ?

---

### [249] 2026-08-17 à 23:49

quand j'ouvre le pdf

---

### [250] 2026-08-17 à 23:53

ok fais la synchro markdown et on s'arrete la pour aujourd'hui. bonne nuit

---

### [251] 2026-08-18 à 00:41

dernier petit travail : on a oublié un détail sérieux, personne ne s'étonne de son jeune age annoncé par le veilleur. il faudrait que ça tienne en une ligne, mais faut que l'age surprenne l'assemblée. 

un autre point, le public n'est pas vraiment décrit, on c'st juste que ce sont des gens qui sont là dans une piece. y a pas une petite estrade ou des chaises ou peu ? ont ils forcement lememe age ? il y a peut etre des" jeunes" dans l'assemblé qui s'étonne d'un arrivant jeune, c'est pas commun, eux meme sont arrivé qu'il était grand.

en faisant lire à d'autres personnes, il manque un hook, quelque chose qui donnerait envie de lire la suite ou meme de continur après les premier phrase. c'est vrai que c'est pas necessaire à tous les chapitre, puis le decoupage nous aidera à poser des clif hanger, mais pour le prologue, peut etre essayer de glisser un truc au debut, je sais pas. la fin me plait bien, jpeut etre tester quand meme une phrase d'accroche mais j'ai peur qu'elle fasse too much

---

### [252] 2026-08-18 à 00:52

"qui allait en sortir." pose le sous entendu "un humain" je suis ok avec toi pour le reste 

tu peux me redire le passage de l'annonce : — Capsule éclaircie, arrivant réactif. L'Archiviste lui a compté dix ans. ?

---

### [253] 2026-08-18 à 00:57

nan on laisse ça, ça va .


— Dix, répéta celui d'une vingtaine d'années. J'en ai jamais vu d'aussi jeune.
— Dix ans, répéta le visiteur d'une vingtaine d'années. C'est si rare ! 

on pourrait pas faire un peu une assemblé dejà semie partagé ? comme si y en a un qui soupirait dans le lot

---

### [254] 2026-08-18 à 01:05

du coup comme derniere retake, la phrase suivant on designe soit andrew soit le veilleur et pas il

---

### [255] 2026-08-18 à 11:34

hello ! on entame direct aujourd'hui ! on part sur la description de notre cher Andrew : 

 Il était grand sans être particulièrement imposant, avec une silhouette solide et équilibrée. Des épaules suffisamment larges, une taille droite, des bras fermes : le physique d'un homme qui entretenait sa condition sans chercher à paraître plus fort qu'il ne l'était. 

Ses cheveux étaient bruns, courts et légèrement désordonnés, quelques mèches refusant obstinément de rester en place. Une barbe courte encadrait sa mâchoire carrée et accentuait la netteté de ses traits. Son visage avait quelque chose de naturellement sympathique malgré des lignes assez franches : un nez droit, des sourcils épais, une bouche expressive.

Ses yeux, d'un brun profond, contrastaient avec cette impression. Ils étaient attentifs, toujours en train d'observer ce qui l'entourait. Son regard pouvait facilement paraître chaleureux lorsqu'il se détendait, mais il suffisait qu'il se concentre pour que son expression devienne nettement plus sérieuse.


Il n'avait rien d'un homme intimidant au premier regard. Sa carrure était normale, son visage presque avenant. Pourtant, dans sa façon de se tenir, de regarder les gens et de mesurer silencieusement ce qui se passait autour de lui, il y avait quelque chose qui suggérait qu'il valait mieux ne pas le sous-estimer.

manque des lignes pour son age, sa tenue; sa manie de tout compter tout le temps.


petit bonus dans un coin pour Join : "Quelques cicatrices discrètes se devinaient sur ses mains et près de son sourcil, sans qu'il semble leur accorder la moindre importance. Elles faisaient simplement partie de lui."

---

### [256] 2026-08-18 à 16:03

"Cinquante-deux ans, et dix ans de service. Dans ce métier, les deux chiffres se lisent ensemble : les plus anciens sont ceux qui ont l'air les plus jeunes, et Andrew avait encore la tête de quelqu'un qu'on venait d'accueillir. Ses cheveux avaient été gris à son arrivée. Ils ne l'étaient plus." je suis pas d'accord pour que la regle du monde soit expliqué dans sa description. et elle est trop frontal. on la reprendra plus tard avec la description du lieu ou.... de la visite du veilleur qui est jeune au lieu d'etre vieux, je ne sais pas encore

je suis pas convaincu des cheveux qui était blanc et ne le sont plus du tout.. il pourrait encore contenir quelques meches blanches

"Elle est claire parce qu'il faut voir ce qu'on a dessus." ?? 

"Les chaises empilées contre un mur. Les gens le long d'une allée. " je veux pas des exemples de passage de l'histoire" en fait globalement il est trop developpé ce passage, il faudrait le faire passer dans la description de son vetement, il pourrait compter les boutons ou autre chose, sans les compter. on decrit mais on imagine que c'est lui qui les compte.

"Sa carrure était normale," repetition, on l'a dit quelque paragraphe plus haut, c'est pas necessaire d'y revenir

---

### [257] 2026-08-18 à 16:19

"On en changeait dès qu'elle était marquée. Il en avait quatre, identiques, et il ne se rappelait pas avoir choisi la première." de trop

"Une seule chose que je te signale sans y toucher : la description n'a plus aucun signal explicite de la manie." oui je suis d'accord, faut retravailler la façon dont c'est ecrit, des saut de ligne, etc.

"Il portait la tenue, comme tout le monde : une blouse de toile écrue, croisée sur le devant.  Six boutons sur le côté droit. L'écusson brodé sur l'épaule opposée. il avait pris l'habitude de compter chacun des boutons un à un tout comme il mettait un point d'honneur à passer la petit clic de la ceinture au 7 eme trou en partant de l'extrémité. pas six, pas huit. sept. Sa blouse finissait en deux poches basses, indispensable pour y ranger ses effets professionnels. 

La seule chose à lui, dans tout ça, c'étaient ses chaussures — usées comme celles d'un homme qui traverse sa ville à pied tous les jours.  Quatre cent trente huit. c'était le nombre de pas qui séparait la ruche de son logement.

v'est peut etre trop rapprocher et too much mais bon...

---

### [258] 2026-08-18 à 16:21

je trouve pas mal l'écusson on appartient à la ruche, ça pourrait etre un peu considéré comme le caducé

---

### [259] 2026-08-18 à 16:39

je me demande comment enchainer apres le prologue sur la suite... est-ce que c'est une si bonne idée que ça d'aller voir dirrectement June et Eliott ? ça introduit le metier de berceur, sa cree un lieu, un quartier, la description d'eloott, son futur metier ou alors son apprentissage à l'école, sur les banc d'un lieu ou les arrivant de tout age ecoute un arrivant leur faire la lecon. le lecteur est directement dans le systeme du monde alors qu'on n'a meme pas encore décrit Andrew. Andrew, je comptais utiliser sa description pour la journée type, on le suit, on le decrit quand il arrive à la ruche, quand il parcout les lieux. qui s'aprrete à parti partir pour une ceremonie quand soudain, en chemin, il voit des veilleurs s'occuper d'une capsule pourrie. alors la description bien degeu bien purulente et hop, fin du chapitre.

que vaut -il mieux faire en premier ? la visite Eliott/June ou la journee type ?

---

### [260] 2026-08-18 à 17:06

oui, tu as finis de me convaincre. oui on commence par la journée type. En effet son objectif premier est la salle de cérémonie. Soit on le suit depuis chez lui, le matin, et on a une petit elude pour le temps du trajet, soit On peut commencer à le suivre quand il entre dans la ruche. Quand il entre, c'est un batiment tout ce qu'il y a de plus normal. en fait, ça fait comme l'impression qu'on est dans une sorte de clinique avec en arrivant une zone administrative puis des longs couloirs qui amène au service que l'on souhaute. dans la zone, il a juste recupéré un papier avec le numero de la salle du jour. ensuite il progresse dans un grand couloir, qui va amener au coeur du complexte. ce couloir fait penser vraiment à un couloir ce qu'il y a de plus classique, avec des neons au plafond. puis, au fur et a mesure, c'est la lumiere du jour qui prend le relais, de la vegetation et les premiers ornements à la Pataya. on rentre pas dans un autre monde, mais un peu quand meme, il y a une cassure. en fait son trajet va le faire evoluer vers une zone adjacente à cette où il est, en le faisant forcement passer au milieu. il arrive donc dans la partie du complexe ou le plafond et le plus haut (imagine par exemple l'interieur de la sagrada familia à barcelone). on a le mur de pierre visible de la salle centrale, les archives. on n'y entrera pas ici. on a ensuite la coulée tout autout. Andrew se situe donc dans la serre. On peut alors décrire comme c'est, voir des cueilleurs en action. on peut avoir un transporteur qui vient chercher Andrew, pour un soucis quelconque, il va alors traverser le quartier des préparateurs et peut etre celui des analysts. il repasse par la sere direction l'aile des ceremonie. en repassant dans la serre, la capsule non eclaircie. je t"ai fait un plan de la zone. je peux te le montrer ? ah et pour la serre, j'imagine bien des analysts qui checks des capsules sur l'avanceement de la maturation


on quitte une zone administratif, rapide, il a juste récupérer l'info sur la salle à preparer. il arpente les couloirs . on peut avoir une description. au fut e

---

### [261] 2026-08-18 à 17:10

non les analysts ont des donnée theorique. il jugent efectivement  à la couleur la maturation, note les changement, à combien d'intervalle et peut alors prédire plus ou moins précisément si la capsule va s'eclaircie le jour meme ou dans deux semaines

---

### [262] 2026-08-18 à 17:27

@"C:\Users\giron\.claude\uploads\2004a0b6-5ae4-4806-96a2-cf4ff6f482d9\7bed9eaa-IMG_7400.jpeg" Alors je te donne le plan et j’essaye de te le décrire si tu comprends pas. Tout en bas tu as l’entrée principale : ça mène sur une pièce avec un accueil et des chaises comme dans une salle d’attente. Ensuite, tu as un long couloir qui mène au cœur du complexe. Tu arrives dans la serre, représenté par tous les zigzagues un peu partout au centre de la serre plus ou moins tu as le registre. Pour rappel, le registre n’est pas forcément une pièce fermée fermé, mais il y a comme une sorte d’enceinte, un mur qui aurait pu être sculpter avec la coulée qui serpente un peu partout. Les hommes ont créé entre la serre et le registre une porte massive, imposante et très ornementé. Àcoller à la serre. Sur la droite tu as plusieurs salles qui sont les différentes salles de cérémonie elles sont de taille différentes, mais ça on le sait qu’une fois qu’on est rentré dedans. Toujours en étant dans la serre, tu as une autre pièce en bas de consultation. C’est ici que les arrivants sont guidés après avoir éclairci. Concernant le grand couloir, il est collé à une salle de repos. Qui sert pour tous les travaillant de la ruche. Cette salle de repos, relis par des couloirs, la zone des analystes ainsi que le quartier des préparateurs. Les deux zones peuvent également être reliés l’une et l’autre par un grand couloir. Le quartier des préparateurs sert à récupérer les capsules cueillis, et plusieurs Poste permettent de travailler sur des capsules. Comme précédemment dit, le rôle des préparateurs et de récupérer les capsules et de les préparer pour la cérémonie. On va oublier le terme de cueilleurs, parce qu’en soi les préparateurs sont les cueilleurs, on va juste garder les préparateurs qui procèdent à la cueillie. Ils sont donc sous les ordres direct des analystes. Si on devait faire une comparaison, les analystes sont des médecins, et les préparateurs sont les infirmiers. L’analyste détermine les capsules qui vont éclaircir et l’indique au préparateur. Le préparateur récupère la capsule la transporte dans le quartier des préparateurs., branche des appareils à la capsule, et attendre que les analystes viennent. C’est un gain de temps pour les analystes, car eux-mêmes jouent sur deux tableaux. Il s’occupe des capsules, mais également des arrivants. Ce sont eux qui vont faire les premières consultations du corps, vérifier que tout va bien que le corps est vierge de toute anomalie. Comme nous l’avons dit précédemment, les préparateurs, prépare les capsules. Une capsules qui éclaircit d’un coup n’a pratiquement pas besoin de travail. Son rabat est tellement fin, qu’il pourrait céder à tout moment. En opposition avec une capsule qui est quasi prête, en général, on attend pas qu’elle arrive au bout du bout, elle est encore assez souple et on choisit expressément de créer des entailles harmonieuses pour faciliter le travail du veilleur par la suite. Concrètement, il prépare l’aspect final de la capsule pour la cérémonie. Il pourrait effectivement regarder le visage en premier., mais par principe il ne le font pas. C’est un rituel que ce soit la découverte de la cérémonie. En parlant des visiteurs, ils ont un accès depuis l’accueil directement sur la droite et peuvent rejoindre n’importe quelle salle de cérémonie. Il passe alors devant un réfectoire, mais aussi des Chambres. Comme dans une clinique. En fait, je ne l’ai pas indiqué, mais quand les arrivants ont fini leurs consultations, il y a un petit accès depuis la salle de consultation qui mène à ce couloir. C’est à partir de là qu’ils sans dispatcher dans des chambres libres. Et resteront 8 jours. Les visiteurs, non seulement peuvent participer aux cérémonies, mais peuvent également rendre vite aux arrivants. Est-ce que tu comprends mieux mon plan ?^^’

---

### [263] 2026-08-18 à 17:27

[Image: original 4032x3024, displayed at 2000x1500. Multiply coordinates by 2.02 to map to original image.]

---

### [264] 2026-08-18 à 17:41

alors c'est ma faute, tu lis le plan comme il t'as été envoyé, le grand couloir mène à la serre qui permet dans tous les cas de rentrer quasiment partout. la salle de repos et les zonne analystes et preparateurs sont des sorte de batiment, crée -et ornementé comme le reste) par les humains DANS la serre. c'est pour ça qu'on peut apercevoir la coulée se balader un peu partout et pareil il y a des capsules un peu partout aussi. les humains on ensuite crée des couloirs pour avoir des acces moins "nature" entre les quartiers pour par soucis de praticité pour pouvoir déplacer les capsules. Quand une ceremonie commence, Andrew a emprunte la porte entre la serre et la salle tandis que les invités on fait le tour depuis l'accueil. quand la cremonie est terminée, les invités sortent par là ou il sont rentré. libre au veilleur de repasser par la serre ou par la meme porte que les invités. dans tous les cas, la "porte du fond" que les arrivant n'avaient pas vu est la porte qui mene dans la serre. pendant quelque metres, ils peuvent apercevoir la coulee et rentrent directement dans la zone de consultation.

"Mais les deux capsules du prologue sont justement des inopinées. Et le texte dit aujourd'hui :" oui, elles n'ont sans doute pas été coupée, mais il en va quand meme qu'elles ont ete préparés. les preparateurs on connecté les machines de analystes pour les relevé d'avant ceremonie, ils ont nettoyé la capsule etc. oui on garde analyste. au meme titre qu'un gyneco, il observe la maturation de la capsule (gestation dans le vendre de maman) et un suivit des arrivants (post partum fait pour maman)

---

### [265] 2026-08-18 à 17:52

Réessayer

---

### [266] 2026-08-18 à 18:05

a partir du plan que jet t'ai donné de la ruche et des explication donnés, génère moi au format html (interaction animation pour l'explication des différents secteurs) (utilise toutes les lib que tu veux) (fais moi rever je vais manger, t'es en full autonomie)

---

### [267] 2026-08-18 à 19:18

ok, je suis revenue

---

### [268] 2026-08-18 à 19:30

@"C:\Users\giron\.claude\uploads\2004a0b6-5ae4-4806-96a2-cf4ff6f482d9\18825b06-IMG_7403.jpeg" Alors franchement on est pas trop mal sur le plan, sauf que par rapport à mon plan à moi, juste, quand on passe le curseur sur le registre, ça nous indique toujours le couloir des visiteurs, comme si la boxe englober le chemin du tour et la moitié du complexe. Effectivement, tu n’as pas bien compris ce que je voulais dire pour la salle de repos, le grand couloir qui relie l’accueil et le registre a une porte qui quand tu feras la franchis mène sur la salle de repos de tous les agents du complexe. À partir de là, la salle de repos à deux embranchements, l’un mène au quartier des préparateurs et l’autre mène au quartier des analystes. Tu l’as bien indiqué, il y a bien un couloir entre les préparateurs et les analystes.  Pour les Chambre, on pourrait un tout petit peu plus développer, ça pourrait comme dans une maternité être réparti par « lot ». 2,3 chambres, un couloir petit. Puis quatre chambres, puis encore un couloir etc. le tout (voisins) au grand couloir, bien sûr.. 

J’aime beaucoup les trajets que tu as proposé. Pour la capsule, j’aurais bien mis une première phase de départ quelque part dans la serre n’importe où

---

### [269] 2026-08-18 à 19:41

il faudrait peut etre un peu réduire le secteur des préparateurs et des analystes pour que la salle de repos (plus petite elle aussi) soit à gauche du long couloir.

le refectoire pourrait etre ici la croix rouge, et il pourrait y avoir un peu plus de chambre aussi, de l'autre coté. pas forcement alignées non plus (zone avec le bleu).

le tour du registre donne l'impression qu'il est collé au salle, ce qui n'est pas le cas. les trait rouge adjacents indique que c'est encore la serre

---

### [270] 2026-08-18 à 19:55

refectoire on est bon, les chambres sont bizarres.. et si on les mets proportionnelles à la taille des salles, c'est super grand ! tu peux facilement diviser la taille par deux je pense.. Tu peux faire des salles à gauche du couloir, mais pas forcement les fait toutes inclinées dans tous les sens 😮 

mieux pour preparateur et analystes et salle de repos, mais la salle de rpos est trop grande ! elle fait quasiment la taille de la salle de cérémonie la plus grande ! tu peux facilement la diviser par 2 aussi. on dirait aussi qu'elle mange le couloir principal alors qu'elle est censée etre un embranchement. les couloirs qui la joint aux deux autre zones sont super ecrasé et limite inexistante, faut mieux les voir

---

### [271] 2026-08-18 à 19:56

vas-y, tu reprends le plan là ? avec mes modifs ?

---

### [272] 2026-08-18 à 20:05

nan ça va pour les capsules 😉 il est plutot cool ce plan, ça donne une raison à Andrew de se faire intercepté par un reparateur en pasant devant. est-ce qu'on ferait pas un mince chemin qui serpente autre du registre et va vers les salle de cérémonie ? là, le long couloir s'arrete brusquement et pareil, le centre de consultation pourrait y etre rattaché histoire que les arrivant ne soit pas les pieds dans la serre, mais sur un petit chemin  quand meme. (au passage, tu n'as pas de salle 3 ni salle 5.. soit tu en rajoutes, soit tu modifies une taille pour que la salle soit deux fois plus petite

---

### [273] 2026-08-18 à 20:20

ok, c'est presque bon, reduit un peut le quartier des analysts stp. il ne contiennent que des bureau d'étude des capsules, ils ont pas besoin d'etre aussi grand que celui des preaprateur ! tu reduis au moins d'un bon tiers on sera bon

---

### [274] 2026-08-18 à 21:28

la prochaine etape est donc d'écrire la journée à la ruche. Andrew franchi l'entrée, prends sont papiers à l'accueil, un peu comme le ferait un medecin. il attend pas au guichet (qui sert à accueillir les visiteurs et les faire patienter) il franchi la barière de confidentialité et le prend de lui meme. un petit bonjour à la "secretaire" et il file dans le long couloir. transition de decors. peut etre pas des neons, en tout cas une lumiere artificielle au plafond qui se remplace peut à peu par les rayons du soleil. je rappelle, on n'est pas en exterieur, le complexe est comme une immense hangar les batiments ont été construit sur l'emplacement de la serre elle meme. la hauteur plafond est immense (exemple la sagrada familia), la lumiere est traversante. melange d'architecture sculpté et naturel avec la coulée qui s'insinue partout (au passage, on a perdu l'animation de la coulé dans le plan de la ruche 😞 ). Andrew se fait intercepter par un preparateur pour une raison amenant à la description du fonctionnement de la ruche au travers du preparateur ou d'un ananlyst. andrew peut le suivre pour qu'on puisse décrire la sorte d'open space des preparateurs. celle des analystes n'est pas forcement necessaire car juste des appareils, mais une discussion à trois pour apprendre au lecteur qui fait quoi est sympa. suite à cette conversation, andrew part pour la ceremonie e ayant choppé les elements de rituel au passage (ou alors on raccourci, quelqu'un lui a déjà deposé dans la piece). à ce moment là, une odeur, il surprend un bizutage (dit en 2 ligne pour signifié l'age de celui qui se fait bizuter) puis on enclenche la description de la capsule pourrie. on ne parle pas de corps. on parle du gele revulsante, il faut des images forte visuellement, des grumeaux, un agglomérat de truc visqueux, je sais pas, une bouille comme du "vomi" mais sans dire "vomi" dire qu'un chat qui regurgite à côté c'est du petit lait ahah. et insister sur l'odeur avec la phrase de fin qui sera repris mot pour mot à la fin du livre pour le reveal. et bien sur dans tout ça, il faut arriver à glisser la description d'Andrew

---

### [275] 2026-08-18 à 22:24

alors, tant qu'on n'a pas validé l'écris, ne t'embete pas à mettre à jour le chapitre dans l'atelier à chaque fois. pareil pour le pdf. 

"C'était le nombre de pas qu'il y avait jusqu'ici. Certains matins il en faisait quatre cent trente-neuf, parce qu'une charrette lui coupait la rue et qu'il fallait bien la contourner. Ces matins-là ne comptaient pas." désolée mais ce premier chapitre n'est absolument pas harmonieux. et on est pas dans un temps ancienne, on peut parler de voiture.

"Au-dessus, dans la pierre, on avait taillé une capsule de profil, d'un seul trait. Tant de mains l'avaient touchée en passant qu'elle n'était plus qu'un creux." au dessus, (je comprends des battents) et tu parles qu'elle eest usée. ça n'a pas de sens...

"ceux qui ne savent pas quoi faire de leurs mains" cette expression est trop recurrent, faut la changer. 

"L'accueil était une pièce carrée et basse" : rectangulaire est basse. 

"On le leur expliquerait encore deux fois." pourquoi ca sera rexepliqué ?

"Un guichet, une vitre, des chaises alignées dos au mur, et sur les chaises des gens qui attendaient qu'on vienne les chercher. " : ...mur, d'autre dos à dos, et sur les chaises.

on va rajouter un coté accueillant avec des plantes en pot, monstera, et cadres abstrait au mur virant sur de jolis ton bleu pale  orangé.

"Il longea le comptoir, poussa le portillon " : Tout de suite en rentrant, à sa gauche, l'accueil. Il longea le comptoir, en poussa le portillon

— Bonjour Célie. : — Bonjour Anna.

"Le grand couloir partait de là et n'allait nulle part ailleurs. " : Le veilleur quitta rapidement l'accueil; s'engageant dans un grand couloir. ce dernier était large, linéaire, avec un plafond bas.... "

"Le jour entrait par des ouvertures si loin au-dessus qu'on ne les distinguait pas, tombait en longues colonnes obliques, et posait sur les dalles des plaques claires qu'on pouvait traverser ou contourner. " la phrase est jolie dans son visuel, mais trop longue, difficile à lire.

"eux, avaient été travaillés. Des nervures partaient du sol, montaient droit sur trois hauteurs d'homme, " je suis pas sur qu'on comprenne que c'est de la sculputre type sanctuaire... un petit "on n'a jamais su à quel génération appartenait les sculpture. aussi longtemps qu'on s'en souvienne elles ont toujours fait parti de ce lieu (autrement dit, la ruche n'a pas poussé hier, mais on sait que ce sont les ancetre) ma phrase est pas jolie mais tu comprends l'idée...

Depuis longtemps, plus personne ne pouvait dire au premier coup d'œil quelle feuille avait été sculptée et laquelle avait poussé. : tu vois ici je comprends pas, tu me parles de feuilles.. pour moi tu as la vegeation de basse, la coulee qui circule majoritairement autre du registre puis des coulants un peu partout. or, les batiments construit pas les anciens, ce sont eux qui on était sculpé. il se fondent harmonieusement dans ce décors semi vegetale semi bati car les sculptures sont riche de forme, de symbole, de visage, partout ou on regard on en voit. c'est un trop plein parfait mais qui se marie magnifiquement bien avec la vegeation qu'on laisse courrir et qui meme si elle ne semble pas maitrisée l'est un peu. bah oui, sinon il aurait pas construit n'importe ou. après ils se sont adapté. n'on jamais chercher à couper un morceau du coulant donc si le coulant passait à un endrout, et bien un trou était crée dans le bati pour pas le detruire. mais globalement, meme si la coulee est traversant, on ne trouve les capsules que dans la serre !

"À mi-parcours, une porte sur la droite ouvrait vers la salle de repos, d'où sortait une douce odeur de café et des échanges animés. Il reconnu la voix de Nora. Il ne s'arrêta pas pour autant. Tout au fond, très loin, il y avait la porte du registre, massive et chargée d'ornements, et il n'allait pas là non plus." 

a ce stade là, on a dit qu'il a quitté le couloir et qu'il est dans une immense zone ??


"— Veilleur !

Il ne se retourna pas. Ils étaient trois à marcher derrière lui et deux d'entre eux étaient veilleurs." j'aime pas mdr

je comprends pas la suite. pour moi la il serait déjà sorti à ce moment là, avant de décrire la porte : 

"Le couloir débouchait dans la serre sans prévenir. Le sol changeait, la lumière changeait, l'air devenait plus lourd de deux ou trois degrés, et la coulée prenait tout le volume : sur les murs, entre les colonnes, en travers du vide, du sol jusqu'à des hauteurs où personne n'était jamais monté vérifier. 
Immanquable, au loin, la porte du registre, massive et chargée d'ornements tronait entourés de murs de pierre de chaque coté. la coulée se sepentant dessus par endroit.  il n'allait pas là non plus." on perd du sens de la phrase je suis d'accord mais bon... il se fait interpellé après. 
Les quartiers étaient là-dedans. On les avait bâtis à l'intérieur, avec des murs, un toit et une porte, et on les avait ornés comme le reste, parce qu'ici on ornait tout et que personne ne savait plus si c'était par goût ou par habitude. La coulée passait entre eux. Elle passait aussi dessus."

-veilleur ! meme si interpeller par la fonction... je sais pas, je suis pas fan...

pour moi on enchaine : "— Alors viens voir la dix-neuf." "le quartier des préparateurs"



"— Justement. Le jour où ça s'ouvre le neuf et que c'est écrit le neuf, on verra bien.

— On ne parie pas, dit Vera.

— Personne ne parie. On dit juste qui avait raison." je comprends pas se dialogue...

et de manire globale, meme le debut est difficile a comprendre et surtout on sais pas qui est le preparateur et qui est l'analyste et quel est vraiment leur sujet de discorde... 

"— Salle 2.

— Deux ?

— Deux.

— Bonne journée, alors." la fin du dialogue est abrupte.. il a servit à quoi alors au final dans la discussion Andrew ? puis tu est entrain de faire d elui quelqu'un qui est pas tres loquace, c'est dommage. ça le rnd antipathique. il est observateur, il a son tic de compter tout tout le temps mais il doit nous paraitre quand meme  aprécié. le lecteur doit s'attacher à lui, c'est pas un anti hero. c'est un mec banal mais qui a son petit truc en plus 😉 

j'arrte ma relecture la pour l'instant

---

### [276] 2026-08-18 à 22:29

ah et d'ailleurs, les mots ne ressortent pas, analyst, la cueillie, la serre, le fait que les capsule soit un peu partout.. il faut arriver à comprendre quitte à l'expliquer dans une description " andrew le savait, l'analiste avait raison, c'était elle qui connaissait par coeur la maturation d'une capsule, c'était ce qu'elle avait appris, par coeur. reconnaitre observer, predir, comparer avec ses graph" le preparateur il se chargeait d'écouter, d'accepter sa décision, sans contradiction.

et d'ailleurs au passage, Andrew est dans le quartier des preparateurs. on pourrait voir comme une capsule est entrain de se faie préparée, nettoyer, branché à des appareils que l'analyst peut verifier. "elle est pour toi celle-ci non ?" "oui, salle 2" 

enfin se sont des pistes, mais la c'est trop plat ce que tu m'as proposé..

---

### [277] 2026-08-18 à 22:36

"Des figures, des mains, des visages tournés dans tous les sens" on n'a pas ecrit quelque chose de similaire dans le prologue ?

je te laisse mettre à jour le chapitre et je regarde

---

### [278] 2026-08-18 à 23:12

"On avait fait ce qu'on avait pu pour que ce ne soit pas triste. " "elles étaient là pour qu'il y ait quelque chose sur le mur." hhhhhhhheeeee, bien sur que c'est pas triste, c'est de la deco pour rendre l'endroit chaleureux et agreable ! les gens sont pas vexé d'zattendre, ils savent que forcément il y a de l'attente, sa change les idees, mais globalement les gens sont contents d'etre là, ils sont meme un peux excités ! quand une famille vient voir un bébé à la maternité, il est super impatient, il s'en fou de la déco, c'est pas ce qu'il note en premier, mais c'est toujours plus agrable d'évoluer dans un environnement accueillant ! 

"ils sont deux." "ils sont quatre aujourd'hui" ça fait un rappel sinon au prologue qui n'est pas voulu.

"Nora descend " : "Nora arrive" elle descendrait d'ou ?

"— Tu as deux heures, et tu as une tache là." je comprends pas mdr

"On savait seulement que ce sont des gens qui les avaient faits." a faire sauter.


Ce n'était pas de la magie, ce patrimoine n'avait pas emergé de nulle par du jour au lendemain, seulement, on n'avait jamais su de quelle génération l'idée était venue" ou un truc du genre...

"vieillissant, jusqu'au jaune très pâle presque translucide de la fin." hmm... pas un mot banni ça ? moi perso ça me choque pas mais bon... c'est pas ce qu'on a noté en tout cas !


"Personne n'avait jamais choisi l'emplacement d'une seule d'entre elles." : fait une redondance avec  "Il y en avait partout, et jamais deux fois au même endroit. "


"Des passerelles avaient été montées un peu partout pour aller chercher les hautes. Des tubes, des planches et des câbles. C'était laid — c'était la seule chose laide du complexe — et personne n'avait jamais proposé de faire autrement." et tu trouves pas ça dommage à titre personne qu'un lieu aussi beau soit gaché par des tuyaux ? et pourquoi pas dire juste qu'il utilise des échafaud ?

"Les capsules ne poussaient qu'ici, et personne ne savait pourquoi." bah... un peu quang meme, la coulee fait ses bailles à trvaers les murs mais comme il n'y a rien autour et qu'on la coupe pas, elle n'est juste que de passage

"Le troisième cherchait à la main l'endroit où elle tenait encore, et il n'y avait aucun moyen de savoir à l'avance où c'était. " ca degage

"Ça pouvait prendre dix minutes, ça pouvait en prendre deux heures, et l'heure exacte où ça lâchait finissait toujours sur une fiche qu'on remettrait à un veilleur." quand on lit ça fait genre il poireaute en dessous qu'elle se detache toute seule. non, il la coupe parce qu'un analyst à dit qu'il etait temps, point.


"Massive, elle aussi tout autant chargée d'ornements que le reste, encadrée de chaque côté par le mur de pierre qui faisait le tour de la salle, et la coulée serpentant dessus par endroits. Il n'allait pas là non plus."


"Les quartiers étaient là-dedans. On les avait bâtis à l'intérieur, avec des murs, un toit et une porte, et sculptés comme le reste. La coulée passait entre eux. Elle passait aussi dessus." sous entendu qu'il sont dans la salle du registre ! ça va pas : 

"les différents quartiers se fondaient dans l'environnement de la serre."


"Un préparateur répondant au nom de Bastien repéra le veilleur de loin. Il n'y avait pas de mal à le repérer. Andrew était grand...."

"Quelqu'un lui demanda comment allait son épaule. Il répondit qu'elle allait très bien, ce qui était faux, et on lui répondit qu'il mentait mal." c'est quoi cette histoire d'épaule ? s'il y a un sous entendu, je le capte pas...

"femme au chiffon." = vera ??

"Vera arrivait derrière eux. Elle se pencha sur le cadran, le regarda deux secondes, ne dit rien, et continua jusqu'au fond de la pièce, où l'attendait un tabouret trop haut pour sa table et l'ensemble de ses planches.

C'était l'analyste.

Andrew le savait comme tout le monde le savait ici : quand l'analyste tranchait, elle avait raison. " : "Vera arrivait derrière eux. En temps qu''analyste, elle se pencha sur le cadran, ..... " faire sauter "C'était l'analyste."

désolée mais j'ai encore du mal à savoir qui parle quand... et je comprend pas le fon du pb ? le préparateur n'a pas a tenir tete à l'analyste, c'est elle qui a le dernier mot! ou alors ils ne parlent pas de la meme capsule et peut prevenir l'analyste qu'il y a un défaut de compte. c'est donc plus un conflit mais une info...

---

### [279] 2026-08-18 à 23:21

bah c'est ça... j'y voit aucun interet dans l'immediat.... "Andrew promet cinq matins, et le chapitre ne dit pas ce qu'il y trouve. C'est soit une porte à rouvrir plus loin, soit un fil qui pend. Dis-moi." bon je vais refaire une passe. c'est bien à jour dans les chapitres ?

---

### [280] 2026-08-18 à 23:39

"des chaises alignées avec le mur et d'autres dos à dos au milieu"

"— Quatre. Tu es en avance de deux minutes.

— Je suis toujours en avance de deux minutes.

— Je sais. C'est pour ça que je le dis.

Il plia la feuille en deux et la glissa dans la poche basse de sa blouse." c'est une boutade de bureau mais qui n'obtient aucune rection, pourtant c'est amusant ^^'

 j'y pense, mais on n'évoque pas le couloir que va emprunter les invités. peut etre une phrases rapide. Eux il passeront de l'autre coté, traverseront d'abord la zone de résidence puis arriveront devant la bonne salle. La zone de résidence permettait d'accueillir les arrivants pour une durée de 8 jours après la premiere consultation . blabla bla on peut l'expliquer de maniere frontal, rapidement, on y mettra pas les pieds de tout façons. on peut parler d'analyste pour la premiere fois à cette endroit la pour dire qu'il joue sur 2 tableaux. examen medical des corps, le checking d'une corps parfait dans blessure ou anomalie et ensuite le retour à la surveillance des capsules.

"Il dit non merci, on lui en servit un, il le prit." désolée mais il est toujours aussi antipathique mdr, "il accepta de bon coeur" il n'a pas été à la salle de repos pour ne pas en prendre, et bien soit, maintenant il le prend, c'est toujours cool une bonne tasse de café.

bon allez, "vera" devient "Yvan. on a du mal à capter que la preparatrice est pas vera. au moins la ca sera plus fluide

"— Qu'est-ce qu'elle a, la dix-neuf ? la travée dix-neuf?"
— Oui, Elle a douze capsules.
"— Elle en avait onze. Je les ai comptées trois fois." : " ça c'était avant..maintenant il y en a douze. je l'ai ete recompté 3 fois !



"Une série non plus, pas tout de suite. Vera pouvait relever cette capsule dans l'heure, et elle n'aurait qu'un point. Il en fallait trois pour voir un sens et cinq pour poser un jour. Elle le dit comme ça, sans s'excuser, parce que c'était le métier et que le métier était bon.

— Cinq jours, dit-elle. Avant ça, je ne dirai rien.
— Elle est claire, dit Bastien.
— Je sais."

---

### [281] 2026-08-18 à 23:50

quoi que... j'aime bien que ce soit une fille analyste... tu peux changé plutot la preparatrice et en fait un preparateur ? xD on garde vera pour l'analyste ^^' 

"Elle ne discuta pas. Une main posée ne remplaçait pas une série, et une main de Bastien n'avait encore jamais menti.

Seulement, une main ne donne pas de date.
Une série non plus, pas tout de suite. Vera pouvait relever cette capsule dans l'heure, et elle n'aurait qu'un point. Il en fallait trois pour voir un sens et cinq pour poser un jour. Elle le dit comme ça, sans s'excuser, parce que c'était le métier et que le métier était bon.

— Cinq jours, dit-elle. Avant ça, je ne dirai rien.
— Elle est claire, dit Bastien.
— Je sais."

"Une main de préparateur ne valait pas cette d'un analyste. Oui bien sur qu'elle pouvait sembler prête. Mais ce n'est pas si simple que ça. 

Le geste seul main ne pouvait pas donner pas de date. Vera pouvait relever cette capsule dans l'heure, mais elle n'aurait qu'un point dans un graphi immaculé. Il en fallait minimum quatre pour chiffer correctement la date à l'heure pret d'une eclaircie totale poser un jour. Tout les capsule n'arrivait pas à maturation de la meme manière. C'est en se basant sur des chiffres et des moyenne en plus des relevés fait sur place, qu'on le savait. Or Bastien pouvait se tromper comme ne pas se tromper, en tant que preparateur, il ne pouvait pas trancher, et tout le monde le pensit tout bas dans le dire tout haut. Il était nouveau dans le métier. Son ignorance n'était pas mal accueilli. 

— deux jours, dit-elle. Avant ça, je ne dirai rien. de tout manier, si ça avait etait une capsule flash, elle se serait déjà ouvert depuis longtemps..
— mais Elle est claire, dit Bastien.
— Je sais."


"— Ça te fait combien, en plus ?

— Rien du tout, dit-il, ce qui faisait vingt minutes." a faire sauter

---

### [282] 2026-08-18 à 23:57

je rechecke le tout

---

### [283] 2026-08-19 à 00:27

"Il n'y avait pas de mal à le repérer." il faut trouver une autre phrase de transition avec la description, c'est pas beau là.

" en fait, parler de quartier pour dire que c'est une seule grande piece... je suis pas convaincue ^^' j'ai pas d'avis tranché, soit on recoupe en boxe avec une allé commune pour déplacé les capsules, soit on ne parle pas de quartier.

"— Non, dit-il. Regarde-la.

Il la regarda. Elle était belle." une figure de style que tu as tenté mais je ne la comprends pas... pourquoi dire non, si juste avant il confirme qu'elles sont toutes belles ?


"C'est là que les arrivants passaient leurs huit premiers jours, après la 1ere consultation : des chambres, un réfectoire, et des visiteurs pour leur tenir compagnie.

Si on inspectait une premier fois les corps, c'était pour verifier que l'arrivant était bien arrivé immaculé, sans anomalie, sans potentiel blessure. On n'était jamais trop prudent. Certaines capsules n'était pas aussi régulières que prévue. ou alors les relevés étaient étrange, autant vérifier que l'arrivant n'avait pas été impcaté d'une maniere ou d'une autre. c'etait l'analyste qui se chargé de cela. Puisqu'il passait deja ses journée à etudier des capsules, c'était un deroulement logique qu'ils s'occupnt egalement du suivi des arrivants.

 Il examine, il vérifie qu'un corps est entier, sans blessure et sans anomalie. Puis il retourne à ses planches.

... je sais pas trop comment formuler mais l'idée est là.. ça amene plus facilement le role d'analyste pour après.

"Toutes les capsules n'arrivaient pas à maturation de la même manière. C'etait en croisant des moyennes, des chiffres accumulés sur des années et les relevés faits sur place qu'on finissait par le savoir."


"ne tranchait pas"

"Avant de descendre." ? on a deja fait sauter le fait de "descendre" pour nora. on va le remettre.

"Il écrivit : travée dix-neuf, douzième capsule et la date et l'heure qu'il était."

" Puis, en dessous, les sept matins qui suivaient, un par ligne. " ça saute.


pour la capsule : plusieurs choses
" parce que celle-ci était plus courte" aucun interet
"— Au fond ! Va chercher au fond !" "ouais et surtout le fond, on laisse rien, faut que ça brille !"

"C'était aussi le seul à qui on aurait donné soixante ans." faudrait l'expliquer bien plus tot... peut etre en décrivant rapidement une consultation ? je sais pas en fait... 

"La travée n'avait jamais éclairci. " : "On disait d'elle que c'était des capsules non éclaircies, ni plus ni moins, une anomalie de la coulée, on n'avais meme pas le temps de la voir. comme si la coulée rejettais la coque avant meme de lui avoir laissé une chance. 

"elle laisse la peau propre." je veux pas le mot peau, nulle part. On peut parler de membrane pour la suite si tu veux, mais rien qui pourrait inciter à dire qu'il y avait quelque dedans. 

"Un animal malade rend sur le carrelage quelque chose qu'on essuie sans y penser. À côté de ça, c'était du petit-lait. " : 
"mais a cote de ça... les regurgitations de n'importe quel etre vivant, petit ou grand... c'était du petit lait..."

tu peux me redonner une definition claire de "travée" stp ?

"Il passa à trois mètres et continua vers la salle 2, où quatre capsules s'apprêtaient à etre redressée pour dix heures précisément, claires et propres, sur leurs chariots. " 

"n linge tiède qu'on aurait laissé plié." l'image n'est pas assez marquante

---

### [284] 2026-08-19 à 00:39

"Une odeur, insipide, et prenante au nez, comme le fond d'un vase de fleurs qu'on aurait oublié tout un été." l'image est belle, on la garde.

oui, au départ, "Nora descend à dix heures." ça donne l'impression que les salles de ceremonie sont plus basses que le reste du complexe. ça ne me choque pas plus que ça. tu peux me donner le passage ou du explique la regle du monde ? parce qu'en vrai, je pense qu'il va falloir ressusi à l'expliquer clairement d'une maniere ou d'une autre. D'ailleur elle pour se notifier avec le preparateur qui trouve la capsule jolie. une phrase qui choque, le hook du chapitre : le preparateur de 72 ans qui est emerveillé par la beauté de la capsule comme s'il n'en avait jamais vu. et en meme temps ça se comprenait.

---

### [285] 2026-08-19 à 00:44

hmm... je sais pas si c'est sufisant... C'était à peu près le cas : il en était à son quatrième mois. Il avait soixante-douze ans.

"— Capsule éclaircie, arrivant réactif. L'Archiviste lui a compté soixante 76 ans. se souvent Andrew rn observant le jeun préparateur"

Tu crois que c'est trop ?

---

### [286] 2026-08-19 à 00:50

"il ne se souvient plus des cérémonies" je sais pas d'ou ça sort, mais c'est pas le cas... il se souvient que partiellement de sa propre ceremonie car comme tout arrivant, il était dans le coltard. au reveal, il raccroche tous les wagon. lui par contre, en temps que veilleur, il se souvient des ceremonie. il est tres physionomiste et clairement il se souvient du monsieur. Je confirme l'interet que tu m'as posé, mais du coup il y a un pb. il ne peut pas occupé ce poste q'il a 72 et qu'il est arrivé à 72 ans aussi.. il va a l'écolé avant..

---

### [287] 2026-08-19 à 00:57

L'homme au chiffon s'émerveillait devant une capsule comme quelqu'un qui n'en aurait jamais vu. 

— Capsule éclaircie, arrivant réactif. L'Archiviste lui a compté soixante-seize ans. se souvint Andrew en considérant ton sourire béa. 
Personne ne pouvait lui en vouloir, il venait tout juste de quitter les bancs de l'école, et il avait encore des cours du soir. ça faisait à peine 1 mois qu'il était là, un apprenti modèle qui apprenait vite.

---

### [288] 2026-08-19 à 01:01

L'homme au chiffon s'émerveillait devant une capsule comme quelqu'un qui n'en aurait jamais vu.

— Tu n'en as pas vu, à l'école ? dit Andrew. (répétition de "vu")

— Oh si, si. Mais ce n'est pas la même chose que de les voir en vrai !

"Capsule éclaircie, arrivant réactif. L'Archiviste lui a compté soixante-seize ans," se souvint Andrew en considérant son sourire béat.

Personne ne pouvait lui en vouloir. Il avait encore des cours du soir, et ça faisait à peine un mois qu'il était là. Un apprenti modèle, qui apprenait vite.

Dans ce service, les plus anciens du métier étaient aussi ceux qui avaient l'air les plus jeunes. Ça se comprenait très bien.

---

### [289] 2026-08-19 à 01:03

"L'homme au chiffon s'émerveillait devant une capsule comme quelqu'un qui n'en aurait jamais vu. "
et je te valide le reste

---

### [290] 2026-08-19 à 01:05

oui, on la place juste après le prologue

---

### [291] 2026-08-19 à 01:28

Un guichet, une vitre, des chaises alignées avec le mur et d'autres dos à dos au milieu, et sur les chaises des gens qui attendaient qu'on vienne les chercher.

On était bien là-dedans. Trois grandes plantes en pot dans les angles, avec de larges feuilles fendues qui montaient plus haut que les chaises.

on ne vient pas ici pour les toiles

en vrai, tout le paragraphe est bizarre... "On était bien là-dedans. Trois grandes plantes en pot dans les angles, avec de larges feuilles fendues qui montaient plus haut que les chaises. Aux murs, des toiles sans sujet, des aplats de bleu pâle qui viraient à l'orange sur les bords. Personne ne les regardait deux fois, et ce n'était pas grave : on ne vient pas ici pour les toiles. Elles faisaient seulement que l'endroit était agréable, ce qui n'est pas rien pour une salle d'attente."

"Anna, la secrétaire, leur avait expliqué (on a beau etre dans monde 2, si on renomme tous les metiers, on n'en ai pas sortir non plus. il est dejà bien assez complete)

Les neuf -> le 18 (on a dit qu'il y avait plus de monde quand pas capsule flash)

Toutes les capsules n'étaient pas aussi régulières qu'annoncé, et il arrivait qu'une série se termine sur des relevés étranges ; autant s'assurer que celui qui en sortait n'avait pas été touché d'une manière ou d'une autre. C'était l'analyste qui s'en chargeait, des hommes et des femmes experts dans leur domaine.

---

### [292] 2026-08-19 à 01:34

"Elle était restée sombre du premier jour au dernier," ça insinue qu'elle est la depuis longtemps. non, une capsule pourrie, elle pop d'un coup, et deverse toute sa merde d'un coup. je la trouve encore "trop propre pour le début. on la considere trop comme une capsule. on devrait meme pas dire qu'elle y ressemble en fait. ça donne l'impression que quelque chose a maturé de façon eroné, mais a maturé quand meme. c'est ce que je veux pas. ça doit juste pareil découtant. presque on a du mal a croire que c'est une capsule comme si c'était plutot une excroissance de la coulée que la coulée elle meme rejeté pour en pas contaminé le reste. c'est l'impression que sa donnait

---

### [293] 2026-08-19 à 01:43

je te valide momentanément ce chapitre, demain j'y rejetterai un oeil a tete reposée

---

### [294] 2026-08-19 à 01:54

je le relirai demain. et pour la capsule aparente... en fait je vois pas trop quoi en faire.. c'est un fait qui n'apportera rien je pense...

---

### [295] 2026-08-19 à 02:02

1) Actuellement tout ce qu'on a produit tu l'enregistres sur git en taguant release 1.0

2 ) Maintenant l'idée est de nettoyer tous les fichiers dont je t'ai  fait une remarque, tu deletes tous ce qui est obsolete et tu me fais un recap de tout ce que tu as fais. demain je pourrai ainsi te dire si tu as supprimé trop ou pas assez

3) ensuite, pendant que je dors c'est d'analyser le style d'écriture des 3 chapitres validé. analyser les temps, les accords, les descriptions, etc. Je t'ai souvent repris sur des tournures de phrases pas belles, sur des répétitions, sur le fait qu'on ne savait plus de qui on parlait (il elle) des phrases anormalement trop longues...

Et tu me ressorts un template d'écriture. je le lierai, je te ferai des retour et se sera ta base pour les propositions suivante

Full autonomie, fais ça bien, fait des verif, controle bien ce que tu fais. pour le template de mon style d'écriture, c'est mon nouveau document. soit critique avec toi meme, soit critique avec ce que tu produis et si tu as des proposition d'amélioraton pour mon style d'écriture, ecrit le dans le dossier, tu dois etre force de proposition. l'idée et de travailler efficacement avec toi !

4) Je veux aussi un glossaire pour tous les dénomination du monde 2. Mais un glossaire propre, destiné à etre lu rapidement. imagine le à la fin du livre pour un lecteur qui galère avec l'univers. ordre alphabétique, mot en gras, comme dans un dictionnaire. une description court et efficace. tu dois la faire apparaitre dans l'atelier.

5) si tu te souviens bien, je t'avais fait une description de l'interieur du jardin avec les airs de jeu, le mur d'enceinte et les dessin, la cantine, les dortoirs, le centre medical style pediatrique et les salle pour la "fin de vie". les cabanons pour velo et tricyle, gymase, salle de jeu, bcp d'arbre, un air frais, aéré, grand espaces etc. j'aimerais que tu me fasses un plan du jardin. cette fois je te passe pas de visuel, à toi de m'en proposer troi différents. tu te bases sur le plan de la ruche pour que l'architecture reste logique. le detail c'est ce qui fait qu'un monde est realiste. les details et imperfection rendent un monde vivant et cohérent. il n'y a qu'à voir la description de la ruche.. je me perdrai dans un decors pareil.

6) des propals de description :
- a) d'abord la ceremonie d'Andrew vu de son point de vue, avec les jumelles à coté. (rappel : il entend à moitié, il est dans les vapes. et description des visages, "ah ce sont des paires" etc.ouverture des yeux jusqu'à salle de consultation pour montrer à quoi ressemble les tests de "début de vie"), 
b) une description du jardin vues de l'exterieur avec une autre de l'interieur du complexe pédiatrique. (le mot pédriatre, peut etre pas bon dans ce cas là.)
c) la description de la scène de la berceuse et du bébé avec Andrew, Isaac et la medecin en chef qui l'observe. bulle dans le temps. on ne met pas l'accent sur la berceuse mais sur le tout petit qui est bercé. rappel, elle pleure et s'excuse
