# -*- coding: utf-8 -*-
"""Fabrique les cinq reseaux de chemins et les verse dans le plan.

Chaque version se distingue par ce qu'elle impose au trace, pas par un
bricolage : des points de passage, ou une penalite qui repousse le chemin
hors de l'etendue. Le routeur fait le reste, et il ne peut pas traverser
un batiment.
"""
import io
import math
import sys

sys.path.insert(0, '.')
import routeur_du_jardin as R

ETENDUE = R.ANNEAU
CENTRE_MEDICAL = (766, 254, 152, 104)


def dedans_etendue(ix, iy):
    p = (R.X0 + ix * R.PAS, R.Y0 + iy * R.PAS)
    return R.dans_polygone(ETENDUE, p)


def dehors(ix, iy):
    """Repousse le trace hors de l'etendue, sans l'interdire."""
    return 2.6 if dedans_etendue(ix, iy) else R.pres_de_anneau(ix, iy)


def dedans(ix, iy):
    """Attire le trace vers l'interieur."""
    return 0 if dedans_etendue(ix, iy) else R.pres_de_anneau(ix, iy) + .25


CARREFOUR = (462, 400)

VERSIONS = [
    (u'La croix', u'deux traversantes qui se croisent',
     [(u'nord-ouest', u'service',    [CARREFOUR], dedans),
      (u'principale', u'sud-ouest',  [CARREFOUR], dedans)],
     u"<b>Les deux routes se croisent au milieu de l'étendue</b>, à un jet de pierre de la mare. "
     u"<em>C'est le plan le plus vivant : tout le monde passe par là, et tout le monde voit les bêtes "
     u"en passant.</em> C'est aussi celui où l'étendue est le moins un lieu à part."),

    (u'Le contour', u'personne ne traverse',
     [(u'nord-ouest', u'sud-ouest',  [], dehors),
      (u'principale', u'service',    [], dehors)],
     u"<b>Aucune route n'entre dans l'étendue.</b> On n'y va que si on décide d'y aller, et la grande "
     u"allée en fait le tour. <em>C'est le plan qui protège le mieux le milieu — et celui qui rend le "
     u"trajet d'Andrew le plus long.</em>"),

    (u'La traverse unique', u"une seule, d'ouest en est",
     [(u'nord-ouest', u'service',    [CARREFOUR], dedans),
      (u'principale', u'sud-ouest',  [], dehors)],
     u"<b>Une seule route traverse, et c'est celle qui va au centre médical.</b> <em>Andrew et Isaac "
     u"passent devant la mare et les prés parce qu'ils n'ont pas le choix — et l'autre route, elle, "
     u"contourne.</em> Le milieu reste calme la moitié du temps."),

    (u'Le Y', u'deux routes, un tronçon commun',
     [(u'nord-ouest', u'service',    [(404, 424), (462, 408)], dedans),
      (u'principale', u'sud-ouest',  [(462, 408), (404, 424)], dedans)],
     u"<b>Les deux routes se rejoignent et partagent le milieu de l'étendue</b> avant de repartir "
     u"chacune de son côté. <em>Il y a un endroit, entre la mare et le pré, où tout le jardin se "
     u"croise.</em> C'est le plan qui crée une place sans qu'on l'ait dessinée."),

    (u'Les deux rives', u'la mare entre les deux',
     [(u'nord-ouest', u'service',    [(430, 296)], dedans),
      (u'principale', u'sud-ouest',  [(466, 438)], dedans)],
     u"<b>Deux traversantes parallèles, la mare prise entre elles.</b> <em>L'une passe au nord de "
     u"l'eau, l'autre au sud ; elles ne se croisent jamais.</em> C'est le plan où l'on peut faire "
     u"passer deux personnes au même moment sans qu'elles se voient."),
]


PORTE_DU_CENTRE = (752, 368)     # devant le bord ouest du centre medical


def cellules_de(traces, rayon=9):
    """Les cellules couvertes par des traces : marcher dessus ne coute rien."""
    dedans = set()
    for pts in traces:
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            d = math.hypot(b[0] - a[0], b[1] - a[1])
            n = max(2, int(d / 2.0))
            for k in range(n + 1):
                t = k / float(n)
                x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                cx, cy = R.cellule((x, y))
                r = int(rayon / R.PAS) + 1
                for dx in range(-r, r + 1):
                    for dy in range(-r, r + 1):
                        dedans.add((cx + dx, cy + dy))
    return dedans


def trajet_andrew(routes):
    """Andrew prend les chemins de sa version. Hors reseau, chaque pas coute
    cher : il ne coupe pas a travers la pelouse pour gagner trente metres."""
    couvert = cellules_de([p for _, _, p in routes] + [R.ANNEAU + [R.ANNEAU[0]]])
    def cout(ix, iy):
        return 0.0 if (ix, iy) in couvert else 3.2
    p = R.chercher(R.PORTES['nord-ouest'], PORTE_DU_CENTRE, cout)
    assert p, 'trajet impossible'
    return degrossir(p)


def propre(pts):
    """Le trace simplifie ne doit rien mordre : simplifier, c'est couper les
    virages, et un virage coupe peut entrer dans un mur."""
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(2, int(d / 1.5))
        for k in range(n + 1):
            t = k / float(n)
            q = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            for bat in R.BATIMENTS:
                if R.dans_rect(q, bat, R.LARGE - 1):
                    return False
            if R.dans_ellipse(q, R.MARE, R.LARGE - 1):
                return False
    return True


def degrossir(p):
    """On simplifie tant que le trace reste propre, pas plus."""
    garde = p
    for tol in (3.2, 2.4, 1.8, 1.2, 0.8, 0.0):
        q = R.simplifier(p, tol) if tol else p
        if propre(q):
            garde = q
            break
    garde = list(garde)
    garde[0] = R.PORTES['nord-ouest']
    garde[-1] = PORTE_DU_CENTRE
    return garde


def js(pts):
    return u'[' + u','.join(u'[%d,%d]' % (round(p[0]), round(p[1])) for p in pts) + u']'


blocs = []
for nom, sous, defs, note in VERSIONS:
    routes, trajet = [], None
    for depart, arrivee, vias, cout in defs:
        p = R.route(depart, arrivee, vias, cout)
        assert p, u'%s : %s -> %s impossible' % (nom, depart, arrivee)
        routes.append((depart, arrivee, p))
    trajet = trajet_andrew(routes)
    assert trajet, nom
    blocs.append(
        u"  {nom:`%s`, sous:`%s`, note:`%s`,\n   routes:[%s],\n   trajet:%s}"
        % (nom, sous, note,
           u','.join(u'{de:`%s`,a:`%s`,pts:%s}' % (d, a, js(p)) for d, a, p in routes),
           js(trajet)))
    print(u'%-20s %s' % (nom, u' | '.join(
        u'%s→%s %d pts' % (d[:4], a[:4], len(p)) for d, a, p in routes)))

io.open('reseaux.js', 'w', encoding='utf-8').write(
    u' reseaux:[\n' + u',\n'.join(blocs) + u'],\n')
print(u'\nreseaux.js ecrit')
