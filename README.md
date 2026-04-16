# Troopod AI · Landing Page Personalizer 🚀

A prototype AI workflow that takes an **ad creative** and a **landing page URL**, then generates a **CRO-optimized, personalized version** of the page aligned to the ad.

## Quick Start

```bash
# 1. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Set your Gemini API key
export GEMINI_API_KEY="your-key-here"

# 4. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## How It Works

1. **Fetch** — Scrapes the target landing page HTML
2. **Extract** — Parses out meaningful text nodes (headlines, paragraphs, CTAs)
3. **Analyse** — Sends text + ad context to the AI (Gemini) for CRO suggestions
4. **Inject** — Deterministically replaces text in the DOM without touching HTML/CSS structure
5. **Render** — Displays the personalized page in a live preview

## Mock Mode

If no API key is provided, the app runs in **mock mode** with sample replacements to demonstrate the full flow.

## Tech Stack

- **Python 3.9+**
- **Streamlit** — UI framework
- **BeautifulSoup4** — HTML parsing & DOM manipulation
- **Google GenAI** — LLM for CRO copy generation
- **Pydantic** — Strict schema enforcement for AI output
