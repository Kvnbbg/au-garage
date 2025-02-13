/* ========================================================================
   1. CSS RESET & GLOBAL SETTINGS
   ======================================================================== */
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  font-size: 16px;
  scroll-behavior: smooth;
  scroll-snap-type: y mandatory;
}

body {
  font-family: 'Poppins', sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
  line-height: 1.6;
  padding: var(--base-padding);
  overflow-x: hidden;
}

/* ========================================================================
   2. CSS VARIABLES (THEMING, SPACING & ANIMATIONS)
   ======================================================================== */
:root {
  /* Colors & Theme */
  --primary-color: #007bff;
  --primary-hover: #0056b3;
  --secondary-color: #6c757d;
  --background-color: #f0f0f0;
  --text-color: #333;
  --accent-color: #ff4081;
  --btn-success: #28a745;
  --btn-success-hover: #218838;
  --link-hover: #d1ecf1;
  
  /* Spacing & Sizing */
  --base-padding: 1rem;
  --container-max-width: 1140px;
  
  /* Animation Settings */
  --float-effect: 3px;
  --float-duration: 8s;
  --bubble-size: 60px;
  --bubble-shadow: 0 4px 15px rgba(255, 64, 129, 0.4);
  --tiktok-duration: 3s;
  --async-delay: 0.3s;
}

/* ========================================================================
   3. TYPOGRAPHY & GLOBAL ELEMENTS
   ======================================================================== */
h1, h2, h3, h4, h5, h6 {
  font-family: 'M PLUS Rounded 1c', sans-serif;
  margin-bottom: 0.5em;
}

p {
  margin-bottom: 1em;
}

/* ========================================================================
   4. LAYOUT CONTAINERS (HEADER, NAV, MAIN, FOOTER)
   ======================================================================== */
header {
  background-color: var(--primary-color);
  color: #fff;
  padding: 1.5rem;
  border-bottom: 3px solid var(--secondary-color);
  position: relative;
  animation: float var(--float-duration) ease-in-out infinite;
  overflow: hidden;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(calc(-1 * var(--float-effect))); }
}

nav.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  padding: 1rem;
  background-color: #333;
}

nav.navbar a {
  color: #fff;
  text-decoration: none;
  font-size: 1.1rem;
  transition: transform 0.3s ease, color 0.3s ease;
  position: relative;
}

nav.navbar a:hover {
  transform: translateY(calc(-1 * var(--float-effect)));
  color: var(--link-hover);
}

/* Animated pseudo-element for navbar links */
nav.navbar a::after {
  content: '';
  position: absolute;
  width: 0%;
  height: 2px;
  left: 0;
  bottom: -4px;
  background: var(--accent-color);
  transition: width 0.3s ease;
}
nav.navbar a:hover::after {
  width: 100%;
}

/* Container for content */
.container,
.container-fluid {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 15px;
}

/* Slide-in animation for main content */
.slide-container {
  animation: slideIn 1s ease-out forwards;
}

@keyframes slideIn {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* Footer */
footer {
  background-color: #222;
  color: #fff;
  padding: 2rem 0;
  text-align: center;
}

/* ========================================================================
   5. BUTTONS, FORMS & INTERACTIVE ELEMENTS
   ======================================================================== */
.btn {
  background-color: var(--btn-success);
  color: #fff;
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 0.25rem;
  text-decoration: none;
  transition: background-color 0.3s ease, transform 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

/* Experiment: button hover with before pseudo-element expanding */
.btn::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 100%;
  transform: translate(-50%, -50%);
  transition: width 0.4s ease, height 0.4s ease;
}

.btn:hover::before {
  width: 200%;
  height: 200%;
}

.btn:hover {
  background-color: var(--btn-success-hover);
  transform: translateY(calc(-1 * var(--float-effect)));
}

/* Form Elements */
form input,
form button,
form select,
form textarea {
  width: 100%;
  padding: 0.5rem;
  margin: 0.625rem 0;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
}

/* ========================================================================
   6. MODALS & POP-UP COMPONENTS
   ======================================================================== */
#customModal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.85);
  color: #fff;
  padding: 20px;
  border-radius: 8px;
  display: none;
  z-index: 10000;
  opacity: 0;
  transition: opacity 0.3s ease;
  max-width: 80%;
  text-align: center;
}

/* ========================================================================
   7. DRAGGABLE & BUZZ EFFECT ELEMENTS
   ======================================================================== */
