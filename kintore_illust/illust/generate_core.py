import sys,math
sys.path.insert(0,'/home/user/my-workspace/kintore_illust/illust')
import figlib
from figlib import *
OKT='<text x="2" y="12" font-size="11" font-weight="bold" fill="#8FBC5A" font-family="sans-serif">OK</text>'
NGT='<text x="2" y="12" font-size="11" font-weight="bold" fill="#E0A458" font-family="sans-serif">NG</text>'
ARROW_UP=lambda x,y0,y1:f'<path d="M{x} {y0} L{x} {y1} M{x-1.4} {y1+1.8} L{x} {y1} L{x+1.4} {y1+1.8}" fill="none" stroke="#1E1E1E" stroke-width="0.6" opacity="0.8"></path>'
S={}
def with_head(fn,func):
    old=figlib.head
    figlib.head=fn
    import builtins
    g=func.__globals__; oh=g.get('head'); g['head']=fn
    try: return func()
    finally: figlib.head=old; g['head']=oh
# ---------- side plank (front view) ----------
def splank(kind):
    f=Fig(f'sp{kind}'); f.raw(FLOOR_H)
    sag = kind in ('ng','down')
    sh=(76,40.5); ankx,anky=15.5,50.6
    if sag: hip=(50,52.4) if kind=='down' else (50,50.2); knee=(32.5,52.2) if kind=='down' else (32.5,51.0)
    else:
        d=norm((ankx-sh[0],anky-sh[1])); hip=add(sh,mul(d,25.5)); knee=add(hip,mul(d,18))
    ank=(ankx,anky)
    d0=norm(sub(hip,sh)); N=add(sh,mul(d0,-3.2)); N=(N[0]+0.4,N[1]-1.2)
    head=add(N,mul(d0,-6.8)); head=(head[0],head[1]-1.0)
    k=K(N,hip,sh,(76.2,52.4),(83.5,53.4),(88,54),knee,ank,(ank[0]+1.6,ank[1]+1.6),(ank[0]-1.2,ank[1]+3.4),(ank[0]-4,ank[1]+3.8),head,0,bend=(2.2 if sag else 0))
    if kind!='ng':
        c,a=bone_pt(k['torso'][1],hip,0.15,0.5); f.plan('torso',[(c[0],c[1],6.5,2.8,a)])
    fa=dict(elb=(77,29.5),wr=(77.6,19),fing=(78,14.5))
    import figlib as L
    oldh=L.head
    globals()['head']=lambda c,t,s=1.0: ell_head(c,0,4.8,5.4); L.head=globals()['head']
    side_figure(f,k,far_arm=fa)
    L.head=oldh; globals()['head']=oldh
    if kind=='ng': f.raw(NGT)
    if kind=='ok': f.raw(OKT)
    if kind=='up': f.raw(ARROW_UP(44,54.6,49.8))
    return f.svg('0 0 100 60','サイドプランク '+{'ok':'良い例 一直線','ng':'悪い例 腰が落ちる','down':'腰を下ろす','up':'腰を持ち上げる'}[kind],ng=(kind=='ng'))

# ---------- cross mountain climber (side) ----------
def xclimb(n):
    f=Fig(f'xc{n}'); f.raw(FLOOR_H)
    sh=(70,29); d=norm((-57,22)); hip=add(sh,mul(d,25)); knee=add(hip,mul(d,18)); ank=add(knee,mul(d,18))
    N=add(sh,mul(d,-3.2)); N=(N[0],N[1]-0.6); head=add(add(N,mul(d,-6.6)),(0.6,0.6))
    k=K(N,hip,sh,(70,41),(70,52.6),(76.5,54.3),knee,ank,(ank[0]-2,ank[1]-3),(ank[0]+0.3,ank[1]+3.4),(ank[0]+3.2,54.2),head,69)
    c,a=bone_pt(k['torso'][1],hip,0.25,2.5); f.plan('torso',[(c[0],c[1],7,3.0,a)])
    fl=None
    if n==2: fl=dict(knee=(66,46.5),ank=(52,52),heel=(50,51),ball=(53,54.3),toe=(56,54.6))
    else: fl=dict(knee=add(knee,(0.4,-0.6)),ank=add(ank,(0.6,-0.4)),heel=(ank[0]-1.4,ank[1]-3.4),ball=(ank[0]+0.9,ank[1]+3.0),toe=(ank[0]+3.8,54.0))
    side_figure(f,k,far_arm=dict(elb=(67.5,41),wr=(67.5,52.6),fing=(74,54.3)),far_leg=fl)
    return f.svg('0 0 100 60','クロスマウンテンクライマー '+('プランク' if n==1 else '膝を対角の肘へ'))
