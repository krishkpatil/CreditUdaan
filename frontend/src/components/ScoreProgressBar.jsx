import React from "react";

/**
 * Progress bar for displaying credit score visually.
 * Props:
 *   - score: number (300-900)
 */
const ScoreProgressBar = ({ score }) => {
  // Map score 300-900 to 0-100%
  const percent = ((score - 300) / 600) * 100;
  return (
    <div className="w-full max-w-xl mx-auto my-8">
      <div className="flex justify-between mb-1">
        <span className="text-sm font-medium text-blue-700">Credit Score</span>
        <span className="text-sm font-medium text-blue-700">{score}</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-6">
        <div
          className="bg-blue-600 h-6 rounded-full transition-all duration-700"
          style={{ width: `${percent}%` }}
        ></div>
      </div>
    </div>
  );
};

export default ScoreProgressBar;
