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
# ---------- plank (forearms, side) ----------
def plank(kind):
    f=Fig(f'pl{kind}'); f.raw(FLOOR_H)
    sh=(70,40.5); ank=(13,50.8)
    if kind=='ng':
        hip=(44,49.6); knee=(28,50.6)
    else:
        d=norm(sub(ank,sh)); hip=add(sh,mul(d,25)); knee=add(hip,mul(d,18))
    d0=norm(sub(hip,sh)); N=add(sh,mul(d0,-3.2)); N=(N[0],N[1]-0.8)
    head=add(add(N,mul(d0,-6.6)),(0.6,0.8))
    k=K(N,hip,sh,(70,53.2),(80,53.4),(85,54),knee,ank,(ank[0]-2,ank[1]-3),(ank[0]+0.3,ank[1]+3.4),(ank[0]+3.2,54.2),head,math.degrees(math.atan2(-d0[1],-d0[0]))+90,bend=(2.4 if kind=='ng' else 0))
    if kind!='ng':
        c,a=bone_pt(k['torso'][1],hip,0.15,4.0); f.plan('torso',[(c[0],c[1],7,2.8,a)])
    side_figure(f,k,far_arm=dict(elb=(67.6,53.2),wr=(77.6,53.4),fing=(82.6,54)))
    f.raw(OKT if kind=='ok' else NGT)
    return f.svg('0 0 100 60','プランク '+('良い例 一直線' if kind=='ok' else '悪い例 腰が落ちて反る'),ng=(kind=='ng'))
# ---------- mountain climber (side) ----------
def mclimb(n):
    f=Fig(f'mc{n}'); f.raw(FLOOR_H)
    sh=(70,29); d=norm((-57,22)); hip=add(sh,mul(d,25)); knee=add(hip,mul(d,18)); ank=add(knee,mul(d,18))
    N=add(sh,mul(d,-3.2)); N=(N[0],N[1]-0.6); head=add(add(N,mul(d,-6.6)),(0.6,0.6))
    far=dict(knee=add(knee,(0.4,-0.6)),ank=add(ank,(0.6,-0.4)),heel=(ank[0]-1.4,ank[1]-3.4),ball=(ank[0]+0.9,ank[1]+3.0),toe=(ank[0]+3.8,54.0))
    if n==2:
        knee=(60,39.5); ank=(46,47); heel=(44,45.5); ball=(47.5,50.6); toe=(50.5,51.6)
    else:
        heel=(ank[0]-2,ank[1]-3); ball=(ank[0]+0.3,ank[1]+3.4); toe=(ank[0]+3.2,54.2)
    k=K(N,hip,sh,(70,41),(70,52.6),(76.5,54.3),knee,ank,heel,ball,toe,head,69)
    c,a=bone_pt(k['torso'][1],hip,0.3,4.0); f.plan('torso',[(c[0],c[1],7,2.8,a)])
    side_figure(f,k,far_arm=dict(elb=(67.5,41),wr=(67.5,52.6),fing=(74,54.3)),far_leg=far)
    return f.svg('0 0 100 60','マウンテンクライマー '+('プランク' if n==1 else '膝を胸へ'))
