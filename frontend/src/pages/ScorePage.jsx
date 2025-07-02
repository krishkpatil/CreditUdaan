import React, { useEffect, useState } from "react";
import ScoreProgressBar from "../components/ScoreProgressBar";

/**
 * ScorePage.jsx
 *
 * Fetches credit analysis from Flask backend at /api/analysis.
 * Shows loading, error, and analysis (score, advice, etc.).
 */
const ScorePage = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    setLoading(true);
    try {
      const stored = localStorage.getItem('credit_analysis');
      if (!stored) {
        setError('No analysis found. Please upload your report.');
        setLoading(false);
        return;
      }
      const data = JSON.parse(stored);
      setAnalysis(data);
      setLoading(false);
    } catch (e) {
      setError('Failed to load analysis.');
      setLoading(false);
    }
  }, []);

  if (loading) {
    return <main className="flex flex-col items-center justify-center min-h-[70vh] py-12"><div className="text-xl">Loading analysis...</div></main>;
  }
  if (error) {
    return <main className="flex flex-col items-center justify-center min-h-[70vh] py-12"><div className="text-xl text-red-600">{error}</div></main>;
  }
  if (!analysis || !analysis.openai_analysis) {
    return null;
  }

  const { model_score, extracted_features, openai_analysis } = analysis;
  const {
    credit_score,
    credit_utilization,
    payment_history,
    avg_account_age,
    account_types,
    negative_items,
    detailed_analysis,
    improvement_advice,
    action_steps,
    negative_item_plans,
    roadmap_90_days,
    approval_advice,
    faq
  } = openai_analysis;

  return (
    <main className="flex flex-col items-center justify-center min-h-[70vh] py-12 bg-gradient-to-br from-blue-50 to-white">
      <div className="bg-white shadow-xl rounded-xl p-8 w-full max-w-3xl">
        <h2 className="text-3xl font-bold mb-2 text-blue-900 flex items-center gap-2">
          <span role="img" aria-label="score">📈</span> Your AI Credit Report
        </h2>
        <div className="flex flex-col md:flex-row gap-6 mt-6">
          <div className="flex-1 flex flex-col items-center">
            <span className="text-lg text-gray-500">Model Score</span>
            <div className="text-5xl font-extrabold text-blue-700 mb-2">{model_score}</div>
            <span className="text-lg text-gray-500">OpenAI Score</span>
            <div className="text-4xl font-bold text-green-700">{credit_score}</div>
            <div className="mt-2 text-sm text-gray-400">Credit Utilization: <span className="font-semibold">{credit_utilization}%</span></div>
            <div className="text-sm text-gray-400">Avg. Account Age: <span className="font-semibold">{avg_account_age} yrs</span></div>
            <div className="text-sm text-gray-400">Accounts: {account_types && Object.entries(account_types).map(([k,v]) => (<span key={k}>{k}: {v} </span>))}</div>
            <div className="text-sm text-gray-400">Missed Payments: <span className="font-semibold">{payment_history?.late}</span></div>
          </div>
          <div className="flex-1">
            <h3 className="text-xl font-semibold text-gray-800 mb-2 flex items-center gap-2"><span role="img" aria-label="summary">📝</span> Executive Summary</h3>
            <p className="text-gray-700 mb-4 whitespace-pre-line">{detailed_analysis}</p>
            <h4 className="text-lg font-semibold text-blue-700 mt-6 mb-2 flex items-center gap-2"><span role="img" aria-label="steps">✅</span> Actionable Steps</h4>
            <ul className="list-disc list-inside text-gray-700">
              {action_steps && action_steps.map((step, idx) => (
                <li key={idx}>{step}</li>
              ))}
            </ul>
            <h4 className="text-lg font-semibold text-blue-700 mt-6 mb-2 flex items-center gap-2"><span role="img" aria-label="advice">💡</span> Improvement Advice</h4>
            <p className="text-gray-700 mb-4 whitespace-pre-line">{improvement_advice}</p>
            <h4 className="text-lg font-semibold text-blue-700 mt-6 mb-2 flex items-center gap-2"><span role="img" aria-label="roadmap">🗺️</span> 90-Day Roadmap</h4>
            <ul className="list-decimal list-inside text-gray-700">
              {roadmap_90_days && roadmap_90_days.map((step, idx) => (
                <li key={idx}>{step}</li>
              ))}
            </ul>
            <h4 className="text-lg font-semibold text-blue-700 mt-6 mb-2 flex items-center gap-2"><span role="img" aria-label="approval">🏦</span> Approval Advice</h4>
            <p className="text-gray-700 mb-4 whitespace-pre-line">{approval_advice}</p>
            <h4 className="text-lg font-semibold text-blue-700 mt-6 mb-2 flex items-center gap-2"><span role="img" aria-label="faq">❓</span> Credit Myths & FAQs</h4>
            <ul className="list-disc list-inside text-gray-700">
              {faq && faq.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
            {negative_items > 0 && (
              <>
                <h4 className="text-lg font-semibold text-red-700 mt-6 mb-2 flex items-center gap-2"><span role="img" aria-label="risk">⚠️</span> Negative Items & Plans</h4>
                <ul className="list-disc list-inside text-gray-700">
                  {negative_item_plans && negative_item_plans.map((plan, idx) => (
                    <li key={idx}>{plan}</li>
                  ))}
                </ul>
              </>
            )}
            <h4 className="text-lg font-semibold text-blue-700 mt-6 mb-2 flex items-center gap-2"><span role="img" aria-label="raw">📄</span> Extracted Features</h4>
            <pre className="bg-gray-100 rounded p-2 text-xs text-gray-600 overflow-x-auto">{JSON.stringify(extracted_features, null, 2)}</pre>
          </div>
        </div>
      </div>
    </main>
  );
};

export default ScorePage;
