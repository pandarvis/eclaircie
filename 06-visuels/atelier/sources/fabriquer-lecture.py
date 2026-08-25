# -*- coding: utf-8 -*-
"""L'atelier de lecture : la version qu'on peut donner a lire.

Meme design que l'atelier, et rien de ce qui nous appartient. Ni notes,
ni parcours, ni questions ouvertes, ni fiches de personnages -- celles-ci
sont ecrites pour l'autrice et donnent le livre en trois lignes.

Regle de fabrication, et elle est absolue : le fichier de lecture ne
CONTIENT pas la matiere d'autrice, il ne se contente pas de la cacher.
Quelqu'un qui ouvre la source ne doit rien trouver de plus que ce qu'il
voit a l'ecran.

  python fabriquer-lecture.py

Sortie : 06-visuels/atelier/lecture.html
"""
import io
import os
import re
import unicodedata

ICI = os.path.dirname(os.path.abspath(__file__))


def lire(nom):
    return io.open(os.path.join(ICI, nom), encoding='utf-8').read()


def entre(s, a, b):
    return s[s.index(a) + len(a):s.index(b)]


def sans_scelle(src):
    """Retire les blocs marques scelle : ce sont des notes d'autrice.

    Le plan de la ruche est ecrit pour elle, et certains encarts disent
    ce que le livre met six cents pages a dire. On les marque dans la
    source avec la classe << scelle >>, et ils ne sortent jamais ici.
    """
    out, n = [], 0
    i = 0
    while True:
        j = src.find(u'<div class="cite scelle">', i)
        if j < 0:
            out.append(src[i:])
            break
        out.append(src[i:j])
        k = src.index(u'</div>', j) + len(u'</div>')
        i = k
        n += 1
    src = u''.join(out)
    print(u'  %d encart(s) scelle(s) retire(s) de la lecture' % n)
    return src


B = u'`'


# =====================================================================
#  LES TEXTES — le prologue et le chapitre premier, sans leur appareil
# =====================================================================
js = lire('pB-textes.js')
bornes = [(m.group(1), m.start()) for m in re.finditer(r'\n  id: `([a-z0-9-]+)`,', js)]

LISIBLES = ['prologue', 'chapitre-1', 'chapitre-2', 'chapitre-3',
            'chapitre-4', 'chapitre-5', 'chapitre-6', 'epilogue']
SOUS_CLEF = ['epilogue']          # lisibles, mais seulement apres le mot de passe


def empreinte(mot):
    """FNV-1a 32 bits, sur le mot mis a plat.

    Le mot de passe ne doit apparaitre nulle part dans le fichier : on
    n'y met que ce nombre, et la page refait le meme calcul sur ce
    qu'on tape. Ce n'est pas un coffre-fort -- voir la note du bas.
    """
    plat = unicodedata.normalize('NFD', mot.lower())
    plat = u''.join(c for c in plat if unicodedata.category(c) != 'Mn')
    plat = u''.join(c for c in plat if c.isalnum())
    h = 0x811c9dc5
    for c in plat:
        h = ((h ^ ord(c)) * 0x01000193) & 0xffffffff
    return h


CLEF = empreinte(u'Joël')
textes = []
for ident in LISIBLES:
    n = [i for i, (x, _) in enumerate(bornes) if x == ident][0]
    deb = bornes[n][1]
    fin = bornes[n + 1][1] if n + 1 < len(bornes) else len(js)
    bloc = js[deb:fin]
    rang = re.search(r'rang: `([^`]*)`', bloc).group(1)
    titre = re.search(r'titre: `([^`]*)`', bloc).group(1)
    paras = re.findall(r'\[`(p|tiret|pause)`,`([^`]*)`', bloc)
    textes.append({'id': ident, 'rang': rang, 'titre': titre, 'p': list(paras),
                   'clef': ident in SOUS_CLEF})


# =====================================================================
#  LE GLOSSAIRE — les mots du monde, sans source ni question ouverte
# =====================================================================
# (le liage des renvois se fait plus bas, une fois le glossaire lu)
monde = lire('p7-monde.js')
bloc = entre(monde, u'const GLOSSAIRE = [', u'\n];')
mots = re.findall(r'\[`([^`]*)`,`([^`]*)`,`[^`]*`,`[^`]*`\],', bloc)
assert len(mots) > 18, u'%d mots' % len(mots)   # le glossaire du lecteur se resserre quand une entree en dit trop
MOTS = (u'const MOTS = [\n'
        + u'\n'.join(u'[%s%s%s,%s%s%s],' % (B, m, B, B, d, B) for m, d in mots)
        + u'\n];\n')


# =====================================================================
#  LES RENVOIS — la premiere fois qu'un mot du monde apparait, il mene
#  a son entree. Une seule fois pour tout le livre, et jamais pour un
#  mot qui porte une tension du recit.
# =====================================================================
NE_PAS_LIER = [u'Porteur de voiles', u'Paire', u'Archiviste', u'Section 0']

