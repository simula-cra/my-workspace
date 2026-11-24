# v10: PWA (manifest, icons, service worker). The HTML still works on its own (file:// / Drive):
# the manifest and service worker are only used when served over https (GitHub Pages).
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def sub1(a,b):
    global s; assert a in s,a[:60]; s=s.replace(a,b,1)
sub1('<title>筋トレ管理</title>\n','''<title>筋トレ管理</title>
<!-- v10: PWA（ホーム画面にインストールできるようにする）。GitHub Pages で開いたときだけ使われる -->
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#1C1E1F">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
''')
sub1("  renderHome();\n})();\n</script>","""  renderHome();
})();
/* v10: オフラインでも開けるよう service worker を登録（https のときだけ。Driveやファイルで開いたときは何もしない） */
if('serviceWorker' in navigator && (location.protocol==='https:' || location.hostname==='localhost')){
  window.addEventListener('load', ()=>{ navigator.serviceWorker.register('sw.js').catch(()=>{}); });
}
</script>""")
open(dst,'w',encoding='utf-8').write(s); print('ok')
