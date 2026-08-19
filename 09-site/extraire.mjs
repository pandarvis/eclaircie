/* La moisson : les sources de l'atelier -> du JSON pour le site.
   Meme procede que `06-visuels/atelier/valide.js` : on evalue les modules de
   donnees dans un bac a sable Node, sans navigateur. On ne touche a rien. */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { createContext, runInContext } from 'node:vm';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { verifierLeContrat, pourLeLecteur } from './outils/contrat.mjs';

const ici = dirname(fileURLToPath(import.meta.url));
const SOURCES = join(ici, '..', '06-visuels', 'atelier', 'sources');

/* Seulement les deux modules dont le site a besoin. Aucun ne touche au DOM. */
const MODULES = ['p5-scenes.js', 'pB-textes.js'];

export function moissonner(dossier = SOURCES) {
  const src = MODULES.map((f) => readFileSync(join(dossier, f), 'utf8')).join('\n')
    .replace(/<\/?script>/g, '')
    + '\n;globalThis.__d = { TEXTES, SCENES };';
  const ctx = {};
  createContext(ctx);
  runInContext(src, ctx);
  return ctx.__d;
}

function principal() {
  const controleSeul = process.argv.includes('--controle-seul');
  const donnees = moissonner();
  const pb = verifierLeContrat(donnees);

  if (pb.length) {
    console.error('\nLe site de lecture ne peut plus lire l\'atelier :\n');
    for (const m of pb) console.error('  · ' + m);
    console.error('\nLa forme des donnees a change. Repare-la, ou previens la session'
                + ' du site — voir 09-site/CLAUDE.md.\n');
    process.exit(1);
  }

  if (controleSeul) {
    console.log('contrat du site : respecte');
    return;
  }

  mkdirSync(join(ici, 'donnees'), { recursive: true });
  writeFileSync(
    join(ici, 'donnees', 'textes.json'),
    JSON.stringify(pourLeLecteur(donnees.TEXTES), null, 2),
    'utf8',
  );
  console.log(`moisson : ${donnees.TEXTES.length} textes`);
}

if (process.argv[1] === fileURLToPath(import.meta.url)) principal();