def formes(entree):
    """Les ecritures possibles d'une entree, de la plus longue a la plus courte."""
    out = []
    for part in entree.split(u','):
        base = part.split(u'(')[0].strip()
        if not base:
            continue
        out.append(base)
        if not base.endswith(u's'):
            out.append(base + u's')
    return sorted(set(out), key=len, reverse=True)


def lier(textes_bruts):
    """Enveloppe la premiere occurrence de chaque entree. Retourne le compte."""
    a_lier = [m for m, d in mots if m not in NE_PAS_LIER]
    restants = {m: formes(m) for m in a_lier}
    faits = []
    for t in [x for x in textes_bruts if not x['clef']]:   # dans l'ordre de lecture
        for i, (genre, texte) in enumerate(t['p']):
            for entree in list(restants):
                pose = False
                for f in restants[entree]:
                    # hors d'une balise, sur un mot entier, casse indifferente
                    # une frontiere de mot, et hors d'une balise
                    motif = re.compile(u'\\b(' + re.escape(f) + u')\\b(?![^<]*>)',
                                       re.IGNORECASE)
                    m = motif.search(texte)
                    if m:
                        texte = (texte[:m.start(1)]
                                 + u'<a class="glo" data-mot="' + entree + u'">'
                                 + m.group(1) + u'</a>'
                                 + texte[m.end(1):])
                        t['p'][i] = (genre, texte)
                        faits.append(entree)
                        pose = True
                        break
                if pose:
                    del restants[entree]
    return faits


# =====================================================================
#  LES GENS — ecrits pour le lecteur, et seulement d'apres ce qu'il a lu
# =====================================================================
GENS = u"""const GENS = [
{ rang:`Au centre`, nom:`Andrew`, quoi:`Veilleur`,
  quand:`Depuis la première page`,
  texte:`Cinquante-deux ans, dix ans de service. Il tient les cérémonies : il prépare la salle, relève l'âge, demande son nom à celui qui sort et l'inscrit. **Il compte sans avoir décidé de compter** — les chaises, les pas, les éléments sur une table. Depuis la cérémonie du premier matin, il retourne voir le garçon sans que personne le lui ait demandé.` },

{ rang:`Au centre`, nom:`Eliott`, quoi:`Arrivant`,
  quand:`Depuis la première page`,
  texte:`Dix ans. Il sort d'une capsule au matin du prologue et **il se nomme lui-même**, comme on le demande à tous ceux qui ont plus de huit ans. Il vit chez June, il porte le courrier d'un quartier, et il dit des choses que personne ne croit.` },

{ rang:`Au centre`, nom:`Isaac`, quoi:`?`, verrou:true,
  quand:`Pas encore rencontré`,
  texte:`Son nom n'a pas encore été prononcé devant vous.` },

{ rang:`Autour`, nom:`June`, quoi:`Berceuse`,
  quand:`Chapitres deuxième et troisième`,
  texte:`Elle a le visage d'une jeune femme au début de la vingtaine, et trois arrivants sous son toit. Elle les prend à quatorze ans, les accompagne des années, puis les mène à la grille du jardin et passe la main. **Elle a choisi ce métier.** Avec Eliott, pour la première fois, elle n'y arrive pas.` },

{ rang:`Autour`, nom:`Julie`, quoi:`Chez June`,
  quand:`Chapitres deuxième et troisième`,
  texte:`Dix ans, le même âge qu'Eliott, et **vingt-cinq ans de couture derrière elle** — un grand magasin de vêtements, en ville. Elle a repris toutes ses affaires sans qu'on le lui demande. Protectrice, et jamais démonstrative.` },

{ rang:`Autour`, nom:`Paul`, quoi:`Chez June`,
  quand:`Chapitre deuxième`,
  texte:`Huit ans. **Il entre au jardin dans quelques semaines** et il compte les jours à l'envers depuis un mois. Il aime les livres et il essaie d'en parler à quelqu'un qui commence à peine à lire.` },

{ rang:`En passant`, nom:`Nora`, quoi:`Veilleuse`,
  quand:`Prologue`,
  texte:`Elle entre la dernière, en nouant ses manches, et prend le second poste. *« Alors c'est un bon jour. »* **Deux capsules, deux veilleurs** : à partir de là, chacun a le sien.` },

{ rang:`En passant`, nom:`Bastien`, quoi:`Préparateur`,
  quand:`Chapitre premier`,
  texte:`Il vient de la coulée et ça se voit — manches roulées, avant-bras verts jusqu'au coude. **Nouveau dans le métier**, et il a trouvé quelque chose qui n'était pas là la veille.` },

{ rang:`En passant`, nom:`Vera`, quoi:`Analyste`,
  quand:`Chapitre premier`,
  texte:`C'est elle qui donne les dates, et **elle ne les donne pas avant d'être sûre**. *« Deux jours. Avant ça, je ne dirai rien. »* Quand elle tranche, personne ne discute — et ce n'est pas une affaire de grade.` }
];
"""


