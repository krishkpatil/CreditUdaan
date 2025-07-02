import React from "react";

/**
 * Pricing page with 3-tier pricing table.
 * All plans are free for now; "Try for Free" CTA instead of payment.
 */
const plans = [
  {
    name: "Basic",
    price: "Free",
    features: [
      "Upload 1 CIBIL report",
      "Simulated credit score",
      "Basic recommendations",
      "Email support",
    ],
    recommended: false,
  },
  {
    name: "Pro",
    price: "Free",
    features: [
      "Upload up to 3 reports",
      "Detailed analysis",
      "Personalized tips",
      "Priority email support",
    ],
    recommended: true,
  },
  {
    name: "Premium",
    price: "Free",
    features: [
      "Unlimited uploads",
      "Advanced analytics",
      "1-on-1 expert call",
      "Early access to features",
    ],
    recommended: false,
  },
];

const PricingPage = () => (
  <main className="py-16 bg-gray-50 min-h-[80vh]">
    <h2 className="text-4xl font-extrabold text-center text-gray-900 mb-12">Pricing Plans</h2>
    <div className="flex flex-col md:flex-row gap-8 justify-center items-stretch max-w-5xl mx-auto px-4">
      {plans.map((plan, idx) => (
        <div
          key={plan.name}
          className={`flex-1 bg-white rounded-2xl shadow-lg border-2 transition hover:scale-105 duration-200 ${
            plan.recommended ? "border-blue-600 shadow-blue-100 scale-105" : "border-gray-200"
          }`}
        >
          <div className="p-8 flex flex-col items-center">
            <h3 className={`text-2xl font-bold mb-2 ${plan.recommended ? "text-blue-600" : "text-gray-900"}`}>{plan.name}</h3>
            <div className="text-3xl font-extrabold mb-4">{plan.price}</div>
            <ul className="mb-8 space-y-2 text-gray-700">
              {plan.features.map((f, i) => (
                <li key={i} className="flex items-center">
                  <span className="inline-block w-2 h-2 rounded-full bg-blue-400 mr-2"></span> {f}
                </li>
              ))}
            </ul>
            <button
              className={`w-full py-3 rounded-lg font-semibold text-lg shadow transition-colors duration-150 ${
                plan.recommended
                  ? "bg-blue-600 text-white hover:bg-blue-700"
                  : "bg-blue-50 text-blue-700 hover:bg-blue-100"
              }`}
            >
              Try for Free
            </button>
          </div>
        </div>
      ))}
    </div>
  </main>
);

export default PricingPage;
