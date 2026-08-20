/* Le seul controle qui compte : on regarde ce que le lecteur recoit.
   Il tourne sur dist/, apres la construction.

   Il est pilote par les donnees, pas par des mots choisis a la main : on
   prend les champs interdits dans les vraies sources et on verifie que leur
   contenu est absent des pages. « Andrew » ne peut pas servir de sonde — le
   prenom est dans le roman (« Bonjour Andrew. On est deux ? »). */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { moissonner } from '../extraire.mjs';

const ici = dirname(fileURLToPath(import.meta.url));
const DIST = join(ici, '..', 'dist');

function toutesLesPages(dossier) {
  const trouvees = [];
  for (const nom of readdirSync(dossier)) {
    const chemin = join(dossier, nom);
    if (statSync(chemin).isDirectory()) trouvees.push(...toutesLesPages(chemin));
    else if (nom.endsWith('.html')) trouvees.push(chemin);
  }
  return trouvees;
}

assert.ok(existsSync(DIST), 'dist/ n\'existe pas : construire le site avant ce controle');

const pages = toutesLesPages(DIST).map((c) => [c, readFileSync(c, 'utf8')]);
const { TEXTES } = moissonner();

/* Les couleurs de voie de l'atelier, dans les deux themes.
   Source : 06-visuels/atelier/sources/p1-style.html */
const COULEURS_DE_VOIE = [
  '#7CC6DC', '#D2A06B', '#94A3B1', '#2C5B6B', '#6A4E2C', '#3A4854',
  '#1B7690', '#8E5D1E', '#5A6C7C', '#B4DCE7', '#EBD6B8', '#CBD5DD',
];

test('la construction a bien produit des pages', () => {
  assert.ok(pages.length >= 4, `attendu au moins 4 pages, trouve ${pages.length}`);
});

test('aucune note de travail de l autrice n atteint le lecteur', () => {
  for (const t of TEXTES) {
    const interdits = [
      t.sous, t.note,
      ...(Array.isArray(t.tenu) ? t.tenu : []),
      ...(Array.isArray(t.ouvre) ? t.ouvre : []),
    ].filter((v) => typeof v === 'string' && v.length > 40);

    for (const morceau of interdits) {
      const sonde = morceau.replace(/<[^>]+>/g, '').slice(0, 40);
      if (sonde.length < 40) continue;
      for (const [chemin, html] of pages) {
        assert.ok(
          !html.includes(sonde),
          `fuite dans ${chemin} : « ${sonde}… » vient d'un champ interdit du texte « ${t.id} »`,
        );
      }
    }
  }
});

test('aucune couleur de voie n atteint le lecteur', () => {
  for (const couleur of COULEURS_DE_VOIE) {
    for (const [chemin, html] of pages) {
      assert.ok(
        !html.toUpperCase().includes(couleur.toUpperCase()),
        `fuite dans ${chemin} : la couleur de voie ${couleur} est presente`,
      );
    }
  }
});

test('aucun vocabulaire de montage n atteint le lecteur', () => {
  /* Les mots par lesquels l'atelier nomme la mecanique du roman. Aucun
     n'appartient a la prose : s'ils apparaissent, ils viennent de nous. */
  const mecanique = ['point de vue d', 'faux raccord', 'voie-andrew', 'voie-joel', 'l-andrew', 'l-joel'];
  for (const mot of mecanique) {
    for (const [chemin, html] of pages) {
      assert.ok(
        !html.toLowerCase().includes(mot),
        `fuite dans ${chemin} : « ${mot} » nomme le montage du roman`,
      );
    }
  }
});

test('aucun objet de donnees brut n est serialise dans une page', () => {
  for (const [chemin, html] of pages) {
    for (const champ of ['"sous":', '"tenu":', '"ouvre":', '"scene":']) {
      assert.ok(
        !html.includes(champ),
        `fuite dans ${chemin} : le champ ${champ} a ete serialise dans la page`,
      );
    }
  }
});
