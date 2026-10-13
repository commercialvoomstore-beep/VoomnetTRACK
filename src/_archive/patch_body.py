# -*- coding: utf-8 -*-
"""Patch HTML : écran d'accès RH, sidebar sans Véhicules, dashboard RH centralisé, suppression de l'onglet Véhicules."""
p = 'src/part2_body.html'
s = open(p).read()

def rep(old, new, label):
    global s
    assert old in s, "INTROUVABLE : " + label
    s = s.replace(old, new, 1)
    print("  ✓", label)

# ============================================================ 1. ÉCRAN D'ACCÈS RH
old_start = s.index('<!-- ============================ ÉCRAN DE CONNEXION ============================ -->')
old_end   = s.index('<div class="app">')
new_login = '''<!-- ============================ ÉCRAN D'ACCÈS RH ============================ -->
<div id="login" class="hidden">
  <div class="login-card">
    <aside class="login-brand">
      <img class="login-logo" data-logo-track alt="VOOMNET Track" width="__W_LOGO_TRACK__" height="__H_LOGO_TRACK__">
      <span class="login-badge"><span class="ic" data-ico="shield"></span> Gestion RH &amp; Mobility Control</span>
      <h2>Le centre de pilotage unique de la mobilité.</h2>
      <p>Une seule plateforme pour la RH : déplacements, collaborateurs, services et coûts de mobilité réunis dans un tableau de bord centralisé.</p>
      <ul class="login-perks">
        <li><span class="ic" data-ico="list"></span><span><b>Registre des sorties</b> — motif, trajet, montant et justificatif par déplacement.</span></li>
        <li><span class="ic" data-ico="users"></span><span><b>Collaborateurs &amp; services</b> — des données suivies et filtrables, pas des espaces séparés.</span></li>
        <li><span class="ic" data-ico="pdf"></span><span><b>Rapport mensuel PDF</b> — totaux par service, prêt à signer, généré localement.</span></li>
      </ul>
    </aside>

    <section class="login-form">
      <div>
        <h3>Accès à la plateforme RH</h3>
        <p class="lead">Pilotez les déplacements, les collaborateurs et les coûts de mobilité depuis un espace centralisé.</p>
      </div>

      <div class="field">
        <label for="loginName">Nom / identité</label>
        <input class="input" id="loginName" placeholder="Ex : Service Ressources Humaines" autocomplete="name">
        <div class="err-msg" id="err-loginName">Merci d'indiquer votre nom ou votre identifiant.</div>
      </div>

      <div class="field">
        <label for="loginRole">Fonction</label>
        <select class="input" id="loginRole"></select>
      </div>

      <div class="login-role-hint">
        <span class="ic" data-ico="info"></span>
        <span>Un seul espace de pilotage : les services et les collaborateurs sont des données gérées par la RH.</span>
      </div>

      <div class="login-actions">
        <button class="btn btn-primary btn-lg btn-block" id="btnLogin"><span class="ic" data-ico="arrowRight"></span> Accéder au tableau de bord</button>
        <div class="login-sep">ou</div>
        <button class="link-btn" id="btnLoginSkip" type="button">Mode consultation</button>
      </div>

      <div class="login-foot">Données conservées localement sur cet appareil · VOOMNET Track v3.0</div>
    </section>
  </div>
</div>

'''
s = s[:old_start] + new_login + s[old_end:]
print("  ✓ nouvel écran d'accès RH")

# ============================================================ 2. SIDEBAR
rep('''    <div class="nav-label">Ressources</div>
    <div class="nav-item" data-view="vehicules">
      <span class="ic" data-ico="car"></span> Véhicules
      <span class="nav-badge gold" id="badgeVehicules">0</span>
    </div>
    <div class="nav-item" data-view="collaborateurs">
      <span class="ic" data-ico="users"></span> Collaborateurs
      <span class="nav-badge violet" id="badgeCollabs">0</span>
    </div>

    <div class="nav-label">Configuration</div>
    <div class="nav-item" data-view="new">
      <span class="ic" data-ico="plus"></span> Nouveau déplacement
    </div>
    <div class="nav-item" data-view="params">
      <span class="ic" data-ico="settings"></span> Paramètres
    </div>''',
'''    <div class="nav-label">Ressources</div>
    <div class="nav-item" data-view="collaborateurs">
      <span class="ic" data-ico="users"></span> Collaborateurs
      <span class="nav-badge violet" id="badgeCollabs">0</span>
    </div>

    <div class="nav-label">Configuration</div>
    <div class="nav-item" data-view="params">
      <span class="ic" data-ico="settings"></span> Paramètres
    </div>''', "sidebar : Véhicules et Nouveau déplacement retirés")

