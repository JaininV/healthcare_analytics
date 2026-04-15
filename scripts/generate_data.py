"""
Healthcare Analytics Project — Phase 1: Dataset Generation
Generates 4 CSV files with realistic dirty data injections.
Output: D:/D/Projects/Healthcare Analytics/data/raw/patients.csv, admissions.csv, claims.csv, readmissions.csv
"""

import os
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "D:/D/Projects/Healthcare Analytics/data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
N_PATIENTS      = 10_000
N_ADMISSIONS    = 200_000
N_CLAIMS        = 200_000
N_READMISSIONS  = 3_000

DEPARTMENTS     = ["Cardiology", "Emergency", "Orthopedics", "Neurology", "ICU", "Oncology", "General Surgery", "Pediatrics"]
INSURANCE_TYPES = ["Private", "Medicare", "Medicaid", "Uninsured"]
REGIONS         = ["North", "South", "East", "West", "Central"]
SEVERITIES      = ["Low", "Medium", "High", "Critical"]
OUTCOMES        = ["Discharged", "Transferred", "Deceased", "AMA"]
PAYERS          = ["BlueCross", "Aetna", "Medicare", "Medicaid", "Self-pay", "UnitedHealth", "Cigna"]
CLAIM_STATUSES  = ["Approved", "Denied", "Pending", "Partial"]
DENIAL_REASONS  = ["Not Medically Necessary", "Missing Information", "Out of Network",
                   "Duplicate Claim", "Authorization Required", "Expired Coverage"]
READMIT_REASONS = ["Complication", "Infection", "Unrelated Condition", "Follow-up Required", "Medication Issue"]
BLOOD_TYPES     = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

# Valid ICD-10 codes with descriptions
ICD10_CODES = {
    "I21.0":  "Acute anterior myocardial infarction",
    "I50.9":  "Heart failure, unspecified",
    "J18.9":  "Pneumonia, unspecified organism",
    "N18.3":  "Chronic kidney disease, stage 3",
    "E11.9":  "Type 2 diabetes without complications",
    "I63.9":  "Cerebral infarction, unspecified",
    "J44.1":  "COPD with acute exacerbation",
    "K92.1":  "Melena",
    "S72.001": "Femur fracture",
    "C34.90": "Malignant neoplasm of bronchus and lung",
    "G35":    "Multiple sclerosis",
    "M54.5":  "Low back pain",
    "F32.9":  "Major depressive disorder",
    "Z38.00": "Single liveborn infant",
    "A41.9":  "Sepsis, unspecified organism",
    "I10":    "Essential hypertension",
    "E78.5":  "Hyperlipidemia, unspecified",
    "K21.0":  "GERD with esophagitis",
    "J06.9":  "Acute upper respiratory infection",
    "R07.9":  "Chest pain, unspecified",
}

INVALID_ICD_CODES = ["XX999", "ZZZ00", "123AB", "I21", "BAD-CODE", "999.99", "MISSING", "N/A"]


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
def random_date(start: datetime, end: datetime) -> datetime:
    return start + timedelta(days=random.randint(0, (end - start).days))

def fmt_date(d) -> str:
    return d.strftime("%Y-%m-%d") if d else None


# ─────────────────────────────────────────────
# 1. PATIENTS
# ─────────────────────────────────────────────
print("Generating patients.csv ...")

patient_ids = [f"PAT-{str(i).zfill(5)}" for i in range(1, N_PATIENTS + 1)]

patients = []
for pid in patient_ids:
    dob = random_date(datetime(1930, 1, 1), datetime(2005, 12, 31))
    patients.append({
        "patient_id":     pid,
        "full_name":      fake.name(),
        "dob":            fmt_date(dob),
        "gender":         random.choice(["M", "F", "Other"]),
        "blood_type":     random.choice(BLOOD_TYPES),
        "insurance_type": random.choices(INSURANCE_TYPES, weights=[40, 30, 20, 10])[0],
        "region":         random.choice(REGIONS),
        "signup_date":    fmt_date(random_date(datetime(2015, 1, 1), datetime(2022, 12, 31))),
        "phone":          fake.phone_number(),
        "email":          fake.email(),
    })

patients_df = pd.DataFrame(patients)

# ── DIRTY: inject ~2% duplicate patients (same name/dob, slightly different ID)
n_dupes = int(N_PATIENTS * 0.02)
dupe_source = patients_df.sample(n_dupes, random_state=1).copy()
dupe_source["patient_id"] = [f"PAT-{str(i).zfill(5)}" for i in range(N_PATIENTS + 1, N_PATIENTS + n_dupes + 1)]
# Slightly alter email/phone to simulate real-world duplicates
dupe_source["email"] = dupe_source["email"].apply(lambda x: x.replace("@", "2@"))
patients_df = pd.concat([patients_df, dupe_source], ignore_index=True)

patients_df.to_csv(f"{OUTPUT_DIR}/patients.csv", index=False)
print(f"  patients.csv → {len(patients_df):,} rows (incl. {n_dupes} duplicates)")


