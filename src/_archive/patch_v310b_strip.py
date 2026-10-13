# -*- coding: utf-8 -*-
"""v3.10b — bandeau des logos du PDF : grille reguliere + libelle Direction."""
import io, sys

P = "src/part4_pdf.js.html"
s = io.open(P, encoding="utf-8").read()
orig = s

OLD = '''  /* --- Bandeau des logos --- */
  y=H-72-6;
  const stripH=44;
  roundRect(ML, y-stripH, CW, stripH, 8, "#FFFFFF", {border:C.line, lw:0.8});
  const stripY=y-stripH, midY=stripY+stripH/2;
  let groupW=0; const lg=[];
  cfg.strip.forEach(k=>{ const m=cfg.images[k]; if(!m) return; const h=21, w=h*m.w/m.h; lg.push({k:k,w:w,h:h}); groupW+=w; });
  groupW+= (lg.length-1)*20;
  let gx=ML+(CW-groupW)/2;
  lg.forEach((g,i)=>{ img(g.k, gx, midY-10.5, 21, g.w, "left");
    const cx=gx+g.w/2, cy=midY-6.5;
    text(cfg.images[g.k].label, cx-46, cy, 6.4, {color:C.muted,align:"center",w:92});
    gx+=g.w;
    if(i<lg.length-1){ gx+=10; hline(gx, gx, stripY+9, C.line, 0.8); add(strokeOp(C.line)+" 1 w "+n3(gx)+" "+n3(stripY+9)+" m "+n3(gx)+" "+n3(stripY+35)+" l S"); gx+=10; }
  });'''

NEW = '''  /* --- Bandeau des logos : une colonne reguliere par entite (aucun chevauchement) --- */
  y=H-72-6;
  const stripH=44;
  roundRect(ML, y-stripH, CW, stripH, 8, "#FFFFFF", {border:C.line, lw:0.8});
  const stripY=y-stripH;
  const lg=[];
  cfg.strip.forEach(k=>{ const m=cfg.images[k]; if(!m) return; lg.push({k:k,m:m}); });
  const slotW=CW/Math.max(1,lg.length);
  lg.forEach((g,i)=>{
    const cx=ML+slotW*(i+0.5);
    const maxW=slotW-14, labW=slotW-8;
    img(g.k, cx-maxW/2, stripY+14, 20, maxW, "center");   /* image centree dans sa colonne */
    text(fit(g.m.label,6.3,false,labW), cx-labW/2, stripY+7.6, 6.3, {color:C.muted,align:"center",w:labW});
    if(i<lg.length-1){
      const sx=ML+slotW*(i+1);
      add(strokeOp(C.line)+" 0.8 w "+n3(sx)+" "+n3(stripY+9)+" m "+n3(sx)+" "+n3(stripY+35)+" l S");
    }
  });'''

assert OLD in s, "bloc bandeau introuvable"
s = s.replace(OLD, NEW, 1)

OLD2 = '''    images[k]={ idx:i, w:m.w, h:m.h, label:({
      tech:"VOOMNET TECHNOLOGY", encaci:"ENCACI", form:"VOOMNET FORMATION", head:"VOOMNET"})[k]||"" };'''
NEW2 = '''    images[k]={ idx:i, w:m.w, h:m.h, label:({
      tech:"VOOMNET TECHNOLOGY", encaci:"ENCACI", form:"VOOMNET FORMATION",
      direction:"DIRECTION G\\u00C9N\\u00C9RALE", head:"VOOMNET"})[k]||"" };'''
assert OLD2 in s, "mappe des libelles introuvable"
s = s.replace(OLD2, NEW2, 1)

assert s != orig
io.open(P, "w", encoding="utf-8").write(s)
print("patch v3.10b applique")
for k in ["const slotW=CW", "DIRECTION G\\u00C9N\\u00C9RALE", "cx-maxW/2, stripY+14, 20, maxW"]:
    print("  verif", k[:26], "->", k in s)
