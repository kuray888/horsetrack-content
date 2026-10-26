import sys, os, subprocess
from playwright.sync_api import sync_playwright

FPS = 30
here = os.path.dirname(os.path.abspath(__file__))
mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
out = os.path.join(here, os.environ.get("FR","frames"))
os.makedirs(out, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=sorted(__import__("glob").glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome"))[-1],
                          args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto("file://" + os.path.join(here, os.environ.get("HTML","reel.html")))
    pg.wait_for_timeout(800)
    pg.evaluate("document.fonts.ready")
    end = pg.evaluate("END")
    if mode == "preview":
        times = [float(x) for x in sys.argv[2:]]
        for t in times:
            pg.evaluate(f"render({t})")
            pg.screenshot(path=os.path.join(here, f"prev_{t:05.2f}.png"))
    else:
        n = int(end * FPS)
        for i in range(n):
            pg.evaluate(f"render({i / FPS})")
            pg.screenshot(path=os.path.join(out, f"f{i:04d}.jpg"), type="jpeg", quality=95)
        print("frames", n)
    b.close()
