# ScoreLift Frontend

This is a React + TailwindCSS frontend for ScoreLift, a credit analysis platform for India.

## Features
- Landing page with hero section, CTA, testimonials
- PDF upload form for CIBIL report
- Live (simulated) credit score display with progress bar
- Modern, responsive 3-tier pricing page
- Mobile-first, fully responsive design
- React Router for navigation
- Well-commented, reusable components

## Pages
- `/` — Landing (hero, testimonials)
- `/upload` — PDF upload
- `/score` — Live score display
- `/pricing` — Pricing table

## Setup
1. Install dependencies:
   ```sh
   npm install
   # or
   yarn
   ```
2. Start development server:
   ```sh
   npm run dev
   # or
   yarn dev
   ```

## TailwindCSS
Tailwind is preconfigured. All styling is via Tailwind utility classes.

## Backend Integration
- To connect PDF upload or score analysis, see comments in `src/pages/UploadPage.jsx` and `src/pages/ScorePage.jsx` for where to call your API endpoints.
- Payment is not implemented; the pricing page uses a "Try for Free" CTA instead of Stripe.

## Project Structure
- `src/components/` — Reusable UI components
- `src/pages/` — Page components
- `src/App.jsx` — Routing

## Notes
- All images and avatars are placeholders.
- No backend code is included.

---

Built with ❤️ for ScoreLift.
