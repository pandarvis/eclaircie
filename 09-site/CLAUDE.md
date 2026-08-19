# Le site de lecture — règles de travail

Lire d'abord `conception/2026-08-19-site-de-lecture.md`. Ce fichier n'en est que le rappel
opérationnel.

## Ce qui ne se négocie pas

**1. Le texte se lit même si tout le reste tombe.** JavaScript coupé, ambiance cassée,
navigateur ancien : on lit le roman. Toute fonctionnalité est une couche par-dessus du HTML
qui se suffit à lui-même.

**2. Rien des notes de l'autrice n'atteint le lecteur.** Les entrées de `TEXTES` contiennent
`sous`, `tenu`, `ouvre` et `note` : ce sont ses analyses d'écriture, elles expliquent le
montage du roman en clair. La moisson **liste ce qui traverse** (`id`, `rang`, `titre`, `p`)
au lieu d'exclure ce qui ne doit pas passer. Un champ nouveau ne franchit donc jamais la
frontière par accident.

**3. Le roman est bâti sur un tour, et le site le joue.** Les scènes d'Andrew se passent dans
la ruche, celles de Joël dans la vie d'avant, et le lecteur ne le sait pas. En première
lecture, aucune couleur de voie, aucun plan, aucune frise, aucun point de vue nommé.

**4. On ne touche à rien hors de `09-site/`.** Une seule exception, décidée avec l'autrice :
l'accroche du contrôle de contrat dans `06-visuels/atelier/sources/fabriquer.sh`.

## Les commandes

```bash
npm run moisson     # sources de l'atelier -> donnees/textes.json
npm run dev         # moisson puis serveur de developpement
npm run build       # moisson, construction, controle anti-fuite
npm test            # les tests des outils
```

## La pile

Astro 6.3, statique. Aucune dépendance de test : `node:test`, fourni par Node 22.
Le natif partout où le navigateur sait faire ; une librairie seulement là où il ne sait pas.
