-- ============================================================================
-- RISKTRACE — PHASE D: DATA PIPELINES (RAW -> CURATED -> FEATURE STORE)
-- Project: Snowflake CoCo CLI Hackathon 2026 — GCC Edition
-- ============================================================================

USE DATABASE RISKTRACE_DB;
USE SCHEMA STAGING;

-- 1. Create Staging Stream for Incremental Transaction Ingestion
CREATE OR REPLACE STREAM TRANSACTION_RAW_STREAM ON TABLE RISKTRACE_DB.RAW.RAW_TRANSACTION;

-- 2. Create Dynamic Table for Real-Time 30-Day Behavioral Baseline per Account
CREATE OR REPLACE DYNAMIC TABLE RISKTRACE_DB.RISK.ACCOUNT_BEHAVIORAL_BASELINE
    TARGET_LAG = '1 minute'
    WAREHOUSE = COMPUTE_WH
AS
SELECT 
    account_id,
    COUNT(transaction_id) AS txn_count_30d,
    SUM(amount) AS total_volume_30d,
    AVG(amount) AS avg_txn_amount_30d,
    MEDIAN(DATEDIFF('minute', LAG(transaction_timestamp) OVER (PARTITION BY account_id ORDER BY transaction_timestamp), transaction_timestamp)) AS median_holding_time_minutes,
    COUNT(DISTINCT counterparty_id) AS distinct_counterparty_count_30d,
    MAX(transaction_timestamp) AS last_txn_time
FROM RISKTRACE_DB.CURATED.TRANSACTION
WHERE transaction_timestamp >= DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY account_id;

-- 3. Stored Procedure for Incrementally Pipeline Loading
CREATE OR REPLACE PROCEDURE RISKTRACE_DB.CURATED.SP_LOAD_CURATED_TRANSACTIONS()
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    INSERT INTO RISKTRACE_DB.CURATED.TRANSACTION (
        transaction_id, account_id, counterparty_id, beneficiary_id,
        transaction_type, amount, currency, status, channel, device_id, location_id, transaction_timestamp
    )
    SELECT 
        raw_json:transaction_id::VARCHAR,
        raw_json:account_id::VARCHAR,
        raw_json:counterparty_id::VARCHAR,
        raw_json:beneficiary_id::VARCHAR,
        raw_json:transaction_type::VARCHAR,
        raw_json:amount::NUMBER(18,2),
        raw_json:currency::VARCHAR,
        raw_json:status::VARCHAR,
        raw_json:channel::VARCHAR,
        raw_json:device_id::VARCHAR,
        raw_json:location_id::VARCHAR,
        raw_json:transaction_timestamp::TIMESTAMP_NTZ
    FROM RISKTRACE_DB.RAW.RAW_TRANSACTION;

    RETURN 'Successfully loaded curated transactions pipeline.';
END;
$$;
