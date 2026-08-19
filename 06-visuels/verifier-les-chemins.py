# -*- coding: utf-8 -*-
"""Aucun chemin ne mord un batiment, et la mare ne touche aucun chemin.

Le controleur des rectangles ne voyait que les rectangles. Les chemins sont
lisses au rendu : leur trace reel ne se calcule pas depuis les points, il se
mesure dans le navigateur.

Et on ne teste pas l'axe du chemin mais sa largeur : une allee de neuf
pixels mord un batiment que son axe evite. On echantillonne donc le
contour de chaque batiment et de la mare, et on demande a chaque trace
s'il passe dessus -- isPointInStroke repond exactement.

usage : python verifier-les-chemins.py
"""
import io
import os
import re
import subprocess
import sys

CHROME = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ICI, 'plan-du-jardin.html')
TMP = os.path.join(ICI, '.controle-chemins.html')

SONDE = u"""<script>
setTimeout(function(){
  var rz=document.querySelectorAll('#reseaux .rz');
  if(rz.length && rz[__N__]) rz[__N__].click();
},900);
setTimeout(function(){
  try{
    var svg=document.getElementById('svg');
    var pt=svg.createSVGPoint();
    var bats=[].slice.call(svg.querySelectorAll('[data-nom]'));
    var mare=svg.querySelector('.eau');
    var voies=[].slice.call(svg.querySelectorAll('.anneau, .chemin, .allee, .trajet'));
    var nomVoie=function(c){return c.getAttribute('data-voie')||c.getAttribute('class');};
    var fautes={};

    /* Le contour d'un rectangle, dans le repere du dessin (rotation comprise). */
    var contourBat=function(b){
      var x=+b.getAttribute('x'), y=+b.getAttribute('y');
      var w=+b.getAttribute('width'), h=+b.getAttribute('height');
      /* getCTM() descend jusqu'aux pixels de l'ecran. Ce qu'il faut ici,
         c'est la transformation propre du rectangle -- sa rotation -- qui
         l'amene dans le repere du dessin, celui des chemins. */
      var tr=b.transform.baseVal.consolidate();
      var m=tr ? tr.matrix : svg.createSVGMatrix();
      var out=[], N=24;
      for(var i=0;i<N;i++){
        var t=i/N*4, c=Math.floor(t), u=t-c;
        var px = c===0 ? x+w*u : c===1 ? x+w : c===2 ? x+w*(1-u) : x;
        var py = c===0 ? y     : c===1 ? y+h*u : c===2 ? y+h     : y+h*(1-u);
        pt.x=px; pt.y=py; out.push(pt.matrixTransform(m));
      }
      return out;
    };

    bats.forEach(function(b){
      var pts=contourBat(b);
      voies.forEach(function(c){
        for(var i=0;i<pts.length;i++){
          pt.x=pts[i].x; pt.y=pts[i].y;
          if(c.isPointInStroke(pt)){
            fautes['"'+nomVoie(c)+'" mord "'+b.getAttribute('data-nom')+'"']=1;
            return;
          }
        }
      });
    });

    if(mare){
      var LM=mare.getTotalLength();
      for(var j=0;j<=300;j++){
        var m2=mare.getPointAtLength(LM*j/300);
        pt.x=m2.x; pt.y=m2.y;
        voies.forEach(function(c){
          if(c.isPointInStroke(pt)) fautes['LA MARE touche "'+nomVoie(c)+'"']=1;
        });
        bats.forEach(function(b){
          var tr2=b.transform.baseVal.consolidate();
          var mm=tr2 ? tr2.matrix : svg.createSVGMatrix();
          pt.x=m2.x; pt.y=m2.y;
          var q=pt.matrixTransform(mm.inverse());
          if(b.isPointInFill(q)) fautes['LA MARE touche "'+b.getAttribute('data-nom')+'"']=1;
        });
      }
      /* Et l'inverse : un chemin qui passerait dans l'eau. */
      voies.forEach(function(c){
        var L=c.getTotalLength();
        for(var k=0;k<=400;k++){
          var q=c.getPointAtLength(L*k/400);
          pt.x=q.x; pt.y=q.y;
          if(mare.isPointInFill(pt)){ fautes['"'+nomVoie(c)+'" passe dans la mare']=1; break; }
        }
      });
    }

    var l=Object.keys(fautes);
    var on=document.querySelector('#reseaux .rz.on');
    document.title='CONTROLE|'+(on?on.textContent:'plan')+'|'+bats.length+'|'
      +(l.length?l.join(' ~ '):'RIEN');
  }catch(e){ document.title='CONTROLE|0|0|ERREUR '+e.message; }
},1700);
</script>"""

N = sys.argv[1] if len(sys.argv) > 1 else '0'
page = io.open(SRC, encoding='utf-8').read()
io.open(TMP, 'w', encoding='utf-8').write(
    page.replace(u'</body>', SONDE.replace('__N__', N) + u'</body>', 1))

url = 'file:///' + TMP.replace('\\', '/')
out = subprocess.Popen(
    [CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=40000',
     '--dump-dom', url],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode('utf-8', 'replace')
os.remove(TMP)

m = re.search(r'<title>CONTROLE\|(.*?)\|(\d+)\|(.*?)</title>', out, re.S)
if not m:
    print(u"la sonde n'a rien rendu")
    raise SystemExit(1)

print(u'reseau : %s   (%s batiments testes)' % (m.group(1), m.group(2)))
if m.group(3) == 'RIEN':
    print(u'\nAucun chemin ne mord un batiment, et la mare ne touche rien.')
else:
    fautes = m.group(3).split(' ~ ')
    print(u'\n%d faute(s) :' % len(fautes))
    for x in fautes:
        print(u'  ' + x)
