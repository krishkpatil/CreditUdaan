import React, { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

/**
 * UploadPage.jsx
 *
 * Handles PDF upload to Flask backend at /upload.
 * On success, navigates to /score for analysis fetch.
 */
const UploadPage = () => {
  const fileInputRef = useRef();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Upload PDF to backend
  const uploadPDF = (file) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('pdf', file);
    fetch('http://localhost:5001/api/auto_analysis', {
      method: 'POST',
      body: formData,
    })
      .then(res => res.json())
      .then(data => {
        setLoading(false);
        if (data.error) {
          setError(data.error);
        } else {
          localStorage.setItem('credit_analysis', JSON.stringify(data));
          navigate('/score');
        }
      })
      .catch(() => {
        setLoading(false);
        setError('Upload failed.');
      });
  };

  const handleFileChange = (e) => {
    setError("");
    const file = e.target.files[0];
    if (!file) return;
    if (file.type !== "application/pdf") {
      setError("Only PDF files are allowed.");
      fileInputRef.current.value = "";
      return;
    }
    uploadPDF(file);
  };

  return (
    <main className="flex flex-col items-center justify-center py-16 min-h-[70vh]">
      <div className="bg-white shadow-lg rounded-xl p-8 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">Upload Your CIBIL Report</h2>
        <form>
          <input
            ref={fileInputRef}
            type="file"
            accept="application/pdf"
            className="block w-full text-gray-700 border border-gray-300 rounded-lg py-2 px-3 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-400"
            onChange={handleFileChange}
            disabled={loading}
          />
          {error && <div className="text-red-500 mb-2">{error}</div>}
          <button
            type="button"
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold text-lg shadow hover:bg-blue-700 transition-colors disabled:opacity-50"
            onClick={() => fileInputRef.current && fileInputRef.current.click()}
            disabled={loading}
          >
            {loading ? "Uploading..." : "Submit PDF"}
          </button>
        </form>
        <p className="text-gray-500 text-xs mt-4">Your data is private and secure. Only .pdf files are accepted.</p>
      </div>
    </main>
  );
};

export default UploadPage;
