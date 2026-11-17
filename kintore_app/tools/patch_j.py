# v9 part j: add 8 no-equipment exercises from the illustration list (with illustrations)
import sys,pathlib
p=sys.argv[1]
IL=pathlib.Path('/home/user/my-workspace/kintore_illust/illust')
S={x.stem:x.read_text().strip() for x in IL.glob('*.svg')}
s=open(p,encoding='utf-8').read()
def sub1(a,b):
    global s; assert a in s,a[:70]; s=s.replace(a,b,1)
EX=[ # name, category, type, default, sets, met, secPerRep, svg key, labels, tips, caution, levelUp
 ('プローンYレイズ','背筋','reps',10,2,2.8,3,'prone_y_raise',['腕を前に伸ばす','腕を浮かす'],
  ['うつ伏せで腕を頭の先へY字に伸ばし、親指を天井に向ける','肩甲骨を寄せ下げるようにして、腕を床から少し浮かす','額は床に向けたまま。首を反らさない'],
  ['腰を反らせて腕を上げない','肩がすくむ場合は浮かす高さを低くする'],['上げたところで2秒キープ','腕を伸ばしたまま、ゆっくり下ろす']),
 ('プローンTレイズ','背筋','reps',10,2,2.8,3,'prone_t_raise',['真横に下ろす','真横のまま浮かす'],
  ['うつ伏せで腕を真横に広げ、親指を天井に向ける','肩甲骨の間を寄せるようにして腕を浮かす','額は床に向けたまま'],
  ['反動で上げない','首や肩に力を入れすぎない'],['上げたところで2秒キープ','回数を少しずつ増やす']),
 ('リバーススノーエンジェル','背筋','reps',8,2,2.8,4,'reverse_snow_angel',['頭上へ','腰の横へ'],
  ['うつ伏せで腕を床から浮かせたまま、頭上に伸ばす','腕を浮かせたまま、弧を描いて腰の横まで動かす','ゆっくり往復する'],
  ['肩に痛みが出る範囲まで動かさない','腰を反らさない'],['往復を4秒かけてゆっくり','途中で1秒止める']),
 ('プローンコブラ','背筋','time',20,3,2.8,0,'prone_cobra',['うつ伏せ','胸を浮かせる'],
  ['うつ伏せで腕を体の横に置く','胸を少し浮かせ、腕を後ろに引いて肩甲骨を寄せる','目線は床。首を反らさない'],
  ['腰で反らない。胸だけを浮かせる','腰に痛みが出たら中止'],['キープ時間を10秒ずつ伸ばす','親指を外に向けて肩甲骨をより寄せる']),
 ('バードドッグ（左右）','背筋','reps',10,2,2.8,4,'bird_dog',['四つん這い','対角に伸ばす'],
  ['手は肩の真下、膝は股関節の真下','右腕と左脚を、床と平行になるまで伸ばす','背中が傾かないよう、お腹に力を入れる'],
  ['腰を反らせて脚を高く上げすぎない','体が左右に傾かないように'],['伸ばしたところで3秒キープ','肘と膝を体の下でつけてから伸ばす']),
 ('ホロウボディホールド','腹筋','time',20,3,3.0,0,'hollow_body',['膝を曲げる','手足を伸ばす'],
  ['仰向けで腰を床に押しつけたまま、肩と脚を浮かす','きついうちは膝を曲げた形でOK','慣れたら手足を伸ばしてバナナのような形でキープ'],
  ['腰が床から浮いたら膝を曲げた形に戻す','呼吸を止めない'],['手足を床に近づける','キープ時間を伸ばす']),
 ('スプリットスクワット（左右）','下半身','reps',10,2,3.8,3,'split_squat',['開いて立つ','沈む'],
  ['足を前後に大きく開き、その位置のまま動かさない（ランジとの違い）','上体はまっすぐのまま、真下に沈む','後ろの膝は床すれすれまで'],
  ['前の膝が内側に入らないように','バランスが不安なら壁に手を添える'],['沈むのに3秒かける','回数を増やす']),
 ('静かなバーピー','全身','reps',10,2,6.0,4,'silent_burpee',['しゃがむ','プランク'],
  ['しゃがんで両手を肩幅で床につく','足を1本ずつ後ろに下げて、腕立ての姿勢になる','足を1本ずつ戻して立つ。ジャンプはしない（集合住宅でも静か）'],
  ['腰が反ったプランクにならないように','膝や手首に痛みが出たら回数を減らす'],['足を両足同時に下げる','立ったところで腕を上に伸ばす']),
]
lib=''.join(f"    {{name:'{n}', category:'{c}', type:'{t}', "+(f"defReps:{d}" if t=='reps' else f"defSeconds:{d}")+f", defSets:{st}}}, /* v9 */\n" for n,c,t,d,st,*_ in EX)
sub1("  const EXERCISE_LIBRARY = [\n","  const EXERCISE_LIBRARY = [\n"+lib)
met=''.join(f"    '{n}': {{met:{m}, secPerRep:{spr}}}, /* v9 */\n" for n,c,t,d,st,m,spr,*_ in EX)
sub1("  const MET_TABLE = {\n","  const MET_TABLE = {\n"+met)
consts="\n  /* v9: 新しく追加した道具なし種目のイラスト（案C） */\n"
fg=''; cl=''
for i,(n,c,t,d,st,m,spr,key,labels,tips,cau,lv) in enumerate(EX):
    cn=f"SVG_NEW{i}"
    consts+=f"  const {cn}_1 = '{S[key+'_1']}';\n  const {cn}_2 = '{S[key+'_2']}';\n"
    fg+=f"    '{n}': {{ labels:['{labels[0]}','{labels[1]}'], frames:[{cn}_1, {cn}_2], tips:[ /* v9 */\n"+',\n'.join(f"      '{x}'" for x in tips)+"\n    ]},\n"
    cl+=f"    '{n}': {{ caution:["+','.join(f"'{x}'" for x in cau)+"], levelUp:["+','.join(f"'{x}'" for x in lv)+"] }, /* v9 */\n"
s=s.replace("\n  const FORM_GUIDES = {",consts+"\n  const FORM_GUIDES = {",1)
sub1("\n  const FORM_GUIDES = {\n","\n  const FORM_GUIDES = {\n"+fg)
sub1("\n  const CAUTION_LEVELUP = {\n","\n  const CAUTION_LEVELUP = {\n"+cl)
open(p,'w',encoding='utf-8').write(s); print('ok',len(s.encode()))
