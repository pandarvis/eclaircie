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
            'chapitre-4', 'chapitre-5', 'chapitre-6', 'chapitre-7', 'chapitre-8']

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
        # la mention de temps est facultative : peu de chapitres en ont
        'quand': (re.search(r'quand: `([^`]*)`', bloc).group(1)
                  if re.search(r'quand: `([^`]*)`', bloc) else u''),
        # une page seule, posee devant ce chapitre. Facultative.
        'encart': (re.search(r'encart: `([^`]*)`', bloc).group(1)
                   if re.search(r'encart: `([^`]*)`', bloc) else u''),
        # le troisieme champ est facultatif : il porte une marque de
        # forme, et les autres scripts ne le lisent pas.
        'p': [list(x) for x in re.findall(
            r'\[`(p|tiret|pause)`,`([^`]*)`(?:,`([^`]*)`)?\]', bloc)],
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
#  LES SAUTS DE PAGE DEMANDES
#
#  On nomme le debut du paragraphe qui doit commencer une page. L'ancre
#  est le texte, pas un numero : la pagination se recalcule a chaque
#  correction. Si le passage est reecrit, la fabrication s'arrete ici
#  plutot que de perdre le saut sans rien dire.
# =====================================================================
SAUTS = {
    'prologue': [u'Après le nom, le pichet.'],
}


def plat(txt):
    return re.sub(r'<[^>]+>', u'', txt)


# =====================================================================
#  LES DRAPEAUX — ce que la mise en page doit savoir de chaque
#  paragraphe. 1 : pas d'alinea (debut de chapitre, ou apres une
#  pause) — jamais sur un tiret, dont l'alinea tient la colonne
#  des cadratins. 2 : premiere ligne en petites capitales. 4 :
#  commence une page neuve.
# =====================================================================
poses_saut = 0
for t in textes:
    precedent = None
    premier = True
    demandes = [typo(x) for x in SAUTS.get(t['id'], [])]
    trouves = []
    for para in t['p']:
        f = 0
        # Un tiret garde son alinea : c'est lui qui aligne la colonne
        # des cadratins. La liseuse fait deja cette exception.
        if para[0] == 'p' and (precedent is None or precedent == 'pause'):
            f |= 1
        if premier and para[0] != 'pause':
            f |= 2
            premier = False
        for d in demandes:
            if plat(para[1]).startswith(d):
                f |= 4
                trouves.append(d)
        para.append(f)
        precedent = para[0]
    for d in demandes:
        assert trouves.count(d) == 1, \
            u'saut de page dans %s : %d paragraphe(s) commencent par %s' \
            % (t['id'], trouves.count(d), d[:40])
    poses_saut += len(trouves)
if poses_saut:
    print(u'sauts de page demandes : %d' % poses_saut)


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
    lignes.append(u'{ id:%s%s%s, rang:%s%s%s, titre:%s%s%s, quand:%s%s%s, encart:%s%s%s, p:['
                  % (B, t['id'], B, B, echapper(t['rang']), B,
                     B, echapper(t['titre']), B,
                     B, echapper(t['quand']), B,
                     B, echapper(t['encart']), B))
    for genre, texte, marque, f in t['p']:
        lignes.append(u'[%s%s%s,%s%s%s,%s%s%s,%d],'
                      % (B, genre, B, B, echapper(texte), B,
                         B, marque, B, f))
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
  --plume:"Segoe Script","Bradley Hand","Lucida Handwriting","Ink Free","Segoe Print",cursive;
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
/* un message ressemble a ce qu'il lit : un encart tres leger, une
   lineale d'interface, le nom et l'heure d'arrivee. Le remplissage
   n'est que lateral : une hauteur casserait la grille. */
.bloc p.sms{
  margin:0;text-indent:0;text-align:left;padding:2px 14px 3px;
  border:0 solid transparent;border-width:9px 0 9px;
  background:var(--papier-2);background-clip:padding-box;border-radius:4px;
  font:400 .84em/{{LIGNE}}px "Segoe UI",Tahoma,Arial,sans-serif;
  color:var(--encre);letter-spacing:0;
}
.bloc p.sms::before{
  content:attr(data-de) " · " attr(data-h);display:block;
  min-height:{{LIGNE}}px;
  font:400 .62em/{{LIGNE}}px "Segoe UI",Tahoma,Arial,sans-serif;
  color:var(--encre-3);letter-spacing:.06em;
}
.bloc p.coupe{text-align-last:justify;-moz-text-align-last:justify}
.bloc p.pause{
  text-indent:0;text-align:center;letter-spacing:.5em;color:var(--encre-3);
  margin:{{LIGNE}}px 0;height:{{LIGNE}}px;
}
/* Une pause sans marque : une ligne de blanc, et rien d'ecrit. La
   grille reste juste -- une ligne, pas trois. */
