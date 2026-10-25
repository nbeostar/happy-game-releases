#!/usr/bin/env python3
"""Generate the download pages and QR codes of happy-game-releases.

    python3 -m venv .venv && .venv/bin/pip install segno && .venv/bin/python tools/build.py

Writes index.html, <game>/index.html and assets/qr-<game>.svg. Edit GAMES to add a game:
copy its icon to assets/<slug>-icon.png and three screenshots to assets/shots/<key>-1..3.png.
The pages look up the newest release whose tag starts with "<slug>-v" in the browser
(GitHub releases API), so a new release needs no site change.
"""
import html
import os

import segno

SITE = "https://nbeostar.github.io/happy-game-releases"
REPO = "nbeostar/happy-game-releases"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GAMES = [
    {
        "slug": "letterpostbode",
        "key": "lpb",
        "name": "Letterpostbode",
        "tagline": "Leren lezen met de postbode",
        "intro": "De postbode brengt brieven rond. Op elke envelop staat een letter, een woord of een zinnetje. "
                 "Lees het en stop de brief in de juiste brievenbus!",
        "color": "#ffb37a",
        "feats": [
            "27 niveaus: van losse letters tot zinnetjes met drie woorden of meer",
            "Lukt het niet? Het woord licht klank voor klank op, zodat je kunt hardop lezen",
            "Geen tijdsdruk, geen verliezen: fout? Gewoon nog een keer proberen",
            "Past bij groep 2 tot en met 4 (5 tot 7 jaar)",
        ],
        "shots": ["Een woord lezen en de goede brievenbus kiezen",
                  "Zinnetjes lezen: wie doet wat?",
                  "Negen werelden om uit te kiezen"],
    },
    {
        "slug": "rekenrups",
        "key": "rr",
        "name": "Rekenrups",
        "tagline": "Optellen en aftrekken tot 20",
        "intro": "Een vrolijke rups loopt door een zonnig landschap. Elke som die je goed hebt, laat hem een stukje groeien. "
                 "Tel de stipjes en kies het antwoord!",
        "color": "#a8dd9c",
        "feats": [
            "15 niveaus: plus en min tot 10, daarna tot 20 en door elkaar",
            "Stipjes om mee te tellen, ook bij het bruggetje over de tien",
            "Geen tijdsdruk, geen verliezen: fout? Gewoon nog een keer proberen",
            "Past bij groep 2 tot en met 4 (5 tot 7 jaar)",
        ],
        "shots": ["Tel de stipjes en kies het antwoord",
                  "Vijf werelden met elk drie niveaus",
                  "Klaar! Hoeveel sterren haal jij?"],
    },
]

HEAD = """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#8fd3f4">
<link rel="icon" href="{base}assets/{icon}">
<link rel="stylesheet" href="{base}assets/style.css">
</head>
"""


def esc(s):
    return html.escape(s, quote=True)


def make_qr(game):
    url = "%s/%s/" % (SITE, game["slug"])
    qr = segno.make(url, error="m")
    path = os.path.join(ROOT, "assets", "qr-%s.svg" % game["slug"])
    qr.save(path, scale=8, border=2, dark="#2a2a40", light="#ffffff", xmldecl=False, svgns=True)
    return url


