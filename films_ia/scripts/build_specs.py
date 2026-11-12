#!/usr/bin/env python3
"""Construit spec_c1.json / spec_c4.json pour films.py (à lancer dans ~/films)."""
import json, subprocess, sys

def probe(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())
def W_(f): return json.load(open(f))
def merge_elisions(ws):
    out = []
    for a, b, t in ws:
        if t.startswith("'") and out: out[-1] = [out[-1][0], b, out[-1][2] + t]
        elif t.startswith("-") and out: out[-1] = [out[-1][0], b, out[-1][2] + t]
        elif t.strip("?!.,") == "" and out: out[-1] = [out[-1][0], b, out[-1][2] + " " + t]
        else: out.append([a, b, t])
    return out
def shift(ws, off, fix=None, lo=-1, hi=99):
    r = []
    for i, (a, b, t) in enumerate(ws):
        if not (lo <= a < hi): continue
        r.append([round(a + off, 3), round(b + off, 3), t])
    if fix:
        for i, t in fix.items(): r[i][2] = t
    return r

FONTS = "/home/user/film2/fonts"; BIG = "/home/user/film2/clips/big.mp4"
which = sys.argv[1]

if which == "c1":
    LIP = "lip_c1.mp4"
    A = merge_elisions(W_("src/c1_biscotte.words.json"))
    M = merge_elisions(W_("src/v_a.words.json")); DM = probe("src/v_a.mp3")
    M_AT = 24.05; B_OFF = 26.7 - 23.9; END_T0 = 28.75; TOTAL = END_T0 + 3.0
    wa = [w for w in A if 4.3 <= w[0] < 23.8]
    txt = ["Ses", "notes :", "maréchal,", "point", "d'interrogation.", "Vaccin,", "quand,", "point", "de", "suspension.",
           "Acheter", "carottes.", "Ça,", "c'est", "moi", "qui", "l'ai", "écrit.", "Alors", "je", "lui", "ai", "installé",
           "Horsetrack.", "Vaccins,", "maréchal,", "dentiste,", "ostéo :", "tout", "au", "même", "endroit,", "avec", "la",
           "date", "du", "prochain", "passage.", "Et", "un", "rappel", "avant.", "Pas", "après."]
    # whisper : C'est | note, | maréchale | .interrogation | Vaccin, | camp, | point | de | suspension | ...
    seq = []
    for a, b, t in wa:
        if t == ".interrogation":
            mid = round((a + b) / 2, 2); seq += [[a, mid, "x"], [mid, b, "x"]]
        else: seq.append([a, b, t])
    assert len(seq) == len(txt), (len(seq), len(txt), [s[2] for s in seq])
    words = [[a, b, t] for (a, b, _), t in zip(seq, txt)]
    mw = shift(M, M_AT); mtxt = "Attends… c'est toi qui as mis le dentiste ?".split(" ")
    mw = [[a, b, t] for (a, b, _), t in zip(mw, mtxt)] if len(mw) == len(mtxt) else mw
    words += mw
    words += shift([w for w in A if w[0] >= 23.9], B_OFF)
    rap = "src/C1_rappel.mp4"; san = "src/C1_sante.mp4"
    spec = {
        "fonts": FONTS, "total": TOTAL, "work": "work_c1",
        "audio": [{"file": "src/c1_biscotte.mp3", "src0": 0, "src1": 23.8, "at": 0.0},
                  {"file": "src/v_a.mp3", "src0": 0, "src1": DM, "at": M_AT},
                  {"file": "src/c1_biscotte.mp3", "src0": 23.9, "src1": 25.55, "at": 26.7}],
        "dings": [22.45, END_T0],
        "video": [
            {"t0": 0, "t1": 4.3, "kind": "clip", "file": LIP, "src": 0},
            {"t0": 4.3, "t1": 7.9, "kind": "clip", "file": BIG, "src": 5.5},
            {"t0": 7.9, "t1": 11.7, "kind": "clip", "file": BIG, "src": 9.0},
            {"t0": 11.7, "t1": 13.4, "kind": "clip", "file": LIP, "src": 11.7},
            {"t0": 13.4, "t1": 15.5, "kind": "phone", "file": rap, "src": 0.3, "bg": LIP, "bgsrc": 13.4},
            {"t0": 15.5, "t1": 21.6, "kind": "phone", "file": san, "src": 0.0, "bg": LIP, "bgsrc": 15.5},
            {"t0": 21.6, "t1": 23.95, "kind": "phone", "file": rap, "src": 3.6, "bg": LIP, "bgsrc": 21.6},
            {"t0": 23.95, "t1": 26.65, "kind": "clip", "file": BIG, "src": 12.3},
            {"t0": 26.65, "t1": END_T0, "kind": "clip", "file": LIP, "src": 23.85}],
        "hook": {"t0": 0, "t1": 4.2, "text": "Je vais vous montrer le téléphone de ma propriétaire."},
        "notes": {"t0": 4.6, "t1": 11.75, "title": "Notes", "lines": [[5.6, "maréchal ??"], [7.9, "vaccin… quand ?"], [10.5, "acheter carottes"]]},
        "callouts": [
            {"t0": 16.3, "t1": 21.55, "img": "src/co_vaccin.png", "y": 430, "tag": "Fiche santé de Biscotte"},
            {"t0": 16.75, "t1": 21.55, "img": "src/co_marechal.png", "y": 740},
            {"t0": 17.3, "t1": 21.55, "img": "src/co_dentiste.png", "y": 1050},
            {"t0": 22.35, "t1": 23.9, "img": "src/co_notif.png", "y": 330, "tag": "Rappel Horsetrack"}],
        "speakers": [[M_AT, M_AT + DM, "Manon"]],
        "words": words,
        "end": {"t0": END_T0, "title": "Le carnet de santé de ton cheval, dans ta poche.",
                "subs": ["Gratuit pour 1 cheval · iPhone", "Lien en bio"]}}
    json.dump(spec, open("spec_c1.json", "w"), ensure_ascii=False, indent=1)
    print("c1 ok", TOTAL, len(words))

