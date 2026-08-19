# -*- coding: utf-8 -*-
"""Ecarte des chemins tout ce qui les mord, et rend les nouvelles positions.

Treize batiments poses a l'oeil finissent toujours par mordre un trace :
corriger a la main en cree d'autres ailleurs. Le calcul, lui, converge.

Pour chaque batiment qui touche une voie, on cherche le plus petit
deplacement qui le degage -- seize directions, par pas de deux -- sans le
faire sortir du mur, sans le mettre dans la mare et sans le poser sur un
voisin. La mare est traitee pareil.

usage : python degager-les-chemins.py      (ecrit les nouvelles positions)
"""
import io
import json
import os
import re
import subprocess

CHROME = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ICI, 'plan-du-jardin.html')
TMP = os.path.join(ICI, '.solveur.html')

SONDE = u"""<script>
setTimeout(function(){
  try{
    var svg=document.getElementById('svg');
    var pt=svg.createSVGPoint();
    var P=PLANS[2];
    var voies=[].slice.call(svg.querySelectorAll('.anneau, .chemin, .allee, .trajet'));
    var mare=svg.querySelector('.eau');
    var murPath=svg.querySelector('.mur');

    function tourner(px,py,cx,cy,deg){
      var a=deg*Math.PI/180, c=Math.cos(a), s=Math.sin(a);
      return [cx+(px-cx)*c-(py-cy)*s, cy+(px-cx)*s+(py-cy)*c];
    }
    function contour(x,y,w,h,ang){
      var cx=x+w/2, cy=y+h/2, out=[], N=28;
      for(var i=0;i<N;i++){
        var t=i/N*4, c=Math.floor(t), u=t-c;
        var px = c===0 ? x+w*u : c===1 ? x+w : c===2 ? x+w*(1-u) : x;
        var py = c===0 ? y     : c===1 ? y+h*u : c===2 ? y+h     : y+h*(1-u);
        out.push(ang ? tourner(px,py,cx,cy,ang) : [px,py]);
      }
      return out;
    }
    /* Deux tests, et il faut les deux : le contour du batiment peut eviter
       le trace alors que le trace lui passe au travers -- et l'inverse. */
    var echant=[];
    voies.forEach(function(c){
      var L=c.getTotalLength();
      for(var i=0;i<=500;i++){ var q=c.getPointAtLength(L*i/500); echant.push([q.x,q.y]); }
    });
    function surVoie(pts,x,y,w,h,ang){
      for(var i=0;i<pts.length;i++){
        pt.x=pts[i][0]; pt.y=pts[i][1];
        for(var j=0;j<voies.length;j++) if(voies[j].isPointInStroke(pt)) return true;
        if(mare && mare.isPointInFill(pt)) return true;
      }
      var cx=x+w/2, cy=y+h/2;
      for(var k=0;k<echant.length;k++){
        var q=echant[k];
        var p2 = ang ? tourner(q[0],q[1],cx,cy,-ang) : q;
        if(p2[0]>x-4 && p2[0]<x+w+4 && p2[1]>y-4 && p2[1]<y+h+4) return true;
      }
      return false;
    }
    function dansMur(pts){
      for(var i=0;i<pts.length;i++){
        pt.x=pts[i][0]; pt.y=pts[i][1];
        if(!murPath.isPointInFill(pt)) return false;
      }
      return true;
    }
    function chevauche(a,b){
      return a[1]<b[1]+b[3] && a[1]+a[3]>b[1] && a[2]<b[2]+b[4] && a[2]+a[4]>b[2];
    }

    var bat=P.bat.map(function(b){return b.slice();});
    var libre=function(k,x,y){
      var b=bat[k], ang=b[7]===1?-11:(b[7]||0);
      var pts=contour(x,y,b[3],b[4],ang);
      if(surVoie(pts,x,y,b[3],b[4],ang)) return false;
      if(!dansMur(pts)) return false;
      for(var i=0;i<bat.length;i++){
        if(i===k) continue;
        var c=bat[i];
        if(x<c[1]+c[3] && x+b[3]>c[1] && y<c[2]+c[4] && y+b[4]>c[2]) return false;
      }
      return true;
    };

    var bouges={}, restes=[];
    for(var k=0;k<bat.length;k++){
      var b=bat[k];
      if(libre(k,b[1],b[2])) continue;
      var trouve=false;
      for(var r=2;r<=70 && !trouve;r+=2){
        for(var a=0;a<16 && !trouve;a++){
          var th=a/16*Math.PI*2;
          var nx=Math.round(b[1]+Math.cos(th)*r), ny=Math.round(b[2]+Math.sin(th)*r);
          if(libre(k,nx,ny)){
            bouges[b[5]]=[b[1],b[2],nx,ny];
            bat[k][1]=nx; bat[k][2]=ny; trouve=true;
          }
        }
      }
      if(!trouve) restes.push(b[5]);
    }

    /* La mare : meme traitement, sans changer sa forme. */
    var mareBouge=null;
    if(mare && P.eau){
      var e=P.eau, LM=mare.getTotalLength();
      var contourMare=function(dx,dy){
        var out=[];
        for(var j=0;j<160;j++){
          var q=mare.getPointAtLength(LM*j/160);
          out.push([q.x+dx,q.y+dy]);
        }
        return out;
      };
      var libreMare=function(dx,dy){
        var pts=contourMare(dx,dy);
        for(var i=0;i<pts.length;i++){
          pt.x=pts[i][0]; pt.y=pts[i][1];
          for(var j=0;j<voies.length;j++) if(voies[j].isPointInStroke(pt)) return false;
        }
        for(var i2=0;i2<bat.length;i2++){
          var c=bat[i2];
          for(var m=0;m<pts.length;m++)
            if(pts[m][0]>c[1]&&pts[m][0]<c[1]+c[3]&&pts[m][1]>c[2]&&pts[m][1]<c[2]+c[4])
              return false;
        }
        return true;
      };
      if(!libreMare(0,0)){
        for(var r2=2;r2<=60 && !mareBouge;r2+=2)
          for(var a2=0;a2<16 && !mareBouge;a2++){
            var th2=a2/16*Math.PI*2;
            var dx=Math.round(Math.cos(th2)*r2), dy=Math.round(Math.sin(th2)*r2);
            if(libreMare(dx,dy)) mareBouge=[e[0],e[1],e[0]+dx,e[1]+dy];
          }
      }
    }

    document.title='SOLVEUR|'+JSON.stringify({b:bouges,m:mareBouge,ko:restes});
  }catch(e){ document.title='SOLVEUR|{"erreur":"'+e.message+'"}'; }
},1800);
</script>"""