# ─────────────────────────────────────────────
# 2. ADMISSIONS
# ─────────────────────────────────────────────
print("Generating admissions.csv ...")

all_patient_ids = patients_df["patient_id"].tolist()
icd_codes       = list(ICD10_CODES.keys())

admissions = []
for i in range(1, N_ADMISSIONS + 1):
    admit_dt    = random_date(datetime(2020, 1, 1), datetime(2024, 6, 30))
    los         = random.randint(1, 30)
    discharge_dt = admit_dt + timedelta(days=los)
    icd         = random.choice(icd_codes)

    admissions.append({
        "admission_id":        f"ADM-{str(i).zfill(6)}",
        "patient_id":          random.choice(all_patient_ids),
        "admit_date":          fmt_date(admit_dt),
        "discharge_date":      fmt_date(discharge_dt),
        "department":          random.choice(DEPARTMENTS),
        "diagnosis_code":      icd,
        "diagnosis_desc":      ICD10_CODES[icd],
        "severity":            random.choices(SEVERITIES, weights=[30, 40, 20, 10])[0],
        "attending_physician": fake.name(),
        "los_days":            los,
        "outcome":             random.choices(OUTCOMES, weights=[70, 10, 5, 15])[0],
    })

adm_df = pd.DataFrame(admissions)

# ── DIRTY 1: ~3% nulls in critical fields
null_idx = adm_df.sample(frac=0.03, random_state=2).index
adm_df.loc[null_idx, random.choice(["department", "diagnosis_code", "severity"])] = np.nan

# ── DIRTY 2: ~1% discharge BEFORE admit (date logic error)
date_err_idx = adm_df.sample(frac=0.01, random_state=3).index
adm_df.loc[date_err_idx, "discharge_date"] = adm_df.loc[date_err_idx, "admit_date"].apply(
    lambda d: fmt_date(datetime.strptime(d, "%Y-%m-%d") - timedelta(days=random.randint(1, 10)))
    if pd.notna(d) else d
)

# ── DIRTY 3: ~2% invalid ICD-10 codes
icd_err_idx = adm_df.sample(frac=0.02, random_state=4).index
adm_df.loc[icd_err_idx, "diagnosis_code"] = [random.choice(INVALID_ICD_CODES) for _ in icd_err_idx]
adm_df.loc[icd_err_idx, "diagnosis_desc"] = "INVALID"

# ── DIRTY 4: ~1% negative LOS
neg_los_idx = adm_df.sample(frac=0.01, random_state=5).index
adm_df.loc[neg_los_idx, "los_days"] = adm_df.loc[neg_los_idx, "los_days"] * -1

# ── DIRTY 5: ~0.5% orphan admissions (patient_id not in patients)
orphan_idx = adm_df.sample(frac=0.005, random_state=6).index
adm_df.loc[orphan_idx, "patient_id"] = [f"PAT-GHOST-{i}" for i in range(len(orphan_idx))]

adm_df.to_csv(f"{OUTPUT_DIR}/admissions.csv", index=False)
print(f"  admissions.csv → {len(adm_df):,} rows")
print(f"    Nulls injected:          {len(null_idx):,} rows")
print(f"    Date logic errors:       {len(date_err_idx):,} rows")
print(f"    Invalid ICD codes:       {len(icd_err_idx):,} rows")
print(f"    Negative LOS:            {len(neg_los_idx):,} rows")
print(f"    Orphan admissions:       {len(orphan_idx):,} rows")


# ─────────────────────────────────────────────
# 3. CLAIMS
# ─────────────────────────────────────────────
print("Generating claims.csv ...")

admission_ids = adm_df["admission_id"].tolist()

claims = []
for i in range(1, N_CLAIMS + 1):
    adm_id      = random.choice(admission_ids)
    billed      = round(random.uniform(500, 150_000), 2)
    approved    = round(billed * random.uniform(0.5, 0.95), 2)
    status      = random.choices(CLAIM_STATUSES, weights=[50, 20, 20, 10])[0]

    # Submission date: 1–30 days after a plausible discharge
    sub_date    = random_date(datetime(2020, 2, 1), datetime(2024, 7, 30))
    pay_date    = (sub_date + timedelta(days=random.randint(14, 90))) if status == "Approved" else None

    claims.append({
        "claim_id":         f"CLM-{str(i).zfill(6)}",
        "admission_id":     adm_id,
        "billed_amount":    billed,
        "approved_amount":  approved if status != "Denied" else 0.0,
        "payer":            random.choice(PAYERS),
        "claim_status":     status,
        "denial_reason":    random.choice(DENIAL_REASONS) if status == "Denied" else None,
        "submission_date":  fmt_date(sub_date),
        "payment_date":     fmt_date(pay_date),
    })

claims_df = pd.DataFrame(claims)

