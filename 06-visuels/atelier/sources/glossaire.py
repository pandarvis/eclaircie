# -*- coding: utf-8 -*-
"""Verse le glossaire et la bible dans l'atelier et dans le livre.

La source est 02-univers/le-glossaire.md, et elle est la seule. On y edite, on
relance ce script, on refabrique.

Avant, il y avait deux listes : un lexique ecrit a la main dans p7-monde.js
et un glossaire en markdown. Quarante-neuf mots sur cinquante et un etaient
definis deux fois, et les deux definitions avaient commence a diverger --
le corps medical du jardin portait deja deux noms.

Ce script produit :
  - p7-monde.js            les tableaux GLOSSAIRE et BIBLE de l'atelier
  - 05-manuscrit/glossaire.md   la page de fin de volume, generee

La page du livre ne recoit que les mots du monde, et sans leur ligne de
source : la bible ne va jamais sous les yeux du lecteur.
"""
import hashlib
import io
import os
import re

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, '..', '..', '..'))
SRC = os.path.join(RACINE, '02-univers', 'le-glossaire.md')
JS = os.path.join(ICI, 'p7-monde.js')
PAGE = os.path.join(RACINE, '05-manuscrit', 'glossaire.md')

md = io.open(SRC, encoding='utf-8').read()
# Sur les octets du fichier, pas sur le texte decode : sha256sum lit des
# octets, et io.open convertit les CRLF en LF au passage.
empreinte = hashlib.sha256(open(SRC, 'rb').read()).hexdigest()


def cle(mot):
    """L'ordre alphabetique, accents et guillemets ignores."""
    t = mot.lower()
    for a, b in ((u'é', 'e'), (u'è', 'e'), (u'ê', 'e'), (u'à', 'a'),
                 (u'ç', 'c'), (u'ô', 'o'), (u'û', 'u'), (u'î', 'i'),
                 (u'«', ''), (u'"', ''), (u'’', "'")):
        t = t.replace(a, b)
    return t.strip()


def decoupe(bloc):
    """Chaque entree : **Mot.** definition, puis une ligne > source [· ❓ question]."""
    entrees = []
    for morceau in re.split(r'\n\s*\n', bloc):
        morceau = morceau.strip()
        m = re.match(r'^\*\*(.+?)\.\*\*\s+(.*)$', morceau, re.S)
        if not m:
            continue
        mot = m.group(1).strip()
        reste = m.group(2)
        source, ouvert = u'', u''
        ligne = re.search(r'^>\s*(.*)$', reste, re.M)
        if ligne:
            meta = ligne.group(1).strip()
            reste = reste[:ligne.start()]
            if u'❓' in meta:
                source, ouvert = meta.split(u'❓', 1)
                source = source.rstrip(u' ·')
            else:
                source = meta
            source = source.strip().strip(u'`')
            ouvert = ouvert.strip()
        definition = u' '.join(reste.split())
        entrees.append((mot, definition, source, ouvert))
    return entrees


# ---------- les deux parties ----------
assert u'\n# Les mots du monde\n' in md, u'titre « Les mots du monde » introuvable'
assert u'\n# La bible\n' in md, u'titre « La bible » introuvable'
corps = md.split(u'\n# Les mots du monde\n', 1)[1]
part_monde, part_bible = corps.split(u'\n# La bible\n', 1)

MONDE = decoupe(part_monde)
BIBLE = decoupe(part_bible)
assert MONDE and BIBLE, u'une des deux parties est vide'

# ---------- l'ordre alphabetique, sur les mots du monde ----------
ordonne = sorted(MONDE, key=lambda e: cle(e[0]))
hors = [a[0] for a, b in zip(MONDE, ordonne) if a[0] != b[0]]
if hors:
    raise SystemExit(u'HORS ORDRE ALPHABETIQUE : ' + u', '.join(hors))

doubles = [m for m, n in zip(MONDE, MONDE[1:]) if cle(m[0]) == cle(n[0])]
if doubles:
    raise SystemExit(u'ENTREE EN DOUBLE : ' + u', '.join(d[0] for d in doubles))

# ---------- p7-monde.js ----------
B = u'`'
BS = chr(92)                       # la barre inverse


def sur(t):
    """Rien qui puisse fermer un litteral JS ni ouvrir une interpolation."""
    t = t.replace(BS, BS + BS)
    t = t.replace(B, BS + B)
    return t.replace(u'${', BS + u'${')


def tableau(nom, entrees):
    lignes = [u'[%s%s%s,%s%s%s,%s%s%s,%s%s%s],'
              % (B, sur(m), B, B, sur(d), B, B, sur(s), B, B, sur(o), B)
              for m, d, s, o in entrees]
    return u'const %s = [\n%s\n];\n' % (nom, u'\n'.join(lignes))


bloc = (u'/* Genere depuis 02-univers/le-glossaire.md par glossaire.py.\n'
        u'   Ne pas editer ici : editer le markdown, puis relancer le script.\n'
        u'   empreinte-source: %s */\n\n' % empreinte
        + tableau(u'GLOSSAIRE', MONDE) + u'\n' + tableau(u'BIBLE', BIBLE))

js = io.open(JS, encoding='utf-8').read()
deb = js.index(u'/* Genere depuis')
fin = js.index(u'const REGLES = [')
js = js[:deb] + bloc + u'\n' + js[fin:]
open(JS, 'wb').write(js.encode('utf-8'))

# ---------- la page du livre ----------
tete = (u'# Glossaire\n\n'
        u'*Page de fin de volume. Se lit vite, se consulte en cours de lecture, ne raconte rien.*\n\n'
        u'> ⚠️ **Cette page est générée depuis '
        u'[`../02-univers/le-glossaire.md`](../02-univers/le-glossaire.md).**\n'
        u'> *On corrige là-bas, jamais ici.*\n\n---\n\n')


def enveloppe(texte, largeur=94):
    """Un paragraphe par entree, coupe a la main comme le reste du dossier."""
    mots, ligne, out = texte.split(u' '), u'', []
    for w in mots:
        if ligne and len(ligne) + 1 + len(w) > largeur:
            out.append(ligne)
            ligne = w
        else:
            ligne = (ligne + u' ' + w).strip()
    if ligne:
        out.append(ligne)
    return u'\n'.join(out)


page = tete + u'\n\n'.join(enveloppe(u'**%s.** %s' % (m, d)) for m, d, _, _ in MONDE) + u'\n'
open(PAGE, 'wb').write(page.encode('utf-8'))

print(u'%d mots du monde, %d entrees de bible' % (len(MONDE), len(BIBLE)))
print(u'de « %s » a « %s »' % (MONDE[0][0], MONDE[-1][0]))
print(u'empreinte %s' % empreinte[:16])
