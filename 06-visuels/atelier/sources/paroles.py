# -*- coding: utf-8 -*-
"""Extrait la parole de l'autrice, telle quelle, dans le depot."""
import io, json, re

SRC = r"C:\Users\giron\.claude\projects\R--Documents-l-Eclaircie\2004a0b6-5ae4-4806-96a2-cf4ff6f482d9.jsonl"
OUT = r"R:\Documents\l'Eclaircie\01-dossier\paroles-de-l-autrice.md"

def txt(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return u"\n".join(b.get("text", "") for b in c
                          if isinstance(b, dict) and b.get("type") == "text")
    return u""

REJET = (u"<local-command", u"<command-name>", u"Caveat:", u"[SYSTEM NOTIFICATION",
         u"This session is being continued", u"<task-notification", u"<system-reminder")

msgs, n = [], 0
with io.open(SRC, encoding="utf-8") as f:
    for line in f:
        n += 1
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("type") != "user":
            continue
        t = txt((r.get("message") or {}).get("content"))
        t = re.sub(r"<system-reminder>.*?</system-reminder>", u"", t, flags=re.S).strip()
        if not t or t.lstrip().startswith(REJET):
            continue
        if u"Result of calling the" in t or t.startswith(u"Tool loaded"):
            continue
        msgs.append((r.get("timestamp", "")[:16].replace(u"T", u" \u00e0 "), t))

# Le journal contient des branches : il n'est pas chronologique et il repete.
# On trie sur l'horodatage brut, puis on ecarte tout doublon de texte.
msgs.sort(key=lambda x: x[0])
propre, vus = [], set()
for ts, t in msgs:
    cle = u" ".join(t.split())
    if cle in vus:
        continue
    vus.add(cle)
    propre.append((ts, t))

with io.open(OUT, "w", encoding="utf-8") as o:
    o.write(u"# Les paroles de l'autrice\n\n")
    o.write(u"*Transcription brute et int\u00e9grale, du 13 au 19 ao\u00fbt 2026. "
            u"%d messages, dans l'ordre.*\n\n" % len(propre))
    o.write(u"> **Ce fichier ne se r\u00e9\u00e9crit jamais.** Ni corrections, ni reformulations, "
            u"ni coupes.\n> C'est la mati\u00e8re premi\u00e8re : tout le reste du dossier en d\u00e9coule "
            u"et peut \u00eatre v\u00e9rifi\u00e9 contre lui.\n> Il se r\u00e9g\u00e9n\u00e8re avec "
            u"`06-visuels/atelier/sources/paroles.py`.\n")
    for i, (ts, t) in enumerate(propre, 1):
        o.write(u"\n---\n\n### [%03d] %s\n\n%s\n" % (i, ts, t))

print(u"%d lignes lues, %d messages de l'autrice" % (n, len(propre)))
