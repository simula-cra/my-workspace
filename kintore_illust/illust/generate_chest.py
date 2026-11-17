import json,math,sys
src=open('/tmp/claude-0/gen2/fig6.py').read()
src=src[:src.index("S={}")]  # library only
exec(src)
def ik(sh,wr,l1,l2,sign=1):
    d=math.hypot(*sub(wr,sh)); d=min(d,l1+l2-0.01)
    a=(l1*l1-l2*l2+d*d)/(2*d); h=math.sqrt(max(l1*l1-a*a,0))
    u=norm(sub(wr,sh)); base=add(sh,mul(u,a)); n=(-u[1],u[0])
    return add(base,mul(n,h*sign))
def K(N,hip,sh,elb,wr,fing,knee,ank,heel,ball,toe,head,ht,bend=0.0):
    mid=add(mul(add(N,hip),0.5),(0,0))
    if bend: 
        u=norm(sub(hip,N)); n=(-u[1],u[0]); mid=add(mid,mul(n,bend))
    k=dict(N=N,hip=hip,sh=sh,elb=elb,wr=wr,fing=fing,knee=knee,ank=ank,heel=heel,ball=ball,toe=toe,head=head,ht=ht)
    k['torso']=[N,mid,hip]; k['hc_neck']=hpt(head,ht,-1.2,3.2); return k
WALLV='<line x1="56.5" y1="4" x2="56.5" y2="95.4" stroke="#8C8C8C" stroke-width="1.4"></line>'
S={}
# ---------- wall pushup (60x100) ----------
def wall(n):
    f=Fig(f'wp{n}'); f.raw(FLOOR_V); f.raw(WALLV)
    ank=(7,91.6); th=math.radians(24 if n==1 else 30); up=(math.sin(th),-math.cos(th))
    knee=add(ank,mul(up,19)); hip=add(knee,mul(up,19)); N=add(hip,mul(up,26))
    sh=add(N,(1.0,2.6)); head=add(N,mul(up,6.8)); head=(head[0]+0.6,head[1])
    wr=(53.6,37.5); fing=(54.6,31.5)
    elb=ik(sh,wr,13,12,1) if n==2 else mul(add(sh,wr),0.5)
    k=K(N,hip,sh,elb,wr,fing,knee,ank,(ank[0]-2.6,93.8),(ank[0]+4.5,94.4),(ank[0]+8,94.6),head,math.degrees(th)-4)
    fa=dict(elb=add(elb,(-1.5,1.2)),wr=add(wr,(-0.4,1.6)),fing=add(fing,(-0.4,1.6)))
    c1,a1=bone_pt(N,k['torso'][1],0.4,5.0); c2,a2=bone_pt(sh,elb,0.5,-1.4)
    f.plan_m(['torso'],[(c1[0],c1[1],4.8,2.4,a1)]); f.plan_m(['arm'],[(c2[0],c2[1],4.2,1.6,a2)])
    side_figure(f,k,far_arm=fa)
    return f.svg('0 0 60 100','壁腕立て '+('腕を伸ばす' if n==1 else '胸を壁に近づける'))
S['wall_pushup_1']=wall(1); S['wall_pushup_2']=wall(2)
# ---------- knee pushup (100x60) ----------
def kneep(n):
    f=Fig(f'kp{n}'); f.raw(FLOOR_H)
    knee=(30,51.5)
    if n==1: sh=(70,29)
    else: sh=(67,45.5)
    d=norm(sub(knee,sh)); L=math.hypot(*sub(knee,sh))
    N=add(sh,mul(d,-3.0)); N=(N[0],N[1]-0.8)
    hip=add(sh,mul(d,25)); # rest is thigh
    head=add(add(N,mul(d,-6.8)),(0.5,0.5)); ht=math.degrees(math.atan2(-d[1],-d[0]))+90
    ank=(14,46.5); heel=(12.2,44); ball=(10.5,48.5); toe=(8.5,49.5)
    if n==1: elb=(70,41); wr=(70,52.6); fing=(76.5,54.3)
    else: wr=(62,52.6); elb=(58.6,41.8); fing=(68.5,54.3)
    k=K(N,hip,sh,elb,wr,fing,knee,ank,heel,ball,toe,head,ht)
    fa=dict(elb=add(elb,(-2.4,0.4)),wr=add(wr,(-2.4,0)),fing=add(fing,(-2.4,0)))
    c1,a1=bone_pt(N,k['torso'][1],0.35,4.2); c2,a2=bone_pt(sh,elb,0.5,-1.3 if n==1 else 1.2)
    f.plan_m(['torso'],[(c1[0],c1[1],5,2.4,a1)]); f.plan_m(['arm'],[(c2[0],c2[1],4.2,1.6,a2)])
    side_figure(f,k,far_arm=fa)
    return f.svg('0 0 100 60','膝つき腕立て '+('上' if n==1 else '下'))
