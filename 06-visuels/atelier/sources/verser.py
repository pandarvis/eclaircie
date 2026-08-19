# -*- coding: utf-8 -*-
"""Verse le brouillon markdown d'un chapitre dans le corps de l'atelier.
   usage : python verser.py <fichier.md> <id-du-chapitre>"""
import io, sys

src, cible = sys.argv[1], sys.argv[2]
B = u'`'

brut = io.open(src, encoding='utf-8').read()
blocs = [x.strip() for x in brut.split(u'\n\n') if x.strip()]

lignes = []
for i, x in enumerate(blocs):
    dernier = (i == len(blocs) - 1)
    if x == u'· · ·':
        lignes.append(u'[%spause%s,%s· · ·%s],' % (B, B, B, B))
    elif x.startswith(u'—'):
        lignes.append(u'[%stiret%s,%s%s%s],' % (B, B, B, x, B))
    elif dernier:
        lignes.append(u'[%sp%s,%s%s%s,%sfin%s],' % (B, B, B, x, B, B, B))
    else:
        lignes.append(u'[%sp%s,%s%s%s],' % (B, B, B, x, B))

f = 'pB-textes.js'
s = io.open(f, encoding='utf-8').read()
deb = s.index(u'id: %s%s%s' % (B, cible, B))
d0 = s.index(u'  p: [', deb)
d1 = s.index(u'\n  ],', d0)
neuf = u'  p: [\n\n' + u'\n'.join(lignes) + u'\n'
s = s[:d0] + neuf + s[d1 + 1:]
io.open(f, 'w', encoding='utf-8').write(s)

mots = len(u' '.join(blocs).split())
print(u'%d blocs, %d mots verses dans %s' % (len(blocs), mots, cible))
