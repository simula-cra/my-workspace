# v9 part i: ab roller (knee/stand/oblique), jump rope, step up, running in place illustrations
import re,sys,pathlib
p=sys.argv[1]
IL=pathlib.Path('/home/user/my-workspace/kintore_illust/illust')
S={x.stem:x.read_text().strip() for x in IL.glob('*.svg')}
s=open(p,encoding='utf-8').read()
def sub1(a,b):
    global s; assert a in s,a[:70]; s=s.replace(a,b,1)
def rc(name,key):
    global s
    m=re.search(r"  const "+name+r" = .*?;\n",s); assert m,name
    s=s[:m.start()]+f"  const {name} = '{S[key]}'; /* v9: リアル寄りの人体イラスト（案C） */\n"+s[m.end():]
for c,k in [('SVG_JUMPROPE_1','jump_rope_1'),('SVG_JUMPROPE_2','jump_rope_2'),('SVG_STEP_1','step_up_1'),('SVG_STEP_2','step_up_2'),('SVG_RUN_1','high_knee_1'),('SVG_RUN_2','high_knee_2')]:
    rc(c,k)
block="\n  /* v9: リアル寄りの人体イラスト（案C）アブローラー */\n"+''.join(f"  const {c} = '{S[k]}';\n" for c,k in
  [('SVG_ROLLK_1','ab_roller_knee_1'),('SVG_ROLLK_2','ab_roller_knee_2'),('SVG_ROLLS_1','ab_roller_stand_1'),('SVG_ROLLS_2','ab_roller_stand_2'),('SVG_ROLLO_1','ab_roller_oblique_1'),('SVG_ROLLO_2','ab_roller_oblique_2')])
s=s.replace("\n  const FORM_GUIDES = {",block+"\n  const FORM_GUIDES = {",1)
sub1("'アブローラー（立ちコロ/膝コロ）': { labels:['開始','伸ばす'], frames:[SVG_ABROLLER_START, SVG_ABROLLER_END]","'アブローラー（立ちコロ/膝コロ）': { labels:['開始','伸ばす'], frames:[SVG_ROLLK_1, SVG_ROLLK_2]")
sub1("'アブローラー（立ちコロ）': { labels:['開始','伸ばす'], frames:[SVG_ABROLLER_START, SVG_ABROLLER_END]","'アブローラー（立ちコロ）': { labels:['開始','伸ばす'], frames:[SVG_ROLLS_1, SVG_ROLLS_2]")
m=re.search(r"'アブローラー（斜めコロ・腹斜筋狙い）': \{ labels:\[[^\]]*\], frames:\[SVG_ABROLLER_START, SVG_ABROLLER_END\]",s); assert m
s=s[:m.start()]+"'アブローラー（斜めコロ・腹斜筋狙い）': { labels:['開始','斜め前へ'], frames:[SVG_ROLLO_1, SVG_ROLLO_2]"+s[m.end():]
sub1("'その場ステップ（踏み台昇降）': { labels:['乗る','踏み込む']","'その場ステップ（踏み台昇降）': { labels:['片足を乗せる','乗り上がる']")
open(p,'w',encoding='utf-8').write(s); print('ok',len(s.encode()))
