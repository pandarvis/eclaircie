
/* ==========================================================================
   L'APPLICATION
   ========================================================================== */
const $  = (s, r) => (r || document).querySelector(s);
const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
const esc = s => String(s == null ? `` : s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
/* **gras** et *italique* dans les textes de données */
/* Quatre marques, et rien d'autre. Elles remplacent les pastilles :
   un mot se lit, un rond rouge ne dit rien — et il y en avait trente-sept. */
/* Le rond rouge marquait « ça vient d'elle, ne le perds pas ». Il y en avait
   trente-sept : il ne marquait donc plus rien. On ne garde que l'état. */
const MARQ = { '⛔':[`i`,`interdit`], '⚠':[`t`,`à trancher`], '✅':[`v`,`tranché`] };
/* Sur les cartes du plateau, tout le balisage saute : ni marque, ni gras,
   ni italique. Un aperçu se survole, il ne se lit pas. */
const nu = s => esc(String(s == null ? `` : s)
  .replace(/[\u{1F534}⛔⚠✅]️?\s*/gu, ``)
  .replace(/\*\*(.+?)\*\*/g, `$1`)
  .replace(/(^|[\s(«"])\*(?!\s)(.+?)\*/g, `$1$2`));
const rich = s => esc(s)
  /* Un seul gras par bloc. Tout souligner revient a ne rien souligner :
     la premiere emphase reste, les suivantes redeviennent du texte. */
  .replace(/\*\*(.+?)\*\*/g, (m, t, i, whole) =>
    whole.slice(0, i).includes(`**`) ? t : `<strong>${t}</strong>`)
  .replace(/\*\*/g, ``)
  .replace(/(^|[\s(«"])\*(?!\s)(.+?)\*/g, `$1<em>$2</em>`)
  .replace(/\u{1F534}️?\s*/gu, ``)
  .replace(/(⛔|⚠|✅)️?\s*/gu,
           (m, e) => `<span class="marq m-${MARQ[e][0]}">${MARQ[e][1]}</span>`);
const ST = { acquis:`acquis`, provisoire:`provisoire`, trou:`à trouver`, ouvert:`ouvert`, ecarte:`écarté` };

/* ---------- mémoire du navigateur, avec repli ----------
   Certains contextes interdisent le stockage. Le document doit fonctionner
   quand même : on retombe alors sur une mémoire vive, perdue en fermant. */
const memo = (() => {
  let dispo = false;
  try { localStorage.setItem(`__essai`, `1`); localStorage.removeItem(`__essai`); dispo = true; } catch (e) {}
  const tampon = Object.create(null);
  return {
    dispo,
    lire: k => { try { return dispo ? localStorage.getItem(k) : (k in tampon ? tampon[k] : null); }
                 catch (e) { return k in tampon ? tampon[k] : null; } },
    ecrire: (k, v) => { tampon[k] = v; try { if (dispo) localStorage.setItem(k, v); } catch (e) {} },
    effacer: k => { delete tampon[k]; try { if (dispo) localStorage.removeItem(k); } catch (e) {} }
  };
})();

/* ---------- thème ---------- */
const clefTheme = `eclaircie-theme`;
function poserTheme(t){
  if (t) document.documentElement.setAttribute(`data-theme`, t);
  else document.documentElement.removeAttribute(`data-theme`);
}
const SOLEIL = `<circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.4M12 19.6V22M2 12h2.4M19.6 12H22M4.9 4.9l1.7 1.7M17.4 17.4l1.7 1.7M19.1 4.9l-1.7 1.7M6.6 17.4l-1.7 1.7"/>`;
const LUNE = `<path d="M20 14.2A8.4 8.4 0 0 1 9.8 4a8.4 8.4 0 1 0 10.2 10.2z"/>`;
function themeActuel(){
  return document.documentElement.getAttribute(`data-theme`)
    || (matchMedia(`(prefers-color-scheme: dark)`).matches ? `dark` : `light`);
}
function marquerTheme(){
  const vaVers = themeActuel() === `dark` ? `light` : `dark`;
  const b = $(`#btn-theme`);
  $(`svg`, b).innerHTML = vaVers === `dark` ? LUNE : SOLEIL;
  $(`span`, b).textContent = vaVers === `dark` ? `Sombre` : `Clair`;
  b.setAttribute(`aria-label`, vaVers === `dark` ? `Passer au thème sombre` : `Passer au thème clair`);
  b.title = vaVers === `dark` ? `Passer au thème sombre` : `Passer au thème clair`;
}
poserTheme(memo.lire(clefTheme));
marquerTheme();
$(`#btn-theme`).addEventListener(`click`, () => {
  const t = themeActuel() === `dark` ? `light` : `dark`;
  poserTheme(t); memo.ecrire(clefTheme, t);
  marquerTheme(); dessinerCourbes();
});

/* ---------- navigation ---------- */
$$(`.rail-btn[data-vue]`).forEach(b => b.addEventListener(`click`, () => {
  $$(`.rail-btn[data-vue]`).forEach(x => x.classList.remove(`on`));
  $$(`.vue`).forEach(v => v.classList.remove(`on`));
  b.classList.add(`on`);
  $(`#v-` + b.dataset.vue).classList.add(`on`);
  if (b.dataset.vue === `monde`) dessinerCourbes();
}));

function souffler(txt){
  const s = $(`#souffleur`); s.innerHTML = txt; s.classList.add(`on`);
  clearTimeout(s._t); s._t = setTimeout(() => s.classList.remove(`on`), 2600);
}
$(`#btn-aide`).addEventListener(`click`, () => souffler(
  `<kbd>←</kbd> <kbd>→</kbd> scène précédente / suivante &nbsp;·&nbsp; <kbd>Échap</kbd> fermer le dossier &nbsp;·&nbsp; tout est enregistré dans ce navigateur`));

/* ==========================================================================
   VUE 1 — LE PARCOURS
   ========================================================================== */
const COLW = 268, NODEW = 208, NODEH = 134, X0 = 172, BANDEH = 44;
/* deux voies de récit, et entre elles la bande mince des étapes */
let ROWY = { andrew: 60, commun: 226, joel: 300 }, HAUT = 500;
function mesurerVoies(){
  const dispo = $(`#plateau`).clientHeight;
  HAUT = Math.max(470, dispo - 12);
  const trou = Math.max(20, (HAUT - 2 * NODEH - BANDEH) / 4);
  ROWY = {
    andrew: trou,
    commun: 2 * trou + NODEH,
    joel:   3 * trou + NODEH + BANDEH
  };
}

let filtreVoie = `tous`;
let scenesVisibles = SCENES.slice();
let idSel = null;

/* filtres de voie */
(function filtresParcours(){
  const box = $(`#f-parcours`);
  const opts = [[`tous`,`tout le parcours`],[`andrew`,`Andrew`],[`joel`,`Joël`],[`gris`,`non écrites`],[`trou`,`à trouver`]];
  opts.forEach(([k, lab]) => {
    const b = document.createElement(`button`);
    b.className = `puce` + (k === `tous` ? ` on` : ``);
    const n = k === `tous` ? SCENES.length
            : k === `trou` ? SCENES.filter(s => s.statut === `trou`).length
            : k === `gris` ? SCENES.filter(s => s.gris).length
            : SCENES.filter(s => s.row === k && !s.gris).length;
    b.innerHTML = esc(lab) + `<span class="n">${n}</span>`;
    b.addEventListener(`click`, () => {
      filtreVoie = k;
      $$(`#f-parcours .puce`).forEach(x => x.classList.remove(`on`));
      b.classList.add(`on`);
      construirePlateau();
    });
    box.appendChild(b);
  });
})();

const colX = c => X0 + c * COLW;

function construirePlateau(){
  const carte = $(`#carte`);
  mesurerVoies();
  $$(`.noeud, .acte, .voie-nom, .etape, .lot`, carte).forEach(e => e.remove());

  scenesVisibles = filtreVoie === `tous` ? SCENES
    : filtreVoie === `trou` ? SCENES.filter(s => s.statut === `trou`)
    : filtreVoie === `gris` ? SCENES.filter(s => s.gris)
    : SCENES.filter(s => s.row === filtreVoie && !s.gris);
  scenesVisibles = scenesVisibles.slice().sort((a, b) => a.col - b.col);

  const colMax = Math.max(...SCENES.map(s => s.col));
  const larg = colX(colMax) + NODEW + 90;
  carte.style.width = larg + `px`;
  carte.style.minHeight = HAUT + `px`;

  /* fond : les travées */
  const tv = $(`#travees`);
  tv.setAttribute(`viewBox`, `0 0 ${larg} ${HAUT}`);
  tv.setAttribute(`width`, larg); tv.setAttribute(`height`, HAUT);
  let f = ``;
  for (let x = X0 - 40; x < larg; x += 67)
    f += `<line x1="${x}" y1="0" x2="${x}" y2="${HAUT}" stroke="var(--trait)" stroke-width=".5" opacity=".35"/>`;
  [`andrew`, `joel`].forEach(k => {
    f += `<rect x="0" y="${ROWY[k] - 14}" width="${larg}" height="${NODEH + 28}" fill="var(--fond-2)" opacity=".38"/>`;
  });
  f += `<rect x="0" y="${ROWY.commun - 8}" width="${larg}" height="${BANDEH + 16}" fill="var(--fond-2)" opacity=".22"/>`;
  tv.innerHTML = f;

  /* les lots : posés avant tout le reste, ils passent derrière */
  if (filtreVoie === `tous`) BLOCS.forEach(b => {
    const d = document.createElement(`div`);
    d.className = `lot` + (b.pic ? ` pic` : ``) + (b.vert ? ` vert` : ``);
    d.style.left = (colX(b.c0) - 26) + `px`;
    d.style.width = (colX(b.c1) - colX(b.c0) + NODEW + 52) + `px`;
    d.style.top = (ROWY.andrew - 32) + `px`;
    d.style.height = (ROWY.joel + NODEH + 26 - ROWY.andrew + 32) + `px`;
    d.innerHTML = `<b>${esc(b.t)}<em>${esc(b.q)}</em></b>`;
    carte.appendChild(d);
  });

  /* actes */
  ACTES.forEach(a => {
    const d = document.createElement(`div`);
    d.className = `acte`;
    d.style.left = (colX(a.c0) - 34) + `px`;
    d.innerHTML = `<i>${esc(a.t)}</i>`;
    carte.appendChild(d);
  });

  /* étiquettes de voie */
  const voies = $(`#voies`);
  voies.innerHTML = ``;
  Object.entries(VOIES).forEach(([k, v]) => {
    const d = document.createElement(`div`);
    d.className = `voie-nom voie-${k}`;
    d.style.top = (ROWY[k] + 8) + `px`;
    d.innerHTML = `<b>${esc(v.nom)}</b><i>${esc(v.desc)}</i>`;
    voies.appendChild(d);
  });

  /* les étapes du tronc */
  if (filtreVoie === `tous` || filtreVoie === `commun`) ETAPES.forEach(e => {
    const d = document.createElement(`div`);
    d.className = `etape`;
    d.style.left = colX(e.c0) + `px`;
    d.style.top = ROWY.commun + `px`;
    d.style.width = (colX(e.c1) - colX(e.c0) + NODEW) + `px`;
    d.innerHTML = `<i>ÉTAPE</i><b>${esc(e.t)}</b>`;
    carte.appendChild(d);
  });

  /* nœuds */
  const visibles = new Set(scenesVisibles.map(s => s.id));
  scenesVisibles.forEach((s, i) => {
    const b = document.createElement(`button`);
    b.className = `noeud n-${s.row}` + (s.statut === `trou` ? ` trou` : ``)
                + (s.pivot ? ` pivot` : ``) + (s.gris ? ` gris` : ``);
    b.style.left = colX(s.col) + `px`;
    b.style.top = ROWY[s.row] + `px`;
    b.style.height = (s.gris ? NODEH - 26 : NODEH) + `px`;
    if (s.gris) b.style.top = (ROWY[s.row] + 13) + `px`;
    b.style.animationDelay = Math.min(i * 26, 900) + `ms`;
    b.dataset.id = s.id;
    b.innerHTML =
      `<span class="bandeau"></span>` +
      `<span class="no">${esc(s.no)}</span>` +
      `<h3>${esc(s.titre)}</h3>` +
      `<p>${nu(s.resume)}</p>` +
      `<div class="marques">` +
        (s.statut !== `acquis` ? `<span class="cle">${esc(ST[s.statut] || s.statut)}</span>` : ``) +
        (s.flottant ? `<span class="cle" style="color:var(--texte-4)">placement à trancher</span>` : ``) +
      `</div>`;
    b.addEventListener(`click`, () => ouvrirTiroir(s.id));
    carte.appendChild(b);
  });

  /* liens */
  const sv = $(`#liens`);
  sv.setAttribute(`viewBox`, `0 0 ${larg} ${HAUT}`);
  sv.setAttribute(`width`, larg); sv.setAttribute(`height`, HAUT);
  const parId = Object.fromEntries(SCENES.map(s => [s.id, s]));
  let p = ``;
  LIENS.forEach(([a, z, cls], i) => {
    const A = parId[a], Z = parId[z];
    if (!A || !Z || !visibles.has(a) || !visibles.has(z)) return;
    const x1 = colX(A.col) + NODEW, y1 = ROWY[A.row] + NODEH / 2;
    const x2 = colX(Z.col),          y2 = ROWY[Z.row] + NODEH / 2;
    const teinte = cls === `a` ? `var(--andrew)` : cls === `j` ? `var(--joel)` : `var(--commun)`;
    p += `<path class="${cls ? `l-` + (cls === `a` ? `andrew` : `joel`) : ``}" d="${trace(x1, y1, x2, y2)}" `
       + `stroke-dasharray="1400" stroke-dashoffset="1400" style="animation-delay:${Math.min(i * 30, 900)}ms"/>`;
    /* pointe de direction */
    p += `<polygon points="${x2 - 9},${y2 - 5} ${x2},${y2} ${x2 - 9},${y2 + 5}" fill="${teinte}"/>`;
  });
  sv.innerHTML = p;

  carte.classList.remove(`anim`); void carte.offsetWidth; carte.classList.add(`anim`);
}

function trace(x1, y1, x2, y2){
  if (Math.abs(y1 - y2) < 2) return `M ${x1} ${y1} H ${x2}`;
  const m = x1 + (x2 - x1) / 2, r = 11, s = y2 > y1 ? 1 : -1;
  return `M ${x1} ${y1} H ${m - r} Q ${m} ${y1} ${m} ${y1 + r * s} V ${y2 - r * s} Q ${m} ${y2} ${m + r} ${y2} H ${x2}`;
}

/* ---------- le tiroir ---------- */
const parIdScene = Object.fromEntries(SCENES.map(s => [s.id, s]));
const parIdGens  = Object.fromEntries(GENS.map(g => [g.id, g]));

function ouvrirTiroir(id){
  const s = parIdScene[id]; if (!s) return;
  idSel = id;
  $$(`.noeud`).forEach(n => n.classList.toggle(`sel`, n.dataset.id === id));
  $(`#t-no`).textContent = s.no + `  ·  ` + s.acte;
  $(`#t-titre`).textContent = s.titre;
  $(`#t-meta`).innerHTML =
    `<span class="st st-${s.statut}">${esc(ST[s.statut] || s.statut)}</span>` +
    `<span class="etiq">${esc(VOIES[s.row].nom)}</span>` +
    (s.flottant ? `<span class="etiq" style="color:var(--provisoire)">placement à trancher</span>` : ``);

  let h = ``;
  h += bloc(`Ce qui s'y passe`, `<p>${rich(s.resume)}</p>`);
  if (s.produit) h += bloc(`Ce que la scène doit produire`, `<p>${rich(s.produit)}</p>`);
  if (s.clef)    h += bloc(`Le point de la scène`, `<div class="dit">${rich(s.clef)}</div>`);
  if (s.clefFin) h += bloc(`Ce qui la referme`, `<div class="dit">${rich(s.clefFin)}</div>`);
  if (s.lecture) h += bloc(`Ce que le lecteur en fait`, `<div class="dit">${rich(s.lecture)}</div>`);
  if (s.monde)   h += bloc(`Ce qu'elle apprend du monde`, `<p>${rich(s.monde)}</p>`);
  if (s.garde_forme) h += bloc(`Comment ça se donne`, `<div class="dit">${rich(s.garde_forme)}</div>`);
  if (s.garde_bis)   h += bloc(`Ce qu'il faut savoir sans l'écrire`, `<div class="dit">${rich(s.garde_bis)}</div>`);
  if (s.double)  h += bloc(`Beat doublable`, `<p>${rich(s.double)}</p>`);
  if (s.pourquoi && s.pourquoi.length)
    h += bloc(`Pourquoi là`, `<ul>` + s.pourquoi.map(x => `<li>${rich(x)}</li>`).join(``) + `</ul>`);
  if (s.contre)
    h += bloc(`L'autre option`, `<div class="garde"><b>ce qu'elle coûterait</b>${rich(s.contre)}</div>`);

  if (s.face && parIdScene[s.face]){
    const o = parIdScene[s.face];
    h += bloc(`En face — ce qui se passe de l'autre côté`,
      `<div class="face f-${o.row}">
         <span class="etiq">${esc(VOIES[o.row].nom)}${o.gris ? ` · repère, ne s'écrira pas` : ``}</span>
         <h5>${esc(o.titre)}</h5>
         <p>${rich(o.resume)}</p>
         <button class="renvoi" data-face="${esc(o.id)}">ouvrir son dossier →</button>
       </div>
       <p class="prio"><strong>La branche d'Andrew est prioritaire.</strong> On écrit la scène pour qu'elle se lise
        d'abord comme celle de ce monde-ci ; l'autre lecture doit seulement rester <em>possible</em>, jamais servie.
        <br>Trois questions à se poser : <em>est-ce qu'un mot d'ici manque là-bas ? est-ce qu'un mot de là-bas
        n'existe pas ici ? est-ce que ce qui vient d'arriver tient dans les deux calendriers ?</em></p>`);
  }
  if (s.qui && s.qui.length){
    h += bloc(`Qui est là`, s.qui.map(q => {
      const g = parIdGens[q];
      return `<button class="renvoi" data-gens="${esc(q)}">${esc(g ? g.nom : q)}</button>`;
    }).join(``));
  }
  if (s.phrases && s.phrases.length){
    h += bloc(`Phrases à placer`, s.phrases.map(f =>
      `<div class="dit parle">« ${esc(f.t)} »<cite>${rich(f.n)}</cite></div>`).join(``));
  }
  if (s.gardes && s.gardes.length){
    h += bloc(`Ce qu'il faut tenir`, `<div class="garde"><b>à surveiller à l'écriture</b><ul>` +
      s.gardes.map(g => `<li>${rich(g)}</li>`).join(``) + `</ul></div>`);
  }
  if (s.refs && s.refs.length){
    h += bloc(`Références`, s.refs.map(r =>
      `<div class="paie"><span class="q">modèle</span><div><strong>${esc(r.t)}</strong><br>${rich(r.d)}</div></div>`).join(``) +
      (s.refNote ? `<p style="margin-top:12px">${rich(s.refNote)}</p>` : ``));
  }
  if (s.ouvert && s.ouvert.length){
    h += bloc(`Reste à trancher`, `<ul>` + s.ouvert.map(o => `<li>${rich(o)}</li>`).join(``) + `</ul>`);
  }
  h += bloc(`Source`, `<p style="font-family:var(--mono);font-size:11.5px;color:var(--texte-4)">${esc(s.src)}</p>`);

  $(`#t-corps`).innerHTML = h;
  $(`#t-corps`).scrollTop = 0;
  $$(`#t-corps [data-face]`).forEach(b => b.addEventListener(`click`, () => {
    const n = $(`.noeud[data-id="${b.dataset.face}"]`);
    if (n) $(`#plateau`).scrollTo({ left: Math.max(0, n.offsetLeft - 300), behavior: `smooth` });
    ouvrirTiroir(b.dataset.face);
  }));
  $$(`#t-corps [data-gens]`).forEach(b => b.addEventListener(`click`, () => {
    $(`.rail-btn[data-vue="gens"]`).click();
    const c = document.getElementById(`g-` + b.dataset.gens);
    if (c) { c.scrollIntoView({ behavior:`smooth`, block:`center` }); c.style.borderColor = `var(--andrew)`;
             setTimeout(() => c.style.borderColor = ``, 1800); }
  }));

  const i = scenesVisibles.findIndex(x => x.id === id);
  $(`#t-pos`).textContent = (i + 1) + ` / ` + scenesVisibles.length;
  $(`#tiroir`).classList.add(`on`);
  $(`#tiroir`).setAttribute(`aria-hidden`, `false`);
}
function bloc(t, c){ return `<section class="bloc"><h4>${esc(t)}</h4>${c}</section>`; }

function fermerTiroir(){
  $(`#tiroir`).classList.remove(`on`);
  $(`#tiroir`).setAttribute(`aria-hidden`, `true`);
  $$(`.noeud`).forEach(n => n.classList.remove(`sel`));
  idSel = null;
}
function bouger(pas){
  if (!idSel) return;
  const i = scenesVisibles.findIndex(x => x.id === idSel);
  const j = i + pas;
  if (j < 0 || j >= scenesVisibles.length) return;
  const s = scenesVisibles[j];
  ouvrirTiroir(s.id);
  const n = $(`.noeud[data-id="${s.id}"]`);
  if (n) $(`#plateau`).scrollTo({ left: Math.max(0, n.offsetLeft - 260), behavior: `smooth` });
}
$(`#t-fermer`).addEventListener(`click`, fermerTiroir);
$(`#t-prec`).addEventListener(`click`, () => bouger(-1));
$(`#t-suiv`).addEventListener(`click`, () => bouger(1));
document.addEventListener(`keydown`, e => {
  if (e.target.matches(`input,textarea`)) return;
  if (e.key === `Escape`) fermerTiroir();
  if (!$(`#v-parcours`).classList.contains(`on`)) return;
  if (e.key === `ArrowRight`) { bouger(1); }
  if (e.key === `ArrowLeft`)  { bouger(-1); }
});

construirePlateau();

/* la molette fait défiler vers la droite */
$(`#plateau`).addEventListener(`wheel`, e => {
  const p = $(`#plateau`);
  if (e.ctrlKey || p.scrollWidth <= p.clientWidth + 2) return;
  const k = e.deltaMode === 1 ? 26 : e.deltaMode === 2 ? p.clientWidth : 1;
  const d = (Math.abs(e.deltaY) >= Math.abs(e.deltaX) ? e.deltaY : e.deltaX) * k;
  if (!d) return;
  p.scrollLeft += d;
  e.preventDefault();
}, { passive: false });

let _redim;
addEventListener(`resize`, () => {
  clearTimeout(_redim);
  _redim = setTimeout(() => { construirePlateau(); if (idSel) ouvrirTiroir(idSel); }, 180);
});

/* ==========================================================================
   VUE 2 — LE CHAPITRAGE
   ========================================================================== */
const CLEF_CH = `eclaircie-chapitres-v1`;
let plan = JSON.parse(memo.lire(CLEF_CH) || `null`) || { ch: [{ t: `Chapitre 1`, s: [] }] };
function sauverPlan(){ memo.ecrire(CLEF_CH, JSON.stringify(plan)); }

function jeton(s, dansChapitre){
  const b = document.createElement(`div`);
  b.className = `jeton j-${s.row}`;
  b.draggable = true;
  b.dataset.id = s.id;
  b.innerHTML = `<span class="n">${esc(s.no)}</span><span class="t">${esc(s.titre)}</span>`;
  b.addEventListener(`dragstart`, e => {
    e.dataTransfer.setData(`text/plain`, s.id);
    e.dataTransfer.effectAllowed = `move`;
    b.classList.add(`glisse`);
  });
  b.addEventListener(`dragend`, () => b.classList.remove(`glisse`));
  b.title = dansChapitre
    ? `glisser vers un autre chapitre · cliquer pour remettre en réserve`
    : `glisser dans un chapitre · cliquer pour l'ajouter au dernier`;
  b.addEventListener(`click`, () => {
    if (dansChapitre) retirer(s.id);
    else { retirer(s.id); plan.ch[plan.ch.length - 1].s.push(s.id); }
    sauverPlan(); rendreChapitrage();
  });
  return b;
}
function retirer(id){ plan.ch.forEach(c => { c.s = c.s.filter(x => x !== id); }); sauverPlan(); }

function rendreChapitrage(){
  const places = new Set(plan.ch.flatMap(c => c.s));
  const res = $(`#ch-reserve`); res.innerHTML = ``;
  const reste = SCENES.filter(s => !places.has(s.id));
  reste.forEach(s => res.appendChild(jeton(s, false)));
  $(`#ch-reste`).textContent = reste.length;
  if (!reste.length) res.innerHTML = `<div class="vide">tout est placé</div>`;

  const liste = $(`#ch-liste`); liste.innerHTML = ``;
  plan.ch.forEach((c, i) => {
    const d = document.createElement(`div`);
    d.className = `chapitre`;
    d.innerHTML = `<div class="ct"><span class="rang">${String(i + 1).padStart(2, `0`)}</span>` +
      `<input value="${esc(c.t)}" aria-label="Titre du chapitre"><button title="Supprimer">supprimer</button></div>` +
      `<div class="depot"></div>`;
    const inp = $(`input`, d);
    inp.addEventListener(`input`, () => { c.t = inp.value; sauverPlan(); });
    $(`button`, d).addEventListener(`click`, () => {
      plan.ch.splice(i, 1); if (!plan.ch.length) plan.ch = [{ t:`Chapitre 1`, s:[] }];
      sauverPlan(); rendreChapitrage();
    });
    const dep = $(`.depot`, d);
    c.s.forEach(id => { const s = parIdScene[id]; if (s) dep.appendChild(jeton(s, true)); });
    dep.addEventListener(`dragover`, e => { e.preventDefault(); d.classList.add(`survol`); });
    dep.addEventListener(`dragleave`, () => d.classList.remove(`survol`));
    dep.addEventListener(`drop`, e => {
      e.preventDefault(); d.classList.remove(`survol`);
      const id = e.dataTransfer.getData(`text/plain`);
      if (!id) return;
      retirer(id); c.s.push(id); sauverPlan(); rendreChapitrage();
    });
    liste.appendChild(d);
  });
}
$(`#ch-reserve`).addEventListener(`dragover`, e => e.preventDefault());
$(`#ch-reserve`).addEventListener(`drop`, e => {
  e.preventDefault();
  const id = e.dataTransfer.getData(`text/plain`);
  if (id) { retirer(id); rendreChapitrage(); }
});
$(`#ch-ajouter`).addEventListener(`click`, () => {
  plan.ch.push({ t: `Chapitre ` + (plan.ch.length + 1), s: [] }); sauverPlan(); rendreChapitrage();
});
$(`#ch-vider`).addEventListener(`click`, () => {
  plan.ch.forEach(c => c.s = []); sauverPlan(); rendreChapitrage();
});
$(`#ch-export`).addEventListener(`click`, () => {
  const txt = `L'ÉCLAIRCIE — plan de chapitres\n\n` + plan.ch.map((c, i) =>
    `${String(i + 1).padStart(2, `0`)}. ${c.t}\n` +
    (c.s.length ? c.s.map(id => { const s = parIdScene[id];
      return `    · ${s.no} — ${s.titre}  [${VOIES[s.row].nom}]`; }).join(`\n`) : `    (vide)`)
  ).join(`\n\n`);
  const b = new Blob([txt], { type: `text/plain;charset=utf-8` });
  const a = document.createElement(`a`);
  a.href = URL.createObjectURL(b); a.download = `eclaircie-plan-chapitres.txt`; a.click();
  URL.revokeObjectURL(a.href);
  souffler(`Plan exporté en fichier texte.`);
});
rendreChapitrage();

/* ==========================================================================
   VUE 3 — LES NOTES
   ========================================================================== */
let nTag = `tout`, nTexte = ``;
const TAGS = [...new Set(NOTES.flatMap(n => n.t))].sort();

(function filtresNotes(){
  const box = $(`#n-filtres`);
  const opts = [[`tout`, `tout`], ...TAGS.map(t => [t, t]),
                [`__ecarte`, `écarté`], [`__ouvert`, `ouvert`], [`__provisoire`, `provisoire`]];
  opts.forEach(([k, lab]) => {
    const b = document.createElement(`button`);
    b.className = `puce` + (k === `tout` ? ` on` : ``);
    const n = k === `tout` ? NOTES.length
            : k.startsWith(`__`) ? NOTES.filter(x => x.e === k.slice(2)).length
            : NOTES.filter(x => x.t.includes(k)).length;
    b.innerHTML = esc(lab) + `<span class="n">${n}</span>`;
    b.addEventListener(`click`, () => {
      nTag = k; $$(`#n-filtres .puce`).forEach(x => x.classList.remove(`on`)); b.classList.add(`on`);
      rendreNotes();
    });
    box.appendChild(b);
  });
})();
$(`#n-cherche`).addEventListener(`input`, e => { nTexte = e.target.value.toLowerCase().trim(); rendreNotes(); });

function rendreNotes(){
  const l = $(`#n-liste`);
  const sel = NOTES.filter(n => {
    if (nTag !== `tout`) {
      if (nTag.startsWith(`__`)) { if (n.e !== nTag.slice(2)) return false; }
      else if (!n.t.includes(nTag)) return false;
    }
    if (nTexte && !(n.v + ` ` + n.q + ` ` + n.s + ` ` + n.t.join(` `)).toLowerCase().includes(nTexte)) return false;
    return true;
  });
  l.innerHTML = sel.length ? sel.map(n =>
    `<article class="note n-${n.e === `ecarte` ? `ecarte` : n.e === `provisoire` ? `provisoire` : n.e === `acquis` ? `decision` : `elle`}">
      <div class="tete">
        <span class="jour">${esc(n.d)}</span>
        <span class="sujet">${esc(n.s)}</span>
        <span class="st st-${n.e}">${esc(ST[n.e] || n.e)}</span>
      </div>
      ${n.v && n.v !== `—` ? `<p class="verbatim">${esc(n.v)}</p>` : ``}
      <p class="quoi">${rich(n.q)}</p>
      <div class="bas">${n.t.map(t => `<span class="mot">${esc(t)}</span>`).join(``)}</div>
    </article>`).join(``)
    : `<div class="vide">rien ici</div>`;
}
rendreNotes();

/* ==========================================================================
   VUE 4 — LE MONDE
   ========================================================================== */
let mOnglet = `glossaire`, mTexte = ``;
const ONGLETS = [[`glossaire`,`Le glossaire`],[`bible`,`La bible`],[`regles`,`Les règles`],[`interdits`,`Les interdits`],
                 [`decompte`,`Le décompte`],[`calendrier`,`Le calendrier`],
                 [`dispositif`,`Le dispositif`],[`raccords`,`Les faux raccords`]];
(function ongletsMonde(){
  const box = $(`#m-onglets`);
  ONGLETS.forEach(([k, lab]) => {
    const b = document.createElement(`button`);
    b.className = `puce` + (k === `glossaire` ? ` on` : ``);
    b.textContent = lab;
    b.addEventListener(`click`, () => {
      mOnglet = k; $$(`#m-onglets .puce`).forEach(x => x.classList.remove(`on`)); b.classList.add(`on`);
      rendreMonde();
    });
    box.appendChild(b);
  });
})();
$(`#m-cherche`).addEventListener(`input`, e => { mTexte = e.target.value.toLowerCase().trim(); rendreMonde(); });

function rendreMonde(){
  const c = $(`#m-corps`);
  const f = t => !mTexte || t.toLowerCase().includes(mTexte);

  if (mOnglet === `glossaire`){
    const l = GLOSSAIRE.filter(([m, d, s, o]) => f(m + ` ` + d + ` ` + o));
    c.innerHTML = `<p class="chapo">Les mots propres à ce monde, et ceux du quotidien qui y prennent un autre sens. <strong>Aucun ne s'explique dans le texte : ils s'emploient.</strong><br>
      <em>Cette liste <strong>est</strong> la page de fin de volume du livre. La source est <code>02-univers/le-glossaire.md</code> ; <code>05-manuscrit/glossaire.md</code> en est généré. La ligne de source et la question ouverte, elles, ne vont jamais sous les yeux du lecteur.</em></p>`
      + `<p class="chapo" style="opacity:.7">${l.length} mot${l.length > 1 ? `s` : ``}${mTexte ? ` sur ${GLOSSAIRE.length}` : ``}.</p>`
      + `<dl class="lexique">` + l.map(([m, d, s, o]) =>
        `<div class="mot-l"><dt><b>${esc(m)}</b>${o ? `<br><span class="st st-ouvert">non tranché</span>` : ``}</dt>
         <dd>${rich(d)}${o ? `<span class="ouv">${rich(o)}</span>` : ``}
         <span class="src" style="margin-top:7px">${esc(s)}</span></dd></div>`).join(``) + `</dl>`;
  }

  else if (mOnglet === `bible`){
    const l = BIBLE.filter(([m, d, s, o]) => f(m + ` ` + d + ` ` + o));
    c.innerHTML = `<p class="chapo">Ce que l'autrice seule sait : les outils d'écriture, les mots morts, ce qui vendrait la fin du livre, et ce que tout le monde comprend déjà sans qu'on le lui explique. <strong>Rien de cette page ne va sous les yeux du lecteur.</strong><br>
      <em>La chaîne, le sismographe et la règle des retrouvailles sont ici pour cette raison, et pas parce qu'ils comptent moins.</em></p>`
      + `<p class="chapo" style="opacity:.7">${l.length} entrée${l.length > 1 ? `s` : ``}${mTexte ? ` sur ${BIBLE.length}` : ``}.</p>`
      + `<dl class="lexique">` + l.map(([m, d, s, o]) =>
        `<div class="mot-l"><dt><b>${esc(m)}</b>${o ? `<br><span class="st st-ouvert">non tranché</span>` : ``}</dt>
         <dd>${rich(d)}${o ? `<span class="ouv">${rich(o)}</span>` : ``}
         <span class="src" style="margin-top:7px">${esc(s)}</span></dd></div>`).join(``) + `</dl>`;
  }

  else if (mOnglet === `regles`){
    const l = REGLES.filter(([cat, t]) => f(cat + ` ` + t));
    const cats = [...new Set(l.map(r => r[0]))];
    c.innerHTML = `<p class="chapo">Ce que l'autrice doit connaître au chiffre près, pour que le monde soit solide. <strong>Le lecteur, lui, doit juste savoir qui envier.</strong></p>`
      + cats.map(cat => `<h2 class="titre-section">${esc(cat)} <span>${l.filter(r => r[0] === cat).length}</span></h2>`
        + l.filter(r => r[0] === cat).map(([, t, st]) =>
          `<div class="regle"><span class="cat"></span><span class="txt">${rich(t)}</span>
           <span class="st st-${st}">${esc(ST[st] || st)}</span></div>`).join(``)).join(``);
  }

  else if (mOnglet === `interdits`){
    const l = INTERDITS.filter(i => f(i.t + ` ` + i.p + ` ` + (i.e || ``)));
    c.innerHTML = `<p class="chapo">La liste de tout ce que <strong>le texte du roman</strong> ne doit jamais faire. La numérotation est stable : un interdit garde son numéro à vie.<br>
      <em>La bible d'autrice, elle, n'est soumise à aucun d'entre eux — les documents de travail peuvent tout dire, tout nommer, tout calculer.</em></p>`
      + `<div class="grille deux">` + l.map(i =>
        `<article class="interdit"><h3><span class="num">${i.n}</span>${esc(i.t)}</h3>
         ${i.c && i.c !== `—` ? `<p class="cite">${esc(i.c)}</p>` : ``}
         <p>${rich(i.p)}</p>
         ${i.e ? `<p class="ex"><b>ce qui est interdit</b><br>${rich(i.e)}</p>` : ``}
         ${i.bonus ? `<p class="ex" style="margin-top:10px;color:var(--acquis)"><b style="color:var(--acquis)">et sa contrepartie</b><br>${rich(i.bonus)}</p>` : ``}
        </article>`).join(``) + `</div>`;
  }

  else if (mOnglet === `decompte`){
    c.innerHTML = `<p class="chapo"><strong>Tout le monde revient à l'âge où il est parti.</strong> Tout le monde rejoint huit ans — en descendant si l'on arrive au-dessus, en grandissant si l'on arrive en dessous. Puis un plateau, dont la durée varie d'un dossier à l'autre. Puis on repart vers le bas, et on meurt à zéro.<br>
      <strong>La bande du bas est le jardin</strong>, et il ne commence pas au plateau : il prend toute la tranche de huit à zéro. Qui arrive en dessous de huit y entre le jour de son éclaircie et y passe sa vie entière.<br>
      <em>Le trait plein est ce qui est chiffré. Le pointillé est ce que le dossier refuse de chiffrer — et il refuse pour une raison : personne, dans ce monde, ne peut dater sa fin.</em></p>
      <div class="graphe-boite"><svg id="graphe" viewBox="0 0 900 470" preserveAspectRatio="xMidYMid meet"></svg></div>
      <h2 class="titre-section">Le piège <span>à ne jamais confondre</span></h2>
      <p class="chapo"><strong>Cinquante-quatre n'est pas un âge, c'est un nombre d'années vécues.</strong> L'âge rejoint huit, s'y immobilise le temps du plateau, puis repart jusqu'à zéro ; le temps vécu monte et ne s'arrête jamais. Personne n'a jamais cinquante-quatre ans dans ce monde : on les vit.<br><br>
      Et <strong>personne ne meurt à huit ans</strong> — quand on disparaît, le corps n'a plus d'âge du tout. Ne jamais écrire « il s'éteint à huit ans » : presque toutes les erreurs d'arithmétique du dossier viennent de là.</p>
      <h2 class="titre-section">Les vitesses <span>fixées à l'arrivée, jamais recalculées</span></h2>
      <div class="grille">
        <div class="fiche"><span class="sur">au-dessus de cinquante ans</span><p><strong>Une marche par an.</strong> On descend d'un an chaque année. Andrew descendra d'un an par an jusqu'au bout, y compris quand il en aura vingt.</p></div>
        <div class="fiche"><span class="sur">chez les jeunes arrivants</span><p><strong>Environ trois ans par marche.</strong> On vit trois ans pour perdre un an d'âge. C'est ce que le lecteur ratera s'il compte 1:1.</p></div>
        <div class="fiche"><span class="sur">en dessous de huit ans</span><p><strong>1:1.</strong> On grandit d'un an par an. La seule vitesse du système qui ne dépende pas du chiffre d'arrivée.</p></div>
        <div class="fiche"><span class="sur">entre huit et cinquante</span><p><strong>Non chiffrée</strong> — et le dossier refuse de la chiffrer. Aucune vitesse n'existe pour ces arrivées-là.</p></div>
      </div>`;
    dessinerCourbes();
  }

  else if (mOnglet === `calendrier`){
    const l = CALENDRIER.filter(([r, t]) => f(r + ` ` + t));
    c.innerHTML = `<p class="chapo"><strong>Aucun chapitre n'est jamais daté.</strong> Pas d'année, pas de mention de durée, pas de « six ans plus tard » écrit en toutes lettres. Ce tableau est pour l'autrice seule.</p>`
      + l.map(([r, t, st]) =>
        `<div class="regle"><span class="cat">${esc(r)}</span><span class="txt">${rich(t)}</span>
         <span class="st st-${st}">${esc(ST[st] || st)}</span></div>`).join(``);
  }

  else if (mOnglet === `dispositif`){
    const l = DISPOSITIF.filter(([t, d]) => f(t + ` ` + d));
    c.innerHTML = `<p class="chapo">Comment deux histoires se lisent comme une seule, et pourquoi ce n'est pas une tricherie : <strong>Andrew enquête comme l'enquêteur parce qu'il est l'enquêteur.</strong> Le lecteur a été trompé par une cohérence, pas par une omission.</p>`
      + `<div class="grille deux">` + l.map(([t, d]) =>
        `<article class="fiche"><h3>${esc(t)}</h3><p>${rich(d)}</p></article>`).join(``) + `</div>`;
  }

  else if (mOnglet === `raccords`){
    const l = RACCORDS.filter(r => f(r.join(` `)));
    c.innerHTML = `<p class="chapo"><strong>Ce qui diffère est du corps. Ce qui se ressemble est de la personne.</strong><br>
      Les indices qui trahissent qu'on suit deux hommes — invisibles à la première lecture, évidents à la seconde.</p>`
      + `<div class="grille deux">` + l.map(([t, j, a, ou, st]) =>
        `<article class="fiche"><div class="haut"><h3>${esc(t)}</h3><span class="st st-${st === `retenu` || st === `structurel` ? `acquis` : st === `écarté` ? `ecarte` : `ouvert`}">${esc(st)}</span></div>
         <div class="paie"><span class="q" style="color:var(--joel)">Joël</span><div>${rich(j)}</div></div>
         <div class="paie"><span class="q" style="color:var(--andrew)">Andrew</span><div>${rich(a)}</div></div>
         <div class="paie"><span class="q">où</span><div>${rich(ou)}</div></div></article>`).join(``) + `</div>`
      + `<h2 class="titre-section">Les règles d'usage <span>elles valent pour toutes les paires</span></h2>`
      + `<div class="fiche"><ul>` + RACCORDS_REGLES.map(r => `<li>${rich(r)}</li>`).join(``) + `</ul></div>`;
  }
}

function dessinerCourbes(){
  const g = document.getElementById(`graphe`); if (!g) return;
  const W = 960, H = 540, ML = 150, MR = 178, MT = 20, MB = 44;
  const px = v => ML + (v / 100) * (W - ML - MR);
  const py = v => H - MB - (v / 94) * (H - MT - MB);
  let s = ``;

  /* la bande du jardin */
  s += `<rect x="${ML}" y="${py(8)}" width="${W - ML - MR}" height="${py(0) - py(8)}"
         fill="var(--provisoire)" opacity=".05"/>`;
  /* quadrillage */
  for (let a = 0; a <= 90; a += 10)
    s += `<line class="gq" x1="${ML}" y1="${py(a)}" x2="${W - MR}" y2="${py(a)}" opacity=".4"/>
          <text x="${ML - 10}" y="${py(a) + 4}" text-anchor="end" fill="var(--texte-4)" font-size="10.5" font-family="var(--sans)">${a}</text>`;
  for (let t = 20; t <= 100; t += 20)
    s += `<line class="gq" x1="${px(t)}" y1="${MT}" x2="${px(t)}" y2="${py(0)}" opacity=".25"/>
          <text x="${px(t)}" y="${H - MB + 18}" text-anchor="middle" fill="var(--texte-4)" font-size="10.5" font-family="var(--sans)">${t}</text>`;
  s += `<line class="gaxe" x1="${ML}" y1="${py(0)}" x2="${W - MR}" y2="${py(0)}"/>
        <line class="gaxe" x1="${ML}" y1="${MT}" x2="${ML}" y2="${py(0)}"/>`;
  /* la ligne des huit ans, et la bande du jardin */
  s += `<line class="gpalier" x1="${ML}" y1="${py(8)}" x2="${W - MR + 40}" y2="${py(8)}"/>
        <text x="${W - MR + 46}" y="${py(8) + 4}" fill="var(--provisoire)" font-size="10" font-family="var(--sans)" letter-spacing=".1em">HUIT ANS</text>
        <text x="${W - MR + 46}" y="${(py(8) + py(0)) / 2 + 4}" fill="var(--provisoire)" font-size="10.5" font-family="var(--sans)" letter-spacing=".14em">LE JARDIN</text>
        <text x="${W - MR + 46}" y="${(py(8) + py(0)) / 2 + 19}" fill="var(--texte-4)" font-size="9.5" font-family="var(--sans)">de huit à zéro, tout entier</text>`;
  s += `<text x="${ML - 10}" y="${MT + 2}" text-anchor="end" fill="var(--texte-4)" font-size="9.5" font-family="var(--sans)" letter-spacing=".1em">ÂGE</text>
        <text x="${W - MR}" y="${H - MB + 34}" text-anchor="end" fill="var(--texte-4)" font-size="9.5" font-family="var(--sans)" letter-spacing=".1em">ANNÉES VÉCUES →</text>`;

  /* étiquettes rangées à gauche, sans se chevaucher */
  const tri = COURBES.map((c, i) => ({ c, i, y: py(c.arr) })).sort((a, b) => a.y - b.y);
  let dernier = -99;
  tri.forEach(o => { o.ly = Math.max(o.y, dernier + 15); dernier = o.ly; });

  COURBES.forEach((cb, idx) => {
    const d = cb.desc === null ? null : Math.abs(cb.desc);
    const y0 = cb.arr;
    let xEnd;
    if (d === null){
      xEnd = 28;
      s += `<path class="gc flou" stroke="${cb.c}" d="M ${px(0)} ${py(y0)} L ${px(xEnd)} ${py(8)}"/>`;
      s += `<text x="${px(12)}" y="${py((y0 + 8) / 2) - 7}" fill="var(--texte-4)" font-size="12" font-family="var(--sans)">?</text>`;
    } else {
      xEnd = d;
      s += `<path class="gc" stroke="${cb.c}" d="M ${px(0)} ${py(y0)} L ${px(xEnd)} ${py(8)}"/>`;
    }
    const plat = 15, fin = 13;
    s += `<path class="gc flou" stroke="${cb.c}" d="M ${px(xEnd)} ${py(8)} L ${px(xEnd + plat)} ${py(8)} L ${px(xEnd + plat + fin)} ${py(0)}"/>`;
    s += `<circle cx="${px(0)}" cy="${py(y0)}" r="3.4" fill="${cb.c}"/>`;
    /* étiquette + trait de rappel */
    const o = tri.find(t => t.i === idx);
    s += `<line x1="${ML - 46}" y1="${o.ly}" x2="${px(0) - 5}" y2="${py(y0)}" stroke="${cb.c}" stroke-width=".8" opacity=".4"/>`;
    s += `<text class="glab" x="${ML - 50}" y="${o.ly + 4}" text-anchor="end" fill="${cb.c}">${esc(cb.lab)}</text>`;
  });
  g.setAttribute(`viewBox`, `0 0 ${W} ${H}`);
  g.innerHTML = s;
}
rendreMonde();

/* ==========================================================================
   VUE 5 — LES GENS
   ========================================================================== */
let gFiltre = `tous`;
(function filtresGens(){
  const box = $(`#g-filtres`);
  [[`tous`,`tout le monde`],[`andrew`,`ce monde-ci`],[`joel`,`la vie d'avant`]].forEach(([k, lab]) => {
    const b = document.createElement(`button`);
    b.className = `puce` + (k === `tous` ? ` on` : ``);
    b.innerHTML = esc(lab) + `<span class="n">${k === `tous` ? GENS.length : GENS.filter(g => g.voie === k).length}</span>`;
    b.addEventListener(`click`, () => {
      gFiltre = k; $$(`#g-filtres .puce`).forEach(x => x.classList.remove(`on`)); b.classList.add(`on`);
      rendreGens();
    });
    box.appendChild(b);
  });
})();
function rendreGens(){
  const l = GENS.filter(g => gFiltre === `tous` || g.voie === gFiltre);
  $(`#g-liste`).innerHTML = l.map(g =>
    `<article class="fiche" id="g-${esc(g.id)}" style="border-left:2px solid var(--${g.voie === `joel` ? `joel` : `andrew`})">
      <span class="sur">${esc(g.role)}</span>
      <h3>${esc(g.nom)}</h3>
      <p style="font-family:var(--sans);font-size:12.5px;color:var(--texte-3)">${esc(g.age)}</p>
      <p>${rich(g.resume)}</p>
      ${g.cle ? `<div class="dit">${rich(g.cle)}</div>` : ``}
      ${g.portrait && g.portrait.length ? `<div class="rub">son portrait</div><ul>${g.portrait.map(t => `<li>${rich(t)}</li>`).join(``)}</ul>` : ``}
      ${g.traits && g.traits.length ? `<div class="rub">à l'écriture</div><ul>${g.traits.map(t => `<li>${rich(t)}</li>`).join(``)}</ul>` : ``}
      ${g.faille && g.faille !== `—` ? `<div class="rub">sa faille</div><p>${rich(g.faille)}</p>` : ``}
      ${g.arc && g.arc !== `—` ? `<div class="rub">son arc</div><p>${rich(g.arc)}</p>` : ``}
      ${g.gardes && g.gardes.length ? `<div class="garde" style="margin-top:12px"><b>ce qu'on ne fait jamais</b><ul>${g.gardes.map(t => `<li>${rich(t)}</li>`).join(``)}</ul></div>` : ``}
      ${g.phrases && g.phrases.length ? `<div class="rub">ses phrases</div>${g.phrases.map(p => `<div class="dit parle">« ${esc(p)} »</div>`).join(``)}` : ``}
      ${g.ouvert && g.ouvert.length ? `<div class="rub">reste à trancher</div><ul>${g.ouvert.map(t => `<li>${rich(t)}</li>`).join(``)}</ul>` : ``}
      <span class="src">${esc(g.src)}</span>
    </article>`).join(``);
}
rendreGens();

/* ==========================================================================
   VUE 6 — À TRANCHER
   ========================================================================== */
let qFiltre = `tout`;
(function filtresQ(){
  const box = $(`#q-filtres`);
  const gs = [...new Set(QUESTIONS.map(q => q.g))];
  [[`tout`,`tout`], ...gs.map(g => [g, g])].forEach(([k, lab]) => {
    const b = document.createElement(`button`);
    b.className = `puce` + (k === `tout` ? ` on` : ``);
    b.innerHTML = esc(lab) + `<span class="n">${k === `tout` ? QUESTIONS.length : QUESTIONS.filter(q => q.g === k).length}</span>`;
    b.addEventListener(`click`, () => {
      qFiltre = k; $$(`#q-filtres .puce`).forEach(x => x.classList.remove(`on`)); b.classList.add(`on`);
      rendreQ();
    });
    box.appendChild(b);
  });
})();
function rendreQ(){
  const l = QUESTIONS.filter(q => qFiltre === `tout` || q.g === qFiltre);
  const gs = [...new Set(l.map(q => q.g))];
  $(`#q-corps`).innerHTML =
    `<p class="chapo">Les trous, les contradictions et les décisions en attente. <strong>Les phrases à garder sont au bas de cette page.</strong></p>` +
    gs.map(g => `<h2 class="titre-section">${esc(g)} <span>${l.filter(q => q.g === g).length}</span></h2>
      <div class="grille deux">` + l.filter(q => q.g === g).map(q =>
        `<article class="fiche">
          <div class="haut"><h3>${esc(q.t)}</h3><span class="st st-${q.e}">${esc(ST[q.e] || q.e)}</span></div>
          <p>${rich(q.q)}</p>
          ${q.o && q.o.length ? `<ul>${q.o.map(o => `<li>${rich(o)}</li>`).join(``)}</ul>` : ``}
          ${q.n ? `<div class="garde" style="margin-top:10px"><b>à savoir avant de trancher</b>${rich(q.n)}</div>` : ``}
        </article>`).join(``) + `</div>`).join(``) +
    `<h2 class="titre-section">Les phrases à garder <span>${PHRASES.length}</span></h2>
     <p class="chapo"><strong>texte</strong> = à prononcer telle quelle dans le roman. <strong>bible</strong> = pour écrire les scènes, jamais pour être dite. <strong>doctrine</strong> = existe dans le livre, mais contestée et jamais confirmée.</p>
     <div class="grille deux">` + PHRASES.map(p =>
      `<article class="fiche">
        <div class="haut"><span class="sur">${esc(p.d)}</span><span class="st st-${p.u === `texte` ? `acquis` : p.u === `doctrine` ? `provisoire` : `ouvert`}">${esc(p.u)}</span></div>
        <div class="dit parle" style="margin-top:4px">« ${esc(p.t)} »</div>
        <p>${rich(p.q)}</p>
      </article>`).join(``) + `</div>`;
}
rendreQ();

/* ==========================================================================
   VUE — LES CHAPITRES ÉCRITS
   ========================================================================== */
let xSel = 0;
(function choixTextes(){
  const box = $(`#x-choix`);
  TEXTES.forEach((t, i) => {
    const b = document.createElement(`button`);
    b.className = `puce` + (i === 0 ? ` on` : ``);
    b.textContent = t.rang;
    b.addEventListener(`click`, () => {
      xSel = i; $$(`#x-choix .puce`).forEach(x => x.classList.remove(`on`)); b.classList.add(`on`);
      rendreTextes();
    });
    box.appendChild(b);
  });
})();

/* ---------- le mode revision ----------
   L'autrice corrige le texte ici meme. Ses changements tiennent dans le
   navigateur (localStorage) et ressortent en un fichier de couples
   avant/apres, que je rejoue sur pB-textes.js. Le texte d'origine n'est
   jamais ecrase : REVIS ne contient que l'ecart. */
const CLEF_REV = `eclaircie-revision-`;
let enRevision = false;

function lireRev(id){
  try { return JSON.parse(localStorage.getItem(CLEF_REV + id)) || []; }
  catch(e){ return []; }
}
function ecrireRev(id, r){
  try {
    if (r.length) localStorage.setItem(CLEF_REV + id, JSON.stringify(r));
    else localStorage.removeItem(CLEF_REV + id);
  } catch(e){ souffler(`Le navigateur refuse d'enregistrer — telecharge avant de fermer.`); }
}

/* Ce que contenteditable rend n'est pas toujours ce qu'on lui a donne :
   on ramene a l'italique et au gras du dossier, et rien d'autre. */
function propre(html){
  return html
    .replace(/<br\s*\/?>/gi, ` `)
    .replace(/<\/?(?:div|span|font|p)[^>]*>/gi, ``)
    .replace(/<b>/gi, `<strong>`).replace(/<\/b>/gi, `</strong>`)
    .replace(/<i>/gi, `<em>`).replace(/<\/i>/gi, `</em>`)
    .replace(/\u00a0/g, ` `)
    .replace(/\s+/g, ` `)
    .trim();
}

/* L'ordre d'affichage : les paragraphes d'origine, leurs corrections,
   les ajouts glisses derriere leur ancre. */
function paragraphes(t){
  const rev = lireRev(t.id);
  const chg = new Map(), otes = new Set(), neufs = new Map();
  rev.forEach(r => {
    if (r.etat === `modifie`) chg.set(r.i, r.apres);
    else if (r.etat === `ote`) otes.add(r.i);
    else if (r.etat === `neuf`) {
      if (!neufs.has(r.apresI)) neufs.set(r.apresI, []);
      neufs.get(r.apresI).push(r);
    }
  });
  const out = [];
  t.p.forEach(([k, s, f], i) => {
    out.push({ i, k, f, s: chg.has(i) ? chg.get(i) : s,
               touche: chg.has(i), ote: otes.has(i) });
    (neufs.get(i) || []).forEach(n => out.push({ i, rang: n.rang, k: n.k, s: n.apres, neuf: true }));
  });
  return out;
}

function corpsTexte(t){
  return paragraphes(t).map(o => {
    const cls = [o.k === `p` ? (o.f || ``) : o.k];
    if (enRevision){
      if (o.touche) cls.push(`touche`);
      if (o.ote) cls.push(`ote`);
      if (o.neuf) cls.push(`neuf`);
    }
    const rep = enRevision
      ? ` contenteditable="true" data-i="${o.i}"${o.neuf ? ` data-rang="${o.rang}"` : ``}`
      : ``;
    const g = enRevision
      ? `<span class="gouttiere" contenteditable="false">`
        + `<button data-act="ote" title="${o.ote ? `remettre` : `oter ce paragraphe`}">${o.ote ? `\u21ba` : `\u00d7`}</button>`
        + `<button data-act="neuf" title="ajouter un paragraphe dessous">+</button></span>`
      : ``;
    return `<p class="${cls.join(` `).trim()}"${rep}>${g}${o.s}</p>`;
  }).join(``);
}

function texteDuP(el){
  const c = el.cloneNode(true);
  const g = c.querySelector(`.gouttiere`);
  if (g) g.remove();
  return propre(c.innerHTML);
}

function barreRevision(t){
  const rev = lireRev(t.id);
  const m = rev.filter(r => r.etat === `modifie`).length;
  const o = rev.filter(r => r.etat === `ote`).length;
  const n = rev.filter(r => r.etat === `neuf`).length;
  const rien = !rev.length;
  return `<div class="barre-revision">
    <span class="compte">${rien ? `Aucun changement pour l'instant. Clique dans un paragraphe et corrige.`
      : `<b>${m}</b> corrig\u00e9${m > 1 ? `s` : ``} \u00b7 <b>${o}</b> \u00f4t\u00e9${o > 1 ? `s` : ``} \u00b7 <b>${n}</b> ajout\u00e9${n > 1 ? `s` : ``}`}</span>
    <button id="r-tel"${rien ? ` disabled style="opacity:.4"` : ``}>enregistrer pour Claude</button>
    <button id="r-copier"${rien ? ` disabled style="opacity:.4"` : ``}>copier les changements</button>
    <button id="r-vider" class="efface"${rien ? ` disabled style="opacity:.4"` : ``}>tout annuler</button>
   </div>`;
}

function fichierRevision(t){
  return JSON.stringify({
    atelier: `revision de chapitre`,
    chapitre: t.id,
    titre: t.titre,
    changements: lireRev(t.id)
  }, null, 2);
}

function texteBrut(t){
  return t.rang.toUpperCase() + `\n` + t.titre + `\n\n` +
    paragraphes(t).filter(o => !o.ote).map(o => o.s.replace(/<[^>]+>/g, ``)).join(`\n\n`) + `\n`;
}
function rendreTextes(){
  const t = TEXTES[xSel]; if (!t) return;
  const sc = parIdScene[t.scene];
  $(`#x-corps`).innerHTML =
    `<article class="page">
      <span class="rang">${esc(t.rang)}</span>
      <h2>${esc(t.titre)}</h2>
      <p class="dedic">${esc(t.sous)}</p>
      <div class="txt${enRevision ? ` revise` : ``}">` + corpsTexte(t) +
      `</div>${enRevision ? barreRevision(t) : ``}</article>
     <aside class="appareil">
      <div class="actes">
        <button id="x-reviser">${enRevision ? `fermer la révision` : `réviser le texte`}</button>
        <button id="x-copier">copier le texte</button>
        <button id="x-tel">télécharger .txt</button>
        ${sc ? `<button id="x-scene">voir la scène</button>` : ``}
      </div>
      <div class="bl"><h4>Ce que c'est</h4><p>${t.note || ``}</p></div>
      <div class="bl tenu"><h4>Ce que le texte tient</h4><ul>${(t.tenu || []).map(x => `<li>${x}</li>`).join(``)}</ul></div>
      <div class="bl ouvre"><h4>Ce qu'il laisse ouvert</h4><ul>${(t.ouvre || []).map(x => `<li>${x}</li>`).join(``)}</ul></div>
     </aside>`;

  $(`#x-reviser`).addEventListener(`click`, () => {
    enRevision = !enRevision;
    rendreTextes();
    souffler(enRevision
      ? `Corrige directement dans le texte. \u00c0 la fin : enregistrer pour Claude.`
      : `R\u00e9vision ferm\u00e9e. Tes changements sont gard\u00e9s.`);
  });

  if (enRevision){
    const zone = $(`#x-corps .txt`);

    /* Entree ne coupe pas un paragraphe : on en ajoute un par le bouton. */
    zone.addEventListener(`keydown`, e => { if (e.key === `Enter`) e.preventDefault(); });

    /* On ne retient que l'ecart : si le texte revient a l'original, la
       ligne de revision dispara\u00eet au lieu de rester \u00e0 tra\u00eener. */
    zone.addEventListener(`focusout`, e => {
      const p = e.target.closest(`p[contenteditable]`); if (!p) return;
      const i = +p.dataset.i, rang = p.dataset.rang, apres = texteDuP(p);
      const rev = lireRev(t.id);
      if (rang !== undefined){
        const l = rev.find(r => r.etat === `neuf` && r.rang === rang);
        if (l) { l.apres = apres; ecrireRev(t.id, rev); rendreTextes(); }
        return;
      }
      const avant = t.p[i][1];
      const j = rev.findIndex(r => r.etat === `modifie` && r.i === i);
      if (apres === propre(avant)){ if (j >= 0) rev.splice(j, 1); }
      else if (j >= 0) rev[j].apres = apres;
      else rev.push({ etat: `modifie`, i, k: t.p[i][0], avant, apres });
      ecrireRev(t.id, rev);
      rendreTextes();
    });

    zone.addEventListener(`click`, e => {
      const b = e.target.closest(`.gouttiere button`); if (!b) return;
      const p = b.closest(`p`), i = +p.dataset.i, rang = p.dataset.rang;
      const rev = lireRev(t.id);
      if (b.dataset.act === `ote`){
        if (rang !== undefined){
          const j = rev.findIndex(r => r.etat === `neuf` && r.rang === rang);
          if (j >= 0) rev.splice(j, 1);
        } else {
          const j = rev.findIndex(r => r.etat === `ote` && r.i === i);
          if (j >= 0) rev.splice(j, 1); else rev.push({ etat: `ote`, i, texte: t.p[i][1] });
        }
      } else {
        rev.push({ etat: `neuf`, apresI: i, rang: `n` + rev.length + `-` + i,
                   k: t.p[i][0], ancre: t.p[i][1], apres: `\u00e0 \u00e9crire\u2026` });
      }
      ecrireRev(t.id, rev);
      rendreTextes();
    });

    $(`#r-vider`).addEventListener(`click`, () => {
      if (!confirm(`On efface tous tes changements sur ce chapitre ?`)) return;
      ecrireRev(t.id, []); rendreTextes(); souffler(`Remis \u00e0 l'original.`);
    });
    $(`#r-tel`).addEventListener(`click`, () => {
      const b = new Blob([fichierRevision(t)], { type: `application/json;charset=utf-8` });
      const a = document.createElement(`a`);
      a.href = URL.createObjectURL(b);
      a.download = `eclaircie-revision-` + t.id + `.json`; a.click();
      URL.revokeObjectURL(a.href);
      souffler(`Fichier enregistr\u00e9. Dis-moi \u00ab j'ai r\u00e9vis\u00e9 \u00bb et je le reprends.`);
    });
    $(`#r-copier`).addEventListener(`click`, () => {
      if (!navigator.clipboard) { souffler(`Presse-papier indisponible \u2014 passe par l'enregistrement.`); return; }
      navigator.clipboard.writeText(fichierRevision(t))
        .then(() => souffler(`Changements copi\u00e9s. Colle-les dans la conversation.`))
        .catch(() => souffler(`Le navigateur a refus\u00e9 \u2014 passe par l'enregistrement.`));
    });
  }

  $(`#x-copier`).addEventListener(`click`, () => {
    if (!navigator.clipboard) { souffler(`Le presse-papier n'est pas disponible ici — passe par le téléchargement.`); return; }
    navigator.clipboard.writeText(texteBrut(t))
      .then(() => souffler(`Texte copié. Colle-le où tu veux.`))
      .catch(() => souffler(`Le navigateur a refusé le presse-papier — passe par le téléchargement.`));
  });
  $(`#x-tel`).addEventListener(`click`, () => {
    const b = new Blob([texteBrut(t)], { type: `text/plain;charset=utf-8` });
    const a = document.createElement(`a`);
    a.href = URL.createObjectURL(b); a.download = `eclaircie-` + t.id + `.txt`; a.click();
    URL.revokeObjectURL(a.href);
  });
  if (sc) $(`#x-scene`).addEventListener(`click`, () => {
    $(`.rail-btn[data-vue="parcours"]`).click();
    ouvrirTiroir(t.scene);
    const n = $(`.noeud[data-id="${t.scene}"]`);
    if (n) $(`#plateau`).scrollTo({ left: Math.max(0, n.offsetLeft - 260), behavior: `smooth` });
  });
}
rendreTextes();

/* ---------- premier souffle ---------- */
setTimeout(() => souffler(`Clique une scène pour ouvrir son dossier d'écriture.`), 900);
</script>
</body>
</html>
