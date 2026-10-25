# happy-game releases

Download pages and APK releases for the Android games (Rekenrups, Letterpostbode).
Site: https://nbeostar.github.io/happy-game-releases/

This repo holds no source code. Releases are published here by the private build repo
(`tools/` is only the page generator: `tools/build.py` writes the HTML and the QR codes).
To add a game: copy its icon to `assets/<slug>-icon.png`, three screenshots to
`assets/shots/<key>-1..3.png`, add it to `GAMES` in `tools/build.py` and run the script
(`python3 -m venv .venv && .venv/bin/pip install segno`).
