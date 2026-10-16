import json,re,subprocess,sys,numpy as np,soundfile as sf
def chunks(f,thr=0.15):
    dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
    out=subprocess.run(["ffmpeg","-i",f,"-af",f"silencedetect=noise=-38dB:d={thr}","-f","null","-"],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",out)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",out)]
    s=[0.0]+en; e=st+[dur]
    return dur,[(a,b) for a,b in zip(s,e) if b-a>0.15]
def build(name,audio,C,LINES,cfg,thr=0.15):
    dur,ch=chunks(audio,thr); assert len(ch)==len(C),(len(ch),len(C),ch)
    def words(i):
        a,b=ch[i]; ws=C[i].replace(" :"," :").replace(" ?"," ?").split(" "); w=[len(x)+1 for x in ws]; tot=sum(w); acc=0; r=[]
        for x,ww in zip(ws,w): r.append([x,round(a+(b-a)*acc/tot,3)]); acc+=ww
        return r
    lines=[{"scene":sc,"t":round(max(0,ch[idx[0]][0]-0.02),3),"d":round(ch[idx[-1]][1]-ch[idx[0]][0],3),"words":sum([words(i) for i in idx],[])} for sc,idx in LINES]
    allw=sum([l["words"] for l in lines],[])
    def at(word):  # time of first word containing `word`
        for w,t in allw:
            if word.lower() in w.lower(): return t
        raise KeyError(word)
    for it in cfg["items"]: it["at"]=at(it["at"]) if isinstance(it["at"],str) else it["at"]
    if isinstance(cfg.get("notifAt"),str): cfg["notifAt"]=at(cfg["notifAt"])
    if isinstance(cfg["chip"]["at"],str): cfg["chip"]["at"]=at(cfg["chip"]["at"])
    cfg.update(lines=lines,end=round(dur+1.4,2))
    open(f"/home/claude/reel/cfg_{name}.js","w").write("window.CFG="+json.dumps(cfg,ensure_ascii=False)+";")
    open(f"/home/claude/reel/short_{name}.html","w").write(open("/home/claude/reel/short.html").read().replace('src="cfg.js"',f'src="cfg_{name}.js"'))
    # audio mix
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",audio,"-ac","1","-ar","44100",f"/home/claude/reel/vo_{name}.wav"],check=True)
    vo,sr=sf.read(f"/home/claude/reel/vo_{name}.wav"); n=int(cfg["end"]*sr); v=np.zeros(n); v[:min(n,len(vo))]=vo[:n]
    fx=np.zeros(n); rng=np.random.default_rng(3)
    def tone(fs,d,vol,dec=26):
        t=np.arange(int(d*sr))/sr; return sum(np.sin(2*np.pi*f*t) for f in fs)/len(fs)*np.exp(-t*dec)*vol
    def whoosh():
        t=np.arange(int(0.4*sr))/sr; nz=np.convolve(rng.standard_normal(len(t)),np.ones(40)/40,'same'); return nz*np.sin(np.pi*t/0.4)**2*0.3
    ev=[(0,'boom')]; seen={'hook'}
    for l in lines:
        if l['scene'] not in seen: seen.add(l['scene']); ev.append((l['t']-0.15,'whoosh'))
    ev+=[(it['at'],'pop') for it in cfg['items']]+[(cfg['chip']['at'],'pop')]
    if cfg.get('notif'): ev.append((cfg['notifAt'],'notif'))
    for a,k in ev:
        y={'boom':tone([110,220],0.6,0.45,6),'whoosh':whoosh(),'pop':tone([880,1320],0.18,0.22,20),'notif':np.concatenate([tone([1568],0.15,0.25),tone([2093],0.3,0.25)])}[k]
        i=max(0,int(a*sr)); fx[i:i+len(y)]+=y[:max(0,n-i)]
    v=v/np.max(np.abs(v))*0.9; mix=np.clip(v+fx*0.45,-1,1)
    sf.write(f"/home/claude/reel/mix_{name}.wav",np.stack([mix,mix],1),sr)
    for i,c in enumerate(ch): print(i,round(c[0],2),round(c[1],2),C[i])
