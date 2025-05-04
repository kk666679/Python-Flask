# ViralBoost: TikTok Virality Prediction Platform

ViralBoost is a Python Flask-based application designed to predict the virality of TikTok videos. It leverages web scraping, AI/ML models, and cloud services to analyze trends and provide insights.

## 🚀 Features

*   **TikTok Trend Scraping:** Automatically scrapes trending hashtags from TikTok's explore page using Playwright.
*   **AI Virality Prediction:** Employs a simple ML model (initially Logistic Regression) to predict the likelihood of a video going viral. (Future: PyTorch Transformer)
*   **User Authentication:** Integrated with Firebase Auth for user signup and management.
*   **Video Processing:** Allows users to upload videos to Firebase Storage.
*   **React Frontend Integration:** Designed to work with a React frontend for a seamless user experience.

## ⚙️ Architecture

*   **Backend:** Flask REST API (Python)
*   **Web Scraping:** Playwright (Python)
*   **AI/ML:** Scikit-learn (Python) (Future: PyTorch)
*   **Database:** Firestore (Firebase)
*   **Authentication:** Firebase Auth
*   **Storage:** Firebase Storage
*   **Frontend:** React (future integration)

## 🛠️ Setup

1.  **Clone the Repository:**
