Micro Projet IAM RBAC/ABAC – MidPoint (Scaffold minimal)
Date: 2025-10-15

Contenu
=======
1. docker-compose.yml (Odoo + Postgres + Adminer facultatif)
2. scripts/export_clean.py (épuration CSV + génération des matrices)
3. reports/
   - Rapport_Installation_Odoo.md
   - Rapport_Etat_de_l_art.md
   - Rapport_Politique_IAM.md
4. data/templates/ (modèles Excel et CSV)
   - target_exports/
     * Odoo_users.xlsx
     * ApacheDS_accounts.xlsx
     * Intranet_users.xlsx
     * VPN_accounts.xlsx
   - IAM_Global_Matrix.xlsx
   - RBAC_only.xlsx
   - ABAC_only.xlsx
   - Hybrid_RBAC_ABAC.xlsx
   - HR_employees_demo.csv (exemple d’entrée pour épuration)
5. Ce README.txt

Objectif
========
Respecter strictement les livrables demandés, sans en faire plus :
- Installer Odoo, charger la base de démonstration (employés), exporter les données RH vers CSV,
  épurer ces données (manuel puis script).
- Simuler l’extraction des droits des systèmes cibles et construire la matrice globale d’habilitations.
- Décliner la politique en 3 cas (RBAC, ABAC, Mixte) via des tableurs.
- Rédiger les rapports (état de l’art, installation/exports, politique IAM).

Prérequis
=========
- WSL2 + Ubuntu (ou Linux natif)
- Docker & Docker Compose
- Python 3.10+ avec pandas et openpyxl (pour le script)
  Installation (exemple):
    python3 -m venv .venv
    source .venv/bin/activate
    pip install pandas openpyxl

Démarrage (Docker / Odoo)
=========================
1) Lancer l’infra (dans ce dossier):
    docker compose up -d

   Services:
   - db: Postgres pour Odoo
   - odoo: Odoo 16 Community (port 8069)
   - adminer (optionnel): DB web admin (port 8080)

2) Accéder à Odoo sur http://localhost:8069 et créer une base **avec les données de démo**.
   - Nom de la base: odoo_demo
   - Mot de passe administrateur: (à choisir)
   - Cocher "Données de démonstration / Load demo data".

3) Exporter les employés (module RH) en CSV depuis Odoo (Vue Liste -> Action -> Export).
   - Exemple de champs utiles: name, work_email, work_phone, department_id, job_title,
     work_location, address_home_id, coach_id, create_date, active.

4) Copier le CSV exporté dans data/HR_employees_demo.csv (ou écraser l’existant).

5) Exécuter le script d’épuration et génération de matrices:
    source .venv/bin/activate
    python scripts/export_clean.py

   Le script crée/écrase:
   - data/HR_employees_clean.csv
   - data/templates/*.xlsx (matrices et exports simulés)

Livrables
=========
Fournir un ZIP avec:
- README.txt
- reports/* (md; vous pouvez exporter en PDF)
- data/templates/*.xlsx + data/HR_employees_clean.csv
- scripts/export_clean.py
- docker-compose.yml

Co-auteur
=========
Ajouter le co-auteur (mode suggestion sur Google Docs/Sheets) et inclure l’email:
  achibani@gmail.com