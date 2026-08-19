# Tranche 1 — un livre qui se lit, en ligne, derrière une porte

> **Pour les agents :** SOUS-SKILL REQUISE — utiliser `superpowers:subagent-driven-development`
> (recommandé) ou `superpowers:executing-plans` pour exécuter ce plan tâche par tâche.
> Les étapes sont en cases à cocher (`- [ ]`).

**But :** publier les trois textes écrits de *L'Éclaircie* sur un site Astro statique, alimenté
par les sources de l'atelier, protégé par une phrase de passe, et incapable de laisser fuiter
les notes de l'autrice.

**Architecture :** un script de moisson évalue les modules de données de l'atelier dans un bac à
sable Node et n'en fait sortir que les champs destinés au lecteur. Astro construit une page
statique par texte. Deux contrôles automatiques gardent l'ouvrage : le contrat de données, qui
échoue si la forme change, et le contrôle anti-fuite, qui échoue si une note d'autrice apparaît
dans le HTML livré.

**Pile :** Node 22 · Astro 6.3 · `node:test` (aucune dépendance de test) · Vercel Routing
Middleware.

**Référence :** [la conception](2026-08-19-site-de-lecture.md). Hors périmètre ici : l'ambiance,
la progression, la seconde lecture.

---

## Ce que l'inspection des données a révélé

Deux découvertes changent le plan par rapport à la conception :

**1. Les entrées de `TEXTES` contiennent les notes de travail de l'autrice.** Chaque texte porte
neuf champs : `id`, `rang`, `titre`, `scene`, `sous`, `p`, `tenu`, `ouvre`, `note`. Seul `p` est
le roman. `tenu` et `ouvre` sont des analyses d'écriture qui expliquent le montage en clair
(*« six cents pages plus loin il dira… »*), et `sous` nomme le point de vue — donc **la voie**.

Conséquence : la moisson ne copie pas les objets, **elle liste ce qui traverse**. Passent `id`,
`rang`, `titre`, `p`. Rien d'autre. Un champ ajouté demain par l'autrice ne franchira pas la
frontière tout seul.

**2. Un paragraphe du roman contient du HTML.** Un seul, dans le prologue :
`— <em>C'est toi qui porteras la corde.</em>`. On ne peut donc ni tout échapper (l'italique
serait perdu) ni tout laisser passer. Il faut un filtre à liste blanche : `<em>` et `<strong>`
passent, tout le reste s'échappe.

**2 bis. Un bloc de paragraphe peut porter une classe.** *Découvert à l'exécution, par le
contrat lui-même :* deux paragraphes du roman s'écrivent `[balise, texte, classe]`, avec la
classe `fin` — une respiration avant le dernier paragraphe, que le rendu de l'atelier applique
déjà (`p3-style.html:206`). La forme admise est donc le couple **ou** le triplet, et la classe
passe elle aussi par liste blanche : une classe nouvelle arrête la fabrication au lieu
d'entrer dans le HTML.

**3. Le contrôle anti-fuite ne peut pas chercher « andrew ».** Le prénom est dans le roman
(*« Bonjour Andrew. On est deux ? »*). Le contrôle sera donc **piloté par les données** : on prend
les champs interdits dans les sources, et on vérifie que leur contenu exact est absent du HTML
construit. Zéro faux positif, zéro angle mort.

---

## Structure des fichiers

| Fichier | Responsabilité |
|---|---|
| `CLAUDE.md` (racine du dépôt) | la loi commune et la frontière entre les deux sessions |
| `09-site/CLAUDE.md` | les règles du site seul |
| `09-site/package.json` | dépendances et commandes |
| `09-site/astro.config.mjs` | configuration Astro |
| `09-site/outils/contrat.mjs` | le contrat de données et la liste blanche — fonctions pures |
| `09-site/outils/assainir.mjs` | le filtre HTML des paragraphes — fonction pure |
| `09-site/extraire.mjs` | la moisson : sources → JSON, applique le contrat |
| `09-site/tests/contrat.test.mjs` | tests du contrat |
| `09-site/tests/assainir.test.mjs` | tests du filtre |
| `09-site/tests/fuite.test.mjs` | contrôle anti-fuite sur `dist/` |
| `09-site/src/styles/jetons.css` | les jetons hérités de l'atelier, **sans les couleurs de voie** |
| `09-site/src/layouts/Page.astro` | l'ossature commune, `noindex` |
| `09-site/src/pages/index.astro` | le sommaire |
| `09-site/src/pages/lire/[id].astro` | une page par texte |
| `09-site/middleware.ts` | la porte |
| `09-site/donnees/textes.json` | produit par la moisson, jamais commité |

---

## Tâche 1 : La frontière

Elle vient en premier : elle protège tout ce qui suit.

**Fichiers :**
- Créer : `CLAUDE.md`
- Créer : `09-site/CLAUDE.md`

- [ ] **Étape 1 : Écrire la loi commune**

Créer `CLAUDE.md` à la racine du dépôt :

