import math, json
INK='#1E1E1E'; FAR='#9A9A9A'; SW=0.75
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(a,k): return (a[0]*k,a[1]*k)
def norm(a):
    L=math.hypot(*a) or 1; return (a[0]/L,a[1]/L)
def cr(pts,closed=True):
    n=len(pts); P=lambda i: pts[i%n] if closed else pts[max(0,min(n-1,i))]
    d=f'M{pts[0][0]:.2f} {pts[0][1]:.2f}'
    for i in range(n if closed else n-1):
        p0,p1,p2,p3=P(i-1),P(i),P(i+1),P(i+2)
        c1=add(p1,mul(sub(p2,p0),1/6)); c2=sub(p2,mul(sub(p3,p1),1/6))
        d+=f' C{c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {p2[0]:.2f} {p2[1]:.2f}'
    return d+('Z' if closed else '')
def limb(joints,keys,cap0=0.6,cap1=0.6,step=1.2):
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
class Fig:
    def __init__(s,uid): s.uid=uid; s.out=[]; s.defs=[]; s.n=0; s.clips={}
    pending={}
    def part(s,d,far=False,name=None):
        s.out.append(P(d,FAR if far else INK,'#F4F4F4' if far else '#FFFFFF'))
        if name and name in s.pending:
            s.n+=1; cid=f'{s.uid}c{s.n}'
            s.defs.append(f'<clipPath id="{cid}"><path d="{d}"></path></clipPath>')
            s.out.append(f'<g clip-path="url(#{cid})">'+''.join(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx}" ry="{ry}" transform="rotate({a:.0f} {x:.1f} {y:.1f})" fill="#BDBDBD"></ellipse>' for x,y,rx,ry,a in s.pending[name])+'</g>')
            s.out.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{SW}"></path>')
    def plan(s,name,ells): s.pending=dict(s.pending); s.pending.setdefault(name,[]); s.pending[name]=s.pending[name]+ells
    def muscle(s,names,ells):
        s.n+=1; cid=f'{s.uid}c{s.n}'
        s.defs.append(f'<clipPath id="{cid}">'+''.join(f'<path d="{d}"></path>' for nm in names for d in s.clips[nm])+'</clipPath>')
        s.out.append(f'<g clip-path="url(#{cid})">'+''.join(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx}" ry="{ry}" transform="rotate({a:.0f} {x:.1f} {y:.1f})" fill="#BDBDBD"></ellipse>' for x,y,rx,ry,a in ells)+'</g>')
        # redraw outlines of those parts on top for crispness
        s.out.append(''.join(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{SW}"></path>' for nm in names for d in s.clips[nm]))
    def plan_m(s,names,ells):
        s.plan(names[0],ells)
    def raw(s,x): s.out.append(x)
    def svg(s,vb,label): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{label}" style="width:100%;height:100%;display:block"><defs>{"".join(s.defs)}</defs>{"".join(s.out)}</svg>'
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
    f.raw(f'<line x1="{p[0]:.2f}" y1="{p[1]:.2f}" x2="{q[0]:.2f}" y2="{q[1]:.2f}" stroke="{FAR if far else INK}" stroke-width="0.55" stroke-linecap="round"></line>')
def side_figure(f,k,far_arm=None,far_leg=None,order='arm_front'):
    if far_leg: f.part(limb([far_leg['heel'],far_leg['ball'],far_leg['toe']],FOOT,1,0.8),True); f.part(limb([k['hip'],far_leg['knee'],far_leg['ank']],LEG),True)
    if far_arm: f.part(limb([k['sh'],far_arm['elb'],far_arm['wr']],ARM),True); f.part(limb([far_arm['wr'],far_arm['fing']],HAND,0.5,0.9),True)
    f.part(limb([k['hc_neck'],k['N']],NECK),name='neck')
    f.part(head(k['head'],k['ht'],k.get('hs',1)),name='head')
    f.part(limb([k['heel'],k['ball'],k['toe']],FOOT,1,0.8),name='foot')
    f.part(limb([k['hip'],k['knee'],k['ank']],LEG,0.4,0.6),name='leg')
    f.part(limb(k['torso'],TORSO,0.5,0.7),name='torso')
    f.part(limb([k['sh'],k['elb'],k['wr']],ARM,0.6,0.5),name='arm')
    f.part(limb([k['wr'],k['fing']],HAND,0.5,0.9),name='hand')
    tor=k['torso']
    if far_leg: seam(f,k['hip'],far_leg['knee'],far_leg['ank'],2.9,3.3,True)
    if far_arm: seam(f,k['sh'],far_arm['elb'],far_arm['wr'],2.0,1.9,True)
    seam(f,tor[0],tor[1],tor[2],4.3,5.6)
    seam(f,tor[1],k['hip'],k['knee'],3.9,3.9,shift=2.6)
    seam(f,k['hip'],k['knee'],k['ank'],2.7,2.9)
    seam(f,k['knee'],k['ank'],k['toe'],1.5,1.5)
    seam(f,tor[0],k['sh'],k['elb'],3.0,3.1,shift=1.6)
    seam(f,k['sh'],k['elb'],k['wr'],1.9,1.9)
    seam(f,k['elb'],k['wr'],k['fing'],1.3,1.4)
S={}
# ---- pushup 1
f=Fig('pu1'); f.raw(FLOOR_H)
sh=(70,29); d=norm((-57,22)); hip=add(sh,mul(d,25)); knee=add(hip,mul(d,18)); ank=add(knee,mul(d,18))
N=add(sh,mul(d,-3.2)); N=(N[0],N[1]-0.6); hc=add(N,mul(d,-6.6)); hc=(hc[0]+0.6,hc[1]+0.6); ht=69
k=dict(sh=sh,elb=(70,41),wr=(70,52.6),fing=(77.5,54.4),hip=hip,knee=knee,ank=ank,heel=(ank[0]-2.2,ank[1]-3),ball=(ank[0]+0.3,ank[1]+3.4),toe=(ank[0]+3.6,54.3),
 N=N,torso=[N,add(N,mul(d,13)),hip],head=hc,ht=ht,hc_neck=hpt(hc,ht,-1.2,3.2))
c1,a1=bone_pt(N,add(N,mul(d,13)),0.45,4.0); c2,a2=bone_pt(sh,(70,41),0.42,-1.3)
f.plan_m(['torso'],[(c1[0],c1[1],5.5,2.6,a1)]); f.plan_m(['arm'],[(c2[0],c2[1],4.6,1.8,a2)])
side_figure(f,k,far_arm=dict(elb=(67.5,41),wr=(67.5,52.6),fing=(74.5,54.4)))
S['pushup_1']=f.svg('0 0 100 60','腕立て伏せ 上の姿勢')
# ---- pushup 2
f=Fig('pu2'); f.raw(FLOOR_H)
sh=(68,46); d=norm((-55,5)); hip=add(sh,mul(d,25)); knee=add(hip,mul(d,18)); ank=add(knee,mul(d,18))
N=add(sh,mul(d,-3.2)); N=(N[0],N[1]-0.8); hc=add(N,mul(d,-6.6)); hc=(hc[0]+0.4,hc[1]+0.2); ht=86
k=dict(sh=sh,elb=(59.4,42),wr=(62,52.6),fing=(69.5,54.4),hip=hip,knee=knee,ank=ank,heel=(ank[0]-1.6,ank[1]-3.4),ball=(ank[0]+0.4,ank[1]+2.8),toe=(ank[0]+3.6,54.3),
 N=N,torso=[N,add(N,mul(d,13)),hip],head=hc,ht=ht,hc_neck=hpt(hc,ht,-1.2,3.2))
c1,a1=bone_pt(N,add(N,mul(d,13)),0.45,4.2); c2,a2=bone_pt(sh,(59.4,42),0.5,1.2)
f.plan_m(['torso'],[(c1[0],c1[1],5.5,2.6,a1)]); f.plan_m(['arm'],[(c2[0],c2[1],4.2,1.7,a2)])
side_figure(f,k,far_arm=dict(elb=(57,42.5),wr=(59.5,52.6),fing=(67,54.4)))
S['pushup_2']=f.svg('0 0 100 60','腕立て伏せ 下の姿勢')
# ---- squat OK
OKT='<text x="2" y="12" font-size="11" font-weight="bold" fill="#1E1E1E" font-family="sans-serif">OK</text>'
NGT='<text x="2" y="12" font-size="11" font-weight="bold" fill="#1E1E1E" font-family="sans-serif">NG</text>'
f=Fig('sq1'); f.raw(FLOOR_V); f.raw(OKT)
hip=(20.5,70.5); ax=norm((0.643,-0.766)); N=add(hip,mul(ax,28)); mid=add(hip,mul(ax,14))
hc=add(N,mul(ax,6.8)); ht=18
k=dict(sh=add(N,(1.2,2.6)),elb=(44,62),wr=(49.5,53.5),fing=(52,47.5),hip=hip,knee=(40,72.6),ank=(31,90.6),heel=(27.6,92.6),ball=(36.5,94.1),toe=(40.5,94.6),
 N=N,torso=[N,mid,hip],head=hc,ht=ht,hc_neck=hpt(hc,ht,-1.2,3.2))
c1,a1=bone_pt(hip,(40,72.6),0.55,3.0); c2,a2=bone_pt(N,mid,0.0,0)
g,ga=bone_pt(mid,hip,0.9,-4.2)
f.plan_m(['leg'],[(c1[0],c1[1],7.5,2.4,a1)]); f.plan_m(['torso','leg'],[(g[0],g[1],4.2,3.6,ga)])
side_figure(f,k,far_arm=dict(elb=(42,63),wr=(48,54.5),fing=(50.5,48.5)),far_leg=dict(knee=(37.5,73.5),ank=(28.5,90.6),heel=(25.2,92.6),ball=(34,94.1),toe=(38,94.6)))
S['squat_1']=f.svg('0 0 60 100','スクワット 良い例')
# ---- squat NG
f=Fig('sq2'); f.raw(FLOOR_V); f.raw(NGT)
f.raw('<line x1="40.5" y1="62" x2="40.5" y2="94.6" stroke="#6E6E6E" stroke-width="0.7" stroke-dasharray="1.6 1.4"></line>')
hip=(24,71); N=(32.5,47.5); mid=(23,58.5); hc=(39.5,47.5); ht=58
k=dict(sh=(33.5,50.5),elb=(36,62),wr=(40.5,71),fing=(42.5,77),hip=hip,knee=(44.5,77.5),ank=(29.5,90.6),heel=(26,92.6),ball=(36.5,94.1),toe=(40.5,94.6),
 N=N,torso=[N,mid,hip],head=hc,ht=ht,hc_neck=hpt(hc,ht,-1.2,3.2))
side_figure(f,k,far_arm=dict(elb=(34,62.5),wr=(38,71.5),fing=(40,77.5)),far_leg=dict(knee=(42,78.5),ank=(27,90.6),heel=(23.6,92.6),ball=(34,94.1),toe=(38,94.6)))
S['squat_2']=f.svg('0 0 60 100','スクワット 悪い例 膝がつま先より前に出て背中が丸い')
# ---- prone Y (top view)
TT=[[(0,3.2,3.2),(0.1,8.6,8.6),(0.32,8.0,8.0),(0.62,6.0,6.0),(0.85,6.9,6.9),(1,6.0,6.0)]]
LT=[[(0,3.6,3.6),(0.6,3.0,3.0),(1,2.3,2.3)],[(0,2.3,2.3),(0.3,2.6,2.6),(1,1.5,1.5)]]
AT=[[(0,2.8,2.8),(0.5,2.4,2.4),(1,1.8,1.8)],[(0,1.8,1.8),(0.3,2.0,2.0),(1,1.3,1.3)]]
HT=[[(0,1.3,1.3),(0.5,1.7,1.7),(1,1.0,1.0)]]
def prone(n):
    f=Fig(f'py{n}')
    if n==1: arms=[((31,23),(18,19.5),(8,17),(3,15.8)),((31,37),(18,40.5),(8,43),(3,44.2))]
    else: arms=[((31,23),(22.5,13.5),(15,6.5),(11.5,3)),((31,37),(22.5,46.5),(15,53.5),(11.5,57))]
    if n==2:
        for a in arms:
            sh=[add(p,(3.5,3.5)) for p in a]
            f.raw(f'<path d="{limb(list(sh[:3]),AT)}" fill="#D9D9D9"></path><path d="{limb([sh[2],sh[3]],HT,0.5,0.9)}" fill="#D9D9D9"></path>')
    f.plan_m(['torso'],[(46.5,26.2,6.5,2.2,27),(46.5,33.8,6.5,2.2,-27)])
    for y0,y1,y2 in ((27,26.6,26.2),(33,33.4,33.8)):
        f.part(limb([(92,y2),(97.5,y2)],[[(0,1.4,1.4),(1,1.0,1.0)]],0.6,0.9))
        f.part(limb([(63,y0),(79,y1),(92.5,y2)],LT,0.4,0.6))
    for a in arms:
        f.part(limb(list(a[:3]),AT,0.6,0.5),name='arm'); f.part(limb([a[2],a[3]],HT,0.5,0.9))
    f.part(limb([(26,30),(66,30)],TT,0.4,0.6),name='torso')
    f.part(limb([(19,30),(29,30)],[[(0,2.0,2.0),(1,2.6,2.6)]],0.3,0.3))
    f.part(cr([(21+5*math.cos(a/16*2*math.pi)*(1.05 if math.cos(a/16*2*math.pi)<0 else 0.95),30+4.3*math.sin(a/16*2*math.pi)) for a in range(16)]),name='head')
    f.raw(f'<path d="M30 30 L60 30" stroke="#8C8C8C" stroke-width="0.5"></path>')
    f.raw(f'<path d="M31 30 L60 30" stroke="#6E6E6E" stroke-width="0.5"></path>')
    for y0,y1,y2 in ((27,26.6,26.2),(33,33.4,33.8)):
        seam(f,(55,y0),(63.5,y0),(79,y1),3.4,3.4); seam(f,(63,y0),(79,y1),(92,y2),2.6,2.6); seam(f,(79,y1),(92,y2),(97,y2),1.5,1.5)
    seam(f,(30,30),(48,30),(66,30),6.0,6.0)
    for a_ in arms:
        seam(f,(40,30),a_[0],a_[1],2.8,2.8,shift=2.0); seam(f,a_[0],a_[1],a_[2],2.0,2.0); seam(f,a_[1],a_[2],a_[3],1.3,1.3)
    top=f.svg('0 0 100 60','x')
    top=top[top.index('>')+1:top.rindex('</svg>')]
    g=Fig(f'pys{n}')
    k=dict(N=(66.5,90.4),hip=(41,91.2),knee=(24,92.6),ank=(8,93.8),heel=(8.4,91.0),ball=(4.4,95.4),toe=(1.2,96.4),
           head=(77,91.2),ht=95,sh=(67.5,92.4))
    k['torso']=[k['N'],(53.5,90.6),k['hip']]; k['hc_neck']=hpt(k['head'],k['ht'],-1.2,3.2)
    if n==1: k.update(elb=(81,94.6),wr=(92.5,95.4),fing=(98.8,96.4))
    else: k.update(elb=(80.6,88.8),wr=(91.6,85.2),fing=(98,83.4))
    c1,a1=bone_pt(k['N'],(53.5,90.6),0.65,3.4)
    g.plan_m(['torso'],[(c1[0],c1[1],4.5,2.2,a1)])
    side_figure(g,k)
    if n==2: g.raw('<path d="M94.5 92.4 L94.5 88" stroke="#1E1E1E" stroke-width="0.6" opacity="0.7"></path><path d="M93.2 89.4 L94.5 87.6 L95.8 89.4" fill="none" stroke="#1E1E1E" stroke-width="0.6" opacity="0.7"></path>')
    sv=g.svg('0 0 100 60','x'); sv=sv[sv.index('>')+1:sv.rindex('</svg>')]
    inner=f'<g transform="translate(4 0) scale(0.92)">{top}</g><line x1="2" y1="57.5" x2="98" y2="57.5" stroke="#D0D0D0" stroke-width="0.5" stroke-dasharray="2 2"></line><line x1="2" y1="97.4" x2="98" y2="97.4" stroke="#8C8C8C" stroke-width="0.8"></line><g transform="translate(100 0) scale(-1 1)">{sv}</g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="プローンYレイズ 上から見た図と横から見た図 '+('腕を下ろす' if n==1 else '腕をY字に浮かす')+f'" style="width:100%;height:100%;display:block">{inner}</svg>'
S['prone_y_raise_1']=prone(1); S['prone_y_raise_2']=prone(2)
json.dump(S,open('/tmp/claude-0/gen2/svgs4.json','w'),ensure_ascii=False)
html='<body style="background:#fff;margin:16px">'
for nm in ['pushup','squat','prone_y_raise']:
    for s in (92,300): html+=f'<div style="display:flex;gap:12px;margin:8px"><div style="width:{s}px;height:{s}px;outline:1px dashed #ccc">{S[nm+"_1"]}</div><div style="width:{s}px;height:{s}px;outline:1px dashed #ccc">{S[nm+"_2"]}</div></div>'
open('/tmp/claude-0/gen2/p4.html','w').write(html)
