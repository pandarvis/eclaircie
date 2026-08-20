#!/bin/sh
# Fabrique l'atelier a partir des douze morceaux, dans l'ordre.
# usage : sh fabriquer.sh        (depuis ce dossier)
set -e
ORDRE="p1-style.html p2-style.html p3-style.html p4-corps.html
       p5-scenes.js p6-notes.js p7-monde.js p8-gens.js p9-trancher.js
       pB-textes.js pC-ruche.js pD-jardin.js pA-app.js"

# Verification 0 : la copie du plan du jardin n'a pas pris de retard.
# Elle est figee ici ; la page autonome, elle, bouge. On a deja livre deux
# corrections que personne n'a jamais vues parce que cette copie dormait.
ATTENDU=$(sha256sum ../../plan-du-jardin.html | cut -d' ' -f1)
PORTE=$(sed -n 's|.*empreinte-source: ||p' pD-jardin.js | tr -d ' 
')
if [ "$ATTENDU" != "$PORTE" ]; then
  echo "PROBLEME : pD-jardin.js est en retard sur plan-du-jardin.html."
  echo "           relancer  python integrer-le-jardin.py  depuis 06-visuels/"
  exit 1
fi
echo "le plan du jardin : a jour"

# Verification 0 bis : le glossaire n'a pas pris de retard non plus.
# p7-monde.js et 05-manuscrit/glossaire.md sont generes depuis le markdown.
ATTENDU=$(sha256sum ../../../02-univers/le-glossaire.md | cut -d' ' -f1)
PORTE=$(grep -o 'empreinte-source: [0-9a-f]*' p7-monde.js | head -1 | cut -d' ' -f2)
if [ "$ATTENDU" != "$PORTE" ]; then
  echo "PROBLEME : p7-monde.js est en retard sur 02-univers/le-glossaire.md."
  echo "           relancer  python glossaire.py  depuis ce dossier"
  exit 1
fi
echo "le glossaire : a jour"

cat $ORDRE > ../atelier.html
echo "atelier.html fabrique"

# Verification 1 : le JavaScript est syntaxiquement correct.
cat p5-scenes.js p6-notes.js p7-monde.js p8-gens.js p9-trancher.js \
    pB-textes.js pC-ruche.js pD-jardin.js pA-app.js \
  | sed '1s|<script>||' | sed 's|</script>||;s|</body>||;s|</html>||' > combo.js
node --check combo.js && echo "syntaxe : correcte"

# Verification 2 : le controleur de coherence.
# Il tourne hors navigateur : pC-ruche.js et pD-jardin.js, qui touchent au DOM.
cat p5-scenes.js p6-notes.js p7-monde.js p8-gens.js p9-trancher.js \
    pB-textes.js pA-app.js \
  | sed '1s|<script>||' | sed 's|</script>||;s|</body>||;s|</html>||' > check.js
node ../valide.js
rm -f check.js combo.js
echo "FABRICATION OK"
