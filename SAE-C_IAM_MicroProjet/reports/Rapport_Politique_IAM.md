# Rapport de politique IAM (Synthèse)

## Matrice globale (qui, quoi, comment, d'où)
- Voir `data/templates/IAM_Global_Matrix.xlsx`

## Études de cas
1. **RBAC only**: rôles standardisés par métier → permissions prédéfinies.
2. **ABAC only**: attributs (département, localisation, ancienneté, statut) → règles d'accès.
3. **Mixte**: rôle de base + raffinements ABAC contextuels.

## Choix proposé
- **Mixte RBAC+ABAC** recommandé: lisibilité (RBAC) + finesse (ABAC).
- ABAC seul plus flexible mais plus complexe à auditer; RBAC seul trop rigide.

## Implémentation sous MidPoint (approche)
- Source d'identités: CSV RH (ou connecteur DB/Odoo).
- Rôles métiers: SalesUser, BillingUser, ITSupport, Employee.
- Politiques ABAC: conditions sur attributs (ex. `work_location == "Paris"`, `seniority_years >= 2`).
- Affectations: rôle de base + constraints; provisioning vers LDAP (ApacheDS), Odoo, Intranet/DB, VPN.