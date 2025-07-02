import os
import torch
import numpy as np
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import PyPDF2
import re
import json
from dotenv import load_dotenv
import os

# Define the model class (must match model.py)
import torch.nn as nn
class CreditScoreNet(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )
        self.output_min = 300
        self.output_max = 900

    def forward(self, x):
        raw = self.net(x)
        scaled = torch.sigmoid(raw)
        return scaled * (self.output_max - self.output_min) + self.output_min

# Model feature order
MODEL_FEATURES = [
    "credit_utilization",
    "open_accounts",
    "missed_payments",
    "monthly_rent",
    "active_subscriptions"
]

# Load scaler
scaler = None
if os.path.exists("scaler.pkl"):
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

# Load model
model_path = "credit_score_model.pt"
input_dim = 5
model = CreditScoreNet(input_dim)
model.load_state_dict(torch.load(model_path, map_location="cpu"))
model.eval()

# Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# --- PDF and Feature Extraction Utilities (from credit_analyzer.py) ---
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_credit_info(text):
    info = {}
    util_match = re.search(r"Credit Utilization(?:\s*):(?:\s*)([\d,.]+)%", text, re.IGNORECASE)
    if util_match:
        info['credit_utilization_percent'] = float(util_match.group(1).replace(',', ''))
    else:
        util_match = re.search(r"Utilization(?:\s*):(?:\s*)([\d,.]+)%", text, re.IGNORECASE)
        if util_match:
            info['credit_utilization_percent'] = float(util_match.group(1).replace(',', ''))
        else:
            info['credit_utilization_percent'] = None
    open_acc_match = re.search(r"Open Accounts(?:\s*):(?:\s*)(\d+)", text, re.IGNORECASE)
    if open_acc_match:
        info['number_of_open_accounts'] = int(open_acc_match.group(1))
    else:
        open_accs = re.findall(r"Status\s*:\s*Open", text, re.IGNORECASE)
        info['number_of_open_accounts'] = len(open_accs)
    missed = 0
    late_pay_match = re.search(r"Late Payment(?:s)?\s*:\s*(\d+)", text, re.IGNORECASE)
    if late_pay_match:
        missed = int(late_pay_match.group(1))
    info['missed_payments'] = missed
    return info

@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.json
    features = [data.get(f, 0) for f in MODEL_FEATURES]
    if scaler:
        features = scaler.transform([features])[0]
    features = np.array(features, dtype=np.float32).reshape(1, -1)
    with torch.no_grad():
        x = torch.tensor(features, dtype=torch.float32)
        score = model(x).item()
    return jsonify({"predicted_score": round(score, 2)})

@app.route("/api/auto_analysis", methods=["POST"])
def api_auto_analysis():
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'No PDF uploaded.'}), 400
        pdf_file = request.files['pdf']
        temp_path = "temp_uploaded.pdf"
        pdf_file.save(temp_path)
        # Extract text and features
        text = extract_text_from_pdf(temp_path)
        info = extract_credit_info(text)
        # Prepare features for model
        features = [
            info.get('credit_utilization_percent') or 0,
            info.get('number_of_open_accounts') or 0,
            info.get('missed_payments') or 0,
            20000,  # Placeholder for monthly_rent
            2       # Placeholder for active_subscriptions
        ]
        if scaler:
            features = scaler.transform([features])[0]
        features = np.array(features, dtype=np.float32).reshape(1, -1)
        with torch.no_grad():
            x = torch.tensor(features, dtype=torch.float32)
            model_score = model(x).item()
        # OpenAI analysis using GPT-4o and JSON schema
        def analyze_credit_report(text):
            import json
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-2024-08-06",
                    messages=[
                        {"role": "system", "content": (
                            "You are a world-class financial analyst specializing in credit reports. "
                            "Analyze the given credit report and provide a detailed summary. "
                            "In your output, ensure the following: "
                            "1. Give a concise executive summary of the person's credit health and risks. "
                            "2. List at least five highly actionable, personalized steps to improve their credit, referencing specific numbers from the report. "
                            "3. For each negative item or risk, provide a clear explanation and a step-by-step action plan to resolve it (with links to reputable resources if possible). "
                            "4. Provide a 90-day improvement roadmap with monthly milestones. "
                            "5. Offer tailored advice for maximizing approval odds for loans, credit cards, or mortgages, based on their profile. "
                            "6. Include a myth-busting FAQ section about credit scores and reports. "
                            "7. Make the advice practical, detailed, and worth at least $99—do not be generic. "
                            "8. Use clear, confident, and encouraging language."
                        )},
                        {"role": "user", "content": f"Analyze the following credit report:\n\n{text}"}
                    ],
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "credit_report_analysis",
                            "strict": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "credit_score": {"type": "integer"},
                                    "credit_utilization": {"type": "number"},
                                    "payment_history": {
                                        "type": "object",
                                        "properties": {
                                            "on_time": {"type": "integer"},
                                            "late": {"type": "integer"}
                                        },
                                        "required": ["on_time", "late"],
                                        "additionalProperties": False
                                    },
                                    "avg_account_age": {"type": "number"},
                                    "account_types": {
                                        "type": "object",
                                        "additionalProperties": {"type": "integer"}
                                    },
                                    "negative_items": {"type": "integer"},
                                    "detailed_analysis": {"type": "string"},
                                    "improvement_advice": {"type": "string"},
                                    "action_steps": {"type": "array", "items": {"type": "string"}},
                                    "negative_item_plans": {"type": "array", "items": {"type": "string"}},
                                    "roadmap_90_days": {"type": "array", "items": {"type": "string"}},
                                    "approval_advice": {"type": "string"},
                                    "faq": {"type": "array", "items": {"type": "string"}}
                                },
                                "required": [
                                    "credit_score", "credit_utilization", "payment_history", "avg_account_age", "negative_items", "detailed_analysis", "improvement_advice", "action_steps", "negative_item_plans", "roadmap_90_days", "approval_advice", "faq"
                                ],
                                "additionalProperties": False
                            }
                        }
                    }
                )
                return json.loads(response.choices[0].message.content)
            except Exception as oe:
                return {"openai_error": str(oe)}

        # Use extracted PDF text for analysis
        openai_result = analyze_credit_report(text)
        # Clean up temp file
        os.remove(temp_path)
        return jsonify({
            "model_score": round(model_score, 2),
            "extracted_features": info,
            "openai_analysis": openai_result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