# ---------- crunch (side, lying on back, head right, knees up) ----------
def lying(n,kind):
    f=Fig(f'{kind}{n}'); f.raw(FLOOR_H)
    if kind=='cr':
        hip=(42,51.2); N=(64,48.5) if n==1 else (63,42.5)
    else:  # leg raise: torso flat
        hip=(46,51.2); N=(70,50.6)
    u=norm(sub(N,hip)); head=add(N,mul(u,6.6)); head=(head[0],head[1]-1.0 if (kind=='cr' and n==2) else head[1]-0.6)
    face=(u[1],-u[0]); th=math.degrees(math.atan2(face[1],face[0]))
    sh=add(N,(-1.0,2.0))
    if kind=='cr':
        knee=(30,38.5); ank=(19,51.6); ft=dict(heel=(18,53),ball=(22,54.2),toe=(25.5,54.6))
        elb=(60,39) if n==2 else (61,45.5); wr=(70,40) if n==2 else (72,47.5)
        farleg=dict(knee=(31.5,38.8),ank=(20.5,51.6),heel=(19.5,53),ball=(23.5,54.2),toe=(27,54.6))
    else:
        if n==1: knee=(28,49.8); ank=(11,48.6); ft=dict(heel=(10,50.4),ball=(8.5,46.6),toe=(7.6,44.2))
        else: knee=(44.5,33); ank=(43.5,16); ft=dict(heel=(45.2,15.5),ball=(42,13.5),toe=(39.8,12.4))
        elb=(58,53.4); wr=(48,54); farleg=None
    tor=[N,mul(add(N,hip),0.5),hip]
    k=dict(N=N,hip=hip,sh=sh,elb=elb,wr=wr,fing=add(wr,(-4.5,0.3)),knee=knee,ank=ank,head=head,ht=th,torso=tor,hc_neck=add(head,mul(u,-3.2)),**ft)
    c,a=bone_pt(N,hip,0.55 if kind=='cr' else 0.82,0.0)
    f.plan('torso',[(c[0],c[1],6.0,2.8,a)])
    import figlib as L
    oldh=L.head; globals()['head']=lambda c,t,s=1.0: head_m(c,t,s); L.head=globals()['head']
    side_figure(f,k,far_leg=farleg,far_arm=dict(elb=add(elb,(-2,0.2)),wr=add(wr,(-2,0)),fing=add(add(wr,(-4.5,0.3)),(-2,0))))
    L.head=oldh; globals()['head']=oldh
    if kind=='lr' and n==2: f.raw(ARROW_UP(30,46,36))
    nm={'cr':('クランチ',('寝た姿勢','肩甲骨を浮かせる')),'lr':('レッグレイズ',('脚を床すれすれまで下ろす','脚を垂直まで上げる'))}[kind]
    return f.svg('0 0 100 60',nm[0]+' '+nm[1][n-1])
# ---------- prone (head right): superman / back extension ----------
def prone_side(n,kind):
    f=Fig(f'{kind}{n}'); f.raw(FLOOR_H)
    hip=(41,49.6); N=(66.5,48.6); sh=(67.5,50.6); head=(77,49.4); ht=95
    knee=(24,50.8); ank=(8,52); ft=dict(heel=(8.4,49.4),ball=(4.4,53.6),toe=(1.2,54.6))
    if kind=='sm':
        elb,wr,fing=(81,53.2),(92.5,53.8),(98.6,54.4)
        if n==2:
            N=(66,45.6); sh=(67,47.6); head=(76.5,44.6); ht=82
            elb,wr,fing=(80,43.6),(91,41.2),(97,40.2)
            knee=(24,48.6); ank=(8.5,45.6); ft=dict(heel=(8.8,43.2),ball=(4.6,47.4),toe=(1.6,48.2))
    else:
        if n==2: N=(65.5,42); sh=(66.5,44.2); head=(75,38.8); ht=70
        elb=add(sh,(6.5,-5.5 if n==1 else -6.8)); wr=add(head,(-3.6,-3.6)); fing=add(head,(-1.2,-5.6))
    tor=[N,mul(add(N,hip),0.5),hip]
    k=dict(N=N,hip=hip,sh=sh,elb=elb,wr=wr,fing=fing,knee=knee,ank=ank,head=head,ht=ht,torso=tor,hc_neck=hpt(head,ht,-1.2,3.2),**ft)
    c,a=bone_pt(tor[1],hip,0.55,3.6); f.plan('torso',[(c[0],c[1],6.0,2.4,a)])
    side_figure(f,k)
    lab={'sm':('スーパーマン',('うつ伏せで手足を伸ばす','手足を同時に浮かす')),'be':('バックエクステンション',('うつ伏せ','上体を起こす'))}[kind]
    return f.svg('0 0 100 60',lab[0]+' '+lab[1][n-1])
