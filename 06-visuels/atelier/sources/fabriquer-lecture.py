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

ICI = os.path.dirname(os.path.abspath(__file__))


def lire(nom):
    return io.open(os.path.join(ICI, nom), encoding='utf-8').read()


def entre(s, a, b):
    return s[s.index(a) + len(a):s.index(b)]


B = u'`'


# =====================================================================
#  LES TEXTES — le prologue et le chapitre premier, sans leur appareil
# =====================================================================
js = lire('pB-textes.js')
bornes = [(m.group(1), m.start()) for m in re.finditer(r'\n  id: `([a-z0-9-]+)`,', js)]

LISIBLES = ['prologue', 'chapitre-1', 'chapitre-2', 'chapitre-3']
textes = []
for ident in LISIBLES:
    n = [i for i, (x, _) in enumerate(bornes) if x == ident][0]
    deb = bornes[n][1]
    fin = bornes[n + 1][1] if n + 1 < len(bornes) else len(js)
    bloc = js[deb:fin]
    rang = re.search(r'rang: `([^`]*)`', bloc).group(1)
    titre = re.search(r'titre: `([^`]*)`', bloc).group(1)
    paras = re.findall(r'\[`(p|tiret|pause)`,`([^`]*)`', bloc)
    corps = u',\n'.join(u'[%s%s%s,%s%s%s]' % (B, k, B, B, t, B) for k, t in paras)
    textes.append(u'{ id:%s%s%s, rang:%s%s%s, titre:%s%s%s, p:[\n%s\n]}'
                  % (B, ident, B, B, rang, B, B, titre, B, corps))
TEXTES = u'const TEXTES = [\n' + u',\n'.join(textes) + u'\n];\n'


# =====================================================================
#  LE GLOSSAIRE — les mots du monde, sans source ni question ouverte
# =====================================================================
monde = lire('p7-monde.js')
bloc = entre(monde, u'const GLOSSAIRE = [', u'\n];')
mots = re.findall(r'\[`([^`]*)`,`([^`]*)`,`[^`]*`,`[^`]*`\],', bloc)
assert len(mots) > 25, u'%d mots' % len(mots)
MOTS = (u'const MOTS = [\n'
        + u'\n'.join(u'[%s%s%s,%s%s%s],' % (B, m, B, B, d, B) for m, d in mots)
        + u'\n];\n')


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
  texte:`Dix ans, le même âge qu'Eliott, et **onze ans de couture derrière elle** — un grand magasin de vêtements, en ville. Elle a repris toutes ses affaires sans qu'on le lui demande. Protectrice, et jamais démonstrative.` },

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
SOMMAIRE = u"""const SOMMAIRE = [
{ etat:`lu`, rang:`Prologue`, note:``,
  mot:`Deux capsules étaient venues pendant la nuit, et personne ne savait qui allait en sortir.` },
{ etat:`lu`, rang:`Chapitre premier`, note:``,
  mot:`Quatre cent trente-huit. C'était le nombre de pas qui séparaient sa porte de celle de la ruche.` },
{ etat:`lu`, rang:`Chapitre deuxième`, note:``,
  mot:`Il n'avait rien écrit dans la case.` },
{ etat:`lu`, rang:`Chapitre troisième`, note:``,
  mot:`Il y retourna le mardi suivant, et le mardi d'après.` },
{ etat:`vient`, rang:`La suite`, note:`en cours d'écriture`,
  mot:`` },
{ etat:`loin`, rang:`Épilogue`, note:`écrit, et gardé pour la fin`,
  mot:`` }
];
"""


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
$('#s-liste').innerHTML = SOMMAIRE.map(s => `
  <article class="carte ${s.etat}">
    <h3>${esc(s.rang)}</h3>
    ${s.note ? `<div class="rang-s">${esc(s.note)}</div>` : ``}
    ${s.mot ? `<p class="incipit">${esc(s.mot)}</p>` : ``}
    ${s.etat === 'lu' ? `<button class="puce lire" data-rang="${esc(s.rang)}">lire</button>` : ``}
  </article>`).join('');

$$('#s-liste .lire').forEach(b => b.addEventListener('click', () => {
  const i = TEXTES.findIndex(t => t.rang === b.dataset.rang);
  $('.rail-btn[data-vue="textes"]').click();
  if (i >= 0) { xSel = i; majChoix(); rendreTextes(); }
}));

/* ---------- les chapitres ---------- */
let xSel = 0;
const boxChoix = $('#x-choix');
TEXTES.forEach((t, i) => {
  const b = document.createElement('button');
  b.className = 'puce' + (i === 0 ? ' on' : '');
  b.textContent = t.rang;
  b.addEventListener('click', () => { xSel = i; majChoix(); rendreTextes(); });
  boxChoix.appendChild(b);
});
function majChoix(){
  $$('#x-choix .puce').forEach((x, i) => x.classList.toggle('on', i === xSel));
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
.page .txt{max-width:none}
.page{padding:44px 52px 56px}
@media (max-width:640px){.page{padding:28px 22px 34px}}
.rang-s{
  font-family:var(--sans);font-size:11px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--texte-3);margin-bottom:6px
}
#s-liste{display:grid;gap:14px;max-width:760px}
#s-liste .carte h3{margin:0 0 8px;font-family:var(--serif);font-weight:400;font-size:21px}
#s-liste .incipit{
  font-family:var(--serif);font-size:15px;line-height:1.6;color:var(--texte-2);
  font-style:italic;margin:0 0 14px;max-width:60ch
}
#s-liste .carte.vient,#s-liste .carte.loin{opacity:.5}
#s-liste .carte.loin h3,#s-liste .carte.vient h3{color:var(--texte-2)}
#g-liste .role{
  font-family:var(--sans);font-size:12px;letter-spacing:.06em;color:var(--or);
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
  width:26px;height:26px;fill:none;stroke:var(--or);stroke-width:1.6;
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

page = (lire('p1-style.html') + lire('p2-style.html') + lire('p3-style.html')
        + STYLE_SUP + CORPS
        + u'<script>\n' + TEXTES + u'\n' + MOTS + u'\n' + GENS + u'\n' + SOMMAIRE + u'</script>\n'
        + u'<script>\n' + lire('pC-ruche.js') + u'\n</script>\n'
        + u'<script>\n' + lire('pD-jardin.js') + u'\n</script>\n'
        + APP)

SORTIE = os.path.join(ICI, '..', 'lecture.html')
open(SORTIE, 'wb').write(page.encode('utf-8'))

# --------- le controle qui compte : rien de l'autrice n'a fui ---------
INTERDITS = [u'const NOTES', u'const SCENES', u'const REGLES', u'const INTERDITS',
             u'const BIBLE', u'const QUESTIONS', u'const DISPOSITIF', u'const RACCORDS',
             u'faille:', u'gardes:', u'arc:', u'Joël', u'ravisseuse', u'reliquat']
fuites = [m for m in INTERDITS if m in page]
if fuites:
    raise SystemExit(u'FUITE dans lecture.html : ' + u', '.join(fuites))

print(u'lecture.html : %d chapitres, %d mots de glossaire, %d personnages, %d ko'
      % (len(textes), len(mots), page.count(u', nom:`'), len(page.encode('utf-8')) // 1024))
print(u'aucune matiere d\'autrice dans le fichier')
