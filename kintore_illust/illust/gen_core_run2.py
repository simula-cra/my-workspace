exec(open('/home/user/my-workspace/kintore_illust/illust/generate_core.py').read())
S['plank_1']=plank('ok'); S['plank_2']=plank('ng')
S['mountain_climber_1']=mclimb(1); S['mountain_climber_2']=mclimb(2)
S['crunch_1']=lying(1,'cr'); S['crunch_2']=lying(2,'cr')
S['leg_raise_1']=lying(1,'lr'); S['leg_raise_2']=lying(2,'lr')
import pathlib
for k,v in S.items(): pathlib.Path(f'/home/user/my-workspace/kintore_illust/illust/{k}.svg').write_text(v+'\n')
print({k:len(v.encode()) for k,v in S.items()})
