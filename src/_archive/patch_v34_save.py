#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.4 — Enregistrement SUR L'APPAREIL (PDF / CSV / JSON)."""
import io, sys

# ---------------------------------------------------------------- 1. noyau
p = 'src/part3_core.js.html'
s = open(p, encoding='utf-8').read()

start = s.index('function downloadBlob(blob, filename){')
end = s.index('\n}\n', start) + 3

NEW = r'''/* -------- 5b. ENREGISTREMENT SUR L'APPAREIL (jamais « dans l'application ») -------- */
function isFramed(){ try{ return window.self!==window.top; }catch(e){ return true; } }
/* iframe d'aperçu au bac à sable → le navigateur bloque volontairement les téléchargements */
function sandboxedHere(){
  if(!isFramed()) return false;
  try{ void window.top.location.href; return false; }catch(e){ return true; }
}
function canSavePicker(){ return !isFramed() && typeof window.showSaveFilePicker==="function"; }
function mimeType(type,name){
  if(type==="application/pdf"||/\.pdf$/i.test(name)) return {description:"Document PDF",accept:{"application/pdf":[".pdf"]}};
  if(/csv/i.test(type||"")||/\.csv$/i.test(name))    return {description:"Fichier CSV (tableur)",accept:{"text/csv":[".csv"]}};
  if(/json/i.test(type||"")||/\.json$/i.test(name))  return {description:"Sauvegarde JSON",accept:{"application/json":[".json"]}};
  return null;
}
/* Enregistre un fichier SUR L'APPAREIL :
   1) « Enregistrer sous » natif — l'utilisateur choisit Bureau / Documents / clé USB ;
   2) sinon téléchargement classique → dossier « Téléchargements » de l'appareil. */
function saveToDevice(blob,filename){
  return new Promise(function(resolve){
    (async function(){
      if(canSavePicker()){
        try{
          const t=mimeType(blob.type,filename);
          const handle=await window.showSaveFilePicker(Object.assign({suggestedName:filename}, t?{types:[t]}:{}) );
          const w=await handle.createWritable(); await w.write(blob); await w.close();
          resolve({ok:true,mode:"picker",name:handle.name||filename}); return;
        }catch(err){
          if(err&&err.name==="AbortError"){ resolve({ok:false,mode:"abort"}); return; }
        }
      }
      try{
        const url=URL.createObjectURL(blob);
        const a=document.createElement("a");
        a.href=url; a.download=filename; a.rel="noopener"; a.style.display="none";
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function(){ URL.revokeObjectURL(url); },8000);
        resolve({ok:true,mode:"download",name:filename,sandboxed:sandboxedHere()});
      }catch(err){ resolve({ok:false,mode:"error",err:err}); }
    })();
  });
}
/* Boîte d'aide : deux étapes claires quand l'aperçu bloque le téléchargement */
function openSaveHelp(filename,onRetry){
  const bg=$("#modalBg"), box=$("#modalBox"), url=location.href, framed=isFramed();
  box.innerHTML =
   '<header><div><h3>Enregistrer sur votre appareil</h3>'+
   '<div class="sub">'+esc(filename)+' — le fichier doit arriver dans vos téléchargements, pas rester dans l\'aperçu.</div></div>'+
   '<button class="x" data-close>'+ic("x")+'</button></header>'+
   '<div class="bd"><div class="save-steps">'+
     '<div class="sstep"><span class="n">1</span><div><b>Ouvrez l\'application dans un onglet</b>'+
     '<div class="tx">'+(framed? 'Vous êtes dans une fenêtre d\'aperçu, qui bloque volontairement les téléchargements. ' : '')+
     'Cliquez sur le bouton doré ci-dessous : l\'application s\'ouvre normalement dans votre navigateur.</div></div></div>'+
     '<div class="sstep"><span class="n">2</span><div><b>Cliquez sur « Télécharger le PDF »</b>'+
     '<div class="tx">Le navigateur ouvre alors « Enregistrer sous » : choisissez Bureau, Documents ou votre clé USB. Le fichier est enregistré sur l\'appareil.</div></div></div>'+
   '</div>'+
   '<div class="save-url"><span class="ic" data-ico="key"></span><code id="saveUrlTxt">'+esc(url)+'</code>'+
   '<button class="btn btn-ghost btn-sm" id="saveUrlCopy">'+ic("doc")+' Copier le lien</button></div></div>'+
   '<footer><button class="btn btn-ghost" data-close>Fermer</button>'+
   '<button class="btn btn-primary" id="saveRetry">'+ic("download")+' Réessayer ici</button>'+
   '<a class="btn btn-gold" href="'+esc(url)+'" target="_blank" rel="noopener">'+ic("arrowRight")+' Ouvrir dans un onglet</a></footer>';
  hydrateIcons(box); bg.classList.add("on");
  $$("[data-close]",bg).forEach(function(b){ b.onclick=function(){ bg.classList.remove("on"); }; });
  const cp=$("#saveUrlCopy",box);
  if(cp) cp.onclick=async function(){
    try{ await navigator.clipboard.writeText(url); toast("Lien copié","Collez-le dans la barre d'adresse de votre navigateur.","ok"); }
    catch(e){ const t=$("#saveUrlTxt",box); const r=document.createRange(); r.selectNodeContents(t);
      const sel=getSelection(); sel.removeAllRanges(); sel.addRange(r); toast("Lien sélectionné","Appuyez sur Ctrl+C pour le copier.","info"); }
  };
  const rt=$("#saveRetry",box);
  if(rt) rt.onclick=function(){ bg.classList.remove("on"); onRetry&&onRetry(); };
}
/* Raccourci commun : enregistre puis message adapté (et aide si l'aperçu bloque) */
function saveAndTell(blob,filename,onRetry){
  return saveToDevice(blob,filename).then(function(res){
    const ko=Math.round(blob.size/1024);
    if(res.mode==="abort") return res;
    if(res.ok&&res.mode==="picker")  toast("Enregistré sur votre appareil ✅", filename+" ("+ko+" Ko) — à l'emplacement choisi.");
    else if(res.ok&&!res.sandboxed)  toast("Téléchargement lancé ✅", filename+" ("+ko+" Ko) → dossier « Téléchargements » de votre appareil.");
    else { openSaveHelp(filename,onRetry); toast("2 étapes pour enregistrer","L'aperçu bloque les téléchargements : ouvrez l'application dans un onglet.","info"); }
    return res;
  });
}
/* Compat : ancien nom conservé */
function downloadBlob(blob,filename){
  try{ const url=URL.createObjectURL(blob); const a=document.createElement("a");
    a.href=url; a.download=filename; a.rel="noopener"; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function(){ URL.revokeObjectURL(url); },8000); return true; }catch(e){ return false; }
}
'''
s = s[:start] + NEW + s[end:]

