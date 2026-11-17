# v9 parts b+c: oblique (くびれ) illustrations, two new oblique exercises, くびれ group in the builder
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
rc('SVG_SIDEPLANK_OK','side_plank_1'); rc('SVG_SIDEPLANK_NG','side_plank_2')
rc('SVG_BICYCLE_1','bicycle_crunch_1'); rc('SVG_BICYCLE_2','bicycle_crunch_2')
rc('SVG_TWIST_1','russian_twist_1'); rc('SVG_TWIST_2','russian_twist_2')
block="\n  /* v9: リアル寄りの人体イラスト（案C）くびれ（脇腹） */\n"+''.join(f"  const {c} = '{S[k]}';\n" for c,k in
  [('SVG_XCLIMB_1','cross_mountain_climber_1'),('SVG_XCLIMB_2','cross_mountain_climber_2'),('SVG_SPHIP_1','side_plank_hipup_1'),('SVG_SPHIP_2','side_plank_hipup_2'),('SVG_HEELTOUCH_1','heel_touch_crunch_1'),('SVG_HEELTOUCH_2','heel_touch_crunch_2')])
s=s.replace("\n  const FORM_GUIDES = {",block+"\n  const FORM_GUIDES = {",1)
sub1("'クロスマウンテンクライマー（腹斜筋）': { labels:['プランク','クロス'], frames:[SVG_CLIMBER_1, SVG_CLIMBER_2]","'クロスマウンテンクライマー（腹斜筋）': { labels:['プランク','膝を対角の肘へ'], frames:[SVG_XCLIMB_1, SVG_XCLIMB_2]")
sub1("'ロシアンツイスト': { labels:['右','左']","'ロシアンツイスト': { labels:['右へ','左へ']")
# new exercises
sub1("    'ロシアンツイスト': {met:5.0, secPerRep:2},\n","    'ロシアンツイスト': {met:5.0, secPerRep:2},\n    'サイドプランク・ヒップアップ（左右）': {met:3.8, secPerRep:2.5}, /* v9 */\n    'ヒールタッチクランチ': {met:3.8, secPerRep:1.5}, /* v9 */\n")
sub1("    {name:'ロシアンツイスト', category:'腹筋', type:'reps', defReps:20, defSets:2},\n","    {name:'ロシアンツイスト', category:'腹筋', type:'reps', defReps:20, defSets:2},\n    {name:'サイドプランク・ヒップアップ（左右）', category:'腹筋', type:'reps', defReps:10, defSets:2}, /* v9 */\n    {name:'ヒールタッチクランチ', category:'腹筋', type:'reps', defReps:20, defSets:2}, /* v9 */\n")
sub1("\n  const FORM_GUIDES = {\n","""\n  const FORM_GUIDES = {
    'サイドプランク・ヒップアップ（左右）': { labels:['腰を下ろす','持ち上げる'], frames:[SVG_SPHIP_1, SVG_SPHIP_2], tips:[ /* v9 */
      '横向きで前腕をつき、肘は肩の真下に置く',
      '腰を床の近くまで下ろし、脇腹の力で頭から足まで一直線になるまで持ち上げる',
      '左右とも同じ回数。反動は使わずゆっくり'
    ]},
    'ヒールタッチクランチ': { labels:['右へ','左へ'], frames:[SVG_HEELTOUCH_1, SVG_HEELTOUCH_2], tips:[ /* v9 */
      '仰向けで膝を立て、肩甲骨を床から少し浮かせる',
      '体を横に曲げて、右手で右かかと、左手で左かかとを交互にタッチ',
      '首は力を抜き、あごを軽く引いたまま'
    ]},
""")
sub1("\n  const CAUTION_LEVELUP = {\n","""\n  const CAUTION_LEVELUP = {
    'サイドプランク・ヒップアップ（左右）': { caution:['肩がすくむ・肘が肩の真下からずれると肩を痛める','腰をひねらず、横向きのまま上下する'], levelUp:['上げたところで2秒キープ','上側の脚を浮かせて行う'] }, /* v9 */
    'ヒールタッチクランチ': { caution:['首を前に引っ張らない','腰が反らないよう、お腹に力を入れたまま'], levelUp:['かかとを少しお尻から遠ざける','テンポを落として左右でゆっくり止める'] }, /* v9 */
""")
# くびれ group in the builder (shown first). Same items stay in their own category too.
sub1("  function renderBuilderLibrary(){\n    builderLibraryList.innerHTML = '';\n    CATEGORIES.forEach(cat=>{\n      const items = EXERCISE_LIBRARY.filter(e=>e.category===cat);",
"""  /* v9: くびれ（脇腹・腹斜筋）の種目。種目一覧の先頭にまとめて出す */
  const KUBIRE = ['サイドプランク（左右）','サイドプランク・ヒップアップ（左右）','ヒールタッチクランチ','バイシクルクランチ','ロシアンツイスト','クロスマウンテンクライマー（腹斜筋）','アブローラー（斜めコロ・腹斜筋狙い）'];
  function renderBuilderLibrary(){
    builderLibraryList.innerHTML = '';
    ['くびれ（脇腹）'].concat(CATEGORIES).forEach(cat=>{
      const items = cat==='くびれ（脇腹）' ? EXERCISE_LIBRARY.filter(e=>KUBIRE.indexOf(e.name)>=0) : EXERCISE_LIBRARY.filter(e=>e.category===cat);""")
sub1("      head.className = 'cat-head';\n      head.textContent = cat;","      head.className = 'cat-head' + (cat==='くびれ（脇腹）' ? ' kubire' : '');\n      head.textContent = cat==='くびれ（脇腹）' ? '★ くびれ（脇腹）' : cat;")
sub1("  .cat-head:first-child{ margin-top:4px; }\n","  .cat-head:first-child{ margin-top:4px; }\n  .cat-head.kubire{ color:var(--lime); } /* v9 */\n")
open(p,'w',encoding='utf-8').write(s); print('ok',len(s.encode()))
