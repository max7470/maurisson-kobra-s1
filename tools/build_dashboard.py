# -*- coding: utf-8 -*-
"""Génère un tableau de bord HTML autoportant depuis data/*.json + kobra-s1.json."""
import json, os

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "data")

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

bundle = {
    "manifest": load(os.path.join(ROOT, "kobra-s1.json")),
    "printer": load(os.path.join(DATA, "printer.json")),
    "calibration": load(os.path.join(DATA, "calibration.json")),
    "maintenance": load(os.path.join(DATA, "maintenance.json")),
    "troubleshooting": load(os.path.join(DATA, "troubleshooting.json")),
    "consumables": load(os.path.join(DATA, "consumables.json")),
    "materials": load(os.path.join(DATA, "materials.json")),
    "slicer": load(os.path.join(DATA, "slicer.json")),
    "mods": load(os.path.join(DATA, "mods.json")),
    "models": load(os.path.join(DATA, "models.json")),
}
data_json = json.dumps(bundle, ensure_ascii=False).replace("</", "<\\/")

HTML = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bible Kobra S1 Combo — Tableau de bord</title>
<style>
  :root{
    --bg:#0e1014; --panel:#181b22; --panel2:#1f232c; --line:#2a2f3a;
    --txt:#e7e9ee; --muted:#9aa1ad; --accent:#ff7a18; --accent2:#ffb347;
    --ok:#3ecf8e; --warn:#ffcc4d; --bad:#ff6b6b; --blue:#5aa9ff;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--txt);font:15px/1.55 system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
  a{color:var(--accent2);text-decoration:none} a:hover{text-decoration:underline}
  header{position:sticky;top:0;z-index:20;background:linear-gradient(180deg,#14171d,#0e1014);border-bottom:1px solid var(--line);padding:14px 20px 0}
  .htop{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
  h1{font-size:19px;margin:0}
  h1 .sub{color:var(--accent);font-weight:600}
  .pill{background:var(--panel2);border:1px solid var(--line);border-radius:999px;padding:2px 10px;font-size:12px;color:var(--muted)}
  nav{display:flex;gap:4px;flex-wrap:wrap;margin-top:12px}
  nav button{background:transparent;border:0;border-bottom:2px solid transparent;color:var(--muted);padding:9px 12px;font-size:14px;cursor:pointer;border-radius:6px 6px 0 0}
  nav button:hover{color:var(--txt);background:var(--panel)}
  nav button.on{color:var(--accent);border-bottom-color:var(--accent);background:var(--panel)}
  main{max-width:1180px;margin:0 auto;padding:22px 20px 80px}
  section.tab{display:none} section.tab.on{display:block}
  h2{font-size:17px;margin:26px 0 12px;color:var(--accent2);border-left:3px solid var(--accent);padding-left:10px}
  h3{font-size:15px;margin:18px 0 8px;color:var(--txt)}
  .grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}
  .fact{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
  .fact .k{color:var(--accent);font-size:12px;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px}
  .rules{list-style:none;padding:0;margin:0;display:grid;gap:8px}
  .rules li{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:8px;padding:10px 12px}
  .kvs{display:grid;gap:8px}
  .kv{display:grid;grid-template-columns:200px 1fr;gap:12px;padding:8px 0;border-bottom:1px solid var(--line)}
  .kv .k{color:var(--accent2);font-weight:600;font-size:13px}
  .cards{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(280px,1fr))}
  .mini{background:var(--panel2);border:1px solid var(--line);border-radius:9px;padding:10px 12px}
  .mini .kv{grid-template-columns:130px 1fr;padding:5px 0}
  ul.bul{margin:4px 0;padding-left:18px} ul.bul li{margin:2px 0}
  .muted{color:var(--muted)}
  .panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:10px 0}
  /* ----- Modèles ----- */
  .controls{position:sticky;top:96px;z-index:10;background:var(--bg);padding:10px 0;display:flex;gap:10px;flex-wrap:wrap;align-items:center;border-bottom:1px solid var(--line)}
  .controls input[type=search],.controls select{background:var(--panel2);border:1px solid var(--line);color:var(--txt);border-radius:8px;padding:8px 10px;font-size:14px}
  .controls input[type=search]{min-width:240px;flex:1}
  .controls label{font-size:13px;color:var(--muted);display:flex;align-items:center;gap:6px}
  .count{font-size:13px;color:var(--muted);margin:10px 0}
  .mgrid{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));align-items:start}
  .model{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:12px 14px}
  .model h4{margin:0 0 6px;font-size:14.5px}
  .badges{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}
  .b{font-size:11px;border-radius:6px;padding:2px 7px;border:1px solid var(--line);background:var(--panel2);color:var(--muted)}
  .b.diff-tres_facile{color:var(--ok);border-color:#22543d}
  .b.diff-facile{color:var(--ok);border-color:#22543d}
  .b.diff-moyen{color:var(--warn);border-color:#5c4a12}
  .b.diff-difficile{color:var(--bad);border-color:#5c2222}
  .b.diff-expert{color:var(--bad);border-color:#5c2222}
  .b.ace{color:#0e1014;background:var(--accent);border-color:var(--accent);font-weight:600}
  .b.sup{color:var(--blue);border-color:#244}
  .chips{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:8px}
  .chip{font-size:11px;color:var(--accent2);background:rgba(255,122,24,.08);border:1px solid rgba(255,122,24,.25);border-radius:999px;padding:1px 8px;cursor:pointer}
  .why{font-size:13.5px;color:#d6d9e0;margin:6px 0}
  .mmeta{font-size:12px;color:var(--muted);margin-top:6px}
  .btn{display:inline-block;margin-top:8px;font-size:12.5px;background:var(--panel2);border:1px solid var(--line);border-radius:7px;padding:5px 10px;color:var(--accent2)}
  details{margin-top:6px;font-size:12.5px;color:var(--muted)}
  .foot{margin-top:40px;color:var(--muted);font-size:12px;border-top:1px solid var(--line);padding-top:14px}
  .secsub{margin-top:30px}
</style>
</head>
<body>
<header>
  <div class="htop">
    <h1>🖨️ Bible <span class="sub">Anycubic Kobra S1 Combo</span> + ACE Pro</h1>
    <span class="pill" id="pillModels"></span>
    <span class="pill" id="pillCompiled"></span>
  </div>
  <nav id="nav"></nav>
</header>
<main>
  <section class="tab" data-tab="apercu" id="t-apercu"></section>
  <section class="tab" data-tab="machine" id="t-machine"></section>
  <section class="tab" data-tab="filaments" id="t-filaments"></section>
  <section class="tab" data-tab="slicer" id="t-slicer"></section>
  <section class="tab" data-tab="mods" id="t-mods"></section>
  <section class="tab" data-tab="entretien" id="t-entretien"></section>
  <section class="tab on" data-tab="modeles" id="t-modeles"></section>
</main>
<script>
const DATA = __DATA_JSON__;

/* ---------- helpers ---------- */
function esc(s){const d=document.createElement('div');d.textContent=(s==null?'':String(s));return d.innerHTML;}
function isUrl(s){return typeof s==='string' && /^https?:\/\//.test(s);}
function human(k){return k.replace(/_/g,' ').replace(/\b\w/g,c=>c.toUpperCase());}
function link(u,label){return '<a href="'+esc(u)+'" target="_blank" rel="noopener">'+esc(label||u)+'</a>';}
function renderAny(v){
  if(v===null||v===undefined||v==='') return '<span class="muted">—</span>';
  if(Array.isArray(v)){
    if(!v.length) return '<span class="muted">—</span>';
    if(v.every(x=>x===null||typeof x!=='object'))
      return '<ul class="bul">'+v.map(x=>'<li>'+(isUrl(x)?link(x):esc(x))+'</li>').join('')+'</ul>';
    return '<div class="cards">'+v.map(x=>'<div class="mini">'+renderAny(x)+'</div>').join('')+'</div>';
  }
  if(typeof v==='object'){
    let r='';
    for(const[k,val] of Object.entries(v)){
      if(k==='_meta') continue;
      r+='<div class="kv"><div class="k">'+esc(human(k))+'</div><div class="val">'+renderAny(val)+'</div></div>';
    }
    return '<div class="kvs">'+r+'</div>';
  }
  if(isUrl(v)) return link(v);
  return esc(v);
}
function block(obj){ // render a data-file object minus _meta, sources last
  return renderAny(obj);
}

/* ---------- nav ---------- */
const TABS=[['apercu','🧭 Aperçu'],['machine','⚙️ Machine'],['filaments','🧵 Filaments'],
['slicer','🪄 Slicer & purge'],['mods','🔧 Mods'],['entretien','🩺 Entretien & pannes'],['modeles','🗂️ Modèles']];
const nav=document.getElementById('nav');
TABS.forEach(([id,label])=>{
  const b=document.createElement('button');b.textContent=label;b.dataset.t=id;
  if(id==='modeles')b.classList.add('on');
  b.onclick=()=>{document.querySelectorAll('nav button').forEach(x=>x.classList.remove('on'));
    b.classList.add('on');
    document.querySelectorAll('section.tab').forEach(s=>s.classList.toggle('on',s.dataset.tab===id));
    window.scrollTo(0,0);};
  nav.appendChild(b);
});

/* ---------- pills ---------- */
document.getElementById('pillModels').textContent=DATA.models.models.length+' modèles · '+DATA.models.categories.length+' catégories';
document.getElementById('pillCompiled').textContent='compilé '+(DATA.manifest._meta.compiled||'');

/* ---------- Aperçu ---------- */
(function(){
  const m=DATA.manifest;
  let h='<h2>Quick facts</h2><div class="grid">';
  for(const[k,v] of Object.entries(m.quick_facts||{}))
    h+='<div class="fact"><div class="k">'+esc(human(k))+'</div><div>'+esc(v)+'</div></div>';
  h+='</div><h2>Règles d\'or</h2><ol class="rules">';
  (m.golden_rules||[]).forEach(r=>h+='<li>'+esc(r)+'</li>');
  h+='</ol>';
  document.getElementById('t-apercu').innerHTML=h;
})();

/* ---------- generic tabs ---------- */
document.getElementById('t-machine').innerHTML='<h2>Machine & ACE Pro</h2>'+block(DATA.printer)+'<h2 class="secsub">Calibrations</h2>'+block(DATA.calibration);
document.getElementById('t-filaments').innerHTML='<h2>Guide des filaments</h2>'+block(DATA.materials);
document.getElementById('t-slicer').innerHTML='<h2>Slicer, profils, purge & séchage</h2>'+block(DATA.slicer);
document.getElementById('t-mods').innerHTML='<h2>Mods, firmware & upgrades</h2>'+block(DATA.mods);
document.getElementById('t-entretien').innerHTML='<h2>Maintenance</h2>'+block(DATA.maintenance)+'<h2 class="secsub">Pannes & codes d\'erreur</h2>'+block(DATA.troubleshooting)+'<h2 class="secsub">Consommables</h2>'+block(DATA.consumables);

/* ---------- Modèles (interactif) ---------- */
(function(){
  const M=DATA.models, models=M.models;
  const cats={}; models.forEach(m=>(m.categories||[]).forEach(c=>cats[c]=(cats[c]||0)+1));
  const catList=Object.keys(cats).sort();
  const diffs=['tres_facile','facile','moyen','difficile','expert'];
  const root=document.getElementById('t-modeles');
  root.innerHTML=
   '<h2>Catalogue — '+models.length+' modèles</h2>'+
   '<p class="muted">'+esc(M.purge_principle||'')+'</p>'+
   '<div class="controls">'+
     '<input type="search" id="q" placeholder="Rechercher (nom, description, tag)…">'+
     '<select id="cat"><option value="">Toutes catégories</option>'+catList.map(c=>'<option value="'+c+'">'+esc(human(c))+' ('+cats[c]+')</option>').join('')+'</select>'+
     '<select id="diff"><option value="">Toutes difficultés</option>'+diffs.map(d=>'<option value="'+d+'">'+esc(human(d))+'</option>').join('')+'</select>'+
     '<label><input type="checkbox" id="ace"> ACE-friendly</label>'+
     '<label><input type="checkbox" id="sup"> Sans supports</label>'+
   '</div>'+
   '<div class="count" id="count"></div>'+
   '<div class="mgrid" id="mgrid"></div>'+
   '<div class="secsub"><h2>Systèmes modulaires ('+(M.systems||[]).length+')</h2>'+renderAny(M.systems)+'</div>'+
   '<div class="secsub"><h2>Modèles de calibration ('+(M.calibration_models||[]).length+')</h2>'+renderAny(M.calibration_models)+'</div>'+
   '<div class="secsub"><h2>Raccourcis de recherche</h2>'+renderAny(M.search_shortcuts)+'</div>'+
   '<div class="foot">Source de vérité : <code>data/models.json</code>. Notes de thème ('+(M.theme_notes||[]).length+') et sources dans le JSON.</div>';

  const q=root.querySelector('#q'), cat=root.querySelector('#cat'), diff=root.querySelector('#diff'),
        ace=root.querySelector('#ace'), sup=root.querySelector('#sup'),
        grid=root.querySelector('#mgrid'), count=root.querySelector('#count');

  function card(m){
    const url=m.url;
    let b='';
    if(m.difficulty)b+='<span class="b diff-'+esc(m.difficulty)+'">'+esc(human(m.difficulty))+'</span>';
    if(m.ace_pro_friendly)b+='<span class="b ace">ACE ✓</span>';
    if(m.multicolor && m.multicolor!=='mono' && m.multicolor!=='none')b+='<span class="b">'+esc(human(m.multicolor))+'</span>';
    if(m.supports_free===true)b+='<span class="b sup">sans support</span>';
    const chips=(m.categories||[]).map(c=>'<span class="chip" data-c="'+esc(c)+'">'+esc(human(c))+'</span>').join('');
    const meta=[ (m.material&&m.material.length)?m.material.join(', '):null, m.time||null, m.platform||null ].filter(Boolean).map(esc).join(' · ');
    return '<div class="model">'+
      '<h4>'+(url?link(url,m.name):esc(m.name))+'</h4>'+
      '<div class="badges">'+b+'</div>'+
      (chips?'<div class="chips">'+chips+'</div>':'')+
      (m.why?'<div class="why">'+esc(m.why)+'</div>':'')+
      (meta?'<div class="mmeta">'+meta+'</div>':'')+
      (url?'<a class="btn" href="'+esc(url)+'" target="_blank" rel="noopener">Ouvrir ↗</a>':'')+
      (m.notes?'<details><summary>Notes</summary>'+esc(m.notes)+'</details>':'')+
    '</div>';
  }
  function apply(){
    const s=(q.value||'').toLowerCase().trim(), c=cat.value, d=diff.value, a=ace.checked, su=sup.checked;
    const out=models.filter(m=>{
      if(c && !(m.categories||[]).includes(c)) return false;
      if(d && m.difficulty!==d) return false;
      if(a && !m.ace_pro_friendly) return false;
      if(su && m.supports_free!==true) return false;
      if(s){
        const hay=((m.name||'')+' '+(m.why||'')+' '+((m.tags||[]).join(' '))+' '+((m.categories||[]).join(' '))).toLowerCase();
        if(!hay.includes(s)) return false;
      }
      return true;
    });
    count.textContent=out.length+' modèle'+(out.length>1?'s':'')+' affiché'+(out.length>1?'s':'');
    grid.innerHTML=out.map(card).join('') || '<p class="muted">Aucun résultat.</p>';
    grid.querySelectorAll('.chip').forEach(ch=>ch.onclick=()=>{cat.value=ch.dataset.c;apply();});
  }
  [q,cat,diff,ace,sup].forEach(e=>e.addEventListener('input',apply));
  apply();
})();
</script>
</body>
</html>
"""

out = HTML.replace("__DATA_JSON__", data_json)
dest = os.path.join(ROOT, "Dashboard-Kobra-S1.html")
with open(dest, "w", encoding="utf-8") as f:
    f.write(out)
print("Dashboard écrit :", os.path.abspath(dest))
print("Taille :", round(len(out)/1024), "Ko |", len(bundle["models"]["models"]), "modèles embarqués")
