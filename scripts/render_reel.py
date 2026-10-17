"""Rendu générique d'un modèle animé (render(t), END, SOUNDS) en MP4 1080x1920 30 i/s.
Usage :
  python3 scripts/render_reel.py preview modeles/X.html dossier_sortie t1 t2 ...
  python3 scripts/render_reel.py video modeles/X.html sortie.mp4 [fond: calme|rythme|aucun]
"""
import sys, os, subprocess, tempfile, shutil
import numpy as np, soundfile as sf
from playwright.sync_api import sync_playwright

FPS = 30
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
mode, html = sys.argv[1], os.path.abspath(sys.argv[2])

def page(p):
    b = p.chromium.launch(executable_path=CHROME, args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto("file://" + html); pg.wait_for_timeout(800); pg.evaluate("document.fonts.ready")
    return b, pg

if mode == "preview":
    out = sys.argv[3]; os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b, pg = page(p)
        print("END", pg.evaluate("END"))
        for t in sys.argv[4:]:
            pg.evaluate(f"render({float(t)})")
            pg.screenshot(path=os.path.join(out, f"prev_{float(t):05.2f}.jpg"), type="jpeg", quality=80)
        b.close()
    sys.exit()

out = sys.argv[3]; bed = sys.argv[4] if len(sys.argv) > 4 else "calme"
tmp = tempfile.mkdtemp()
with sync_playwright() as p:
    b, pg = page(p)
    end = pg.evaluate("END"); snd = pg.evaluate("SOUNDS")
    n = int(end * FPS)
    for i in range(n):
        pg.evaluate(f"render({i / FPS})")
        pg.screenshot(path=os.path.join(tmp, f"f{i:04d}.jpg"), type="jpeg", quality=93)
    b.close()

# ---- audio : bruitages + petit fond musical synthétisé ----
sr = 44100; N = int(end * sr); fx = np.zeros(N); rng = np.random.default_rng(9)
def tone(fs, d, vol, dec=26):
    t = np.arange(int(d * sr)) / sr; return sum(np.sin(2 * np.pi * f * t) for f in fs) / len(fs) * np.exp(-t * dec) * vol
def whoosh():
    t = np.arange(int(0.4 * sr)) / sr; nz = np.convolve(rng.standard_normal(len(t)), np.ones(40) / 40, 'same'); return nz * np.sin(np.pi * t / 0.4) ** 2 * 0.35
def scratch():
    t = np.arange(int(0.35 * sr)) / sr; f = 900 - 2200 * t; ph = 2 * np.pi * np.cumsum(np.abs(f)) / sr
    return np.sign(np.sin(ph)) * 0.12 * np.exp(-t * 6) + rng.standard_normal(len(t)) * 0.08 * np.exp(-t * 10)
def tick():
    t = np.arange(int(0.05 * sr)) / sr; return (rng.standard_normal(len(t)) * 0.25 + np.sin(2 * np.pi * 2200 * t) * 0.3) * np.exp(-t * 120)
def notif():
    return np.concatenate([tone([1568], 0.12, 0.35), tone([2093], 0.28, 0.35)])
S = {'boom': lambda: tone([110, 220], 0.6, 0.5, 6), 'whoosh': whoosh, 'scratch': scratch, 'tick': tick, 'notif': notif,
     'pop': lambda: tone([880, 1320], 0.18, 0.25, 20), 'soft': lambda: tone([660, 990], 0.5, 0.18, 8),
     'ding': lambda: np.concatenate([tone([1318], 0.12, 0.35), tone([1760, 2637], 0.7, 0.35, 5)])}
for at, k in snd:
    s = S[k](); i = max(0, int(at * sr)); fx[i:i + len(s)] += s[:max(0, N - i)]

music = np.zeros(N)
if bed != "aucun":
    bpm = 84 if bed == "calme" else 104
    beat = 60 / bpm
    # progression I–V–vi–IV en do majeur (fréquences)
    prog = [[261.63, 329.63, 392.0], [196.0, 246.94, 392.0], [220.0, 261.63, 329.63], [174.61, 220.0, 349.23]]
    t = 0.0; k = 0
    while t < end:
        ch = prog[(k // 4) % 4]
        note = ch[k % 3] * (2 if bed == "rythme" and k % 2 else 1)
        d = beat * 1.6; tt = np.arange(int(d * sr)) / sr
        pl = (np.sin(2 * np.pi * note * tt) + 0.3 * np.sin(4 * np.pi * note * tt)) * np.exp(-tt * 3.2) * 0.16
        i = int(t * sr); music[i:i + len(pl)] += pl[:max(0, N - i)]
        if k % 4 == 0:  # nappe grave
            dd = beat * 4; t2 = np.arange(int(dd * sr)) / sr
            pad = sum(np.sin(2 * np.pi * f / 2 * t2) for f in ch) / 3 * np.sin(np.pi * t2 / dd) * 0.09
            music[i:i + len(pad)] += pad[:max(0, N - i)]
        if bed == "rythme" and k % 2 == 0:
            kk = tone([60, 90], 0.25, 0.22, 14); music[i:i + len(kk)] += kk[:max(0, N - i)]
        t += beat; k += 1
    fade = np.ones(N); fl = int(1.2 * sr); fade[-fl:] = np.linspace(1, 0, fl); music *= fade
mix = np.clip(fx + music, -1, 1)
wav = os.path.join(tmp, "a.wav"); sf.write(wav, np.stack([mix, mix], 1), sr)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.jpg"), "-i", wav,
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
                "-movflags", "+faststart", "-shortest", out], check=True)
shutil.rmtree(tmp); print("ok", out, round(end, 2), "s")
