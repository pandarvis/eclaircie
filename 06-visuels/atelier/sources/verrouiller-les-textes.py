# -*- coding: utf-8 -*-
"""Le verrou des textes valides.

Un chapitre valide ne bouge plus, sauf demande explicite de l'autrice.
Une regle ecrite ne suffit pas : elle tient tant que quelqu'un y pense,
et on a deja paye trois fois pour savoir ce que ca vaut.

Ce script enregistre l'empreinte de chaque texte verrouille. fabriquer.sh
la recalcule et refuse de fabriquer si un texte a bouge.

  python verrouiller-les-textes.py --verifier      dit si un texte a bouge
  python verrouiller-les-textes.py --poser         enregistre l'etat actuel
  python verrouiller-les-textes.py --ouvrir <id>   retire un texte du verrou

Pour corriger un chapitre verrouille : --ouvrir, corriger, --poser.
Le detour est volontaire. C'est ce qui empeche une correction de passer
sans que personne l'ait demandee.
"""
import hashlib
import io
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
JS = os.path.join(ICI, 'pB-textes.js')
VERROU = os.path.join(ICI, 'textes-verrouilles.txt')


def empreintes():
    """Le texte seul : ni les fiches, ni les titres, ni l'appareil."""
    js = io.open(JS, encoding='utf-8').read()
    bornes = [(m.group(1), m.start()) for m in re.finditer(r'\n  id: `([a-z0-9-]+)`,', js)]
    out = []
    for n, (ident, deb) in enumerate(bornes):
        fin = bornes[n + 1][1] if n + 1 < len(bornes) else len(js)
        paras = re.findall(r'\[`(?:p|tiret|pause)`,`([^`]*)`', js[deb:fin])
        brut = u'\n'.join(paras).encode('utf-8')
        out.append((ident, hashlib.sha256(brut).hexdigest(), len(paras)))
    return out


def lire_verrou():
    if not os.path.exists(VERROU):
        return {}
    d = {}
    for l in io.open(VERROU, encoding='utf-8'):
        l = l.strip()
        if not l or l.startswith('#'):
            continue
        ident, emp = l.split()[:2]
        d[ident] = emp
    return d


def poser(idents=None):
    verrou = lire_verrou()
    for ident, emp, n in empreintes():
        if idents is None or ident in idents:
            verrou[ident] = emp
    lignes = [u'# Les textes verrouilles, et leur empreinte.',
              u"# Un chapitre d'ici ne bouge que sur demande explicite de l'autrice.",
              u'# Pour en corriger un : --ouvrir <id>, corriger, --poser.', u'']
    for ident, emp, n in empreintes():
        if ident in verrou:
            lignes.append(u'%-12s %s  # %d paragraphes' % (ident, verrou[ident], n))
    open(VERROU, 'wb').write((u'\n'.join(lignes) + u'\n').encode('utf-8'))
    print(u'verrou pose sur : ' + u', '.join(sorted(verrou)))


def ouvrir(ident):
    verrou = lire_verrou()
    if ident not in verrou:
        raise SystemExit(u'%s n\'est pas verrouille.' % ident)
    del verrou[ident]
    lignes = [u'# Les textes verrouilles, et leur empreinte.',
              u"# Un chapitre d'ici ne bouge que sur demande explicite de l'autrice.",
              u'# Pour en corriger un : --ouvrir <id>, corriger, --poser.', u'']
    for i, emp, n in empreintes():
        if i in verrou:
            lignes.append(u'%-12s %s  # %d paragraphes' % (i, verrou[i], n))
    open(VERROU, 'wb').write((u'\n'.join(lignes) + u'\n').encode('utf-8'))
    print(u'%s est ouvert. Il faudra le reverrouiller avec --poser.' % ident)


def verifier():
    verrou = lire_verrou()
    if not verrou:
        print(u'aucun texte verrouille')
        return 0
    actuel = {i: e for i, e, n in empreintes()}
    bouges = [i for i, e in verrou.items() if actuel.get(i) != e]
    if bouges:
        print(u'PROBLEME : texte(s) verrouille(s) modifie(s) : ' + u', '.join(sorted(bouges)))
        print(u'           un chapitre valide ne bouge que sur demande explicite.')
        print(u'           si elle l\'a demande : python verrouiller-les-textes.py --ouvrir '
              + sorted(bouges)[0])
        return 1
    print(u'textes verrouilles : %d, aucun n\'a bouge' % len(verrou))
    return 0


args = sys.argv[1:]
if not args or args[0] == '--verifier':
    raise SystemExit(verifier())
if args[0] == '--poser':
    poser(args[1:] or None)
elif args[0] == '--ouvrir':
    if len(args) < 2:
        raise SystemExit(u'usage : --ouvrir <id>')
    ouvrir(args[1])
else:
    raise SystemExit(u'usage : --verifier | --poser [id...] | --ouvrir <id>')
