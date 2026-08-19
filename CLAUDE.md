# Comment on travaille dans ce dépôt

Ce dépôt porte un roman en cours d'écriture, *L'Éclaircie*, et les outils qui servent à
l'écrire. Deux personnes y travaillent, chacune avec sa propre session, et les sessions ne
se parlent pas. Ce fichier est ce qu'elles ont en commun.

## La règle qui prime sur toutes les autres

**On valide avec l'autrice avant d'intégrer.** Aucune proposition n'entre dans `develop`
sans son accord, et rien ne touche à la frise narrative sans qu'elle l'ait dit.

## La source de vérité

`06-visuels/atelier/atelier.html` est la source de vérité du projet. Les fichiers Markdown
sont les développements : en cas de désaccord, l'atelier a raison.

**On n'édite jamais `atelier.html` à la main.** On modifie un morceau dans
`06-visuels/atelier/sources/`, puis :

```bash
cd 06-visuels/atelier/sources && sh fabriquer.sh
```

## Les branches

Gitflow, décrit en détail dans `CONTRIBUER.md`. `main` ne reçoit que des états publiés,
`develop` le travail en cours, et tout passe par une branche `feature/` partie de `develop`.
On ne commite jamais directement sur `main`.

**Une branche ne se fusionne pas si `fabriquer.sh` ne passe pas.**

## La frontière

Le dossier `09-site/` contient le site de lecture publié sur Vercel. Il est tenu à part.

- **La session d'écriture ne descend jamais dans `09-site/`.** Rien de ce qui s'y trouve
  n'a besoin d'être modifié pour écrire le roman.
- **La session du site ne touche jamais au manuscrit** — ni `05-manuscrit/`, ni
  `06-visuels/atelier/sources/`, ni aucun des dossiers numérotés `01-` à `08-`. Elle les lit,
  elle ne les écrit pas.

Cette frontière existe parce que le site *lit* les données de l'atelier. Il en dépend, et il
ne doit jamais devenir une raison de modifier le travail d'écriture.

## Le contrat de données

Le site lit `TEXTES` dans `pB-textes.js` et `SCENES` dans `p5-scenes.js`.

**Le contenu est libre — c'est le texte de l'autrice.** Ce qui est sous contrat, c'est la
*forme* : le nom des champs, la structure des paragraphes `[balise, texte]`, l'existence des
identifiants de scène.

`fabriquer.sh` vérifie ce contrat à chaque fabrication. S'il échoue, le message dit quoi
réparer. Ne pas contourner le contrôle : le corriger, ou prévenir la session du site.
