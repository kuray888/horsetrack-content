#!/usr/bin/env python3
"""Moteur de montage des mini-films Horsetrack (1080x1920, 30 i/s), piloté par un spec JSON.
Usage: python3 films.py spec.json out.mp4
"""
import json, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
NAVY = (35, 27, 107); VIOLET = (108, 95, 214); LILAC = (184, 176, 242); CREAM = (246, 244, 240)
S = json.load(open(sys.argv[1])); OUT = sys.argv[2]
FD = S["fonts"]; TOTAL = S["total"]
WORK = S.get("work", "work"); os.makedirs(WORK, exist_ok=True)

def font(name, size, var):
    f = ImageFont.truetype(os.path.join(FD, name), size); f.set_variation_by_name(var); return f

def run(cmd): subprocess.run(cmd, check=True)
def probe(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())

F_CAP = font("Inter.ttf", 64, b"ExtraBold"); F_HOOK = font("Fraunces.ttf", 64, b"Bold")
F_TAG = font("Inter.ttf", 34, b"Bold"); F_STAMP = font("Fraunces.ttf", 112, b"Black")
F_STAMP2 = font("Inter.ttf", 50, b"Bold"); F_NOTE_T = font("Inter.ttf", 54, b"ExtraBold")
F_NOTE = font("Inter.ttf", 50, b"Medium"); F_END1 = font("Fraunces.ttf", 72, b"Bold")
F_END2 = font("Fraunces.ttf", 100, b"Bold"); F_END3 = font("Inter.ttf", 42, b"SemiBold")

# ---------- phone frame assets ----------
PH = 1440; PW = int(round(PH * S.get("rec_ratio", 1320 / 2868) / 2) * 2); PX = (W - PW) // 2; PY = 160; R = 64; BZ = 14
mask = Image.new("L", (PW, PH), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, PW - 1, PH - 1], R, fill=255)
mask.save(f"{WORK}/mask.png")
bez = Image.new("RGBA", (PW + 2 * BZ + 40, PH + 2 * BZ + 40), (0, 0, 0, 0)); bd = ImageDraw.Draw(bez)
bd.rounded_rectangle([20, 26, 20 + PW + 2 * BZ, 26 + PH + 2 * BZ], R + BZ, fill=(0, 0, 0, 90))
from PIL import ImageFilter
bez = bez.filter(ImageFilter.GaussianBlur(12)); bd = ImageDraw.Draw(bez)
bd.rounded_rectangle([20, 20, 20 + PW + 2 * BZ, 20 + PH + 2 * BZ], R + BZ, fill=(18, 16, 30, 255))
bez.save(f"{WORK}/bezel.png")

