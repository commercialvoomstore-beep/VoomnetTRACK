/* Données de départ (aucun secret) — partagées par db/seed.js et POST /api/init. */
"use strict";
const COLLABS = [
  { id: "C-WILFRIED", nom: "M. WILFRIED GADOU",     service: "DIRECTION",  email: "", telephone: "" },
  { id: "C-KOFFI",    nom: "M. KOFFI Jean-Marc",    service: "TECHNOLOGY", email: "", telephone: "" },
  { id: "C-BAMBA",    nom: "Mme BAMBA Aïcha",       service: "ENCACI",     email: "", telephone: "" },
  { id: "C-TRAORE",   nom: "M. TRAORÉ Ibrahim",     service: "FORMATION",  email: "", telephone: "" }
];
const VEHICULES = [
  { id: "V-AA1234", plate: "AA-1234-CI", marque: "Toyota",  modele: "Hilux",    type: "Pick-up",     annee: 2021, km: 84600,  service: "TECHNOLOGY", state: "En mission",  entretien: "2026-11-15", note: "" },
  { id: "V-BB9087", plate: "BB-9087-CI", marque: "Hyundai", modele: "Accent",   type: "Berline",     annee: 2019, km: 132400, service: "ENCACI",     state: "Disponible",  entretien: "2026-10-28", note: "" },
  { id: "V-CC4455", plate: "CC-4455-CI", marque: "Yamaha",  modele: "XTZ 125",  type: "Moto",        annee: 2022, km: 21350,  service: "FORMATION",  state: "Disponible",  entretien: "2026-12-05", note: "" },
  { id: "V-DD7712", plate: "DD-7712-CI", marque: "Renault", modele: "Kangoo",   type: "Camionnette", annee: 2018, km: 158900, service: "ENCACI",     state: "Maintenance", entretien: "2026-10-09", note: "Révision boîte de vitesses" }
];
module.exports = { COLLABS, VEHICULES };
