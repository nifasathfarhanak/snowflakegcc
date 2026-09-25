# RiskTrace Snowflake Data Model Specification

**Project Name:** RiskTrace — Evidence-First Financial Risk Intelligence Copilot  
**Database Namespace:** `RISKTRACE_DB`  

---

## 🗂️ Database Schemas Overview

```
RISKTRACE_DB
├── RAW          -- Staging tables for synthetic banking ingestion
├── CURATED      -- Cleaned, dimensionally modeled core entity tables
├── RISK         -- Risk features, signals, scores, and detector outputs
├── REGULATORY   -- Policy documents, regulatory sections, and vector embeddings
├── EVIDENCE     -- Granular evidence records and graph relation lineages
├── AUDIT        -- Immutable prompt/query execution logs & human decisions
├── AGENT        -- Semantic layer views & Cortex Agent tool procedures
└── TEST         -- Automated test assertions and evaluation results
```

---

## 📜 Table Definitions & DDL Specs

### 1. RAW Schema (`RISKTRACE_DB.RAW`)
- `RAW_CUSTOMER`: Ingested customer demography & KYC metadata.
- `RAW_ACCOUNT`: Ingested account master details & status.
- `RAW_TRANSACTION`: High-throughput transaction stream payload.
- `RAW_COUNTERPARTY`: Counterparty entity registry.
- `RAW_BENEFICIARY`: Registered beneficiary accounts.
- `RAW_DEVICE`: Login/Device metadata for digital transactions.
- `RAW_LOCATION`: Geo-location IP/GPS data per session.
- `RAW_LOAN`: Credit agreements, EMI schedules & balances.
- `RAW_PAYMENT`: Repayment transaction records.
- `RAW_ACCOUNT_BALANCE`: End-of-day & intraday balance snapshots.

---

### 2. CURATED Schema (`RISKTRACE_DB.CURATED`)

```sql
CREATE OR REPLACE TABLE RISKTRACE_DB.CURATED.CUSTOMER (
    customer_id VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(100),
    kyc_status VARCHAR(20),
    risk_rating VARCHAR(20),
    segment VARCHAR(50),
    country VARCHAR(50),
    created_at TIMESTAMP_NTZ
);

CREATE OR REPLACE TABLE RISKTRACE_DB.CURATED.ACCOUNT (
    account_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) REFERENCES RISKTRACE_DB.CURATED.CUSTOMER(customer_id),
    account_type VARCHAR(30), -- SAVINGS, CURRENT, CREDIT_CARD, LOAN
    currency VARCHAR(10),
    current_balance NUMBER(18,2),
    status VARCHAR(20),
    opened_at TIMESTAMP_NTZ
);

CREATE OR REPLACE TABLE RISKTRACE_DB.CURATED.TRANSACTION (
    transaction_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50) REFERENCES RISKTRACE_DB.CURATED.ACCOUNT(account_id),
    counterparty_id VARCHAR(50),
    beneficiary_id VARCHAR(50),
    transaction_type VARCHAR(30), -- INBOUND_WIRE, OUTBOUND_WIRE, ATM, POS
    amount NUMBER(18,2),
    currency VARCHAR(10),
    status VARCHAR(20),
    channel VARCHAR(30),
    device_id VARCHAR(50),
    location_id VARCHAR(50),
    transaction_timestamp TIMESTAMP_NTZ
);
```

---

### 3. RISK Schema (`RISKTRACE_DB.RISK`)

```sql
CREATE OR REPLACE TABLE RISKTRACE_DB.RISK.RISK_SIGNAL (
    signal_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50),
    customer_id VARCHAR(50),
    risk_domain VARCHAR(30), -- AML, FRAUD, CREDIT, LIQUIDITY
    signal_type VARCHAR(50), -- MULE_PASS_THROUGH, STRUCTURING, VELOCITY_SPIKE, CREDIT_DEFAULT, OUTFLOW_SURGE
    severity VARCHAR(20),    -- LOW, MEDIUM, HIGH, CRITICAL
    risk_score NUMBER(5,2),  -- 0.00 to 100.00
    detected_at TIMESTAMP_NTZ,
    rule_or_model_version VARCHAR(30),
    calculation_method VARCHAR(255),
    explanation TEXT
);
```

---

### 4. EVIDENCE Schema (`RISKTRACE_DB.EVIDENCE`)

```sql
CREATE OR REPLACE TABLE RISKTRACE_DB.EVIDENCE.EVIDENCE (
    evidence_id VARCHAR(50) PRIMARY KEY,
    signal_id VARCHAR(50) REFERENCES RISKTRACE_DB.RISK.RISK_SIGNAL(signal_id),
    evidence_type VARCHAR(30), -- TRANSACTION, CALCULATION, BEHAVIORAL_BASELINE, POLICY, REGULATORY
    source_table VARCHAR(100),
    source_record_id VARCHAR(100),
    metric_name VARCHAR(100),
    metric_value VARCHAR(255),
    baseline_value VARCHAR(255),
    citation_reference VARCHAR(255),
    created_at TIMESTAMP_NTZ
);

CREATE OR REPLACE TABLE RISKTRACE_DB.EVIDENCE.FINDING (
    finding_id VARCHAR(50) PRIMARY KEY,
    case_id VARCHAR(50),
    account_id VARCHAR(50),
    primary_signal_id VARCHAR(50),
    summary TEXT,
    confidence_score NUMBER(5,2),
    status VARCHAR(30), -- PENDING_REVIEW, CONFIRMED, REJECTED, NEEDS_EVIDENCE
    created_at TIMESTAMP_NTZ
);
```

---

### 5. REGULATORY Schema (`RISKTRACE_DB.REGULATORY`)

```sql
CREATE OR REPLACE TABLE RISKTRACE_DB.REGULATORY.REGULATORY_DOCUMENT (
    document_id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255),
    jurisdiction VARCHAR(50), -- RBI, FATF, BASEL_III
    document_type VARCHAR(50), -- CIRCULAR, REGULATION, INTERNAL_POLICY
    effective_date DATE,
    version VARCHAR(20)
);

CREATE OR REPLACE TABLE RISKTRACE_DB.REGULATORY.REGULATORY_SECTION (
    section_id VARCHAR(50) PRIMARY KEY,
    document_id VARCHAR(50) REFERENCES RISKTRACE_DB.REGULATORY.REGULATORY_DOCUMENT(document_id),
    section_number VARCHAR(50),
    section_title VARCHAR(255),
    chunk_text TEXT,
    embedding VECTOR(FLOAT, 768) -- Snowflake Cortex Embedding
);
```

---

### 6. AUDIT Schema (`RISKTRACE_DB.AUDIT`)

```sql
CREATE OR REPLACE TABLE RISKTRACE_DB.AUDIT.AUDIT_EVENT (
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
    event_timestamp TIMESTAMP_NTZ
);
```