# ---------- base vidéo ----------
parts = []
for i, sg in enumerate(S["video"]):
    D = round(sg["t1"] - sg["t0"], 3); out = f"{WORK}/seg_{i:02d}.mp4"
    fit = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
    if sg["kind"] == "clip":
        cd = probe(sg["file"]) - sg["src"]
        f = max(sg.get("speed", 1.0), D / max(cd - 0.05, 0.1))
        vf = f"{fit},setpts={f:.4f}*(PTS-STARTPTS),fps={FPS},tpad=stop_mode=clone:stop_duration=2,trim=duration={D},setpts=PTS-STARTPTS"
        if sg.get("zoom"):
            z = sg["zoom"]; vf += f",scale={int(W*z)}:{int(H*z)},crop={W}:{H}"
        run(["ffmpeg", "-y", "-v", "error", "-ss", str(sg["src"]), "-i", sg["file"], "-an", "-vf", vf,
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", out])
    else:  # phone : enregistrement d'écran dans un téléphone, fond flouté
        sp = sg.get("speed", 1.0)
        fc = (f"[0:v]{fit},gblur=sigma=26,eq=brightness=-0.10:saturation=0.85,fps={FPS},setpts=PTS-STARTPTS,"
              f"tpad=stop_mode=clone:stop_duration={D},trim=duration={D}[bg];"
              f"[1:v]fps={FPS},scale={PW}:{PH},setpts={1/sp:.4f}*(PTS-STARTPTS),tpad=stop_mode=clone:stop_duration={D},"
              f"trim=duration={D},format=rgba[p0];[2:v]format=gray,scale={PW}:{PH}[m];[p0][m]alphamerge[ph];"
              f"[bg][3:v]overlay={PX - BZ - 20}:{PY - BZ - 20}[b1];[b1][ph]overlay={PX}:{PY},format=yuv420p[v]")
        run(["ffmpeg", "-y", "-v", "error", "-ss", str(sg["bgsrc"]), "-i", sg["bg"], "-ss", str(sg["src"]), "-i", sg["file"],
             "-loop", "1", "-i", f"{WORK}/mask.png", "-loop", "1", "-i", f"{WORK}/bezel.png",
             "-filter_complex", fc, "-map", "[v]", "-t", str(D), "-c:v", "libx264", "-preset", "veryfast",
             "-crf", "16", "-pix_fmt", "yuv420p", out])
    parts.append(out)
open(f"{WORK}/parts.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{WORK}/parts.txt",
     "-vf", "tpad=stop_mode=clone:stop_duration=6", "-t", str(TOTAL), "-c:v", "libx264", "-preset", "veryfast",
     "-crf", "16", "-pix_fmt", "yuv420p", f"{WORK}/base.mp4"])

# ---------- audio ----------
run(["sox", "-n", "-r", "48000", "-c", "2", f"{WORK}/ding.wav", "synth", "0.5", "sine", "1320",
     "fade", "0", "0.5", "0.45", "vol", "0.16"])
ins, fc, labels = [], "", []
for k, a in enumerate(S["audio"]):
    ins += ["-i", a["file"]]
    ms = int(a["at"] * 1000)
    fc += (f"[{k}:a]atrim={a['src0']}:{a['src1']},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,"
           f"volume={a.get('vol', 1.0)},adelay={ms}|{ms}[a{k}];")
    labels.append(f"[a{k}]")
for j, t in enumerate(S.get("dings", [])):
    k = len(S["audio"]) + j; ins += ["-i", f"{WORK}/ding.wav"]; ms = int(t * 1000)
    fc += f"[{k}:a]adelay={ms}|{ms}[d{j}];"; labels.append(f"[d{j}]")
fc += f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,apad,atrim=0:{TOTAL}[a]"
run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", fc, "-map", "[a]", "-ar", "48000", "-ac", "2", f"{WORK}/audio.wav"])

# ---------- incrustations ----------
def wrap(d, text, f, maxw):
    lines, line = [], ""
    for w in text.split(" "):
        t = (line + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: line = t
        else: lines.append(line); line = w
    lines.append(line); return lines

def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3

def box_text(img, text, f, y, pad=34, fg=NAVY, bg=(255, 255, 255, 238), maxw=920):
    d = ImageDraw.Draw(img); lines = wrap(d, text, f, maxw - 2 * pad)
    lh = f.size * 1.18; bw = max(d.textlength(l, font=f) for l in lines) + 2 * pad
    bh = lh * len(lines) + 2 * pad - f.size * 0.18; x0 = (W - bw) / 2
    d.rounded_rectangle([x0, y, x0 + bw, y + bh], 36, fill=bg)
    for i, l in enumerate(lines):
        lw = d.textlength(l, font=f); d.text(((W - lw) / 2, y + pad + i * lh - f.size * 0.12), l, font=f, fill=fg)
    return y + bh

def caption(img, ws, active, y, tag=None):
    d = ImageDraw.Draw(img); lines = wrap(d, " ".join(ws), F_CAP, 920); idx = 0
    if tag:
        tw = d.textlength(tag, font=F_TAG)
        d.rounded_rectangle([(W - tw) / 2 - 22, y - 70, (W + tw) / 2 + 22, y - 18], 26, fill=VIOLET)
        d.text(((W - tw) / 2, y - 66), tag, font=F_TAG, fill=(255, 255, 255))
    for li, line in enumerate(lines):
        x = (W - d.textlength(line, font=F_CAP)) / 2; yy = y + li * 82
        for w in line.split(" "):
            d.text((x, yy), w, font=F_CAP, fill=LILAC if idx == active else (255, 255, 255), stroke_width=7, stroke_fill=(20, 16, 60))
            x += d.textlength(w + " ", font=F_CAP); idx += 1

groups, cur = [], []
for w in S["words"]:
    cur.append(w)
    if len(cur) == 3 or w[2][-1] in ".,:…?!" or w[2].endswith("??") or (len(w) > 3 and w[3]):
        groups.append(cur); cur = []
if cur: groups.append(cur)

def seg_kind(t):
    for sg in S["video"]:
        if sg["t0"] <= t < sg["t1"]: return sg["kind"]
    return "clip"

def speaker(t):
    for a, b, n in S.get("speakers", []):
        if a - 0.1 <= t < b + 0.2: return n
    return None

def end_card(e):
    img = Image.new("RGBA", (W, H), CREAM + (255,)); d = ImageDraw.Draw(img)
    lines = wrap(d, e["title"], F_END1, 900); y = 600 - len(lines) * 45
    for l in lines:
        d.text(((W - d.textlength(l, font=F_END1)) / 2, y), l, font=F_END1, fill=NAVY); y += 92
    y += 90; d.line([(W / 2 - 60, y), (W / 2 + 60, y)], fill=LILAC, width=6); y += 80
    d.text(((W - d.textlength("Horsetrack", font=F_END2)) / 2, y), "Horsetrack", font=F_END2, fill=NAVY); y += 145
    for s in e["subs"]:
        d.text(((W - d.textlength(s, font=F_END3)) / 2, y), s, font=F_END3, fill=VIOLET); y += 64
    return img
END = S["end"]; END_IMG = end_card(END)

def notes_card(img, nc, t):
    lines = [l for l in nc["lines"] if t >= l[0]]
    a = ease((t - nc["t0"]) / 0.3) * ease((nc["t1"] - t) / 0.25)
    card = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
    x0, y0, cw = 110, 250, 860; ch = 150 + 96 * max(len(nc["lines"]), 1)
    d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], 40, fill=(255, 253, 245, 245))
    d.text((x0 + 50, y0 + 40), nc["title"], font=F_NOTE_T, fill=(214, 160, 20))
    for i, (tin, txt) in enumerate(lines):
        p = ease((t - tin) / 0.25); yy = y0 + 140 + i * 96 + int(20 * (1 - p))
        d.ellipse([x0 + 52, yy + 14, x0 + 84, yy + 46], outline=(190, 186, 176, int(255 * p)), width=4)
        d.text((x0 + 110, yy), txt, font=F_NOTE, fill=(40, 36, 30, int(255 * p)))
    card.putalpha(card.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(card)

def stamp(img, st, t):
    s = 0.6 + 0.4 * ease((t - st["t0"]) / 0.22); fade = ease((st["t1"] - t) / 0.2)
    lay = Image.new("RGBA", (W, 460), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    tw = max(d.textlength(st["title"], font=F_STAMP), d.textlength(st.get("sub", ""), font=F_STAMP2)) + 100
    bh = 300 if st.get("sub") else 190
    d.rounded_rectangle([(W - tw) / 2, 40, (W + tw) / 2, 40 + bh], 40, fill=VIOLET + (242,))
    d.text(((W - d.textlength(st["title"], font=F_STAMP)) / 2, 58), st["title"], font=F_STAMP, fill=(255, 255, 255))
    if st.get("sub"):
        d.text(((W - d.textlength(st["sub"], font=F_STAMP2)) / 2, 222), st["sub"], font=F_STAMP2, fill=(236, 233, 255))
    sw, sh = int(W * s), int(460 * s); lay = lay.resize((sw, sh), Image.LANCZOS)
    lay.putalpha(lay.getchannel("A").point(lambda v: int(v * fade)))
    img.alpha_composite(lay, ((W - sw) // 2, st.get("y", 230) + (460 - sh) // 2))

def frame(t):
    if t >= END["t0"]:
        im = END_IMG.copy(); im.putalpha(int(255 * ease((t - END["t0"]) / 0.35))); return im
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hk = S["hook"]
    if hk["t0"] <= t < hk["t1"]:
        box_text(img, hk["text"], F_HOOK, 300)
    nc = S.get("notes")
    if nc and nc["t0"] <= t < nc["t1"]: notes_card(img, nc, t)
    for st in S.get("stamps", []):
        if st["t0"] <= t < st["t1"]: stamp(img, st, t)
    y = 1690 if seg_kind(t) == "phone" else 1380
    for g in groups:
        if g[0][0] - 0.05 <= t < g[-1][1] + 0.3:
            act = max([i for i, w in enumerate(g) if t >= w[0] - 0.05] or [0])
            caption(img, [w[2] for w in g], act, y, tag=speaker(t)); break
    return img

p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-i", f"{WORK}/base.mp4", "-i", f"{WORK}/audio.wav",
    "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
    "-filter_complex", "[0:v][2:v]overlay=0:0:format=auto,format=yuv420p[v]", "-map", "[v]", "-map", "1:a",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart", "-t", str(TOTAL), OUT], stdin=subprocess.PIPE)
for n in range(int(TOTAL * FPS)):
    p.stdin.write(frame(n / FPS).tobytes())
p.stdin.close(); p.wait()
print("OK", OUT, TOTAL)