.bloc p.pause:empty{margin:0;height:{{LIGNE}}px;letter-spacing:0}
.bloc em{font-style:italic}
.ouvre{padding:{{OUVRE_HAUT}}px 0 {{OUVRE_BAS}}px;text-align:center}
.ouvre h2{
  margin:0;font:400 17px/{{TITRE_LH}}px var(--serif);color:var(--encre);
  letter-spacing:.26em;text-transform:uppercase;
  /* l’interlettrage ajoute un blanc apres la derniere lettre :
     text-indent le rattrape, moitie du blanc, et le titre est centre */
  text-indent:.26em;
}
/* la mention de temps : plus petite que le rang, et elle ne crie pas */
.ouvre .quand{
  margin:-10px 0 0;font:italic 400 11.5px/16px var(--serif);
  color:var(--encre-3);letter-spacing:.05em;text-indent:.05em;
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

/* le plan : une planche au trait, pas une illustration */
.planche{
  position:absolute;inset:0;display:flex;align-items:center;
  justify-content:center;padding:0 34px;
}
.planche > div{width:100%;max-width:402px}
.planche .p-tete{
  margin:0 0 18px;font:400 9.4px/14px var(--sans);color:var(--encre-2);
  letter-spacing:.3em;text-transform:uppercase;text-indent:.3em;
  text-align:center;
}
.planche svg{width:100%;display:block}
.plan .p-mur{fill:none;stroke:var(--encre-3);stroke-width:2.4}
.plan .p-serre{fill:none;stroke:var(--encre-3);stroke-width:1.6;opacity:.7}
.plan .p-bande path{fill:none;stroke:var(--encre-3);opacity:.16;
  stroke-linecap:round;stroke-linejoin:round}
.plan .p-coulee path,.plan .p-coulee circle{
  fill:none;stroke:var(--encre);stroke-width:3.4;opacity:.42;
  stroke-linecap:round;
}
.plan .p-caps ellipse{fill:var(--encre);opacity:.72}
/* celles qui vont s'ouvrir : la paroi a pali */
.plan .p-caps .claire{
  fill:none;stroke:var(--encre);stroke-width:1.6;opacity:.6;
}
/* celles qui vont s'ouvrir : la paroi a pali */
.plan .p-caps .claire{
  fill:none;stroke:var(--encre);stroke-width:1.6;opacity:.6;
}
/* celles qui vont s'ouvrir : la paroi a pali */
.plan .p-caps .claire{
  fill:none;stroke:var(--encre);stroke-width:1.6;opacity:.6;
}
/* celles qui vont s'ouvrir : la paroi a pali */
.plan .p-caps .claire{
  fill:none;stroke:var(--encre);stroke-width:1.6;opacity:.6;
}
/* celles qui vont s'ouvrir : la paroi a pali */
.plan .p-caps .claire{
  fill:none;stroke:var(--encre);stroke-width:1.6;opacity:.6;
}
/* celles qui vont s'ouvrir : la paroi a pali */
.plan .p-caps .claire{
  fill:none;stroke:var(--encre);stroke-width:1.6;opacity:.6;
}
/* celles qui vont s'ouvrir : la paroi a pali */
.plan .p-caps .claire{
  fill:none;stroke:var(--encre);stroke-width:1.6;opacity:.6;
}
/* celles qui vont s'ouvrir : la paroi a pali */
.plan .p-caps .claire{
  fill:none;stroke:var(--encre);stroke-width:1.6;opacity:.6;
}
/* celles qui vont s'ouvrir : la paroi a pali */
.plan .p-caps .claire{
  fill:none;stroke:var(--encre);stroke-width:1.6;opacity:.6;
}
.plan .p-piece circle,.plan .p-piece path,.plan .p-piece rect{
  fill:none;stroke:var(--encre-3);stroke-width:1.8;
}
/* le tiret qui vise le sol : la serre n'a pas de contour a elle */
.plan .p-tiret path{fill:none;stroke:var(--encre-3);stroke-width:1.2}
.plan .p-tiret circle{fill:var(--encre-3)}
.plan .p-nom text{
  font:400 17px var(--sans);fill:var(--encre-2);
  letter-spacing:.14em;text-transform:uppercase;
  paint-order:stroke;stroke:var(--papier);stroke-width:3.6px;
  stroke-linejoin:round;
}
/* la fiche de placement : un formulaire, donc une lineale et des filets */
.fiche{
  position:absolute;inset:0;display:flex;align-items:center;
  justify-content:center;padding:0 58px;
}
.fiche .f-corps{width:100%}
.fiche .f-tete{
  margin:0;font:400 9.4px/14px var(--sans);color:var(--encre-2);
  letter-spacing:.3em;text-transform:uppercase;text-indent:.3em;
  text-align:center;
}
.fiche .f-sous{
  margin:4px 0 0;font:italic 400 9px/13px var(--sans);
  color:var(--encre-3);letter-spacing:.05em;text-align:center;
}
.fiche .f-champs{
  margin:20px 0 0;border-top:1px solid var(--encre-3);
  border-bottom:1px solid var(--encre-3);padding:7px 0 6px;
}
.fiche .f-champs > div{
  display:flex;align-items:baseline;
  font:400 9.8px/20px var(--sans);color:var(--encre);
}
/* imprime : ce que le formulaire demande */
.fiche .f-champs span{
  flex:0 0 128px;color:var(--encre-3);letter-spacing:.14em;
  text-transform:uppercase;font-size:7.8px;
}
/* a la plume : ce qu'Andrew a rempli */
.fiche .f-champs b{
  font:400 12.6px/20px var(--plume);
  font-weight:400;letter-spacing:0;color:var(--encre);
}
/* les deux options sont imprimees ; seule la croix est de lui */
.fiche .f-champs b.f-opt{
  font:400 9.8px/20px var(--sans);letter-spacing:.02em;
}
.fiche .c{
  display:inline-block;width:8px;height:8px;margin-right:7px;
  border:1px solid var(--encre-3);position:relative;vertical-align:-1px;
}
.fiche .c-on::after{
  content:"✕";position:absolute;left:-2px;top:-6.5px;
  font:400 12.5px/1 var(--plume);color:var(--encre);
}
.fiche .c-b{margin-left:20px}
.fiche .f-consigne{
  margin:13px 0 1px;font:italic 400 9px/13px var(--sans);
  color:var(--encre-3);letter-spacing:.04em;
}
.fiche svg{display:block;margin:0 auto}
.fiche .f-lg text{
  font:400 5.9px var(--sans);fill:var(--encre-3);
  letter-spacing:.2em;text-transform:uppercase;
}
.fiche .f-case{
  margin:13px 0 0;border:1px solid var(--encre-3);padding:7px 10px 8px;
}
/* dans un cadre, les champs n'ont plus besoin de leurs propres filets */
.fiche .f-case .f-nb{margin:0;border:0;padding:0}
.fiche .f-clef{
  margin:0;font:400 7.8px/12px var(--sans);color:var(--encre-3);
  letter-spacing:.2em;text-transform:uppercase;
}
.fiche .f-est{
  margin:4px 0 0;font:italic 400 8.6px/12px var(--sans);color:var(--encre-3);
}
.fiche .f-obs{padding-bottom:6px}
/* le pied : un filet imprime, et la main d'Andrew posee dessus */
.fiche .f-pied{
  margin:13px 2px 0;display:flex;align-items:flex-end;
  justify-content:flex-end;gap:13px;
}
.fiche .f-pied .f-clef{padding-bottom:4px}
.fiche .f-trait{
  width:132px;height:27px;border-bottom:1px solid var(--encre-3);
  display:flex;align-items:flex-end;justify-content:center;
}
.fiche .f-sign{
  font:400 17px/1 var(--plume);font-style:normal;color:var(--encre);
  transform:rotate(-2.5deg);padding-bottom:2px;
}
.fiche .f-lignes{margin-top:9px}
/* la main d'Andrew se pose au-dessus du premier filet */
.fiche .f-lignes .f-note{
  display:block;margin:0 0 2px;font:400 11.8px/16px var(--plume);
  font-weight:400;color:var(--encre);
}
.fiche .f-lignes i{
  display:block;height:1px;margin-bottom:11px;
  background:var(--encre-3);opacity:.45;
}
.suite{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.suite span{
  font:400 14px var(--serif);letter-spacing:.44em;text-transform:uppercase;
  color:var(--encre-3);padding-left:.44em;
}
.suite span::before,.suite span::after{
  content:"";display:block;width:38px;height:1px;background:var(--encre-3);
  opacity:.5;margin:0 auto;
}
.suite span::before{margin-bottom:26px;margin-left:calc(50% - 19px - .22em)}
.suite span::after{margin-top:26px;margin-left:calc(50% - 19px - .22em)}

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
/* la profondeur exacte de chaque face est posee lame par lame */
.face.verso{transform:rotateY(180deg)}

/* Les lames : la feuille est courbe parce qu'elle est articulee. */
.lame{position:absolute;top:0;height:{{PH}}px;transform-origin:0 50%;transform-style:preserve-3d}
/* Chaque lame deborde d'un pixel sur sa voisine, et ce debordement
   passe DERRIERE elle : ce qui fuit par la couture est alors le meme
   texte au meme endroit, et la couture disparait. */
.lame>.face{left:0;top:0;right:auto;bottom:auto;width:calc(100% + 1px);height:100%}
.fen{position:absolute;top:0;width:{{PW}}px;height:{{PH}}px}
/* Les voiles d'ombre sont AU NIVEAU DE LA LAME, devant tout le reste,
   et ils font EXACTEMENT sa largeur : debordants, ils se superposaient
   d'une couture a l'autre et l'ombre y comptait double. L'ame, elle,
   depasse toujours d'un pixel -- elle s'assombrit par filtre, voir
   courber(). Un voile par sens de vue, chacun invisible de dos. */
.voile{
  position:absolute;left:0;top:0;bottom:0;width:calc(100% + 1px);
  pointer-events:none;background:none;
  backface-visibility:hidden;-webkit-backface-visibility:hidden;
}
.voile.ar{transform:rotateY(180deg)}

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

/* La corne gauche : la meme, en miroir, pour revenir en arriere.
   Discrete au repos ; elle se leve quand le curseur passe. */
#corneg{
  position:absolute;left:0;bottom:0;width:46px;height:46px;z-index:6;
  border:0;padding:0;background:transparent;cursor:pointer;opacity:.3;
  transition:width 260ms cubic-bezier(.3,.85,.4,1),height 260ms cubic-bezier(.3,.85,.4,1),opacity 220ms ease;
}
#corneg::before{
  content:"";position:absolute;left:2px;right:-6px;top:-6px;bottom:2px;
  background:linear-gradient(45deg,rgba(0,0,0,.55) 0 50%,transparent 50%);
  filter:blur(5px);
}
#corneg::after{
  content:"";position:absolute;inset:0;
  background:
    linear-gradient(45deg,rgba(0,0,0,.18) 0 14%,rgba(0,0,0,0) 44%,rgba(0,0,0,0) 50%,transparent 50%),
    linear-gradient(45deg,var(--corne) 0 49.4%,var(--corne-2) 49.4% 50%,transparent 50%);
}
#corneg:hover{width:88px;height:88px;opacity:1}
#corneg:focus-visible{outline:2px solid var(--or);outline-offset:3px;opacity:1}
html[data-ouvert="0"] #corneg{display:none}
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
      <button id="corneg" title="Page précédente" aria-label="Page précédente"></button>
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
  if(it[3]&1) c+=' plat';
  /* un message : une police d'ecran, le nom et l'heure */
  if(it[2] && it[2].slice(0,3)==='sms'){
    c+=' sms';
    const q=it[2].slice(4).split('|');
    if(q[0]) p.dataset.de=q[0];
    if(q[1]) p.dataset.h=q[1];
  }
  p.className=c.trim();
  p.innerHTML=it[1];
  return p;
}

