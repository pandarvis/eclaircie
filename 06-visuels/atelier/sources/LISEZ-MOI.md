# Les sources de l'atelier

`atelier.html` fait sept cent mille caractères. On ne l'édite pas à la main :
on édite un des treize morceaux ci-dessous, puis on refabrique.

```bash
sh fabriquer.sh
```

## Les treize morceaux, dans l'ordre du fichier

| Morceau | Ce qu'il contient |
|---|---|
| `p1-style.html` · `p2-style.html` · `p3-style.html` | l'apparence — le dernier porte aussi le style du plan de la ruche |
| `p4-corps.html` | le squelette : les onglets, les zones vides que le script remplit |
| `p5-scenes.js` | la frise — les scènes, les actes, les liens, les étapes |
| `p6-notes.js` | les notes datées : une décision, ce qu'a dit l'autrice, ce que ça change |
| `p7-monde.js` | le lexique, les règles, les interdits |
| `p8-gens.js` | les personnages et les phrases gardées |
| `p9-trancher.js` | les questions ouvertes et les arbitrages |
| `pB-textes.js` | **les textes du livre** — prologue, chapitres, épilogue |
| `pC-ruche.js` | le plan de la ruche, injecté depuis `../../plan-de-la-ruche.html` |
| `pD-jardin.js` | le plan du jardin, mis en iframe depuis `../../plan-du-jardin.html` |
| `pA-app.js` | l'application : rendu, navigation, recherche. **Toujours en dernier.** |

`pA-app.js` passe après `pC-ruche.js` dans le fichier final alors qu'il est
nommé avant : c'est voulu, l'application doit démarrer quand tout est déjà là.

## Les outils

| Script | À quoi il sert |
|---|---|
| `verser.py <fichier.md> <id-du-chapitre>` | verse un brouillon markdown dans `pB-textes.js` |
| `pdf3.py <id> <rang> <sous-titre> <sortie.html>` | fabrique la page A4 d'un chapitre ; **le PDF se tire ensuite avec Chrome `--print-to-pdf`, cette page n'est pas le PDF** |
| `grille.py` | vide la frise dans un tableau lisible, pour vérifier l'ordre des colonnes |
| `../../integrer-le-plan.py` | ré-injecte le plan de la ruche dans `p3-style.html`, `p4-corps.html` et `pC-ruche.js` |
| `../../integrer-le-jardin.py` | ré-injecte le plan du jardin. **Il passe par une iframe** : aucune classe à renommer, isolation totale |

## Deux pièges déjà payés

**Un commentaire HTML posé dans une feuille de style avale la règle qui suit.**
Les marqueurs d'injection du CSS sont donc des commentaires CSS. C'est ce qui
avait fait disparaître la couleur de la coulée.

**`pdf3.py` n'imprime rien.** Il écrit une page HTML. Passer directement un
chemin `.pdf` en sortie produit un fichier HTML déguisé en PDF.

**Un heredoc de shell avale les antislashs d'une expression régulière.** Un motif
`(...)` écrit dans un `python << EOF` arrive comme `` simple, c'est-à-dire un
caractère d'effacement, et le motif ne trouve plus rien — **sans erreur, en annonçant
zéro résultat.** C'est ainsi qu'un contrôle a certifié « aucun mot banni » sur un texte
qui en contenait trois. *Tout script qui contient un antislash s'écrit dans un fichier.*

## Les outils d'écriture

| Script | À quoi il sert |
|---|---|
| `analyse-style.py` | mesure les textes de l'atelier : temps, longueurs, répétitions, ambiguïtés |
| `controler-un-texte.py <fichier.md>` | passe un brouillon au même contrôle : mots bannis et mesures de style |
| `glossaire.py` | verse `05-manuscrit/glossaire.md` dans l'atelier |
| `paroles.py` | régénère `01-dossier/paroles-de-l-autrice.md` depuis la transcription |
