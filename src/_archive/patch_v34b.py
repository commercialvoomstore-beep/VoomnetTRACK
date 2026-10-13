#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.4b — Téléchargement DIRECT vers l'appareil en priorité (dossier Téléchargements),
avec « Choisir l'emplacement… » à la demande et aide si l'aperçu bloque."""
p = 'src/part3_core.js.html'
s = open(p, encoding='utf-8').read()

start = s.index("/* -------- 5b. ENREGISTREMENT SUR L'APPAREIL")
end = s.index("/* Compat : ancien nom conservé */")

NEW = r'''/* -------- 5b. ENREGISTREMENT SUR L'APPAREIL (jamais « dans l'application ») ------- */
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
/* 1. TÉLÉCHARGEMENT DIRECT : le fichier part immédiatement dans le dossier
      « Téléchargements » de l'appareil. Universel, sans boîte de dialogue. */
function downloadToDevice(blob,filename){
  try{
    const url=URL.createObjectURL(blob);
    const a=document.createElement("a");
    a.href=url; a.download=filename; a.rel="noopener"; a.style.display="none";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function(){ URL.revokeObjectURL(url); },10000);
    return true;
  }catch(e){ return false; }
}
/* 2. « ENREGISTRER SOUS » : choix libre du dossier (Bureau, Documents, clé USB).
      Proposé À LA DEMANDE, car certains navigateurs annulent la boîte automatiquement. */
async function saveWithPicker(blob,filename){
  if(!canSavePicker()) return {ok:false,mode:"unsupported"};
  try{
    const t=mimeType(blob.type,filename);
    const handle=await window.showSaveFilePicker(Object.assign({suggestedName:filename}, t?{types:[t]}:{}));
    const w=await handle.createWritable(); await w.write(blob); await w.close();
    return {ok:true,mode:"picker",name:handle.name||filename};
  }catch(err){
    if(err&&err.name==="AbortError") return {ok:false,mode:"abort"};
    if(downloadToDevice(blob,filename)) return {ok:true,mode:"download",name:filename,sandboxed:sandboxedHere()};
    return {ok:false,mode:"error",err:err};
  }
}
/* Enregistre un fichier SUR L'APPAREIL (téléchargement direct par défaut) */
function saveToDevice(blob,filename){
  return new Promise(function(resolve){
    const ok=downloadToDevice(blob,filename);
    resolve({ok:ok,mode:"download",name:filename,sandboxed:sandboxedHere()});
  });
}
/* Boîte d'aide : quand l'aperçu (iframe) empêche le téléchargement */
function openSaveHelp(filename,onRetry,blob){
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
     '<div class="tx">Le fichier part alors directement dans le dossier « Téléchargements » de votre appareil. '+
     'Utilisez « Choisir l\'emplacement… » pour l\'enregistrer sur le Bureau ou une clé USB.</div></div></div>'+
   '</div>'+
   '<div class="save-url"><span class="ic" data-ico="key"></span><code id="saveUrlTxt">'+esc(url)+'</code>'+
   '<button class="btn btn-ghost btn-sm" id="saveUrlCopy">'+ic("doc")+' Copier le lien</button></div></div>'+
   '<footer><button class="btn btn-ghost" data-close>Fermer</button>'+
   (canSavePicker()? '<button class="btn btn-primary" id="savePicker">'+ic("save")+' Choisir l\'emplacement…</button>' : '')+
   (blob? '<button class="btn btn-ghost" id="saveRetry">'+ic("download")+' Réessayer ici</button>' : '')+
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
  const sp=$("#savePicker",box);
  if(sp&&blob) sp.onclick=async function(){
    const r=await saveWithPicker(blob,filename);
    if(r.mode==="abort") return;
    if(r.ok){ bg.classList.remove("on"); toast("Enregistré sur votre appareil ✅",(r.name||filename)+" — à l'emplacement choisi."); }
    else toast("Enregistrement impossible","Utilisez « Ouvrir dans un onglet » puis le bouton doré.","err");
  };
}
/* Raccourci commun : enregistre puis message adapté (et aide si l'aperçu bloque) */
function saveAndTell(blob,filename,onRetry){
  return saveToDevice(blob,filename).then(function(res){
    const ko=Math.round(blob.size/1024);
    if(res.ok&&!res.sandboxed) toast("Enregistré sur votre appareil ✅", filename+" ("+ko+" Ko) → dossier « Téléchargements ».");
    else if(res.ok) { toast("Téléchargement lancé","Si le fichier n'arrive pas, ouvrez l'application dans un onglet.","info"); openSaveHelp(filename,onRetry,blob); }
    else { openSaveHelp(filename,onRetry,blob); toast("2 étapes pour enregistrer","L'aperçu bloque les téléchargements : ouvrez l'application dans un onglet.","info"); }
    return res;
  });
}
'''
s = s[:start] + NEW + s[end:]
open(p, 'w', encoding='utf-8').write(s)
print("✓ téléchargement direct prioritaire + « Choisir l'emplacement… » à la demande")

# --- bouton secondaire « Choisir l'emplacement… » dans la vue Rapports -------
p2 = 'src/part2_body.html'
b = open(p2, encoding='utf-8').read()
old = '<button class="btn btn-gold btn-lg btn-block" id="btnPdf"><span class="ic" data-ico="pdf"></span> Télécharger le PDF</button>'
new = ('<button class="btn btn-gold btn-lg btn-block" id="btnPdf"><span class="ic" data-ico="pdf"></span> Télécharger le PDF</button>'
       '\n              <button class="btn btn-ghost btn-block" id="btnPdfSaveAs"><span class="ic" data-ico="save"></span> Choisir l\'emplacement…</button>')
assert old in b
b = b.replace(old, new, 1)
open(p2, 'w', encoding='utf-8').write(b)
print("✓ bouton « Choisir l'emplacement… » dans Rapports")

# --- branchement du bouton ------------------------------------------------
p3 = 'src/part3b_dash.js.html'
d = open(p3, encoding='utf-8').read()
anchor = '  $("#btnPdfOpen").onclick=()=>buildPDF(false);'
assert anchor in d
d = d.replace(anchor, anchor + '''

  /* « Choisir l'emplacement… » : enregistrement PDF au dossier choisi (Bureau, clé USB) */
  const bsa=$("#btnPdfSaveAs");
  if(bsa) bsa.onclick=()=>buildPDF("picker");''', 1)
open(p3, 'w', encoding='utf-8').write(d)
print("✓ bouton branché (buildPDF(\"picker\"))")

# --- buildPDF : accepter le mode « picker » --------------------------------
p4 = 'src/part4_pdf.js.html'
f = open(p4, encoding='utf-8').read()
old = '''  if(thenDownload){
    /* enregistrement SUR L'APPAREIL : « Enregistrer sous », ou dossier Téléchargements */
    saveAndTell(blob,fname,function(){ buildPDF(true); });
    return;
  }else{'''
new = '''  if(thenDownload==="picker"){
    /* « Enregistrer sous » : l'utilisateur choisit l'emplacement sur son appareil */
    saveWithPicker(blob,fname).then(function(r){
      if(r.mode==="abort") return;
      if(r.ok) toast("Enregistré sur votre appareil ✅",(r.name||fname)+" ("+Math.round(bytes.length/1024)+" Ko) — à l'emplacement choisi.");
      else { saveAndTell(blob,fname,function(){ buildPDF(true); }); }
    });
    return;
  }
  if(thenDownload){
    /* téléchargement DIRECT → dossier « Téléchargements » de l'appareil */
    saveAndTell(blob,fname,function(){ buildPDF(true); });
    return;
  }else{'''
assert old in f
f = f.replace(old, new, 1)
open(p4, 'w', encoding='utf-8').write(f)
print("✓ buildPDF gère le mode « picker »")
