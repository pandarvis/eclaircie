# -*- coding: utf-8 -*-
"""La relecture de surface : les fautes betes, et rien d'autre.

  python relire.py                 tous les textes
  python relire.py prologue        un seul

Ce script SIGNALE. Il ne corrige pas, il n'ecrit dans aucun fichier.
C'est voulu : le texte est a l'autrice, et une correction qui passe
sans qu'elle l'ait vue est une correction dont personne ne repond.

Il ne cherche que le mecanique -- ce qui est faux quel que soit le sens
de la phrase : une espace en double, un mot ecrit deux fois de suite,
une ponctuation sans son espace. Le style, le
rythme, les repetitions voulues : ce n'est pas son affaire.
"""
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ICI = os.path.dirname(os.path.abspath(__file__))
JS = os.path.join(ICI, 'pB-textes.js')
B = chr(96)


def textes():
    js = io.open(JS, encoding='utf-8').read()
    bornes = [(m.group(1), m.start()) for m in re.finditer(r'\n  id: ' + B + r'([a-z0-9-]+)' + B + r',', js)]
    out = []
    for n, (ident, deb) in enumerate(bornes):
        fin = bornes[n + 1][1] if n + 1 < len(bornes) else len(js)
        titre = re.search(r'titre: ' + B + r'([^' + B + r']*)' + B, js[deb:fin])
        paras = re.findall(r'\[' + B + r'(?:p|tiret|pause)' + B + r',' + B + r'([^' + B + r']*)' + B,
                           js[deb:fin])
        out.append((ident, titre.group(1) if titre else ident, paras))
    return out


def nu(s):
    """Le texte sans les balises : on ne releve pas une faute dans du <em>."""
    return re.sub(r'<[^>]+>', u'', s)


# Chaque regle : (motif, ce qu'on en dit). Rien d'interpretatif ici.
MOTS = u"[A-Za-zà-ÿŒœ]"
REGLES = [
    (re.compile(u'  +'),                       u'deux espaces de suite'),
    (re.compile(u' [,.]'),                     u'une espace avant la virgule ou le point'),
    (re.compile(u'[a-zà-ÿ][,.][A-Za-zà-ÿ]'), u'une ponctuation sans son espace'),
    (re.compile(u'(?i)\\b(' + MOTS + u'+) \\1\\b'), u'le meme mot ecrit deux fois de suite'),
    (re.compile(u'\\.\\.\\.'),                 u'trois points au lieu des points de suspension'),
    (re.compile(u'\\s$|^\\s'),                 u'une espace au bord du paragraphe'),
    (re.compile(u'[a-zà-ÿ]\\.\\s+[a-zà-ÿ]'), u'une minuscule apres un point'),
    (re.compile(u'ça\\s+ça|\\bde de\\b|\\bla la\\b|\\ble le\\b'), u'un mot double'),
    (re.compile(u'-\\s'),                      u'un tiret suivi d\'une espace en debut de mot', True),
]


def bornes_du_relev(p):
    """Les ennuis d'un paragraphe : liste de (ce qu'on en dit, extrait)."""
    t = nu(p)
    vus = []
    for regle in REGLES:
        motif, dit = regle[0], regle[1]
        if len(regle) > 2:                        # les regles bavardes : hors service
            continue
        for m in motif.finditer(t):
            a, b = max(0, m.start() - 34), min(len(t), m.end() + 34)
            vus.append((dit, u'…' + t[a:b].strip() + u'…'))
    return vus


cibles = [a for a in sys.argv[1:] if not a.startswith('-')]

total = 0
for ident, titre, paras in textes():
    if cibles and ident not in cibles:
        continue
    releve = []
    for n, p in enumerate(paras, 1):
        for dit, extrait in bornes_du_relev(p):
            releve.append((n, dit, extrait))
    print(u'\n%s — %d paragraphes' % (titre, len(paras)))
    if not releve:
        print(u'  rien a signaler.')
        continue
    total += len(releve)
    for n, dit, extrait in releve:
        print(u'  §%-4d %s' % (n, dit))
        print(u'        %s' % extrait)

print(u'\n%d chose(s) a signaler. Rien n\'a ete modifie.' % total)
