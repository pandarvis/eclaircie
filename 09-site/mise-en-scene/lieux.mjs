/* Ou se passe ce qu'on est en train de lire.

   Cette table appartient au site, pas a l'atelier : on ne demande jamais a
   l'autrice d'annoter son texte pour nous. Mais elle est sous contrat comme
   tout le reste — chaque ancre porte les mots qui doivent se trouver dans le
   paragraphe vise. Si elle recrit ce paragraphe, la fabrication s'arrete et
   on vient revoir l'ancre, au lieu d'allumer silencieusement la mauvaise piece.

   REGLE : le plan ne montre que ce que le texte a deja dit. Il n'annonce
   rien, il fait echo. Un lecteur qui vient de lire « la salle 4 » voit la
   salle 4 s'allumer ; il n'apprend rien qu'il ne sache. */

export const LIEUX = [
  { texte: 'prologue', bloc: 1, lieu: 'Salle 4', ancre: 'la salle 4' },

  { texte: 'chapitre-1', bloc: 4, lieu: "L'accueil", ancre: "l'accueil" },
  { texte: 'chapitre-1', bloc: 21, lieu: 'Le grand couloir', ancre: 'le grand couloir' },
  { texte: 'chapitre-1', bloc: 37, lieu: 'La serre', ancre: "C'était la serre" },
  { texte: 'chapitre-1', bloc: 39, lieu: 'Le registre', ancre: 'la porte du registre' },
  { texte: 'chapitre-1', bloc: 132, lieu: 'Salle 2', ancre: 'la salle 2' },
];

export function verifierLesAncres(TEXTES, lieuxDuPlan) {
  const pb = [];
  const parId = new Map(TEXTES.map((t) => [t.id, t]));
  const connus = new Set(lieuxDuPlan.map((l) => l.nom));

  for (const a of LIEUX) {
    const ou = `l'ancre « ${a.ancre} » (${a.texte}, bloc ${a.bloc})`;
    const t = parId.get(a.texte);

    if (!t) { pb.push(`${ou} : le texte « ${a.texte} » n'existe plus`); continue; }
    if (!connus.has(a.lieu)) { pb.push(`${ou} : le plan n'a plus de lieu « ${a.lieu} »`); continue; }

    const bloc = t.p[a.bloc];
    if (!bloc) { pb.push(`${ou} : ce texte n'a plus de bloc n° ${a.bloc}`); continue; }

    const dit = bloc[1].replace(/<[^>]+>/g, '').toLowerCase();
    if (!dit.includes(a.ancre.toLowerCase())) {
      pb.push(`${ou} : ce paragraphe ne dit plus ces mots. Il dit maintenant `
            + `« ${bloc[1].replace(/<[^>]+>/g, '').slice(0, 70)}… »`);
    }
  }

  return pb;
}