```markdown
# Comment on travaille dans ce dépôt

Ce dépôt porte un roman en cours d'écriture, *L'Éclaircie*, et les outils qui servent à
l'écrire. Deux personnes y travaillent, chacune avec sa propre session, et les sessions ne
se parlent pas. Ce fichier est ce qu'elles ont en commun.

## La règle qui prime sur toutes les autres

**On valide avec l'autrice avant d'intégrer.** Aucune proposition n'entre dans `develop`
sans son accord, et rien ne touche à la frise narrative sans qu'elle l'ait dit.

## La source de vérité

`06-visuels/atelier/atelier.html` est la source de vérité du projet. Les fichiers Markdown
sont les développements : en cas de désaccord, l'atelier a raison.

**On n'édite jamais `atelier.html` à la main.** On modifie un morceau dans
`06-visuels/atelier/sources/`, puis :

```bash
cd 06-visuels/atelier/sources && sh fabriquer.sh
```

## Les branches

Gitflow, décrit en détail dans `CONTRIBUER.md`. `main` ne reçoit que des états publiés,
`develop` le travail en cours, et tout passe par une branche `feature/` partie de `develop`.
On ne commite jamais directement sur `main`.

**Une branche ne se fusionne pas si `fabriquer.sh` ne passe pas.**

## La frontière

Le dossier `09-site/` contient le site de lecture publié sur Vercel. Il est tenu à part.

- **La session d'écriture ne descend jamais dans `09-site/`.** Rien de ce qui s'y trouve
  n'a besoin d'être modifié pour écrire le roman.
- **La session du site ne touche jamais au manuscrit** — ni `05-manuscrit/`, ni
  `06-visuels/atelier/sources/`, ni aucun des dossiers numérotés `01-` à `08-`. Elle les lit,
  elle ne les écrit pas.

Cette frontière existe parce que le site *lit* les données de l'atelier. Il en dépend, et il
ne doit jamais devenir une raison de modifier le travail d'écriture.

## Le contrat de données

Le site lit `TEXTES` dans `pB-textes.js` et `SCENES` dans `p5-scenes.js`.

**Le contenu est libre — c'est le texte de l'autrice.** Ce qui est sous contrat, c'est la
*forme* : le nom des champs, la structure des paragraphes `[balise, texte]`, l'existence des
identifiants de scène.

`fabriquer.sh` vérifie ce contrat à chaque fabrication. S'il échoue, le message dit quoi
réparer. Ne pas contourner le contrôle : le corriger, ou prévenir la session du site.
```

- [ ] **Étape 2 : Écrire les règles du site**

Créer `09-site/CLAUDE.md` :

```markdown
# Le site de lecture — règles de travail

Lire d'abord `conception/2026-08-19-site-de-lecture.md`. Ce fichier n'en est que le rappel
opérationnel.

## Ce qui ne se négocie pas

**1. Le texte se lit même si tout le reste tombe.** JavaScript coupé, ambiance cassée,
navigateur ancien : on lit le roman. Toute fonctionnalité est une couche par-dessus du HTML
qui se suffit à lui-même.

**2. Rien des notes de l'autrice n'atteint le lecteur.** Les entrées de `TEXTES` contiennent
`sous`, `tenu`, `ouvre` et `note` : ce sont ses analyses d'écriture, elles expliquent le
montage du roman en clair. La moisson **liste ce qui traverse** (`id`, `rang`, `titre`, `p`)
au lieu d'exclure ce qui ne doit pas passer. Un champ nouveau ne franchit donc jamais la
frontière par accident.

**3. Le roman est bâti sur un tour, et le site le joue.** Les scènes d'Andrew se passent dans
la ruche, celles de Joël dans la vie d'avant, et le lecteur ne le sait pas. En première
lecture, aucune couleur de voie, aucun plan, aucune frise, aucun point de vue nommé.

**4. On ne touche à rien hors de `09-site/`.** Une seule exception, décidée avec l'autrice :
l'accroche du contrôle de contrat dans `06-visuels/atelier/sources/fabriquer.sh`.

## Les commandes

```bash
npm run moisson     # sources de l'atelier -> donnees/textes.json
npm run dev         # moisson puis serveur de developpement
npm run build       # moisson, construction, controle anti-fuite
npm test            # les tests des outils
```

## La pile

Astro 6.3, statique. Aucune dépendance de test : `node:test`, fourni par Node 22.
Le natif partout où le navigateur sait faire ; une librairie seulement là où il ne sait pas.
```

- [ ] **Étape 3 : Vérifier que les deux fichiers existent**

Lancer : `ls -l CLAUDE.md 09-site/CLAUDE.md`
Attendu : les deux fichiers listés, non vides.

- [ ] **Étape 4 : Commiter**

```bash
git add CLAUDE.md 09-site/CLAUDE.md
git commit -m "La frontiere entre les deux sessions est ecrite"
```

---

## Tâche 2 : Le socle

**Fichiers :**
- Créer : `09-site/package.json`
- Créer : `09-site/astro.config.mjs`
- Créer : `09-site/src/pages/index.astro`
- Modifier : `.gitignore`

- [ ] **Étape 1 : Écrire `09-site/package.json`**

```json
{
  "name": "eclaircie-site",
  "type": "module",
  "private": true,
  "scripts": {
    "moisson": "node extraire.mjs",
    "dev": "npm run moisson && astro dev",
    "build": "npm run moisson && astro build && node --test tests/fuite.test.mjs",
    "preview": "astro preview",
    "test": "node --test tests/contrat.test.mjs tests/assainir.test.mjs"
  },
  "dependencies": {
    "astro": "^6.3.1",
    "@vercel/functions": "^2.0.0"
  }
}
```

