import { test } from 'node:test';
import assert from 'node:assert/strict';
import { verifierLeContrat, pourLeLecteur } from '../outils/contrat.mjs';

const scenes = [{ id: 'ouv' }, { id: 'capsule' }];
const texteValide = {
  id: 'prologue', rang: 'Prologue', titre: 'La cérémonie', scene: 'ouv',
  sous: "point de vue d'Andrew",
  p: [['p', 'Deux capsules.'], ['tiret', '— On est deux.'], ['pause', '· · ·']],
  tenu: ['note interne'], ouvre: ['chantier'], note: 'ecrit avec l autrice',
};

test('des donnees conformes ne remontent aucun probleme', () => {
  assert.deepEqual(verifierLeContrat({ TEXTES: [texteValide], SCENES: scenes }), []);
});

test('un champ manquant est signale avec le nom du texte', () => {
  const { titre, ...sansTitre } = texteValide;
  const pb = verifierLeContrat({ TEXTES: [sansTitre], SCENES: scenes });
  assert.equal(pb.length, 1);
  assert.match(pb[0], /prologue/);
  assert.match(pb[0], /titre/);
});

test('une scene inconnue est signalee', () => {
  const pb = verifierLeContrat({ TEXTES: [{ ...texteValide, scene: 'nulle-part' }], SCENES: scenes });
  assert.equal(pb.length, 1);
  assert.match(pb[0], /nulle-part/);
});

test('un identifiant en double est signale', () => {
  const pb = verifierLeContrat({ TEXTES: [texteValide, texteValide], SCENES: scenes });
  assert.ok(pb.some((m) => /double/.test(m)));
});

test('une balise inconnue du site est signalee', () => {
  const casse = { ...texteValide, p: [['citation', 'un mot']] };
  const pb = verifierLeContrat({ TEXTES: [casse], SCENES: scenes });
  assert.equal(pb.length, 1);
  assert.match(pb[0], /citation/);
});

test('un bloc mal forme est signale', () => {
  const casse = { ...texteValide, p: [['p']] };
  const pb = verifierLeContrat({ TEXTES: [casse], SCENES: scenes });
  assert.equal(pb.length, 1);
  assert.match(pb[0], /balise, texte/);
});

test('TEXTES disparu est signale sans planter', () => {
  const pb = verifierLeContrat({ SCENES: scenes });
  assert.equal(pb.length, 1);
  assert.match(pb[0], /TEXTES/);
});

test('seuls quatre champs traversent jusqu au lecteur', () => {
  const [sorti] = pourLeLecteur([texteValide]);
  assert.deepEqual(Object.keys(sorti).sort(), ['id', 'p', 'rang', 'titre']);
});

test('un champ nouveau ne traverse pas tout seul', () => {
  const avecNouveau = { ...texteValide, confidence: "ce qui ne doit pas sortir" };
  const [sorti] = pourLeLecteur([avecNouveau]);
  assert.equal(sorti.confidence, undefined);
});
