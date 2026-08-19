# -*- coding: utf-8 -*-
"""Mesure le style des chapitres ecrits. Ne juge rien : compte.

usage : python analyse-style.py > ../../../99-archives/mesures-style.txt
"""
import io
import re
import sys
import collections

if sys.version_info[0] < 3:
    reload(sys)                      # noqa
    sys.setdefaultencoding('utf-8')  # noqa

SRC = 'pB-textes.js'
s = io.open(SRC, encoding='utf-8').read()


def chapitres():
    """Rend [(id, titre, [blocs])] dans l'ordre du fichier."""
    out = []
    for m in re.finditer(r'id: `([^`]+)`', s):
        ident = m.group(1)
        d = s.find('  p: [', m.end())
        if d < 0:
            continue
        f = s.index('\n  ],', d)
        corps = s[d:f]
        blocs = []
        for b in re.finditer(r'\[`(p|tiret|pause)`,`(.*?)`(?:,`[^`]*`)?\],', corps, re.S):
            if b.group(1) != 'pause':
                blocs.append((b.group(1), b.group(2)))
        t = re.search(r'titre: `([^`]*)`', s[m.end():m.end() + 400])
        out.append((ident, t.group(1) if t else '', blocs))
    return out


def phrases(texte):
    """Decoupe en phrases. Protege les abreviations et les points de suspension."""
    t = texte.replace('…', '…')
    t = re.sub(r'([.!?])(\s+["«—A-ZÀ-Ü])', r'\1\2', t)
    return [x.strip().replace('', '') for x in t.split('') if x.strip()]


MOTS = re.compile(r"[\wÀ-ſ']+", re.U)

# Marqueurs de temps. On ne fait pas de morphologie : on compte des formes
# frequentes et caracteristiques, ce qui suffit a voir une dominante.
IMPARFAIT = re.compile(r'\b\w{2,}(ait|aient|ais|iez|ions)\b', re.U)
PASSE_SIMPLE = re.compile(r'\b\w{2,}(èrent|irent|urent|îrent)\b|'
                          r'\b(fut|furent|eut|eurent|dit|firent|vint|vinrent|prit|prirent|'
                          r'mit|mirent|sortit|entra|regarda|posa|tourna|leva|passa|resta|'
                          r'ouvrit|repartit|descendit|monta|reprit|se souvint|souvint)\b', re.U)
PLUS_QUE_PARFAIT = re.compile(r"\b(avait|était|avaient|étaient)\s+\w+[és]\b", re.U)
PRESENT_VERITE = re.compile(r'\bon (ne )?(fait|dit|sait|voit|met|prend|laisse|compte|'
                            r'appelle|garde|donne|entre|sort|est|a)\b', re.U)