# ---- menu utilisateur : "Changer de profil" → "Se déconnecter", + garder Nouveau déplacement
rep('''          <div class="pop-item" data-action="logout"><span class="ic" data-ico="user"></span><span class="tx"><b>Changer de profil</b>Revenir à l'écran de connexion</span></div>''',
'''          <div class="pop-item" data-action="logout"><span class="ic" data-ico="user"></span><span class="tx"><b>Se déconnecter</b>Revenir à l'écran d'accès RH</span></div>''', "menu : déconnexion")

# ============================================================ 3. DASHBOARD RH
d0 = s.index('<!-- ================================ DASHBOARD ================================ -->')
d1 = s.index('<!-- ============================== NOUVEAU DÉPLACEMENT ============================== -->')
new_dash = '''<!-- ======================= TABLEAU DE BORD RH CENTRALISÉ ======================= -->
      <section class="view active" id="view-dashboard">

        <!-- 1. EN-TÊTE RH -->
        <div class="welcome reveal" style="--i:0">
          <div>
            <h2 id="welcomeTitle">Bonjour, RH 👋</h2>
            <div class="sub" id="welcomeSub">Voici la situation de la mobilité de votre organisation.</div>
            <div class="pills" id="welcomePills"></div>
          </div>
          <div class="actions">
            <button class="btn btn-soft" id="btnSeedDemo"><span class="ic" data-ico="sparkle"></span> Exemples</button>
            <button class="btn btn-gold" id="qaPdf"><span class="ic" data-ico="pdf"></span> Télécharger le PDF</button>
            <button class="btn btn-primary" data-goto="new"><span class="ic" data-ico="plus"></span> Nouveau déplacement</button>
          </div>
        </div>

        <!-- 2. FILTRES GLOBAUX (appliqués à tout le tableau de bord) -->
        <div class="filterbar section reveal" style="--i:1">
          <div class="fb-cell">
            <label for="dashMonth">Période</label>
            <input type="month" class="input" id="dashMonth">
          </div>
          <div class="fb-cell">
            <label for="gService">Service</label>
            <select class="input" id="gService"><option value="">Tous les services</option></select>
          </div>
          <div class="fb-cell">
            <label for="gAgent">Collaborateur</label>
            <select class="input" id="gAgent"><option value="">Tous les collaborateurs</option></select>
          </div>
          <div class="fb-cell">
            <label for="gType">Type de déplacement</label>
            <select class="input" id="gType"><option value="">Tous les types</option></select>
          </div>
          <div class="fb-reset">
            <button class="btn btn-ghost btn-sm" id="btnResetFilters"><span class="ic" data-ico="x"></span> Réinitialiser</button>
          </div>
          <div class="filter-chips" id="filterChips" style="grid-column:1/-1"></div>
        </div>

        <!-- 3. KPI -->
        <div class="grid kpi-grid section" id="kpiRow" style="--i:2"></div>

        <!-- 4. GRAPHIQUES -->
        <div class="grid g-32 section">
          <div class="card pad-lg reveal" style="--i:1">
            <div class="card-h">
              <div class="t">
                <h3><span class="ic-chip"><span class="ic" data-ico="chart"></span></span> Évolution des dépenses</h3>
                <div class="desc" id="evoDesc">6 derniers mois — total mensuel consolidé</div>
              </div>
              <div class="seg" id="evoRange">
                <button class="on" data-range="6">6 mois</button>
                <button data-range="12">12 mois</button>
              </div>
            </div>
            <div id="chartEvo"></div>
          </div>

          <div class="card pad-lg reveal" style="--i:2">
            <div class="card-h">
              <div class="t">
                <h3><span class="ic-chip"><span class="ic" data-ico="wallet"></span></span> Part des services</h3>
                <div class="desc">Dépenses de la période sélectionnée</div>
              </div>
            </div>
            <div id="chartSvc"></div>
          </div>
        </div>

        <!-- 5. RÉPARTITION PAR SERVICE -->
        <div class="section">
          <div class="section-h">
            <div>
              <h2>Répartition par service</h2>
              <div class="desc">Cliquez sur un service pour filtrer tout le tableau de bord — aucun espace séparé, uniquement un filtre</div>
            </div>
            <button class="link-btn" data-goto="analyse">Analyse détaillée →</button>
          </div>
          <div class="svc-list" id="svcList"></div>
        </div>

        <!-- 6. ACTIVITÉ DES COLLABORATEURS -->
        <div class="section">
          <div class="section-h">
            <div>
              <h2>Activité des collaborateurs</h2>
              <div class="desc">Les personnes suivies par la RH et leur consommation de mobilité</div>
            </div>
            <div class="row-scope">
              <label class="mini-search" for="caSearch">
                <span class="ic" data-ico="search"></span>
                <input id="caSearch" type="search" placeholder="Rechercher un collaborateur…" autocomplete="off">
              </label>
            </div>
          </div>
          <div class="card pad-lg" style="padding:10px">
            <div class="table-wrap" style="border:none;box-shadow:none" id="collabActivity"></div>
          </div>
        </div>

        <!-- 7. DERNIERS DÉPLACEMENTS + CONTRÔLE -->
        <div class="grid g-32 section">
          <div class="card pad-lg">
            <div class="card-h">
              <div class="t">
                <h3><span class="ic-chip"><span class="ic" data-ico="list"></span></span> Derniers déplacements</h3>
                <div class="desc">Les sorties les plus récentes, tous services confondus</div>
              </div>
              <button class="btn btn-ghost btn-sm" data-goto="registre"><span class="ic" data-ico="list"></span> Ouvrir le registre</button>
            </div>
            <div class="table-wrap" id="recentWrap"></div>
          </div>

          <div style="display:flex;flex-direction:column;gap:var(--gap)">
            <div class="card pad-lg">
              <div class="card-h">
                <div class="t">
                  <h3><span class="ic-chip"><span class="ic" data-ico="alert"></span></span> Points d'attention</h3>
                  <div class="desc">À traiter en priorité</div>
                </div>
              </div>
              <div id="attentionList" class="rank-list"></div>
            </div>

            <div class="card pad-lg">
              <div class="card-h">
                <div class="t">
                  <h3><span class="ic-chip"><span class="ic" data-ico="shield"></span></span> Contrôle &amp; conformité</h3>
                  <div class="desc">Qualité des données de la période</div>
                </div>
              </div>
              <div id="insights" class="stat-stack"></div>
            </div>
          </div>
        </div>

      </section>

      '''
