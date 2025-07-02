# 🚀 Credit Udaan

Credit Udaan is a modern, AI-powered credit analysis web application designed to help users in India understand, improve, and plan their credit journey. It allows users to upload their CIBIL report, analyze it with an AI backend, and receive actionable insights along with a simulated credit score. The app also provides easy subscription options via integrated payment gateways.

---

## 🛠 Technologies Used

- **PyTorch Neural Network:**  
  - Custom model trained on synthetic data to predict credit scores in the range of 300–900.
  - Includes fairness optimization to minimize bias in predictions.

- **Synthetic Data Generation:**  
  - Automatically creates realistic datasets simulating Indian credit features, rent payments, and subscriptions for model training and testing.

- **OpenAI GPT-4o Structured Outputs:**  
  - Used for analyzing parsed credit reports and generating step-by-step, personalized advice for users.

- **Flask API (Python):**  
  - Backend for handling PDF uploads, data processing, and communication with the AI models.

- **React + TailwindCSS Frontend:**  
  - Modern, responsive UI with pages for upload, live score display, and pricing.
  - Integrated with Stripe Checkout (future scope: Razorpay).

---

## 🌟 Features

- **Modern, mobile-responsive frontend** built with React and TailwindCSS.
- **Hero landing page** with engaging CTA and testimonials.
- **Secure PDF upload form** for users to submit their CIBIL credit report.
- **Live credit score display** after analysis.
- **Placeholder testimonials** to build trust and credibility.
- **React Router navigation** across landing, upload, score, and pricing pages.

---

## 🚧 Future Scope

We plan to add the following features to make Credit Udaan more robust, privacy-focused, and user-friendly:

- **🔒 Zero-Knowledge Proofs (zkProof):**
  - Integrate zkProof protocols to enable privacy-preserving credit analysis.
  - Allow users to prove their creditworthiness without revealing their full credit data.

- **💳 Razorpay Integration:**
  - Add **Razorpay** as an alternative payment gateway tailored for Indian customers.
  - Provide users with more localized, UPI-friendly, and bank transfer options.

- **📊 Dashboard & Reports:**
  - Offer users a personal dashboard to track progress over time.
  - Download detailed analysis reports in PDF format.

- **🔔 Notifications & Reminders:**
  - Send personalized notifications on payment due dates or actionable tips.

---

## ⚙️ Setup Instructions

Follow these steps to set up and run the Credit Udaan app locally:

1️⃣ **Clone the repository:**

```bash
git clone https://github.com/krishkpatil/creditudaan.git
cd creditudaan
```
2️⃣ Install Python dependencies:

Make sure you have Python 3.8+ installed, then run:

```bash

pip install -r requirements.txt
```
3️⃣ Start the Python backend:

```bash

python app.py
```
By default, this will start your backend server at http://localhost:5001

4️⃣ Install React frontend dependencies:

```bash

npm install
```
5️⃣ Run the React development server:

```bash

npm run dev
```
By default, this will start your frontend on http://localhost:3000.

6️⃣ Access the app:

Open your browser and go to http://localhost:3000 to start using Credit Udaan!

✅ That’s it! Your backend and frontend should now be running locally.
