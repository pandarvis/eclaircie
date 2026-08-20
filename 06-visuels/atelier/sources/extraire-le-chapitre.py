# -*- coding: utf-8 -*-
"""Regenere un brouillon markdown depuis le texte de l'atelier.

L'atelier est la source ; 05-manuscrit/chapitres/en-cours/ en est un
miroir lisible. Ce script fait le trajet dans ce sens-la, et jamais
l'autre -- verser.py fait l'inverse, pour un texte qui arrive du dehors.

  python extraire-le-chapitre.py chapitre-1
  python extraire-le-chapitre.py --tous

A lancer apres chaque correction, et notamment apres
reprendre-la-revision.py : un brouillon qui diverge en silence est
exactement la panne qu'on a deja payee deux fois.
"""
import io
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
JS = os.path.join(ICI, 'pB-textes.js')
DST = os.path.abspath(os.path.join(ICI, '..', '..', '..',
                                   '05-manuscrit', 'chapitres', 'en-cours'))

js = io.open(JS, encoding='utf-8').read()

# Les bornes de chaque chapitre dans le tableau.
bornes = [(m.group(1), m.start()) for m in re.finditer(r'id: `([a-z0-9-]+)`,', js)]
assert bornes, u'aucun chapitre dans pB-textes.js'


def paragraphes(i, j):
    out = []
    for k, t in re.findall(r'\[`(p|tiret|pause)`,`([^`]*)`', js[i:j]):
        t = re.sub(r'<[^>]+>', u'', t)          # le markdown n'a pas de balises
        out.append(t)
    return out


def extraire(nom):
    for n, (ident, deb) in enumerate(bornes):
        if ident == nom:
            fin = bornes[n + 1][1] if n + 1 < len(bornes) else len(js)
            paras = paragraphes(deb, fin)
            assert paras, u'chapitre vide : ' + nom
            cible = os.path.join(DST, nom + '-en-cours.md')
            if not os.path.exists(cible):
                # On ne cree pas de brouillon : en-cours ne contient que ce
                # qui est en cours. Un epilogue fini n'y a pas sa place.
                print(u'  %-12s pas de brouillon ouvert, on passe' % nom)
                return
            avant = io.open(cible, encoding='utf-8').read()
            texte = u'\n\n'.join(paras) + u'\n'
            if u' '.join(avant.split()) == u' '.join(texte.split()):
                print(u'  %-12s deja en phase (%d paragraphes)' % (nom, len(paras)))
                return
            open(cible, 'wb').write(texte.encode('utf-8'))
            print(u'  %-12s %d paragraphes ecrits dans %s'
                  % (nom, len(paras), os.path.basename(cible)))
            return
    raise SystemExit(u'chapitre inconnu : %s (connus : %s)'
                     % (nom, u', '.join(b[0] for b in bornes)))


args = sys.argv[1:]
if not args:
    raise SystemExit(u'usage : extraire-le-chapitre.py <id> | --tous\n'
                     u'  chapitres : ' + u', '.join(b[0] for b in bornes))
for nom in ([b[0] for b in bornes] if args[0] == '--tous' else args):
    extraire(nom)