S['knee_pushup_1']=kneep(1); S['knee_pushup_2']=kneep(2)
# ---------- pike pushup (100x60) ----------
def pike(n):
    f=Fig(f'pk{n}'); f.raw(FLOOR_H)
    ank=(20,50.8); heel=(17.6,48.4); ball=(20.8,54); toe=(24.2,54.6)
    if n==1:
        hip=(41,13.5); sh=(62.5,30); wr=(64,52.6); elb=mul(add(sh,wr),0.5); fing=(70.5,54.3)
    else:
        hip=(43,17.5); sh=(68,41); wr=(62,52.6); elb=ik(sh,wr,10.5,12,-1); fing=(68.5,54.3)
    knee=mul(add(hip,ank),0.5); knee=(knee[0]+0.6,knee[1]-0.3)
    d=norm(sub(sh,hip)); N=add(sh,mul(d,2.6)); N=(N[0]-0.8,N[1]-0.6)
    head=add(N,mul(d,6.6)); ht=math.degrees(math.atan2(d[1],d[0]))-90
    head=(head[0]-1.2,head[1]+0.4)
    k=K(N,hip,sh,elb,wr,fing,knee,ank,heel,ball,toe,head,ht+180)
    k['torso']=[N,add(mul(add(N,hip),0.5),(0,0)),hip]
    fa=dict(elb=add(elb,(-2.4,0.4)),wr=add(wr,(-2.4,0)),fing=add(fing,(-2.4,0)))
    c2,a2=bone_pt(sh,elb,0.12,0.0)
    f.plan_m(['arm'],[(c2[0],c2[1],3.6,3.0,a2)])
    side_figure(f,k,far_arm=fa)
    return f.svg('0 0 100 60','パイクプッシュアップ '+('上' if n==1 else '頭を下ろす'))
S['pike_pushup_1']=pike(1); S['pike_pushup_2']=pike(2)
json.dump(S,open('/tmp/claude-0/gen7/b1.json','w'),ensure_ascii=False)
html='<style>div>svg{width:100%;height:100%;display:block}</style><body style="background:#1C1E1F;margin:16px">'
for nm in ['wall_pushup','knee_pushup','pike_pushup']:
    for s in (92,260): html+=f'<div style="display:flex;gap:12px;margin:8px"><div style="width:{s}px;height:{s}px;outline:1px dashed #333">{S[nm+"_1"]}</div><div style="width:{s}px;height:{s}px;outline:1px dashed #333">{S[nm+"_2"]}</div></div>'
open('/tmp/claude-0/gen7/p.html','w').write(html)
# ---------- wide / narrow (front view, slightly above) ----------
def front(n):
    f=Fig(f'wn{n}'); f.raw(FLOOR_H)
    # legs and torso recede upward (seen from front-above)
    for x0,x1 in ((46.5,47.5),(53.5,52.5)):
        f.part(limb([(x0,13),(x1,4.5)],[[(0,2.6,2.6),(1,1.6,1.6)]],0.4,0.8),True)
    tor=limb([(50,31),(50,13)],[[(0,10.5,10.5),(0.25,10,10),(0.7,6.5,6.5),(1,5.8,5.8)]],0.35,0.5)
    if n==1: hands=((20,53.2),(80,53.2)); elbs=((27.5,41.5),(72.5,41.5))
    else: hands=((43.5,53.2),(56.5,53.2)); elbs=((41,42.5),(59,42.5))
    shs=((40.5,31.5),(59.5,31.5))
    f.plan_m(['torso'],[(41,31.5,4.2,3.0,0),(59,31.5,4.2,3.0,0)] if n==1 else [])
    f.part(tor,name='torso')
    seam(f,(50,40),(50,22),(50,13),6.6,6.6)
    for i in (0,1):
        sh,el,hd=shs[i],elbs[i],hands[i]
        if n==2:
            c,a=bone_pt(sh,el,0.5,0); f.plan('arm',[(c[0],c[1],4.6,2.2,a)])
        f.part(limb([sh,el,hd],[[(0,3.0,3.0),(1,2.2,2.2)],[(0,2.1,2.1),(1,1.5,1.5)]],0.6,0.4),name='arm')
        f.pending.pop('arm',None)
        seam(f,sh,el,hd,2.1,2.1)
        dx=-3.4 if i==0 else 3.4
        f.part(cr([(hd[0]-2.6,hd[1]-0.6),(hd[0]+dx*0.2,hd[1]-1.8),(hd[0]+2.6,hd[1]-0.6),(hd[0]+2.2,hd[1]+1.2),(hd[0],hd[1]+1.6),(hd[0]-2.2,hd[1]+1.2)]))
    f.part(cr([(50+5.2*math.cos(t/16*2*math.pi),38.5+5.4*math.sin(t/16*2*math.pi)) for t in range(16)]),name='head')
    f.raw('<path d="M46.4 40.6 Q50 43 53.6 40.6" fill="none" stroke="#1E1E1E" stroke-width="0.5"></path>')
    return f.svg('0 0 100 60','腕立て伏せ 正面から '+('手幅ワイド' if n==1 else '手幅ナロー'))
