# -*- coding: utf-8 -*-
"""Sort n'importe quel chapitre en page imprimable, depuis la source de l'atelier.
   usage : python pdf3.py <id> <rang> <sous-titre> <fichier-de-sortie>"""
import io, re, sys

cible, rang, sous, sortie = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

s = io.open('pB-textes.js', encoding='utf-8').read()
d = s.index(u"id: `%s`" % cible)
corps = s[s.index(u"p: [", d) + 4 : s.index(u"\n  ],", d)]

paras = re.findall(r"\[`(p|tiret|pause)`,`(.*?)`(?:,`\w+`)?\]", corps, re.S)
assert len(paras) > 30, len(paras)

lignes = []
for genre, texte in paras:
    texte = texte.strip()
    if genre == u"pause":
        lignes.append(u'<p class="pause">* * *</p>')
    elif genre == u"tiret":
        lignes.append(u'<p class="dial">%s</p>' % texte)
    else:
        lignes.append(u'<p>%s</p>' % texte)

mots = len(re.sub(r"<[^>]+>", "", u" ".join(t for _, t in paras)).split())

page = u"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>L'Éclaircie — %s</title>
<style>
@page { size: A4; margin: 28mm 26mm 26mm 26mm; }
html { font-size: 12pt; }
body {
  font-family: Cambria, Constantia, "Palatino Linotype", Georgia, serif;
  line-height: 1.72; color: #16181c; margin: 0; text-align: justify;
  hyphens: auto; -webkit-hyphens: auto;
}
.titre { text-align: center; margin: 0 0 26mm 0; page-break-after: avoid; }
.titre .oeuvre {
  font: 400 10pt/1 Cambria, Georgia, serif; letter-spacing: .34em;
  text-transform: uppercase; color: #6a6f78;
}
.titre h1 {
  font: 400 21pt/1.2 Cambria, Georgia, serif; letter-spacing: .04em;
  margin: 9mm 0 6mm; font-variant: small-caps;
}
.titre .filet { width: 34mm; height: 1px; background: #b9bec6; margin: 0 auto; }
.titre .info {
  font: italic 9.5pt/1.5 Cambria, Georgia, serif; color: #8a9099; margin-top: 6mm;
}
p { margin: 0; text-indent: 5.5mm; orphans: 3; widows: 3; }
p:first-of-type, .pause + p, .dial + p { text-indent: 0; }
p.dial { text-indent: 0; margin-top: 1.6mm; }
p.dial + p.dial { margin-top: 0; }
p + p.dial { margin-top: 3.2mm; }
p.pause { text-indent: 0; text-align: center; margin: 6mm 0; color: #9aa0a8; letter-spacing: .5em; }
em { font-style: italic; }
</style></head><body>
<div class="titre">
  <div class="oeuvre">L'Éclaircie</div>
  <h1>%s</h1>
  <div class="filet"></div>
  <div class="info">%s<br>%d mots</div>
</div>
%s
</body></html>""" % (rang, rang, sous, mots, u"\n".join(lignes))

io.open(sortie, 'w', encoding='utf-8').write(page)
print(u"%d paragraphes, %d mots -> %s" % (len(paras), mots, sortie))