# =====================================================================
#  LE SOMMAIRE — la forme du livre, et rien de plus
# =====================================================================
# Par defaut le sommaire prend la premiere phrase du chapitre. Quand celle-ci
# ne suffit pas -- parce qu'elle est coupee en deux paragraphes, ou parce
# qu'elle ouvre sur une description -- on choisit la phrase ici. Elle doit
# exister mot pour mot dans le texte.
ACCROCHES = {
    'chapitre-1': u"Quatre cent trente-huit. C'était le nombre de pas qui "
                  u"séparaient sa porte de celle de la ruche.",
    'chapitre-5': u"On n'entrait pas là par hasard.",
}


def batir_sommaire(textes):
    """Le sommaire se deduit des chapitres lus : il ne peut plus se perimer."""
    B = chr(96)
    lignes = []
    for t in textes:
        if t['clef']:
            continue
        mot = ACCROCHES.get(t['id'], u'')
        if mot:
            plat = u' '.join(re.sub(r'<[^>]+>', u'', x[1]) for x in t['p'])
            assert mot.split(u'. ')[-1] in plat, \
                u'accroche introuvable dans ' + t['id']
        else:
            for genre, txt in t['p']:
                if genre == 'p':
                    mot = re.sub(r'<[^>]+>', u'', txt)
                    break
        assert mot, u'pas de premiere phrase pour ' + t['id']
        lignes.append(u'{ etat:%slu%s, rang:%s%s%s, note:%s%s,' % (B, B, B, t['rang'], B, B, B)
                      + u'\n  mot:%s%s%s }' % (B, mot, B))
    lignes.append(u'{ etat:%svient%s, rang:%sLa suite%s, note:%sen cours d\'écriture%s,' % (B, B, B, B, B, B)
                  + u'\n  mot:%s%s }' % (B, B))
    for t in textes:
        if t['clef']:
            lignes.append(u'{ etat:%sclef%s, rang:%s%s%s, note:%sécrit, et gardé pour la fin%s,'
                          % (B, B, B, t['rang'], B, B, B)
                          + u'\n  mot:%s%s }' % (B, B))
    return u'const SOMMAIRE = [\n' + u',\n'.join(lignes) + u'\n];\n'


SOMMAIRE = batir_sommaire(textes)
print(u'sommaire : %d entrees' % SOMMAIRE.count(u'etat:'))


# =====================================================================
#  LE LIAGE, puis le rendu des textes
# =====================================================================
poses = lier(textes)
TEXTES = (u'const TEXTES = [\n'
          + u',\n'.join(
              u'{ id:%s%s%s, rang:%s%s%s, titre:%s%s%s, clef:%s, p:[\n%s\n]}'
              % (B, t['id'], B, B, t['rang'], B, B, t['titre'], B,
                 u'true' if t['clef'] else u'false',
                 u',\n'.join(u'[%s%s%s,%s%s%s]' % (B, k, B, B, x, B) for k, x in t['p']))
              for t in textes)
          + u'\n];\n')


# =====================================================================
#  LE CORPS
# =====================================================================
corps4 = lire('p4-corps.html')
RUCHE_BTN = entre(corps4, u'<!--<<ruche-bouton>>-->', u'<!--<<fin ruche-bouton>>-->')
JARDIN_BTN = entre(corps4, u'<!--<<jardin-bouton>>-->', u'<!--<<fin jardin-bouton>>-->')
RUCHE_VUE = entre(corps4, u'<!--<<ruche-vue>>-->', u'<!--<<fin ruche-vue>>-->')
JARDIN_VUE = entre(corps4, u'<!--<<jardin-vue>>-->', u'<!--<<fin jardin-vue>>-->')

# Le plan reste dessous, et on pose un verrou par-dessus.
VERROU = u"""
      <div class="verrou">
        <div class="verrou-carte">
          <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10.5" width="14" height="9.5" rx="2"/><path d="M8.2 10.5V7.8a3.8 3.8 0 0 1 7.6 0v2.7"/></svg>
          <p>Non disponible.</p>
          <p class="verrou-sous">Vous devez avancer dans l'histoire pour déverrouiller ce nouveau lieu.</p>
        </div>
      </div>
"""
JARDIN_VUE = JARDIN_VUE.replace(u'</section>', VERROU + u'    </section>', 1)

