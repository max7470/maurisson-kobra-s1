# -*- coding: utf-8 -*-
"""Récupère la photo og:image de chaque modèle du Dossier-Kobra-S1-Combo.html
et l'injecte dans les cartes .model. Photos stockées dans photos-modeles/.
Usage : python fetch_photos.py [--inject-only]
"""
import re, os, sys, json, time, subprocess, hashlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(BASE, "Dossier-Kobra-S1-Combo.html")
PHOTOS = os.path.join(BASE, "photos-modeles")
MAP = os.path.join(PHOTOS, "_mapping.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

# pas de photo unique pour les recherches/collections/catégories/outils
SKIP = ("search", "/collections/", "/3d-models/", "gridfinity.xyz", "wiki.anycubic",
        "thangs.com/designer", "github.com", "itslitho.com", "/SupportCenter/")

def curl(args, timeout=30):
    return subprocess.run(["curl", "-sL", "--compressed", "-m", str(timeout),
                           "-H", f"User-Agent: {UA}",
                           "-H", "Accept: text/html,application/xhtml+xml,image/*"] + args,
                          capture_output=True)

def get_og_image(url):
    r = curl([url])
    html = r.stdout.decode("utf-8", "ignore")
    m = (re.search(r'property="og:image"[^>]*content="([^"]+)"', html)
         or re.search(r'content="([^"]+)"[^>]*property="og:image"', html))
    return m.group(1).replace("&amp;", "&") if m else None

def slugify(url):
    tail = url.rstrip("/").split("/")[-1][:60]
    tail = re.sub(r"[^a-zA-Z0-9_-]", "_", tail)
    return tail + "_" + hashlib.md5(url.encode()).hexdigest()[:6]

def ext_of(img_url):
    path = img_url.split("?")[0].lower()
    for e in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
        if path.endswith(e):
            return ".jpg" if e == ".jpeg" else e
    return ".jpg"

def main():
    inject_only = "--inject-only" in sys.argv
    os.makedirs(PHOTOS, exist_ok=True)
    with open(HTML, encoding="utf-8") as f:
        doc = f.read()

    # cartes modèle : <div class="model"><h4><a href="URL">
    card_urls = re.findall(r'<div class="model"><h4><a href="([^"]+)"', doc)
    uniq = list(dict.fromkeys(card_urls))
    mapping = {}
    if os.path.exists(MAP):
        mapping = json.load(open(MAP, encoding="utf-8"))

    if not inject_only:
        todo = [u for u in uniq if u not in mapping and not any(s in u for s in SKIP)]
        print(f"{len(uniq)} liens uniques, {len(todo)} a fetcher")
        for i, url in enumerate(todo, 1):
            try:
                img = get_og_image(url)
                if not img:
                    mapping[url] = None
                    print(f"[{i}/{len(todo)}] OG ABSENT  {url[:80]}")
                else:
                    # vignette plus légère côté makerworld
                    img_dl = img.replace("resize,w_1200", "resize,w_520")
                    fname = slugify(url) + ext_of(img)
                    fpath = os.path.join(PHOTOS, fname)
                    r = curl(["-o", fpath, img_dl], timeout=40)
                    ok = os.path.exists(fpath) and os.path.getsize(fpath) > 2000
                    mapping[url] = fname if ok else None
                    print(f"[{i}/{len(todo)}] {'OK ' if ok else 'KO '} {fname[:70]}")
                json.dump(mapping, open(MAP, "w", encoding="utf-8"), indent=1)
                time.sleep(0.6)
            except Exception as e:
                mapping[url] = None
                print(f"[{i}/{len(todo)}] ERREUR {url[:60]} : {e}")

    # injection : <img> juste apres <div class="model"> quand on a une photo
    injected = 0
    def repl(m):
        nonlocal injected
        url = m.group(1)
        fname = mapping.get(url)
        if not fname:
            return m.group(0)
        injected += 1
        return (f'<div class="model"><a href="{url}" class="thumbwrap">'
                f'<img class="thumb" src="photos-modeles/{fname}" loading="lazy" alt=""'
                f' onerror="this.style.display=\'none\'"></a><h4><a href="{url}"')

    # ne pas re-injecter si deja fait
    doc = re.sub(r'<div class="model"><a href="[^"]+" class="thumbwrap">.*?</a>(<h4>)',
                 r'<div class="model">\1', doc, flags=re.S)
    doc = re.sub(r'<div class="model"><h4><a href="([^"]+)"', repl, doc)

    if ".model img.thumb" not in doc:
        doc = doc.replace(".model .meta{",
            ".model img.thumb{width:100%; height:150px; object-fit:cover; border-radius:8px;"
            " margin-bottom:10px; background:#0a0d12; display:block;}\n  .model .meta{")

    with open(HTML, "w", encoding="utf-8") as f:
        f.write(doc)
    have = sum(1 for v in mapping.values() if v)
    print(f"FINI : {have} photos en local, {injected} cartes illustrees, "
          f"{sum(1 for v in mapping.values() if not v)} sans photo (recherches/collections/og absent)")

if __name__ == "__main__":
    main()
