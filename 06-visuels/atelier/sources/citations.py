# -*- coding: utf-8 -*-
"""Les citations de l'appareil existent-elles encore dans le texte ?

Une fiche survit facilement a son chapitre. On corrige une phrase le
matin, la fiche qui la citait garde l'ancienne version, et six mois
plus tard on travaille sur une phrase qui n'existe plus. C'est arrive
trois fois le 22 aout 2026, et rien ne l'avait signale.

Ce script compare ce que les fiches citent a ce que les textes disent.
Il ne verifie que les scenes dont le chapitre est ecrit -- ailleurs,
une citation est une proposition, pas un rappel.

  python citations.py            les repliques retenues des chapitres ecrits
  python citations.py --tout     plus tout ce qui est entre guillemets
  python citations.py --court    seulement les introuvables

Il SIGNALE et n'ecrit rien, et il se trompe volontiers : une replique
peut etre gardee pour un chapitre qui n'est pas encore ecrit, ou avoir
ete donnee comme modele sans devoir etre reprise mot pour mot. C'est
l'autrice qui tranche.
"""
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ICI = os.path.dirname(os.path.abspath(__file__))
B = chr(96)


def lire(nom):
    return io.open(os.path.join(ICI, nom), encoding='utf-8').read()


def plat(t):
    """Le texte compare : sans balise, sans gras, sans fioriture."""
    t = re.sub(r'<[^>]+>', u' ', t)
    t = t.replace(u'**', u'').replace(u'*', u'')
    t = t.replace(u'’', u"'").replace(u'‘', u"'")
    t = t.replace(u'…', u'...').replace(u'—', u'-').replace(u'–', u'-')
    t = t.replace(u' ', u' ')
    t = re.sub(u'[\u00ab\u00bb"]', u' ', t)
    t = re.sub(u'[.,;:!?()\\[\\]\u2013\u2014-]', u' ', t)
    return u' '.join(t.lower().split())


# ---------- les textes ecrits, par scene ----------
js = lire('pB-textes.js')
bornes = [(m.group(1), m.start()) for m in re.finditer(r'\n  id: ' + B + r'([a-z0-9-]+)' + B + r',', js)]
par_scene = {}
for n, (ident, deb) in enumerate(bornes):
    fin = bornes[n + 1][1] if n + 1 < len(bornes) else len(js)
    bloc = js[deb:fin]
    sc = re.search(r'scene: ' + B + r'([a-z0-9-]+)' + B, bloc)
    paras = re.findall(r'\[' + B + r'(?:p|tiret|pause)' + B + r',' + B + r'([^' + B + r']*)' + B, bloc)
    if sc:
        par_scene[sc.group(1)] = (ident, plat(u' '.join(paras)))

if not par_scene:
    raise SystemExit(u'aucun texte trouve')


# ---------- ce que l'appareil cite ----------
def citations(bloc):
    """Les repliques du champ phrases, et les passages entre guillemets."""
    out = []
    for m in re.finditer(r'\{ t: ' + B + r'([^' + B + r']*)' + B, bloc):
        out.append((u'phrase', m.group(1)))
    if u'--tout' in sys.argv:
        # les guillemets servent aussi a citer l'autrice : beaucoup de bruit
        for m in re.finditer(u'\u00ab\\s*([^\u00bb]{18,})\\s*\u00bb', bloc):
            out.append((u'citation', m.group(1)))
    return out


scenes = lire('p5-scenes.js')
blocs = []
for m in re.finditer(r'\n  id: ' + B + r'([a-z0-9-]+)' + B + r',', scenes):
    blocs.append((m.group(1), m.start()))

court = '--court' in sys.argv
introuvables, approchees, total = [], [], 0

for n, (ident, deb) in enumerate(blocs):
    if ident not in par_scene:
        continue                       # le chapitre n'est pas ecrit
    fin = blocs[n + 1][1] if n + 1 < len(blocs) else len(scenes)
    chapitre, texte = par_scene[ident]
    for genre, brut in citations(scenes[deb:fin]):
        c = plat(brut)
        if len(c.split()) < 4:
            continue
        total += 1
        if c in texte:
            continue
        debut = u' '.join(c.split()[:5])
        if debut in texte:
            approchees.append((chapitre, genre, brut))
        else:
            introuvables.append((chapitre, genre, brut))


def montre(titre, liste):
    if not liste:
        return
    print(u'\n%s (%d)' % (titre, len(liste)))
    for chapitre, genre, brut in liste:
        print(u'  %-12s %s' % (chapitre, u' '.join(brut.split())[:96]))


montre(u'INTROUVABLES — la fiche cite ce que le texte ne dit plus', introuvables)
if not court:
    montre(u'reformulees — le debut se retrouve, la suite a bouge', approchees)

print(u'\n%d citations verifiees sur %d chapitres ecrits : %d introuvable(s), %d reformulee(s).'
      % (total, len(par_scene), len(introuvables), len(approchees)))
print(u'Rien n\'a ete modifie.')
