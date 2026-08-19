# -*- coding: utf-8 -*-
"""Verse le plan du jardin dans l'atelier.

Le plan de la ruche avait ete integre en prefixant tous ses identifiants et
en confinant sa feuille de style. Le plan du jardin passe autrement : la
page entiere est mise dans une iframe, et l'isolation est totale sans
renommer une seule classe. On peut donc modifier la page autonome sans
jamais se demander si un nom entre en collision avec l'atelier.

usage : python integrer-le-jardin.py   (depuis 06-visuels/)
"""
import io
import json
import re

SRC = u"plan-du-jardin.html"
DST = u"atelier/sources/pD-jardin.js"

page = io.open(SRC, encoding='utf-8').read()

# Une chaine JS qui contient </script> ferme la balise qui l'entoure : le
# navigateur ne lit pas le JavaScript, il cherche la fin du script.
brut = json.dumps(page, ensure_ascii=False).replace(u'</', u'<\\/')

part = u"""
/* ==========================================================================
   LE PLAN DU JARDIN — genere depuis 06-visuels/plan-du-jardin.html
   Ne pas editer ici : editer la page autonome, puis relancer
   06-visuels/integrer-le-jardin.py
   ========================================================================== */
const JARDIN_SRC = %s;

(function(){
  const b = document.querySelector('.rail-btn[data-vue="jardin"]');
  const v = document.getElementById('v-jardin');
  if(!b || !v) return;
  let pose = false;
  /* On ne fabrique la page qu'au premier clic : l'atelier s'ouvre en une
     seconde et le plan ne coute rien tant que personne ne le regarde. */
  b.addEventListener('click', () => {
    if(pose) return; pose = true;
    const f = document.createElement('iframe');
    f.title = 'Le plan du jardin';
    f.setAttribute('loading','lazy');
    f.srcdoc = JARDIN_SRC;
    v.appendChild(f);
  });
})();
""" % brut

io.open(DST, 'w', encoding='utf-8').write(part)

# ---------- le style, la vue et le bouton ----------
def injecter(fichier, balise, bloc, ancre, css=False):
    """css=True : marqueurs en commentaires CSS. Un commentaire HTML pose dans
       une feuille de style avale la premiere regle qui le suit."""
    t = io.open(fichier, encoding='utf-8').read()
    deb, fin = u'/*<<%s>>*/' % balise, u'/*<<fin %s>>*/' % balise
    if u'<' in ancre and not css:
        deb, fin = u'<!--<<%s>>-->' % balise, u'<!--<<fin %s>>-->' % balise
    t = re.sub(re.escape(deb) + u'.*?' + re.escape(fin), u'', t, flags=re.S)
    assert ancre in t, fichier + u' :: ' + ancre[:40]
    t = t.replace(ancre, deb + u'\n' + bloc + u'\n' + fin + u'\n' + ancre, 1)
    io.open(fichier, 'w', encoding='utf-8').write(t)


style = (u"#v-jardin{padding:0;height:100%;overflow:hidden}\n"
         u"#v-jardin iframe{width:100%;height:100%;border:0;display:block;"
         u"background:var(--fond)}\n"
         u"#v-jardin .attente{padding:60px;color:var(--texte-3);font-size:13px}\n")

vue = (u'    <!-- ================= LE PLAN DU JARDIN ================= -->\n'
       u'    <section class="vue" id="v-jardin">\n'
       u'      <div class="attente">Le plan s\'ouvre…</div>\n'
       u'    </section>')

bouton = (u'    <button class="rail-btn" data-vue="jardin" aria-label="Le plan du jardin">\n'
          u'      <svg viewBox="0 0 24 24">'
          u'<path d="M12 3c-3 2.5-4.5 5-4.5 7.5a4.5 4.5 0 0 0 9 0C16.5 8 15 5.5 12 3Z"/>'
          u'<path d="M12 13v8"/><path d="M8.5 21h7"/>'
          u'</svg><span>Le jardin</span>\n    </button>')

injecter(u'atelier/sources/p3-style.html', u'jardin-style', style, u'</style>', css=True)
injecter(u'atelier/sources/p4-corps.html', u'jardin-vue', vue, u'  </main>')
injecter(u'atelier/sources/p4-corps.html', u'jardin-bouton', bouton, u'    <div class="bas">')

print(u'ok — page %d caracteres, part %d' % (len(page), len(part)))
