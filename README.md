Healthcare Claims Workflow & Readmission Analytics Pipeline

Built a Python + Excel analytics pipeline to validate and analyze healthcare insurance claims across 400K+ relational records spanning patients, admissions, claims, and readmissions datasets.

Project Objectives

This project simulates a real-world claims analytics workflow used by insurance operations and healthcare quality teams to:

detect billing inconsistencies
validate claim lifecycle logic
monitor approval and denial trends
analyze payer settlement efficiency
evaluate 30-day hospital readmission risk patterns

Dataset Overview
Table	    Records
Patients	10,000
Admissions	200,000
Claims	    200,000
Readmissions	~3,000

Intentional data quality issues were injected to simulate real operational datasets:

invalid diagnosis codes
orphan admissions
negative LOS values
approval > billed anomalies
workflow timing violations
Data Validation Pipeline

Implemented automated integrity checks for:

financial rule validation (approved ≤ billed)
payment timing consistency
diagnosis code formatting
admission date logic
orphan record detection
LOS correction logic
workflow readiness flags

Result:

96%+ analytics-ready admissions
96%+ analytics-ready claims
Claims Analytics KPIs Generated

Calculated:

approval rate (~50%)
denial rate (~20%)
pending rate (~20%)
payout ratio by payer (~57%)
denial reason distribution
workflow readiness coverage
Outcome Analytics (Hospital Readmissions)

Analyzed:

department-level readmission risk
readmission cause distribution
discharge-to-readmission timelines
30-day readmission rate (~1.5%)

Example insight:

Most readmissions occurred in the 15–30 day window (~53%), indicating expected follow-up cycle behavior rather than early discharge failure patterns.

Excel Dashboard

Built an operational Excel dashboard summarizing:

claim approval performance
payer settlement efficiency
denial drivers
workflow readiness metrics

Designed to simulate analyst reporting used in insurance claims operations environments.

Tools Used

Python
Pandas
NumPy
Excel (operations dashboard reporting)