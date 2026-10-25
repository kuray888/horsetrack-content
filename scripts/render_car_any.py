"""Rendu d'un carrousel 1080x1350 : python3 scripts/render_car_any.py modeles/c3.json medias/carrousels/c3"""
import sys, os, json
from playwright.sync_api import sync_playwright
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
name = os.path.basename(out.rstrip('/'))
mod = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modeles'))
data = json.load(open(src))
html = open(os.path.join(mod, 'carrousel.html'), encoding='utf-8').read().replace('<script src="car.js"></script>', '<script>window.CAR=' + json.dumps(data, ensure_ascii=False) + ';</script>')
tmp = os.path.join(mod, '_car_tmp.html'); open(tmp, 'w', encoding='utf-8').write(html)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1350}); pg.goto("file://" + tmp); pg.wait_for_timeout(700); pg.evaluate("document.fonts.ready")
    for i in range(len(data["slides"])):
        pg.evaluate(f"render({i})"); pg.wait_for_timeout(200)
        pg.screenshot(path=os.path.join(out, f"{name}_{i+1:02d}.png"))
    b.close()
os.remove(tmp); print("ok", out)
