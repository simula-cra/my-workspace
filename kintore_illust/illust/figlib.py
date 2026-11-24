import math, json
INK='#1E1E1E'; FAR='#9A9A9A'; SW=0.75
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(a,k): return (a[0]*k,a[1]*k)
def norm(a):
    L=math.hypot(*a) or 1; return (a[0]/L,a[1]/L)
def cr(pts,closed=True):
    n=len(pts); P=lambda i: pts[i%n] if closed else pts[max(0,min(n-1,i))]
    f=lambda v:(f'{v:.1f}').rstrip('0').rstrip('.') if abs(v-round(v))>0.05 else str(int(round(v)))
    d=f'M{f(pts[0][0])} {f(pts[0][1])}'
    for i in range(n if closed else n-1):
        p0,p1,p2,p3=P(i-1),P(i),P(i+1),P(i+2)
        c1=add(p1,mul(sub(p2,p0),1/6)); c2=sub(p2,mul(sub(p3,p1),1/6))
        if i==0: d+=f'C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}'
        else: d+=f'S{f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}'
    return d+('Z' if closed else '')
def limb(joints,keys,cap0=0.6,cap1=0.6,step=2.6):
    """joints: list of points; keys: per bone list of (t,A,B). A=left of travel (posterior)."""
    S=[];W=[]
    for b in range(len(joints)-1):
        p,q=joints[b],joints[b+1]; L=math.hypot(*sub(q,p)); k=keys[b]
        n=max(2,int(L/step))
        for i in range(n+ (1 if b==len(joints)-2 else 0)):
            t=i/n
            for j in range(len(k)-1):
                if k[j][0]<=t<=k[j+1][0]:
                    u=(t-k[j][0])/((k[j+1][0]-k[j][0]) or 1)
                    u=(1-math.cos(u*math.pi))/2
                    A=k[j][1]+(k[j+1][1]-k[j][1])*u; B=k[j][2]+(k[j+1][2]-k[j][2])*u; break
            S.append(add(p,mul(sub(q,p),t))); W.append((A,B))
    # smooth skeleton tangents
    left=[];right=[]
    for i,s in enumerate(S):
        t=norm(sub(S[min(i+2,len(S)-1)],S[max(i-2,0)])); nrm=(-t[1],t[0])
        left.append(add(s,mul(nrm,-W[i][0]))); right.append(add(s,mul(nrm,W[i][1])))
    def filt(side):
        out=[side[0]]
        for i in range(1,len(side)):
            t=norm(sub(S[min(i+1,len(S)-1)],S[max(i-1,0)]))
            v=sub(side[i],out[-1])
            if v[0]*t[0]+v[1]*t[1]>0.15: out.append(side[i])
        return out
    left=filt(left); right=filt(right)
    t0=norm(sub(S[1],S[0])); t1=norm(sub(S[-1],S[-2]))
    e0=sub(S[0],mul(t0,(W[0][0]+W[0][1])/2*cap0)); e1=add(S[-1],mul(t1,(W[-1][0]+W[-1][1])/2*cap1))
    pts=left+[e1]+right[::-1]+[e0]
    return cr(pts)
def head(c,theta,s=1.0):
    loc=[(-5,0.2),(-4.6,-2.8),(-2.8,-5),(0,-5.7),(2.8,-4.9),(4.5,-2.9),(4.9,-1.0),(5.8,0.5),(5.0,1.3),(5.0,2.4),(4.6,3.2),(4.3,4.4),(3.2,5.0),(1.2,4.7),(-0.8,3.6),(-3.6,2.8)]
    th=math.radians(theta); c_,s_=math.cos(th),math.sin(th)
    return cr([(c[0]+s*(x*c_-y*s_),c[1]+s*(x*s_+y*c_)) for x,y in loc])
def hpt(c,theta,x,y,s=1.0):
    th=math.radians(theta); return (c[0]+s*(x*math.cos(th)-y*math.sin(th)),c[1]+s*(x*math.sin(th)+y*math.cos(th)))
