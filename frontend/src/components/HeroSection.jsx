import React from "react";
import { Link } from "react-router-dom";
import heroImg from "../assets/hero-placeholder.svg";

/**
 * Hero section for the landing page.
 * Includes headline, subheading, CTA, and hero image.
 */
const HeroSection = () => {
  return (
    <section className="flex flex-col md:flex-row items-center justify-between py-12 md:py-20 max-w-6xl mx-auto px-4">
      <div className="flex-1 mb-10 md:mb-0">
        <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6 leading-tight">
          Unlock Your <span className="text-blue-600">Credit Potential</span> with ScoreLift
        </h1>
        <p className="text-lg md:text-xl text-gray-700 mb-8">
          Upload your CIBIL report, get a live credit score, and discover actionable insights for financial growth. Designed for India.
        </p>
        <Link
          to="/upload"
          className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold text-lg shadow hover:bg-blue-700 transition-colors"
        >
          Analyze My Credit Report
        </Link>
      </div>
      <div className="flex-1 flex justify-center md:justify-end">
        {/* Placeholder hero image */}
        <img
          src={heroImg}
          alt="ScoreLift Hero"
          className="w-80 h-80 object-contain drop-shadow-xl"
        />
      </div>
    </section>
  );
};

export default HeroSection;
