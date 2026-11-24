# v9 part d: unify MET values (Compendium of Physical Activities: calisthenics light 2.8 / moderate 3.8 / vigorous 8.0) and default body weight
import re,sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
NEW={
 'アブローラー（立ちコロ/膝コロ）':3.8,'アブローラー（立ちコロ）':5.0,'アブローラー（斜めコロ・腹斜筋狙い）':3.8,
 '腕立て伏せ':3.8,'腕立て伏せ（ワイド/ナロー交互）':3.8,'ダイヤモンドプッシュアップ':3.8,'パイクプッシュアップ':3.8,
 'リバースプッシュアップ（椅子ディップス）':3.8,'プランク':3.0,'サイドプランク（左右）':3.0,
 '縄跳び':8.8,'縄跳び（二重跳び挑戦）':12.0,'その場ステップ（踏み台昇降）':5.0,
 'バイシクルクランチ':3.8,'クランチ':3.8,'ロシアンツイスト':3.8,'レッグレイズ':3.8,
 'ヒップリフト（お尻上げ）':3.8,'カーフレイズ（かかと上げ）':2.8,'バックエクステンション（背筋伸ばし）':3.8,'スーパーマン':3.8,'ハイリバースプランク':3.0}
before={}
for name,met in NEW.items():
    pat=re.compile(r"(    '"+re.escape(name)+r"': \{met:)([\d.]+)(, secPerRep:[\d.]+\},?)")
    m=pat.search(s); assert m,name
    before[name]=float(m.group(2))
    s=s[:m.start()]+m.group(1)+f"{met}"+m.group(3)+(" /* v9: MET見直し */" if float(m.group(2))!=met else "")+s[m.end():]
a="  if(!data.bodyWeight) data.bodyWeight = 68;"
assert a in s
s=s.replace(a,"  if(!data.bodyWeight) data.bodyWeight = 60; /* v9: 初期値68kg→60kg（保存済みの体重はそのまま） */")
s=s.replace("  const MET_TABLE = {","  /* v9: METは身体活動のメッツ表（Compendium）の自重トレ基準にそろえた：軽い2.8／ふつう3.8／きつい8.0。キープ系3.0、有酸素は種目ごと */\n  const MET_TABLE = {",1)
open(p,'w',encoding='utf-8').write(s)
for k,v in NEW.items():
    if before[k]!=v: print(f"{k}: {before[k]} -> {v}")