S['pushup_wide_narrow_1']=front(1); S['pushup_wide_narrow_2']=front(2)
# ---------- diamond ----------
def diamond1():
    f=Fig('dm1')
    for sgn in (-1,1):
        f.part(limb([(50+sgn*33,63),(50+sgn*15,41)],[[(0,5.4,5.4),(1,4.0,4.0)]],0.3,0.6))  # forearm
    for sgn in (-1,1):
        palm=(50+sgn*12.5,37.5); tip=(50+sgn*1.0,21.5)
        f.part(limb([palm,tip],[[(0,4.6,4.6),(0.5,4.2,4.2),(1,2.4,2.4)]],0.6,0.9))  # palm+fingers
        u=norm(sub(tip,palm)); nn=(-u[1],u[0])
        for o in (-1.5,0.2,1.9):
            p0=add(add(palm,mul(sub(tip,palm),0.55)),mul(nn,o)); p1=add(add(palm,mul(sub(tip,palm),0.97)),mul(nn,o*0.55))
            f.raw(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}"></line>','seam')
        f.part(limb([(50+sgn*9.5,41.5),(50+sgn*1.0,42.8)],[[(0,2.0,2.0),(1,1.4,1.4)]],0.4,0.9))  # thumb
    return f.svg('0 0 100 60','ダイヤモンドプッシュアップ 手元を上から 親指と人差し指でひし形')
def diamond2():
    f=Fig('dm2'); f.raw(FLOOR_H)
    sh=(68,46); d=norm((-55,5)); hip=add(sh,mul(d,25)); knee=add(hip,mul(d,18)); ank=add(knee,mul(d,18))
    N=add(sh,mul(d,-3.2)); N=(N[0],N[1]-0.8); head=(77.4,45.0)
    elb=(55.5,43.6); wr=(64.5,52.6); fing=(71,54.3)
    k=K(N,hip,sh,elb,wr,fing,knee,ank,(ank[0]-1.6,ank[1]-3.4),(ank[0]+0.4,ank[1]+2.8),(ank[0]+3.4,54.2),head,86)
    c2,a2=bone_pt(sh,elb,0.5,1.3)
    f.plan_m(['arm'],[(c2[0],c2[1],5.0,1.8,a2)])
    side_figure(f,k,far_arm=dict(elb=(53.5,44.2),wr=(62.5,52.6),fing=(69,54.3)))
    return f.svg('0 0 100 60','ダイヤモンドプッシュアップ 肘を体に沿わせて下ろす')
S['diamond_pushup_1']=diamond1(); S['diamond_pushup_2']=diamond2()
json.dump(S,open('/tmp/claude-0/gen7/b1.json','w'),ensure_ascii=False)
html='<style>div>svg{width:100%;height:100%;display:block}</style><body style="background:#1C1E1F;margin:16px">'
for nm in ['wall_pushup','knee_pushup','pushup_wide_narrow','diamond_pushup','pike_pushup']:
    for s in (92,240): html+=f'<div style="display:flex;gap:12px;margin:6px"><div style="width:{s}px;height:{s}px;outline:1px dashed #333">{S[nm+"_1"]}</div><div style="width:{s}px;height:{s}px;outline:1px dashed #333">{S[nm+"_2"]}</div></div>'
open('/tmp/claude-0/gen7/p.html','w').write(html)
