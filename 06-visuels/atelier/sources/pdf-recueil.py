# -*- coding: utf-8 -*-
"""Sort plusieurs chapitres a la suite, en une seule page imprimable.

  python pdf-recueil.py <sortie.html> <id> [<id> ...]

Chaque chapitre commence sur une page neuve. Les pages sont numerotees
en pied ; le premier feuillet, lui, ne l'est pas -- on ne numerote pas
une page de titre.

Aucun nombre de mots : c'est une lecture, pas un rapport.

Le PDF se tire ensuite avec Chrome :
  chrome --headless=new --print-to-pdf=sortie.pdf --no-pdf-header-footer sortie.html
"""
import io
import os
import re
import sys

if len(sys.argv) < 3:
    raise SystemExit(u'usage : python pdf-recueil.py <sortie.html> <id> [<id> ...]')

sortie, cibles = sys.argv[1], sys.argv[2:]
s = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pB-textes.js'),
            encoding='utf-8').read()


def chapitre(cible):
    d = s.index(u"id: `%s`" % cible)
    rang = re.search(r"rang: `([^`]*)`", s[d:]).group(1)
    titre = re.search(r"titre: `([^`]*)`", s[d:]).group(1)
    corps = s[s.index(u"p: [", d) + 4: s.index(u"\n  ],", d)]
    paras = re.findall(r"\[`(p|tiret|pause)`,`(.*?)`(?:,`\w+`)?\]", corps, re.S)
    assert len(paras) > 30, u'%s : %d paragraphes' % (cible, len(paras))
    lignes = []
    for genre, texte in paras:
        texte = texte.strip()
        if genre == u"pause":
            lignes.append(u'<p class="pause">* * *</p>')
        elif genre == u"tiret":
            lignes.append(u'<p class="dial">%s</p>' % texte)
        else:
            lignes.append(u'<p>%s</p>' % texte)
    return rang, titre, u"\n".join(lignes), len(paras)


SEPARATEUR = chr(10) + chr(10)

blocs, total = [], 0
for n, cible in enumerate(cibles):
    rang, titre, corps, nb = chapitre(cible)
    total += nb
    # Le titre ne sort pas : c'est une etiquette de travail, pas un
    # titre de chapitre -- decision de l'autrice, 23 aout 2026.
    blocs.append(u"""<section class="chap%s">
  <header class="ouverture">
    <h1>%s</h1>
    <div class="filet"></div>
  </header>
%s
</section>""" % (u' premier' if n == 0 else u'', rang, corps))

page = u"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>L'Éclaircie</title>
<style>
@page {
  size: A4; margin: 26mm 26mm 22mm 26mm;
}
html { font-size: 12pt; }
body {
  font-family: Cambria, Constantia, "Palatino Linotype", Georgia, serif;
  line-height: 1.72; color: #16181c; margin: 0; text-align: justify;
  hyphens: auto; -webkit-hyphens: auto;
  counter-reset: page 0;
}

/* ---------- le bandeau de tete, sur la premiere page seulement ---------- */
.bandeau { text-align: center; margin: 0 0 22mm 0; page-break-after: avoid; }
.bandeau .oeuvre {
  font: 400 12pt/1 Cambria, Georgia, serif; letter-spacing: .42em;
  text-transform: uppercase; color: #16181c;
}
.bandeau .filet { width: 40mm; height: 1px; background: #b9bec6; margin: 7mm auto 0; }

/* ---------- l'ouverture d'un chapitre ---------- */
section { page-break-before: always; }
section.premier { page-break-before: avoid; }
.ouverture { text-align: center; margin: 0 0 20mm 0; page-break-after: avoid; }
.ouverture h1 {
  font: 400 19pt/1.25 Cambria, Georgia, serif; letter-spacing: .04em;
  margin: 0 0 5mm; font-variant: small-caps;
}
.ouverture .filet { width: 30mm; height: 1px; background: #b9bec6; margin: 0 auto; }

/* ---------- le corps ---------- */
p { margin: 0; text-indent: 5.5mm; orphans: 3; widows: 3; }
.ouverture + p, .pause + p, .dial + p { text-indent: 0; }
p.dial { text-indent: 0; margin-top: 1.6mm; }
p.dial + p.dial { margin-top: 0; }
p + p.dial { margin-top: 3.2mm; }
p.pause { text-indent: 0; text-align: center; margin: 6mm 0; color: #9aa0a8; letter-spacing: .5em; }
em { font-style: italic; }
</style></head><body>

<div class="bandeau">
  <div class="oeuvre">L'Éclaircie</div>
  <div class="filet"></div>
</div>

%s
</body></html>""" % SEPARATEUR.join(blocs)

io.open(sortie, 'w', encoding='utf-8').write(page)
print(u"%d chapitres, %d paragraphes -> %s" % (len(cibles), total, sortie))
