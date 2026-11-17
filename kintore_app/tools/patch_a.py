# v9 part a: realistic illustrations (pushup/squat/chest) + rendering helpers + 2 new exercises
import re,sys,pathlib
src,dst=sys.argv[1],sys.argv[2]
IL=pathlib.Path('/home/user/my-workspace/kintore_illust/illust')
S={p.stem:p.read_text().strip() for p in IL.glob('*.svg')}
for k,v in S.items(): assert "'" not in v and '\\' not in v, k
s=open(src,encoding='utf-8').read()
def rc(name,key,note='v9: リアル寄りの人体イラスト（案C）'):
    global s
    m=re.search(r"  const "+name+r" = .*?;\n",s); assert m,name
    s=s[:m.start()]+f"  const {name} = '{S[key]}'; /* {note} */\n"+s[m.end():]
rc('SVG_PUSHUP_UP','pushup_1'); rc('SVG_PUSHUP_DOWN','pushup_2')
rc('SVG_SQUAT_OK','squat_1'); rc('SVG_SQUAT_NG','squat_2')
rc('SVG_DIAMOND_UP','diamond_pushup_1','v9: 手元のひし形（真上から）'); rc('SVG_DIAMOND_DOWN','diamond_pushup_2','v9: 肘を体に沿わせた下')
rc('SVG_PIKE_1','pike_pushup_1'); rc('SVG_PIKE_2','pike_pushup_2')
block="\n  /* v9: リアル寄りの人体イラスト（案C）胸・腕 */\n"+''.join(f"  const {c} = '{S[k]}';\n" for c,k in
  [('SVG_WALLPU_1','wall_pushup_1'),('SVG_WALLPU_2','wall_pushup_2'),('SVG_KNEEPU_1','knee_pushup_1'),('SVG_KNEEPU_2','knee_pushup_2'),('SVG_WIDENARROW_1','pushup_wide_narrow_1'),('SVG_WIDENARROW_2','pushup_wide_narrow_2')])
s=s.replace("\n  const FORM_GUIDES = {",block+"\n  const FORM_GUIDES = {",1)
def sub1(a,b):
    global s; assert a in s,a[:60]; s=s.replace(a,b,1)
sub1("'腕立て伏せ（ワイド/ナロー交互）': { labels:['上','下'], frames:[SVG_PUSHUP_UP, SVG_PUSHUP_DOWN]","'腕立て伏せ（ワイド/ナロー交互）': { labels:['ワイド','ナロー'], frames:[SVG_WIDENARROW_1, SVG_WIDENARROW_2]")
sub1("'ダイヤモンドプッシュアップ': { labels:['上','下'], frames:[SVG_DIAMOND_UP, SVG_DIAMOND_DOWN]","'ダイヤモンドプッシュアップ': { labels:['手の形','下'], frames:[SVG_DIAMOND_UP, SVG_DIAMOND_DOWN]")
sub1("'パイクプッシュアップ': { labels:['上','下'], frames:[SVG_PIKE_1, SVG_PIKE_2]","'パイクプッシュアップ': { labels:['上','頭を下ろす'], frames:[SVG_PIKE_1, SVG_PIKE_2]")
# helpers
sub1("  function guideHtml(name){\n","""  /* v9: 新イラストは clipPath の id を使うので、同じ絵が画面に複数出ても衝突しないよう描画ごとに id を付け直す */
  let svgUid = 0;
  function uniqSvg(svg){
    if(svg.indexOf(' id="') < 0) return svg;
    const sfx = '_' + (svgUid++).toString(36);
    return svg.replace(/ id="([^"]+)"/g, ' id="$1'+sfx+'"').replace(/(href="#|url\\(#)([^")]+)/g, '$1$2'+sfx);
  }
  function figCls(svg){ return /viewBox="0 0 100 60"/.test(svg) ? 'guide-fig wide' : 'guide-fig'; } /* v9: 横長の絵は横長の枠 */
  function guideHtml(name){
""")
for i in (0,1):
    sub1(f"'<div class=\"guide-fig\">'+g.frames[{i}]+'", f"'<div class=\"'+figCls(g.frames[{i}])+'\">'+uniqSvg(g.frames[{i}])+'")
sub1("<div class=\"guide-figs\"><div class=\"guide-fig\">'+g.frames[0]+'","<div class=\"guide-figs\"><div class=\"'+figCls(g.frames[0])+'\">'+uniqSvg(g.frames[0])+'")
sub1("  #workoutGuideCard .guide-figs svg{ width:112px; height:112px; }\n","""  #workoutGuideCard .guide-figs svg{ width:112px; height:112px; }
  /* v9: 横長の絵（寝る・四つん這いの種目）は横長の枠で表示 */
  .guide-fig.wide svg, #workoutGuideCard .guide-fig.wide svg{ width:136px; height:82px; }
  .guide-figs:has(.wide){ gap:8px; }
""")
# new exercises (4 tables)
sub1("    'パイクプッシュアップ': {met:8.0, secPerRep:2.5},\n","    'パイクプッシュアップ': {met:8.0, secPerRep:2.5},\n    '壁腕立て': {met:2.8, secPerRep:2.5}, /* v9 */\n    '膝つき腕立て': {met:3.8, secPerRep:2.5}, /* v9 */\n")
sub1("    {name:'腕立て伏せ', category:'上半身', type:'reps', defReps:15, defSets:2},\n","    {name:'壁腕立て', category:'上半身', type:'reps', defReps:15, defSets:2}, /* v9 */\n    {name:'膝つき腕立て', category:'上半身', type:'reps', defReps:12, defSets:2}, /* v9 */\n    {name:'腕立て伏せ', category:'上半身', type:'reps', defReps:15, defSets:2},\n")
sub1("\n  const FORM_GUIDES = {\n","""\n  const FORM_GUIDES = {
    '壁腕立て': { labels:['伸ばす','近づける'], frames:[SVG_WALLPU_1, SVG_WALLPU_2], tips:[ /* v9 */
      '壁から一歩半ほど離れて立ち、肩の高さで肩幅より少し広く手をつく',
      '頭からかかとまで一直線のまま、肘を曲げて胸を壁に近づける',
      '壁を押して元に戻る。お腹に軽く力を入れて腰を反らさない'
    ]},
    '膝つき腕立て': { labels:['上','下'], frames:[SVG_KNEEPU_1, SVG_KNEEPU_2], tips:[ /* v9 */
      '膝を床につき、頭から膝まで一直線にする',
      '手は肩幅よりやや広め、肘は体から45度くらいで曲げる',
      '胸が床に近づくまで下ろし、床を押して戻る'
    ]},
""")
sub1("\n  const CAUTION_LEVELUP = {\n","""\n  const CAUTION_LEVELUP = {
    '壁腕立て': { caution:['足が滑らない靴・床で行う','手首が痛い場合は指先を少し外に向ける'], levelUp:['足を壁から遠ざけるほど負荷が上がる','楽になったら膝つき腕立てへ進む'] }, /* v9 */
    '膝つき腕立て': { caution:['膝が痛い場合はタオルやマットを敷く','お尻が上がる・腰が反るのはフォーム崩れ'], levelUp:['下ろす動作を3秒かけてゆっくり行う','10回×3セットが楽になったら通常の腕立て伏せへ'] }, /* v9 */
""")
open(dst,'w',encoding='utf-8').write(s)
print('ok',len(s.encode()))
