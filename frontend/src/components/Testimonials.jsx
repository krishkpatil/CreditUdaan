import React from "react";
import avatar1 from "../assets/avatar1.png";
import avatar2 from "../assets/avatar2.png";
import avatar3 from "../assets/avatar3.png";

/**
 * Fake testimonials section for the landing page.
 * Uses placeholder avatars and names.
 */
const testimonials = [
  {
    name: "Amit S.",
    avatar: avatar1,
    text: "ScoreLift helped me understand my credit score and improve it in just a month! Highly recommended.",
  },
  {
    name: "Priya R.",
    avatar: avatar2,
    text: "The live score feature is amazing. The insights were spot on for Indian users!",
  },
  {
    name: "Rahul D.",
    avatar: avatar3,
    text: "Loved the simple upload process and clear recommendations. Great for anyone with a CIBIL report.",
  },
];

const Testimonials = () => (
  <section className="bg-white py-12">
    <div className="max-w-4xl mx-auto px-4">
      <h2 className="text-3xl font-bold text-center text-gray-900 mb-8">What Our Users Say</h2>
      <div className="flex flex-col md:flex-row gap-8 justify-center items-stretch">
        {testimonials.map((t, idx) => (
          <div
            key={idx}
            className="bg-gray-50 border border-gray-200 rounded-xl shadow p-6 flex-1 flex flex-col items-center hover:shadow-lg transition"
          >
            <img
              src={t.avatar}
              alt={t.name}
              className="w-16 h-16 rounded-full mb-4 object-cover border-2 border-blue-200"
            />
            <p className="text-gray-700 text-center mb-4">“{t.text}”</p>
            <span className="font-semibold text-gray-900">{t.name}</span>
          </div>
        ))}
      </div>
    </div>
  </section>
);

export default Testimonials;
