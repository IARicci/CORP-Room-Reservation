#!/usr/bin/env python3
"""Build the Megawide Room Reservations portal.

Reads src/template.html and src/assets/*, embeds the images as data URIs,
and writes one self-contained HTML file per environment into dist/.

    python3 build.py              # build every environment
    python3 build.py staging      # build one environment
"""
import base64, mimetypes, pathlib, sys

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "dist"

# name: (output file, page title, published link used for app QR codes)
ENVIRONMENTS = {
    "production":   ("megawide-room-reservations.html",        "Megawide Room Reservations",        "https://claude.ai/artifact/HopqFU4zQC3hdbwunKbKTu"),
    "staging":      ("megawide-reservations-staging.html",     "Megawide Reservations Staging",     "https://claude.ai/artifact/QoUUo7y6TvgJKb9Kv9ymcw"),
    "demo":         ("megawide-reservations-demo.html",        "Megawide Reservations Demo",        "https://claude.ai/artifact/14aSvMadGKUXKdVyCwe2fV"),
    "presentation": ("megawide-reservations-client-demo.html", "Megawide Reservations Client Demo", "https://claude.ai/artifact/MAtJH3KC2oPHGHYN2wYgw3"),
}
ASSETS = {"LOGO": "logo.png", "LOGODARK": "logo-dark.png", "BOARD": "boardroom.jpg", "STUDIO": "studio.jpg", "LOBBY": "lobby.jpg"}


def data_uri(path: pathlib.Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def build(env: str) -> pathlib.Path:
    out_name, title, url = ENVIRONMENTS[env]
    html = (SRC / "template.html").read_text(encoding="utf-8")
    html = html.replace("{{ENV}}", env).replace("{{TITLE}}", title).replace("{{URL}}", url)
    for key, file in ASSETS.items():
        html = html.replace("{{" + key + "}}", data_uri(SRC / "assets" / file))
    if "{{" in html:
        i = html.index("{{")
        raise SystemExit(f"Unresolved placeholder near: {html[i-40:i+40]!r}")
    DIST.mkdir(exist_ok=True)
    out = DIST / out_name
    out.write_text(html, encoding="utf-8")
    return out


if __name__ == "__main__":
    targets = sys.argv[1:] or list(ENVIRONMENTS)
    for env in targets:
        if env not in ENVIRONMENTS:
            raise SystemExit(f"Unknown environment '{env}'. Choose from: {', '.join(ENVIRONMENTS)}")
        path = build(env)
        print(f"{env:13} -> {path.relative_to(ROOT)} ({path.stat().st_size // 1024} KB)")
