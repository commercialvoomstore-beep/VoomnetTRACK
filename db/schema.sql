-- ============================================================================
--  VOOMNET Track — schéma PostgreSQL (compatible Neon)
--  Idempotent : peut être exécuté plusieurs fois sans rien détruire.
--  Aucune instruction DROP / TRUNCATE / DELETE n'est présente.
-- ============================================================================

CREATE TABLE IF NOT EXISTS services (
  id             TEXT PRIMARY KEY,
  code           TEXT,
  nom            TEXT NOT NULL,
  libelle_court  TEXT,
  role           TEXT,
  couleur        TEXT,
  couleur2       TEXT,
  logo           TEXT,
  icone          TEXT,
  ordre          INTEGER DEFAULT 100,
  maj_le         TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS collaborateurs (
  id          TEXT PRIMARY KEY,
  nom         TEXT NOT NULL,
  service_id  TEXT REFERENCES services(id) ON DELETE SET NULL,
  actif       BOOLEAN NOT NULL DEFAULT TRUE,
  email       TEXT,
  telephone   TEXT,
  cree_le     TIMESTAMPTZ DEFAULT now(),
  maj_le      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS vehicules (
  id          TEXT PRIMARY KEY,
  plaque      TEXT,
  marque      TEXT,
  modele      TEXT,
  type        TEXT,
  annee       INTEGER,
  km          INTEGER,
  service_id  TEXT REFERENCES services(id) ON DELETE SET NULL,
  etat        TEXT,
  entretien   DATE,
  note        TEXT,
  cree_le     TIMESTAMPTZ DEFAULT now(),
  maj_le      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS deplacements (
  id           TEXT PRIMARY KEY,
  date         DATE NOT NULL,
  service_id   TEXT REFERENCES services(id) ON DELETE SET NULL,
  agent        TEXT,
  motif        TEXT,
  origine      TEXT,
  destination  TEXT,
  transport    TEXT,
  vehicule     TEXT,
  km           NUMERIC(10,2),
  montant      NUMERIC(12,2) NOT NULL DEFAULT 0,
  statut       TEXT NOT NULL DEFAULT 'A_REGLE',
  justif       TEXT DEFAULT 'NON',
  note         TEXT,
  cree_par     TEXT,
  cree_le      TIMESTAMPTZ DEFAULT now(),
  maj_le       TIMESTAMPTZ DEFAULT now(),
  supprime_le  TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_deplacements_date     ON deplacements (date DESC);
CREATE INDEX IF NOT EXISTS idx_deplacements_service  ON deplacements (service_id);
CREATE INDEX IF NOT EXISTS idx_deplacements_actifs   ON deplacements (supprime_le) WHERE supprime_le IS NULL;

CREATE TABLE IF NOT EXISTS transports (
  id       SERIAL PRIMARY KEY,
  libelle  TEXT UNIQUE NOT NULL,
  ordre    INTEGER DEFAULT 100
);

CREATE TABLE IF NOT EXISTS comptes (
  id                      TEXT PRIMARY KEY,
  identifiant             TEXT NOT NULL,
  nom                     TEXT,
  role                    TEXT,
  admin                   BOOLEAN NOT NULL DEFAULT FALSE,
  actif                   BOOLEAN NOT NULL DEFAULT TRUE,
  mot_de_passe_hash       TEXT NOT NULL,          -- scrypt$sel$empreinte (jamais en clair)
  mot_de_passe_defaut_hash TEXT,                  -- utilisé par « rétablir l'accès d'origine »
  derniere_connexion_le   TIMESTAMPTZ,
  cree_le                 TIMESTAMPTZ DEFAULT now(),
  maj_le                  TIMESTAMPTZ DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_comptes_identifiant ON comptes (lower(identifiant));

CREATE TABLE IF NOT EXISTS sessions (
  id          BIGSERIAL PRIMARY KEY,
  jeton_hash  TEXT UNIQUE NOT NULL,               -- SHA-256 du jeton : le jeton en clair n'est jamais stocké
  compte_id   TEXT NOT NULL REFERENCES comptes(id) ON DELETE CASCADE,
  cree_le     TIMESTAMPTZ DEFAULT now(),
  expire_le   TIMESTAMPTZ NOT NULL,
  revoquee_le TIMESTAMPTZ,
  ip          TEXT,
  agent       TEXT
);
CREATE INDEX IF NOT EXISTS idx_sessions_compte ON sessions (compte_id);
CREATE INDEX IF NOT EXISTS idx_sessions_valides ON sessions (expire_le) WHERE revoquee_le IS NULL;

CREATE TABLE IF NOT EXISTS journal (
  id                  BIGSERIAL PRIMARY KEY,
  at                  TIMESTAMPTZ DEFAULT now(),
  compte_identifiant  TEXT,
  action              TEXT NOT NULL,
  cible               TEXT,
  details             JSONB,
  ip                  TEXT
);
CREATE INDEX IF NOT EXISTS idx_journal_at ON journal (at DESC);

CREATE TABLE IF NOT EXISTS parametres (
  cle     TEXT PRIMARY KEY,
  valeur  JSONB,
  maj_le  TIMESTAMPTZ DEFAULT now()
);

-- ---------------------------------------------------------------------------
--  Référentiel des services (identique aux services de l'application)
-- ---------------------------------------------------------------------------
INSERT INTO services (id, code, nom, libelle_court, role, couleur, couleur2, logo, icone, ordre) VALUES
  ('DIRECTION','DIR','M. WILFRIED GADOU','Direction','Direction Générale','#4A2A63','#4A2A63','direction','user',1),
  ('TECHNOLOGY','TEC','VOOMNET TECHNOLOGY','Technology','Service Technique','#6B4A82','#6B4A82','tech','settings',2),
  ('ENCACI','ENC','ENCACI','ENCACI','Service Partenaire','#9A7A15','#C9A227','encaci','building',3),
  ('FORMATION','FOR','VOOMNET FORMATION','Formation','Service Formation','#A98A1F','#C9A227','form','users',4)
ON CONFLICT (id) DO UPDATE SET
  code = EXCLUDED.code, nom = EXCLUDED.nom, libelle_court = EXCLUDED.libelle_court,
  role = EXCLUDED.role, couleur = EXCLUDED.couleur, couleur2 = EXCLUDED.couleur2,
  logo = EXCLUDED.logo, icone = EXCLUDED.icone, ordre = EXCLUDED.ordre, maj_le = now();

-- ---------------------------------------------------------------------------
--  Moyens de transport
-- ---------------------------------------------------------------------------
INSERT INTO transports (libelle, ordre) VALUES
  ('Taxi (ville)',1),('Taxi collectif / Woro-woro',2),('Gbaka / Minicar',3),('Bus (SOTRA)',4),
  ('Moto-taxi',5),('Véhicule personnel (carburant)',6),('Location de véhicule',7),('Péage / Frais routiers',8),
  ('Avion',9),('Train',10),('Bateau / Pinasse',11),('Autre',12)
ON CONFLICT (libelle) DO NOTHING;

-- ---------------------------------------------------------------------------
--  Paramètres généraux de la plateforme
-- ---------------------------------------------------------------------------
INSERT INTO parametres (cle, valeur) VALUES
  ('nom',    '"VOOMNET"'),
  ('slogan', '"Votre partenaire à votre service"'),
  ('ville',  '"Abidjan – Côte d''Ivoire"'),
  ('tel',    '"+225 · contact@voomnet.ci"'),
  ('devise', '"FCFA"')
ON CONFLICT (cle) DO NOTHING;