def game_page(game):
    s = game["slug"]
    base = "../"
    other = [g for g in GAMES if g is not game]
    feats = "\n".join("<li>%s</li>" % esc(f) for f in game["feats"])
    shots = "\n".join(
        '<figure><img src="../assets/shots/%s-%d.png" alt="%s" width="1280" height="800">'
        "<figcaption>%s</figcaption></figure>" % (game["key"], i + 1, esc(cap), esc(cap))
        for i, cap in enumerate(game["shots"])
    )
    others = "\n".join(
        '<a class="card small" href="../%s/"><img src="../assets/%s-icon.png" alt="" width="72" height="72">'
        "<span><strong>%s</strong><br>%s</span></a>" % (o["slug"], o["slug"], esc(o["name"]), esc(o["tagline"]))
        for o in other
    )
    return HEAD.format(
        title="%s – gratis spel voor Android" % game["name"],
        desc=esc(game["tagline"] + ". " + game["intro"]),
        base=base,
        icon="%s-icon.png" % s,
    ) + f"""<body class="game" style="--accent:{game['color']}">
<header class="top"><a href="../">&larr; Alle spelletjes</a></header>
<main>
<section class="hero">
  <img class="icon" src="../assets/{s}-icon.png" alt="" width="160" height="160">
  <div>
    <h1>{esc(game['name'])}</h1>
    <p class="tagline">{esc(game['tagline'])}</p>
    <p>{esc(game['intro'])}</p>
    <p><a class="btn" id="download" href="https://github.com/{REPO}/releases" data-game="{s}">Download voor Android</a></p>
    <p class="meta" id="meta">Gratis &middot; geen advertenties &middot; werkt zonder internet</p>
  </div>
</section>

<section class="two">
  <div class="panel">
    <h2>Zo installeer je het</h2>
    <ol class="steps">
      <li><strong>Download</strong> het bestand met de knop hierboven (op de tablet zelf) of scan de QR-code.</li>
      <li>Tik op het gedownloade bestand. Vraagt Android of je apps uit deze bron mag installeren? Zet dan <em>Toestaan</em> aan.</li>
      <li>Tik op <strong>Installeren</strong>. Klaar! Het spel staat nu tussen de apps.</li>
    </ol>
    <p class="hint">Meldt <em>Play Protect</em> dat de app onbekend is? Kies <em>Toch installeren</em>. Het spel staat niet in de Play Store.</p>
  </div>
  <div class="panel qr">
    <h2>Scan met de tablet</h2>
    <img src="../assets/qr-{s}.svg" alt="QR-code naar deze pagina" width="220" height="220">
    <p class="hint">Open de camera van de tablet of telefoon en richt op de code.</p>
  </div>
</section>

<section class="panel">
  <h2>Over dit spel</h2>
  <ul class="feats">
{feats}
  </ul>
  <p class="safe"><strong>Veilig voor kinderen:</strong> geen advertenties, geen aankopen, geen account en er worden geen gegevens verzameld of verstuurd.</p>
</section>

<section class="shots">
{shots}
</section>

<section class="panel">
  <h2>Updates</h2>
  <p>Nieuwe versies verschijnen op deze pagina. Een nieuwe versie installeer je gewoon over de oude heen; je sterren blijven bewaard.
  Wil je automatisch updaten? Installeer dan de gratis app <a href="https://obtainium.imranr.dev/">Obtainium</a> en voeg
  <code>https://github.com/{REPO}</code> toe met het filter <code>{s}-v</code>.</p>
</section>

<section>
<h2>Meer spelletjes</h2>
<div class="cards">
{others}
</div>
</section>
</main>
<footer>Gemaakt met zorg voor kleine lezers en rekenaars. Vragen of een idee? Zeg het de maker.</footer>
<script src="../assets/site.js"></script>
</body>
</html>
"""


def index_page():
    cards = "\n".join(
        f'<a class="card" href="{g["slug"]}/" style="--accent:{g["color"]}"><img src="assets/{g["slug"]}-icon.png" alt="" width="120" height="120">'
        f'<span><strong>{esc(g["name"])}</strong><br>{esc(g["tagline"])}<br><em class="go">Bekijk en download &rarr;</em></span></a>'
        for g in GAMES
    )
    return HEAD.format(
        title="Happy Games – gratis spelletjes voor kleine lezers en rekenaars",
        desc="Gratis Android-spelletjes voor kinderen van 5 tot 7 jaar: leren lezen en rekenen. Geen advertenties.",
        base="",
        icon="letterpostbode-icon.png",
    ) + f"""<body class="home">
<main>
<section class="hero center">
  <h1>Happy Games</h1>
  <p class="tagline">Gratis spelletjes voor kinderen van 5 tot 7 jaar</p>
  <p>Geen advertenties, geen aankopen, geen account. Alles werkt zonder internet.</p>
</section>
<section class="cards big">
{cards}
</section>
</main>
<footer>Voor Android-tablets en -telefoons. De spellen staan niet in de Play Store; installeren gaat met een downloadbestand.</footer>
</body>
</html>
"""


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    write("index.html", index_page())
    for g in GAMES:
        make_qr(g)
        write("%s/index.html" % g["slug"], game_page(g))
    print("built", len(GAMES), "games")


if __name__ == "__main__":
    main()