# ---------- high reverse plank (supine, head right) ----------
def hrplank(kind):
    f=Fig(f'hr{kind}'); f.raw(FLOOR_H)
    sh=(76,31.5); ank=(15,50.2)
    if kind=='ng': hip=(46,47.5); knee=(30,49.2)
    else:
        d=norm(sub(ank,sh)); hip=add(sh,mul(d,25)); knee=add(hip,mul(d,18))
    d0=norm(sub(hip,sh)); u=mul(d0,-1)
    N=add(sh,mul(d0,-3.0)); N=(N[0],N[1]-0.4)
    head=add(N,mul(u,6.6)); face=(u[1],-u[0]); th=math.degrees(math.atan2(face[1],face[0]))
    k=dict(N=N,hip=hip,sh=sh,elb=(76.6,42.4),wr=(77,53.2),fing=(71.5,54.4),knee=knee,ank=ank,heel=(14,53.4),ball=(17.6,48.6),toe=(18.6,46),head=head,ht=th,
           torso=[N,mul(add(N,hip),0.5) if kind!='ng' else add(mul(add(N,hip),0.5),(0,2.2)),hip],hc_neck=add(head,mul(u,-3.2)))
    if kind!='ng':
        c,a=bone_pt(k['torso'][1],hip,0.75,-3.8); f.plan('torso',[(c[0],c[1],6.5,2.4,a)])
    import figlib as L
    oldh=L.head; globals()['head']=lambda c,t,s=1.0: head_m(c,t,s); L.head=globals()['head']
    side_figure(f,k,far_arm=dict(elb=(74.4,42.4),wr=(74.8,53.2),fing=(69.3,54.4)))
    L.head=oldh; globals()['head']=oldh
    f.raw(OKT if kind=='ok' else NGT)
    return f.svg('0 0 100 60','ハイリバースプランク '+('良い例 一直線' if kind=='ok' else '悪い例 お尻が落ちる'),ng=(kind=='ng'))
# ---------- lunge / calf raise (vertical) ----------
def standing(n,kind):
    f=Fig(f'{kind}{n}'); f.raw(FLOOR_V)
    if kind=='lu' and n==2:
        hip=(27,70); N=(27.6,44); head=(29,37); sh=(28.2,46.5); elb=(27.4,58); wr=(28.2,68); fing=(28.8,73)
        knee=(46,71); ank=(45,91.4); ft=dict(heel=(42.4,93.6),ball=(50,94.4),toe=(53,94.8))
        far=dict(knee=(20,88.6),ank=(3.4,91.6),heel=(2.6,89.8),ball=(5.6,94.4),toe=(8.6,94.9))
    else:
        lift=4.2 if (kind=='ca' and n==2) else 0
        hip=(30,52-lift); N=(30.4,26-lift); head=(31.6,19-lift); sh=(31,28.5-lift); elb=(30.4,40-lift); wr=(31,50.6-lift); fing=(31.6,55.6-lift)
        knee=(30.8,72-lift); ank=(30,91.4-lift)
        ft=dict(heel=(27.2,93.6),ball=(35,94.4),toe=(38,94.8)) if lift==0 else dict(heel=(28,89.6),ball=(34.6,94.4),toe=(37.6,94.9))
        far=dict(knee=add(knee,(-1.2,0)),ank=add(ank,(-1.4,0)),heel=add(ft['heel'],(-1.4,0)),ball=add(ft['ball'],(-1.4,0)),toe=add(ft['toe'],(-1.4,0)))
    tor=[N,mul(add(N,hip),0.5),hip]
    k=dict(N=N,hip=hip,sh=sh,elb=elb,wr=wr,fing=fing,knee=knee,ank=ank,head=head,ht=0,torso=tor,hc_neck=hpt(head,0,-1.2,3.2),**ft)
    if kind=='lu':
        c,a=bone_pt(hip,knee,0.5,-2.6); f.plan('leg',[(c[0],c[1],7.0,2.4,a)])
        c2,a2=bone_pt(tor[1],hip,0.9,3.6); f.plan('torso',[(c2[0],c2[1],3.6,4.4,a2)])
    else:
        c,a=bone_pt(knee,ank,0.3,1.9); f.plan('leg',[(c[0],c[1],5.0,1.8,a)])
    side_figure(f,k,far_leg=far,far_arm=dict(elb=add(elb,(-1.2,0)),wr=add(wr,(-1.2,0)),fing=add(fing,(-1.2,0))))
    lab={'lu':('ランジ',('直立','前に踏み込む')),'ca':('カーフレイズ',('かかとを下ろす','かかとを上げる'))}[kind]
    return f.svg('0 0 60 100',lab[0]+' '+lab[1][n-1])
