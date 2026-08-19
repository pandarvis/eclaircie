# -*- coding: utf-8 -*-
"""Trace des chemins qui ne peuvent pas traverser un batiment.

Router a la main dans un jardin aussi dense, c'est deplacer une faute pour
en creer une autre. Ici l'espace libre est une grille, et le chemin est
cherche dedans : il ne peut pas passer ou il n'a pas le droit.

Chaque version se distingue par ses points de passage imposes, pas par un
trace bricole.
"""
import heapq
import math

PAS = 3                      # maille de la grille
LARGE = 6.5                  # demi-largeur d'un chemin, marge comprise
X0, X1, Y0, Y1 = 72, 956, 44, 662

MUR = [(150, 86), (520, 52), (900, 96), (946, 300), (906, 560), (560, 650),
       (190, 616), (80, 330)]

PORTES = {
    'nord-ouest': (115, 208),
    'principale': (700, 74),
    'service':    (940, 330),
    'sud-ouest':  (330, 628),
}

ANNEAU = [(468, 236), (556, 250), (624, 286), (656, 340), (652, 410), (616, 470),
          (548, 514), (468, 530), (386, 516), (320, 478), (286, 418), (292, 348),
          (334, 286), (398, 250)]

BATIMENTS = [
    ('Centre medical', 766, 254, 152, 104, -4),
    ('Fin de vie', 778, 406, 124, 54, 6),
    ('Refectoire', 518, 102, 150, 64, 3),
    ('Gymnase', 227, 507, 124, 64, -6),
    ('Salle de jeu', 694, 182, 112, 60, 5),
    ("L'ecurie", 632, 266, 52, 26, 6),
    ('Le poulailler', 416, 450, 36, 18, 16),
    ('Le clapier', 346, 432, 32, 16, 3),
    ("L'abri", 454, 296, 54, 22, -4),
    ('La cabane', 491, 375, 44, 22, -5),
    ('Le local technique', 322, 402, 52, 22, -9),
    ('Dortoirs 1', 196, 120, 100, 52, -5),
    ('Dortoirs 2', 323, 185, 100, 52, 4),
    ('Dortoirs 3', 544, 167, 100, 52, -3),
    ('Dortoirs 4', 760, 120, 100, 52, 7),
    ('Dortoirs 5', 146, 330, 96, 52, 3),
    ('Dortoirs 6', 160, 432, 96, 52, -4),
    ('Dortoirs 7', 406, 562, 100, 52, 5),
    ('Dortoirs 8', 548, 556, 100, 52, -6),
    ('Dortoirs 9', 670, 508, 106, 56, 8),
    ('Cabanon nord', 298, 140, 46, 28, 0),
    ('Cabanon est', 704, 270, 46, 28, 0),
    ('Loge', 232, 400, 44, 28, 0),
    ('Garage', 712, 300, 44, 28, 0),
    ('Aire de jeu ouest', 196, 214, 92, 62, 0),
    ('Aire de jeu est', 810, 180, 92, 58, 0),
    ('Bacs a sable', 196, 284, 86, 44, 0),
    ('Le terrain', 330, 92, 152, 74, 0),
]

MARE = (385, 350, 56, 40)
PRES = [(546, 328, 56, 42), (538, 444, 50, 34)]
ENCL = [(466, 486, 36, 22), (356, 462, 34, 20)]


def tourner(px, py, cx, cy, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return (cx + (px - cx) * c - (py - cy) * s,
            cy + (px - cx) * s + (py - cy) * c)


def dans_rect(p, b, marge=0.0):
    _, x, y, w, h, ang = b
    cx, cy = x + w / 2.0, y + h / 2.0
    px, py = tourner(p[0], p[1], cx, cy, -ang) if ang else p
    return (x - marge < px < x + w + marge) and (y - marge < py < y + h + marge)


def dans_polygone(pts, p):
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


def dans_ellipse(p, e, marge=0.0):
    cx, cy, rx, ry = e
    return ((p[0]-cx)/(rx*1.2+marge))**2 + ((p[1]-cy)/(ry*1.2+marge))**2 < 1


def retreci(pts, d):
    cx = sum(p[0] for p in pts) / float(len(pts))
    cy = sum(p[1] for p in pts) / float(len(pts))
    out = []
    for x, y in pts:
        dx, dy = x - cx, y - cy
        l = math.hypot(dx, dy) or 1
        out.append((x - dx / l * d, y - dy / l * d))
    return out


MUR_DEDANS = retreci(MUR, 9)

NX = (X1 - X0) // PAS + 1
NY = (Y1 - Y0) // PAS + 1


def libre(ix, iy):
    p = (X0 + ix * PAS, Y0 + iy * PAS)
    if not dans_polygone(MUR_DEDANS, p):
        return False
    for b in BATIMENTS:
        if dans_rect(p, b, LARGE):
            return False
    if dans_ellipse(p, MARE, LARGE):
        return False
    for e in PRES + ENCL:
        if dans_ellipse(p, e, LARGE):
            return False
    return True


GRILLE = [[libre(ix, iy) for iy in range(NY)] for ix in range(NX)]
# les portes sont dans le mur : on les force praticables
for g in PORTES.values():
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            ix, iy = (g[0]-X0)//PAS+dx, (g[1]-Y0)//PAS+dy
            if 0 <= ix < NX and 0 <= iy < NY:
                GRILLE[ix][iy] = True

VOISINS = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]


