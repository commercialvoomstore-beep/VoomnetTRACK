/* Harnais de test : exécute l'application dans un DOM simulé et génère le PDF. */
import fs from "node:fs";
import vm from "node:vm";

const html = fs.readFileSync("/home/user/index.html", "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
console.log("scripts trouvés :", scripts.length);

/* ---------- DOM simulé ---------- */
const els = {};
function mkEl(id) {
  const e = {
    id, value: "", checked: false, innerHTML: "", textContent: "", textContentSet: null,
    dataset: {}, style: {}, files: [], href: "", download: "", rel: "",
    classList: { _s: new Set(), add(c){this._s.add(c);}, remove(c){this._s.delete(c);},
                 toggle(c,v){ v===undefined? (this._s.has(c)?this._s.delete(c):this._s.add(c)) : (v?this._s.add(c):this._s.delete(c)); },
                 contains(c){ return this._s.has(c); } },
    addEventListener(){}, appendChild(){}, remove(){}, click(){}, focus(){},
    querySelector(){ return null; }, querySelectorAll(){ return []; },
    getContext(){ return null; }, onclick: null, onchange: null, scrollTo(){}, insertAdjacentHTML(){}, closest(){ return null; },
  };
  return e;
}
const listeners = {};
let capturedBlob = null;
const document = {
  querySelector(sel){ const k = String(sel).replace(/^#/,""); return els[k] || (els[k] = mkEl(k)); },
  querySelectorAll(){ return []; },
  createElement(t){ return mkEl("new:"+t); },
  addEventListener(ev, fn){ listeners[ev] = fn; },
  body: mkEl("body"),
};
const store = {};
const localStorage = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = String(v); },
  removeItem: k => { delete store[k]; },
};
const sandbox = {
  console, Intl, Date, Math, JSON, Object, Array, String, Number, Boolean, Error, RegExp, Map, Set, Promise,
  atob: (s) => Buffer.from(s, "base64").toString("binary"),
  setTimeout, clearTimeout,
  Blob: class Blob { constructor(parts){ this._p = parts; } async arrayBuffer(){
      const bufs = this._p.map(p => Buffer.isBuffer(p)? p : Buffer.from(p));
      const b = Buffer.concat(bufs);
      return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength);
    } },
  URL: { createObjectURL(b){ capturedBlob = b; return "blob:mock"; }, revokeObjectURL(){} },
  navigator: { userAgent: "node" },
  scrollTo(){}, matchMedia(){ return { matches:false, addEventListener(){} }; },
  document, localStorage, window: null,
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;
const ctx = vm.createContext(sandbox);

/* ---------- exécution ---------- */
try {
  ctx.__scripts = scripts;
  vm.runInContext(scripts[0], ctx, { filename: "core.js" });
  console.log("✔ core.js chargé");
  if (scripts[1]) { vm.runInContext(scripts[1], ctx, { filename: "pdf.js" }); console.log("✔ pdf.js chargé"); }
} catch (e) {
  console.error("✘ Erreur de chargement :", e.message, "\n", (e.stack||"").split("\n").slice(0,4).join("\n"));
  process.exit(1);
}

/* ---------- init ---------- */
try { listeners["DOMContentLoaded"] && listeners["DOMContentLoaded"](); }
catch (e) { console.error("✘ Erreur dans init() :", e.message, "\n", (e.stack||"").split("\n").slice(0,6).join("\n")); process.exit(1); }
console.log("✔ init() exécuté");

/* ---------- données + PDF ---------- */
const run = (code) => vm.runInContext(code, ctx, { filename: "test.js" });
try {
  const info = run(`(()=>{ const m=currentMonth();
    $("#rMonth").value=m; $("#rService").value=""; $("#rAgent").value="";
    $("#rDetail").checked=true; $("#rSign").checked=true; $("#rLogos").checked=true;
    return JSON.stringify({seedTrips:DB.trips.length, month:m, total:sum(tripsOf(m)), services:SERVICES.length, logos:Object.keys(LOGOS).length, bytes:logoBytes("tech").length}); })()`);
  console.log("état app :", info);
  run(`buildPDF(true)`);
} catch (e) {
  console.error("✘ Erreur PDF :", e.message, "\n", (e.stack||"").split("\n").slice(0,8).join("\n"));
  process.exit(1);
}

if (!capturedBlob) { console.error("✘ Aucun blob capturé"); process.exit(1); }
const buf = Buffer.from(await capturedBlob.arrayBuffer());
fs.mkdirSync("/home/user/test", { recursive: true });
fs.writeFileSync("/home/user/test/rapport.pdf", buf);
console.log("✔ PDF généré :", buf.length, "octets");
