/* Tire un PDF depuis une page HTML, avec une numerotation en pied.
 *
 *   node tirer-le-pdf.js <entree.html> <sortie.pdf>
 *
 * Pourquoi ce detour plutot que --print-to-pdf : Chrome n'implemente pas
 * les boites de marge de CSS (@bottom-center), donc une numerotation
 * ecrite en CSS ne sort jamais. Le protocole, lui, accepte un gabarit de
 * pied de page. On passe donc par lui, pour un numero centre et rien
 * d'autre -- ni date, ni titre, ni adresse du fichier.
 */
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const [entree, sortie] = process.argv.slice(2);
if (!entree || !sortie) {
  console.error('usage : node tirer-le-pdf.js <entree.html> <sortie.pdf>');
  process.exit(1);
}

const CHROMES = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
];
const chrome = CHROMES.find(p => fs.existsSync(p));
if (!chrome) { console.error('Chrome introuvable.'); process.exit(1); }

const PORT = 9333;
const profil = fs.mkdtempSync(path.join(os.tmpdir(), 'eclaircie-pdf-'));

const PIED = `<div style="width:100%;font-family:Georgia,'Times New Roman',serif;
  font-size:9px;color:#6a6f78;text-align:center;margin:0 26mm;">
  <span class="pageNumber"></span></div>`;

const dors = ms => new Promise(r => setTimeout(r, ms));

async function attendre(url, essais = 60) {
  for (let i = 0; i < essais; i++) {
    try { return await (await fetch(url)).json(); } catch (e) { await dors(150); }
  }
  throw new Error('Chrome ne repond pas sur le port ' + PORT);
}

(async () => {
  const proc = spawn(chrome, [
    '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
    '--remote-debugging-port=' + PORT, '--user-data-dir=' + profil, 'about:blank',
  ], { stdio: 'ignore' });

  try {
    const info = await attendre(`http://127.0.0.1:${PORT}/json/version`);
    const ws = new WebSocket(info.webSocketDebuggerUrl);
    await new Promise((ok, ko) => { ws.onopen = ok; ws.onerror = ko; });

    let n = 0;
    const attente = new Map();
    const evenements = new Map();
    ws.onmessage = e => {
      const m = JSON.parse(e.data);
      if (m.id && attente.has(m.id)) {
        const { ok, ko } = attente.get(m.id); attente.delete(m.id);
        m.error ? ko(new Error(m.error.message)) : ok(m.result);
      } else if (m.method && evenements.has(m.method)) {
        evenements.get(m.method)(); evenements.delete(m.method);
      }
    };
    const envoyer = (method, params, sessionId) => new Promise((ok, ko) => {
      const id = ++n;
      attente.set(id, { ok, ko });
      ws.send(JSON.stringify({ id, method, params: params || {}, sessionId }));
    });

    const { targetId } = await envoyer('Target.createTarget', { url: 'about:blank' });
    const { sessionId } = await envoyer('Target.attachToTarget', { targetId, flatten: true });

    await envoyer('Page.enable', {}, sessionId);
    const charge = new Promise(ok => evenements.set('Page.loadEventFired', ok));
    const url = 'file:///' + path.resolve(entree).replace(/\\/g, '/');
    await envoyer('Page.navigate', { url }, sessionId);
    await charge;
    await dors(400);                       /* le temps que la mise en page se pose */

    const { data } = await envoyer('Page.printToPDF', {
      paperWidth: 8.27, paperHeight: 11.69,        /* A4 */
      marginTop: 1.02, marginBottom: 0.87,         /* 26 mm et 22 mm */
      marginLeft: 1.02, marginRight: 1.02,
      printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: '<span></span>',
      footerTemplate: PIED,
    }, sessionId);

    fs.writeFileSync(sortie, Buffer.from(data, 'base64'));
    const ko = (fs.statSync(sortie).size / 1024).toFixed(0);
    console.log(`${sortie} \u2014 ${ko} ko`);
    ws.close();
  } finally {
    proc.kill();
    try { fs.rmSync(profil, { recursive: true, force: true }); } catch (e) {}
  }
})().catch(e => { console.error('PROBLEME : ' + e.message); process.exit(1); });
