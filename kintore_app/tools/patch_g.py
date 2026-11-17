# v9 part g: plank / mountain climber / crunch / leg raise illustrations
import re,sys,pathlib
p=sys.argv[1]
IL=pathlib.Path('/home/user/my-workspace/kintore_illust/illust')
S={x.stem:x.read_text().strip() for x in IL.glob('*.svg')}
s=open(p,encoding='utf-8').read()
def rc(name,key):
    global s
    m=re.search(r"  const "+name+r" = .*?;\n",s); assert m,name
    s=s[:m.start()]+f"  const {name} = '{S[key]}'; /* v9: リアル寄りの人体イラスト（案C） */\n"+s[m.end():]
for c,k in [('SVG_PLANK_OK','plank_1'),('SVG_PLANK_NG','plank_2'),('SVG_CLIMBER_1','mountain_climber_1'),('SVG_CLIMBER_2','mountain_climber_2'),('SVG_CRUNCH_1','crunch_1'),('SVG_CRUNCH_2','crunch_2'),('SVG_LEGRAISE_1','leg_raise_1'),('SVG_LEGRAISE_2','leg_raise_2')]:
    rc(c,k)
open(p,'w',encoding='utf-8').write(s); print('ok',len(s.encode()))
