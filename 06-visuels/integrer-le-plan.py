# -*- coding: utf-8 -*-
"""Verse le plan de la ruche dans l'atelier, depuis la page autonome.
   Relancable : les parties injectees sont delimitees par des balises."""
import io, re

SRC = u"R:/Documents/l'Eclaircie/06-visuels/plan-de-la-ruche.html"
src = io.open(SRC, encoding='utf-8').read()

css    = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
js     = re.search(r'<script>(.*?)</script>', src, re.S).group(1)
markup = re.search(r'<body>(.*?)<script>', src, re.S).group(1)

# ---------- 1. les identifiants sont prefixes ----------
IDS = ['app','scene','svg','titre','flotte','panneau','pan-corps','accueil-pan',
       'pan-fiche','pan-num','pan-titre','pan-sur','pan-txt','cmd','reset',
       'trace','voyageur','halo-reg','c-fond','c-coulee','c-caps','c-bat',
       'c-trace','c-etiq','c-zone']
def prefixer(t):
    for x in sorted(IDS, key=len, reverse=True):
        t = t.replace(u'id="%s"' % x, u'id="r-%s"' % x)
        t = t.replace(u"getElementById('%s')" % x, u"getElementById('r-%s')" % x)
        t = t.replace(u"g('%s')" % x, u"g('r-%s')" % x)
        t = t.replace(u"id:'%s'" % x, u"id:'r-%s'" % x)
        t = re.sub(r'#' + re.escape(x) + r'(?=[\s{,.:>])', u'#r-' + x, t)
    return t
css, js, markup = prefixer(css), prefixer(js), prefixer(markup)

# ---------- 2. la feuille de style est confinee a la vue ----------
def scoper(feuille, pref):
    out, i, n = [], 0, len(feuille)
    while i < n:
        j = feuille.find(u'{', i)
        if j < 0:
            break
        sel = feuille[i:j].strip()
        if sel.startswith(u'@'):
            d, k = 0, j
            while k < n:
                if feuille[k] == u'{': d += 1
                elif feuille[k] == u'}':
                    d -= 1
                    if d == 0: break
                k += 1
            inner = feuille[j+1:k]
            out.append(sel + u'{' + (scoper(inner, pref) if sel.startswith(u'@media') else inner) + u'}')
            i = k + 1
            continue
        k = feuille.find(u'}', j)
        corps, sels = feuille[j+1:k], []
        for sp in sel.split(u','):
            sp = sp.strip()
            if not sp or sp == u'html': continue
            if sp in (u':root', u'body'): sels.append(pref)
            elif sp == u'*': sels.append(pref + u' *')
            else: sels.append(pref + u' ' + sp)
        if sels: out.append(u', '.join(sels) + u'{' + corps + u'}')
        i = k + 1
    return u'\n'.join(out)

css = scoper(css, u'#v-ruche').replace(u'100vh', u'100%')
css = css.replace(u'#v-ruche{margin:0;height:100%}', u'')

# ---------- 3. la vue, et le bouton du rail ----------
markup = markup.strip()
vue = (u'\n    <!-- ================= LE PLAN DE LA RUCHE ================= -->\n'
       u'    <section class="vue" id="v-ruche">\n' + markup + u'\n    </section>\n')

bouton = (u'    <button class="rail-btn" data-vue="ruche" aria-label="Le plan de la ruche">\n'
          u'      <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/>'
          u'<path d="M12 9V4M12 15v5M9 12H4M15 12h5M9.9 9.9 6.3 6.3M14.1 14.1l3.6 3.6M14.1 9.9l3.6-3.6M9.9 14.1l-3.6 3.6"/>'
          u'</svg><span>La ruche</span>\n    </button>\n')

# ---------- 4. le script, sans le hash ni les fleches ----------
js = re.sub(r"/\* ouverture directe.*?window\.addEventListener\('hashchange',depuisHash\);", u'', js, flags=re.S)
js = re.sub(r"/\* les fleches pour passer.*?\}\);\s*$", u'', js, flags=re.S)
js = js.replace(u"\n", u"\n  ")
part = (u"\n/* ==========================================================================\n"
        u"   LE PLAN DE LA RUCHE — genere depuis 06-visuels/plan-de-la-ruche.html\n"
        u"   Ne pas editer ici : editer la page autonome, puis relancer integrer.py\n"
        u"   ========================================================================== */\n"
        u"(function(){\n  let bati=false;\n  function batir(){\n    if(bati) return; bati=true;\n  "
        + js + u"\n  }\n"
        u"  const b=document.querySelector('.rail-btn[data-vue=\"ruche\"]');\n"
        u"  if(b) b.addEventListener('click',batir);\n})();\n")
io.open('pC-ruche.js', 'w', encoding='utf-8').write(part)

# ---------- 5. injection dans les parties ----------
def injecter(fichier, balise, bloc, ancre):
    t = io.open(fichier, encoding='utf-8').read()
    deb, fin = u'/*<<%s>>*/' % balise, u'/*<<fin %s>>*/' % balise
    if u'<' in ancre:   # markup : balises HTML
        deb, fin = u'<!--<<%s>>-->' % balise, u'<!--<<fin %s>>-->' % balise
    t = re.sub(re.escape(deb) + u'.*?' + re.escape(fin), u'', t, flags=re.S)
    assert ancre in t, fichier + u' :: ' + ancre[:40]
    t = t.replace(ancre, deb + u'\n' + bloc + u'\n' + fin + u'\n' + ancre, 1)
    io.open(fichier, 'w', encoding='utf-8').write(t)

injecter('p3-style.html', u'ruche-style', css, u'</style>')
injecter('p4-corps.html', u'ruche-vue',   vue, u'  </main>')
injecter('p4-corps.html', u'ruche-bouton', bouton, u'    <div class="bas">')
print(u'ok — css %d, markup %d, js %d' % (len(css), len(vue), len(part)))
