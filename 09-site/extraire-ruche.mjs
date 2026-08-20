/* La moisson du plan de la ruche.
   Sa page dessine le complexe en JavaScript, a partir de sa geometrie. On ne
   recopie pas ce code : on le rejoue dans un faux DOM et on capture ce qu'il
   fabrique. Le site recoit donc un dessin calcule par SON code a elle — si
   elle deplace une salle, le site suit sans qu'on touche a rien.

   On s'arrete avant la couche interactive de sa page : tout ce qui suit
   `la serre doit rester derriere` se sert du navigateur (getBoundingClientRect,
   getTotalLength, requestAnimationFrame) et ne nous concerne pas. */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { createContext, runInContext } from 'node:vm';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ici = dirname(fileURLToPath(import.meta.url));
const PLAN = join(ici, '..', '06-visuels', 'plan-de-la-ruche.html');
const ARRET = 'la serre doit rester derrière tout le monde';

function faireNoeud(tag) {
  return {
    tag, attrs: {}, enfants: [], texte: '', dataset: {}, style: {},
    setAttribute(k, v) { this.attrs[k] = String(v); },
    getAttribute(k) { return this.attrs[k]; },
    appendChild(e) { this.enfants.push(e); return e; },
    insertBefore(e) { this.enfants.unshift(e); return e; },
    addEventListener() {},
    classList: { add() {}, remove() {}, toggle() {} },
    get firstChild() { return this.enfants[0] ?? null; },
    set textContent(v) { this.texte = String(v); },
    get textContent() { return this.texte; },
  };
}

export function moissonnerLaRuche(fichier = PLAN) {
  const page = readFileSync(fichier, 'utf8');

  const vue = (page.match(/viewBox="([^"]*)"/) || [])[1];
  if (!vue) throw new Error('le plan de la ruche n\'a plus de viewBox');

  const style = (page.match(/<style>([\s\S]*?)<\/style>/) || [])[1] || '';

  const script = (page.match(/<script>([\s\S]*?)<\/script>/) || [])[1];
  if (!script) throw new Error('le plan de la ruche n\'a plus de script');

  const coupe = script.indexOf(ARRET);
  if (coupe < 0) throw new Error(`le repere « ${ARRET} » a disparu du plan de la ruche`);
  const dessin = script.slice(0, script.lastIndexOf('/*', coupe));

  const racine = faireNoeud('svg');
  const ctx = {
    document: {
      getElementById: (id) => (id === 'svg' ? racine : faireNoeud('div')),
      createElementNS: (_ns, tag) => faireNoeud(tag),
      createElement: (tag) => faireNoeud(tag),
      addEventListener() {},
    },
    window: { addEventListener() {} },
    console: { log() {}, warn() {} },
  };
  createContext(ctx);
  runInContext(dessin + '\n;globalThis.__zones = typeof ZONES === "undefined" ? [] : ZONES;', ctx);

  const propre = (n) => ({
    tag: n.tag,
    attrs: n.attrs,
    ...(n.texte ? { texte: n.texte } : {}),
    ...(n.enfants.length ? { enfants: n.enfants.map(propre) } : {}),
  });

  const lieux = ctx.__zones.map((z) => ({
    id: z.dataset.id,
    nom: z.dataset.nom,
    tag: z.tag,
    attrs: z.attrs,
  }));

  return { vue, style, dessin: racine.enfants.map(propre), lieux };
}

function principal() {
  const controleSeul = process.argv.includes('--controle-seul');
  const ruche = moissonnerLaRuche();

  const pb = [];
  if (!ruche.dessin.length) pb.push('le plan de la ruche n\'a produit aucun dessin');
  if (ruche.lieux.length < 10) pb.push(`le plan n'a que ${ruche.lieux.length} lieux nommes`);
  for (const l of ruche.lieux) {
    if (!l.id || !l.nom) pb.push(`un lieu du plan n'a plus d'identifiant ou de nom`);
  }

  if (pb.length) {
    console.error('\nLe site ne peut plus lire le plan de la ruche :\n');
    for (const m of pb) console.error('  · ' + m);
    console.error('');
    process.exit(1);
  }

  if (controleSeul) {
    console.log('plan de la ruche : lisible');
    return;
  }

  mkdirSync(join(ici, 'donnees'), { recursive: true });
  writeFileSync(join(ici, 'donnees', 'ruche.json'), JSON.stringify(ruche), 'utf8');
  const compte = (n) => 1 + (n.enfants || []).reduce((s, e) => s + compte(e), 0);
  const total = ruche.dessin.reduce((s, n) => s + compte(n), 0);
  console.log(`plan de la ruche : ${total} traces, ${ruche.lieux.length} lieux`);
}

if (process.argv[1] === fileURLToPath(import.meta.url)) principal();
