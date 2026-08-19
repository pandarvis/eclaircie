# -*- coding: utf-8 -*-
"""Passe un brouillon au meme controle que les chapitres de l'atelier.

usage : python controler-un-texte.py <fichier.md> [<fichier.md> ...]

Deux choses : les mots que le monde ne connait pas, et les mesures du style
etablies dans 01-dossier/le-style.md. Ne juge rien d'autre.
"""
import io
import re
import sys

BANNIS = re.compile(
    r"\b(enfants?|b[ée]b[ée]s?|nourrissons?|vieux|vieilles?|vieillards?|seniors?|"
    r"p[èe]res?|m[èe]res?|fils|famille|jumeaux?|jumelles?|peaux?)\b", re.I | re.U)

MOTS = re.compile(r"[\wÀ-ſ']+", re.U)
FAUX_ADVERBES = {'mouvement', 'moment', 'bâtiment', 'comment', 'appartement',
                 'raclement', 'bruissement', 'ronflement', 'hochement',
                 'haussement', 'ralentissement', 'instrument', 'équipement',
                 'emplacement', 'environnement', 'bercement', 'tintement',
                 'craquement', 'grincement', 'battement', 'frottement'}

SEUIL_LONGUE = 35


def texte_seul(brut):
    """Retire les titres, les consignes en italique et les filets."""
    gardees = []
    for ligne in brut.split('\n'):
        l = ligne.strip()
        if l.startswith('#') or l.startswith('---') or l.startswith('>'):
            continue
        if l.startswith('*') and l.endswith('*') and len(l) > 2:
            continue
        gardees.append(ligne)
    return '\n'.join(gardees)


def controle(chemin):
    brut = io.open(chemin, encoding='utf-8').read()
    print('\n' + '=' * 74)
    print(chemin)
    print('=' * 74)

    # Les mots bannis se cherchent dans TOUT le fichier, commentaires compris :
    # une consigne qui emploie le mot finira par se retrouver dans le texte.
    trouves = {}
    for m in BANNIS.finditer(brut):
        ligne = brut[:m.start()].count('\n') + 1
        trouves.setdefault(m.group(0).lower(), []).append(ligne)
    if trouves:
        print('\nMOTS BANNIS')
        for mot in sorted(trouves):
            print('   %-14s ligne %s' % (mot, ', '.join(str(x) for x in trouves[mot])))
    else:
        print('\nMOTS BANNIS   aucun')

    t = texte_seul(brut)
    ph = [x for x in re.split(r'(?<=[.!?…])\s+', t) if len(MOTS.findall(x)) > 1]
    if not ph:
        print('\nrien a mesurer')
        return
    lg = sorted(len(MOTS.findall(x)) for x in ph)
    mots = MOTS.findall(t)
    adv = [w for w in mots if w.lower().endswith('ment') and len(w) > 6
           and re.sub(r"^[ldjcnstm]'", '', w.lower()) not in FAUX_ADVERBES]
    ronds = [w for w in re.findall(r'\b(dix|vingt|trente|quarante|cinquante|soixante|'
                                   r'cent|mille)\b(?!-)', t, re.I)]

    print('\nMESURES')
    print('   %d mots, %d phrases' % (len(mots), len(ph)))
    print('   mediane %d mots, moyenne %.1f  (le livre : mediane 11, moyenne 12,9)'
          % (lg[len(lg) // 2], sum(lg) / float(len(lg))))
    print('   phrases de 5 mots ou moins : %d (%.0f %%)  (le livre : 21 %%)'
          % (sum(1 for x in lg if x <= 5), 100.0 * sum(1 for x in lg if x <= 5) / len(lg)))
    print('   parentheses %d · points-virgules %d · adverbes en -ment %d'
          % (t.count('('), t.count(';'), len(adv)))
    if adv:
        print('      ' + ', '.join(sorted(set(adv))))
    if ronds:
        print('   nombres ronds a verifier : ' + ', '.join(sorted(set(w.lower() for w in ronds))))

    longues = [x for x in ph if len(MOTS.findall(x)) > SEUIL_LONGUE]
    print('\nPHRASES DE PLUS DE %d MOTS : %d' % (SEUIL_LONGUE, len(longues)))
    for x in longues:
        print('   [%d] %s' % (len(MOTS.findall(x)), ' '.join(x.split())[:170]))

    # Les negations : c'est ce qui avait alourdi le chapitre premier.
    neg = len(re.findall(r"\bn[e']", t, re.I | re.U))
    print('\nNEGATIONS   %.1f pour mille mots  (prologue 19,2 · chapitre premier 36,1)'
          % (1000.0 * neg / max(1, len(mots))))


if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(1)
for chemin in sys.argv[1:]:
    controle(chemin)