# CSV
old_csv = '''function exportCsv(list,name){
  const ok=downloadBlob(new Blob([csvOf(list)],{type:"text/csv;charset=utf-8"}), name);
  toast(ok?"Export CSV prêt":"Téléchargement bloqué",
        ok? name+" a été généré." : "Ouvrez index.html directement dans votre navigateur.", ok?"ok":"err");
}'''
new_csv = '''function exportCsv(list,name){
  saveAndTell(new Blob([csvOf(list)],{type:"text/csv;charset=utf-8"}), name, function(){ exportCsv(list,name); });
}'''
assert old_csv in s, 'exportCsv introuvable'
s = s.replace(old_csv, new_csv, 1)

old_json = s[s.index('function doBackup(){'):]
old_json = old_json[:old_json.index('\n}\n') + 3]
new_json = '''function doBackup(){
  const blob=new Blob([JSON.stringify({
    trips:DB.trips,agents:DB.agents,transports:DB.transports,vehicles:DB.vehicles,
    params:DB.params,meta:DB.meta,user:DB.user,accounts:DB.accounts},null,1)],{type:"application/json"});
  saveAndTell(blob,"VOOMNET_Track_sauvegarde_"+todayISO()+".json",function(){ doBackup(); });
}
'''
s = s.replace(old_json, new_json, 1)
open(p,'w',encoding='utf-8').write(s)
print("✓ noyau : enregistrement sur l'appareil (PDF / CSV / JSON)")

# ---------------------------------------------------------------- 2. bouton PDF
p2 = 'src/part4_pdf.js.html'
s2 = open(p2, encoding='utf-8').read()
old = s2[s2.index('  if(thenDownload){'):]
old = old[:old.index('  }else{')]
new = '''  if(thenDownload){
    /* enregistrement SUR L'APPAREIL : « Enregistrer sous », ou dossier Téléchargements */
    saveAndTell(blob,fname,function(){ buildPDF(true); });
    return;
'''
s2 = s2.replace(old, new, 1)
open(p2,'w',encoding='utf-8').write(s2)
print("✓ bouton « Télécharger le PDF » branché sur l'enregistrement appareil")