- [ ] **Étape 2 : Écrire `09-site/astro.config.mjs`**

```js
import { defineConfig } from 'astro/config';

export default defineConfig({
  // Statique : chaque texte est une page HTML complete, servie telle quelle.
  output: 'static',
  build: { format: 'directory' },
});
```

- [ ] **Étape 3 : Écrire une page témoin `09-site/src/pages/index.astro`**

```astro
---
// Page temoin : remplacee par le sommaire a la tache 6.
---
<html lang="fr">
  <head><meta charset="utf-8" /><title>L'Éclaircie</title></head>
  <body><p>Le socle tient.</p></body>
</html>
```

- [ ] **Étape 4 : Étendre `.gitignore`**

Ajouter à la fin de `.gitignore`, à la racine du dépôt :

```gitignore
# le site de lecture : tout se regenere
09-site/node_modules/
09-site/dist/
09-site/donnees/
09-site/.astro/
09-site/.vercel/
```

- [ ] **Étape 5 : Installer et construire**

Lancer : `cd 09-site && npm install && npx astro build`
Attendu : `dist/index.html` existe et contient « Le socle tient. »

> `npm run build` échouera à ce stade : `extraire.mjs` n'existe pas encore. C'est normal,
> on passe par `npx astro build` jusqu'à la tâche 4.

- [ ] **Étape 6 : Commiter**

```bash
git add 09-site/package.json 09-site/package-lock.json 09-site/astro.config.mjs 09-site/src/pages/index.astro .gitignore
git commit -m "Le socle du site tient debout"
```

---

## Tâche 3 : Le contrat de données

Fonctions pures, sans lecture de fichier : elles se testent seules.

**Fichiers :**
- Créer : `09-site/outils/contrat.mjs`
- Créer : `09-site/tests/contrat.test.mjs`

- [ ] **Étape 1 : Écrire le test qui échoue**

Créer `09-site/tests/contrat.test.mjs` :

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { verifierLeContrat, pourLeLecteur } from '../outils/contrat.mjs';

const scenes = [{ id: 'ouv' }, { id: 'capsule' }];
const texteValide = {
  id: 'prologue', rang: 'Prologue', titre: 'La cérémonie', scene: 'ouv',
  sous: "point de vue d'Andrew",
  p: [['p', 'Deux capsules.'], ['tiret', '— On est deux.'], ['pause', '· · ·']],
  tenu: ['note interne'], ouvre: ['chantier'], note: 'ecrit avec l autrice',
};

test('des donnees conformes ne remontent aucun probleme', () => {
  assert.deepEqual(verifierLeContrat({ TEXTES: [texteValide], SCENES: scenes }), []);
});

test('un champ manquant est signale avec le nom du texte', () => {
  const { titre, ...sansTitre } = texteValide;
  const pb = verifierLeContrat({ TEXTES: [sansTitre], SCENES: scenes });
  assert.equal(pb.length, 1);
  assert.match(pb[0], /prologue/);
  assert.match(pb[0], /titre/);
});

test('une scene inconnue est signalee', () => {
  const pb = verifierLeContrat({ TEXTES: [{ ...texteValide, scene: 'nulle-part' }], SCENES: scenes });
  assert.equal(pb.length, 1);
  assert.match(pb[0], /nulle-part/);
});

test('un identifiant en double est signale', () => {
  const pb = verifierLeContrat({ TEXTES: [texteValide, texteValide], SCENES: scenes });
  assert.ok(pb.some((m) => /double/.test(m)));
});

test('une balise inconnue du site est signalee', () => {
  const casse = { ...texteValide, p: [['citation', 'un mot']] };
  const pb = verifierLeContrat({ TEXTES: [casse], SCENES: scenes });
  assert.equal(pb.length, 1);
  assert.match(pb[0], /citation/);
});

test('un bloc mal forme est signale', () => {
  const casse = { ...texteValide, p: [['p']] };
  const pb = verifierLeContrat({ TEXTES: [casse], SCENES: scenes });
  assert.equal(pb.length, 1);
  assert.match(pb[0], /balise, texte/);
});

test('un bloc avec une classe connue passe', () => {
  const avecClasse = { ...texteValide, p: [['p', 'Il éteignit les deux lampes.', 'fin']] };
  assert.deepEqual(verifierLeContrat({ TEXTES: [avecClasse], SCENES: scenes }), []);
});

test('une classe inconnue du site est signalee', () => {
  const casse = { ...texteValide, p: [['p', 'Il sortit.', 'exergue']] };
  const pb = verifierLeContrat({ TEXTES: [casse], SCENES: scenes });
  assert.equal(pb.length, 1);
  assert.match(pb[0], /exergue/);
});

test('un bloc a quatre elements est signale', () => {
  const casse = { ...texteValide, p: [['p', 'a', 'fin', 'de trop']] };
  const pb = verifierLeContrat({ TEXTES: [casse], SCENES: scenes });
  assert.equal(pb.length, 1);
  assert.match(pb[0], /triplet/);
});