def cellule(p):
    return (int(round((p[0]-X0)/float(PAS))), int(round((p[1]-Y0)/float(PAS))))


def chercher(a, b, cout_sup=None):
    """A* de a vers b. cout_sup(ix,iy) ajoute un cout, pour attirer un trace."""
    ca, cb = cellule(a), cellule(b)
    ouvert = [(0, ca)]
    vientDe, g = {}, {ca: 0}
    while ouvert:
        _, n = heapq.heappop(ouvert)
        if n == cb:
            break
        for dx, dy in VOISINS:
            m = (n[0]+dx, n[1]+dy)
            if not (0 <= m[0] < NX and 0 <= m[1] < NY) or not GRILLE[m[0]][m[1]]:
                continue
            c = g[n] + (1.4142 if dx and dy else 1.0)
            if cout_sup:
                c += cout_sup(m[0], m[1])
            if m not in g or c < g[m]:
                g[m] = c
                vientDe[m] = n
                h = math.hypot(m[0]-cb[0], m[1]-cb[1])
                heapq.heappush(ouvert, (c + h, m))
    if cb not in vientDe and cb != ca:
        return None
    out, n = [], cb
    while n != ca:
        out.append(n)
        n = vientDe[n]
    out.append(ca)
    out.reverse()
    return [(X0+i*PAS, Y0+j*PAS) for i, j in out]


def simplifier(pts, tol=3.2):
    """Douglas-Peucker : on garde la forme, on jette les points."""
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    dx, dy = b[0]-a[0], b[1]-a[1]
    n = math.hypot(dx, dy) or 1
    pire, idx = 0, 0
    for i in range(1, len(pts)-1):
        d = abs(dy*(pts[i][0]-a[0]) - dx*(pts[i][1]-a[1])) / n
        if d > pire:
            pire, idx = d, i
    if pire > tol:
        return simplifier(pts[:idx+1], tol)[:-1] + simplifier(pts[idx:], tol)
    return [a, b]


def route(depart, arrivee, vias=(), attire=None):
    """Un chemin d'une porte a une autre, par les points de passage donnes."""
    etapes = [PORTES[depart]] + list(vias) + [PORTES[arrivee]]
    plein = []
    for i in range(len(etapes)-1):
        bout = chercher(etapes[i], etapes[i+1], attire)
        if bout is None:
            return None
        plein += bout if not plein else bout[1:]
    p = simplifier(plein)
    p[0], p[-1] = PORTES[depart], PORTES[arrivee]
    return p


def pres_de_anneau(ix, iy):
    """Cout reduit quand on longe la grande allee : les chemins s'y collent."""
    p = (X0+ix*PAS, Y0+iy*PAS)
    d = min(math.hypot(p[0]-a[0], p[1]-a[1]) for a in ANNEAU)
    return 0 if d < 26 else 0.55


if __name__ == '__main__':
    n = sum(1 for i in range(NX) for j in range(NY) if GRILLE[i][j])
    print(u'grille %dx%d, %d cellules libres (%.0f %%)'
          % (NX, NY, n, 100.0*n/(NX*NY)))
    for a, b in (('nord-ouest', 'service'), ('principale', 'sud-ouest'),
                 ('nord-ouest', 'sud-ouest'), ('principale', 'service')):
        r = route(a, b, attire=pres_de_anneau)
        print(u'%-12s -> %-11s %s' % (a, b, (u'%d points' % len(r)) if r else u'IMPOSSIBLE'))