/* une page seule qui porte un document du monde, pas du texte. */
const PLAN_RUCHE='<svg viewBox="0 0 1010 1010" width="100%" preserveAspectRatio="xMidYMid meet" aria-hidden="true" class="plan"><rect x="54" y="54" width="902" height="902" rx="26" class="p-mur"/><path d="M150,150 C300,96 640,104 760,168 C852,218 880,340 862,470 C846,596 872,700 812,782 C742,876 560,884 430,872 C296,860 168,838 122,742 C74,640 108,506 106,410 C104,300 92,190 150,150 Z" class="p-serre"/><g class="p-bande"><path d="M516,822 C506,772 486,730 470,686 C456,644 448,620 444,596" style="stroke-width:46"/><path d="M676,900 L836,900 C860,900 868,890 868,868 L868,384 C868,362 856,352 836,352 L746.1,338.6 A322,322 0 0 0 109.8,366.3" style="stroke-width:30"/><path d="M868,388 L822,388 L822,714 L868,714" style="stroke-width:13"/><path d="M868,407 L894,407" style="stroke-width:11"/><path d="M868,521 L910,521" style="stroke-width:11"/><path d="M868,621 L894,621" style="stroke-width:11"/><path d="M868,735 L910,735" style="stroke-width:11"/><path d="M822,433 L798,433" style="stroke-width:11"/><path d="M822,561 L780,561" style="stroke-width:11"/><path d="M822,671 L798,671" style="stroke-width:11"/><path d="M810,808 L862,808" style="stroke-width:14"/></g><g class="p-coulee"><path d="M150,300 C240,250 320,330 300,420 C282,502 200,520 214,600 C226,672 320,690 380,650 C444,608 470,540 540,556 C612,572 640,650 720,630 C790,612 812,540 796,470"/><path d="M760,180 C688,232 620,214 566,254 C508,296 512,368 560,404 C612,442 690,414 736,452 C784,492 780,570 826,596"/><path d="M180,700 C260,742 340,724 400,760 C462,798 520,806 596,790 C672,774 720,806 790,790"/><path d="M120,470 C176,452 214,392 200,330 C188,274 216,214 276,192 C338,168 396,204 452,186 C508,168 546,120 616,132"/><path d="M430,560 C382,608 310,600 268,646 C226,692 236,760 200,796"/><path d="M640,300 C700,340 692,412 646,448 C600,484 604,548 654,566"/><circle cx="430" cy="400" r="136" stroke-dasharray="22 15"/><circle cx="430" cy="400" r="120" stroke-dasharray="9 20"/></g><g class="p-caps"><ellipse cx="255.4" cy="657.7" rx="9" ry="4.6" transform="rotate(29.3 255.4 657.7)"/><ellipse cx="303.5" cy="670.7" rx="9" ry="4.6" transform="rotate(3.1 303.5 670.7)"/><ellipse cx="432.7" cy="605.1" rx="9" ry="4.6" transform="rotate(-44.6 432.7 605.1)"/><ellipse cx="646.3" cy="619.3" rx="9" ry="4.6" transform="rotate(30.2 646.3 619.3)"/><ellipse cx="694.5" cy="633.3" rx="9" ry="4.6" transform="rotate(0.7 694.5 633.3)"/><ellipse cx="742.1" cy="621.8" rx="9" ry="4.6" transform="rotate(-26.2 742.1 621.8)"/><ellipse cx="800" cy="494" rx="9" ry="4.6" transform="rotate(-95.7 800 494)"/><ellipse cx="752.3" cy="185.3" rx="9" ry="4.6" transform="rotate(146.4 752.3 185.3)"/><ellipse cx="706.9" cy="207.9" rx="9" ry="4.6" transform="rotate(160 706.9 207.9)"/><ellipse cx="566" cy="254" rx="9" ry="4.6" transform="rotate(143.8 566 254)"/><ellipse cx="629.8" cy="426.2" rx="9" ry="4.6" transform="rotate(6 629.8 426.2)"/><ellipse cx="679.7" cy="430.9" rx="9" ry="4.6" transform="rotate(7.6 679.7 430.9)"/><ellipse cx="726.7" cy="445.5" rx="9" ry="4.6" transform="rotate(30.6 726.7 445.5)"/><ellipse cx="760.7" cy="482.1" rx="9" ry="4.6" transform="rotate(59.5 760.7 482.1)"/><ellipse cx="366.1" cy="745.2" rx="9" ry="4.6" transform="rotate(16.8 366.1 745.2)"/><ellipse cx="411.9" cy="767" rx="9" ry="4.6" transform="rotate(29.2 411.9 767)"/><ellipse cx="456.6" cy="786.7" rx="9" ry="4.6" transform="rotate(18.3 456.6 786.7)"/><ellipse cx="506.5" cy="796.9" rx="9" ry="4.6" transform="rotate(5.2 506.5 796.9)"/><ellipse cx="555.4" cy="796.4" rx="9" ry="4.6" transform="rotate(-5.5 555.4 796.4)"/><ellipse cx="605.6" cy="788.2" rx="9" ry="4.6" transform="rotate(-9.5 605.6 788.2)"/><ellipse cx="655.5" cy="785.8" rx="9" ry="4.6" transform="rotate(3.1 655.5 785.8)"/><ellipse cx="540.8" cy="142.1" rx="9" ry="4.6" transform="rotate(-23.7 540.8 142.1)"/><ellipse cx="589.1" cy="130.2" rx="9" ry="4.6" transform="rotate(-2.7 589.1 130.2)"/><ellipse cx="380.5" cy="591.6" rx="9" ry="4.6" transform="rotate(157.3 380.5 591.6)"/><ellipse cx="334.3" cy="608" rx="9" ry="4.6" transform="rotate(161 334.3 608)"/><ellipse cx="288.7" cy="628.6" rx="9" ry="4.6" transform="rotate(147.3 288.7 628.6)"/><ellipse cx="254.2" cy="664.7" rx="9" ry="4.6" transform="rotate(121.1 254.2 664.7)"/><ellipse cx="682.7" cy="376.7" rx="9" ry="4.6" transform="rotate(90.9 682.7 376.7)"/><ellipse cx="668.2" cy="423.6" rx="9" ry="4.6" transform="rotate(122.2 668.2 423.6)"/><ellipse cx="714.1" cy="663.8" rx="9" ry="4.6" transform="rotate(145.6 714.1 663.8)"/><ellipse cx="595.8" cy="682.6" rx="9" ry="4.6" transform="rotate(122 595.8 682.6)"/><ellipse cx="860.3" cy="794.9" rx="9" ry="4.6" transform="rotate(53.8 860.3 794.9)"/><ellipse cx="657.7" cy="690" rx="9" ry="4.6" transform="rotate(82 657.7 690)"/><ellipse cx="674.4" cy="159.4" rx="9" ry="4.6" transform="rotate(60.4 674.4 159.4)"/><ellipse cx="836.5" cy="826.5" rx="9" ry="4.6" transform="rotate(46.6 836.5 826.5)"/><ellipse cx="630.5" cy="675.1" rx="9" ry="4.6" transform="rotate(169.5 630.5 675.1)"/><ellipse cx="713.1" cy="216.4" rx="9" ry="4.6" transform="rotate(6.1 713.1 216.4)"/><ellipse cx="682.1" cy="232.5" rx="9" ry="4.6" transform="rotate(67.4 682.1 232.5)"/><ellipse cx="586.1" cy="755" rx="9" ry="4.6" transform="rotate(112.4 586.1 755)"/><ellipse cx="557.9" cy="552.1" rx="9" ry="4.6" transform="rotate(134.6 557.9 552.1)"/><ellipse cx="675.5" cy="706.5" rx="9" ry="4.6" transform="rotate(65.2 675.5 706.5)"/><ellipse cx="482" cy="712.3" rx="9" ry="4.6" transform="rotate(59.4 482 712.3)"/><ellipse cx="784.1" cy="185.1" rx="9" ry="4.6" transform="rotate(113.4 784.1 185.1)"/><ellipse cx="150.5" cy="647.4" rx="9" ry="4.6" transform="rotate(64.3 150.5 647.4)"/><ellipse cx="847.8" cy="741.7" rx="9" ry="4.6" transform="rotate(60.5 847.8 741.7)"/><ellipse cx="558.5" cy="758.4" rx="9" ry="4.6" transform="rotate(2.1 558.5 758.4)"/><ellipse cx="272.6" cy="575" rx="9" ry="4.6" transform="rotate(62.4 272.6 575)"/><ellipse cx="120.5" cy="749.9" rx="9" ry="4.6" transform="rotate(15.1 120.5 749.9)"/><ellipse cx="146.4" cy="701.2" rx="9" ry="4.6" transform="rotate(10.6 146.4 701.2)"/><ellipse cx="772.4" cy="278.6" rx="9" ry="4.6" transform="rotate(62.8 772.4 278.6)"/><ellipse cx="419.5" cy="604.5" rx="9" ry="4.6" transform="rotate(76.6 419.5 604.5)"/><ellipse cx="548.1" cy="119.7" rx="9" ry="4.6" transform="rotate(117.8 548.1 119.7)"/><ellipse cx="478.1" cy="627.3" rx="9" ry="4.6" transform="rotate(28.1 478.1 627.3)"/><ellipse cx="771.7" cy="220.7" rx="9" ry="4.6" transform="rotate(164 771.7 220.7)"/><ellipse cx="132.4" cy="816.2" rx="9" ry="4.6" transform="rotate(117.5 132.4 816.2)"/><ellipse cx="472.6" cy="784.2" rx="9" ry="4.6" transform="rotate(0.3 472.6 784.2)"/><ellipse cx="728.7" cy="747.6" rx="9" ry="4.6" transform="rotate(46.1 728.7 747.6)"/><ellipse cx="588.8" cy="742.7" rx="9" ry="4.6" transform="rotate(137 588.8 742.7)"/><ellipse cx="824.3" cy="784.1" rx="9" ry="4.6" transform="rotate(135.9 824.3 784.1)"/><ellipse cx="713.1" cy="644.9" rx="9" ry="4.6" transform="rotate(173.8 713.1 644.9)"/><ellipse cx="619.3" cy="122.3" rx="9" ry="4.6" transform="rotate(2.3 619.3 122.3)"/><ellipse cx="477.1" cy="613.7" rx="9" ry="4.6" transform="rotate(4.3 477.1 613.7)"/><ellipse cx="150.5" cy="213.6" rx="9" ry="4.6" transform="rotate(19.7 150.5 213.6)"/><ellipse cx="355.2" cy="615.2" rx="9" ry="4.6" transform="rotate(119 355.2 615.2)"/><ellipse cx="531.2" cy="623.1" rx="9" ry="4.6" transform="rotate(95.4 531.2 623.1)"/><ellipse cx="802" cy="629.1" rx="9" ry="4.6" transform="rotate(169.3 802 629.1)"/><ellipse cx="515.6" cy="215.8" rx="9" ry="4.6" transform="rotate(88.2 515.6 215.8)"/><ellipse cx="136.1" cy="315.8" rx="9" ry="4.6" transform="rotate(177.3 136.1 315.8)"/><ellipse cx="277.5" cy="268.1" rx="9" ry="4.6" transform="rotate(86 277.5 268.1)"/><ellipse cx="701" cy="378.2" rx="9" ry="4.6" transform="rotate(84.5 701 378.2)"/><ellipse cx="463.8" cy="671.6" rx="9" ry="4.6" transform="rotate(44.6 463.8 671.6)"/><ellipse cx="791.5" cy="476.4" rx="9" ry="4.6" transform="rotate(34 791.5 476.4)"/><ellipse cx="487.6" cy="587.6" rx="9" ry="4.6" transform="rotate(126.4 487.6 587.6)"/><ellipse cx="778.7" cy="273.4" rx="9" ry="4.6" transform="rotate(175.3 778.7 273.4)"/><ellipse cx="173.7" cy="225.9" rx="9" ry="4.6" transform="rotate(118.5 173.7 225.9)"/><ellipse cx="701.4" cy="641.3" rx="9" ry="4.6" transform="rotate(17.4 701.4 641.3)"/><ellipse cx="771.7" cy="121.7" rx="9" ry="4.6" transform="rotate(78.6 771.7 121.7)"/><ellipse cx="800.8" cy="334.7" rx="9" ry="4.6" transform="rotate(63 800.8 334.7)"/><ellipse cx="634.2" cy="359.8" rx="9" ry="4.6" transform="rotate(140.2 634.2 359.8)"/><ellipse cx="233" cy="495.2" rx="9" ry="4.6" transform="rotate(37.9 233 495.2)"/><ellipse cx="747.3" cy="185" rx="9" ry="4.6" transform="rotate(98.9 747.3 185)"/></g><g class="p-piece"><circle cx="430" cy="400" r="150"/><circle cx="430" cy="400" r="88"/><path d="M214,400 A216,216 0 0 1 227,326.1 L155.6,300.1 A292,292 0 0 0 138,400 Z"/><path d="M234.2,308.7 A216,216 0 0 1 272,252.7 L228.1,211.8 A276,276 0 0 0 179.9,283.4 Z"/><path d="M282.7,242 A216,216 0 0 1 352.6,198.3 L321.1,116.2 A304,304 0 0 0 222.7,177.7 Z"/><path d="M363.3,194.6 A216,216 0 0 1 437.5,184.1 L440.3,106.2 A294,294 0 0 0 339.1,120.4 Z"/><path d="M460.1,186.1 A216,216 0 0 1 517.9,202.7 L539,155.2 A268,268 0 0 0 467.3,134.6 Z"/><path d="M538,212.9 A216,216 0 0 1 595.5,261.2 L658.3,208.4 A298,298 0 0 0 579,141.9 Z"/><path d="M606.9,276.1 A216,216 0 0 1 636.6,336.8 L701.6,317 A284,284 0 0 0 662.6,237.1 Z"/><path d="M639.6,452.3 A216,216 0 0 1 563,570.2 L613.5,634.8 A298,298 0 0 0 719.1,472.1 Z"/><path d="M260.2,563.9 A236,236 0 0 1 195.3,424.7 L79.9,436.8 A352,352 0 0 0 176.8,644.5 Z"/><path d="M327.7,734.7 A350,350 0 0 1 205,668.1 L147.2,737.1 A440,440 0 0 0 301.4,820.8 Z"/><path d="M421.4,645.9 A246,246 0 0 1 337.8,628.1 L313.1,689.3 A312,312 0 0 0 419.1,711.8 Z"/><rect x="368" y="812" width="300" height="106" rx="4"/><rect x="706" y="772" width="104" height="74" rx="5"/><rect x="890" y="362" width="30" height="26" rx="3"/><rect x="890" y="394" width="30" height="26" rx="3"/><rect x="890" y="426" width="30" height="26" rx="3"/><rect x="906" y="492" width="30" height="26" rx="3"/><rect x="906" y="524" width="30" height="26" rx="3"/><rect x="890" y="576" width="30" height="26" rx="3"/><rect x="890" y="608" width="30" height="26" rx="3"/><rect x="890" y="640" width="30" height="26" rx="3"/><rect x="906" y="706" width="30" height="26" rx="3"/><rect x="906" y="738" width="30" height="26" rx="3"/><rect x="772" y="404" width="30" height="26" rx="3"/><rect x="772" y="436" width="30" height="26" rx="3"/><rect x="754" y="516" width="30" height="26" rx="3"/><rect x="754" y="548" width="30" height="26" rx="3"/><rect x="754" y="580" width="30" height="26" rx="3"/><rect x="772" y="642" width="30" height="26" rx="3"/><rect x="772" y="674" width="30" height="26" rx="3"/></g><g class="p-tiret"><path d="M180,890 L212,826"/></g><g class="p-nom"><text x="385.7" y="85.1" text-anchor="middle">Salles de cérémonie</text><text x="223.4" y="496.4" text-anchor="middle">Préparateurs</text><text x="271.3" y="698.4" text-anchor="middle">Analystes</text><text x="380.5" y="632.8" text-anchor="middle">Salle de repos</text><text x="518" y="871" text-anchor="middle">Accueil</text><text x="646.4" y="540.5" text-anchor="middle">Consultation</text><text x="918" y="326" text-anchor="middle" transform="rotate(90 918 326)">Chambres</text><text x="758" y="764" text-anchor="middle">Réfectoire</text><text x="430" y="404" text-anchor="middle">Registre</text><text x="168" y="906" text-anchor="middle">La serre</text><text x="516" y="986" text-anchor="middle">Entrée principale</text></g></svg>';