CORPS = u"""<body>
<div id="app">

  <nav class="rail" aria-label="Écrans">
    <span class="sigle">L'Éclaircie</span>

    <button class="rail-btn on" data-vue="sommaire" aria-label="Le sommaire">
      <svg viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h10"/></svg><span>Sommaire</span>
    </button>
    <button class="rail-btn" data-vue="textes" aria-label="Les chapitres">
      <svg viewBox="0 0 24 24"><path d="M4 4.5h7a2 2 0 0 1 2 2V20a2 2 0 0 0-2-2H4zM20 4.5h-7a2 2 0 0 0-2 2V20a2 2 0 0 1 2-2h7z"/></svg><span>Chapitres</span>
    </button>
    <button class="rail-btn" data-vue="gens" aria-label="Les personnages">
      <svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.2"/><path d="M3.5 19c0-3 2.5-5 5.5-5s5.5 2 5.5 5"/><circle cx="17.5" cy="9" r="2.4"/><path d="M15 15.5c2.6-.6 5.5.9 5.5 3.5"/></svg><span>Personnages</span>
    </button>
    <button class="rail-btn" data-vue="mots" aria-label="Le glossaire">
      <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c4 4.5 4 12.5 0 17M12 3.5c-4 4.5-4 12.5 0 17"/></svg><span>Glossaire</span>
    </button>
%s
%s
    <div class="bas">
      <button class="rail-btn" id="btn-theme" aria-label="Changer de thème">
        <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.4M12 19.6V22M2 12h2.4M19.6 12H22M4.9 4.9l1.7 1.7M17.4 17.4l1.7 1.7M19.1 4.9l-1.7 1.7M6.6 17.4l-1.7 1.7"/></svg><span>Thème</span>
      </button>
    </div>
  </nav>

  <main class="vues">

    <section class="vue on" id="v-sommaire">
      <header class="chapeau">
        <h1>L'Éclaircie</h1>
        <p class="sous">Un roman en cours d'écriture. <strong>Ce qui se lit ici est écrit ; le reste ne l'est pas encore.</strong></p>
      </header>
      <div class="corps"><div class="mise"><div id="s-liste"></div></div></div>
    </section>

    <section class="vue" id="v-textes">
      <header class="chapeau">
        <h1>Les chapitres</h1>
        <p class="sous">Le texte, tel qu'il est aujourd'hui.</p>
        <div class="outils" id="x-choix"></div>
      </header>
      <div class="corps"><div class="lecture" id="x-corps"></div></div>
    </section>

    <section class="vue" id="v-gens">
      <header class="chapeau">
        <h1>Les personnages</h1>
        <p class="sous">Ceux que tu as déjà croisés, et rien de ce qu'ils feront ensuite.</p>
      </header>
      <div class="corps"><div class="mise"><div id="g-liste"></div></div></div>
    </section>

    <section class="vue" id="v-mots">
      <header class="chapeau">
        <h1>Le glossaire</h1>
        <p class="sous">La page de fin de volume. <strong>Rien n'y raconte le livre</strong> — on vient y chercher un mot, on repart.</p>
        <p class="avis">⚠️ <strong>Il s'écrit en même temps que le roman.</strong> Les définitions bougent encore : à ne pas prendre au pied de la lettre en l'état.</p>
        <input class="cherche" id="m-cherche" placeholder="chercher un mot…" autocomplete="off">
      </header>
      <div class="corps"><div class="mise"><dl class="lexique" id="m-liste"></dl></div></div>
    </section>
%s
%s
  </main>
</div>

<div class="souffleur" id="souffleur"></div>

<div class="voile" id="voile" hidden>
  <form class="coffre" id="coffre">
    <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10.5" width="14" height="9.5" rx="2"/><path d="M8.2 10.5V7.8a3.8 3.8 0 0 1 7.6 0v2.7"/></svg>
    <h2>L'épilogue est fermé</h2>
    <p>Il est écrit, et il se lit en dernier. Si on t'a donné son nom, tu peux entrer.</p>
    <input id="c-mot" type="password" autocomplete="off" placeholder="son nom" aria-label="son nom">
    <div class="coffre-btn">
      <button type="button" class="puce" id="c-non">plus tard</button>
      <button type="submit" class="puce on">entrer</button>
    </div>
    <p class="coffre-err" id="c-err" hidden>Ce n'est pas lui.</p>
  </form>
</div>
""" % (RUCHE_BTN, JARDIN_BTN, RUCHE_VUE, JARDIN_VUE)


