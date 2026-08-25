# -*- coding: utf-8 -*-
u"""Le livre : L'Eclaircie en pocket, a lire comme un livre.

Une double page au format poche, la couverture fermee au depart, les
pages qui se tournent, les folios en bas au centre, un chapitre qui
commence toujours sur une belle page.

  python fabriquer-le-livre.py

Sortie : 06-visuels/atelier/le-livre.html   (autonome, aucun appel reseau)

DEUX REGLES DE FABRICATION.

1. Le texte ne bouge pas. On le lit dans pB-textes.js et on n'y ecrit
   jamais. La typographie francaise -- les espaces insecables devant
   ; : ! ? et dans les guillemets -- se pose ICI, au rendu. Trois
   chapitres sont verrouilles par empreinte : y toucher casserait les
   verrous, et surtout ce n'est pas au fabricant de corriger l'autrice.

2. La pagination est calculee dans une geometrie LOGIQUE fixe, puis le
   livre entier est mis a l'echelle de la fenetre. C'est ce qui permet
   d'avoir a la fois un livre qui remplit n'importe quel ecran et des
   numeros de page qui ne bougent jamais. Changer un chiffre de GEO
   change la pagination de tout le livre.
"""
import base64
import io
import os
import re
import unicodedata

ICI = os.path.dirname(os.path.abspath(__file__))
B = u'`'


def lire(nom):
    return io.open(os.path.join(ICI, nom), encoding='utf-8').read()


def entre(s, a, b):
    return s[s.index(a) + len(a):s.index(b)]


# =====================================================================
#  LA GEOMETRIE — logique, fixe, et seule source de verite
#  La feuille est un poche : 110 x 176 mm, soit un rapport de 0,625.
#  La justification tombe sur une grille de 30 lignes exactement.
# =====================================================================
GEO = {
    'PW': 470, 'PH': 752,
    'HAUT': 74, 'BAS': 80, 'DEDANS': 62, 'DEHORS': 48,
    'CORPS': 14.2, 'LIGNE': 23,
}
GEO['TW'] = GEO['PW'] - GEO['DEDANS'] - GEO['DEHORS']      # 364
GEO['TH'] = GEO['PH'] - GEO['HAUT'] - GEO['BAS']           # 612
LIGNES = 26
assert abs(GEO['TH'] / GEO['LIGNE'] - LIGNES) < 1e-9, \
    u'la grille ne tombe pas juste : %s lignes' % (GEO['TH'] / GEO['LIGNE'])
GEO['OUVRE_HAUT'] = GEO['LIGNE'] * 6                        # 6 lignes de blanc
GEO['OUVRE_BAS'] = GEO['LIGNE'] * 3                         # 3 lignes apres le titre
GEO['TITRE_LH'] = GEO['LIGNE'] * 2                          # le titre tient sur 2 lignes


# =====================================================================
#  LES TEXTES
# =====================================================================
js = lire('pB-textes.js')
bornes = [(m.group(1), m.start()) for m in re.finditer(r'\n  id: `([a-z0-9-]+)`,', js)]
# L'epilogue est ecrit, et il ne se lit pas ici : il donne la fin.
LISIBLES = ['prologue', 'chapitre-1', 'chapitre-2', 'chapitre-3',
            'chapitre-4', 'chapitre-5', 'chapitre-6']

def romain(n):
    paires = ((10, u'X'), (9, u'IX'), (5, u'V'), (4, u'IV'), (1, u'I'))
    out = u''
    for val, sig in paires:
        while n >= val:
            out += sig
            n -= val
    return out


textes = []
for ident in LISIBLES:
    n = [i for i, (x, _) in enumerate(bornes) if x == ident][0]
    deb = bornes[n][1]
    fin = bornes[n + 1][1] if n + 1 < len(bornes) else len(js)
    bloc = js[deb:fin]
    textes.append({
        'id': ident,
        # Le manuscrit dit << Chapitre premier >>. Le livre dit << Chapitre I >>,
        # et il ne dit pas << La ceremonie >> : dans un livre, le titre du
        # chapitre annonce ce qui va se passer, et ici ca ne regarde personne.
        'rang': (u'Chapitre ' + romain(int(ident.split('-')[1]))
                 if ident.startswith('chapitre-')
                 else re.search(r'rang: `([^`]*)`', bloc).group(1)),
        'titre': re.search(r'titre: `([^`]*)`', bloc).group(1),
        'p': [list(x) for x in re.findall(r'\[`(p|tiret|pause)`,`([^`]*)`', bloc)],
    })
print(u'%d chapitres, %d paragraphes'
      % (len(textes), sum(len(t['p']) for t in textes)))


# =====================================================================
#  LA TYPOGRAPHIE FRANCAISE — posee au rendu, jamais dans la source
#
#  L'espace fine insecable devant ; ! ? -- l'insecable pleine devant :
#  et dans les guillemets. Sans elles, en texte justifie, un point
#  d'interrogation finit par tomber seul en debut de ligne, et ca se
#  voit tout de suite.
# =====================================================================
FINE = u' '      # espace fine insecable
DURE = u' '      # espace insecable


def typo(t):
    t = re.sub(u'[   ]*([;!?])', FINE + u'\\1', t)
    t = re.sub(u'[   ]*:', DURE + u':', t)
    t = re.sub(u'«[   ]*', u'«' + DURE, t)
    t = re.sub(u'[   ]*»', DURE + u'»', t)
    # le tiret qui ouvre une replique ne se separe pas de son premier mot
    if t.startswith(u'— '):
        t = u'—' + DURE + t[2:]
    return t


poses = 0
for t in textes:
    for para in t['p']:
        if para[0] == 'pause':
            continue
        avant = para[1]
        para[1] = typo(avant)
        poses += sum(para[1].count(c) for c in (FINE, DURE))
print(u'typographie : %d espaces insecables posees au rendu' % poses)


# =====================================================================
#  LE GLOSSAIRE — les mots du monde, et le renvoi sur la premiere
#  occurrence seulement. Jamais sur un mot qui porte une tension du
#  recit : le lecteur n'a pas a se faire expliquer ce qu'il doit
#  comprendre tout seul.
# =====================================================================
monde = lire('p7-monde.js')
bloc = entre(monde, u'const GLOSSAIRE = [', u'\n];')
mots = re.findall(r'\[`([^`]*)`,`([^`]*)`,`[^`]*`,`[^`]*`\],', bloc)
assert len(mots) > 18, u'%d mots seulement' % len(mots)

NE_PAS_LIER = [u'Porteur de voiles', u'Paire', u'Archiviste', u'Section 0']


def formes(entree):
    out = []
    for part in entree.split(u','):
        base = part.split(u'(')[0].strip()
        if not base:
            continue
        out.append(base)
        if not base.endswith(u's'):
            out.append(base + u's')
    return sorted(set(out), key=len, reverse=True)


