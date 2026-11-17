# v9 parts e,f: monthly summary on the history tab, reward message after training
import sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
def sub1(a,b):
    global s; assert a in s,a[:70]; s=s.replace(a,b,1)
# HTML: monthly summary under the calendar
sub1('      <div class="cal" id="calGrid"></div>\n    </div>','''      <div class="cal" id="calGrid"></div>
      <div class="month-sum" id="monthSum"></div> <!-- v9: 今月のまとめ -->
    </div>''')
# CSS
sub1("  .cal .d.today{ outline:2px solid var(--steel); }\n","""  .cal .d.today{ outline:2px solid var(--steel); }
  /* v9: 今月のまとめ */
  .month-sum{ display:flex; gap:8px; margin-top:12px; }
  .month-sum .ms{ flex:1; background:var(--bg); border:1px solid var(--border); border-radius:10px; padding:8px 6px; text-align:center; }
  .month-sum .ms b{ display:block; font-size:22px; color:var(--lime); line-height:1.2; }
  .month-sum .ms span{ font-size:10px; color:var(--text-dim); }
  .month-sum .food{ flex-basis:100%; }
""")
# helpers (before renderHistory)
sub1("  function renderHistory(){\n","""  /* v9: 月の集計・連続日数・食べ物換算（ごほうび表示と記録タブで共通） */
  const ONIGIRI_KCAL = 180; // コンビニおにぎり1個の目安
  function monthStats(year, month){
    let days=0, kcal=0;
    Object.keys(data.logs).forEach(k=>{
      const d = new Date(k+'T00:00:00');
      if(d.getFullYear()===year && d.getMonth()===month){ days++; kcal += (data.logs[k].kcal||0); }
    });
    return {days, kcal};
  }
  function currentStreak(){
    let n=0; const d=new Date();
    while(data.logs[todayKey(d)]){ n++; d.setDate(d.getDate()-1); }
    return n;
  }
  function onigiri(kcal){ return Math.round(kcal/ONIGIRI_KCAL*10)/10; }
  function renderHistory(){
""")
sub1("      calGrid.appendChild(cell);\n    }\n","""      calGrid.appendChild(cell);
    }
    /* v9: 今月のまとめ */
    const ms = monthStats(year, month);
    document.getElementById('monthSum').innerHTML =
      '<div class="ms"><b>'+ms.days+'</b><span>今月の実施日数</span></div>'
      + '<div class="ms"><b>'+ms.kcal+'</b><span>今月の消費kcal</span></div>'
      + '<div class="ms"><b>'+currentStreak()+'</b><span>連続日数</span></div>'
      + '<div class="ms food"><span>今月の消費は おにぎり約</span><b style="display:inline;font-size:18px"> '+onigiri(ms.kcal)+' </b><span>個分</span></div>';
""")
# reward message
sub1("""      msg: 'ルーティン：'+routine.label+'\\n消費カロリー目安：約'+kcal+'kcal\\nあすけんの運動記録に入力してください。',""",
"""      msg: (function(){ /* v9: ごほうび表示（今月の回数・合計・連続日数） */
        const now=new Date(); const ms=monthStats(now.getFullYear(), now.getMonth());
        return '今月 '+ms.days+' 回目のトレーニング！\\n'
          + '今日：約'+kcal+'kcal（'+routine.label+'）\\n'
          + '今月の合計：約'+ms.kcal+'kcal（おにぎり約'+onigiri(ms.kcal)+'個分）\\n'
          + '連続 '+currentStreak()+' 日\\n\\n'
          + 'あすけんの運動記録に入力してください。';
      })(),""")
open(p,'w',encoding='utf-8').write(s); print('ok')