# width presets (posterior A, anterior B)
TORSO=[[(0,3.0,3.6),(0.2,4.6,6.4),(0.45,4.4,6.6),(1,3.8,5.2)],[(0,3.8,5.2),(0.55,5.4,5.0),(1,4.6,4.2)]]
ARM=[[(0,3.0,3.1),(0.45,2.9,2.5),(1,1.8,1.8)],[(0,1.8,1.9),(0.3,2.1,2.4),(1,1.2,1.3)]]
LEG=[[(0,4.6,4.4),(0.5,3.9,4.5),(0.85,3.0,3.4),(1,2.6,2.8)],[(0,2.6,2.6),(0.25,3.4,2.3),(0.8,1.8,1.6),(1,1.4,1.4)]]
HAND=[[(0,0.9,1.3),(0.6,0.8,1.5),(1,0.5,0.8)]]
FOOT=[[(0,1.2,1.4),(1,1.0,1.6)],[(0,1.0,1.6),(1,0.5,0.8)]]
NECK=[[(0,1.9,1.9),(1,2.1,2.3)]]
def P(d,stroke=INK,fill='#FFFFFF'): return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{SW}" stroke-linejoin="round"></path>'
C=dict(NF='#DADDDF',FF='#7E8488',INK='#141516',MUS='#5B8A9E',NGF='#E0A458',NGFF='#8E6E40')
STY={'near':lambda ng:f'fill="{C["NGF"] if ng else C["NF"]}" stroke="{C["INK"]}" stroke-width="0.75" stroke-linejoin="round"',
     'far':lambda ng:f'fill="{C["NGFF"] if ng else C["FF"]}" stroke="{C["INK"]}" stroke-width="0.75" stroke-linejoin="round"',
     'mus':lambda ng:f'fill="{C["MUS"]}"',
     'out':lambda ng:f'fill="none" stroke="{C["INK"]}" stroke-width="0.75"',
     'seam':lambda ng:f'stroke="{C["INK"]}" stroke-width="0.55" stroke-linecap="round"',
     'seamfar':lambda ng:f'stroke="{C["INK"]}" stroke-width="0.55" stroke-linecap="round"',
     'raw':None}