test('TEXTES disparu est signale sans planter', () => {
  const pb = verifierLeContrat({ SCENES: scenes });
  assert.equal(pb.length, 1);
  assert.match(pb[0], /TEXTES/);
});

test('seuls quatre champs traversent jusqu au lecteur', () => {
  const [sorti] = pourLeLecteur([texteValide]);
  assert.deepEqual(Object.keys(sorti).sort(), ['id', 'p', 'rang', 'titre']);
});

test('un champ nouveau ne traverse pas tout seul', () => {
  const avecNouveau = { ...texteValide, confidence: "ce qui ne doit pas sortir" };
  const [sorti] = pourLeLecteur([avecNouveau]);
  assert.equal(sorti.confidence, undefined);
});
```

- [ ] **Étape 2 : Lancer le test pour le voir échouer**

Lancer : `cd 09-site && node --test tests/contrat.test.mjs`
Attendu : ÉCHEC — `Cannot find module '../outils/contrat.mjs'`

- [ ] **Étape 3 : Écrire l'implémentation**

Créer `09-site/outils/contrat.mjs` :

```js
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
```

- [ ] **Étape 4 : Lancer le test pour le voir passer**

Lancer : `cd 09-site && node --test tests/contrat.test.mjs`
Attendu : SUCCÈS — 12 tests passés.

- [ ] **Étape 5 : Commiter**

```bash
git add 09-site/outils/contrat.mjs 09-site/tests/contrat.test.mjs
git commit -m "Le contrat de donnees sait dire ce qui a change"
```

---

## Tâche 4 : La moisson

**Fichiers :**
- Créer : `09-site/extraire.mjs`

- [ ] **Étape 1 : Écrire l'implémentation**

Il n'y a pas de test unitaire pour cette tâche : la moisson n'est que de la lecture de
fichiers plus le contrat, déjà testé. Elle se vérifie sur les vraies données à l'étape 2.

Créer `09-site/extraire.mjs` :

```js
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
```

- [ ] **Étape 2 : Vérifier sur les vraies données**

Lancer : `cd 09-site && node extraire.mjs`
Attendu : `moisson : 3 textes`

- [ ] **Étape 3 : Vérifier qu'aucune note d'autrice n'est dans le JSON**

Lancer : `cd 09-site && node -e "const t=require('./donnees/textes.json'); console.log(JSON.stringify(Object.keys(t[0])))"`
Attendu : `["id","rang","titre","p"]`

- [ ] **Étape 4 : Vérifier que le contrôle seul fonctionne**

Lancer : `cd 09-site && node extraire.mjs --controle-seul`
Attendu : `contrat du site : respecte`, et aucun fichier réécrit.

- [ ] **Étape 5 : Commiter**

```bash
git add 09-site/extraire.mjs
git commit -m "La moisson va chercher les textes dans l'atelier"
```

---

## Tâche 5 : L'assainisseur

**Fichiers :**
- Créer : `09-site/outils/assainir.mjs`
- Créer : `09-site/tests/assainir.test.mjs`

- [ ] **Étape 1 : Écrire le test qui échoue**

Créer `09-site/tests/assainir.test.mjs` :

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { assainir } from '../outils/assainir.mjs';

test('un paragraphe ordinaire ne bouge pas', () => {
  assert.equal(assainir('Deux capsules étaient venues.'), 'Deux capsules étaient venues.');
});

test('l italique du roman passe', () => {
  assert.equal(
    assainir("— <em>C'est toi qui porteras la corde.</em>"),
    "— <em>C'est toi qui porteras la corde.</em>",
  );
});

test('le gras passe', () => {
  assert.equal(assainir('<strong>net</strong>'), '<strong>net</strong>');
});

test('toute autre balise est echappee', () => {
  assert.equal(assainir('<script>vol()</script>'), '&lt;script&gt;vol()&lt;/script&gt;');
});

test('une esperluette est echappee', () => {
  assert.equal(assainir('Pierre & Paul'), 'Pierre &amp; Paul');
});

test('un chevron seul est echappe', () => {
  assert.equal(assainir('a < b'), 'a &lt; b');
});

test('une balise autorisee avec un attribut est echappee', () => {
  assert.equal(
    assainir('<em onclick="vol()">x</em>'),
    '&lt;em onclick="vol()"&gt;x&lt;/em&gt;',
  );
});
```

- [ ] **Étape 2 : Lancer le test pour le voir échouer**

Lancer : `cd 09-site && node --test tests/assainir.test.mjs`
Attendu : ÉCHEC — `Cannot find module '../outils/assainir.mjs'`

- [ ] **Étape 3 : Écrire l'implémentation**

Créer `09-site/outils/assainir.mjs` :

```js
/* Les paragraphes du roman portent, tres rarement, de l'italique ou du gras.
   Tout le reste est du texte, et s'echappe.
   Liste blanche stricte : les balises nues, sans le moindre attribut. */

const AUTORISEES = /<\/?(?:em|strong)>/g;
const SENTINELLE = (n) => ` ${n} `;

export function assainir(texte) {
  const gardees = [];

  /* 1. On met les balises autorisees de cote. */
  let s = String(texte).replace(AUTORISEES, (balise) => {
    gardees.push(balise);
    return SENTINELLE(gardees.length - 1);
  });

  /* 2. On echappe tout ce qui reste. */
  s = s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  /* 3. On les remet. */
  gardees.forEach((balise, n) => {
    s = s.split(SENTINELLE(n)).join(balise);
  });

  return s;
}
```

