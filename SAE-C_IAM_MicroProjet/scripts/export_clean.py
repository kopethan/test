import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TEMPL_DIR = DATA_DIR / "templates"
TARGET_EXPORTS = TEMPL_DIR / "target_exports"

DATA_DIR.mkdir(parents=True, exist_ok=True)
TEMPL_DIR.mkdir(parents=True, exist_ok=True)
TARGET_EXPORTS.mkdir(parents=True, exist_ok=True)

# 1) Read Odoo HR export CSV and produce a minimal, "clean" dataset
src_csv = DATA_DIR / "HR_employees_demo.csv"
dst_csv = DATA_DIR / "HR_employees_clean.csv"

if not src_csv.exists():
    # Create a tiny demo file if the user hasn't exported yet
    demo = pd.DataFrame([
        {"name": "Alice Martin", "work_email": "alice.martin@example.com", "department": "Sales",
         "job_title": "Sales Rep", "work_location": "Paris", "status": "CDI", "seniority_years": 3},
        {"name": "Bob Dupont", "work_email": "bob.dupont@example.com", "department": "Finance",
         "job_title": "Accountant", "work_location": "Lyon", "status": "CDD", "seniority_years": 1},
        {"name": "Claire Bernard", "work_email": "claire.bernard@example.com", "department": "IT",
         "job_title": "Support IT", "work_location": "Paris", "status": "CDI", "seniority_years": 5},
    ])
    demo.to_csv(src_csv, index=False)

df = pd.read_csv(src_csv)

# Keep only fields we need for IAM attributes
keep_cols = []
for c in ["name","work_email","department","job_title","work_location","status","seniority_years"]:
    if c in df.columns:
        keep_cols.append(c)

clean = df[keep_cols].copy()

# Normalize/clean
clean["department"] = clean["department"].astype(str).str.strip().str.title()
clean["job_title"] = clean["job_title"].astype(str).str.strip().str.title()
clean["work_location"] = clean["work_location"].astype(str).str.strip().str.title()
if "status" in clean.columns:
    clean["status"] = clean["status"].astype(str).str.upper()

# Add derived fields useful for ABAC examples
if "seniority_years" in clean.columns:
    clean["is_senior"] = clean["seniority_years"].fillna(0).astype(float) >= 3

clean.to_csv(dst_csv, index=False)
print(f"[OK] Clean CSV written -> {dst_csv}")

# 2) Create simulated exports from target systems (minimal schemas)
def save_xlsx(path, df):
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path) as writer:
        df.to_excel(writer, index=False, sheet_name="data")

# Odoo users (basic role/profile mapping example)
odoo_users = clean.rename(columns={
    "name":"user_name",
    "work_email":"login",
    "department":"department",
    "job_title":"job_title"
})
odoo_users["profile"] = odoo_users["department"].map({
    "Sales":"SalesUser",
    "Finance":"BillingUser",
    "It":"ITSupport"
}).fillna("Employee")
odoo_users["password_policy"] = "OdooDefault"
save_xlsx(TARGET_EXPORTS/"Odoo_users.xlsx", odoo_users[["user_name","login","profile","password_policy"]])

# ApacheDS (LDAP) accounts simulation
apacheds = pd.DataFrame({
    "uid": clean["work_email"].fillna("").str.replace("@.*","",regex=True),
    "cn": clean["name"],
    "groups": clean["department"].map({"Sales":"grp_sales","Finance":"grp_finance","It":"grp_it"}).fillna("grp_staff"),
    "password_policy": "LDAPDefault"
})
save_xlsx(TARGET_EXPORTS/"ApacheDS_accounts.xlsx", apacheds)

# Intranet app (PostgreSQL) users+permissions simulation
intranet = pd.DataFrame({
    "username": clean["work_email"].fillna(""),
    "role": clean["job_title"].map({"Sales Rep":"crm_user","Accountant":"billing_user","Support It":"it_support"}).fillna("employee"),
    "permissions": ["read,write" if r!="employee" else "read" for r in clean["job_title"].map({"Sales Rep":"crm_user","Accountant":"billing_user","Support It":"it_support"}).fillna("employee")]
})
save_xlsx(TARGET_EXPORTS/"Intranet_users.xlsx", intranet)

# VPN accounts
vpn = pd.DataFrame({
    "user": clean["work_email"].fillna(""),
    "profile": clean["work_location"].map({"Paris":"vpn_full","Lyon":"vpn_limited"}).fillna("vpn_basic"),
    "mfa": True
})
save_xlsx(TARGET_EXPORTS/"VPN_accounts.xlsx", vpn)

# 3) Global IAM matrix (who, what, how, where from)
global_matrix = pd.DataFrame({
    "identity": clean["name"],
    "email": clean["work_email"],
    "function": clean["job_title"],
    "department": clean["department"],
    "permission_target": ["CRM","Billing","IT Helpdesk"],
    "permission_action": ["read/write","read","read"],
    "auth_method": ["SSO","Password+MFA","Password+VPN"],
    "origin_required": ["Local/VPN","Local","VPN only"]
})
save_xlsx(TEMPL_DIR/"IAM_Global_Matrix.xlsx", global_matrix)

# 4) Case 1: RBAC-only (roles -> permissions)
rbac = pd.DataFrame({
    "role_name": ["SalesUser","BillingUser","ITSupport","Employee"],
    "description": ["CRM access","Billing & invoices","IT tickets & tools","Basic apps"],
    "systems": ["Odoo CRM, Intranet","Odoo Billing, Intranet","Intranet, LDAP","All"],
    "permissions": ["crm:read,write","billing:read,write","it:read,write","basic:read"]
})
save_xlsx(TEMPL_DIR/"RBAC_only.xlsx", rbac)

# 5) Case 2: ABAC-only (attributes -> permissions)
abac = pd.DataFrame({
    "attribute_condition": [
        "department == 'Sales'",
        "department == 'Finance'",
        "department == 'IT' and is_senior == True",
        "work_location == 'Paris' and status == 'CDI'"
    ],
    "granted_permissions": [
        "crm:read,write",
        "billing:read,write",
        "it:admin",
        "vpn_full"
    ],
    "target_systems": ["Odoo CRM, Intranet","Odoo Billing, Intranet","Intranet, LDAP","VPN"]
})
save_xlsx(TEMPL_DIR/"ABAC_only.xlsx", abac)

# 6) Case 3: Hybrid RBAC+ABAC
hybrid = pd.DataFrame({
    "profile_or_function": ["Sales Rep","Accountant","Support IT","Employee"],
    "base_role": ["SalesUser","BillingUser","ITSupport","Employee"],
    "abac_conditions": ["work_location == 'Paris'","seniority_years >= 2","status == 'CDI'",""],
    "effective_permissions": ["crm:read,write; vpn_full if Paris","billing:read,write","it:read,write; it:admin if CDI","basic:read"],
    "systems": ["Odoo CRM, VPN","Odoo Billing","Intranet, LDAP","All"]
})
save_xlsx(TEMPL_DIR/"Hybrid_RBAC_ABAC.xlsx", hybrid)

print("[OK] Templates generated in data/templates/ and target_exports/")