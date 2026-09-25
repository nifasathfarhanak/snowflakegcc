-- ============================================================================
-- RISKTRACE — PHASE G: EVIDENCE LINEAGE ENGINE ("PROVE THIS FINDING")
-- Populates evidence graph linking signals, transactions, calculations, and regulatory rules
-- Project: Snowflake CoCo CLI Hackathon 2026 — GCC Edition
-- ============================================================================

USE DATABASE RISKTRACE_DB;
USE SCHEMA EVIDENCE;

-- Procedure to populate evidence records for Account A1029 Demo Case
CREATE OR REPLACE PROCEDURE SP_BUILD_EVIDENCE_FOR_ACCOUNT(ACCOUNT_ID_PARAM VARCHAR)
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    -- 1. Inbound Transaction Evidence
    INSERT INTO EVIDENCE (evidence_id, signal_id, evidence_type, source_table, source_record_id, metric_name, metric_value, baseline_value, citation_reference)
    VALUES (
        'EVID-001', 'SIG-AML-DEMO-01', 'TRANSACTION', 'CURATED.TRANSACTION', 'TXN-048022',
        'Inbound Volume Summary', '17 transactions from 14 counterparties (₹8.7L total)', '2 transactions / month baseline', 'Account A1029 Inbound Stream'
    );

    -- 2. Outbound Pass-Through Calculation Evidence
    INSERT INTO EVIDENCE (evidence_id, signal_id, evidence_type, source_table, source_record_id, metric_name, metric_value, baseline_value, citation_reference)
    VALUES (
        'EVID-002', 'SIG-AML-DEMO-01', 'CALCULATION', 'RISK.ACCOUNT_BEHAVIORAL_BASELINE', 'A1029-METRICS',
        'Outbound Transfer Ratio & Holding Time', '₹8.3L transferred out (95.4% ratio) with 11-min median holding time', '8.4x baseline activity deviation', 'Metric Calc ID #8492'
    );

    -- 3. Regulatory Grounding Citation Evidence
    INSERT INTO EVIDENCE (evidence_id, signal_id, evidence_type, source_table, source_record_id, metric_name, metric_value, baseline_value, citation_reference)
    VALUES (
        'EVID-003', 'SIG-AML-DEMO-01', 'REGULATORY', 'REGULATORY.REGULATORY_SECTION', 'RBI-AML-SEC-4.2',
        'RBI Master Direction on KYC/AML', 'Section 4.2: Pass-Through / Mule Account Indicators requiring mandatory STR filing within 7 days', 'N/A', 'RBI/2023-24/94 Master Direction Sec 4.2'
    );

    -- 4. Create Audit-Ready Finding Record
    INSERT INTO FINDING (finding_id, case_id, account_id, primary_signal_id, summary, confidence_score, status)
    VALUES (
        'FINDING-A1029', 'CASE-2026-001', ACCOUNT_ID_PARAM, 'SIG-AML-DEMO-01',
        'Account A1029 identified as potential Money Mule. Received ₹8.7L across 17 inbound wires from unrelated counterparties, rapidly transferred out ₹8.3L (11-min holding time). Supported by RBI Master Direction Sec 4.2.',
        96.50, 'PENDING_REVIEW'
    );

    RETURN 'Successfully generated evidence lineage graph for ' || ACCOUNT_ID_PARAM;
END;
$$;
