# -*- coding: utf-8 -*-
"""Verse le glossaire du livre dans l'atelier.

La source est 05-manuscrit/glossaire.md — c'est une page du livre, pas une
fiche de travail. L'atelier n'en est qu'un miroir : on corrige le markdown,
on relance ce script, on refabrique.
"""
import io
import re

SRC = u"R:/Documents/l'Eclaircie/05-manuscrit/glossaire.md"
DST = 'p7-monde.js'

md = io.open(SRC, encoding='utf-8').read()

# Chaque entree est un paragraphe qui commence par **Mot.**
entrees = []
for bloc in re.split(r'\n\s*\n', md):
    bloc = bloc.strip()
    m = re.match(r'^\*\*(.+?)\.\*\*\s+(.*)$', bloc, re.S)
    if not m:
        continue
    mot = m.group(1).strip()
    definition = u' '.join(m.group(2).split())
    entrees.append((mot, definition))

assert entrees, u'aucune entree trouvee'

# Verification : l'ordre alphabetique, accents et articles ignores.
def cle(mot):
    t = mot.lower()
    for a, b in ((u'é', 'e'), (u'è', 'e'), (u'ê', 'e'), (u'à', 'a'),
                 (u'ç', 'c'), (u'ô', 'o'), (u'û', 'u'), (u'î', 'i'), (u'«', ''), (u'"', '')):
        t = t.replace(a, b)
    return t.strip()

ordonne = sorted(entrees, key=lambda e: cle(e[0]))
desordre = [a[0] for a, b in zip(entrees, ordonne) if a[0] != b[0]]
if desordre:
    print(u'ATTENTION, hors ordre alphabetique : %s' % u', '.join(desordre))

B = '`'
lignes = [u'[%s%s%s,%s%s%s],' % (B, mot, B, B, d, B) for mot, d in entrees]
bloc = u'const GLOSSAIRE = [\n' + u'\n'.join(lignes) + u'\n];\n'

s = io.open(DST, encoding='utf-8').read()
if 'const GLOSSAIRE = [' in s:
    d = s.index('const GLOSSAIRE = [')
    f = s.index('\n];\n', d) + 4
    s = s[:d] + bloc + s[f:]
else:
    anc = 'const REGLES = ['
    assert anc in s
    s = s.replace(anc, bloc + '\n' + anc, 1)
io.open(DST, 'w', encoding='utf-8').write(s)

print(u'%d entrees versees dans %s' % (len(entrees), DST))
print(u'de « %s » a « %s »' % (entrees[0][0], entrees[-1][0]))
