#!/usr/bin/env python3
"""
generate_synthetic_data.py

Generates a synthetic dataset for credit score prediction, simulating features from credit reports and external financial data.
- Features include: credit utilization %, open accounts, missed payments, monthly rent, subscriptions, race, and credit score (target).
- Race is randomly assigned for fairness analysis.
- Credit score is correlated with features, but not with race (unless desired for fairness testing).
- Output: synthetic_credit_data.csv

Usage:
    python generate_synthetic_data.py --n_samples 10000 --output synthetic_credit_data.csv

Requirements:
    - Python 3.x
    - numpy, pandas

Reproducibility ensured via random seed.
"""
import numpy as np
import pandas as pd
import argparse

# Set random seed for reproducibility
def set_seed(seed=42):
    np.random.seed(seed)

# Generate synthetic data
def generate_data(n_samples=10000, seed=42):
    set_seed(seed)
    data = {}
    # Credit utilization: 0-100% (realistic: 5-80%)
    data['credit_utilization'] = np.clip(np.random.normal(35, 15, n_samples), 5, 95)
    # Number of open accounts: 1-15 (skewed towards 3-8)
    data['open_accounts'] = np.clip(np.random.poisson(5, n_samples), 1, 15)
    # Missed payments in last 2 years: 0-6 (most have 0-2)
    data['missed_payments'] = np.clip(np.random.poisson(0.7, n_samples), 0, 6)
    # Monthly rent (INR): 5000-75000 (log-normal distribution)
    data['monthly_rent'] = np.clip(np.random.lognormal(mean=9, sigma=0.5, size=n_samples), 5000, 75000)
    # Number of active subscriptions: 0-7 (most have 1-3)
    data['active_subscriptions'] = np.clip(np.random.poisson(2, n_samples), 0, 7)
    # Race: categorical (simulate 3 groups: 'A', 'B', 'C')
    data['race'] = np.random.choice(['A', 'B', 'C'], size=n_samples)

    # Target credit score (300-900), correlated with features
    # Higher utilization, more missed payments, more subscriptions lower score
    # More open accounts (up to a point) and higher rent (proxy for income) increase score
    base_score = 700
    score = (
        base_score
        - 2.2 * data['credit_utilization']
        - 25 * data['missed_payments']
        - 8 * data['active_subscriptions']
        + 7 * data['open_accounts']
        + 0.0006 * data['monthly_rent']
        + np.random.normal(0, 25, n_samples)  # noise
    )
    # Clip to 300-900
    data['credit_score'] = np.clip(score, 300, 900)

    # Return as DataFrame
    df = pd.DataFrame(data)
    return df

def main():
    parser = argparse.ArgumentParser(description='Generate synthetic credit data for model training')
    parser.add_argument('--n_samples', type=int, default=10000, help='Number of samples to generate')
    parser.add_argument('--output', type=str, default='synthetic_credit_data.csv', help='Output CSV file path')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')
    args = parser.parse_args()

    df = generate_data(n_samples=args.n_samples, seed=args.seed)
    df.to_csv(args.output, index=False)
    print(f"Synthetic dataset saved to {args.output} with {args.n_samples} samples.")
    print(df.head())

if __name__ == '__main__':
    main()
