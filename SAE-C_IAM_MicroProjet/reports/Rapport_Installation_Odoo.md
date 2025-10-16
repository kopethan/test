# Rapport d'installation Odoo & Export RH (Très synthétique)

## Environnement
- WSL2 + Ubuntu
- Docker + Docker Compose
- Odoo 16 Community + Postgres 15

## Déploiement
- `docker compose up -d`
- Accès: http://localhost:8069
- Création de la base **avec données de démonstration**

## Export RH (CSV)
- Module RH > Employés > Vue Liste > Action > Export
- Champs exportés (exemple): name, work_email, department, job_title, work_location, status, seniority_years
- Fichier placé dans `data/HR_employees_demo.csv`

## Épuration (manuel -> script)
- Échantillon épuré manuellement (conserver colonnes utiles)
- Script `python scripts/export_clean.py` pour automatiser
- Résultat: `data/HR_employees_clean.csv` + gabarits Excel