.draggable {
  user-select: none;
  cursor: move;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
}

.draggable:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

@keyframes buzz {
  0% { transform: translate(0, 0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(-2px, -2px); }
  60% { transform: translate(2px, 2px); }
  80% { transform: translate(2px, -2px); }
  100% { transform: translate(0, 0); }
}

.buzz-effect {
  animation: buzz 0.5s linear;
}

/* ========================================================================
   8. SPREADSHEET & DATA TABLE STYLES
   ======================================================================== */
.spreadsheet-container {
  overflow-x: auto;
  margin: 20px auto;
  max-width: 95%;
}

.spreadsheet-container table {
  width: 100%;
  border-collapse: collapse;
}

.spreadsheet-container th,
.spreadsheet-container td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
  min-width: 80px;
}

.spreadsheet-container th {
  background-color: var(--primary-color);
  color: #fff;
}

/* ========================================================================
   9. FLOATING BUBBLE BUTTON & BACKGROUND ANIMATION
   ======================================================================== */
.bubble-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: var(--bubble-size);
  height: var(--bubble-size);
  background-color: var(--accent-color);
  border-radius: 50%;
  box-shadow: var(--bubble-shadow);
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
  font-size: 1.5rem;
  cursor: pointer;
  z-index: 10000;
  animation: bubbleFloat 4s ease-in-out infinite;
}

@keyframes bubbleFloat {
  0% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0); }
}

/* ========================================================================
   10. TIKTOK-INSPIRED INTERACTIVE LOOP ANIMATION
   ======================================================================== */
.tiktok-interactive {
  animation: tiktokLoop var(--tiktok-duration) ease-in-out infinite;
}

@keyframes tiktokLoop {
  0% { transform: scale(1) rotate(0deg); }
  50% { transform: scale(1.1) rotate(5deg); }
  100% { transform: scale(1) rotate(0deg); }
}

/* ========================================================================
   11. EXPERIMENTAL: ASYNCHRONOUS & LOOPING ANIMATIONS
   ======================================================================== */
/* Example: a text shimmer effect using before/after with delay */
.shimmer {
  position: relative;
  color: #333;
  overflow: hidden;
}
.shimmer::before {
  content: '';
  position: absolute;
  top: 0;
  left: -150%;
  width: 100%;
  height: 100%;
  background: linear-gradient(120deg, transparent, rgba(255,255,255,0.5), transparent);
  animation: shimmerEffect 2s infinite;
}

@keyframes shimmerEffect {
  0% {
    left: -150%;
  }
  50% {
    left: 150%;
  }
  100% {
    left: 150%;
  }
}

/* Asynchronous style: delays on hover for a list of items */
.async-hover li {
  opacity: 0;
  transform: translateY(10px);
  animation: asyncFadeIn 0.5s forwards;
  animation-delay: calc(var(--async-delay) * var(--i));
}

@keyframes asyncFadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========================================================================
   12. CSS GRID EXPERIMENTS FOR LAYOUTS
   ======================================================================== */
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.grid-item {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 4px;
  position: relative;
  transition: transform 0.3s ease;
}

.grid-item:hover {
  transform: translateY(-5px);
}

/* ========================================================================
   13. ADDITIONAL COMPONENTS & PSEUDO-ELEMENT EXPERIMENTS
   ======================================================================== */
/* Decorative title with a gradient underline using ::after */
.decorative-title {
  font-size: 2rem;
  margin-bottom: 1rem;
  position: relative;
  display: inline-block;
}

.decorative-title::after {
  content: "";
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
  border-radius: 2px;
}

/* Experiment: Animated border around a container on hover */
.hover-border {
  position: relative;
  padding: 1rem;
  transition: all 0.3s ease;
}

.hover-border::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 0%;
  height: 100%;
  border: 2px solid var(--accent-color);
  transition: width 0.3s ease;
}

.hover-border:hover::before {
  width: 100%;
}

/* ========================================================================
   14. RESPONSIVE DESIGN & MEDIA QUERIES
   ======================================================================== */
@media (max-width: 992px) {
  header { padding: 1rem; }
  nav.navbar { gap: 1rem; padding: 0.5rem; }
}

@media (max-width: 768px) {
  nav.navbar { flex-direction: column; }
  html { scroll-snap-type: none; }
}

/* ========================================================================
   15. ACCESSIBILITY: PREFERS-REDUCED-MOTION
   ======================================================================== */
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
