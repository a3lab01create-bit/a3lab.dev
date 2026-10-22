#!/usr/bin/env python3
"""Build the deployable docs/ folder from the artifact source.

index.html in this folder is the artifact version: it has no <!doctype>,
<head> or <body>, because the Artifact host adds them. This script wraps
it in a full document with search and link-preview tags for GitHub Pages,
and renders the preview image and icons from brand/ with headless Chrome.

Run:  python3 build.py            (page only)
      python3 build.py --images   (page + og.png + icons)
"""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "index.html"
SITE = ROOT / "docs"
BRAND = ROOT / "brand"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

DOMAIN = "a3lab.dev"
URL = f"https://{DOMAIN}/"
TITLE = "a3lab | 일하는 방식에 AI를 연결합니다"
DESC = ("a3lab은 회사에 이미 있는 데이터와 도구를 AI 에이전트로 연결하는 AX 스튜디오입니다. "
        "Claude, Gemini, GPT 등 여러 AI가 역할을 나눠 반복 업무를 처리합니다.")
OG_ALT = "a3lab 로고와 '일하는 방식에 AI를 연결합니다' 문구"

# Google Analytics (GA4). Google asks for it right after <head>.
GA_ID = "G-6CPVVVQCG3"
GTAG = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{GA_ID}');
</script>
"""

HEAD = f"""<!doctype html>
<html lang="ko">
<head>
{GTAG}<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<meta name="theme-color" content="#faf9f9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#111012" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="a3lab">
<meta property="og:locale" content="ko_KR">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="{URL}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{OG_ALT}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{URL}og.png">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>:root{{color-scheme:light}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
"""

# Lines only the artifact host understands; dropped from the real page.
ARTIFACT_ONLY = ("<title>", '<meta name="claude:viewport-fit-sides"')


def build_page():
    src = SRC.read_text(encoding="utf-8")
    cut = src.find("\n<nav")
    if cut < 0:
        sys.exit("build.py: could not find <nav> where the page body starts")
    head_part = "\n".join(
        ln for ln in src[:cut].splitlines() if not ln.lstrip().startswith(ARTIFACT_ONLY)
    )
    body_part = src[cut + 1:]
    SITE.mkdir(exist_ok=True)
    (SITE / "index.html").write_text(
        HEAD + head_part + "\n</head>\n<body>\n" + body_part.rstrip() + "\n</body>\n</html>\n",
        encoding="utf-8",
    )
    (SITE / "CNAME").write_text(DOMAIN + "\n", encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    print("built docs/index.html, CNAME, .nojekyll")


def shot(html, out, w, h):
    with tempfile.TemporaryDirectory() as prof:
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             f"--user-data-dir={prof}", "--force-device-scale-factor=1",
             f"--window-size={w},{h}", "--virtual-time-budget=5000",
             f"--screenshot={out}", html.as_uri()],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )


def build_images():
    from PIL import Image

    shot(BRAND / "og.html", SITE / "og.png", 1200, 630)
    with tempfile.TemporaryDirectory() as tmp:
        big = Path(tmp) / "icon-512.png"
        shot(BRAND / "icon.html", big, 512, 512)
        icon = Image.open(big).convert("RGBA")
        icon.resize((180, 180), Image.LANCZOS).save(SITE / "apple-touch-icon.png")
        icon.resize((32, 32), Image.LANCZOS).save(SITE / "favicon-32.png")
        icon.save(SITE / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("built docs/og.png, apple-touch-icon.png, favicon-32.png, favicon.ico")


if __name__ == "__main__":
    build_page()
    if "--images" in sys.argv:
        build_images()
