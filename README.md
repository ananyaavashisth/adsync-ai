# AdSync AI · Landing Page Personalizer 🚀

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://adsync-ai.streamlit.app)

**AdSync AI** is an intelligent workflow that aligns your landing page messaging with your ad creatives in real-time to boost conversion rates (CRO).

## 🔗 Live Demo
**Check it out here: [adsync-ai.streamlit.app](https://adsync-ai.streamlit.app)**

---

## 🎯 The Goal
The goal of this project is to take a raw ad creative and a target landing page, then surgically personalize the page copy to match the ad's hook without breaking the site's design or functionality.

## 🛠️ How It Works
1.  **Surgical Extraction**: The system fetches the target HTML and extracts only the text nodes that impact performance (Headlines, CTAs, Paragraphs).
2.  **AI Alignment**: Using **Gemini 1.5 Flash**, the system compares the ad creative context with the page copy to find alignment gaps.
3.  **Deterministic Injection**: Suggestions are injected back into the original HTML DOM using Python. This ensures that **CSS, JS, and layout remain 100% intact**.
4.  **Live Preview**: The personalized version is rendered in a sandboxed preview with all original styles and assets loading via a proxy base tag.

---

## 🚀 Local Setup (For Developers)

If you want to run this project locally, follow these steps:

```bash
# 1. Clone & Setup
git clone https://github.com/ananyaavashisth/adsync-ai.git
cd adsync-ai
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Gemini API key (Optional for demo mode)
export GEMINI_API_KEY="your-key-here"

# 4. Run the app
streamlit run app.py
```

## 🧪 Demo Mode
If no API key is provided, the app runs in **Demo Mode**. This uses deterministic sample optimizations so you can experience the full workflow without an API key.

## 🏗️ Tech Stack
- **Python 3.9+**
- **Streamlit** (UI)
- **BeautifulSoup4** (DOM Manipulation)
- **Google Gemini AI** (Copywriting Engine)
- **Pydantic** (Schema Enforcement)
