/* Les paragraphes du roman portent, tres rarement, de l'italique ou du gras.
   Tout le reste est du texte, et s'echappe.
   Liste blanche stricte : les balises nues, sans le moindre attribut -- et
   seulement quand elles s'apparient vraiment. Une balise fermante ne passe
   que si la balise ouvrante correspondante, plus tot dans le meme texte, a
   elle-meme ete autorisee : sinon un </em> orphelin pourrait refermer un
   <em> legitime plus loin dans le paragraphe. */

const BALISE = /<[^>]*>/g;
const OUVRANTES = new Set(['<em>', '<strong>']);
const FERMANTES = { '</em>': 'em', '</strong>': 'strong' };

function echapper(morceau) {
  return morceau.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

export function assainir(texte) {
  const s = String(texte);
  const pile = [];
  let resultat = '';
  let position = 0;

  for (const trouvee of s.matchAll(BALISE)) {
    const [balise] = trouvee;
    const debut = trouvee.index;

    /* Le texte avant la balise s'echappe normalement. */
    resultat += echapper(s.slice(position, debut));
    position = debut + balise.length;

    if (OUVRANTES.has(balise)) {
      pile.push(balise.slice(1, -1));
      resultat += balise;
    } else if (FERMANTES[balise] && pile[pile.length - 1] === FERMANTES[balise]) {
      pile.pop();
      resultat += balise;
    } else {
      resultat += echapper(balise);
    }
  }

  resultat += echapper(s.slice(position));
  return resultat;
}