- [ ] **Étape 4 : Lancer le test pour le voir passer**

Lancer : `cd 09-site && node --test tests/assainir.test.mjs`
Attendu : SUCCÈS — 7 tests passés.

- [ ] **Étape 5 : Commiter**

```bash
git add 09-site/outils/assainir.mjs 09-site/tests/assainir.test.mjs
git commit -m "L'italique du roman passe, le reste s'echappe"
```

---

## Tâche 6 : Les jetons et l'ossature

**Fichiers :**
- Créer : `09-site/src/styles/jetons.css`
- Créer : `09-site/src/layouts/Page.astro`

- [ ] **Étape 1 : Écrire les jetons**

Créer `09-site/src/styles/jetons.css`. Sous-ensemble neutre de la palette de l'atelier —
**aucune couleur de voie**, elles appartiennent à la seconde lecture.

```css
/* Herite de l'atelier : 06-visuels/atelier/sources/p1-style.html.
   Les couleurs de voie (--andrew, --joel, --commun) sont volontairement
   absentes : elles trahiraient le montage du roman. */
:root {
  --fond: #E9EDF1; --fond-2: #FFFFFF; --fond-3: #F5F8FA;
  --trait: #D0D9E1; --trait-fort: #A9B9C7;
  --texte: #13202C; --texte-2: #43596E; --texte-3: #6E8699; --texte-4: #93A6B5;
  --accent: #1B7690;
  --serif: Constantia, "Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif;
  --sans: Corbel, Candara, "Segoe UI", Tahoma, sans-serif;
  --mesure: 34rem;
}

@media (prefers-color-scheme: dark) {
  :root {
    --fond: #0A0E13; --fond-2: #101720; --fond-3: #161F2A;
    --trait: #22303E; --trait-fort: #35495D;
    --texte: #E6EBF0; --texte-2: #A7B5C2; --texte-3: #6D8093; --texte-4: #4B5D6E;
    --accent: #7CC6DC;
  }
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--fond);
  color: var(--texte);
  font-family: var(--serif);
  font-size: 1.125rem;
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}

a { color: inherit; }
::selection { background: var(--accent); color: var(--fond); }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }
```

- [ ] **Étape 2 : Écrire l'ossature**

Créer `09-site/src/layouts/Page.astro` :

```astro
---
import '../styles/jetons.css';
const { titre } = Astro.props;
---
<html lang="fr">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <!-- Phase privee : le site ne s'indexe pas. -->
    <meta name="robots" content="noindex, nofollow" />
    <title>{titre}</title>
  </head>
  <body>
    <slot />
  </body>
</html>
```

- [ ] **Étape 3 : Commiter**

```bash
git add 09-site/src/styles/jetons.css 09-site/src/layouts/Page.astro
git commit -m "Les jetons de l'atelier, moins ce qui trahit"
```

---

## Tâche 7 : Le sommaire

**Fichiers :**
- Modifier : `09-site/src/pages/index.astro` (remplace la page témoin)

- [ ] **Étape 1 : Remplacer la page témoin**

Écrire `09-site/src/pages/index.astro` :

```astro
---
import Page from '../layouts/Page.astro';
import textes from '../../donnees/textes.json';
---
<Page titre="L'Éclaircie">
  <main class="sommaire">
    <h1>L'Éclaircie</h1>
    <p class="exergue">
      L'irréparable est condamné, le réparable est pardonné, le meurtri est gracié.
    </p>

    <ol>
      {textes.map((t) => (
        <li>
          <a href={`/lire/${t.id}/`}>
            <span class="rang">{t.rang}</span>
            <span class="titre">{t.titre}</span>
          </a>
        </li>
      ))}
    </ol>

    <p class="etat">Un roman en cours d'écriture.</p>
  </main>
</Page>

<style>
  .sommaire { max-width: var(--mesure); margin: 0 auto; padding: 4rem 1.5rem; }
  h1 { font-weight: 400; font-size: 2.25rem; letter-spacing: .01em; margin: 0 0 1.5rem; }
  .exergue { color: var(--texte-2); font-style: italic; margin: 0 0 3rem; }
  ol { list-style: none; padding: 0; margin: 0; }
  li { border-top: 1px solid var(--trait); }
  li:last-child { border-bottom: 1px solid var(--trait); }
  a { display: flex; flex-direction: column; gap: .2rem; padding: 1.1rem 0; text-decoration: none; }
  a:hover .titre { color: var(--accent); }
  .rang {
    font-family: var(--sans); font-size: .75rem; letter-spacing: .16em;
    text-transform: uppercase; color: var(--texte-3);
  }
  .titre { font-size: 1.25rem; transition: color .16s; }
  .etat { margin-top: 3rem; font-family: var(--sans); font-size: .8rem; color: var(--texte-4); }
</style>
```

- [ ] **Étape 2 : Construire et vérifier**

