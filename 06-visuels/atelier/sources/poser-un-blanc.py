# -*- coding: utf-8 -*-
u"""Pose un blanc d'une ligne entre deux paragraphes.

  python poser-un-blanc.py "fin du paragraphe qui precede"
  python poser-un-blanc.py --oter "fin du paragraphe qui precede"

L'ancre est la FIN du paragraphe apres lequel le blanc doit tomber : un
bout de phrase suffit, du moment qu'il ne se trouve qu'a un endroit du
manuscrit. On refuse de travailler si l'ancre est absente ou ambigue --
poser un blanc au mauvais endroit ne se voit pas tout de suite.

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


def sortir(message):
    print(message)
    sys.exit(1)


args = [a for a in sys.argv[1:] if a != '--oter']
oter = '--oter' in sys.argv[1:]
if len(args) != 1:
    sortir(__doc__.strip())

ancre = args[0].decode('utf-8') if isinstance(args[0], bytes) else args[0]
ancre = ancre.strip()
if not ancre:
    sortir(u'PROBLEME : ancre vide.')
if B in ancre:
    sortir(u'PROBLEME : l ancre ne peut pas contenir un accent grave.')

s = io.open(F, encoding='utf-8').read()

# La fin d'un paragraphe, c'est l'ancre suivie de la fermeture de la ligne.
FIN = ancre + B + u'],\n'
n = s.count(FIN)
if n == 0:
    if s.count(ancre) == 0:
        sortir(u'PROBLEME : introuvable dans le manuscrit :\n           ' + ancre)
    sortir(u'PROBLEME : trouve %d fois dans le texte, mais jamais en FIN de\n'
           u'           paragraphe. L ancre doit finir le paragraphe :\n'
           u'           ' % s.count(ancre) + ancre)
if n > 1:
    sortir(u'PROBLEME : %d paragraphes finissent par cette ancre. Allongez-la.'
           % n)

# Quel chapitre ?
bornes = [(m.group(1), m.start()) for m in re.finditer(r'\n  id: `([a-z0-9-]+)`,', s)]
place = s.index(FIN)
chapitre = [x for x, d in bornes if d < place][-1]

verrous = io.open(os.path.join(ICI, 'textes-verrouilles.txt'), encoding='utf-8').read()
if re.search(r'^' + re.escape(chapitre) + r'\s+[0-9a-f]{64}', verrous, re.M):
    sortir(u'PROBLEME : %s est verrouille.\n'
           u'           python verrouiller-les-textes.py --ouvrir %s'
           % (chapitre, chapitre))

if oter:
    if s.count(FIN + BLANC) != 1:
        sortir(u'PROBLEME : il n y a pas de blanc juste apres cette ancre.')
    s = s.replace(FIN + BLANC, FIN, 1)
    fait = u'ote'
else:
    if s.count(FIN + BLANC) == 1:
        sortir(u'PROBLEME : il y a deja un blanc juste apres cette ancre.')
    s = s.replace(FIN, FIN + BLANC, 1)
    fait = u'pose'

open(F, 'wb').write(s.encode('utf-8'))

apres = s[s.index(FIN) + len(FIN):]
suivant = re.search(r'\[' + B + r'(?:p|tiret)' + B + r',' + B + r'([^' + B + r']*)',
                    apres)
print(u'blanc %s dans %s' % (fait, chapitre))
print(u'  avant : …' + ancre[-58:])
if suivant:
    print(u'  apres : ' + re.sub(r'<[^>]+>', u'', suivant.group(1))[:58] + u'…')
print(u'\nrelancer :  sh fabriquer.sh')