const FICHES={
  'fiche-nicolas':{n:'Nicolas',num:'812 665',dh:'an 1147, jour 214 — 8 h 50',g:1,
    age:'quarante-deux ans',jar:'dans trente-quatre ans',
    obs:'Remontée lente. Sans suite.',
    pal:'environ trente ans',
    encre:'<path d="M20 50 C 78 64 140 88 204 96" fill="none" stroke="var(--encre)" stroke-width="1.5" stroke-linecap="round"/><path d="M16.4 46.4 L23.6 53.6 M23.6 46.4 L16.4 53.6" fill="none" stroke="var(--encre)" stroke-width="1.2" stroke-linecap="round"/>'},
  'fiche-eliott':{n:'Eliott',num:'812 664',dh:'an 1147, jour 214 — 8 h 40',g:1,
    age:'dix ans',jar:'dans six ans',
    pal:'au moins trente-quatre ans',
    encre:'<path d="M20 86 C 36 88 54 94 72 96" fill="none" stroke="var(--encre)" stroke-width="1.5" stroke-linecap="round"/><path d="M16.4 82.4 L23.6 89.6 M23.6 82.4 L16.4 89.6" fill="none" stroke="var(--encre)" stroke-width="1.2" stroke-linecap="round"/>'}
};

function htmlPlan(){
  return '<div class="planche"><div>'
    +'<p class="p-tete">Plan de la ruche</p>'
    + PLAN_RUCHE + '</div></div>';
}

