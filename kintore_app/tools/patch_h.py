# v9 part h: back and lower-body illustrations
import re,sys,pathlib
p=sys.argv[1]
IL=pathlib.Path('/home/user/my-workspace/kintore_illust/illust')
S={x.stem:x.read_text().strip() for x in IL.glob('*.svg')}
s=open(p,encoding='utf-8').read()
def rc(name,key):
    global s
    m=re.search(r"  const "+name+r" = .*?;\n",s); assert m,name
    s=s[:m.start()]+f"  const {name} = '{S[key]}'; /* v9: リアル寄りの人体イラスト（案C） */\n"+s[m.end():]
for c,k in [('SVG_SUPERMAN_1','superman_1'),('SVG_SUPERMAN_2','superman_2'),('SVG_BACKEXT_1','back_extension_1'),('SVG_BACKEXT_2','back_extension_2'),
            ('SVG_HIREVPLANK_1','high_reverse_plank_1'),('SVG_HIREVPLANK_2','high_reverse_plank_2'),('SVG_HIPLIFT_1','hip_lift_1'),('SVG_HIPLIFT_2','hip_lift_2'),
            ('SVG_LUNGE_1','lunge_1'),('SVG_LUNGE_2','lunge_2'),('SVG_CALF_1','calf_raise_1'),('SVG_CALF_2','calf_raise_2')]:
    rc(c,k)
a="'ハイリバースプランク': { labels:['キープ','']"; assert a in s
s=s.replace(a,"'ハイリバースプランク': { labels:['良い例','悪い例']")  # v9: 2コマ目が同じ絵だった問題を解消
open(p,'w',encoding='utf-8').write(s); print('ok',len(s.encode()))