restants = {m: formes(m) for m, d in mots if m not in NE_PAS_LIER}
lies = []
for t in textes:
    for i, para in enumerate(t['p']):
        for entree in list(restants):
            for f in restants[entree]:
                motif = re.compile(u'\\b(' + re.escape(f) + u')\\b(?![^<]*>)',
                                   re.IGNORECASE)
                m = motif.search(para[1])
                if m:
                    para[1] = (para[1][:m.start(1)]
                               + u'<a class="glo" data-mot="' + entree + u'">'
                               + m.group(1) + u'</a>' + para[1][m.end(1):])
                    lies.append(entree)
                    del restants[entree]
                    break
print(u'glossaire : %d mots sur %d renvoyes une fois'
      % (len(lies), len(mots)))


# =====================================================================
#  LES DRAPEAUX — ce que la mise en page doit savoir de chaque
#  paragraphe. 1 : pas d'alinea (debut de chapitre, ou apres une
#  pause). 2 : premiere ligne en petites capitales.
# =====================================================================
for t in textes:
    precedent = None
    premier = True
    for para in t['p']:
        f = 0
        if para[0] != 'pause' and (precedent is None or precedent == 'pause'):
            f |= 1
        if premier and para[0] != 'pause':
            f |= 2
            premier = False
        para.append(f)
        precedent = para[0]


# =====================================================================
#  LA COUVERTURE — embarquee, pour que le fichier tienne tout seul
# =====================================================================
SOURCE = os.path.join(ICI, '..', '..', '..', 'cover.png')
jpg = os.path.join(ICI, 'couverture.jpg')

# On retaille depuis l'originale des qu'elle bouge : deux couvertures dans
# le depot, c'est une qui finit par dormir pendant que l'autre change.
if os.path.exists(SOURCE) and (not os.path.exists(jpg)
                               or os.path.getmtime(SOURCE) > os.path.getmtime(jpg)):
    try:
        from PIL import Image
        im = Image.open(SOURCE).convert('RGB')
        rapport = float(GEO['PW']) / GEO['PH']
        large = int(round(im.height * rapport))
        bord = (im.width - large) // 2
        im = im.crop((bord, 0, bord + large, im.height))
        im = im.resize((GEO['PW'] * 2, GEO['PH'] * 2), Image.LANCZOS)
        im.save(jpg, quality=80, optimize=True, progressive=True)
        print(u'couverture : retaillee depuis cover.png')
    except ImportError:
        print(u'couverture : cover.png a bouge, mais Pillow manque'
              u' -- on garde la coupe precedente')

if os.path.exists(jpg):
    COUV = (u'data:image/jpeg;base64,'
            + base64.b64encode(open(jpg, 'rb').read()).decode('ascii'))
    print(u'couverture : %.0f ko embarques' % (os.path.getsize(jpg) / 1024.0))
else:
    COUV = u''
    print(u'couverture : ABSENTE (couverture.jpg introuvable) -- fond peint')


# =====================================================================
#  LES DONNEES
# =====================================================================
def echapper(s):
    return s.replace(u'\\', u'\\\\').replace(B, u'\\' + B).replace(u'${', u'\\${')


lignes = []
for t in textes:
    lignes.append(u'{ id:%s%s%s, rang:%s%s%s, titre:%s%s%s, p:['
                  % (B, t['id'], B, B, echapper(t['rang']), B,
                     B, echapper(t['titre']), B))
    for genre, texte, f in t['p']:
        lignes.append(u'[%s%s%s,%s%s%s,%d],' % (B, genre, B, B, echapper(texte), B, f))
    lignes.append(u']},')
def enrichir(d):
    u"""Le gras et l'italique du glossaire sont ecrits en markdown."""
    d = re.sub(u'\\*\\*([^*]+)\\*\\*', u'<strong>\\1</strong>', d)
    d = re.sub(u'(?<!\\*)\\*([^*]+)\\*(?!\\*)', u'<em>\\1</em>', d)
    return typo(d)


DATA = u'const LIVRE = [\n' + u'\n'.join(lignes) + u'\n];\n'
DATA += (u'const PAIRES = [\n'
         + u'\n'.join(u'[%s%s%s,%s%s%s],' % (B, echapper(m), B, B, echapper(enrichir(d)), B)
                      for m, d in mots)
         + u'\n];\nconst MOTS = {};\n'
         + u'PAIRES.forEach(function(x){ MOTS[x[0]] = x[1] });\n')