function htmlEncart(clef){
  if(clef==='plan-ruche') return htmlPlan();
  const f=FICHES[clef];
  if(!f) return '';
  const li=function(s,v){
    return '<div><span>'+s+'</span><b>'+v+'</b></div>' };
  const svg='<svg viewBox="0 0 330 144" width="100%" preserveAspectRatio="xMidYMid meet" aria-hidden="true">'
    +'<path d="M20 8 L20 128 L312 128" fill="none" stroke="var(--encre-3)" stroke-width=".7" opacity=".6"/>'
    +'<path d="M20 96 H312" fill="none" stroke="var(--encre-3)" stroke-width=".7" stroke-dasharray="1.5 3" opacity=".5"/>'
    +'<path d="M20 16 C 84 34 156 74 236 96" fill="none" stroke="var(--encre-3)" stroke-width=".9"/>'
    +'<path d="M20 122 C 32 116 40 99 56 96" fill="none" stroke="var(--encre-3)" stroke-width=".9"/>'
    +'<path d="M56 96 H288" fill="none" stroke="var(--encre-3)" stroke-width=".9"/>'
    +'<path d="M288 96 C 298 100 304 114 308 128" fill="none" stroke="var(--encre-3)" stroke-width=".9" stroke-dasharray="2 2.5" opacity=".7"/>'
    + f.encre
    +'<g class="f-lg">'
    +'<text x="28" y="13">moyenne haute</text>'
    +'<text x="46" y="126">moyenne basse</text>'
    +'<text x="108" y="91">palier d’insouciance</text>'
    +'<text x="11" y="68" transform="rotate(-90 11 68)">âge</text>'
    +'<text x="312" y="139" text-anchor="end">temps</text>'
    +'</g></svg>';
  return '<div class="fiche"><div class="f-corps">'
    +'<p class="f-tete">Fiche de placement</p>'
    +'<p class="f-sous">à remplir par le veilleur · à déposer au registre</p>'
    +'<div class="f-champs">'
    + li('Prénom',f.n) + li('Numéro',f.num)
    + li('Date et heure',f.dh)
    +'<div><span>Sexe</span><b class="f-opt">'
    +'<i class="c'+(f.g?' c-on':'')+'"></i>garçon'
    +'<i class="c c-b'+(f.g?'':' c-on')+'"></i>fille</b></div>'
    + li('Âge de l’arrivant',f.age)
    +'</div>'
    +'<p class="f-consigne">Porter l’arrivant sur la courbe.</p>'
    + svg
    +'<div class="f-case"><div class="f-champs f-nb">'
    + li('Entrée au jardin',f.jar) + li('Palier d’insouciance',f.pal)
    +'</div><p class="f-est">estimations moyennes</p></div>'
    +'<div class="f-case f-obs"><p class="f-clef">Observations</p>'
    +'<div class="f-lignes">'
    + (f.obs ? '<b class="f-note">'+f.obs+'</b>' : '')
    +'<i></i><i></i><i></i></div></div>'
    +'<div class="f-pied">'
    +'<span class="f-clef">Veilleur</span>'
    +'<span class="f-trait"><i class="f-sign">Andrew</i></span>'
    +'</div>'
    +'</div></div>';
}

