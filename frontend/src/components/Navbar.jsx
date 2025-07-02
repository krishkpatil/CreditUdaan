import React from "react";
import { Link, useLocation } from "react-router-dom";

/**
 * Responsive navigation bar for ScoreLift.
 * Uses TailwindCSS for styling.
 */
const Navbar = () => {
  const location = useLocation();
  const navLinks = [
    { name: "Home", path: "/" },
    { name: "Upload", path: "/upload" },
    { name: "Live Score", path: "/score" },
    { name: "Pricing", path: "/pricing" },
  ];
  return (
    <nav className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-blue-600 tracking-tight">
          ScoreLift
        </Link>
        <div className="space-x-4">
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className={`text-gray-700 hover:text-blue-600 px-2 py-1 rounded transition-colors duration-150 ${
                location.pathname === link.path ? "bg-blue-100" : ""
              }`}
            >
              {link.name}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