# =====================================================================
#  LA PAGE
# =====================================================================
GABARIT = r"""<!doctype html>
<html lang="fr" data-nuit="0" data-glo="0" data-ouvert="0">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>L'Éclaircie</title>
<style>
:root{
  --papier:#F3EDE1; --papier-2:#EAE2D2;
  --encre:#201D18; --encre-2:#514A3E; --encre-3:#928975;
  --bureau:#221F1B; --bureau-2:#15130F;
  --gouttiere:.17; --or:#B08B4F; --corne:#D8CDB4; --corne-2:#C6B999;
  --serif:Constantia,"Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --sans:Corbel,Candara,"Segoe UI",Tahoma,sans-serif;
}
html[data-nuit="1"]{
  --papier:#141A21; --papier-2:#0F151B;
  --encre:#DCE3EA; --encre-2:#A2AFBB; --encre-3:#63717F;
  --bureau:#080B0F; --bureau-2:#04060A;
  --gouttiere:.34; --or:#7CC6DC; --corne:#202934; --corne-2:#2C3846;
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0;background:radial-gradient(120% 100% at 50% 0%,var(--bureau),var(--bureau-2));
  color:var(--encre-3);font-family:var(--sans);overflow:hidden;
  -webkit-font-smoothing:antialiased;
}

/* ---------- la scène ---------- */
#scene{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
#cadre{transform-origin:50% 50%;will-change:transform}
#livre{
  position:relative;width:{{SW}}px;height:{{PH}}px;
  perspective:3500px;perspective-origin:50% 48%;
  transform:translateX(-{{DEMI}}px);
  transition:transform 560ms cubic-bezier(.36,.06,.24,1);
}
html[data-ouvert="1"] #livre{transform:translateX(0)}
#ombre{
  position:absolute;left:12px;right:12px;top:16px;bottom:-4px;
  box-shadow:0 44px 90px -26px rgba(0,0,0,.85),0 8px 22px -8px rgba(0,0,0,.6);
  border-radius:3px;
}
html[data-ouvert="0"] #ombre{left:{{PWP12}}px;right:12px}

/* ---------- la tranche : l'épaisseur qui dit où on en est ---------- */
.tranche{
  position:absolute;top:7px;bottom:7px;width:0;pointer-events:none;
  background:
    linear-gradient(90deg,rgba(0,0,0,.30),rgba(0,0,0,0) 45%,rgba(0,0,0,.22)),
    repeating-linear-gradient(90deg,var(--papier-2) 0 1.5px,rgba(90,74,48,.16) 1.5px 3px);
  transition:width 280ms ease;opacity:.9;
}
#trG{right:100%;border-radius:3px 0 0 3px}
#trD{left:100%;border-radius:0 3px 3px 0}
html[data-ouvert="0"] .tranche{width:0!important}

/* ---------- une page ---------- */
.cote{position:absolute;top:0;width:{{PW}}px;height:{{PH}}px}
.cote.g{left:0}
.cote.d{left:{{PW}}px}
.page{
  position:absolute;inset:0;background:var(--papier);color:var(--encre);
  overflow:hidden;
}
.page::after{
  content:"";position:absolute;top:0;bottom:0;width:64px;pointer-events:none;
  opacity:var(--gouttiere);
}
.page[data-cote="g"]::after{right:0;background:linear-gradient(90deg,transparent,rgba(0,0,0,.55))}
.page[data-cote="d"]::after{left:0;background:linear-gradient(270deg,transparent,rgba(0,0,0,.55))}
.page.garde{background:linear-gradient(145deg,#2E2A24,#1A1713)}
html[data-nuit="1"] .page.garde{background:linear-gradient(145deg,#111820,#080C11)}
.page.nulle{background:transparent}
.page.nulle::after{display:none}

.bloc{
  position:absolute;top:{{HAUT}}px;width:{{TW}}px;height:{{TH}}px;
  font:{{CORPS}}px/{{LIGNE}}px var(--serif);
  text-align:justify;text-justify:inter-word;hyphens:auto;-webkit-hyphens:auto;
  letter-spacing:.002em;
}
.page[data-cote="g"] .bloc{left:{{DEHORS}}px}
.page[data-cote="d"] .bloc{left:{{DEDANS}}px}
.bloc p{margin:0;text-indent:1.25em;orphans:2;widows:2}
.bloc p.plat{text-indent:0}
.bloc p.coupe{text-align-last:justify;-moz-text-align-last:justify}
.bloc p.pause{
  text-indent:0;text-align:center;letter-spacing:.5em;color:var(--encre-3);
  margin:{{LIGNE}}px 0;height:{{LIGNE}}px;
}
.bloc em{font-style:italic}
.ouvre{padding:{{OUVRE_HAUT}}px 0 {{OUVRE_BAS}}px;text-align:center}
.ouvre h2{
  margin:0;font:400 17px/{{TITRE_LH}}px var(--serif);color:var(--encre);
  letter-spacing:.26em;text-transform:uppercase;
}
.tete{
  position:absolute;top:34px;width:{{TW}}px;
  font:8.6px/12px var(--sans);letter-spacing:.24em;text-transform:uppercase;
  color:var(--encre-3);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.page[data-cote="g"] .tete{left:{{DEHORS}}px;text-align:left}
.page[data-cote="d"] .tete{left:{{DEDANS}}px;text-align:right}
.folio{
  position:absolute;bottom:36px;left:0;width:100%;text-align:center;
  font:10.5px var(--serif);color:var(--encre-3);letter-spacing:.14em;
}

/* ---------- la page de titre et le sommaire ---------- */
.titrage{position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;text-align:center;padding:0 56px}
.titrage h1{
  margin:0;font:400 34px/1.15 var(--serif);letter-spacing:.14em;
  text-transform:uppercase;color:var(--encre);
}
.titrage .filet{width:64px;height:1px;background:var(--encre-3);margin:26px 0}
.titrage .quoi{font:12px var(--serif);letter-spacing:.34em;text-transform:uppercase;color:var(--encre-3)}
.titrage .bas{position:absolute;bottom:74px;font:9.5px var(--sans);letter-spacing:.2em;
  text-transform:uppercase;color:var(--encre-3)}

.som{position:absolute;top:{{HAUT}}px;width:{{TW}}px;height:{{TH}}px;color:var(--encre)}
.page[data-cote="g"] .som{left:{{DEHORS}}px}
.page[data-cote="d"] .som{left:{{DEDANS}}px}
.som h3{
  margin:0 0 {{OUVRE_BAS}}px;font:400 13px/{{LIGNE}}px var(--serif);
  letter-spacing:.34em;text-transform:uppercase;color:var(--encre-3);text-align:center;
}
.som ul{list-style:none;margin:0;padding:0;font:13.4px/{{DEUX}}px var(--serif)}
.som li{display:flex;align-items:baseline;cursor:default}
.som .fil{
  flex:1;margin:0 .55em;border-bottom:2px dotted var(--encre-3);
  transform:translateY(-.24em);opacity:.95;
}
.som .f{font-variant-numeric:tabular-nums;color:var(--encre-2)}
.som li.ici .n,.som li.ici .f{color:var(--or);font-weight:600}

/* ---------- la couverture ---------- */
#couv,#feuille{
  position:absolute;left:{{PW}}px;top:0;width:{{PW}}px;height:{{PH}}px;
  transform-style:preserve-3d;transform-origin:0 50%;
}
#couv{z-index:9}
#feuille{z-index:8}
.face{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;overflow:hidden}
.face.recto{transform:translateZ(.4px)}
.face.verso{transform:rotateY(180deg) translateZ(.4px)}

/* Les lames : la feuille est courbe parce qu'elle est articulee. */
.lame{position:absolute;top:0;height:{{PH}}px;transform-origin:0 50%;transform-style:preserve-3d}
/* L'ame de la feuille : un fond de papier un peu plus large que la lame.
   Le jour entre deux lames laisse voir cette ame au lieu du bureau, et
   comme c'est une couleur plate, on ne la voit pas. */
.ame{
  position:absolute;left:-1px;right:-1px;top:0;bottom:0;
  background:var(--papier);
}
.lame>.face{left:0;top:0;right:auto;bottom:auto;width:100%;height:100%}
.fen{position:absolute;top:0;width:{{PW}}px;height:{{PH}}px}
/* Les voiles d'ombre sont AU NIVEAU DE LA LAME, devant tout le reste :
   ils couvrent l'ame en meme temps que la face, sinon elle restait
   claire quand la page se met de chant, et ca dessinait un lisere a
   chaque couture. Un voile par sens de vue, chacun invisible de dos. */
.voile{
  position:absolute;left:-1px;right:-1px;top:0;bottom:0;pointer-events:none;
  background:#0A0805;opacity:0;
  backface-visibility:hidden;-webkit-backface-visibility:hidden;
}
.voile.av{transform:translateZ(.9px)}
.voile.ar{transform:rotateY(180deg) translateZ(.9px)}

/* Quand le livre est ferme, il n'y a que la couverture : le contre-plat
   restait affiche a cote d'elle, et faisait un carre sombre. */
html[data-ouvert="0"] .cote{visibility:hidden}

/* La corne : le coin deja replie, qui dit qu'on peut prendre la page. */
#corne{
  position:absolute;right:0;bottom:0;width:46px;height:46px;z-index:6;
  border:0;padding:0;background:transparent;cursor:pointer;
  transition:width 260ms cubic-bezier(.3,.85,.4,1),height 260ms cubic-bezier(.3,.85,.4,1);
}
/* l'ombre que le rabat porte sur la page qu'il decouvre */
#corne::before{
  content:"";position:absolute;left:-6px;right:2px;top:-6px;bottom:2px;
  background:linear-gradient(315deg,rgba(0,0,0,.55) 0 50%,transparent 50%);
  filter:blur(5px);
}
/* le rabat lui-meme : le dos de la feuille, et le pli net */
#corne::after{
  content:"";position:absolute;inset:0;
  background:
    linear-gradient(315deg,rgba(0,0,0,.18) 0 14%,rgba(0,0,0,0) 44%,rgba(0,0,0,0) 50%,transparent 50%),
    linear-gradient(315deg,var(--corne) 0 49.4%,var(--corne-2) 49.4% 50%,transparent 50%);
}
#corne:hover{width:88px;height:88px}
#corne:focus-visible{outline:2px solid var(--or);outline-offset:3px}
html[data-ouvert="0"] #corne{display:none}
#couv .recto{
  background:#171410 center/cover no-repeat;
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.06);
}
#couv .recto .habillage{
  position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(8,6,4,.60) 0%,rgba(8,6,4,.05) 34%,rgba(8,6,4,.10) 62%,rgba(8,6,4,.78) 100%);
}
#couv .recto .titre{
  position:absolute;left:0;right:0;top:52px;text-align:center;padding:0 34px;
  font:400 33px/1.1 var(--serif);letter-spacing:.17em;text-transform:uppercase;
  color:#F6EFE0;text-shadow:0 2px 18px rgba(0,0,0,.8);
}
#couv .recto .sous{
  position:absolute;left:0;right:0;bottom:58px;text-align:center;
  font:10px var(--sans);letter-spacing:.42em;text-transform:uppercase;color:#D9C9A6;
  text-shadow:0 2px 12px rgba(0,0,0,.9);
}
#couv .recto .filet{
  position:absolute;left:50%;top:112px;width:52px;height:1px;margin-left:-26px;
  background:rgba(246,239,224,.55);
}
#couv .verso{background:linear-gradient(145deg,#2E2A24,#1A1713)}
html[data-nuit="1"] #couv .verso{background:linear-gradient(145deg,#111820,#080C11)}

/* ---------- les flèches ---------- */
.fleche{
  position:fixed;top:50%;transform:translateY(-50%);z-index:20;
  width:56px;height:96px;border:0;border-radius:6px;cursor:pointer;
  background:rgba(255,255,255,.07);color:#8B8474;box-shadow:inset 0 0 0 1px rgba(255,255,255,.06);
  display:flex;align-items:center;justify-content:center;
  transition:background 160ms,color 160ms,opacity 200ms;
}
.fleche:hover{background:rgba(255,255,255,.16);color:#F2EADA}
.fleche:disabled{opacity:.16;cursor:default}
.fleche svg{width:26px;height:26px;fill:none;stroke:currentColor;stroke-width:1.6;
  stroke-linecap:round;stroke-linejoin:round}
#prec{left:16px}
#suiv{right:16px}

/* ---------- la barre du bas ---------- */
#barre{
  position:fixed;left:0;right:0;bottom:0;z-index:20;
  display:flex;align-items:center;gap:16px;padding:10px 18px 12px;
  font:11px var(--sans);color:var(--encre-3);
  background:linear-gradient(180deg,transparent,rgba(0,0,0,.45));
}
#barre button{
  border:0;background:rgba(255,255,255,.06);color:var(--encre-3);
  font:11px var(--sans);letter-spacing:.1em;text-transform:uppercase;
  padding:7px 12px;border-radius:4px;cursor:pointer;transition:background 150ms,color 150ms;
}
#barre button:hover{background:rgba(255,255,255,.14);color:#EFE7D6}
#barre button[aria-pressed="true"]{background:rgba(176,139,79,.26);color:#E8D3AA}
#ou{margin-left:auto;letter-spacing:.08em;white-space:nowrap}
#ou b{font-weight:600;color:#CFC3AC}
#rail{flex:1;height:20px;position:relative;cursor:pointer;min-width:120px}
#rail .voie{position:absolute;left:0;right:0;top:9px;height:2px;background:rgba(255,255,255,.11);border-radius:2px}
#rail .fait{position:absolute;left:0;top:9px;height:2px;background:var(--or);border-radius:2px;transition:width 260ms ease}
#rail .cran{position:absolute;top:5px;width:1px;height:10px;background:rgba(255,255,255,.30)}

/* ---------- le sommaire en surimpression ---------- */
#voile{
  position:fixed;inset:0;z-index:30;display:none;
  background:rgba(6,8,11,.72);backdrop-filter:blur(3px);
  align-items:center;justify-content:center;
}
#voile.on{display:flex}
#voile .boite{
  width:min(440px,86vw);max-height:80vh;overflow:auto;
  background:var(--papier);color:var(--encre);padding:34px 38px 30px;border-radius:4px;
  box-shadow:0 40px 90px -20px rgba(0,0,0,.8);
}
#voile .som{position:static;width:auto;height:auto;left:auto}
#voile .som li{cursor:pointer;padding:2px 0;border-radius:3px}
#voile .som li:hover .n{color:var(--or)}

/* ---------- la fiche du glossaire ---------- */
#fiche{
  position:fixed;z-index:22;width:212px;max-height:62vh;overflow:auto;display:none;
  background:var(--papier);color:var(--encre);
  box-shadow:0 22px 48px -14px rgba(0,0,0,.75),0 0 0 1px rgba(255,255,255,.07);
  padding:15px 17px 16px;border-radius:3px;
}
#fiche.on{display:block;animation:venir 180ms ease-out}
#fiche.bas{
  width:auto;left:20px;right:20px;top:auto;bottom:50px;max-height:24vh;
  display:none;column-width:300px;column-gap:26px;
}
#fiche.bas.on{display:block}
#fiche.bas h4{column-span:all}
@keyframes venir{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.glo.ouvert{background:rgba(176,139,79,.22);border-radius:2px}
#fiche h4{margin:0 0 6px;font:600 10px var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--encre-3)}
#fiche p{margin:0;font:12.6px/1.55 var(--serif)}
html[data-glo="1"] .glo{
  border-bottom:1px dotted var(--encre-3);cursor:help;
}
html[data-glo="0"] .glo{border:0;cursor:inherit;pointer-events:none}

/* Le mot d'accueil : rien ne disait que les fleches ouvraient le livre. */
#indice{
  position:fixed;z-index:15;display:flex;align-items:baseline;gap:11px;
  opacity:0;transition:opacity 700ms ease;pointer-events:none;
  color:#7A7262;font-family:var(--sans);max-width:224px;
}
html[data-nuit="1"] #indice{color:#5C6875}
#indice.on{opacity:1;pointer-events:auto;cursor:pointer}
#indice .k{
  font-size:17px;line-height:1;color:#A2917A;
}
html[data-nuit="1"] #indice .k{color:#7CC6DC}
#indice .t{font-size:11px;letter-spacing:.17em;text-transform:uppercase;line-height:1.5}
#indice em{
  display:block;font-style:normal;text-transform:none;letter-spacing:.02em;
  font-size:11.5px;line-height:1.75;opacity:.78;margin-top:6px;
}
/* les touches se dessinent comme des touches, sinon on croit qu'on
   parle des deux fleches posees a l'ecran */
#indice b{
  display:inline-block;font-weight:400;font-size:10.5px;line-height:15px;
  min-width:17px;text-align:center;padding:0 3px;margin:0 1px;
  border:1px solid currentColor;border-radius:3px;opacity:.85;
  vertical-align:.06em;
}

#banc{position:absolute;left:-9999px;top:0;visibility:hidden;height:auto!important}
#attente{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;
  font:11px var(--sans);letter-spacing:.3em;text-transform:uppercase;color:#6A6053;z-index:40}
</style>
</head>
<body>

<div id="attente">on relie le livre…</div>

<div id="scene">
  <div id="cadre">
    <div id="livre">
      <div id="ombre"></div>
      <div class="tranche" id="trG"></div>
      <div class="tranche" id="trD"></div>
      <div class="cote g" id="pG"></div>
      <div class="cote d" id="pD"></div>
      <button id="corne" title="Page suivante" aria-label="Page suivante"></button>
      <div id="feuille" hidden></div>
      <div id="couv">
        <div class="face recto">
          <div class="habillage"></div>
          <div class="titre">L’Éclaircie</div>
          <div class="filet"></div>
          <div class="sous">Roman</div>
        </div>
        <div class="face verso"></div>
      </div>
    </div>
  </div>
</div>
<div id="fiche"><h4></h4><p></p></div>

<button class="fleche" id="prec" title="Page précédente — flèche gauche"><svg viewBox="0 0 24 24"><path d="M15 5 8 12l7 7"/></svg></button>
<button class="fleche" id="suiv" title="Page suivante — flèche droite"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>

<div id="barre">
  <button id="bSom" title="Sommaire — touche S">Sommaire</button>
  <button id="bNuit" aria-pressed="false" title="Lecture de nuit — touche N">Nuit</button>
  <div id="rail"><div class="voie"></div><div class="fait"></div></div>
  <div id="ou"></div>
</div>

<div id="indice"><span class="k">&rarr;</span><span class="t">Pour ouvrir<em>Les flèches de l’écran, ou <b>&larr;</b> <b>&rarr;</b> au clavier, tournent les pages.</em></span></div>

<div id="voile"><div class="boite" id="boite"></div></div>
<div class="bloc" id="banc"></div>

<script>
{{DATA}}
const COUV = "{{COUV}}";
</script>
<script>
(function(){
'use strict';

const PW={{PW}}, PH={{PH}}, TW={{TW}}, TH={{TH}}, LH={{LIGNE}}, SW={{SW}}, DEMI={{DEMI}};
const RACINE=document.documentElement;
const $=function(s){return document.getElementById(s)};
const pG=$('pG'), pD=$('pD'), feuille=$('feuille'), couv=$('couv'), banc=$('banc');
const fiche=$('fiche'), voile=$('voile'), boite=$('boite'), rail=$('rail');

if(COUV) couv.querySelector('.recto').style.backgroundImage='url('+COUV+')';

/* ================================================================
   1. LA PAGINATION
   Elle tourne une fois, au chargement, dans la géométrie logique.
   Un paragraphe qui déborde est coupé à la ligne, avec au moins
   deux lignes de chaque côté — pas de veuve, pas d'orpheline.
   ================================================================ */
const PAGES=[];

function jetonner(html){
  const gard=[];
  const plat=html.replace(/<(a|em|strong|i|b)\b[^>]*>[\s\S]*?<\/\1>/g,function(m){
    gard.push(m); return '\x01'+(gard.length-1)+'\x01';
  });
  return {mots:plat.split(' ').filter(Boolean), gard:gard};
}
function rendre(mots,gard){
  return mots.join(' ').replace(/\x01(\d+)\x01/g,function(m,i){return gard[+i]});
}

function noeud(it){
  const p=document.createElement('p');
  let c = it[0]==='pause' ? 'pause' : (it[0]==='tiret' ? 'tiret' : '');
  if(it[2]&1) c+=' plat';
  p.className=c.trim();
  p.innerHTML=it[1];
  return p;
}

function teteChap(ch){
  const d=document.createElement('div');
  d.className='ouvre';
  d.innerHTML='<h2>'+ch.rang+'</h2>';
  return d;
}

function tient(){ return banc.scrollHeight <= TH + 0.6; }

function largeurDerniereLigne(n){
  const r=document.createRange();
  r.selectNodeContents(n);
  const rects=r.getClientRects();
  return rects.length ? rects[rects.length-1].width : 0;
}

function couper(it,n){
  if(it[0]==='pause') return null;
  const t=jetonner(it[1]);
  if(t.mots.length<12) return null;
  banc.appendChild(n);
  let lo=3, hi=t.mots.length-3, best=0;
  while(lo<=hi){
    const mid=(lo+hi)>>1;
    n.innerHTML=rendre(t.mots.slice(0,mid),t.gard);
    if(tient()){ best=mid; lo=mid+1 } else hi=mid-1;
  }
  while(best>3){
    n.style.textIndent='';
    n.innerHTML=rendre(t.mots.slice(0,best),t.gard);
    const av=Math.round(n.offsetHeight/LH);
    n.style.textIndent='0';
    n.innerHTML=rendre(t.mots.slice(best),t.gard);
    const ap=Math.round(n.offsetHeight/LH);
    n.style.textIndent='';
    if(av<2){ best=0; break }
    if(ap>=2) break;
    best-=1;
  }
  if(best<4){ banc.removeChild(n); return null }
  n.innerHTML=rendre(t.mots.slice(0,best),t.gard);
  /* On ne justifie la derniere ligne que si elle est deja presque pleine :
     etiree depuis six mots, elle se voit de l'autre bout de la piece. */
  if(largeurDerniereLigne(n)>=TW*.78) n.className=(n.className+' coupe').trim();
  if(!tient()){ banc.removeChild(n); return null }
  return {apres:[it[0], rendre(t.mots.slice(best),t.gard), 1]};
}

function paginer(){
  PAGES.length=0;
  PAGES.push({type:'garde'});
  PAGES.push({type:'titre'});
  PAGES.push({type:'blanc'});
  PAGES.push({type:'sommaire'});
  PAGES.push({type:'blanc'});

  LIVRE.forEach(function(ch,ci){
    /* belle page : un chapitre commence toujours sur une page de droite,
       c'est-à-dire un folio impair. */
    if(PAGES.length%2===0) PAGES.push({type:'blanc'});
    ch.page=PAGES.length;
    const reste=ch.p.map(function(x){return x.slice()});
    let ouverture=true;
    for(;;){
      banc.innerHTML='';
      if(ouverture) banc.appendChild(teteChap(ch));
      let pose=0;
      while(reste.length){
        const it=reste[0];
        const n=noeud(it);
        banc.appendChild(n);
        if(tient()){ reste.shift(); pose++; continue }
        banc.removeChild(n);
        const c=couper(it,n);
        if(c){ reste[0]=c.apres; pose++ }
        else if(pose===0 && !ouverture){ banc.appendChild(n); reste.shift(); pose++ }
        break;
      }
      PAGES.push({type:'texte',ch:ci,ouverture:ouverture,html:banc.innerHTML});
      ouverture=false;
      if(!reste.length) break;
    }
  });
  if(PAGES.length%2) PAGES.push({type:'blanc'});
  PAGES.push({type:'garde'});
  if(PAGES.length%2) PAGES.push({type:'blanc'});
  banc.innerHTML='';
}

/* ================================================================
   2. LE RENDU D'UNE PAGE
   ================================================================ */
const HTML_TITRE='<div class="titrage"><h1>L’Éclaircie</h1>'
  +'<div class="filet"></div><div class="quoi">Roman</div>'
  +'<div class="bas">Version de travail</div></div>';

function htmlSommaire(){
  const l=LIVRE.map(function(ch){
    return '<li data-page="'+ch.page+'"><span class="n">'+ch.rang+'</span>'
      +'<span class="fil"></span><span class="f">'+ch.page+'</span></li>';
  }).join('');
  return '<div class="som"><h3>Sommaire</h3><ul>'+l+'</ul></div>';
}

function pageEl(i,cote){
  const p=PAGES[i];
  const d=document.createElement('div');
  d.className='page'; d.dataset.cote=cote;
  if(!p){ d.className='page nulle'; return d }
  if(p.type==='garde'){ d.className='page garde'; return d }
  if(p.type==='blanc') return d;
  if(p.type==='titre'){ d.innerHTML=HTML_TITRE; return d }
  if(p.type==='sommaire'){ d.innerHTML=htmlSommaire(); return d }
  let h='';
  if(!p.ouverture){
    h='<div class="tete">'+(cote==='g' ? 'L’Éclaircie' : LIVRE[p.ch].rang)+'</div>';
  }
  h+='<div class="bloc">'+p.html+'</div><div class="folio">'+i+'</div>';
  d.innerHTML=h;
  return d;
}

/* ================================================================
   3. LA BASCULE
   300 ms. Si on enchaîne, on n'anime plus : au bout de trente pages
   une jolie animation devient une taxe.
   ================================================================ */
const DUREE=500;
/* NLAME : le nombre de lames. Plus il y en a, plus la courbe est douce,
   et plus il faut composer de copies de page a chaque tour.
   BOSSE : quelle part de la rotation part dans la courbure, au milieu du
   tour. SIG : la largeur de la bosse, en fraction de page. */
const NLAME=14, LW={{PW}}/NLAME, BOSSE=.46, SIG=.42;
let spread=-1, anime=false, vise=0, dernier=0, minuteur=0, rafId=0;

/* La chaine de lames se batit une seule fois : chacune est fille de la
   precedente, donc les rotations s'additionnent le long de la feuille. */
const LAMES=(function(){
  const out=[]; let mere=feuille;
  for(let k=0;k<NLAME;k++){
    const lame=document.createElement('div');
    lame.className='lame';
    lame.style.left=(k===0?0:LW)+'px';
    lame.style.width=LW+'px';
    const ame=document.createElement('div'); ame.className='ame';
    lame.appendChild(ame);
    const parts=[];
    ['recto','verso'].forEach(function(quel,i){
      const f=document.createElement('div'); f.className='face '+quel;
      const fen=document.createElement('div'); fen.className='fen';
      /* le recto se lit depuis la reliure, le verso depuis son bord oppose */
      fen.style.left=(i===0 ? -k*LW : -({{PW}}-(k+1)*LW))+'px';
      f.appendChild(fen); lame.appendChild(f);
      const lu=document.createElement('div');
      lu.className='voile '+(i===0?'av':'ar');
      lame.appendChild(lu);
      parts.push({fen:fen, lu:lu});
    });
    mere.appendChild(lame);
    out.push({lame:lame, r:parts[0], v:parts[1]});
    mere=lame;
  }
  return out;
})();

function garnir(elRecto,elVerso){
  LAMES.forEach(function(L){
    L.r.fen.replaceChildren(elRecto.cloneNode(true));
    L.v.fen.replaceChildren(elVerso.cloneNode(true));
  });
}

/* t va de 0 a 1. La rotation totale de la feuille est repartie entre les
   lames : une part reste a la charniere, le reste se met sous une bosse
   qui voyage du bord libre vers la reliure. */
function courber(t,sens){
  const T = sens>0 ? -180*t : -180*(1-t);
  const centre = sens>0 ? 1-t : t;
  const bosse = BOSSE*Math.sin(Math.PI*t);
  const poids=[]; let somme=0;
  for(let k=0;k<NLAME;k++){
    const u=k/(NLAME-1);
    const g=Math.exp(-Math.pow((u-centre)/SIG,2));
    poids.push(g); somme+=g;
  }
  let cumul=0;
  for(let k=0;k<NLAME;k++){
    const a = T*((k===0?1-bosse:0) + bosse*poids[k]/somme);
    LAMES[k].lame.style.transform='rotateY('+a.toFixed(3)+'deg)';
    cumul+=a;
    /* Une lame de chant ne recoit plus la lumiere. sin carre, et pas
       1 - |cos| : les deux ont la meme forme, mais |cos| fait un angle
       vif a 90 degres, en plein dans le moment ou la page tourne le
       plus vite. On voyait la cassure. */
    const o=(.62*Math.pow(Math.sin(cumul*Math.PI/180),2)).toFixed(3);
    LAMES[k].r.lu.style.opacity=o;
    LAMES[k].v.lu.style.opacity=o;
  }
}

function lisser(t){ return t*t*(3-2*t) }

function poser(){
  pG.innerHTML=''; pD.innerHTML='';
  pG.appendChild(pageEl(spread*2,'g'));
  pD.appendChild(pageEl(spread*2+1,'d'));
  majEtat();
}

function finir(){
  clearTimeout(minuteur);
  cancelAnimationFrame(rafId);
  if(!anime) return;
  anime=false; spread=vise;
  poser();
  /* la feuille ne s'efface qu'une fois la page fixe peinte dessous,
     sinon on voit un trou d'une image */
  requestAnimationFrame(function(){
    feuille.hidden=true;
    LAMES.forEach(function(L){
      L.lame.style.transform='rotateY(0deg)';
      L.r.lu.style.opacity=0; L.v.lu.style.opacity=0;
      L.r.fen.replaceChildren(); L.v.fen.replaceChildren();
    });
  });
}

function animer(sens,cible){
  anime=true; vise=cible;
  let recto,verso;
  if(sens>0){
    recto=pageEl(spread*2+1,'d'); verso=pageEl(cible*2,'g');
    pD.replaceChildren(pageEl(cible*2+1,'d'));
  }else{
    recto=pageEl(cible*2+1,'d'); verso=pageEl(spread*2,'g');
    pG.replaceChildren(pageEl(cible*2,'g'));
  }
  garnir(recto,verso);
  $('corne').hidden=true;
  feuille.hidden=false;
  courber(0,sens);
  const depart=performance.now();
  (function pas(maintenant){
    const t=Math.min(1,(maintenant-depart)/DUREE);
    courber(lisser(t),sens);
    if(t<1) rafId=requestAnimationFrame(pas); else finir();
  })(depart);
  minuteur=setTimeout(finir,DUREE+220);   /* filet, si l'onglet dort */
}

function tourner(sens){
  cacherFiche();
  if(spread<0){ if(sens>0) ouvrirLivre(); return }
  const cible=spread+sens;
  if(cible<0){ fermerLivre(); return }
  if(cible*2>=PAGES.length) return;
  const t=Date.now();
  const vite=anime || (t-dernier)<DUREE+90;
  dernier=t;
  if(anime) finir();
  if(vite){ spread=cible; poser(); return }
  animer(sens,cible);
}

function allerA(page){
  cacherFiche();
  const cible=Math.max(0,Math.min(Math.floor(page/2),Math.floor((PAGES.length-1)/2)));
  if(anime) finir();
  if(spread<0){
    RACINE.dataset.ouvert='1'; couv.hidden=true;
    spread=cible; poser(); return;
  }
  if(cible===spread) return;
  if(Math.abs(cible-spread)===1){ tourner(cible-spread); return }
  spread=cible; poser();
}

function ouvrirLivre(){
  if(anime) return;
  anime=true;
  spread=0; poser();
  RACINE.dataset.ouvert='1';
  couv.style.transition='transform 560ms cubic-bezier(.36,.06,.24,1)';
  couv.style.transform='rotateY(-180deg)';
  setTimeout(function(){ couv.hidden=true; anime=false; majEtat() },570);
}

function fermerLivre(){
  if(anime) return;
  anime=true;
  couv.hidden=false;
  couv.style.transition='none';
  couv.style.transform='rotateY(-180deg)';
  void couv.offsetHeight;
  couv.style.transition='transform 560ms cubic-bezier(.36,.06,.24,1)';
  couv.style.transform='rotateY(0deg)';
  RACINE.dataset.ouvert='0';
  setTimeout(function(){
    spread=-1; anime=false;
    pG.replaceChildren(); pD.replaceChildren();
    majEtat(); poserIndice(); $('indice').classList.add('on');
  },570);
}

/* ================================================================
   4. OÙ ON EN EST — la seule chose qu'un livre de papier donne
   gratuitement, et qu'un écran doit rendre exprès.
   ================================================================ */
let FIN=0;

function majEtat(){
  const ferme=(spread<0);
  $('prec').disabled=ferme;
  $('suiv').disabled=!ferme && (spread+1)*2>=PAGES.length;
  $('corne').hidden=ferme || $('suiv').disabled;
  if(!ferme) $('indice').classList.remove('on');
  const g=spread*2, d=spread*2+1;
  let txt='';
  if(ferme){ txt='Livre fermé' }
  else if((PAGES[d]&&PAGES[d].type==='titre')||(PAGES[g]&&PAGES[g].type==='titre')){
    txt='Page de titre';
  }
  else if((PAGES[d]&&PAGES[d].type==='sommaire')||(PAGES[g]&&PAGES[g].type==='sommaire')){
    txt='Sommaire';
  }
  else{
    const p=(PAGES[d]&&PAGES[d].type==='texte')?PAGES[d]
           :((PAGES[g]&&PAGES[g].type==='texte')?PAGES[g]:null);
    const folio=(PAGES[d]&&PAGES[d].type==='texte')?d
               :((PAGES[g]&&PAGES[g].type==='texte')?g:0);
    txt = p ? LIVRE[p.ch].rang+' &middot; <b>'+folio+'</b> / '+FIN : 'Fin';
  }
  $('ou').innerHTML=txt;
  const av=ferme?0:Math.min(1,(spread*2)/Math.max(1,FIN));
  rail.querySelector('.fait').style.width=(av*100)+'%';
  const ep=14;
  $('trG').style.width=(ferme?0:2+ep*av)+'px';
  $('trD').style.width=(ferme?0:2+ep*(1-av))+'px';
  if(!ferme){
    try{ localStorage.setItem('eclaircie-livre',String(spread)) }catch(e){}
    try{ history.replaceState(null,'','#p'+(spread*2)) }catch(e){}
  }
}

function poserCrans(){
  LIVRE.forEach(function(ch){
    const c=document.createElement('div');
    c.className='cran';
    c.style.left=Math.min(99.6,(ch.page/FIN)*100)+'%';
    c.title=ch.rang;
    rail.appendChild(c);
  });
}

/* ================================================================
   5. L'ÉCHELLE — le livre flotte au milieu et remplit ce qu'il peut,
   sans jamais changer sa pagination.
   ================================================================ */
function poserIndice(){
  const ind=$('indice');
  if(spread>=0){ ind.classList.remove('on'); return }
  const r=couv.getBoundingClientRect();
  const L=ind.offsetWidth||190, M=30;
  if(r.right+M+L<=window.innerWidth-16){
    ind.style.left=Math.round(r.right+M)+'px';
    ind.style.top=Math.round(r.top+r.height*.44)+'px';
  }else{
    ind.style.left=Math.round(r.left)+'px';
    ind.style.top=Math.round(Math.min(r.bottom+18,window.innerHeight-90))+'px';
  }
}

function ajuster(){
  const vw=window.innerWidth, vh=window.innerHeight;
  /* de l air au-dessus et au-dessous : la feuille qui tourne deborde
     du livre, et elle ne doit pas se faire couper par la fenetre. */
  const k=Math.min((vw-200)/SW,(vh-150)/PH);
  $('cadre').style.transform='scale('+Math.max(.28,k)+')';
}
window.addEventListener('resize',function(){
  ajuster(); poserIndice();
  const o=document.querySelector('.glo.ouvert');
  if(o && fiche.classList.contains('on')) poserFiche(o);
});

/* ================================================================
   6. LE GLOSSAIRE — jamais au survol, jamais tout seul, et la page
   ne bouge pas d'un pixel quand la fiche s'ouvre.
   ================================================================ */
function cacherFiche(){
  fiche.classList.remove('on');
  const o=document.querySelector('.glo.ouvert'); if(o) o.classList.remove('ouvert');
}

/* La fiche se pose sur le bureau, du cote du mot, a sa hauteur. Elle ne
   passe par-dessus la page qu'en dernier recours -- une fenetre etroite. */
function poserFiche(a){
  fiche.classList.remove('bas');
  fiche.style.left=''; fiche.style.top='';
  const liv=$('livre').getBoundingClientRect();
  const r=a.getBoundingClientRect();
  const L=fiche.offsetWidth, M=14;
  const COULOIR=78;          /* la lane des fleches, qui reste libre */
  const aGauche=(r.left+r.width/2)<(liv.left+liv.width/2);
  const placeG=liv.left-M-L, placeD=liv.right+M;
  const tientG=placeG>=COULOIR, tientD=placeD+L<=window.innerWidth-COULOIR;
  let x=null;
  if(aGauche&&tientG) x=placeG;
  else if(!aGauche&&tientD) x=placeD;
  else if(tientD) x=placeD;
  else if(tientG) x=placeG;
  if(x===null){ fiche.classList.add('bas'); return }
  const H=fiche.offsetHeight;
  let y=Math.max(M,Math.min(r.top-6,window.innerHeight-H-56));
  fiche.style.left=Math.round(x)+'px';
  fiche.style.top=Math.round(y)+'px';
}

document.addEventListener('click',function(e){
  const a=e.target.closest?e.target.closest('.glo'):null;
  if(!a){ if(!e.target.closest('#fiche')) cacherFiche(); return }
  if(RACINE.dataset.glo!=='1') return;
  const mot=a.dataset.mot;
  if(!MOTS[mot]) return;
  cacherFiche();
  fiche.querySelector('h4').textContent=mot;
  fiche.querySelector('p').innerHTML=MOTS[mot];
  fiche.classList.add('on');
  a.classList.add('ouvert');
  poserFiche(a);
  e.stopPropagation();
});

/* ================================================================
   7. LES COMMANDES
   ================================================================ */
$('prec').addEventListener('click',function(){tourner(-1)});
$('suiv').addEventListener('click',function(){tourner(1)});
$('corne').addEventListener('click',function(){tourner(1)});
$('indice').addEventListener('click',function(){tourner(1)});

document.addEventListener('keydown',function(e){
  if(e.ctrlKey||e.altKey||e.metaKey) return;
  const k=e.key;
  if(k==='ArrowRight'||k==='PageDown'||k===' '){ e.preventDefault(); tourner(1) }
  else if(k==='ArrowLeft'||k==='PageUp'){ e.preventDefault(); tourner(-1) }
  else if(k==='Home'){ e.preventDefault(); allerA(1) }
  else if(k==='End'){ e.preventDefault(); allerA(PAGES.length-2) }
  else if(k==='s'||k==='S'){ basculerSommaire() }
  else if(k==='g'||k==='G'){ basculerGlossaire() }
  else if(k==='n'||k==='N'){ $('bNuit').click() }
  else if(k==='Escape'){ voile.classList.remove('on'); cacherFiche() }
});

function basculerSommaire(){
  if(voile.classList.contains('on')){ voile.classList.remove('on'); return }
  boite.innerHTML=htmlSommaire();
  const ici=spread*2;
  const li=[].slice.call(boite.querySelectorAll('li'));
  li.forEach(function(x,i){
    const p=+x.dataset.page;
    const suiv=li[i+1]?+li[i+1].dataset.page:1e9;
    if(ici>=p-1&&ici<suiv-1) x.classList.add('ici');
    x.addEventListener('click',function(){
      voile.classList.remove('on'); allerA(p);
    });
  });
  voile.classList.add('on');
}
$('bSom').addEventListener('click',basculerSommaire);
voile.addEventListener('click',function(e){ if(e.target===voile) voile.classList.remove('on') });

function basculerGlossaire(){
  const on=RACINE.dataset.glo==='1';
  RACINE.dataset.glo=on?'0':'1';
  if(on) cacherFiche();
  try{ localStorage.setItem('eclaircie-glo',on?'0':'1') }catch(e){}
}
$('bNuit').addEventListener('click',function(){
  const on=RACINE.dataset.nuit==='1';
  RACINE.dataset.nuit=on?'0':'1';
  this.setAttribute('aria-pressed',on?'false':'true');
  try{ localStorage.setItem('eclaircie-nuit',on?'0':'1') }catch(e){}
});
rail.addEventListener('click',function(e){
  const r=rail.getBoundingClientRect();
  allerA(Math.round(((e.clientX-r.left)/r.width)*FIN));
});

/* ================================================================
   8. ON RELIE
   ================================================================ */
function demarrer(){
  paginer();
  FIN=PAGES.length-1;
  while(FIN>0 && PAGES[FIN].type!=='texte') FIN--;
  try{
    if(localStorage.getItem('eclaircie-nuit')==='1'){
      RACINE.dataset.nuit='1'; $('bNuit').setAttribute('aria-pressed','true');
    }
    if(localStorage.getItem('eclaircie-glo')==='1') RACINE.dataset.glo='1';
  }catch(e){}
  poserCrans();
  ajuster();
  $('attente').remove();
  couv.style.transform='rotateY(0deg)';
  /* une adresse dans l'URL : #p42 ouvre le livre a la page 42 */
  const ancre=/^#p(\d+)$/.exec(location.hash||'');
  let repris=-1;
  if(ancre){ repris=Math.floor(+ancre[1]/2) }
  else{
    try{ const v=localStorage.getItem('eclaircie-livre'); if(v!==null) repris=+v }catch(e){}
  }
  if(repris>0 && repris*2<PAGES.length){
    const liv=$('livre');
    liv.style.transition='none';          /* on ouvre deja ouvert */
    RACINE.dataset.ouvert='1'; couv.hidden=true; spread=repris; poser();
    requestAnimationFrame(function(){ requestAnimationFrame(function(){
      liv.style.transition='';
    })});
  }else{
    majEtat();
    poserIndice();
    setTimeout(function(){ if(spread<0) $('indice').classList.add('on') },900);
  }
  console.log('L’Éclaircie : '+FIN+' pages, '+LIVRE.length+' chapitres');
}

if(document.fonts&&document.fonts.ready){ document.fonts.ready.then(demarrer) }
else{ window.addEventListener('load',demarrer) }
})();
</script>
</body>
</html>
"""