function teteChap(ch){
  const d=document.createElement('div');
  d.className='ouvre';
  d.innerHTML='<h2>'+ch.rang+'</h2>'
    + (ch.quand ? '<p class="quand">'+ch.quand+'</p>' : '');
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

  /* Derniere ligne trop courte ? On recule d'une ligne ENTIERE. Celle
     qui devient la derniere appartient au flux naturel du paragraphe :
     elle est pleine, elle se justifiera sans s'etirer, et on ne perd
     qu'une ligne en bas de page. */
  if(largeurDerniereLigne(n)<TW*.82){
    const lignes=Math.round(n.offsetHeight/LH);
    if(lignes>=3){
      let lo=4, hi=best-1, court=0;
      while(lo<=hi){
        const mid=(lo+hi)>>1;
        n.innerHTML=rendre(t.mots.slice(0,mid),t.gard);
        if(Math.round(n.offsetHeight/LH)<=lignes-1){ court=mid; lo=mid+1 }
        else hi=mid-1;
      }
      if(court>=4){
        n.innerHTML=rendre(t.mots.slice(0,court),t.gard);
        if(largeurDerniereLigne(n)>=TW*.82) best=court;
      }
    }
    n.innerHTML=rendre(t.mots.slice(0,best),t.gard);
  }

  /* Derniere ligne toujours courte ? On ne coupe pas. Le paragraphe
     entier passe a la page suivante : deux ou trois lignes de blanc en
     bas de page valent mieux qu'une phrase coupee qui ne se voit pas. */
  if(largeurDerniereLigne(n)<TW*.82){ banc.removeChild(n); return null }
  n.className=(n.className+' coupe').trim();
  if(!tient()){ banc.removeChild(n); return null }
  return {apres:[it[0], rendre(t.mots.slice(best),t.gard), it[2], 1]};
}