# ---------- bicycle crunch (side, lying on back, head right) ----------
def bicycle(n):
    f=Fig(f'bc{n}'); f.raw(FLOOR_H)
    hip=(44,50.6); N=(67,42); u=norm(sub(N,hip)); head=add(N,mul(u,6.6)); head=(head[0]-0.4,head[1]-1.4)
    face=(u[1],-u[0]); th=math.degrees(math.atan2(face[1],face[0]))
    sh=add(N,(-1.0,2.2)); mid=mul(add(N,hip),0.5); tor=[N,mid,hip]
    pulled=dict(knee=(53.5,36.5),ank=(38.5,33.5)); ext=dict(knee=(27,47.6),ank=(11,44.2))
    def foot(a,pull):
        return dict(heel=(a[0]+1.2,a[1]+1.6),ball=(a[0]-2.4,a[1]-0.8),toe=(a[0]-4.2,a[1]-2.2))
    near,far=(pulled,ext) if n==1 else (ext,pulled)
    nf=foot(near['ank'],0); ff=foot(far['ank'],0)
    c,a=bone_pt(N,hip,0.62,0.0); f.plan('torso',[(c[0],c[1],6.5,2.8,a)])
    # far side (gray)
    f.part(limb([ff['heel'],ff['ball'],ff['toe']],FOOT,1,0.8),True); f.part(limb([hip,far['knee'],far['ank']],LEG),True)
    seam(f,hip,far['knee'],far['ank'],2.9,3.3,True)
    f.part(limb([sh,(62.5,31.5),(71.5,35.5)],ARM),True)
    # neck/head/torso
    f.part(limb([hpt(head,th,-1.2,-3.2) if False else add(head,mul(u,-3.0)),N],NECK))
    f.part(head_m(head,th),name='head')
    f.part(limb(tor,TORSO,0.5,0.7),name='torso'); seam(f,tor[0],tor[1],tor[2],4.3,5.6)
    # near leg on top
    f.part(limb([nf['heel'],nf['ball'],nf['toe']],FOOT,1,0.8))
    f.part(limb([hip,near['knee'],near['ank']],LEG,0.4,0.6),name='leg')
    seam(f,tor[1],hip,near['knee'],3.9,3.9,shift=2.6); seam(f,hip,near['knee'],near['ank'],2.7,2.9)
    # near arm: elbow toward the pulled (opposite) knee
    elb=(58.5,36.8) if n==1 else (60,33.5)
    f.part(limb([sh,elb,(72.5,37.2)],ARM,0.6,0.5),name='arm'); seam(f,sh,elb,(72.5,37.2),1.9,1.9)
    return f.svg('0 0 100 60','バイシクルクランチ '+('右肘と左膝を近づける' if n==1 else '左肘と右膝を近づける'))
# ---------- russian twist (front view, seated) ----------
def rtwist(n):
    f=Fig(f'rt{n}'); f.raw(FLOOR_H)
    sg=-1 if n==1 else 1   # n==1: hands to viewer's left (person's right)
    # legs: thighs come toward viewer (short), shins down to feet slightly lifted
    for x0,kx,fx in ((45.5,41,40.5),(54.5,59,59.5)):
        f.part(limb([(x0,49.5),(kx,45.5),(fx,52.5)],[[(0,4.2,4.2),(1,3.2,3.2)],[(0,2.8,2.8),(1,1.8,1.8)]],0.5,0.6))
        seam(f,(x0,49.5),(kx,45.5),(fx,52.5),3.0,3.0)
        f.part(cr([(fx-2.0,52.4),(fx,51.6),(fx+2.0,52.4),(fx+1.6,54.4),(fx-1.6,54.4)]))
    top=(50+sg*5.5,25.5)
    tor=limb([(50,49),(50+sg*2.5,38),top],[[(0,8.0,8.0),(1,7.2,7.2)],[(0,7.2,7.2),(0.7,9.6,9.6),(1,9.0,9.0)]],0.4,0.4)
    f.plan('torso',[(50+sg*6.2,40.5,2.6,6.0,sg*-12),(50-sg*5.2,40.5,2.2,5.0,sg*-12)])
    f.part(tor,name='torso'); seam(f,(50,49),(50+sg*2.5,38),top,7.4,7.4)
    hd=(top[0]+sg*1.5,top[1]-6.6)
    hands=(50+sg*20,41.5)
    sh_far=(top[0]-sg*8.0,top[1]+1.8); sh_near=(top[0]+sg*8.0,top[1]+1.8)
    f.part(cr([(hd[0]+5.0*math.cos(t/16*2*math.pi),hd[1]+5.4*math.sin(t/16*2*math.pi)) for t in range(16)]),name='head')
    for shp,el in ((sh_near,(hands[0]-sg*3.5,35.5)),(sh_far,(50+sg*8,39.5))):
        f.part(limb([shp,el,hands],[[(0,2.8,2.8),(1,2.1,2.1)],[(0,2.0,2.0),(1,1.5,1.5)]],0.6,0.4))
        seam(f,shp,el,hands,2.0,2.0)
    f.part(cr([(hands[0]+2.6*math.cos(t/12*2*math.pi),hands[1]+2.2*math.sin(t/12*2*math.pi)) for t in range(12)]))
    return f.svg('0 0 100 60','ロシアンツイスト 正面から '+('両手を右へ' if n==1 else '両手を左へ'))
