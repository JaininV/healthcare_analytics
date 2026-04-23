# Healthcare Claims Workflow & Readmission Analytics Pipeline

## Project Overview
Built a Python and Excel analytics pipeline to validate and analyze healthcare claims, admissions, patients, and readmission data across 400K+ records.

## Objective
Simulate a real claims analytics workflow by detecting billing errors, workflow anomalies, invalid diagnosis codes, orphan records, and readmission patterns.

## Tools Used
- Python
- pandas
- NumPy
- Excel
- openpyxl
- Faker

## Dataset
- Patients: 10,000+
- Admissions: 200,000
- Claims: 200,000
- Readmissions: ~3,000

## Key Validation Checks
- Approved amount greater than billed amount
- Payment before submission date
- Negative length of stay
- Invalid ICD diagnosis codes
- Orphan patient/admission records
- Missing or suspicious diagnosis values

## Key Outputs
- 193K+ analytics-ready admissions
- 192K+ analytics-ready claims
- 1.54% simulated 30-day readmission rate
- ~50% claim approval rate
- ~20% denial rate
- ~57–58% payout ratio by payer
- Excel claims operations dashboard

## Excel Dashboard
The Excel dashboard summarizes:
- claim status distribution
- payer performance
- denial reason analysis
- workflow integrity monitoring
- payout ratio by payer

## Project Value
This project demonstrates data profiling, claims workflow validation, financial integrity checks, healthcare readmission analytics, and Excel-based operational reporting.