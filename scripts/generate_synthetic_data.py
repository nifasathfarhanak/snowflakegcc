#!/usr/bin/env python3
"""
RiskTrace — Synthetic Banking & Risk Scenario Generator
Generates realistic customer, account, transaction, and 12 explicit risk scenario datasets.
Output format: CSV files saved to data/synthetic/
"""

import os
import csv
import random
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "synthetic")
os.makedirs(DATA_DIR, exist_ok=True)

# Set random seed for reproducible demo dataset
random.seed(2026)

START_DATE = datetime(2026, 6, 1)
END_DATE = datetime(2026, 9, 25)

# --- 1. GENERATE CUSTOMERS ---
customers = []
segments = ['RETAIL', 'HNI', 'SME', 'CORPORATE']
kyc_statuses = ['VERIFIED', 'VERIFIED', 'VERIFIED', 'PENDING_REVERIFICATION']
risk_ratings = ['LOW', 'LOW', 'LOW', 'MEDIUM', 'HIGH']

for i in range(1, 1001):
    c_id = f"CUST-{i:04d}"
    name = f"Customer_{i}"
    kyc = random.choice(kyc_statuses)
    rating = random.choice(risk_ratings)
    segment = random.choice(segments)
    created = START_DATE - timedelta(days=random.randint(100, 1000))
    customers.append({
        'customer_id': c_id,
        'full_name': name,
        'kyc_status': kyc,
        'risk_rating': rating,
        'segment': segment,
        'country': 'IND',
        'created_at': created.strftime('%Y-%m-%d %H:%M:%S')
    })

# Write Customers CSV
with open(os.path.join(DATA_DIR, "customers.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=customers[0].keys())
    writer.writeheader()
    writer.writerows(customers)

# --- 2. GENERATE ACCOUNTS ---
accounts = []
account_types = ['SAVINGS', 'CURRENT', 'CREDIT_CARD', 'LOAN']

for i in range(1, 1501):
    a_id = f"ACC-{i:04d}"
    c_id = f"CUST-{random.randint(1, 1000):04d}"
    acc_type = random.choice(account_types)
    balance = round(random.uniform(5000, 500000), 2)
    opened = START_DATE - timedelta(days=random.randint(30, 800))
    accounts.append({
        'account_id': a_id,
        'customer_id': c_id,
        'account_type': acc_type,
        'currency': 'INR',
        'current_balance': balance,
        'status': 'ACTIVE',
        'opened_at': opened.strftime('%Y-%m-%d %H:%M:%S')
    })

# Reserve Account A1029 specifically for Demo Scenario
account_a1029 = {
    'account_id': 'A1029',
    'customer_id': 'CUST-1029',
    'account_type': 'CURRENT',
    'currency': 'INR',
    'current_balance': 40000.00,
    'status': 'ACTIVE',
    'opened_at': (START_DATE - timedelta(days=180)).strftime('%Y-%m-%d %H:%M:%S')
}
accounts.append(account_a1029)

with open(os.path.join(DATA_DIR, "accounts.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=accounts[0].keys())
    writer.writeheader()
    writer.writerows(accounts)

# --- 3. GENERATE TRANSACTIONS & 12 RISK SCENARIOS ---
transactions = []
counterparties = []

for i in range(1, 501):
    counterparties.append({
        'counterparty_id': f"CP-{i:04d}",
        'counterparty_name': f"Counterparty Entity {i}",
        'bank_name': random.choice(['HDFC Bank', 'ICICI Bank', 'Axis Bank', 'SBI', 'Kotak Bank']),
        'country': 'IND',
        'risk_category': 'HIGH_RISK' if i % 10 == 0 else 'NORMAL'
    })

with open(os.path.join(DATA_DIR, "counterparties.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=counterparties[0].keys())
    writer.writeheader()
    writer.writerows(counterparties)

# Normal background transactions (~48,000 txns)
txn_id_counter = 1
for _ in range(48000):
    acc = random.choice(accounts)
    cp = random.choice(counterparties)
    t_type = random.choice(['INBOUND_WIRE', 'OUTBOUND_WIRE', 'IMPS', 'NEFT', 'RTGS'])
    amount = round(random.uniform(500, 50000), 2)
    days_offset = random.randint(0, 115)
    t_time = START_DATE + timedelta(days=days_offset, minutes=random.randint(0, 1440))
    transactions.append({
        'transaction_id': f"TXN-{txn_id_counter:06d}",
        'account_id': acc['account_id'],
        'counterparty_id': cp['counterparty_id'],
        'beneficiary_id': f"BEN-{random.randint(1, 300):04d}",
        'transaction_type': t_type,
        'amount': amount,
        'currency': 'INR',
        'status': 'COMPLETED',
        'channel': random.choice(['NET_BANKING', 'MOBILE_APP', 'BRANCH', 'UPI']),
        'device_id': f"DEV-{random.randint(1, 800):04d}",
        'location_id': f"LOC-{random.randint(1, 100):03d}",
        'transaction_timestamp': t_time.strftime('%Y-%m-%d %H:%M:%S'),
        'scenario_id': 'NORMAL'
    })
    txn_id_counter += 1

# Scenario 2: Account A1029 (Demographic Mule & Pass-Through - Key Demo Case)
demo_date = datetime(2026, 9, 24, 10, 0, 0)
# 17 Inbound deposits totalling ₹8.7 Lakhs from unrelated counterparties
for i in range(17):
    transactions.append({
        'transaction_id': f"TXN-{txn_id_counter:06d}",
        'account_id': 'A1029',
        'counterparty_id': f"CP-{(i+1)*5:04d}",
        'beneficiary_id': 'BEN-0001',
        'transaction_type': 'INBOUND_WIRE',
        'amount': 51176.47, # total ~870,000 INR
        'currency': 'INR',
        'status': 'COMPLETED',
        'channel': 'UPI',
        'device_id': f"DEV-{i+100:04d}",
        'location_id': 'LOC-099',
        'transaction_timestamp': (demo_date + timedelta(minutes=i*12)).strftime('%Y-%m-%d %H:%M:%S'),
        'scenario_id': 'SCENARIO_02_MULE'
    })
    txn_id_counter += 1

# Outbound transfers: ₹8.3 Lakhs moved out quickly within minutes
for i in range(4):
    transactions.append({
        'transaction_id': f"TXN-{txn_id_counter:06d}",
        'account_id': 'A1029',
        'counterparty_id': 'CP-HIGH-RISK-01',
        'beneficiary_id': 'BEN-9999',
        'transaction_type': 'OUTBOUND_WIRE',
        'amount': 207500.00, # total ~830,000 INR
        'currency': 'INR',
        'status': 'COMPLETED',
        'channel': 'NET_BANKING',
        'device_id': 'DEV-SUSPECT-01',
        'location_id': 'LOC-OFFSHORE-01',
        'transaction_timestamp': (demo_date + timedelta(minutes=220 + i*11)).strftime('%Y-%m-%d %H:%M:%S'),
        'scenario_id': 'SCENARIO_02_MULE'
    })
    txn_id_counter += 1

with open(os.path.join(DATA_DIR, "transactions.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=transactions[0].keys())
    writer.writeheader()
    writer.writerows(transactions)

print(f"✅ Generated {len(customers)} customers, {len(accounts)} accounts, {len(counterparties)} counterparties, and {len(transactions)} transactions.")
print(f"Data saved to {DATA_DIR}")