remplacements = {
    'PW': GEO['PW'], 'PH': GEO['PH'], 'TW': GEO['TW'], 'TH': GEO['TH'],
    'HAUT': GEO['HAUT'], 'BAS': GEO['BAS'],
    'DEDANS': GEO['DEDANS'], 'DEHORS': GEO['DEHORS'],
    'CORPS': GEO['CORPS'], 'LIGNE': GEO['LIGNE'],
    'DEUX': GEO['LIGNE'] * 1.5,
    'OUVRE_HAUT': GEO['OUVRE_HAUT'], 'OUVRE_BAS': GEO['OUVRE_BAS'],
    'TITRE_LH': GEO['TITRE_LH'],
    'SW': GEO['PW'] * 2, 'DEMI': GEO['PW'] // 2, 'PWP12': GEO['PW'] + 12,
}
page = GABARIT
for clef, val in remplacements.items():
    txt = (u'%g' % val) if isinstance(val, float) else u'%d' % val
    page = page.replace(u'{{' + clef + u'}}', txt)
page = page.replace(u'{{DATA}}', DATA).replace(u'{{COUV}}', COUV)

assert u'{{' not in page, u'un jeton du gabarit n a pas ete remplace : ' \
                          + page[page.index(u'{{'):page.index(u'{{') + 40]

SORTIE = os.path.join(ICI, '..', 'le-livre.html')
data = page.encode('utf-8')
open(SORTIE, 'wb').write(data)
print(u'le-livre.html fabrique : %.0f ko' % (len(data) / 1024.0))
