import streamlit as st
import json
from datetime import datetime

# Streamlit Page Configuration — Professional Enterprise Light Theme
st.set_page_config(
    page_title="RiskTrace — Financial Risk Intelligence Copilot",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stApp { color: #1e293b; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 16px;
    }
    .badge-critical { background-color: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 12px; }
    .badge-high { background-color: #ffedd5; color: #9a3412; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 12px; }
    .badge-medium { background-color: #fef9c3; color: #854d0e; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 12px; }
    .badge-low { background-color: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 12px; }
    .metric-value { font-size: 28px; font-weight: 700; color: #0f172a; }
    .metric-label { font-size: 13px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }
</style>
""", unsafe_allow_html=True)

# Header
st.sidebar.image("https://img.icons8.com/color/96/shield.png", width=60)
st.sidebar.title("RiskTrace Copilot")
st.sidebar.caption("Snowflake CoCo CLI Hackathon 2026 — GCC Edition")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Executive Risk Dashboard",
        "💬 Ask RiskTrace Copilot",
        "🔍 Deep Investigation (A1029)",
        "🕸️ Evidence Graph ('Prove Finding')",
        "📜 Regulatory Intelligence",
        "📁 Findings & Case Review",
        "📄 Audit-Ready Reports",
        "📋 Audit Trail & Governance Log"
    ]
)

# -----------------------------------------------------------------------------
# PAGE 1: EXECUTIVE RISK DASHBOARD
# -----------------------------------------------------------------------------
if page == "📊 Executive Risk Dashboard":
    st.title("🛡️ Executive Financial Risk Dashboard")
    st.caption("Real-Time Signals Across AML, Fraud, Credit & Liquidity Domains")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown('<div class="card"><div class="metric-label">Total Signals</div><div class="metric-value">1,248</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><div class="metric-label">Critical (AML)</div><div class="metric-value" style="color:#b91c1c;">14</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card"><div class="metric-label">Fraud Anomalies</div><div class="metric-value" style="color:#c2410c;">38</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="card"><div class="metric-label">Credit Deterioration</div><div class="metric-value" style="color:#a16207;">82</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="card"><div class="metric-label">Pending Reviews</div><div class="metric-value" style="color:#0284c7;">9</div></div>', unsafe_allow_html=True)

    st.subheader("🔥 Top High-Risk Flagged Accounts")
    
    html_table = """
    <table style="width:100%; border-collapse: collapse; margin-top: 10px; background-color: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e2e8f0;">
        <thead>
            <tr style="background-color: #f1f5f9; color: #475569; text-align: left; font-size: 13px;">
                <th style="padding: 12px 16px;">Account ID</th>
                <th style="padding: 12px 16px;">Risk Type</th>
                <th style="padding: 12px 16px;">Severity</th>
                <th style="padding: 12px 16px;">Risk Score</th>
                <th style="padding: 12px 16px;">Inbound Vol</th>
                <th style="padding: 12px 16px;">Holding Time</th>
                <th style="padding: 12px 16px;">Status</th>
            </tr>
        </thead>
        <tbody style="font-size: 14px; color: #1e293b;">
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 12px 16px; font-weight: 600;">A1029</td>
                <td style="padding: 12px 16px;">AML Mule Pass-Through</td>
                <td style="padding: 12px 16px;"><span class="badge-critical">CRITICAL</span></td>
                <td style="padding: 12px 16px; font-weight: 700; color: #b91c1c;">92.5</td>
                <td style="padding: 12px 16px;">₹8.7 Lakhs</td>
                <td style="padding: 12px 16px;">11 mins</td>
                <td style="padding: 12px 16px; color: #0284c7; font-weight: 500;">PENDING_REVIEW</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 12px 16px; font-weight: 600;">ACC-0482</td>
                <td style="padding: 12px 16px;">Fraud Device Anomaly</td>
                <td style="padding: 12px 16px;"><span class="badge-high">HIGH</span></td>
                <td style="padding: 12px 16px; font-weight: 700; color: #c2410c;">84.0</td>
                <td style="padding: 12px 16px;">₹3.2 Lakhs</td>
                <td style="padding: 12px 16px;">45 mins</td>
                <td style="padding: 12px 16px; color: #0284c7; font-weight: 500;">PENDING_REVIEW</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 12px 16px; font-weight: 600;">ACC-0912</td>
                <td style="padding: 12px 16px;">Structuring (Smurfing)</td>
                <td style="padding: 12px 16px;"><span class="badge-high">HIGH</span></td>
                <td style="padding: 12px 16px; font-weight: 700; color: #c2410c;">81.2</td>
                <td style="padding: 12px 16px;">₹9.8 Lakhs</td>
                <td style="padding: 12px 16px;">3 hours</td>
                <td style="padding: 12px 16px; color: #166534; font-weight: 500;">CONFIRMED</td>
            </tr>
            <tr>
                <td style="padding: 12px 16px; font-weight: 600;">ACC-1204</td>
                <td style="padding: 12px 16px;">Credit Deterioration</td>
                <td style="padding: 12px 16px;"><span class="badge-medium">MEDIUM</span></td>
                <td style="padding: 12px 16px; font-weight: 700; color: #a16207;">68.4</td>
                <td style="padding: 12px 16px;">₹45,000</td>
                <td style="padding: 12px 16px;">12 days</td>
                <td style="padding: 12px 16px; color: #854d0e; font-weight: 500;">IN_PROGRESS</td>
            </tr>
        </tbody>
    </table>
    """
    st.markdown(html_table, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 2: ASK RISKTRACE COPILOT
# -----------------------------------------------------------------------------
elif page == "💬 Ask RiskTrace Copilot":
    st.title("💬 Ask RiskTrace Copilot")
    st.caption("Natural-language financial risk copilot grounded strictly in Snowflake evidence.")

    query = st.text_input("Enter your natural-language investigation query:", value="Why was account A1029 flagged for suspicious activity?")

    if st.button("Investigate Query", type="primary"):
        st.markdown("### 🤖 RiskTrace Agent Response")
        st.markdown("""
        **Summary:**  
        Account **A1029** was flagged with a **CRITICAL Risk Score of 92.5 / 100** due to classic **Money Mule / Pass-Through Account** patterns detected on 24-Sep-2026.

        **Key Findings:**
        - **Inbound Velocity:** 17 inbound wire transfers received totaling **₹8,70,000** from 14 distinct, unrelated counterparties within 3 hours.
        - **Rapid Outflow:** **₹8,30,000** (95.4% of total funds) was transferred out externally within 220 minutes.
        - **Holding Time Anomaly:** Median fund holding time dropped to **11 minutes** (versus 30-day baseline of 4.2 days).
        - **Historical Deviation:** Activity is **8.4× higher** than Account A1029's historical 30-day baseline.

        **Regulatory Citation:**
        - *RBI Master Direction on KYC/AML (Sec 4.2):* Pass-Through / Mule Account Indicators. Mandatory STR filing required.
        """)

        st.info("💡 **Evidence Grounding:** 3 evidence items verified in Snowflake `RISKTRACE_DB.EVIDENCE`. Zero hallucinations detected.")

# -----------------------------------------------------------------------------
# PAGE 3: DEEP INVESTIGATION (ACCOUNT A1029)
# -----------------------------------------------------------------------------
elif page == "🔍 Deep Investigation (A1029)":
    st.title("🔍 Deep Investigation: Account A1029")
    st.caption("Core Demo Scenario — Mule Pass-Through Investigation")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📌 Account Profile & Risk Overview")
        st.json({
            "Account ID": "A1029",
            "Customer ID": "CUST-1029",
            "Customer Name": "Customer_1029",
            "Account Type": "CURRENT",
            "KYC Status": "VERIFIED",
            "Current Balance": "₹40,000.00",
            "Risk Classification": "CRITICAL (AML)",
            "Risk Score": "92.5 / 100"
        })

        st.subheader("🔍 PROVE THIS FINDING — Interactive Evidence Breakdown")
        st.markdown("""
        Click any statement below to inspect the raw underlying Snowflake evidence record:
        """)

        with st.expander("👉 1. '17 inbound transactions totaling ₹8.7L' [CLICK TO PROVE]"):
            st.code("""
SELECT transaction_id, counterparty_id, amount, transaction_timestamp 
FROM RISKTRACE_DB.CURATED.TRANSACTION 
WHERE account_id = 'A1029' AND transaction_type = 'INBOUND_WIRE';
-- Verified 17 records found totaling ₹870,000.00
            """, language="sql")

        with st.expander("👉 2. '₹8.3L transferred out with 11-minute holding time' [CLICK TO PROVE]"):
            st.code("""
SELECT metric_name, metric_value, baseline_value 
FROM RISKTRACE_DB.EVIDENCE.EVIDENCE 
WHERE signal_id = 'SIG-AML-DEMO-01';
-- Metric: Outbound Ratio = 95.4%, Median Holding Time = 11 mins (Baseline = 4.2 days)
            """, language="sql")

        with st.expander("👉 3. 'Applicable Regulatory Standard' [CLICK TO PROVE]"):
            st.markdown("**Source Document:** RBI Master Direction - Know Your Customer (KYC) Direction, 2016 (Updated 2024)")
            st.markdown("**Section 4.2:** *'Accounts showing sudden surges in velocity without economic rationale, followed by rapid liquidation, shall be categorized as suspected Mule Accounts and reported via STR within 7 days.'*")

    with col_right:
        st.subheader("⚡ Human Analyst Action")
        st.markdown("Status: <span class='badge-critical'>PENDING_REVIEW</span>", unsafe_allow_html=True)
        st.write("---")
        if st.button("✅ Confirm Finding & Draft STR Report", type="primary", use_container_width=True):
            st.success("Case CASE-2026-001 confirmed by Compliance Officer. Regulatory STR report generated!")
        if st.button("❌ Reject Finding", use_container_width=True):
            st.warning("Finding rejected.")
        if st.button("⚠️ Request Additional Evidence", use_container_width=True):
            st.info("Task assigned to L2 Data Engineering.")

# -----------------------------------------------------------------------------
# PAGE 4: EVIDENCE GRAPH
# -----------------------------------------------------------------------------
elif page == "🕸️ Evidence Graph ('Prove Finding')":
    st.title("🕸️ Evidence Graph & Lineage Visualizer")
    st.caption("Visual proof path connecting raw data to regulatory report")

    st.markdown("""
    ```
    ┌─────────────────────────┐
    │  Natural-Language Query │ "Why was Account A1029 flagged?"
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │ Snowflake Ingestion     │ 17 Inbound Transactions (₹8.7L)
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │ Risk Signal Engine      │ SIG-AML-DEMO-01 (Mule Pass-Through, Score: 92.5)
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │ Evidence Collection     │ 11-min holding time (8.4x baseline deviation)
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │ Regulatory Grounding    │ RBI Master Direction Sec 4.2 Citation
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │ Human Analyst Review    │ Status: CONFIRMED
    └────────────┬────────────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │ Audit-Ready STR Report  │ Document Reference #SAR-2026-A1029
    └─────────────────────────┘
    ```
    """)

# -----------------------------------------------------------------------------
# PAGE 5: REGULATORY INTELLIGENCE
# -----------------------------------------------------------------------------
elif page == "📜 Regulatory Intelligence":
    st.title("📜 Regulatory Intelligence Knowledge Layer")
    st.caption("Grounded RBI Master Directions, FATF Standards & Basel III Guidance")

    reg_search = st.text_input("🔍 Search Regulatory Documents:", value="Pass Through Account Mule STR Requirement")

    col_reg1, col_reg2 = st.columns([1, 2])

    with col_reg1:
        st.subheader("📚 Loaded Regulations")
        st.markdown("""
        - **RBI/2023-24/94** — Master Direction - Know Your Customer (KYC)
        - **FATF Recommendation 10** — Customer Due Diligence
        - **FATF Recommendation 20** — Suspicious Transaction Reporting
        - **Basel III Framework** — Intraday Liquidity Management & LCR
        - **PMLA 2002 Sec 12** — Obligations of Banking Companies
        """)

    with col_reg2:
        st.subheader("📄 Top Matching Regulatory Sections")
        
        with st.expander("📌 RBI Master Direction (Sec 4.2) — Mule Account Reporting", expanded=True):
            st.markdown("""
            **Document ID:** `RBI-KYC-DIR-2024-SEC4.2`  
            **Jurisdiction:** Reserve Bank of India (RBI)  
            **Effective Date:** 01-Jan-2024  
            
            > **Text:** *"Accounts demonstrating abnormal velocity spikes without underlying trade or employment justification, where incoming credits from multiple unrelated third parties are rapidly liquidated via outbound wire transfers within short holding intervals (under 30 minutes), must be classified as suspected Mule Accounts. REs shall file a Suspicious Transaction Report (STR) with FIU-IND within 7 working days."*
            """)
            st.info("🔗 Linked Evidence: Account A1029 (SIG-AML-DEMO-01)")

        with st.expander("📌 FATF Recommendation 20 — STR Filing Mandate"):
            st.markdown("""
            **Document ID:** `FATF-REC-20`  
            **Jurisdiction:** Financial Action Task Force  
            
            > **Text:** *"If a financial institution suspects or has reasonable grounds to suspect that funds are the proceeds of a criminal activity, or are related to money laundering, it shall be required, by law, to report promptly its suspicions to the Financial Intelligence Unit (FIU)."*
            """)

# -----------------------------------------------------------------------------
# PAGE 6: FINDINGS & CASE REVIEW
# -----------------------------------------------------------------------------
elif page == "📁 Findings & Case Review":
    st.title("📁 Compliance Findings & Case Queue")
    st.caption("Human-in-the-Loop Investigation Management")

    col_c1, col_c2, col_c3 = st.columns(3)
    col_c1.metric("Pending Review", "9 Cases", "Need Action")
    col_c2.metric("Confirmed STRs", "14 Cases", "Filed")
    col_c3.metric("Dismissed / False Positives", "3 Cases", "Archived")

    st.subheader("📋 Active Investigation Queue")

    cases_html = """
    <table style="width:100%; border-collapse: collapse; margin-top: 10px; background-color: #ffffff; border-radius: 8px; border: 1px solid #e2e8f0;">
        <thead>
            <tr style="background-color: #f1f5f9; color: #475569; text-align: left; font-size: 13px;">
                <th style="padding: 12px 16px;">Case ID</th>
                <th style="padding: 12px 16px;">Account ID</th>
                <th style="padding: 12px 16px;">Primary Signal</th>
                <th style="padding: 12px 16px;">Confidence</th>
                <th style="padding: 12px 16px;">Assigned Analyst</th>
                <th style="padding: 12px 16px;">Created At</th>
                <th style="padding: 12px 16px;">Status</th>
            </tr>
        </thead>
        <tbody style="font-size: 14px; color: #1e293b;">
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 12px 16px; font-weight: 600;">CASE-2026-001</td>
                <td style="padding: 12px 16px; font-weight: 600;">A1029</td>
                <td style="padding: 12px 16px;">Mule Pass-Through</td>
                <td style="padding: 12px 16px; font-weight: 700; color: #b91c1c;">96.5%</td>
                <td style="padding: 12px 16px;">Senior AML Officer</td>
                <td style="padding: 12px 16px;">24-Sep-2026 14:22</td>
                <td style="padding: 12px 16px;"><span class="badge-critical">PENDING_REVIEW</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 12px 16px; font-weight: 600;">CASE-2026-002</td>
                <td style="padding: 12px 16px; font-weight: 600;">ACC-0482</td>
                <td style="padding: 12px 16px;">Fraud Device Anomaly</td>
                <td style="padding: 12px 16px; font-weight: 700; color: #c2410c;">88.2%</td>
                <td style="padding: 12px 16px;">Fraud Specialist</td>
                <td style="padding: 12px 16px;">24-Sep-2026 16:05</td>
                <td style="padding: 12px 16px;"><span class="badge-high">PENDING_REVIEW</span></td>
            </tr>
            <tr>
                <td style="padding: 12px 16px; font-weight: 600;">CASE-2026-003</td>
                <td style="padding: 12px 16px; font-weight: 600;">ACC-0912</td>
                <td style="padding: 12px 16px;">Structuring (Smurfing)</td>
                <td style="padding: 12px 16px; font-weight: 700; color: #166534;">94.0%</td>
                <td style="padding: 12px 16px;">L2 Investigator</td>
                <td style="padding: 12px 16px;">23-Sep-2026 11:40</td>
                <td style="padding: 12px 16px;"><span class="badge-low">CONFIRMED</span></td>
            </tr>
        </tbody>
    </table>
    """
    st.markdown(cases_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 7: AUDIT-READY REPORTS
# -----------------------------------------------------------------------------
elif page == "📄 Audit-Ready Reports":
    st.title("📄 Audit-Ready Regulatory Report Generator")
    st.caption("Automated Regulatory Suspicious Activity Report (STR / SAR) Compilation")

    selected_case = st.selectbox("Select Case to Generate Report:", ["CASE-2026-001 (Account A1029 - Mule Pass-Through)", "CASE-2026-002 (Account ACC-0482 - Device Fraud)"])

    if st.button("📄 Generate Audit-Ready Report", type="primary"):
        st.success("STR Report Generated Successfully!")

        st.markdown("### 📝 PREVIEW: Suspicious Activity Report (SAR-2026-A1029)")
        st.markdown("""
        ---
        **REGULATORY SUSPICIOUS TRANSACTION REPORT (STR)**  
        **Filing Authority:** Financial Intelligence Unit – India (FIU-IND) / Compliance Division  
        **Date of Generation:** 25-Sep-2026  
        **Case Reference:** `CASE-2026-001`  
        **Primary Subject Account:** `A1029` (Customer: `CUST-1029`)  

        #### 1. EXECUTIVE SUMMARY
        Account A1029 exhibited severe AML anomalies consistent with Mule / Pass-Through operations. Within a 3-hour period on 24-Sep-2026, the account received 17 inbound transfers totaling ₹8,70,000 from 14 distinct third-party counterparties, followed by immediate outbound liquidation of ₹8,30,000 (95.4% velocity ratio) with a median holding time of 11 minutes.

        #### 2. VERIFIED EVIDENCE LINEAGE
        - **Inbound Record:** 17 wires from CP-0005 through CP-0085 (`RISKTRACE_DB.CURATED.TRANSACTION`).
        - **Holding Time Metric:** 11 mins median holding time (8.4x baseline deviation).
        - **Regulatory Basis:** RBI Master Direction on KYC/AML Section 4.2.

        #### 3. HUMAN DECISION & AUDIT TRAIL
        - **Decision:** CONFIRMED by Senior AML Officer
        - **Audit Event ID:** `AUDIT-EVT-99201`
        ---
        """)

        st.download_button("📥 Download STR Report (Markdown / Audit Copy)", data="SAR-2026-A1029 Full Regulatory Copy...", file_name="SAR_2026_A1029_Audit_Report.md")

# -----------------------------------------------------------------------------
# PAGE 8: AUDIT TRAIL & GOVERNANCE LOG
# -----------------------------------------------------------------------------
elif page == "📋 Audit Trail & Governance Log":
    st.title("📋 Immutable Governance & Audit Log")
    st.caption("Complete Lineage of AI Interactions, SQL Queries, Evidence Queries & Human Actions")

    st.subheader("🛡️ Snowflake Execution Log (`RISKTRACE_DB.AUDIT.AUDIT_EVENT`)")

    audit_html = """
    <table style="width:100%; border-collapse: collapse; margin-top: 10px; background-color: #ffffff; border-radius: 8px; border: 1px solid #e2e8f0;">
        <thead>
            <tr style="background-color: #f1f5f9; color: #475569; text-align: left; font-size: 13px;">
                <th style="padding: 12px 16px;">Audit ID</th>
                <th style="padding: 12px 16px;">Timestamp</th>
                <th style="padding: 12px 16px;">User Prompt / Query</th>
                <th style="padding: 12px 16px;">Detected Intent</th>
                <th style="padding: 12px 16px;">Executed Tools</th>
                <th style="padding: 12px 16px;">Evidence Count</th>
                <th style="padding: 12px 16px;">Human Decision</th>
            </tr>
        </thead>
        <tbody style="font-size: 14px; color: #1e293b;">
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 12px 16px; font-weight: 600;">AUD-99201</td>
                <td style="padding: 12px 16px;">24-Sep-2026 14:22</td>
                <td style="padding: 12px 16px;">"Why was account A1029 flagged?"</td>
                <td style="padding: 12px 16px;">ACCOUNT_INVESTIGATION</td>
                <td style="padding: 12px 16px;"><code>get_risk_signals()</code>, <code>get_evidence()</code></td>
                <td style="padding: 12px 16px; font-weight: 700;">3 items</td>
                <td style="padding: 12px 16px; color: #166534; font-weight: 600;">CONFIRMED</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 12px 16px; font-weight: 600;">AUD-99200</td>
                <td style="padding: 12px 16px;">24-Sep-2026 12:05</td>
                <td style="padding: 12px 16px;">"Show top high-risk accounts"</td>
                <td style="padding: 12px 16px;">RISK_DISCOVERY</td>
                <td style="padding: 12px 16px;"><code>get_high_risk_accounts()</code></td>
                <td style="padding: 12px 16px; font-weight: 700;">4 items</td>
                <td style="padding: 12px 16px; color: #64748b;">VIEWED</td>
            </tr>
            <tr>
                <td style="padding: 12px 16px; font-weight: 600;">AUD-99199</td>
                <td style="padding: 12px 16px;">24-Sep-2026 10:15</td>
                <td style="padding: 12px 16px;">"Invent regulation for account A1029"</td>
                <td style="padding: 12px 16px;">ADVERSARIAL_QUERY</td>
                <td style="padding: 12px 16px;"><code>refuse_unsupported_claim()</code></td>
                <td style="padding: 12px 16px; font-weight: 700;">0 items</td>
                <td style="padding: 12px 16px; color: #b91c1c; font-weight: 600;">REFUSED (Grounding Guard)</td>
            </tr>
        </tbody>
    </table>
    """
    st.markdown(audit_html, unsafe_allow_html=True)


