# -*- coding: utf-8 -*-
u"""Pose un blanc d'une ligne entre deux paragraphes.

  python poser-un-blanc.py "fin du paragraphe qui precede"
  python poser-un-blanc.py "fin du precedent" "debut du suivant"
  python poser-un-blanc.py --oter "fin du paragraphe qui precede"

La premiere ancre est la FIN du paragraphe apres lequel le blanc doit
tomber : un bout de phrase suffit, du moment qu'il ne se trouve qu'a un
endroit du manuscrit. On refuse de travailler si l'ancre est absente ou
ambigue -- poser un blanc au mauvais endroit ne se voit pas tout de
suite.

La seconde ancre, facultative, est le DEBUT du paragraphe qui suit. Elle
sert quand deux chapitres contiennent le meme paragraphe, mot pour mot :
<< Andrew ne repondit pas. >> finit un paragraphe au chapitre troisieme
et un autre au quatrieme, et aucun allongement de la premiere ancre ne
les separe. C'est aussi la facon dont l'autrice formule ses demandes --
<< un blanc entre ceci et cela >>.

Un blanc est une PAUSE SANS MARQUE. Le genre pause existe deja dans les
huit outils qui lisent le manuscrit ; seule sa presentation change, et
elle tient en une regle CSS dans chacun des trois supports. Inventer un
genre pour ca, c'etait huit endroits a ne pas rater.

  [pause] avec les trois points  ->  une rupture de scene, trois lignes
  [pause] avec rien dedans       ->  un blanc d'une ligne, sans marque

Relancer  sh fabriquer.sh  ensuite : l'atelier, la version de lecture et
le livre se refont ensemble.
"""
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ICI = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(ICI, 'pB-textes.js')
B = chr(96)
BLANC = u'[' + B + u'pause' + B + u',' + B + B + u'],\n'
DEBUT = re.compile(u'\\[' + B + u'(?:p|tiret|pause)' + B + u',' + B
                   + u'([^' + B + u']*)')


def sortir(message):
    print(message)
    sys.exit(1)


def lisible(txt):
    return re.sub(r'<[^>]+>', u'', txt)


args = [a for a in sys.argv[1:] if a != '--oter']
oter = '--oter' in sys.argv[1:]
if not args or len(args) > 2:
    sortir(__doc__.strip())

args = [a.decode('utf-8') if isinstance(a, bytes) else a for a in args]
ancre = args[0].strip()
suite = args[1].strip() if len(args) > 1 else None
if not ancre:
    sortir(u'PROBLEME : ancre vide.')
if B in ancre or (suite and B in suite):
    sortir(u'PROBLEME : une ancre ne peut pas contenir un accent grave.')

s = io.open(F, encoding='utf-8').read()
bornes = [(m.group(1), m.start())
          for m in re.finditer(r'\n  id: `([a-z0-9-]+)`,', s)]

# La fin d'un paragraphe, c'est l'ancre suivie de la fermeture de la ligne.
FIN = ancre + B + u'],\n'
places = [m.start() for m in re.finditer(re.escape(FIN), s)]

if not places:
    if ancre not in s:
        sortir(u'PROBLEME : introuvable dans le manuscrit :\n           ' + ancre)
    sortir(u'PROBLEME : trouve %d fois dans le texte, mais jamais en FIN de\n'
           u'           paragraphe. L ancre doit finir le paragraphe :\n'
           u'           %s' % (s.count(ancre), ancre))

# La seconde ancre departage : on garde les endroits ou le paragraphe
# suivant commence bien par elle.
if suite:
    gardes = []
    for p in places:
        # Un blanc deja pose s'interpose : on regarde le paragraphe qui
        # suit VRAIMENT, sinon --oter ne retrouverait jamais sa place.
        apres = p + len(FIN)
        if s[apres:].startswith(BLANC):
            apres += len(BLANC)
        m = DEBUT.search(s, apres)
        if m and lisible(m.group(1)).startswith(suite):
            gardes.append(p)
    if not gardes:
        sortir(u'PROBLEME : nulle part le paragraphe suivant ne commence par :\n'
               u'           ' + suite)
    places = gardes

if len(places) > 1:
    ou = u', '.join(sorted(set(
        [x for x, d in bornes if d < p][-1] for p in places)))
    sortir(u'PROBLEME : %d paragraphes finissent par cette ancre (%s).\n'
           u'           Allongez-la, ou donnez le debut du paragraphe suivant\n'
           u'           en second argument.' % (len(places), ou))

place = places[0]
chapitre = [x for x, d in bornes if d < place][-1]

verrous = io.open(os.path.join(ICI, 'textes-verrouilles.txt'),
                  encoding='utf-8').read()
if re.search(r'^' + re.escape(chapitre) + r'\s+[0-9a-f]{64}', verrous, re.M):
    sortir(u'PROBLEME : %s est verrouille.\n'
           u'           python verrouiller-les-textes.py --ouvrir %s'
           % (chapitre, chapitre))

deja = s[place + len(FIN):].startswith(BLANC)
if oter:
    if not deja:
        sortir(u'PROBLEME : il n y a pas de blanc juste apres cette ancre.')
    s = s[:place] + FIN + s[place + len(FIN) + len(BLANC):]
    fait = u'ote'
else:
    if deja:
        sortir(u'PROBLEME : il y a deja un blanc juste apres cette ancre.')
    s = s[:place] + FIN + BLANC + s[place + len(FIN):]
    fait = u'pose'

open(F, 'wb').write(s.encode('utf-8'))

m = DEBUT.search(s, place + len(FIN) + (0 if oter else len(BLANC)))
print(u'blanc %s dans %s' % (fait, chapitre))
print(u'  avant : …' + ancre[-58:])
if m:
    print(u'  apres : ' + lisible(m.group(1))[:58] + u'…')
print(u'\nrelancer :  sh fabriquer.sh')
