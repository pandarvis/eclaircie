/* Les paragraphes du roman portent, tres rarement, de l'italique ou du gras.
   Tout le reste est du texte, et s'echappe.
   Liste blanche stricte : les balises nues, sans le moindre attribut -- et
   seulement quand elles s'apparient vraiment. Une balise fermante ne passe
   que si la balise ouvrante correspondante, plus tot dans le meme texte, a
   elle-meme ete autorisee : sinon un </em> orphelin pourrait refermer un
   <em> legitime plus loin dans le paragraphe. Et symetriquement, une balise
   ouvrante qui n'est jamais refermee -- ou dont la fermeture tombe au
   mauvais endroit dans un croisement -- n'a jamais ete vraiment autorisee
   non plus : elle est echappee a la fin, comme si on ne l'avait pas laissee
   passer des le depart. La sortie est donc toujours du HTML equilibre. */

const BALISE = /<[^>]*>/g;
const OUVRANTES = new Set(['<em>', '<strong>']);
const FERMANTES = { '</em>': 'em', '</strong>': 'strong' };

function echapper(morceau) {
  return morceau.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

export function assainir(texte) {
  const s = String(texte);
  const morceaux = [];
  /* La pile retient, pour chaque ouvrante gardee, son nom et l'indice du
     morceau ou elle a ete posee -- pour pouvoir revenir dessus a la fin. */
  const pile = [];
  let position = 0;

  for (const trouvee of s.matchAll(BALISE)) {
    const [balise] = trouvee;
    const debut = trouvee.index;

    /* Le texte avant la balise s'echappe normalement. */
    morceaux.push(echapper(s.slice(position, debut)));
    position = debut + balise.length;

    if (OUVRANTES.has(balise)) {
      morceaux.push(balise);
      pile.push({ nom: balise.slice(1, -1), indice: morceaux.length - 1 });
    } else if (FERMANTES[balise] && pile.length > 0
               && pile[pile.length - 1].nom === FERMANTES[balise]) {
      pile.pop();
      morceaux.push(balise);
    } else {
      morceaux.push(echapper(balise));
    }
  }

  morceaux.push(echapper(s.slice(position)));

  /* Ce qui reste sur la pile n'a jamais trouve sa fermante : ces
     ouvrantes-la ne devaient pas passer, on les echappe apres coup. */
  for (const { indice } of pile) {
    morceaux[indice] = echapper(morceaux[indice]);
  }

  return morceaux.join('');
}
