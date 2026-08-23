# Où on en est

*Point d'étape au 24 août 2026, écrit dans la nuit. Ce fichier se réécrit à chaque
séance : il dit l'état du chantier, pas son histoire.*

---

## Le manuscrit

| # | Titre | Scène | Mots | État |
|---|---|---|---|---|
| — | Prologue — La cérémonie | `ouv` | 2 644 | 🔒 verrouillé |
| 1 | Une journée à la ruche | `capsule` | 3 765 | 🔒 verrouillé |
| 2 | L'aquarium | `s1` | 3 451 | ✅ validé, non verrouillé |
| 3 | La tournée | `s2` | 1 834 | ✅ validé, non verrouillé |
| 4 | **La maison** | `s3` | 1 098 | ⚠️ **premier jet, jamais relu par l'autrice** |
| 5 | **Le poste** | `s4` | 854 | ⚠️ **premier jet, jamais relu par l'autrice** |
| — | Épilogue | `jardin-fin` | 2 631 | 🔒 verrouillé |

**Les chapitres 4 et 5 ne sont pas dans `lecture.html`.** *C'est délibéré : la version
bêta est destinée à un lecteur extérieur, et deux premiers jets n'y ont pas leur place.*
**Ils s'y ajouteront d'un mot** — la liste `LISIBLES` en tête de `fabriquer-lecture.py`.

---

## Ce qui attend une décision

### 1. Les deux éléments de notre monde, au chapitre 5

**① *Ça ne nous rajeunit pas, tout ça.*** — Liam, en se relevant du bureau.
**② *J'en ai fait, moi, des bêtises.*** — Liam, sur sa propre jeunesse.

*Tous deux portent sur la direction du temps, qui est le seul fait qui sépare vraiment
les deux mondes. Aucun nom propre, aucun mot proscrit.* **Le raisonnement complet, et
pourquoi l'exemple de Rome est écarté, sont dans la fiche de la scène 4.**

### 2. Le remords de June a changé de nature

*Ma première version lui faisait dire qu'elle ne savait pas comment il allait.* ⛔ **C'était
faux : elle l'avait dit à Andrew la semaine précédente, longuement, assise sur les marches.**

✅ **Le remords écrit est donc : « Je vous l'ai dit, et je n'ai rien fait d'autre que vous
le dire. »** *Ce qui met Andrew dedans avec elle, et donne toujours son prétexte à la fugue.*

### 3. Deux enchaînements que j'ai décidés seul

- **Le chapitre 5 suit le 4 sans respiration.** *Andrew part de chez June et arrive au poste
  dans la foulée — c'est ce qui permet « Je viens à l'instant de chez elle ».*
- **L'employeur ne figure plus au procès-verbal**, seulement dans la bouche de Liam.
  ⚠️ *Côté vie d'avant, ça suppose qu'une des deux travaillait. Ce n'est pas établi.*

---

## Ce qui reste ouvert, par ordre d'urgence

1. ⚠️ ***pédiatre* est mort le 20 août et apparaît encore 81 fois dans 15 fichiers.**
   *Certaines occurrences sont légitimes — les interdits doivent le nommer pour l'interdire,
   les paroles de l'autrice sont une archive. Les autres non.* **Et le mot de remplacement
   n'existe toujours pas.**
2. **Les chapitres 2 et 3 ne sont pas verrouillés.** *Seuls le prologue, le chapitre 1 et
   l'épilogue le sont.*
3. **Les fiches de personnages de la version bêta** — June, Julie, Paul — *sont de moi et
   n'ont jamais été relues.*
4. **18 questions ouvertes au glossaire**, dont plusieurs tranchées en séance sans être
   reportées.
5. **Sans réponse depuis plusieurs jours :** le nom du corps médical du jardin ; le nom du
   rendez-vous de suivi ; la frontière entre chuchoteur et tuteur ; le nombre de travées.

---

## Les outils, et ce qu'ils refusent

*Tout passe par `06-visuels/atelier/sources/fabriquer.sh`, qui doit imprimer
**FABRICATION OK**. Ne jamais le filtrer par `grep` ou `tail` : le code de sortie du filtre
masque celui du script.*

| Outil | Ce qu'il fait |
|---|---|
| `valide.js` | refuse de fabriquer si un chapitre manque de `note`, `tenu` ou `ouvre`, ou s'il emploie un mot interdit |
| `verrouiller-les-textes.py` | `--verifier` · `--poser [id…]` · `--ouvrir <id>` |
| `relire.py` | correcteur mécanique : signale, ne corrige jamais |
| `citations.py` | vérifie que ce que les fiches citent existe encore dans le texte |
| `reprendre-la-revision.py` | reprend un fichier corrigé par l'autrice, réouvre et repose le verrou |

⚠️ **Le mot *peau* ne bloque plus la fabrication.** *Il est signalé seulement quand il
voisine une capsule, une paroi, un rabat, un coulant, une travée ou un fruit — correction
du 24 août : la règle du 19 visait les capsules pourries, jamais les corps.*