# ---------- hip lift (supine, head right) ----------
def hiplift(n):
    f=Fig(f'hl{n}'); f.raw(FLOOR_H)
    N=(70,50.8); sh=(68.5,52.4); head=(77,49.6)
    hip=(45,51.2) if n==1 else (45,38.6)
    knee=(30,38.2) if n==1 else (29,36.5); ank=(22,51.6)
    u=norm(sub(N,hip)); face=(u[1],-u[0]); th=math.degrees(math.atan2(face[1],face[0]))
    tor=[N,mul(add(N,hip),0.5),hip]
    k=dict(N=N,hip=hip,sh=sh,elb=(58,53.6),wr=(50,54),fing=(46,54.4),knee=knee,ank=ank,heel=(20,53.6),ball=(25,54.4),toe=(28,54.8),head=head,ht=th,torso=tor,hc_neck=add(head,mul(u,-3.2)))
    c,a=bone_pt(tor[1],hip,0.85,-3.6); f.plan('torso',[(c[0],c[1],4.0,3.6,a)])
    import figlib as L
    oldh=L.head; globals()['head']=lambda c,t,s=1.0: head_m(c,t,s); L.head=globals()['head']
    side_figure(f,k,far_leg=dict(knee=add(knee,(1.6,0.2)),ank=add(ank,(1.6,0)),heel=(21.6,53.6),ball=(26.6,54.4),toe=(29.6,54.8)))
    L.head=oldh; globals()['head']=oldh
    return f.svg('0 0 100 60','ヒップリフト '+('お尻を下ろす' if n==1 else '肩から膝まで一直線'))
ROLLER=lambda x,y=51.2:f'<g><line x1="{x-5.5}" y1="{y}" x2="{x+5.5}" y2="{y}" stroke="#8C8C8C" stroke-width="1.6" stroke-linecap="round"></line><circle cx="{x}" cy="{y}" r="4.2" fill="#3A3E41" stroke="#8C8C8C" stroke-width="1.2"></circle><circle cx="{x}" cy="{y}" r="1" fill="#8C8C8C"></circle></g>'
def roller_side(n,kind):
    f=Fig(f'{kind}{n}'); f.raw(FLOOR_H)
    if kind=='ak':
        knee=(30,52.2); ank=(13,52.6); ft=dict(heel=(12,50.6),ball=(10,54.2),toe=(8,54.8))
        if n==1: hip=(34,34.5); N=(52,30.5); rx=56
        else: hip=(46,45.5); N=(71,41.6); rx=86
    else:
        ank=(16,51.2); ft=dict(heel=(13.4,53.4),ball=(20,54.4),toe=(23,54.8))
        if n==1: hip=(27,24.5); knee=(22,38); N=(46,38.5); rx=40
        else: knee=(30,49); hip=(45,46.2); N=(70,41.2); rx=86
    if kind=='ak': pass
    sh=add(N,(-0.6,2.6)); wr=(rx-1.2,47.6); elb=mul(add(sh,wr),0.5); fing=(rx+1.2,46.4)
    u=norm(sub(N,hip)); head=add(N,mul(u,6.4)); head=(head[0]+0.8,head[1]+1.6)
    th=math.degrees(math.atan2(u[1],u[0]))+90
    tor=[N,mul(add(N,hip),0.5),hip]
    k=dict(N=N,hip=hip,sh=sh,elb=elb,wr=wr,fing=fing,knee=knee,ank=ank,head=head,ht=th,torso=tor,hc_neck=hpt(head,th,-1.2,3.2),**ft)
    c,a=bone_pt(N,hip,0.55,4.0); f.plan('torso',[(c[0],c[1],6.0,2.8,a)])
    f.raw(ROLLER(rx))
    side_figure(f,k,far_arm=dict(elb=add(elb,(-2,0.3)),wr=add(wr,(-1.6,0)),fing=add(fing,(-1.6,0))))
    lab={'ak':('アブローラー 膝コロ',('膝をついて構える','腕を前に伸ばす')),'as':('アブローラー 立ちコロ',('立って前屈しローラーをつく','体を一直線に伸ばす'))}[kind]
    return f.svg('0 0 100 60',lab[0]+' '+lab[1][n-1])
