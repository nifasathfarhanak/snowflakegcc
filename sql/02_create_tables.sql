-- ============================================================================
-- RISKTRACE — PHASE B: DATA MODEL TABLES DDL
-- Project: Snowflake CoCo CLI Hackathon 2026 — GCC Edition
-- ============================================================================

USE DATABASE RISKTRACE_DB;

-- ----------------------------------------------------------------------------
-- 1. CURATED SCHEMA TABLES
-- ----------------------------------------------------------------------------
USE SCHEMA CURATED;

CREATE OR REPLACE TABLE CUSTOMER (
    customer_id VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    kyc_status VARCHAR(20) NOT NULL,
    risk_rating VARCHAR(20) NOT NULL,
    segment VARCHAR(50),
    country VARCHAR(50) DEFAULT 'IND',
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE OR REPLACE TABLE ACCOUNT (
    account_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) REFERENCES CUSTOMER(customer_id),
    account_type VARCHAR(30) NOT NULL, -- SAVINGS, CURRENT, CREDIT_CARD, LOAN
    currency VARCHAR(10) DEFAULT 'INR',
    current_balance NUMBER(18,2) NOT NULL DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    opened_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE OR REPLACE TABLE TRANSACTION (
    transaction_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50) REFERENCES ACCOUNT(account_id),
    counterparty_id VARCHAR(50),
    beneficiary_id VARCHAR(50),
    transaction_type VARCHAR(30) NOT NULL, -- INBOUND_WIRE, OUTBOUND_WIRE, ATM, POS, IMPS, RTGS, NEFT
    amount NUMBER(18,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    status VARCHAR(20) DEFAULT 'COMPLETED',
    channel VARCHAR(30),
    device_id VARCHAR(50),
    location_id VARCHAR(50),
    transaction_timestamp TIMESTAMP_NTZ NOT NULL
);

CREATE OR REPLACE TABLE COUNTERPARTY (
    counterparty_id VARCHAR(50) PRIMARY KEY,
    counterparty_name VARCHAR(100),
    bank_name VARCHAR(100),
    country VARCHAR(50),
    risk_category VARCHAR(30) -- HIGH_RISK, SHELL_CO, NORMAL
);

CREATE OR REPLACE TABLE LOAN (
    loan_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50) REFERENCES ACCOUNT(account_id),
    principal_amount NUMBER(18,2),
    outstanding_balance NUMBER(18,2),
    emi_amount NUMBER(18,2),
    days_past_due INT DEFAULT 0,
    status VARCHAR(30) -- REGULAR, SMA_1, SMA_2, NPA
);

CREATE OR REPLACE TABLE ACCOUNT_BALANCE (
    balance_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50) REFERENCES ACCOUNT(account_id),
    closing_balance NUMBER(18,2),
    snapshot_date DATE NOT NULL
);

-- ----------------------------------------------------------------------------
-- 2. RISK SCHEMA TABLES
-- ----------------------------------------------------------------------------
USE SCHEMA RISK;

CREATE OR REPLACE TABLE RISK_SIGNAL (
    signal_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50),
    customer_id VARCHAR(50),
    scenario_id VARCHAR(50),
    risk_domain VARCHAR(30) NOT NULL, -- AML, FRAUD, CREDIT, LIQUIDITY
    signal_type VARCHAR(50) NOT NULL, -- MULE_PASS_THROUGH, STRUCTURING, VELOCITY_SPIKE, DEFAULT_RISK
    severity VARCHAR(20) NOT NULL,    -- LOW, MEDIUM, HIGH, CRITICAL
    risk_score NUMBER(5,2) NOT NULL,  -- 0.00 to 100.00
    detected_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    rule_version VARCHAR(30) DEFAULT 'v1.0',
    calculation_method VARCHAR(255),
    explanation TEXT
);

-- ----------------------------------------------------------------------------
-- 3. EVIDENCE SCHEMA TABLES
-- ----------------------------------------------------------------------------
USE SCHEMA EVIDENCE;

CREATE OR REPLACE TABLE EVIDENCE (
    evidence_id VARCHAR(50) PRIMARY KEY,
    signal_id VARCHAR(50) REFERENCES RISKTRACE_DB.RISK.RISK_SIGNAL(signal_id),
    evidence_type VARCHAR(30) NOT NULL, -- TRANSACTION, CALCULATION, BEHAVIORAL_BASELINE, POLICY, REGULATORY
    source_table VARCHAR(100),
    source_record_id VARCHAR(100),
    metric_name VARCHAR(100),
    metric_value VARCHAR(255),
    baseline_value VARCHAR(255),
    citation_reference VARCHAR(255),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE OR REPLACE TABLE FINDING (
    finding_id VARCHAR(50) PRIMARY KEY,
    case_id VARCHAR(50),
    account_id VARCHAR(50),
    primary_signal_id VARCHAR(50) REFERENCES RISKTRACE_DB.RISK.RISK_SIGNAL(signal_id),
    summary TEXT,
    confidence_score NUMBER(5,2),
    status VARCHAR(30) DEFAULT 'PENDING_REVIEW', -- PENDING_REVIEW, CONFIRMED, REJECTED, NEEDS_EVIDENCE
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ----------------------------------------------------------------------------
-- 4. REGULATORY SCHEMA TABLES
-- ----------------------------------------------------------------------------
USE SCHEMA REGULATORY;

CREATE OR REPLACE TABLE REGULATORY_DOCUMENT (
    document_id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    jurisdiction VARCHAR(50) NOT NULL, -- RBI, FATF, BASEL_III
    document_type VARCHAR(50) NOT NULL,
    effective_date DATE,
    version VARCHAR(20)
);

CREATE OR REPLACE TABLE REGULATORY_SECTION (
    section_id VARCHAR(50) PRIMARY KEY,
    document_id VARCHAR(50) REFERENCES REGULATORY_DOCUMENT(document_id),
    section_number VARCHAR(50),
    section_title VARCHAR(255),
    chunk_text TEXT NOT NULL
);

-- ----------------------------------------------------------------------------
-- 5. AUDIT SCHEMA TABLES
-- ----------------------------------------------------------------------------
USE SCHEMA AUDIT;

CREATE OR REPLACE TABLE AUDIT_EVENT (
    audit_id VARCHAR(50) PRIMARY KEY,
    session_id VARCHAR(50),
    user_id VARCHAR(50),
    user_question TEXT,
    detected_intent VARCHAR(50),
    tools_executed VARIANT,
    queries_run VARIANT,
    evidence_ids VARIANT,
    ai_response TEXT,
    confidence_score NUMBER(5,2),
    human_decision VARCHAR(30),
    analyst_notes TEXT,
    event_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