function paginer(){
  PAGES.length=0;
  PAGES.push({type:'garde'});
  PAGES.push({type:'titre'});
  PAGES.push({type:'blanc'});
  PAGES.push({type:'sommaire'});
  PAGES.push({type:'blanc'});

  LIVRE.forEach(function(ch,ci){
    /* l'encart precede le chapitre, seul sur sa page de droite */
    if(ch.encart){
      const kk=ch.encart.split('|');
      /* deux fiches se lisent en vis-a-vis : la premiere tombe
         sur une page de gauche, donc sur un index pair. Seule,
         une fiche prend la page de droite. */
      const veut = kk.length>1 ? 1 : 0;
      if(PAGES.length%2===veut) PAGES.push({type:'blanc'});
      kk.forEach(function(k){ PAGES.push({type:'def',ch:ci,k:k}) });
    }
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
        /* saut demande par l'autrice : on ferme la page, sauf si elle
           est encore vide -- sinon on n'avancerait jamais */
        if((it[3]&4) && (pose>0 || ouverture)) break;
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
  /* le livre n'est pas fini : on le dit, sinon le lecteur croit que
     son fichier l'est. Belle page, comme un chapitre. */
  if(PAGES.length%2===0) PAGES.push({type:'blanc'});
  PAGES.push({type:'suite'});
  /* et rien apres : le contre-plat de fin ne se voit jamais dans un
     vrai livre, la couverture se referme dessus. Ici il se retrouvait
     seul en face d'une page blanche. */
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
  if(p.type==='suite'){ d.innerHTML='<div class="suite"><span>À suivre</span></div>'; return d }
  if(p.type==='def'){ d.innerHTML=htmlEncart(p.k); return d }
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
    /* du fond vers l'oeil : face k, son voile, face k+1, son voile */
    const zf=(k*.12).toFixed(3)+'px', zv=(k*.12+.06).toFixed(3)+'px';
    const parts=[];
    ['recto','verso'].forEach(function(quel,i){
      const dos=(i===0?'':'rotateY(180deg) ');
      const f=document.createElement('div'); f.className='face '+quel;
      f.style.transform=dos+'translateZ('+zf+')';
      const fen=document.createElement('div'); fen.className='fen';
      /* le recto se lit depuis la reliure, le verso depuis son bord oppose */
      fen.style.left=(i===0 ? -k*LW : -({{PW}}-(k+1)*LW))+'px';
      f.appendChild(fen); lame.appendChild(f);
      const lu=document.createElement('div');
      lu.className='voile '+(i===0?'av':'ar');
      lu.style.transform=dos+'translateZ('+zv+')';
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
    const entree=cumul;
    cumul+=a;
    /* Une lame de chant ne recoit plus la lumiere. sin carre, et pas
       1 - |cos| : les deux ont la meme forme, mais |cos| fait un angle
       vif a 90 degres, en plein dans le moment ou la page tourne le
       plus vite. On voyait la cassure. */
    /* Le voile va de l'ombre du bord d'entree a celle du bord de sortie,
       et la sortie de l'une est l'entree de la suivante : l'ombre court
       sans marche d'un bout a l'autre de la feuille. */
    const o0=(.62*Math.pow(Math.sin(entree*Math.PI/180),2)).toFixed(3);
    const o1=(.62*Math.pow(Math.sin(cumul*Math.PI/180),2)).toFixed(3);
    LAMES[k].r.lu.style.backgroundImage=
      'linear-gradient(90deg,rgba(0,0,0,'+o0+'),rgba(0,0,0,'+o1+'))';
    LAMES[k].v.lu.style.backgroundImage=
      'linear-gradient(270deg,rgba(0,0,0,'+o0+'),rgba(0,0,0,'+o1+'))';
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
    if(anime) return;   /* un autre tour a repris la main entre-temps */
    feuille.hidden=true;
    LAMES.forEach(function(L){
      L.lame.style.transform='rotateY(0deg)';
      L.r.lu.style.backgroundImage='none';
    L.v.lu.style.backgroundImage='none';
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
  $('corneg').hidden=true;
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
  $('corneg').hidden=ferme || $('prec').disabled;
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
  else if((PAGES[d]&&PAGES[d].type==='def')||(PAGES[g]&&PAGES[g].type==='def')){
    txt='Fiche';
  }
  else if((PAGES[d]&&PAGES[d].type==='suite')||(PAGES[g]&&PAGES[g].type==='suite')){
    txt='À suivre';
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
$('corneg').addEventListener('click',function(){tourner(-1)});
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
