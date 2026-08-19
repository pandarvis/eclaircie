import { test } from 'node:test';
import assert from 'node:assert/strict';
import { assainir } from '../outils/assainir.mjs';

test('un paragraphe ordinaire ne bouge pas', () => {
  assert.equal(assainir('Deux capsules étaient venues.'), 'Deux capsules étaient venues.');
});

test('l italique du roman passe', () => {
  assert.equal(
    assainir("— <em>C'est toi qui porteras la corde.</em>"),
    "— <em>C'est toi qui porteras la corde.</em>",
  );
});

test('le gras passe', () => {
  assert.equal(assainir('<strong>net</strong>'), '<strong>net</strong>');
});

test('toute autre balise est echappee', () => {
  assert.equal(assainir('<script>vol()</script>'), '&lt;script&gt;vol()&lt;/script&gt;');
});

test('une esperluette est echappee', () => {
  assert.equal(assainir('Pierre & Paul'), 'Pierre &amp; Paul');
});

test('un chevron seul est echappe', () => {
  assert.equal(assainir('a < b'), 'a &lt; b');
});

test('une balise autorisee avec un attribut est echappee', () => {
  assert.equal(
    assainir('<em onclick="vol()">x</em>'),
    '&lt;em onclick="vol()"&gt;x&lt;/em&gt;',
  );
});