def roller_top(n):
    f=Fig(f'ao{n}')
    # top view, knees at bottom, body extends upward (and to the upper-left in frame 2)
    ang=math.radians(-90 if n==1 else -125)
    base=(52,50); L=lambda d:(base[0]+math.cos(ang)*d, base[1]+math.sin(ang)*d)
    nx,ny=-math.sin(ang),math.cos(ang)
    hip=L(10 if n==1 else 12); N=L(26 if n==1 else 34); head=L(32 if n==1 else 40)
    for s_ in (-1,1):
        kn=(base[0]+nx*4.2*s_, base[1]+ny*4.2*s_)
        f.part(limb([(kn[0],kn[1]+6),kn],[[(0,2.4,2.4),(1,3.0,3.0)]],0.6,0.4))
        f.part(limb([kn,(hip[0]+nx*3.4*s_,hip[1]+ny*3.4*s_)],[[(0,3.2,3.2),(1,4.2,4.2)]],0.5,0.5))
    f.plan('torso',[(*L(17 if n==1 else 21),6.5,2.4,math.degrees(ang)+90+(0 if n==1 else 20))])
    f.part(limb([hip,N],[[(0,6.0,6.0),(0.7,8.0,8.0),(1,8.4,8.4)]],0.4,0.4),name='torso')
    seam(f,hip,mul(add(hip,N),0.5),N,6.6,6.6)
    rp=L(48 if n==1 else 60)
    for s_ in (-1,1):
        shp=(N[0]+nx*7*s_,N[1]+ny*7*s_)
        f.part(limb([shp,(rp[0]+nx*2.4*s_,rp[1]+ny*2.4*s_)],[[(0,2.6,2.6),(1,1.6,1.6)]],0.6,0.6))
    f.part(cr([(head[0]+4.6*math.cos(t/16*2*math.pi),head[1]+4.6*math.sin(t/16*2*math.pi)) for t in range(16)]),name='head')
    f.raw(f'<g transform="rotate({math.degrees(ang)+90:.0f} {rp[0]:.1f} {rp[1]:.1f})"><rect x="{rp[0]-6:.1f}" y="{rp[1]-2.6:.1f}" width="12" height="5.2" rx="2" fill="#3A3E41" stroke="#8C8C8C" stroke-width="1.2"></rect></g>')
    return f.svg('0 0 100 60','アブローラー 斜めコロ 真上から '+('開始' if n==1 else '斜め前へ伸ばす'))
def jumprope(n):
    f=Fig(f'jr{n}'); f.raw(FLOOR_V)
    lift=0 if n==1 else 5
    hipy=55-lift
    rope=('M17 58 Q16 99 30 97.5 Q44 99 43 58' if n==1 else 'M17 56 Q15 4 30 3 Q45 4 43 56')
    if n==2: f.raw(f'<path d="{rope}" fill="none" stroke="#8C8C8C" stroke-width="0.9"></path>')
    for s_ in (-1,1):
        hx=30+s_*3.4
        f.part(limb([(hx,hipy),(30+s_*4.2,hipy+18),(30+s_*4.0,hipy+36)],[[(0,4.0,4.0),(1,3.0,3.0)],[(0,2.9,2.9),(0.3,3.2,3.2),(1,1.6,1.6)]],0.4,0.5),name='leg')
        seam(f,(hx,hipy),(30+s_*4.2,hipy+18),(30+s_*4.0,hipy+36),2.8,2.8)
        fx=30+s_*4.4; fy=hipy+38
        f.part(cr([(fx-2.2,fy-1.2),(fx+2.2,fy-1.2),(fx+2.6,fy+1.4),(fx-2.6,fy+1.4)]))
    f.plan('leg',[(30+s*4.1,hipy+24,1.8,5.0,0) for s in (-1,1)])
    f.part(limb([(30,hipy+2),(30,hipy-24)],[[(0,7.4,7.4),(0.5,6.2,6.2),(0.85,8.6,8.6),(1,8.6,8.6)]],0.4,0.4),name='torso')
    seam(f,(30,hipy+4),(30,hipy-10),(30,hipy-24),6.6,6.6)
    f.part(cr([(30+4.6*math.cos(t/16*2*math.pi),hipy-31+5.2*math.sin(t/16*2*math.pi)) for t in range(16)]))
    for s_ in (-1,1):
        shp=(30+s_*8,hipy-21); el=(30+s_*10.6,hipy-9); hd=(30+s_*13,hipy+1)
        f.part(limb([shp,el,hd],[[(0,2.6,2.6),(1,2.0,2.0)],[(0,1.9,1.9),(1,1.4,1.4)]],0.6,0.5))
        seam(f,shp,el,hd,1.9,1.9)
    if n==1: f.raw(f'<path d="{rope}" fill="none" stroke="#8C8C8C" stroke-width="0.9"></path>')
    return f.svg('0 0 60 100','縄跳び 正面から '+('着地' if n==1 else '小さくジャンプ'))