# ---------- heel touch crunch (top view, lying on back) ----------
def heeltouch(n):
    f=Fig(f'ht{n}')
    sg=1 if n==1 else -1   # n==1: reach to the lower side of the image
    hipc=(60,30)
    N=(32,30+sg*6.0); mid=(47,30+sg*3.6)
    for yy,kk in ((26,23.5),(34,36.5)):
        knee=(71,kk); foot=(79,yy+(-1.2 if yy<30 else 1.2))
        f.part(limb([(60,yy),knee,foot],[[(0,4.0,4.0),(1,3.2,3.2)],[(0,2.6,2.6),(1,1.8,1.8)]],0.4,0.6))
        seam(f,(60,yy),knee,foot,3.2,3.2)
        f.part(cr([(foot[0]-1.0,foot[1]-2.0),(foot[0]+4.6,foot[1]-1.6),(foot[0]+5.2,foot[1]),(foot[0]+4.6,foot[1]+1.6),(foot[0]-1.0,foot[1]+2.0)]))
    tor=limb([N,mid,hipc],[[(0,8.6,8.6),(0.3,8.0,8.0),(1,6.0,6.0)],[(0,6.0,6.0),(0.7,6.8,6.8),(1,6.4,6.4)]],0.3,0.5)
    c=(47,30+sg*6.0); f.plan('torso',[(c[0],c[1],6.0,2.0,-sg*8)])
    f.part(tor,name='torso'); seam(f,N,mid,hipc,6.4,6.4)
    hd=(N[0]-8.0,N[1]+sg*1.0)
    f.part(limb([(N[0]-2,N[1]),(N[0]-5,N[1])],[[(0,2.4,2.4),(1,2.4,2.4)]],0.3,0.3))
    f.part(cr([(hd[0]+5.2*math.cos(t/16*2*math.pi),hd[1]+4.6*math.sin(t/16*2*math.pi)) for t in range(16)]),name='head')
    # reaching arm (toward heel on side sg) and the other arm
    shr=(N[0]+1.5,N[1]+sg*8.0); shl=(N[0]+1.5,N[1]-sg*8.0)
    heel=(77,30+sg*8.5)
    f.part(limb([shr,(52,shr[1]+sg*2.2),(70,heel[1]+sg*0.6)],[[(0,2.8,2.8),(1,2.1,2.1)],[(0,2.0,2.0),(1,1.4,1.4)]],0.6,0.6),name='arm')
    seam(f,shr,(52,shr[1]+sg*2.2),(70,heel[1]+sg*0.6),2.0,2.0)
    f.part(limb([shl,(46,shl[1]-sg*1.0),(57,shl[1]-sg*0.4)],[[(0,2.8,2.8),(1,2.1,2.1)],[(0,2.0,2.0),(1,1.4,1.4)]],0.6,0.6))
    seam(f,shl,(46,shl[1]-sg*1.0),(57,shl[1]-sg*0.4),2.0,2.0)
    return f.svg('0 0 100 60','ヒールタッチクランチ 真上から '+('右手で右かかとをタッチ' if n==1 else '左手で左かかとをタッチ'))
