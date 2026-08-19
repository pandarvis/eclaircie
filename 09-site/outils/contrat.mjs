/* Le contrat de donnees : ce que le site attend de l'atelier.
   Fonctions pures — elles ne lisent aucun fichier, pour se tester seules. */

/* Les trois balises de paragraphe que l'atelier emploie aujourd'hui. */
const BALISES = new Set(['p', 'pause', 'tiret']);

/* Un bloc peut porter une classe facultative en troisieme position.
   L'atelier n'en emploie qu'une : `fin`, qui pose une respiration avant le
   dernier paragraphe. Elle passe par liste blanche comme tout le reste — une
   classe nouvelle arrete la fabrication au lieu d'entrer dans le HTML. */
const CLASSES = new Set(['fin']);

/* Ce qui traverse jusqu'au lecteur, et rien d'autre.
   On liste ce qui passe au lieu d'exclure ce qui ne passe pas : un champ
   ajoute demain par l'autrice ne franchira pas la frontiere tout seul.
   Restent a l'atelier : `scene`, `sous` (qui nomme le point de vue, donc la
   voie), `tenu`, `ouvre` et `note` (ses analyses d'ecriture). */
const POUR_LE_LECTEUR = ['id', 'rang', 'titre', 'p'];

export function pourLeLecteur(TEXTES) {
  return TEXTES.map((t) => {
    const sorti = {};
    for (const champ of POUR_LE_LECTEUR) sorti[champ] = t[champ];
    return sorti;
  });
}

export function verifierLeContrat({ TEXTES, SCENES }) {
  const pb = [];

  if (!Array.isArray(TEXTES)) return ['TEXTES a disparu, ou n\'est plus un tableau'];
  if (!Array.isArray(SCENES)) return ['SCENES a disparu, ou n\'est plus un tableau'];

  const scenesConnues = new Set(SCENES.map((s) => s.id));
  const vus = new Set();

  TEXTES.forEach((t, i) => {
    const ou = t.id ? `le texte « ${t.id} »` : `le texte n° ${i + 1}`;

    for (const champ of ['id', 'rang', 'titre', 'scene']) {
      if (typeof t[champ] !== 'string' || t[champ] === '') {
        pb.push(`${ou} : le champ « ${champ} » manque ou n'est plus une chaine`);
      }
    }

    if (typeof t.id === 'string' && t.id !== '') {
      if (vus.has(t.id)) pb.push(`${ou} : cet identifiant est en double`);
      vus.add(t.id);
    }

    if (typeof t.scene === 'string' && t.scene !== '' && !scenesConnues.has(t.scene)) {
      pb.push(`${ou} : la scene « ${t.scene} » n'existe dans aucune entree de SCENES`);
    }

    if (!Array.isArray(t.p) || t.p.length === 0) {
      pb.push(`${ou} : le tableau « p » manque ou est vide`);
      return;
    }

    t.p.forEach((bloc, j) => {
      const ouBloc = `${ou}, bloc n° ${j + 1}`;

      if (!Array.isArray(bloc) || bloc.length < 2 || bloc.length > 3
          || typeof bloc[0] !== 'string' || typeof bloc[1] !== 'string') {
        pb.push(`${ouBloc} : on attend un couple [balise, texte], `
              + `ou un triplet [balise, texte, classe]`);
        return;
      }

      if (!BALISES.has(bloc[0])) {
        pb.push(`${ouBloc} : la balise « ${bloc[0]} » est inconnue du site `
              + `(connues : ${[...BALISES].join(', ')})`);
      }

      if (bloc.length === 3 && !CLASSES.has(bloc[2])) {
        pb.push(`${ouBloc} : la classe « ${bloc[2]} » est inconnue du site `
              + `(connues : ${[...CLASSES].join(', ')})`);
      }
    });
  });

  return pb;
}