# ── DIRTY 1: ~1.5% approved_amount > billed_amount (financial integrity error)
fin_err_idx = claims_df.sample(frac=0.015, random_state=7).index
claims_df.loc[fin_err_idx, "approved_amount"] = claims_df.loc[fin_err_idx, "billed_amount"] * random.uniform(1.05, 1.5)

# ── DIRTY 2: ~1% negative billed amounts
neg_amt_idx = claims_df.sample(frac=0.01, random_state=8).index
claims_df.loc[neg_amt_idx, "billed_amount"] = claims_df.loc[neg_amt_idx, "billed_amount"] * -1

# ── DIRTY 3: ~2% nulls in payer or claim_status
null_claim_idx = claims_df.sample(frac=0.02, random_state=9).index
claims_df.loc[null_claim_idx, random.choice(["payer", "claim_status"])] = np.nan

# ── DIRTY 4: ~0.5% payment_date before submission_date
pay_err_idx = claims_df[claims_df["payment_date"].notna()].sample(frac=0.005, random_state=10).index
claims_df.loc[pay_err_idx, "payment_date"] = claims_df.loc[pay_err_idx, "submission_date"].apply(
    lambda d: fmt_date(datetime.strptime(d, "%Y-%m-%d") - timedelta(days=random.randint(1, 30)))
    if pd.notna(d) else d
)

claims_df.to_csv(f"{OUTPUT_DIR}/claims.csv", index=False)
print(f"  claims.csv → {len(claims_df):,} rows")
print(f"    Financial integrity errors: {len(fin_err_idx):,} rows")
print(f"    Negative billed amounts:    {len(neg_amt_idx):,} rows")
print(f"    Null payer/status:          {len(null_claim_idx):,} rows")
print(f"    Payment before submission:  {len(pay_err_idx):,} rows")


# ─────────────────────────────────────────────
# 4. READMISSIONS
# ─────────────────────────────────────────────
print("Generating readmissions.csv ...")

# Pull a subset of admissions that could realistically have readmissions
eligible_adm = adm_df[adm_df["outcome"] == "Discharged"].sample(N_READMISSIONS, random_state=11)

readmissions = []
for i, (_, row) in enumerate(eligible_adm.iterrows(), 1):
    days_since = random.randint(1, 30)
    try:
        discharge_dt = datetime.strptime(row["discharge_date"], "%Y-%m-%d")
        readmit_dt   = discharge_dt + timedelta(days=days_since)
    except Exception:
        readmit_dt   = random_date(datetime(2020, 3, 1), datetime(2024, 8, 30))
        days_since   = random.randint(1, 30)

    readmissions.append({
        "readmit_id":             f"RDM-{str(i).zfill(5)}",
        "patient_id":             row["patient_id"],
        "original_admission_id":  row["admission_id"],
        "readmit_date":           fmt_date(readmit_dt),
        "days_since_discharge":   days_since,
        "readmit_reason":         random.choice(READMIT_REASONS),
        "readmit_department":     random.choice(DEPARTMENTS),
        "readmit_severity":       random.choices(SEVERITIES, weights=[20, 35, 30, 15])[0],
    })

readm_df = pd.DataFrame(readmissions)

# ── DIRTY: ~2% nulls in readmit_reason
null_rdm_idx = readm_df.sample(frac=0.02, random_state=12).index
readm_df.loc[null_rdm_idx, "readmit_reason"] = np.nan

readm_df.to_csv(f"{OUTPUT_DIR}/readmissions.csv", index=False)
print(f"  readmissions.csv → {len(readm_df):,} rows")


# ─────────────────────────────────────────────
# 5. SUMMARY REPORT
# ─────────────────────────────────────────────
print("\n" + "="*55)
print("  PHASE 1 COMPLETE — Dataset Generation Summary")
print("="*55)
print(f"  patients.csv       {len(patients_df):>10,} rows")
print(f"  admissions.csv     {len(adm_df):>10,} rows")
print(f"  claims.csv         {len(claims_df):>10,} rows")
print(f"  readmissions.csv   {len(readm_df):>10,} rows")
print(f"  {'─'*35}")
print(f"  Total rows         {len(patients_df)+len(adm_df)+len(claims_df)+len(readm_df):>10,}")
print(f"\n  Files saved to → ./{OUTPUT_DIR}/")
print("\n  Dirty data injected:")
print(f"    Duplicate patients            ~{n_dupes} rows")
print(f"    Null critical fields          ~{len(null_idx)+len(null_claim_idx)+len(null_rdm_idx):,} rows")
print(f"    Date logic errors             ~{len(date_err_idx)+len(pay_err_idx):,} rows")
print(f"    Invalid ICD-10 codes          ~{len(icd_err_idx):,} rows")
print(f"    Financial integrity errors    ~{len(fin_err_idx):,} rows")
print(f"    Negative values               ~{len(neg_los_idx)+len(neg_amt_idx):,} rows")
print(f"    Orphan records                ~{len(orphan_idx):,} rows")
print("="*55)
print("  Next step → Phase 2: Data Cleaning & Validation")
print("="*55)