BOX='<rect x="33" y="82.5" width="22" height="12.4" rx="1.2" fill="#3A3E41" stroke="#8C8C8C" stroke-width="1.0"></rect>'
def stepup(n):
    f=Fig(f'su{n}'); f.raw(FLOOR_V); f.raw(BOX)
    if n==1:
        hip=(27,52); N=(29.5,26.5); head=(31.4,19.6); sh=(30,29)
        knee=(41,64.5); ank=(40,80.8); ft=dict(heel=(37.4,82.3),ball=(44.6,82.4),toe=(47.6,82.6))
        far=dict(knee=(25,71.6),ank=(20,91.2),heel=(17,93.4),ball=(24.6,94.4),toe=(27.6,94.8))
    else:
        hip=(42,40); N=(42.6,14.4); head=(43.8,7.4); sh=(43.2,17)
        knee=(42.8,60); ank=(42,79.6); ft=dict(heel=(39.4,82.3),ball=(46.6,82.4),toe=(49.6,82.6))
        far=dict(knee=(41.6,60),ank=(40.6,79.6),heel=(38,82.3),ball=(45.2,82.4),toe=(48.2,82.6))
    elb=add(sh,(1.2,11)); wr=add(sh,(2.4,21)); fing=add(wr,(0.6,4.6))
    tor=[N,mul(add(N,hip),0.5),hip]
    k=dict(N=N,hip=hip,sh=sh,elb=elb,wr=wr,fing=fing,knee=knee,ank=ank,head=head,ht=4,torso=tor,hc_neck=hpt(head,4,-1.2,3.2),**ft)
    c,a=bone_pt(hip,knee,0.5,-2.6); f.plan('leg',[(c[0],c[1],6.5,2.3,a)])
    c2,a2=bone_pt(tor[1],hip,0.9,3.4); f.plan('torso',[(c2[0],c2[1],3.4,4.2,a2)])
    side_figure(f,k,far_leg=far,far_arm=dict(elb=add(elb,(-1.4,0)),wr=add(wr,(-1.4,0)),fing=add(fing,(-1.4,0))))
    return f.svg('0 0 60 100','踏み台昇降 '+('片足を台に乗せる' if n==1 else '台に乗り上がる'))
def highknee(n):
    f=Fig(f'hk{n}'); f.raw(FLOOR_V)
    hip=(30,52); N=(30.6,26.5); head=(31.8,19.6); sh=(31,29)
    up=dict(knee=(44,47),ank=(42,66),heel=(39.4,67.4),ball=(46.4,69.2),toe=(49,70.4))
    down=dict(knee=(29.4,72),ank=(28,91.4),heel=(25.2,93.6),ball=(33,94.4),toe=(36,94.8))
    armF=dict(elb=(37,37.5),wr=(44,31),fing=(46.6,27.6)); armB=dict(elb=(25.6,39.6),wr=(19.6,47.4),fing=(17.6,51.2))
    near,far=(up,down) if n==1 else (down,up)
    nearArm,farArm=(armB,armF) if n==1 else (armF,armB)
    tor=[N,mul(add(N,hip),0.5),hip]
    k=dict(N=N,hip=hip,sh=sh,head=head,ht=4,torso=tor,hc_neck=hpt(head,4,-1.2,3.2),**nearArm,**near)
    c,a=bone_pt(hip,near['knee'],0.5,-2.6 if n==1 else -2.6); f.plan('leg',[(c[0],c[1],6.5,2.3,a)])
    side_figure(f,k,far_leg=far,far_arm=farArm)
    return f.svg('0 0 60 100','その場駆け足 '+('右膝を上げる' if n==1 else '左膝を上げる'))