RECOLOR={'#8C8C8C':'#5F6569','#D9D9D9':'#3A3E41','#6E6E6E':'#C9CDD0','#D0D0D0':'#33373A','#1E1E1E':'#C9CDD0'}
class Fig:
    def __init__(s,uid): s.uid=uid; s.items=[]; s.defs=[]; s.n=0; s.pending={}
    def part(s,d,far=False,name=None):
        s.n+=1; pid=f'{s.uid}{s.n}'
        s.items.append(('far' if far else 'near',f'<path id="{pid}" d="{d}"></path>'))
        if name and name in s.pending:
            cid=pid+'c'; s.defs.append(f'<clipPath id="{cid}"><use href="#{pid}"></use></clipPath>')
            s.items.append(('mus',f'<g clip-path="url(#{cid})">'+''.join(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx}" ry="{ry}" transform="rotate({a:.0f} {x:.1f} {y:.1f})"></ellipse>' for x,y,rx,ry,a in s.pending[name])+'</g>'))
            s.items.append(('out',f'<use href="#{pid}"></use>'))
    def plan(s,name,ells): s.pending.setdefault(name,[]); s.pending[name]=s.pending[name]+ells
    def plan_m(s,names,ells): s.plan(names[0],ells)
    def raw(s,x,cls='raw'): s.items.append((cls,x))
    def inner(s,ng=False):
        out=[]; cur=None; buf=[]
        items=[it for it in s.items if not (ng and it[0] in ('mus','out'))]
        def flush():
            if not buf: return
            if cur=='raw':
                x=''.join(buf)
                for k,v in RECOLOR.items(): x=x.replace(k,v)
                out.append(x)
            else: out.append(f'<g {STY[cur](ng)}>'+''.join(buf)+'</g>')
        for c_,x in items:
            if c_!=cur: flush(); cur=c_; buf=[]
            buf.append(x)
        flush()
        d=f'<defs>{"".join(s.defs)}</defs>' if s.defs and not ng else ''
        return d+''.join(out)
    def svg(s,vb,label,ng=False): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{label}">{s.inner(ng)}</svg>'
def bone_pt(p,q,t,off):
    v=sub(q,p); u=norm(v); n=(-u[1],u[0]); b=add(p,mul(v,t)); return add(b,mul(n,off)), math.degrees(math.atan2(u[1],u[0]))
FLOOR_H='<line x1="2" y1="55.4" x2="98" y2="55.4" stroke="#8C8C8C" stroke-width="0.8"></line>'
FLOOR_V='<line x1="2" y1="95.4" x2="58" y2="95.4" stroke="#8C8C8C" stroke-width="0.8"></line>'
def jm(f,c,r=1.25,far=False):
    col=FAR if far else INK
    x,y=c
    f.raw(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#FFFFFF" fill-opacity="0.85" stroke="{col}" stroke-width="0.5"></circle><path d="M{x:.1f} {y:.1f} L{x+r:.1f} {y:.1f} A{r} {r} 0 0 1 {x:.1f} {y+r:.1f}Z M{x:.1f} {y:.1f} L{x-r:.1f} {y:.1f} A{r} {r} 0 0 1 {x:.1f} {y-r:.1f}Z" fill="{col}"></path>')
def seam(f,a,c,b,A,B,far=False,shift=0.0):
    u1=norm(sub(c,a)); u2=norm(sub(b,c)); u=norm(add(u1,u2)); n=(-u[1],u[0])
    c=add(c,mul(u,shift))
    p=add(c,mul(n,-A)); q=add(c,mul(n,B))
    f.raw(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}"></line>','seamfar' if far else 'seam')
def side_figure(f,k,far_arm=None,far_leg=None,order='arm_front',arm_first=False):
    tor=k['torso']
    if far_leg:
        f.part(limb([far_leg['heel'],far_leg['ball'],far_leg['toe']],FOOT,1,0.8),True); f.part(limb([k['hip'],far_leg['knee'],far_leg['ank']],LEG),True)
        seam(f,k['hip'],far_leg['knee'],far_leg['ank'],2.9,3.3,True)
    if far_arm:
        f.part(limb([k['sh'],far_arm['elb'],far_arm['wr']],ARM),True); f.part(limb([far_arm['wr'],far_arm['fing']],HAND,0.5,0.9),True)
        seam(f,k['sh'],far_arm['elb'],far_arm['wr'],2.0,1.9,True)
    def arm():
        f.part(limb([k['sh'],k['elb'],k['wr']],ARM,0.6,0.5),name='arm')
        seam(f,tor[0],k['sh'],k['elb'],3.0,3.1,shift=1.6); seam(f,k['sh'],k['elb'],k['wr'],1.9,1.9)
        f.part(limb([k['wr'],k['fing']],HAND,0.5,0.9),name='hand')
        seam(f,k['elb'],k['wr'],k['fing'],1.3,1.4)
    if arm_first: arm()
    f.part(limb([k['hc_neck'],k['N']],NECK),name='neck')
    f.part(head(k['head'],k['ht'],k.get('hs',1)),name='head')
    f.part(limb([k['heel'],k['ball'],k['toe']],FOOT,1,0.8),name='foot')
    f.part(limb([k['hip'],k['knee'],k['ank']],LEG,0.4,0.6),name='leg')
    seam(f,tor[1],k['hip'],k['knee'],3.9,3.9,shift=2.6); seam(f,k['hip'],k['knee'],k['ank'],2.7,2.9); seam(f,k['knee'],k['ank'],k['toe'],1.5,1.5)
    f.part(limb(tor,TORSO,0.5,0.7),name='torso')
    seam(f,tor[0],tor[1],tor[2],4.3,5.6)
    if not arm_first: arm()

def ik(sh,wr,l1,l2,sign=1):
    d=math.hypot(*sub(wr,sh)); d=min(d,l1+l2-0.01)
    a=(l1*l1-l2*l2+d*d)/(2*d); h=math.sqrt(max(l1*l1-a*a,0))
    u=norm(sub(wr,sh)); base=add(sh,mul(u,a)); n=(-u[1],u[0])
    return add(base,mul(n,h*sign))
def K(N,hip,sh,elb,wr,fing,knee,ank,heel,ball,toe,head,ht,bend=0.0):
    mid=mul(add(N,hip),0.5)
    if bend:
        u=norm(sub(hip,N)); n=(-u[1],u[0]); mid=add(mid,mul(n,bend))
    k=dict(N=N,hip=hip,sh=sh,elb=elb,wr=wr,fing=fing,knee=knee,ank=ank,heel=heel,ball=ball,toe=toe,head=head,ht=ht)
    k['torso']=[N,mid,hip]; k['hc_neck']=hpt(head,ht,-1.2,3.2); return k
def ell_head(c,theta,rx=5.0,ry=5.6):
    t=math.radians(theta); ct,st=math.cos(t),math.sin(t)
    return cr([(c[0]+rx*math.cos(a)*ct-ry*math.sin(a)*st, c[1]+rx*math.cos(a)*st+ry*math.sin(a)*ct) for a in [i/16*2*math.pi for i in range(16)]])
def head_m(c,theta,s=1.0):
    """mirrored profile head (local y flipped): face=+x, crown=+y"""
    loc=[(-5,0.2),(-4.6,-2.8),(-2.8,-5),(0,-5.7),(2.8,-4.9),(4.5,-2.9),(4.9,-1.0),(5.8,0.5),(5.0,1.3),(5.0,2.4),(4.6,3.2),(4.3,4.4),(3.2,5.0),(1.2,4.7),(-0.8,3.6),(-3.6,2.8)]
    th=math.radians(theta); c_,s_=math.cos(th),math.sin(th)
    return cr([(c[0]+s*(x*c_+y*s_),c[1]+s*(x*s_-y*c_)) for x,y in loc])
def S_out(S,path):
    import json; json.dump(S,open(path,'w'),ensure_ascii=False)
def preview(S,names,path,big=240):
    html='<style>div>svg{width:100%;height:100%;display:block}</style><body style="background:#1C1E1F;margin:12px">'
    for nm in names:
        for s in (92,big): html+=f'<div style="display:flex;gap:10px;margin:5px"><div style="width:{s}px;height:{s}px;outline:1px dashed #333">{S[nm+"_1"]}</div><div style="width:{s}px;height:{s}px;outline:1px dashed #333">{S[nm+"_2"]}</div></div>'
    open(path,'w').write(html)
