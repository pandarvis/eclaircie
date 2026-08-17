/* Contrôle du document avant livraison.
   Vérifie la syntaxe, les trous du tableau, les liens orphelins,
   les collisions de position, et les mots interdits dans les textes. */
const fs = require('fs'), vm = require('vm');

let src = fs.readFileSync('check.js', 'utf8');
const coupe = src.indexOf('const $  = (s, r)');
src = src.slice(0, coupe > 0 ? coupe : src.length);
src += `
;globalThis.__d = { SCENES, LIENS, NOTES, QUESTIONS, TEXTES, VOIES, ACTES,
                    LEXIQUE, REGLES, INTERDITS, GENS, DISPOSITIF, RACCORDS, PHRASES, ETAPES };`;

const ctx = {}; vm.createContext(ctx);
vm.runInContext(src, ctx);
const d = ctx.__d;

const pb = [];
const trous = [];
d.SCENES.forEach((s, i) => { if (s === undefined) trous.push(i); });
if (trous.length) pb.push('trous dans SCENES : ' + trous.join(', '));

const ids = d.SCENES.map(s => s && s.id);
if (new Set(ids).size !== ids.length) pb.push('identifiants en double');

d.LIENS.forEach(([a, b]) => {
  if (!ids.includes(a) || !ids.includes(b)) pb.push('lien orphelin : ' + a + ' -> ' + b);
});

const pos = {};
d.SCENES.forEach(s => {
  const k = s.col + '/' + s.row;
  if (pos[k]) pb.push('collision ' + k + ' : ' + pos[k] + ' et ' + s.titre);
  pos[k] = s.titre;
});

const voies = Object.keys(d.VOIES);
d.SCENES.forEach(s => { if (!voies.includes(s.row)) pb.push('voie inconnue : ' + s.row); });

/* Une liste ecrite en texte ne casse rien au chargement : elle tue l'ecran
   au rendu, et tout ce qui se construit apres. On la cherche donc ici. */
[[`NOTES`, d.NOTES, [`t`]],
 [`SCENES`, d.SCENES, [`qui`,`gardes`,`ouvert`,`pourquoi`,`phrases`,`refs`]],
 [`QUESTIONS`, d.QUESTIONS, [`o`]],
 [`TEXTES`, d.TEXTES, [`p`,`tenu`,`ouvre`]]].forEach(([nom, tab, champs]) => {
  tab.forEach((e, i) => champs.forEach(c => {
    if (e && e[c] !== undefined && !Array.isArray(e[c]))
      pb.push(nom + `[` + i + `].` + c + ` devrait etre une liste, pas ` + JSON.stringify(e[c]).slice(0, 46));
  }));
});

/* les mots que le texte du roman ne peut pas employer */
/* liste arretee par l'autrice le 18 aout 2026 : les mots d'apparence physique passent
   (un gars, un garcon, une femme, une fille, une fillette) ; c'est la categorie sociale
   ou d'age qui est interdite, jamais la matiere. */
const bannis = /\b(enfants?|b[ée]b[ée]s?|nourrissons?|vieux|vieilles?|vieillards?|seniors?|p[èe]res?|m[èe]res?|fils|famille|jumeaux?|jumelles?)\b/i;
d.TEXTES.forEach(t => {
  const brut = t.p.map(x => x[1]).join(' ').replace(/<[^>]+>/g, '');
  const m = brut.match(bannis);
  if (m) pb.push('mot interdit dans « ' + t.rang + ' » : ' + m[0]);
});

const mots = d.TEXTES.map(t => t.p.map(x => x[1].replace(/<[^>]+>/g, '')).join(' ').split(/\s+/).length);

console.log('scènes      ', d.SCENES.filter(s => !s.gris).length,
            '(andrew ' + d.SCENES.filter(s => s.row === 'andrew' && !s.gris).length,
            '· joël ' + d.SCENES.filter(s => s.row === 'joel' && !s.gris).length + ')',
            '+ ' + d.SCENES.filter(s => s.gris).length + ' non écrites');
console.log('étapes      ', d.ETAPES.length);
console.log('liens       ', d.LIENS.length);
console.log('notes       ', d.NOTES.length);
console.log('questions   ', d.QUESTIONS.length);
console.log('lexique     ', d.LEXIQUE.length, '· règles', d.REGLES.length, '· interdits', d.INTERDITS.length);
console.log('gens        ', d.GENS.length, '· phrases', d.PHRASES.length);
console.log('chapitres   ', d.TEXTES.length, '(' + mots.join(', ') + ' mots)');
console.log('à trouver   ', d.SCENES.filter(s => s.statut === 'trou').length, 'scènes');

if (pb.length) { console.log('\nPROBLÈMES :'); pb.forEach(x => console.log('  ✗ ' + x)); process.exit(1); }
console.log('\n✓ tout est cohérent');
