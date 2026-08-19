# -*- coding: utf-8 -*-
"""Etat de la frise : une ligne par scene, triee par colonne."""
import io, re
s = io.open('p5-scenes.js', encoding='utf-8').read()
pat = re.compile(r"id:\s*`([^`]+)`,\s*no:\s*`([^`]*)`(?:,\s*ecrit:\s*\w+)?,\s*col:\s*(\d+),\s*row:\s*`([^`]+)`,\s*acte:\s*`([^`]*)`")
lignes = []
for m in pat.finditer(s):
    i = s.index(u'titre:', m.end())
    j = s.index(u'`', s.index(u'`', i) + 1)
    titre = s[s.index(u'`', i) + 1:j]
    lignes.append((int(m.group(3)), m.group(4), m.group(1), m.group(2), m.group(5), titre))
lignes.sort()
out = []
for col, row, ident, no, acte, titre in lignes:
    out.append(u'col %2d  %-7s  %-12s  %-22s  %-22s  %s' % (col, row, ident, no, acte, titre))
io.open('grille.txt', 'w', encoding='utf-8').write(u'\n'.join(out))
print(u'%d scenes -> grille.txt' % len(lignes))
