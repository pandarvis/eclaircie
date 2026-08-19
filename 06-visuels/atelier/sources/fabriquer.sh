#!/bin/sh
# Fabrique l'atelier a partir des douze morceaux, dans l'ordre.
# usage : sh fabriquer.sh        (depuis ce dossier)
set -e
ORDRE="p1-style.html p2-style.html p3-style.html p4-corps.html
       p5-scenes.js p6-notes.js p7-monde.js p8-gens.js p9-trancher.js
       pB-textes.js pC-ruche.js pA-app.js"

cat $ORDRE > ../atelier.html
echo "atelier.html fabrique"

# Verification 1 : le JavaScript est syntaxiquement correct.
cat p5-scenes.js p6-notes.js p7-monde.js p8-gens.js p9-trancher.js \
    pB-textes.js pC-ruche.js pA-app.js \
  | sed '1s|<script>||' | sed 's|</script>||;s|</body>||;s|</html>||' > combo.js
node --check combo.js && echo "syntaxe : correcte"

# Verification 2 : le controleur de coherence.
# Il tourne hors navigateur : pC-ruche.js, qui touche au DOM, en est exclu.
cat p5-scenes.js p6-notes.js p7-monde.js p8-gens.js p9-trancher.js \
    pB-textes.js pA-app.js \
  | sed '1s|<script>||' | sed 's|</script>||;s|</body>||;s|</html>||' > check.js
node ../valide.js
rm -f check.js combo.js
