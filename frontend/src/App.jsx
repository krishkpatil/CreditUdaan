import React from "react";
import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import UploadPage from "./pages/UploadPage";
import ScorePage from "./pages/ScorePage";
import PricingPage from "./pages/PricingPage";
import Navbar from "./components/Navbar";

/**
 * App.jsx
 *
 * Main entry for ScoreLift React app.
 *
 * Backend integration notes:
 * - The UploadPage should POST the PDF to the Flask backend at /upload (see UploadPage.jsx for fetch example).
 * - After successful upload, navigate to /score and fetch analysis from /api/analysis (see ScorePage.jsx for fetch example).
 * - All fetch requests to backend must use credentials: 'include' for session support.
 * - Update API URLs if backend is hosted elsewhere (e.g., use process.env.REACT_APP_API_URL).
 */
function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navbar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/score" element={<ScorePage />} />
        <Route path="/pricing" element={<PricingPage />} />
      </Routes>
    </div>
  );
}

export default App;
