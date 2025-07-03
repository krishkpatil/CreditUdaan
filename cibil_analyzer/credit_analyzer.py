#!/usr/bin/env python3
"""
credit_analyzer.py

A script for credit analysis in India:
- Accepts a CIBIL PDF report and optional CSVs with financial data (e.g., rent payments, subscriptions).
- Extracts key credit info: credit utilization, open accounts, payment history, subscriptions, etc.
- Consolidates all extracted info into a summary JSON/dict.

Requirements:
- Python 3.x
- PyPDF2 (install via: pip install PyPDF2)
- Only standard libraries and PyPDF2 are used.

Usage:
    python credit_analyzer.py --pdf <CIBIL_REPORT.pdf> [--csv <file1.csv> ...]
"""

import argparse
import json
import os
import re
import sys
from typing import List, Dict, Any

import PyPDF2
import csv

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts all text from a PDF file using PyPDF2.
    """
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_credit_info(text: str) -> Dict[str, Any]:
    """
    Enhanced extraction: credit utilization, open/closed accounts, account age, missed/late payments, credit card count, loan count, recent inquiries, DPD.
    """
    info = {}
    # Credit Utilization
    util_match = re.search(r"Credit Utilization(?:\s*):(?:\s*)([\d,.]+)%", text, re.IGNORECASE)
    if util_match:
        info['credit_utilization_percent'] = float(util_match.group(1).replace(',', ''))
    else:
        util_match = re.search(r"Utilization(?:\s*):(?:\s*)([\d,.]+)%", text, re.IGNORECASE)
        info['credit_utilization_percent'] = float(util_match.group(1).replace(',', '')) if util_match else None
    # Open Accounts
    open_acc_match = re.search(r"Open Accounts(?:\s*):(?:\s*)(\d+)", text, re.IGNORECASE)
    if open_acc_match:
        info['number_of_open_accounts'] = int(open_acc_match.group(1))
    else:
        open_accs = re.findall(r"Status\s*:\s*Open", text, re.IGNORECASE)
        info['number_of_open_accounts'] = len(open_accs)
    # Closed Accounts
    closed_accs = re.findall(r"Status\s*:\s*Closed", text, re.IGNORECASE)
    info['number_of_closed_accounts'] = len(closed_accs)
    # Account Age (years, fallback to months)
    age_match = re.search(r"Account Age(?:\s*):(?:\s*)([\d,.]+)\s*yrs", text, re.IGNORECASE)
    if age_match:
        info['account_age_years'] = float(age_match.group(1).replace(',', ''))
    else:
        age_match = re.search(r"Account Age(?:\s*):(?:\s*)([\d,.]+)\s*months", text, re.IGNORECASE)
        info['account_age_years'] = float(age_match.group(1).replace(',', ''))/12 if age_match else None
    # Credit Card Count
    cc_match = re.search(r"Credit Card(?:\s*):(?:\s*)(\d+)", text, re.IGNORECASE)
    info['credit_card_count'] = int(cc_match.group(1)) if cc_match else len(re.findall(r"Credit Card", text, re.IGNORECASE))
    # Loan Count
    loan_match = re.search(r"Loan(?:\s*):(?:\s*)(\d+)", text, re.IGNORECASE)
    info['loan_count'] = int(loan_match.group(1)) if loan_match else len(re.findall(r"Loan", text, re.IGNORECASE))
    # Recent Inquiries
    inquiries = re.findall(r"Enquiry Date", text, re.IGNORECASE)
    info['recent_inquiries'] = len(inquiries)
    # Payment History (DPD, late/missed)
    payment_history = []
    dpd_lines = re.findall(r"DPD\s*:\s*([0-9\s]+)", text)
    for dpd in dpd_lines:
        months = [int(x) for x in dpd.strip().split() if x.isdigit()]
        payment_history.append({'dpd': months})
    late_pay_match = re.search(r"Late Payment(?:s)?\s*:\s*(\d+)", text, re.IGNORECASE)
    if late_pay_match:
        payment_history.append({'late_payments': int(late_pay_match.group(1))})
    missed_pay_match = re.search(r"Missed Payment(?:s)?\s*:\s*(\d+)", text, re.IGNORECASE)
    if missed_pay_match:
        payment_history.append({'missed_payments': int(missed_pay_match.group(1))})
    info['payment_history'] = payment_history if payment_history else None
    return info

# TEST FUNCTION: For local validation
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1].endswith('.pdf'):
        from PyPDF2 import PdfReader
        pdf_path = sys.argv[1]
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        features = extract_credit_info(text)
        print("Extracted features:\n", features)


def extract_subscriptions(text: str) -> List[str]:
    """
    Extracts subscription services mentioned in the text (e.g., Spotify, Netflix, Amazon Prime).
    """
    subscriptions = []
    known_services = [
        'Spotify', 'Netflix', 'Amazon Prime', 'Hotstar', 'SonyLIV', 'Apple Music',
        'YouTube Premium', 'Gaana', 'JioSaavn', 'ALTBalaji', 'Zee5', 'Voot', 'Prime Video',
        'Disney+', 'Airtel Xstream', 'Sun NXT'
    ]
    for service in known_services:
        if re.search(service, text, re.IGNORECASE):
            subscriptions.append(service)
    return subscriptions

def parse_csv_financial_data(csv_paths: List[str]) -> Dict[str, Any]:
    """
    Parses CSVs for rent payments, recurring obligations, and subscriptions.
    Assumes CSVs have headers and columns like 'Description', 'Amount', 'Date'.
    """
    rent_payments = []
    recurring_obligations = []
    subscriptions = set()
    rent_keywords = ['rent', 'house rent', 'flat rent', 'apartment rent']
    subscription_keywords = [
        'Spotify', 'Netflix', 'Amazon Prime', 'Hotstar', 'SonyLIV', 'Apple Music',
        'YouTube Premium', 'Gaana', 'JioSaavn', 'ALTBalaji', 'Zee5', 'Voot', 'Prime Video',
        'Disney+', 'Airtel Xstream', 'Sun NXT'
    ]
    recurring_keywords = ['EMI', 'insurance', 'loan', 'credit card', 'sip', 'mutual fund', 'subscription']

    for csv_path in csv_paths:
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                desc = row.get('Description', '').lower()
                amt = row.get('Amount', '')
                date = row.get('Date', '')
                # Rent payments
                if any(k in desc for k in rent_keywords):
                    rent_payments.append({'description': desc, 'amount': amt, 'date': date})
                # Subscriptions
                for sub in subscription_keywords:
                    if sub.lower() in desc:
                        subscriptions.add(sub)
                # Recurring obligations
                if any(k in desc for k in recurring_keywords):
                    recurring_obligations.append({'description': desc, 'amount': amt, 'date': date})

    return {
        'rent_payments': rent_payments,
        'recurring_obligations': recurring_obligations,
        'subscriptions': list(subscriptions)
    }

def consolidate_summary(pdf_info: Dict[str, Any], csv_info: Dict[str, Any], pdf_subs: List[str]) -> Dict[str, Any]:
    """
    Combines all extracted information into a summary dictionary.
    """
    summary = {}
    summary.update(pdf_info)
    summary['rent_payments'] = csv_info.get('rent_payments', [])
    summary['recurring_obligations'] = csv_info.get('recurring_obligations', [])
    # Combine subscriptions from PDF and CSVs, remove duplicates
    all_subs = set(pdf_subs) | set(csv_info.get('subscriptions', []))
    summary['active_subscriptions'] = list(all_subs)
    return summary

def main():
    parser = argparse.ArgumentParser(description='Credit Analyzer for Indian Financial Documents')
    parser.add_argument('--pdf', required=True, help='Path to CIBIL report PDF')
    parser.add_argument('--csv', nargs='*', help='Path(s) to external CSV file(s)')
    parser.add_argument('--output', default='summary.json', help='Output JSON file (default: summary.json)')
    args = parser.parse_args()

    # Step 1: Extract text from PDF
    print(f"Extracting text from PDF: {args.pdf}")
    pdf_text = extract_text_from_pdf(args.pdf)

    # Step 2: Extract credit info from PDF
    print("Extracting credit information from CIBIL report...")
    pdf_info = extract_credit_info(pdf_text)

    # Step 3: Extract subscriptions from PDF
    print("Extracting subscription services from CIBIL report...")
    pdf_subs = extract_subscriptions(pdf_text)

    # Step 4: Parse CSVs (if any)
    csv_info = {'rent_payments': [], 'recurring_obligations': [], 'subscriptions': []}
    if args.csv:
        print(f"Parsing CSV files: {args.csv}")
        csv_info = parse_csv_financial_data(args.csv)

    # Step 5: Consolidate all info
    print("Consolidating extracted information...")
    summary = consolidate_summary(pdf_info, csv_info, pdf_subs)

    # Step 6: Output summary as JSON
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)
    print(f"Summary saved to {args.output}")
    print(json.dumps(summary, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    main()