# =====================================================================
#  L'APPLICATION
# =====================================================================
APP = u"""<script>
const $  = (s, r) => (r || document).querySelector(s);
const $$ = (s, r) => [...(r || document).querySelectorAll(s)];
const esc = t => String(t).replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const rich = t => esc(t)
  .replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')
  .replace(/\\*(.+?)\\*/g, '<em>$1</em>');

/* l'epilogue est ferme tant qu'on n'a pas donne le mot ; le sommaire
   le lit des son premier rendu, donc l'etat vient avant tout. */
let ouvert = false;

let souffle;
function souffler(t){
  const s = $('#souffleur'); s.textContent = t; s.classList.add('on');
  clearTimeout(souffle); souffle = setTimeout(() => s.classList.remove('on'), 4200);
}

/* ---------- le rail ---------- */
$$('.rail-btn[data-vue]').forEach(b => b.addEventListener('click', () => {
  $$('.rail-btn[data-vue]').forEach(x => x.classList.remove('on'));
  b.classList.add('on');
  $$('.vue').forEach(v => v.classList.remove('on'));
  const v = $('#v-' + b.dataset.vue); if (v) v.classList.add('on');
}));

/* ---------- le thème ---------- */
const btnT = $('#btn-theme');
if (btnT) btnT.addEventListener('click', () => {
  document.body.classList.toggle('clair');
  souffler(document.body.classList.contains('clair') ? 'Thème clair.' : 'Thème sombre.');
});

/* ---------- le sommaire ---------- */
function rendreSommaire(){
$('#s-liste').innerHTML = `<div class="frise-h"><ol>` + SOMMAIRE.map(s => {
  const dedans = `
      <span class="jalon-point" aria-hidden="true"></span>
      <span class="jalon-rang">${esc(s.rang)}</span>
      ${s.note ? `<span class="jalon-note">${esc(s.note)}</span>` : ``}
      ${s.mot ? `<span class="jalon-mot">${esc(s.mot)}</span>` : ``}
      ${s.etat === 'lu' || (s.etat === 'clef' && ouvert)
          ? `<span class="jalon-lire">lire<svg viewBox="0 0 24 24"><path d="M5 12h13M12.5 6l6 6-6 6"/></svg></span>`
          : s.etat === 'clef'
            ? `<span class="jalon-lire">son nom<svg viewBox="0 0 24 24"><rect x="5" y="10.5" width="14" height="9.5" rx="2"/><path d="M8.2 10.5V7.8a3.8 3.8 0 0 1 7.6 0v2.7"/></svg></span>`
            : ``}`;
  const cliquable = s.etat === 'lu' || (s.etat === 'clef' && TEXTES.some(t => t.rang === s.rang));
  return `<li class="jalon ${s.etat === 'clef' && ouvert ? 'lu' : s.etat}">` +
    (cliquable
      ? `<button class="jalon-bloc" data-rang="${esc(s.rang)}">${dedans}</button>`
      : `<div class="jalon-bloc">${dedans}</div>`) +
  `</li>`;
}).join('') + `</ol></div>`;

$$('#s-liste .jalon-bloc[data-rang]').forEach(b => b.addEventListener('click', () => {
  const i = TEXTES.findIndex(t => t.rang === b.dataset.rang);
  if (i < 0) return;
  const aller = () => {
    $('.rail-btn[data-vue="textes"]').click();
    xSel = i; majChoix(); rendreTextes();
  };
  if (TEXTES[i].clef && !ouvert) { demanderLeMot(aller); return; }
  aller();
}));
}
rendreSommaire();

/* ---------- le coffre ----------
   Le mot n'est ecrit nulle part : la page refait le meme calcul sur
   ce qu'on tape et compare deux nombres. */
const plat = t => t.normalize('NFD').replace(/[\u0300-\u036f]/g, '')
                   .toLowerCase().replace(/[^a-z0-9]/g, '');
function empreinte(t){
  let h = 0x811c9dc5;
  for (const c of plat(t)) { h ^= c.charCodeAt(0); h = Math.imul(h, 0x01000193) >>> 0; }
  return h;
}

let apresCoffre = null;
function demanderLeMot(suite){
  apresCoffre = suite;
  $('#c-err').hidden = true;
  $('#c-mot').value = '';
  $('#voile').hidden = false;
  setTimeout(() => $('#c-mot').focus(), 40);
}
function fermerCoffre(){ $('#voile').hidden = true; apresCoffre = null; }
$('#c-non').addEventListener('click', fermerCoffre);
$('#voile').addEventListener('click', e => { if (e.target.id === 'voile') fermerCoffre(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('#voile').hidden) fermerCoffre(); });
$('#coffre').addEventListener('submit', e => {
  e.preventDefault();
  if (empreinte($('#c-mot').value) !== CLEF) {
    $('#c-err').hidden = false;
    $('#c-mot').select();
    return;
  }
  ouvert = true;
  document.body.classList.add('ouvert');
  const suite = apresCoffre;      /* avant de fermer : fermerCoffre l'efface */
  fermerCoffre();
  souffler('L\u2019\u00e9pilogue est ouvert.');
  majChoix();
  rendreSommaire();
  if (suite) suite();
});

/* ---------- les chapitres ---------- */
let xSel = 0;
const boxChoix = $('#x-choix');
TEXTES.forEach((t, i) => {
  const b = document.createElement('button');
  b.className = 'puce' + (i === 0 ? ' on' : '') + (t.clef ? ' a-clef' : '');
  b.innerHTML = esc(t.rang) + (t.clef
    ? ` <svg class="cadenas" viewBox="0 0 24 24"><rect x="5" y="10.5" width="14" height="9.5" rx="2"/><path d="M8.2 10.5V7.8a3.8 3.8 0 0 1 7.6 0v2.7"/></svg>`
    : ``);
  b.addEventListener('click', () => {
    if (t.clef && !ouvert) { demanderLeMot(() => { xSel = i; majChoix(); rendreTextes(); }); return; }
    xSel = i; majChoix(); rendreTextes();
  });
  boxChoix.appendChild(b);
});
function majChoix(){
  $$('#x-choix .puce').forEach((x, i) => {
    x.classList.toggle('on', i === xSel);
    if (ouvert) x.classList.remove('a-clef');
  });
}
function rendreTextes(){
  const t = TEXTES[xSel]; if (!t) return;
  $('#x-corps').innerHTML =
    `<article class="page">
       <h2>${esc(t.rang)}</h2>
       <div class="txt">` +
       t.p.map(([k, s]) => `<p class="${k === 'p' ? '' : k}">${s}</p>`).join('') +
     `</div></article>`;
  $('#x-corps').scrollTop = 0;
}
rendreTextes();

/* ---------- les personnages, par rangs ---------- */
const RANGS = [...new Set(GENS.map(g => g.rang))];
$('#g-liste').innerHTML = RANGS.map(r => `
  <section class="rang-bloc">
    <h2 class="rang-titre">${esc(r)}</h2>
    <div class="grille deux">` +
    GENS.filter(g => g.rang === r).map(g => `
      <article class="carte${g.verrou ? ' scelle' : ''}">
        <h3>${esc(g.nom)}</h3>
        <div class="role">${esc(g.quoi)} · <span class="ou">${esc(g.quand)}</span></div>
        <p>${rich(g.texte)}</p>
      </article>`).join('') +
    `</div>
  </section>`).join('');

/* ---------- un renvoi mene au mot ---------- */
document.addEventListener('click', e => {
  const a = e.target.closest && e.target.closest('.glo');
  if (!a) return;
  e.preventDefault();
  $('.rail-btn[data-vue="mots"]').click();
  const f = a.dataset.mot;
  /* on montre le glossaire entier et on vise l'entree : le lecteur
     garde ce qu'il y a autour, et il peut lire plus loin s'il veut. */
  $('#m-cherche').value = '';
  rendreMots('');
  const i = MOTS.findIndex(([m]) => m === f);
  const el = $$('#m-liste .mot-l')[i];
  if (el) {
    el.classList.add('vise');
    el.scrollIntoView({ block: 'center', behavior: 'smooth' });
    setTimeout(() => el.classList.remove('vise'), 2800);
  }
});

/* ---------- le glossaire ---------- */
function rendreMots(f){
  const l = MOTS.filter(([m, d]) => !f || (m + ' ' + d).toLowerCase().includes(f));
  $('#m-liste').innerHTML = l.map(([m, d]) =>
    `<div class="mot-l"><dt><b>${esc(m)}</b></dt><dd>${rich(d)}</dd></div>`).join('')
    || `<div class="vide">aucun mot</div>`;
}
rendreMots('');
$('#m-cherche').addEventListener('input', e => rendreMots(e.target.value.toLowerCase().trim()));

setTimeout(() => souffler('Bonne lecture. Le glossaire est l\\u00e0 si un mot te manque.'), 900);
</script>
</body></html>
"""


