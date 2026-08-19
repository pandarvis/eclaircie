# -*- coding: utf-8 -*-
"""Verifie que rien ne deborde du mur, et que rien ne se chevauche.

Le plan est dessine par du JavaScript : les erreurs de geometrie ne se voient
qu'a l'oeil, et mal. Ce script relit les donnees dans le fichier et fait le
calcul. usage : python verifier-le-plan-du-jardin.py
"""
import io
import re
import json

SRC = u"R:/Documents/l'Eclaircie/06-visuels/plan-du-jardin.html"
MARGE = 16          # le mur est arrondi : on exige un peu de recul
s = io.open(SRC, encoding='utf-8').read()


def dedans(pts, p):
    x, y = p
    d = False
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / float(yj - yi) + xi:
            d = not d
        j = i
    return d


def retreci(pts, d):
    cx = sum(p[0] for p in pts) / float(len(pts))
    cy = sum(p[1] for p in pts) / float(len(pts))
    out = []
    for x, y in pts:
        dx, dy = x - cx, y - cy
        l = (dx * dx + dy * dy) ** .5 or 1
        out.append((x - dx / l * d, y - dy / l * d))
    return out


def liste(nom, bloc):
    """Recupere un tableau JS de nombres et de chaines, tolerant aux apostrophes."""
    m = re.search(r"\n\s%s:\[" % nom, bloc)
    if not m:
        return []
    i = m.end() - 1
    prof, j, dans = 0, i, None
    while j < len(bloc):
        c = bloc[j]
        if dans:
            if c == '\\':
                j += 2
                continue
            if c == dans:
                dans = None
        elif c in "'\"":
            dans = c
        elif c == '[':
            prof += 1
        elif c == ']':
            prof -= 1
            if prof == 0:
                break
        j += 1
    return bloc[i:j + 1]


def nombres(txt):
    """Rend la liste des tuples de tete de chaque sous-tableau."""
    out = []
    for sous in re.findall(r'\[([^\[\]]*)\]', txt):
        out.append(sous)
    return out


blocs = re.split(r'\n\{\n cle:', s)[1:]
pb = []
for b in blocs:
    cle = re.match(r"'(\w)'", b).group(1)
    mur = json.loads(re.search(r'\n mur:(\[\[.*?\]\])', b, re.S).group(1))
    dedans_mur = retreci([tuple(p) for p in mur], MARGE)

    rects = []
    # bat : ['classe',x,y,w,h,'nom',...]
    for sous in nombres(liste('bat', b)):
        m = re.match(r"\s*'[^']*',(\d+),(\d+),(\d+),(\d+),'((?:[^'\\]|\\.)*)'", sous)
        if m:
            x, y, w, h = (int(m.group(i)) for i in (1, 2, 3, 4))
            rects.append((m.group(5), x, y, w, h))
    # jeux : [x,y,w,h,'nom']
    for sous in nombres(liste('jeux', b)):
        m = re.match(r"\s*(\d+),(\d+),(\d+),(\d+),'((?:[^'\\]|\\.)*)'", sous)
        if m:
            x, y, w, h = (int(m.group(i)) for i in (1, 2, 3, 4))
            rects.append((m.group(5), x, y, w, h))

    print(u'\nPLAN %s  \u2014 %d rectangles' % (cle, len(rects)))

    for nom, x, y, w, h in rects:
        coins = [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]
        sortis = [c for c in coins if not dedans(dedans_mur, c)]
        if sortis:
            pb.append(u'  PLAN %s : %-26s deborde du mur (%d coin%s)'
                      % (cle, nom, len(sortis), 's' if len(sortis) > 1 else ''))

    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            a, b2 = rects[i], rects[j]
            noms = {a[0], b2[0]}
            if noms == {u'Centre médical', u'Fin de vie'}:
                continue          # voulu dans le plan B : la fin de vie est dedans
            if (a[1] < b2[1] + b2[3] and a[1] + a[3] > b2[1]
                    and a[2] < b2[2] + b2[4] and a[2] + a[4] > b2[2]):
                pb.append(u'  PLAN %s : %s chevauche %s' % (cle, a[0], b2[0]))

if pb:
    print(u'\n%d probleme(s) :' % len(pb))
    for x in pb:
        print(x)
else:
    print(u'\nRien ne deborde, rien ne se chevauche.')
