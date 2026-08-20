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
| `extraire-le-chapitre.py <id>` ou `--tous` | **régénère le brouillon markdown de `05-manuscrit/chapitres/en-cours/` depuis le texte de l'atelier.** *À lancer après chaque correction — un brouillon qui diverge en silence est la panne déjà payée deux fois* |
| `pdf-recueil.py <sortie.html> <id…>` | **plusieurs chapitres à la suite, en une page imprimable.** *Chacun commence sur une page neuve ; aucun nombre de mots* |
| `node tirer-le-pdf.js <entree.html> <sortie.pdf>` | **tire le PDF avec une numérotation en pied.** ⚠️ *Chrome n'implémente pas les boîtes de marge CSS — une numérotation écrite en `@bottom-center` ne sort jamais. On passe par le protocole, qui accepte un gabarit de pied : un numéro centré, ni date, ni titre, ni adresse du fichier* |
| `verrouiller-les-textes.py` | **le verrou des textes validés.** `--verifier` (appelé par la fabrication), `--ouvrir <id>` pour une séance de correction demandée, `--poser` pour refermer |
| `reprendre-la-revision.py` | **rejoue sur `pB-textes.js` les corrections faites par l'autrice dans l'atelier.** Sans argument, il va chercher le dernier `eclaircie-revision-*.json` dans les téléchargements. `--voir` montre sans rien écrire |
| `../../integrer-le-plan.py` | ré-injecte le plan de la ruche dans `p3-style.html`, `p4-corps.html` et `pC-ruche.js` |
| `../../integrer-le-jardin.py` | ré-injecte le plan du jardin. **Il passe par une iframe** : aucune classe à renommer, isolation totale |

## Le mode révision — l'autrice corrige, je reprends

**Onglet Chapitres, bouton « réviser le texte ».** Chaque paragraphe devient modifiable sur
place ; une gouttière à gauche permet d'en ôter un ou d'en glisser un dessous.

**Ce qui est retenu n'est pas le texte : c'est l'écart.** Un couple *avant / après* par
paragraphe touché, gardé dans le `localStorage` du navigateur. *Si le texte revient à son
état d'origine, la ligne disparaît au lieu de traîner.*

**Le circuit :**

1. elle corrige, la page compte les changements en bas ;
2. **« enregistrer pour Claude »** dépose un `eclaircie-revision-<chapitre>.json` ;
3. `python reprendre-la-revision.py` le rejoue sur `pB-textes.js` ;
4. `sh fabriquer.sh`.

⚠️ **Chaque « avant » doit se retrouver une fois et une seule dans `pB-textes.js`, sinon le
script s'arrête.** *Une correction qui ne trouve pas son ancre est une correction qu'on
croirait passée.*

⛔ **Le `localStorage` n'est pas une sauvegarde.** Il tient au navigateur et au chemin du
fichier. *Tant que le `.json` n'est pas enregistré, les corrections ne vivent qu'à un endroit.*

## Deux pièges déjà payés

**Un commentaire HTML posé dans une feuille de style avale la règle qui suit.**
Les marqueurs d'injection du CSS sont donc des commentaires CSS. C'est ce qui
avait fait disparaître la couleur de la coulée.

**`pdf3.py` n'imprime rien.** Il écrit une page HTML. Passer directement un
chemin `.pdf` en sortie produit un fichier HTML déguisé en PDF.

**Un accent grave dans une note ferme le gabarit qui la contient.** Les notes sont écrites
dans des gabarits délimités par des accents graves : en poser un dans le texte coupe le
fichier en deux et l'écran reste blanc. `node --check` l'attrape — **encore faut-il lire ce
qu'il dit.** `fabriquer.sh` finit désormais par `FABRICATION OK` : *si cette ligne manque,
on ne commite pas.* Ne jamais faire passer la fabrication par `| tail` dans une chaîne `&&` :
le code de retour devient celui de `tail`, et l'erreur passe inaperçue.

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
