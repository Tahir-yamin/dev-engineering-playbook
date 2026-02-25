# 🧠 Silent Health | The Neuro-Audit Protocol

[![Next.js](https://img.shields.io/badge/Next.js_15-000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![Gemini](https://img.shields.io/badge/Gemini_3.0_Pro-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe_WASM-0078D4?style=for-the-badge&logo=webassembly&logoColor=white)](https://google.github.io/mediapipe/)
[![Tailwind](https://img.shields.io/badge/Tailwind_v4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Google Antigravity](https://img.shields.io/badge/Google_Antigravity-34A853?style=for-the-badge&logo=google-cloud&logoColor=white)](#)

![Clinical Dashboard](https://github.com/Tahir-yamin/silent-health/raw/master/public/dashboard-preview.png)

> **"Transforming Subtle Biological Noise into Actionable Clinical Intelligence."**

Silent Health is a zero-install, privacy-first neurological monitoring platform designed for the early detection of digital biomarkers associated with Parkinson's Disease and other motor-cognitive conditions. By combining **Mechanical Engineering Rigor** with **Generative AI**, we bridge the gap between infrequent clinic visits and daily physiological reality.

---

## 🚀 Key Features

- **Multimodal Sensing**: Simultaneous tracking of facial motility, blink rates, and vocal micro-tremors via standard web peripherals.
- **Privacy-First (On-Device)**: RAW video and audio buffers never leave the browser. All inference happens locally using WebAssembly.
- **Intelligent Clinical Audit**: Powered by **Gemini 3.0 Pro**, the system generates autonomous reports every 100 frames (~3.3s) to identify deviations from a user's unique baseline.
- **Longitudinal Analytics**: Integrated Recharts-based trend analysis allowing clinicians and users to visualize disease progression over weeks or months.
- **Clinical Alignment**: Metrics are calibrated against **UPDRS (Unified Parkinson's Disease Rating Scale)** protocols for high-fidelity biomarker detection.

---

## 🛠️ The Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Framework** | [Next.js 15 (App Router)](https://nextjs.org/) | Core application architecture & routing. |
| **Inference** | [MediaPipe Face Mesh (WASM)](https://google.github.io/mediapipe/solutions/face_mesh) | 478-point 3D landmark tracking at 30Hz. |
| **Reasoning** | [Google Gemini 3.0 Pro](https://deepmind.google/technologies/gemini/) | Clinical Vector Audit & High-Reasoning Report Generation. |
| **Storage** | [Dexie.js (IndexedDB)](https://dexie.org/) | High-performance, client-side clinical record storage. |
| **Signal Processing** | [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API) | Real-time analysis of Vocal Jitter and Shimmer. |
| **Visualization** | [Recharts](https://recharts.org/) | Longitudinal trend lines & Interactive Brush range selection. |
| **Design** | [Tailwind CSS v4](https://tailwindcss.com/) | Medical-grade, dark-mode specialized UI. |

---

## 📊 Documentation & Methodology

### 1. Visual Audit (Hypomimia)
Using **MediaPipe FaceMesh**, we calculate the **Facial Motility Score**. A decrease in spontaneous muscle activation (Hypomimia) is a primary marker of Parkinsonian "masking." We monitor 78 specific landmarks around the eyes and mouth to detect micro-expressions invisible to the human eye.

### 2. Vocal Audit (Stability)
The **Vocal Jitter** analysis monitors frequency instability during speech. Significant increases in jitter signal the onset of subtle neurological tremors in the laryngeal muscles.

### 3. The "Audit Protocol"
Silent Health does not just "record"—it "audits." The system captures a dedicated **Baseline** for every user. Gemini 3.0 Pro then performs a comparative analysis of the current session against this baseline using Z-score deviations, producing a strictly formatted clinical report.

---

## 🏗️ Getting Started

### Prerequisites
- Node.js 18+
- An API Key (configured in `.env.local`)

### Installation
```bash
git clone https://github.com/Tahir-yamin/silent-health.git
cd silent-health
npm install
```

### Environment Setup
Create a `.env.local` file in the root:
```env
NEXT_PUBLIC_OPENROUTER_API_KEY=your_key_here
```

### Development
```bash
npm run dev
```

---

## 🧬 Scientific Inspiration
The project is rooted in the "mPower" biological protocol, applying the principles of **Predictive Maintenance** (typically used in Mechanical Engineering for turbines/motors) to the most complex machine of all: the human nervous system.

---

## ⚖️ License & Disclaimer
This tool is for **Research and Educational use only**. It is not a diagnostic medical device. All data is processed locally to ensure participant privacy.

Developed with 💚 using **Google Antigravity** & **Gemini 3.0**.
