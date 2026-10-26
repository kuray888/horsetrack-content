import sys,os,json
from playwright.sync_api import sync_playwright
name=sys.argv[1]; here="/home/claude/reel"
data=json.load(open(f"{here}/car/{name}.json"))
open(f"{here}/car.js","w").write("window.CAR="+json.dumps(data,ensure_ascii=False)+";")
os.makedirs(f"{here}/car/{name}",exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=sorted(__import__("glob").glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome"))[-1],args=["--allow-file-access-from-files"])
    pg=b.new_page(viewport={"width":1080,"height":1350}); pg.goto(f"file://{here}/carousel.html"); pg.wait_for_timeout(700); pg.evaluate("document.fonts.ready")
    for i in range(len(data["slides"])):
        pg.evaluate(f"render({i})"); pg.wait_for_timeout(150)
        pg.screenshot(path=f"{here}/car/{name}/{name}_{i+1:02d}.png")
    b.close()