if which == "c4":
    LIP = "lip_c4.mp4"; DUO = "duo.mp4"; MAN = "src/manon_c4.mp3"
    dshots = json.load(open("duo_shots.json"))  # {"lundi":s,"mardi":s,"dialogue":s,"phone":s}
    A = merge_elisions(W_("src/c4_biscotte.words.json"))
    DP = merge_elisions(W_("src/v_b.words.json")); MW = merge_elisions(W_("src/manon_c4.words.json")); DM = probe(MAN)
    DP1 = 14.0; MAT = DP1 + 1.3 + 0.15; X = MAT + DM + 0.15; Q = X + 0.84 + 0.3; OB = Q - 13.85
    END_T0 = round(24.0 + OB + 0.45, 2); TOTAL = END_T0 + 3.0
    fixA = {"Elle": "Elles", "parle": "parlent", "demi-pensionnaire.": "demi-pensionnaire.", "d'obstacles.": "d'obstacle."}
    wa = [[a, b, fixA.get(t, t)] for a, b, t in A if 5.3 <= a < 13.8]
    wb = []
    for a, b, t in A:
        if a < 13.9: continue
        t = {"elle": "elles", "partage": "partagent", "montent": "monte"}.get(t, t)
        if t == "Horst": wb.append([a, b, "Horsetrack."]); continue
        if t == "Track.": wb[-1][1] = b; continue
        wb.append([a, b, t])
    words = wa
    words += [[a + DP1, b + DP1, t] for a, b, t in DP if a < 1.35]
    mtxt = "Ben oui, je l'ai mis sur le groupe.".split(" ")
    mw = [[a + MAT, b + MAT, t] for a, b, t in MW]
    if len(mw) == len(mtxt): mw = [[a, b, t] for (a, b, _), t in zip(mw, mtxt)]
    words += mw
    words += [[a - 1.35 + X, b - 1.35 + X, t] for a, b, t in DP if a >= 1.35]
    words += [[round(a + OB, 3), round(b + OB, 3), t] for a, b, t in wb]
    t_part = round(Q, 2); t_plan = round(16.35 + OB, 2); t_res = round(19.5 + OB, 2); t_dim = round(22.35 + OB, 2)
    spec = {
        "fonts": FONTS, "total": TOTAL, "work": "work_c4",
        "audio": [{"file": "src/c4_biscotte.mp3", "src0": 0, "src1": 13.75, "at": 0.0},
                  {"file": "src/v_b.mp3", "src0": 0, "src1": 1.32, "at": DP1},
                  {"file": MAN, "src0": 0, "src1": DM, "at": MAT},
                  {"file": "src/v_b.mp3", "src0": 1.35, "src1": 2.19, "at": X},
                  {"file": "src/c4_biscotte.mp3", "src0": 13.85, "src1": 24.27, "at": Q}],
        "dings": [END_T0],
        "video": [
            {"t0": 0, "t1": 5.3, "kind": "clip", "file": LIP, "src": 0},
            {"t0": 5.3, "t1": 7.8, "kind": "clip", "file": DUO, "src": dshots["lundi"]},
            {"t0": 7.8, "t1": 9.75, "kind": "clip", "file": DUO, "src": dshots["mardi"]},
            {"t0": 9.75, "t1": 12.45, "kind": "clip", "file": BIG, "src": 0.0},
            {"t0": 12.45, "t1": 13.95, "kind": "clip", "file": LIP, "src": 12.45},
            {"t0": 13.95, "t1": t_part, "kind": "clip", "file": DUO, "src": dshots["dialogue"]},
            {"t0": t_part, "t1": t_plan, "kind": "phone", "file": "src/C4_partage_roles.mp4", "src": 0.3, "bg": LIP, "bgsrc": 14.0},
            {"t0": t_plan, "t1": t_res, "kind": "phone", "file": "src/C4_planning.mp4", "src": 1.0, "bg": LIP, "bgsrc": 16.5},
            {"t0": t_res, "t1": t_dim, "kind": "clip", "file": DUO, "src": dshots["phone"]},
            {"t0": t_dim, "t1": END_T0, "kind": "clip", "file": LIP, "src": 22.35}],
        "hook": {"t0": 0, "t1": 5.2, "text": "J'ai deux cavalières. Elles ne se parlent pas."},
        "stamps": [{"t0": 5.45, "t1": 7.75, "title": "LUNDI", "sub": "2 séances d'obstacle"},
                   {"t0": 7.95, "t1": 9.7, "title": "MARDI", "sub": "personne"},
                   {"t0": 9.85, "t1": 12.4, "title": "MERCREDI", "sub": "ration × 2"},
                   {"t0": round(22.46 + OB, 2), "t1": END_T0 - 0.05, "title": "DIMANCHE", "sub": "repos"}],
        "callouts": [
            {"t0": t_part + 0.5, "t1": t_plan - 0.05, "img": "src/co_partage.png", "y": 760, "tag": "Partager Biscotte"},
            {"t0": t_plan + 0.3, "t1": t_res - 0.05, "img": "src/co_jade.png", "y": 520, "tag": "Planning partagé"},
            {"t0": t_plan + 0.9, "t1": t_res - 0.05, "img": "src/co_manon.png", "y": 850}],
        "speakers": [[DP1, DP1 + 1.3, "Jade, sa demi-pensionnaire"], [MAT, MAT + DM, "Manon, sa propriétaire"], [X, X + 0.84, "Jade"]],
        "words": words,
        "end": {"t0": END_T0, "title": "Une fiche, deux cavalières, zéro malentendu.",
                "subs": ["Gratuit pour 1 cheval · iPhone", "Lien en bio"]}}
    json.dump(spec, open("spec_c4.json", "w"), ensure_ascii=False, indent=1)
    print("c4 ok", TOTAL, len(words))