Lancer : `cd 09-site && npm run moisson && npx astro build`
Attendu : construction réussie ; `dist/index.html` contient « La cérémonie », « Une journée
à la ruche » et « Épilogue ».

- [ ] **Étape 3 : Commiter**

```bash
git add 09-site/src/pages/index.astro
git commit -m "Le sommaire donne les trois textes ecrits"
```

---

## Tâche 8 : La page de lecture

**Fichiers :**
- Créer : `09-site/src/pages/lire/[id].astro`

- [ ] **Étape 1 : Écrire la page**

Créer `09-site/src/pages/lire/[id].astro` :

```astro
---
import Page from '../../layouts/Page.astro';
import { assainir } from '../../../outils/assainir.mjs';
import textes from '../../../donnees/textes.json';

export function getStaticPaths() {
  return textes.map((t, i) => ({
    params: { id: t.id },
    props: { texte: t, precedent: textes[i - 1] ?? null, suivant: textes[i + 1] ?? null },
  }));
}

const { texte, precedent, suivant } = Astro.props;
---
<Page titre={`${texte.titre} — L'Éclaircie`}>
  <article class="texte">
    <header>
      <p class="rang">{texte.rang}</p>
      <h1>{texte.titre}</h1>
    </header>

    {texte.p.map(([balise, contenu, classe]) => (
      balise === 'pause'
        ? <p class="pause" aria-hidden="true">{contenu}</p>
        : <p
            class={[balise === 'tiret' ? 'tiret' : null, classe].filter(Boolean).join(' ')}
            set:html={assainir(contenu)}
          />
    ))}

    <nav>
      {precedent && <a href={`/lire/${precedent.id}/`}>← {precedent.titre}</a>}
      <a href="/">Sommaire</a>
      {suivant && <a href={`/lire/${suivant.id}/`}>{suivant.titre} →</a>}
    </nav>
  </article>
</Page>

<style>
  .texte { max-width: var(--mesure); margin: 0 auto; padding: 4rem 1.5rem 6rem; }
  header { margin-bottom: 3.5rem; }
  .rang {
    font-family: var(--sans); font-size: .75rem; letter-spacing: .16em;
    text-transform: uppercase; color: var(--texte-3); margin: 0 0 .5rem;
  }
  h1 { font-weight: 400; font-size: 2rem; margin: 0; }
  p { margin: 0 0 1.35em; text-wrap: pretty; }
  .tiret { text-indent: 0; }
  /* Une respiration avant le dernier paragraphe, comme dans l'atelier. */
  .fin { margin-top: 1.6em; }
  .pause {
    text-align: center; color: var(--texte-4); letter-spacing: .5em;
    margin: 2.5em 0; user-select: none;
  }
  nav {
    display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap;
    margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid var(--trait);
    font-family: var(--sans); font-size: .85rem;
  }
  nav a { color: var(--texte-3); text-decoration: none; }
  nav a:hover { color: var(--accent); }
</style>
```

- [ ] **Étape 2 : Construire et vérifier les trois pages**

Lancer : `cd 09-site && npm run moisson && npx astro build && ls dist/lire/`
Attendu : `prologue/`, `chapitre-1/`, `epilogue/`

- [ ] **Étape 3 : Vérifier que l'italique du roman a survécu**

Lancer : `cd 09-site && grep -c "<em>C'est toi qui porteras la corde.</em>" dist/lire/prologue/index.html`
Attendu : `1`

- [ ] **Étape 4 : Commiter**

```bash
git add "09-site/src/pages/lire/[id].astro"
git commit -m "Une page par texte, et le roman se lit"
```

---

## Tâche 9 : Le contrôle anti-fuite

Piloté par les données : on prend les champs interdits dans les vraies sources, et on vérifie
que leur contenu exact est absent du HTML construit. Aucun faux positif possible — le prénom
« Andrew » est dans le roman, il ne peut donc pas servir de sonde.

**Fichiers :**
- Créer : `09-site/tests/fuite.test.mjs`

- [ ] **Étape 1 : Écrire le test**

Créer `09-site/tests/fuite.test.mjs` :

```js
/* Le seul controle qui compte : on regarde ce que le lecteur recoit.
   Il tourne sur dist/, apres la construction. */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
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

const pages = toutesLesPages(DIST).map((c) => [c, readFileSync(c, 'utf8')]);
const { TEXTES } = moissonner();

/* Les couleurs de voie de l'atelier — les deux themes.
   Source : 06-visuels/atelier/sources/p1-style.html */
const COULEURS_DE_VOIE = [
  '#7CC6DC', '#D2A06B', '#94A3B1', '#2C5B6B', '#6A4E2C', '#3A4854',  // sombre
  '#1B7690', '#8E5D1E', '#5A6C7C', '#B4DCE7', '#EBD6B8', '#CBD5DD',  // clair
];

test('la construction a bien produit des pages', () => {
  assert.ok(pages.length >= 4, `attendu au moins 4 pages, trouve ${pages.length}`);
});