page = io.open(SRC, encoding='utf-8').read()
io.open(TMP, 'w', encoding='utf-8').write(page.replace(u'</body>', SONDE + u'</body>', 1))
url = 'file:///' + TMP.replace('\\', '/')
out = subprocess.Popen(
    [CHROME, '--headless=new', '--disable-gpu', '--virtual-time-budget=40000',
     '--dump-dom', url],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode('utf-8', 'replace')
os.remove(TMP)

m = re.search(r'<title>SOLVEUR\|(.*?)</title>', out, re.S)
if not m:
    print(u"la sonde n'a rien rendu")
    raise SystemExit(1)
d = json.loads(m.group(1).replace('&quot;', '"'))
if 'erreur' in d:
    print(u'erreur : ' + d['erreur'])
    raise SystemExit(1)

page = io.open(SRC, encoding='utf-8').read()
n = 0
for nom, (x0, y0, x1, y1) in sorted(d['b'].items()):
    vieux = u",%d,%d," % (x0, y0)
    ligne = [l for l in page.split('\n')
             if vieux in l and (u"'" + nom.replace(u"'", u"\\'") + u"'") in l]
    assert len(ligne) == 1, u'%s : %d ligne(s)' % (nom, len(ligne))
    page = page.replace(ligne[0], ligne[0].replace(vieux, u",%d,%d," % (x1, y1), 1), 1)
    print(u'  %-22s (%d,%d) -> (%d,%d)' % (nom, x0, y0, x1, y1))
    n += 1
if d.get('m'):
    x0, y0, x1, y1 = d['m']
    page = page.replace(u' eau:[%d,%d,' % (x0, y0), u' eau:[%d,%d,' % (x1, y1), 1)
    print(u'  %-22s (%d,%d) -> (%d,%d)' % (u'la mare', x0, y0, x1, y1))
    n += 1
io.open(SRC, 'w', encoding='utf-8').write(page)

print(u'\n%d deplacement(s)' % n)
if d.get('ko'):
    print(u'sans solution : ' + u', '.join(d['ko']))