STYLE_SUP = u"""<style>
/* ---------- l'atelier de lecture ---------- */
.lecture{grid-template-columns:minmax(0,1fr);max-width:820px}
/* le rang tient lieu de titre, et il lui faut la place que prenait la dedicace */
.page h2{margin:0 0 32px;padding-bottom:24px;border-bottom:1px solid var(--trait)}
.page .txt{max-width:none}
.page{padding:44px 52px 56px}
@media (max-width:640px){.page{padding:28px 22px 34px}}
.rang-s{
  font-family:var(--sans);font-size:11px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--texte-3);margin-bottom:6px
}
/* ---------- le coffre de l'epilogue ---------- */
.puce.a-clef{opacity:.62}
.puce .cadenas{
  width:11px;height:11px;fill:none;stroke:currentColor;stroke-width:1.7;
  stroke-linecap:round;stroke-linejoin:round;vertical-align:-1px;margin-left:2px
}
body.ouvert .puce .cadenas{display:none}
.jalon.clef{opacity:.72;width:186px}
.jalon.clef .jalon-point{background:var(--fond);border:1px solid var(--andrew)}
.jalon.clef .jalon-rang{color:var(--texte-2);font-size:16px}
.jalon.clef .jalon-bloc{cursor:pointer}
.jalon.clef .jalon-bloc:hover .jalon-lire{opacity:1}
.voile{
  position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;
  background:color-mix(in srgb,#000 62%,transparent);
  backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);padding:20px
}
.voile[hidden]{display:none}
.coffre{
  width:100%;max-width:370px;text-align:center;padding:30px 30px 26px;
  background:var(--fond-2);border:1px solid var(--trait);border-radius:14px;
  box-shadow:0 24px 60px -20px rgba(0,0,0,.7)
}
.coffre > svg{
  width:26px;height:26px;fill:none;stroke:var(--andrew);stroke-width:1.6;
  stroke-linecap:round;stroke-linejoin:round;margin-bottom:14px
}
.coffre h2{
  margin:0 0 9px;font-family:var(--serif);font-weight:400;font-size:21px;color:var(--texte)
}
.coffre p{
  margin:0 0 18px;font-family:var(--sans);font-size:13px;line-height:1.55;color:var(--texte-2)
}
.coffre input{
  width:100%;padding:10px 13px;border-radius:8px;text-align:center;
  background:var(--fond);border:1px solid var(--trait);color:var(--texte);
  font-family:var(--sans);font-size:15px;letter-spacing:.22em
}
.coffre input:focus{outline:none;border-color:var(--andrew)}
.coffre-btn{display:flex;gap:9px;justify-content:center;margin-top:16px}
.coffre-err{
  margin:14px 0 0;color:var(--alerte);font-size:12.5px;letter-spacing:.02em
}
.coffre-err[hidden]{display:none}

/* ---------- les renvois vers le glossaire ---------- */
.mot-l{border-radius:7px;transition:background .3s}
.mot-l.vise{
  background:color-mix(in srgb,var(--andrew) 13%,transparent);
  box-shadow:0 0 0 9px color-mix(in srgb,var(--andrew) 13%,transparent)
}
.glo{
  color:inherit;text-decoration:none;cursor:pointer;
  border-bottom:1px dotted color-mix(in srgb,var(--andrew) 52%,transparent);
  transition:color .14s,border-color .14s
}
.glo:hover{color:var(--andrew);border-bottom-color:var(--andrew)}
.glo:focus-visible{outline:1px solid var(--andrew);outline-offset:2px}

/* ---------- la frise du sommaire ---------- */
.frise-h{overflow-x:auto;overscroll-behavior-x:contain;padding:2px 0 10px}
.frise-h ol{
  position:relative;display:flex;align-items:stretch;gap:14px;
  list-style:none;margin:0;padding:0 2px 2px;width:max-content
}
.frise-h ol::before{
  content:"";position:absolute;left:8px;right:8px;top:5px;height:1px;
  background:linear-gradient(90deg,var(--andrew) 0%,var(--andrew) 46%,var(--trait) 76%,transparent 100%)
}
.jalon{position:relative;flex:none;width:206px;display:flex}
.jalon-bloc{
  display:flex;flex-direction:column;width:100%;text-align:left;
  background:none;border:0;color:inherit;font:inherit;padding:0;
  border-radius:11px;transition:background .16s
}
.jalon-point{
  display:block;width:11px;height:11px;border-radius:50%;flex:none;
  background:var(--andrew);box-shadow:0 0 0 5px var(--fond);margin:0 0 20px 3px;
  transition:transform .16s
}
.jalon.vient .jalon-point,.jalon.loin .jalon-point{
  background:var(--fond);border:1px solid var(--trait);box-shadow:0 0 0 5px var(--fond)
}
.jalon-rang{
  display:block;font-family:var(--serif);font-size:19px;font-weight:400;
  color:var(--texte);letter-spacing:.01em;padding:0 14px
}
.jalon-note{
  display:block;font-family:var(--sans);font-size:10.5px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--texte-3);margin-top:6px;padding:0 14px
}
.jalon-mot{
  display:block;font-family:var(--serif);font-size:14px;line-height:1.6;
  color:var(--texte-2);font-style:italic;margin-top:9px;padding:0 14px
}
.jalon-lire{
  display:inline-flex;align-items:center;gap:6px;margin:auto 0 0;padding:16px 14px 0;
  font-family:var(--sans);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--andrew);opacity:.7;transition:.16s
}
.jalon-lire svg{
  width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:2;
  stroke-linecap:round;stroke-linejoin:round;transition:transform .16s
}
.jalon.lu .jalon-bloc{cursor:pointer}
.jalon.lu .jalon-bloc:hover .jalon-point{transform:scale(1.3)}
.jalon.lu .jalon-bloc:hover .jalon-rang{color:var(--texte)}
.jalon.lu .jalon-bloc:hover .jalon-lire{opacity:1}
.jalon.lu .jalon-bloc:hover .jalon-lire svg{transform:translateX(3px)}
.jalon.lu .jalon-bloc:focus-visible{outline:1px solid var(--andrew);outline-offset:3px}
.jalon.vient .jalon-rang,.jalon.loin .jalon-rang{color:var(--texte-2);font-size:16px}
.jalon.vient,.jalon.loin{opacity:.6;width:152px}
@media (max-width:640px){.jalon{width:200px}}
/* la frise se pose au milieu de la page, pas en haut */
#v-sommaire .corps{display:flex;align-items:center}
#v-sommaire .mise{width:100%}
#g-liste .role{
  font-family:var(--sans);font-size:12px;letter-spacing:.06em;color:var(--andrew);
  margin:0 0 10px
}
#g-liste .role .ou{color:var(--texte-3);letter-spacing:0}
#g-liste .carte p{font-size:14.5px;line-height:1.62;color:var(--texte-2);margin:0}
.rang-bloc{margin:0 0 34px}
.rang-titre{
  font-family:var(--sans);font-size:11px;font-weight:600;letter-spacing:.18em;
  text-transform:uppercase;color:var(--texte-3);margin:0 0 14px
}
#g-liste .carte.scelle{opacity:.42}
#g-liste .carte.scelle .role{color:var(--texte-3)}
.avis{
  font-family:var(--sans);font-size:12.5px;line-height:1.55;color:var(--texte-2);
  background:var(--fond-2);border:1px solid var(--trait);border-radius:8px;
  padding:9px 13px;margin:12px 0 0;max-width:62ch
}
#v-jardin{position:relative}
#v-jardin .verrou{
  position:absolute;inset:0;z-index:40;display:flex;align-items:center;justify-content:center;
  background:color-mix(in srgb, var(--fond) 88%, transparent);
  backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px)
}
#v-jardin .verrou-carte{
  text-align:center;max-width:340px;padding:26px 30px;
  background:var(--fond-2);border:1px solid var(--trait);border-radius:12px
}
#v-jardin .verrou-carte svg{
  width:26px;height:26px;fill:none;stroke:var(--andrew);stroke-width:1.6;
  stroke-linecap:round;stroke-linejoin:round;margin-bottom:12px
}
#v-jardin .verrou-carte p{
  font-family:var(--sans);font-size:14px;color:var(--texte);margin:0;font-weight:600
}
#v-jardin .verrou-carte .verrou-sous{
  font-weight:400;font-size:12.5px;color:var(--texte-2);margin-top:8px;line-height:1.5
}
</style>
"""

