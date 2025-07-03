#!/usr/bin/env python3
"""
model.py

PyTorch neural network for predicting credit score (300-900) from credit and external financial features.
- Accepts features: credit utilization, open accounts, missed payments, monthly rent, subscriptions, race.
- Outputs a credit score in [300, 900].
- Trains on synthetic data (see generate_synthetic_data.py).
- Optimizes for RMSE and demographic fairness (minimizing correlation with race).

Usage:
    python model.py --data synthetic_credit_data.csv --epochs 20 --batch_size 128

Requirements:
    - Python 3.x
    - torch, numpy, pandas, scikit-learn

Reproducibility ensured via random seed.
"""
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import argparse

# Set random seed for reproducibility
def set_seed(seed=42):
    torch.manual_seed(seed)
    np.random.seed(seed)

# Neural network model definition
class CreditScoreNet(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        # Match original architecture: 3 linear layers, no dropout
        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),  # Output: unscaled
        )
        # Output will be scaled to [0, 1] and then mapped to [300, 900]
        self.output_min = 300
        self.output_max = 900

    def forward(self, x):
        raw = self.net(x)
        scaled = torch.sigmoid(raw)  # [0, 1]
        return scaled * (self.output_max - self.output_min) + self.output_min

# NOTE: Update input_dim to match the number of features used in generate_synthetic_data.py and credit_analyzer.py.
# Features: credit_utilization, open_accounts, closed_accounts, account_age_years, credit_card_count, loan_count, recent_inquiries, missed_payments, monthly_rent, active_subscriptions (exclude 'race' for prediction)
# Retrain your model after updating the feature set, then upload the new .pt file to Hugging Face.

# Custom loss: RMSE + fairness penalty (correlation with race)
def fairness_loss(preds, targets, race_tensor, lambda_fair=0.1):
    # RMSE
    mse = nn.MSELoss()(preds, targets)
    rmse = torch.sqrt(mse)
    # Fairness: minimize absolute Pearson correlation between preds and race
    race_mean = race_tensor.mean()
    pred_mean = preds.mean()
    race_centered = race_tensor - race_mean
    pred_centered = preds - pred_mean
    numerator = (race_centered * pred_centered).mean()
    denominator = torch.sqrt((race_centered ** 2).mean() * (pred_centered ** 2).mean() + 1e-8)
    corr = numerator / (denominator + 1e-8)
    fair_penalty = torch.abs(corr)
    # Total loss
    return rmse + lambda_fair * fair_penalty, rmse.item(), fair_penalty.item()

def main():
    parser = argparse.ArgumentParser(description='Train credit score model with fairness constraint')
    parser.add_argument('--data', type=str, required=True, help='Path to synthetic data CSV')
    parser.add_argument('--epochs', type=int, default=20, help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=128, help='Batch size')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    args = parser.parse_args()
    set_seed(args.seed)

    # Load data
    df = pd.read_csv(args.data)
    features = ['credit_utilization', 'open_accounts', 'missed_payments', 'monthly_rent', 'active_subscriptions']
    X = df[features].values
    y = df['credit_score'].values.reshape(-1, 1)
    # Encode race as integer for fairness penalty
    le = LabelEncoder()
    race = le.fit_transform(df['race'])  # e.g., 0, 1, 2
    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    # Train/test split
    X_train, X_test, y_train, y_test, race_train, race_test = train_test_split(
        X_scaled, y, race, test_size=0.2, random_state=args.seed)

    # Convert to torch tensors
    X_train = torch.tensor(X_train, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.float32)
    race_train = torch.tensor(race_train, dtype=torch.float32)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_test = torch.tensor(y_test, dtype=torch.float32)
    race_test = torch.tensor(race_test, dtype=torch.float32)

    # Model
    model = CreditScoreNet(input_dim=X_train.shape[1])
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    # Training loop
    print("Starting training...")
    for epoch in range(args.epochs):
        model.train()
        permutation = torch.randperm(X_train.size()[0])
        epoch_loss, epoch_rmse, epoch_fair = 0, 0, 0
        for i in range(0, X_train.size()[0], args.batch_size):
            idx = permutation[i:i+args.batch_size]
            batch_x, batch_y, batch_race = X_train[idx], y_train[idx], race_train[idx]
            optimizer.zero_grad()
            preds = model(batch_x)
            loss, rmse, fair = fairness_loss(preds, batch_y, batch_race)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * batch_x.size(0)
            epoch_rmse += rmse * batch_x.size(0)
            epoch_fair += fair * batch_x.size(0)
        n_train = X_train.size()[0]
        print(f"Epoch {epoch+1}/{args.epochs} | Loss: {epoch_loss/n_train:.4f} | RMSE: {epoch_rmse/n_train:.4f} | FairPenalty: {epoch_fair/n_train:.4f}")

    # Evaluation
    model.eval()
    with torch.no_grad():
        preds = model(X_test)
        test_rmse = torch.sqrt(nn.MSELoss()(preds, y_test)).item()
        # Fairness: correlation with race
        race_mean = race_test.mean()
        pred_mean = preds.mean()
        race_centered = race_test - race_mean
        pred_centered = preds - pred_mean
        numerator = (race_centered * pred_centered).mean()
        denominator = torch.sqrt((race_centered ** 2).mean() * (pred_centered ** 2).mean() + 1e-8)
        test_corr = numerator / (denominator + 1e-8)
        print(f"Test RMSE: {test_rmse:.4f}")
        print(f"Test fairness (|corr(pred, race)|): {abs(test_corr.item()):.4f}")

    # Save model and scaler
    torch.save(model.state_dict(), "credit_score_model.pt")
    import pickle
    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)


if __name__ == '__main__':
    main()