def bloc_stats(blocs):
    d = {}
    corps = [b for k, b in blocs if k == 'p']
    dialogues = [b for k, b in blocs if k == 'tiret']
    tout = ' '.join(b for k, b in blocs)

    d['blocs'] = len(blocs)
    d['paragraphes'] = len(corps)
    d['repliques'] = len(dialogues)
    d['mots'] = len(MOTS.findall(tout))

    ph = []
    for b in corps:
        ph.extend(phrases(b))
    longueurs = [len(MOTS.findall(p)) for p in ph]
    d['phrases'] = len(ph)
    d['mots_par_phrase'] = sum(longueurs) / float(len(longueurs)) if longueurs else 0
    longueurs_triees = sorted(longueurs)
    n = len(longueurs_triees)
    d['mediane'] = longueurs_triees[n // 2] if n else 0
    d['courtes_5'] = sum(1 for x in longueurs if x <= 5)
    d['longues_40'] = sum(1 for x in longueurs if x >= 40)
    d['longues_50'] = sum(1 for x in longueurs if x >= 50)
    d['plus_longue'] = max(longueurs) if longueurs else 0
    d['_phrases'] = ph
    d['_longueurs'] = longueurs

    par_mots = [len(MOTS.findall(b)) for b in corps]
    d['mots_par_paragraphe'] = sum(par_mots) / float(len(par_mots)) if par_mots else 0
    d['paragraphes_1_phrase'] = sum(1 for b in corps if len(phrases(b)) == 1)

    d['imparfait'] = len(IMPARFAIT.findall(tout))
    d['passe_simple'] = len(PASSE_SIMPLE.findall(tout))
    d['plus_que_parfait'] = len(PLUS_QUE_PARFAIT.findall(tout))
    d['present_verite'] = len(PRESENT_VERITE.findall(tout))

    d['virgules'] = tout.count(',')
    d['tirets_cadratins'] = tout.count('—')
    d['points_virgules'] = tout.count(';')
    d['deux_points'] = tout.count(':')
    d['guillemets'] = tout.count('«')
    d['parentheses'] = tout.count('(')

    mots = [w.lower() for w in MOTS.findall(tout)]
    d['vocabulaire'] = len(set(mots))
    d['richesse'] = len(set(mots)) / float(len(mots)) if mots else 0

    d['_mots'] = mots
    d['_corps'] = corps
    d['_tout'] = tout
    return d


VIDES = set(u"""le la les un une des de du d l et ou a à au aux en y il elle ils elles on
se s ce c que qui quoi dont où ne pas plus n'y n est sont était étaient avait avaient
son sa ses leur leurs lui eux dans sur sous pour par avec sans comme mais donc or ni car
je tu nous vous me te moi toi si tout toute tous toutes même quand puis alors alors
plus moins très bien alors rien qu on  l' d' j' c' n' s' t' m' y'""".split())


def repetitions(mots, n=1, seuil=6):
    if n == 1:
        c = collections.Counter(w for w in mots if w not in VIDES and len(w) > 3)
    else:
        grammes = [' '.join(mots[i:i + n]) for i in range(len(mots) - n + 1)]
        c = collections.Counter(g for g in grammes
                                if sum(1 for w in g.split() if w in VIDES) < n)
    return [(g, k) for g, k in c.most_common(40) if k >= seuil]


def ouvertures(phrases_):
    c = collections.Counter()
    for p in phrases_:
        w = MOTS.findall(p)
        if w:
            c[w[0].lower()] += 1
    return c.most_common(15)


def ambiguite(corps):
    """Reperage grossier : un paragraphe ou 'il' et 'elle' cohabitent sans nom propre
    entre les deux est un endroit ou le lecteur peut perdre le fil."""
    suspects = []
    for b in corps:
        for p in phrases(b):
            a = len(re.findall(r"\bil\b", p, re.I))
            e = len(re.findall(r"\belle\b", p, re.I))
            noms = len(re.findall(r"\b(Andrew|Vera|Bastien|Anna|Nora|Joël|Eliott|"
                                 r"June|Isaac|Chrissy|Tania)\b", p))
            if a and e and not noms:
                suspects.append(p)
    return suspects


def adverbes_ment(mots):
    c = collections.Counter(w for w in mots if w.endswith('ment') and len(w) > 6)
    return c.most_common(12)


print(u'MESURES DE STYLE — L\'ÉCLAIRCIE')
print(u'=' * 78)

tous = chapitres()
globaux = collections.Counter()
for ident, titre, blocs in tous:
    if not blocs:
        continue
    d = bloc_stats(blocs)
    print(u'\n\n### %s — %s' % (ident.upper(), titre))
    print(u'-' * 78)
    print(u'  %d mots, %d blocs (%d paragraphes, %d répliques)'
          % (d['mots'], d['blocs'], d['paragraphes'], d['repliques']))
    print(u'  dialogue : %.0f %% des blocs' % (100.0 * d['repliques'] / d['blocs']))
    print(u'')
    print(u'  PHRASES  %d au total, %.1f mots en moyenne, médiane %d'
          % (d['phrases'], d['mots_par_phrase'], d['mediane']))
    print(u'           %d de 5 mots ou moins (%.0f %%)'
          % (d['courtes_5'], 100.0 * d['courtes_5'] / d['phrases']))
    print(u'           %d de 40 mots ou plus, dont %d de 50 et plus'
          % (d['longues_40'], d['longues_50']))
    print(u'           la plus longue : %d mots' % d['plus_longue'])
    print(u'')
    print(u'  PARAGRAPHES  %.1f mots en moyenne, %d d\'une seule phrase (%.0f %%)'
          % (d['mots_par_paragraphe'], d['paragraphes_1_phrase'],
             100.0 * d['paragraphes_1_phrase'] / max(1, d['paragraphes'])))
    print(u'')
    print(u'  TEMPS  imparfait %d  |  passé simple %d  |  plus-que-parfait %d  |'
          u'  présent de vérité %d'
          % (d['imparfait'], d['passe_simple'], d['plus_que_parfait'], d['present_verite']))
    print(u'')
    print(u'  PONCTUATION pour 1000 mots  virgule %.0f  |  tiret %.0f  |  point-virgule %.0f'
          u'  |  deux-points %.0f  |  parenthèse %.0f'
          % tuple(1000.0 * d[k] / d['mots'] for k in
                  ('virgules', 'tirets_cadratins', 'points_virgules',
                   'deux_points', 'parentheses')))
    print(u'')
    print(u'  VOCABULAIRE  %d mots distincts, richesse %.3f'
          % (d['vocabulaire'], d['richesse']))

    print(u'\n  MOTS QUI REVIENNENT (6 fois ou plus)')
    for g, k in repetitions(d['_mots'], 1, 6):
        print(u'      %3d  %s' % (k, g))

    print(u'\n  GROUPES DE DEUX MOTS (4 fois ou plus)')
    for g, k in repetitions(d['_mots'], 2, 4):
        print(u'      %3d  %s' % (k, g))

    print(u'\n  GROUPES DE TROIS MOTS (3 fois ou plus)')
    for g, k in repetitions(d['_mots'], 3, 3):
        print(u'      %3d  %s' % (k, g))

    print(u'\n  DEBUTS DE PHRASE')
    print(u'      ' + u'  '.join(u'%s×%d' % (w, k) for w, k in ouvertures(d['_phrases'])))

    print(u'\n  ADVERBES EN -MENT')
    print(u'      ' + (u'  '.join(u'%s×%d' % (w, k) for w, k in adverbes_ment(d['_mots']))
                       or u'aucun'))

    amb = ambiguite(d['_corps'])
    print(u'\n  PHRASES OÙ IL ET ELLE COHABITENT SANS NOM PROPRE : %d' % len(amb))
    for p in amb[:6]:
        print(u'      • %s' % p[:150])

    print(u'\n  LES CINQ PLUS LONGUES')
    for p in sorted(d['_phrases'], key=lambda x: -len(MOTS.findall(x)))[:5]:
        print(u'      [%d mots] %s' % (len(MOTS.findall(p)), p[:260]))

    for k in ('mots', 'phrases', 'imparfait', 'passe_simple', 'longues_40', 'courtes_5'):
        globaux[k] += d[k]
    globaux['mots_narratifs'] += sum(d['_longueurs'])

print(u'\n\n' + u'=' * 78)
print(u'ENSEMBLE  %d mots, dont %d hors dialogue, en %d phrases de recit'
      % (globaux['mots'], globaux['mots_narratifs'], globaux['phrases']))
print(u'          %.1f mots par phrase de recit'
      % (globaux['mots_narratifs'] / float(globaux['phrases'])))
print(u'          imparfait %d contre passé simple %d'
      % (globaux['imparfait'], globaux['passe_simple']))
print(u'          %d phrases courtes (≤5 mots), %d longues (≥40)'
      % (globaux['courtes_5'], globaux['longues_40']))
