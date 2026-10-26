import sys,numpy as np,soundfile as sf
from playwright.sync_api import sync_playwright
html,out=sys.argv[1],sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=sorted(__import__("glob").glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome"))[-1])
    pg=b.new_page(); pg.goto(f"file:///home/claude/reel/{html}"); snd=pg.evaluate("SOUNDS"); end=pg.evaluate("END"); b.close()
sr=44100; n=int(end*sr); y=np.zeros(n); rng=np.random.default_rng(9)
def tone(fs,d,vol,dec=26):
    t=np.arange(int(d*sr))/sr; return sum(np.sin(2*np.pi*f*t) for f in fs)/len(fs)*np.exp(-t*dec)*vol
def whoosh():
    t=np.arange(int(0.4*sr))/sr; nz=np.convolve(rng.standard_normal(len(t)),np.ones(40)/40,'same'); return nz*np.sin(np.pi*t/0.4)**2*0.35
def scratch():
    t=np.arange(int(0.35*sr))/sr; f=900-2200*t; ph=2*np.pi*np.cumsum(np.abs(f))/sr
    return np.sign(np.sin(ph))*0.12*np.exp(-t*6)+rng.standard_normal(len(t))*0.08*np.exp(-t*10)
def tick():
    t=np.arange(int(0.05*sr))/sr; return (rng.standard_normal(len(t))*0.25+np.sin(2*np.pi*2200*t)*0.3)*np.exp(-t*120)
def notif():
    t=np.arange(int(0.5*sr))/sr; bz=np.sign(np.sin(2*np.pi*170*t))*0.08*(t<0.35); ch=np.concatenate([tone([1568],0.15,0.4),tone([2093],0.3,0.4)]); bz[:len(ch)]+=ch[:len(bz)]; return bz
S={'boom':lambda:tone([110,220],0.6,0.5,6),'whoosh':whoosh,'scratch':scratch,'tick':tick,'notif':notif,
   'recv':lambda:np.concatenate([tone([1320],0.07,0.35),tone([1760],0.12,0.35)]),'send':lambda:tone([1046,1568],0.14,0.3),
   'pop':lambda:tone([880,1320],0.18,0.25,20),'ding':lambda:np.concatenate([tone([1318],0.12,0.35),tone([1760,2637],0.7,0.35,5)])}
for at,k in snd:
    s=S[k](); i=int(at*sr); y[i:i+len(s)]+=s[:max(0,n-i)]
if html=='reel14.html':
    i=int((snd[-1][0]+0.43)*sr); d=tone([1318,1975],0.8,0.25,5); y[i:i+len(d)]+=d[:max(0,n-i)]
y=np.clip(y,-1,1); sf.write(out,np.stack([y,y],1),sr)