test('aucune note de travail de l autrice n atteint le lecteur', () => {
  for (const t of TEXTES) {
    const interdits = [
      t.sous,
      t.note,
      ...(Array.isArray(t.tenu) ? t.tenu : []),
      ...(Array.isArray(t.ouvre) ? t.ouvre : []),
    ].filter((v) => typeof v === 'string' && v.length > 40);

    for (const morceau of interdits) {
      /* On sonde sur un fragment assez long pour etre sans ambiguite. */
      const sonde = morceau.slice(0, 40);
      for (const [chemin, html] of pages) {
        assert.ok(
          !html.includes(sonde),
          `fuite dans ${chemin} : « ${sonde}… » vient d'un champ interdit du texte « ${t.id} »`,
        );
      }
    }
  }
});

test('le JSON de la moisson n est pas servi au lecteur', () => {
  /* donnees/ est un intermediaire de fabrication : rien n'en sort tel quel. */
  const servis = toutesLesPages(DIST);
  assert.ok(
    !servis.some((c) => c.includes('donnees')),
    'le dossier donnees/ a ete recopie dans dist/',
  );
  for (const [chemin, html] of pages) {
    assert.ok(
      !html.includes('"sous"') && !html.includes('"tenu"') && !html.includes('"ouvre"'),
      `fuite dans ${chemin} : un objet de donnees brut a ete serialise dans la page`,
    );
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
```

> Note d'implémentation : `--accent` a été repris de l'atelier dans les deux thèmes —
> `#1B7690` en clair, `#7CC6DC` en sombre. **Ce sont les deux couleurs d'Andrew.** Le test
> les refusera, et il a raison : une couleur de voie n'a rien à faire dans la première
> lecture, même comme simple accent. C'est précisément le genre d'emprunt distrait que ce
> contrôle existe pour attraper. Les deux se corrigent à l'étape 3.

- [ ] **Étape 2 : Lancer le test pour le voir échouer**

Lancer : `cd 09-site && npm run moisson && npx astro build && node --test tests/fuite.test.mjs`
Attendu : ÉCHEC sur « aucune couleur de voie » — `#1B7690` et `#7CC6DC` sont présents, via
`--accent`.

- [ ] **Étape 3 : Corriger les deux accents**

Dans `09-site/src/styles/jetons.css`, remplacer dans le bloc `:root` :

```css
  --accent: #1B7690;
```

par :

```css
  --accent: #2F6E7E;
```

puis, dans le bloc `@media (prefers-color-scheme: dark)` :

```css
    --accent: #7CC6DC;
```

par :

```css
    --accent: #8FBCCB;
```

- [ ] **Étape 4 : Reconstruire et lancer le test pour le voir passer**

Lancer : `cd 09-site && npx astro build && node --test tests/fuite.test.mjs`
Attendu : SUCCÈS — 4 tests passés.

- [ ] **Étape 5 : Vérifier que `npm run build` enchaîne bien tout**

Lancer : `cd 09-site && npm run build`
Attendu : moisson, construction, puis les 4 tests anti-fuite passés.

- [ ] **Étape 6 : Commiter**

```bash
git add 09-site/tests/fuite.test.mjs 09-site/src/styles/jetons.css
git commit -m "Rien des notes de l'autrice n'atteint le lecteur, et c'est verifie"
```

---

## Tâche 10 : La porte

Un rideau, pas une serrure : assez pour « pas public », pas pour « secret ».

**Fichiers :**
- Créer : `09-site/middleware.ts`

- [ ] **Étape 1 : Écrire la porte**

Créer `09-site/middleware.ts` :

```ts
/* La porte de la phase privee.
   Vercel Routing Middleware : un fichier a la racine du projet, valable pour
   tous les frameworks, y compris un site entierement statique.

   Sans la variable d'environnement PHRASE_DE_PASSE, le site est ouvert :
   c'est ainsi qu'on publiera, le jour venu, sans rien reecrire. */
import { next } from '@vercel/functions';

export const config = { matcher: '/((?!_astro/).*)' };

const COOKIE = 'eclaircie';

const PAGE = `<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>L'Éclaircie</title>
<style>
  body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0A0E13;
       color:#E6EBF0;font-family:Constantia,Georgia,serif}
  form{display:flex;flex-direction:column;gap:1rem;width:min(22rem,80vw)}
  p{margin:0;color:#A7B5C2;font-style:italic;text-align:center}
  input{font:inherit;padding:.7rem .9rem;background:#161F2A;color:inherit;
        border:1px solid #35495D;border-radius:4px}
  button{font-family:Corbel,"Segoe UI",sans-serif;font-size:.8rem;letter-spacing:.16em;
         text-transform:uppercase;padding:.7rem;background:#E6EBF0;color:#0A0E13;
         border:0;border-radius:4px;cursor:pointer}
</style></head><body>
<form method="GET"><p>L'Éclaircie</p>
<input type="password" name="phrase" placeholder="la phrase de passe" autofocus>
<button type="submit">Entrer</button></form>
</body></html>`;

export default function middleware(request: Request): Response {
  const attendue = process.env.PHRASE_DE_PASSE;
  if (!attendue) return next();

  const url = new URL(request.url);
  const cookie = request.headers.get('cookie') ?? '';

  if (cookie.split(';').some((c) => c.trim() === `${COOKIE}=${attendue}`)) return next();

  if (url.searchParams.get('phrase') === attendue) {
    return new Response(null, {
      status: 302,
      headers: {
        location: url.pathname,
        'set-cookie': `${COOKIE}=${attendue}; Path=/; HttpOnly; Secure;`
                    + ` SameSite=Lax; Max-Age=31536000`,
      },
    });
  }

  return new Response(PAGE, {
    status: 401,
    headers: { 'content-type': 'text/html; charset=utf-8' },
  });
}
```

- [ ] **Étape 2 : Vérifier que le fichier compile**

Lancer : `cd 09-site && npx -y -p typescript tsc --noEmit --module esnext --target es2022 --moduleResolution bundler --skipLibCheck middleware.ts`
Attendu : aucune erreur.

- [ ] **Étape 3 : Commiter**

```bash
git add 09-site/middleware.ts
git commit -m "Une porte devant le site, levable d'une variable"
```

---

## Tâche 11 : L'accroche à `fabriquer.sh`

La seule modification hors de `09-site/` de toute la tranche. **Elle se valide avec l'autrice
avant d'être commitée** — c'est son outil de travail quotidien.

**Fichiers :**
- Modifier : `06-visuels/atelier/sources/fabriquer.sh`

- [ ] **Étape 1 : Ajouter le contrôle à la fin du script**

Le script se termine aujourd'hui par :

```sh
node ../valide.js
rm -f check.js combo.js
echo "FABRICATION OK"
```

Insérer le contrôle **entre `rm -f` et le `echo` final**, pour que « FABRICATION OK » ne
s'affiche que si le site tient encore lui aussi :

```sh

# Verification 3 : le site de lecture peut encore lire ces donnees.
# Il n'est pas obligatoire — l'atelier se fabrique sans lui.
if [ -f ../../../09-site/extraire.mjs ]; then
  node ../../../09-site/extraire.mjs --controle-seul || exit 1
fi
```

- [ ] **Étape 2 : Vérifier que la fabrication passe toujours**

Lancer : `cd 06-visuels/atelier/sources && sh fabriquer.sh`
Attendu : `le plan du jardin : a jour`, `atelier.html fabrique`, `syntaxe : correcte`, puis
`contrat du site : respecte`, et enfin `FABRICATION OK`.

- [ ] **Étape 3 : Vérifier que le contrôle attrape une rupture**

Casser volontairement la forme, en renommant un champ dans une copie de travail :

```bash
cd 06-visuels/atelier/sources
cp pB-textes.js pB-textes.js.sauve
sed -i '0,/  titre: /s//  intitule: /' pB-textes.js
sh fabriquer.sh; echo "code de sortie : $?"
```

Attendu : le script échoue, avec un message nommant le texte et le champ `titre`, et
`code de sortie : 1`.

- [ ] **Étape 4 : Restaurer**

```bash
cd 06-visuels/atelier/sources
mv pB-textes.js.sauve pB-textes.js
sh fabriquer.sh
git status --short
```

Attendu : `fabriquer.sh` passe, et `git status` ne montre aucune modification de
`pB-textes.js`.

- [ ] **Étape 5 : Commiter**

```bash
git add 06-visuels/atelier/sources/fabriquer.sh
git commit -m "La fabrication verifie que le site peut encore lire l'atelier"
```

---

## Tâche 12 : Le déploiement

**Fichiers :** aucun. Cette tâche se fait dans l'interface Vercel et demande un compte.

- [ ] **Étape 1 : Pousser la branche**

```bash
git push -u origin feature/site-de-lecture
```

- [ ] **Étape 2 : Créer le projet Vercel**

Importer le dépôt `pandarvis/eclaircie`, puis régler :

| Réglage | Valeur |
|---|---|
| Root Directory | `09-site` |
| Framework Preset | Astro |
| Build Command | `npm run build` |
| Output Directory | `dist` |
| Production Branch | `main` |

- [ ] **Étape 3 : Poser la phrase de passe**

Dans *Settings → Environment Variables*, ajouter `PHRASE_DE_PASSE` avec une phrase choisie
avec Élodie, pour les trois environnements.

- [ ] **Étape 4 : Vérifier l'aperçu**

Ouvrir l'URL d'aperçu de la branche.
Attendu : la porte s'affiche. La phrase entrée, le sommaire apparaît avec les trois textes,
et un rechargement ne redemande rien.

- [ ] **Étape 5 : Vérifier que la mauvaise phrase ne passe pas**

Ouvrir l'URL d'aperçu en navigation privée, entrer une phrase fausse.
Attendu : la porte se réaffiche, statut 401, et le sommaire reste inaccessible.

---

## Ce que cette tranche ne fait pas

L'ambiance (la lumière), la progression du lecteur, la seconde lecture, les transitions de
vue, le glossaire, les plans. Chacune viendra sur sa tranche. Rien ici ne les empêche : la
lumière est une couche à poser sur du HTML qui se suffit déjà, et `progression` est prévue
comme une pièce isolée dès la conception.

## Avant de fusionner dans `develop`

Trois questions attendent une réponse d'Élodie — elles sont au § 11 de la conception, et deux
d'entre elles touchent ce qui est construit ici : **l'épilogue reste-t-il librement
accessible au sommaire**, et **qu'affiche-t-on à la place des trente-cinq scènes non
écrites ?** La tranche est livrable sans y répondre, mais pas publiable.
