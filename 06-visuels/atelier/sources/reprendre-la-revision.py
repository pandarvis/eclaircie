# -*- coding: utf-8 -*-
"""Reprend les corrections faites par l'autrice dans l'atelier.

Elle revise le texte dans l'onglet Chapitres, clique << enregistrer pour
Claude >>, et le navigateur depose un fichier de revision. Ce script le
rejoue sur pB-textes.js.

  python reprendre-la-revision.py                 cherche le dernier fichier
  python reprendre-la-revision.py chemin.json     un fichier precis
  python reprendre-la-revision.py --voir          montre sans rien ecrire

Le fichier ne contient pas le texte entier : il contient l'ecart, sous
forme de couples avant/apres. Chaque avant doit se retrouver une fois et
une seule dans pB-textes.js, sinon on s'arrete -- une correction qui ne
trouve pas son ancre est une correction qu'on croirait passee.
"""
import glob
import io
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
JS = os.path.join(ICI, 'pB-textes.js')
TELECH = os.path.join(os.path.expanduser('~'), 'Downloads')


def trouver():
    """Le fichier de revision le plus recent, ou qu'il soit."""
    coins = [os.path.join(TELECH, 'eclaircie-revision-*.json'),
             os.path.join(ICI, 'eclaircie-revision-*.json'),
             os.path.join(ICI, '..', 'eclaircie-revision-*.json')]
    trouves = []
    for c in coins:
        trouves += glob.glob(c)
    if not trouves:
        raise SystemExit(
            u"Aucun fichier de revision.\n"
            u"Dans l'atelier : onglet Chapitres, << reviser le texte >>,\n"
            u"puis << enregistrer pour Claude >>. Cherche dans " + TELECH)
    return max(trouves, key=os.path.getmtime)


def court(t, n=72):
    t = u' '.join(t.split())
    return t if len(t) <= n else t[:n - 1] + u'…'


voir = '--voir' in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith('--')]
src = args[0] if args else trouver()

d = json.load(io.open(src, encoding='utf-8'))
chgs = d.get('changements') or []
print(u'revision de %s (%s)' % (d.get('titre', '?'), os.path.basename(src)))
if not chgs:
    raise SystemExit(u'  rien dedans.')

js = io.open(JS, encoding='utf-8').read()
avant_len = len(js)
faits = {'modifie': 0, 'ote': 0, 'neuf': 0}
B = u'`'

for c in chgs:
    etat = c['etat']

    if etat == 'modifie':
        a, b = c['avant'], c['apres']
        cle = B + a + B
        if js.count(cle) != 1:
            raise SystemExit(u'  ANCRE INTROUVABLE (%d fois) : %s' % (js.count(cle), court(a)))
        print(u'  ~ %s' % court(a))
        print(u'    %s' % court(b))
        js = js.replace(cle, B + b + B, 1)

    elif etat == 'ote':
        a = c['texte']
        ligne = u'[%s%s%s,%s%s%s],\n' % (B, c.get('k', 'p'), B, B, a, B)
        if js.count(ligne) != 1:
            # la ligne porte peut-etre un troisieme element
            deb = js.find(B + a + B)
            if deb < 0:
                raise SystemExit(u'  ANCRE INTROUVABLE pour la suppression : %s' % court(a))
            d0 = js.rindex(u'\n[', 0, deb) + 1
            d1 = js.index(u'\n', deb) + 1
            ligne = js[d0:d1]
        print(u'  - %s' % court(a))
        js = js.replace(ligne, u'', 1)

    elif etat == 'neuf':
        ancre = c['ancre']
        deb = js.find(B + ancre + B)
        if deb < 0:
            raise SystemExit(u'  ANCRE INTROUVABLE pour l\'ajout : %s' % court(ancre))
        fin = js.index(u'\n', deb) + 1
        neuf = u'[%s%s%s,%s%s%s],\n' % (B, c.get('k', 'p'), B, B, c['apres'], B)
        print(u'  + %s' % court(c['apres']))
        js = js[:fin] + neuf + js[fin:]

    else:
        raise SystemExit(u'  etat inconnu : ' + etat)

    faits[etat] += 1

print(u'\n%d corrige(s), %d ote(s), %d ajoute(s) — %+d caracteres'
      % (faits['modifie'], faits['ote'], faits['neuf'], len(js) - avant_len))

if voir:
    print(u'(--voir : rien n\'a ete ecrit)')
else:
    open(JS, 'wb').write(js.encode('utf-8'))
    print(u'pB-textes.js est a jour. Relancer  sh fabriquer.sh')