def sans_nom(css):
    """Le nom de la seconde voie ne traine pas dans les styles repris.

    L'atelier nomme ses couleurs par personnage. Ici ces noms ne
    servent a rien, et l'un d'eux dit quelque chose : on le remplace.
    """
    return css.replace(u'joel', u'v2')


page = (sans_nom(lire('p1-style.html') + lire('p2-style.html') + lire('p3-style.html'))
        + STYLE_SUP + CORPS
        + u'<script>\nconst CLEF = %d;\n' % CLEF + TEXTES + u'\n' + MOTS + u'\n'
        + GENS + u'\n' + SOMMAIRE + u'</script>\n'
        + u'<script>\n' + sans_scelle(lire('pC-ruche.js')) + u'\n</script>\n'
        + u'<script>\n' + lire('pD-jardin.js') + u'\n</script>\n'
        + APP)

SORTIE = os.path.join(ICI, '..', 'lecture.html')
open(SORTIE, 'wb').write(page.encode('utf-8'))

# --------- le controle qui compte : rien de l'autrice n'a fui ---------
INTERDITS = [u'const NOTES', u'const SCENES', u'const REGLES', u'const INTERDITS',
             u'const BIBLE', u'const QUESTIONS', u'const DISPOSITIF', u'const RACCORDS',
             u'faille:', u'gardes:', u'arc:', u'Joël', u'ravisseuse', u'reliquat',
             u'agonie', u'cite scelle', u'Joel', u'JOEL', u'joel']
def present(mot, texte):
    """Un mot entier, pas un morceau : --joel n'est pas Joel."""
    return re.search(u'(?<![\\w-])' + re.escape(mot) + u'(?![\\w-])', texte) is not None


fuites = [m for m in INTERDITS if present(m, page)]
if fuites:
    raise SystemExit(u'FUITE dans lecture.html : ' + u', '.join(fuites))

print(u'lecture.html : %d chapitres, %d mots de glossaire, %d personnages, %d ko'
      % (len(textes), len(mots), page.count(u', nom:`'), len(page.encode('utf-8')) // 1024))
print(u'%d renvois poses : %s' % (len(poses), u', '.join(poses)))
print(u'aucune matiere d\'autrice dans le fichier')
