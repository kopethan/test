# Rapport d'état de l'art (Ultra synthétique)

## IGA & Modèles d'accès (RBAC, ABAC, MLS)
- **RBAC**: permissions via rôles; simple à auditer; maintenance via rôles.
- **ABAC**: permissions via attributs (identité, contexte, ressource); flexible, dynamique.
- **MLS**: niveaux de sécurité/classification; contraintes *no read up / no write down*.
- Différences: RBAC (statique, lisible), ABAC (contextuel, granulaire), MLS (axé classification).

## IAM vs IGA
- **IAM**: authentification, provisionning, SSO, MFA.
- **IGA**: gouvernance: campagnes de recertification, SoD, attestation, audit.
- Complémentaires: IAM opère, IGA gouverne.

## Outils (marché FR/EU/Monde — aperçu **à compléter avec preuves**)
- Editeurs connus: Microsoft Entra (Azure AD), Okta, Ping, SailPoint (IGA), OneIdentity, ForgeRock, Keycloak (OSS), WSO2 (OSS), Evolveum MidPoint (OSS/IGA).
- En France/Europe: forte présence Microsoft + SailPoint; écosystème open-source (Keycloak, MidPoint).
- [Preuves/études de marché à citer ici: Gartner, IDC, KuppingerCole, etc.]

## MidPoint — Fonctions utiles (pour ce projet)
- Modèle objets (utilisateur, rôle, ressource, affectations).
- Provisioning via connecteurs (LDAP/AD, DB, REST).
- Politique RBAC/ABAC hybride via rôles + conditions.
- Recertification/approbations de base.
- Synchronisation identités (HR → cibles).