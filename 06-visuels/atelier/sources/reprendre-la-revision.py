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

Le verrou des textes ne s'oppose jamais a l'autrice. Il est la pour
empecher une correction que personne n'a demandee, pas pour l'empecher,
elle, de corriger son propre livre. Une revision venue de l'atelier
ouvre donc le verrou et le repose toute seule, et l'inscrit au journal.
"""
import glob
import io
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
JS = os.path.join(ICI, 'pB-textes.js')
TELECH = os.path.join(os.path.expanduser('~'), 'Downloads')


def trouver():
    """Le fichier de revision le plus recent, ou qu'il soit."""
    # Elle enregistre ou son navigateur veut bien : on regarde partout.
    racine = os.path.abspath(os.path.join(ICI, '..', '..', '..'))
    coins = [os.path.join(TELECH, 'eclaircie-revision-*.json'),
             os.path.join(ICI, 'eclaircie-revision-*.json'),
             os.path.join(ICI, '..', 'eclaircie-revision-*.json'),
             os.path.join(racine, 'eclaircie-revision-*.json'),
             os.path.join(racine, '*', 'eclaircie-revision-*.json'),
             os.path.join(os.path.expanduser('~'), 'Desktop', 'eclaircie-revision-*.json')]
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
    raise SystemExit(0)

open(JS, 'wb').write(js.encode('utf-8'))
print(u'pB-textes.js est a jour.')


# ---------- le verrou se repose tout seul ----------
ident = d.get('chapitre')
VERROU = os.path.join(ICI, 'textes-verrouilles.txt')
etait_verrouille = (os.path.exists(VERROU)
                    and ident
                    and any(l.split()[:1] == [ident]
                            for l in io.open(VERROU, encoding='utf-8')
                            if l.strip() and not l.startswith('#')))
if etait_verrouille:
    subprocess.check_call([sys.executable,
                           os.path.join(ICI, 'verrouiller-les-textes.py'),
                           '--poser', ident])
    print(u'  (le verrou s\'est repose : c\'est sa main, pas la mienne)')


# ---------- le journal, pour qu'aucune correction ne se perde ----------
JOURNAL = os.path.join(ICI, 'journal-des-revisions.md')
if not os.path.exists(JOURNAL):
    io.open(JOURNAL, 'w', encoding='utf-8').write(
        u'# Le journal des revisions\n\n'
        u"> **Ce que l'autrice a corrige elle-meme, depuis l'atelier.** "
        u'*Une ligne par passe, la plus recente en haut.*\n\n')
vieux = io.open(JOURNAL, encoding='utf-8').read()
tete, corps = vieux.split(u'\n\n', 2)[:2], vieux.split(u'\n\n', 2)[2:]
entree = u'- **%s** \u2014 %d corrige(s), %d ote(s), %d ajoute(s). `%s`\n' % (
    d.get('titre', ident), faits['modifie'], faits['ote'], faits['neuf'],
    os.path.basename(src))
neuf = u'\n\n'.join(tete) + u'\n\n' + entree + (corps[0] if corps else u'')
open(JOURNAL, 'wb').write(neuf.encode('utf-8'))

# ---------- le fichier consomme s'ecarte ----------
# Sinon il traine, et on ne sait plus si sa correction est passee ou non.
ARCHIVE = os.path.join(ICI, 'revisions-appliquees')
if not os.path.isdir(ARCHIVE):
    os.makedirs(ARCHIVE)
base = os.path.basename(src)
dest = os.path.join(ARCHIVE, base)
n = 2
while os.path.exists(dest):
    dest = os.path.join(ARCHIVE, base[:-5] + u'-%d.json' % n)
    n += 1
os.replace(src, dest)
print(u'  (fichier range dans revisions-appliquees/)')

print(u'Relancer  sh fabriquer.sh')
