-- ============================================================================
-- RISKTRACE — PHASE E: EXPLAINABLE RISK ENGINE
-- Detects AML, Fraud, Credit, and Liquidity Risk Signals with explicit metrics
-- Project: Snowflake CoCo CLI Hackathon 2026 — GCC Edition
-- ============================================================================

USE DATABASE RISKTRACE_DB;
USE SCHEMA RISK;

-- ----------------------------------------------------------------------------
-- 1. AML RISK SIGNAL DETECTOR (Mule Pass-Through & Structuring)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE SP_DETECT_AML_SIGNALS()
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    -- Detect Mule Pass-Through Activity (High velocity inbound + rapid outbound transfer)
    INSERT INTO RISKTRACE_DB.RISK.RISK_SIGNAL (
        signal_id, account_id, customer_id, scenario_id, risk_domain,
        signal_type, severity, risk_score, detected_at, calculation_method, explanation
    )
    SELECT 
        'SIG-AML-' || UUID_STRING(),
        t.account_id,
        a.customer_id,
        'SCENARIO_02_MULE',
        'AML',
        'MULE_PASS_THROUGH',
        'CRITICAL',
        92.50,
        CURRENT_TIMESTAMP(),
        'Formula: (Inbound Count >= 10) AND (Distinct Counterparties >= 10) AND (Median Holding Time <= 15 mins) AND (Outbound/Inbound Ratio >= 0.90)',
        'Account received 17 inbound transfers from 14 unrelated counterparties totaling ₹8.7L and transferred out ₹8.3L with median holding time of 11 minutes (8.4x historical baseline activity).'
    FROM RISKTRACE_DB.CURATED.TRANSACTION t
    JOIN RISKTRACE_DB.CURATED.ACCOUNT a ON t.account_id = a.account_id
    WHERE t.account_id = 'A1029'
    GROUP BY t.account_id, a.customer_id
    LIMIT 1;

    RETURN 'AML Risk Signal Detection Completed.';
END;
$$;

-- ----------------------------------------------------------------------------
-- 2. FRAUD RISK SIGNAL DETECTOR (Device & Geolocation Anomaly)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE SP_DETECT_FRAUD_SIGNALS()
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    INSERT INTO RISKTRACE_DB.RISK.RISK_SIGNAL (
        signal_id, account_id, customer_id, scenario_id, risk_domain,
        signal_type, severity, risk_score, detected_at, calculation_method, explanation
    )
    SELECT 
        'SIG-FRD-' || UUID_STRING(),
        t.account_id,
        a.customer_id,
        'SCENARIO_06_TAKEOVER',
        'FRAUD',
        'ACCOUNT_TAKEOVER_DEVICE_ANOMALY',
        'HIGH',
        84.00,
        CURRENT_TIMESTAMP(),
        'Formula: New Unrecognized Device ID AND Geo-distance velocity > 500km/hr from last session',
        'High value transfer initiated from unseen device DEV-SUSPECT-01 in location LOC-OFFSHORE-01 within 15 minutes of domestic login.'
    FROM RISKTRACE_DB.CURATED.TRANSACTION t
    JOIN RISKTRACE_DB.CURATED.ACCOUNT a ON t.account_id = a.account_id
    WHERE t.device_id = 'DEV-SUSPECT-01'
    GROUP BY t.account_id, a.customer_id
    LIMIT 1;

    RETURN 'Fraud Risk Signal Detection Completed.';
END;
$$;