s = s[:d0] + new_dash + s[d1:]
print("  ✓ dashboard RH centralisé")

# ============================================================ 4. SUPPRESSION VÉHICULES
v0 = s.index('<!-- ================================== VÉHICULES ================================== -->')
v1 = s.index('<!-- ================================ COLLABORATEURS ================================ -->')
s = s[:v0] + s[v1:]
print("  ✓ vue Véhicules supprimée")

# ---- filtre véhicule dans le registre
rep('''            <div>
              <label class="small">Véhicule</label>
              <select class="input" id="fVehicule2"><option value="">Tous les véhicules</option></select>
            </div>
''', '', "registre : filtre Véhicule retiré")

# ---- champ véhicule dans la fiche de déplacement (g-3 → g-2)
rep('''              <div class="grid g-3" style="gap:0 18px">
                <div class="field">
                  <label for="fTrans">Moyen de transport <span class="req">*</span></label>
                  <select id="fTrans" class="input"></select>
                  <div class="err-msg" id="err-trans">Choisissez le moyen de transport.</div>
                </div>
                <div class="field">
                  <label for="fVehicule">Véhicule utilisé</label>
                  <select id="fVehicule" class="input"></select>
                  <div class="hint">Facultatif — renseigne le suivi de flotte.</div>
                </div>
                <div class="field">
                  <label for="fMontant">Montant dépensé <span class="req">*</span></label>''',
'''              <div class="grid g-2" style="gap:0 18px">
                <div class="field">
                  <label for="fTrans">Moyen de transport <span class="req">*</span></label>
                  <select id="fTrans" class="input"></select>
                  <div class="err-msg" id="err-trans">Choisissez le moyen de transport.</div>
                </div>
                <div class="field">
                  <label for="fMontant">Montant dépensé <span class="req">*</span></label>''', "fiche : champ Véhicule retiré")

# ---- "Moyens de transport suivis" : sous-titre sans mention de flotte
rep('<li><b>Distance</b> alimente le kilométrage mensuel du tableau de bord.</li>',
    '<li><b>Distance</b> alimente le kilométrage de la période, suivi par la RH.</li>', "aide-mémoire")

# ---- pied de version
s = s.replace('VOOMNET Track · v2.0', 'VOOMNET Track · v3.0')
s = s.replace('VOOMNET Track · v2.2', 'VOOMNET Track · v3.0')

open(p, 'w').write(s)
print("part2_body.html mis à jour")
