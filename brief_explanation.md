# AdSync AI - Landing Page Personalizer (PM Assignment)

This document explains the technical flow, agent design, and error-handling strategies for the Landing Page Personalization Prototype built for the Troopod AI PM assignment.

---

## 🚀 1. How the System Works (System Flow)

AdSync AI operates on a deterministic **"Fetch → Parse → Personalize → Inject"** sequence. This architecture ensures that the AI can enhance copy without destroying the underlying website's code or styling.

1.  **Input Stage**: The user provides an **Ad Creative** (text/context) and a **Landing Page URL**.
2.  **Scraping Proxy**: The backend fetches the raw HTML of the target landing page. To ensure high fidelity, it uses a browser-like User Agent to retrieve the same version of the site a regular user would see.
3.  **Content Extraction**: Instead of sending the entire HTML to the AI (which is slow and contains noise), the system parses the DOM (Document Object Model) and extracts only meaningful, visible text nodes (Headlines, Paragraphs, CTAs).
4.  **AI Analysis (Gemini 1.5 Flash)**: The system sends the extracted text nodes and the Ad Creative context to the AI Agent. The AI acts as a **Conversion Rate Optimization (CRO) Copywriter**, identifying which pieces of text on the page can be improved to specifically match the ad's hook.
5.  **Structured JSON Output**: The AI returns a strict JSON object mapping the `old_text` (what was on the page) to the `new_text` (the AI suggestion), along with a human-friendly `change_summary`.
6.  **Deterministic Injection**: The backend receives the map and iterates through the original DOM tree. It replaces only the specific text content inside the target elements, preserving all CSS classes, IDs, and HTML attributes.
7.  **Real-Time Rendering**: The modified HTML, now with a `<base>` tag to ensure images and styles load from the original domain, is rendered in an optimized preview window.

---

## 🧠 2. Key Components & Agent Design

Our "Optimizer Agent" is designed with strict boundaries to ensure enterprise-grade reliability:

*   **Context-Aware Prompting**: The agent is instructed to focus exclusively on "Persuasive Copy" (Value Propositions and CTAs). It is forbidden from changing "Utility Copy" (Navigation menus, legal footers, or technical boilerplate).
*   **Structured Output Schema**: We use a **Pydantic-enforced JSON schema**. This forces the AI to output data in a consistent format that our code can parse directly, removing the risk of the AI including "chatty" preamble or invalid characters.
*   **Zero-Shot CRO Expertise**: The agent is fine-tuned via the system instruction to act as a world-class marketer, looking for alignment between the *Ad Hook* and the *Landing Page Headline*.

---

## 🛡️ 3. Handling AI Edge Cases & Reliability

Building with AI is risky because of non-deterministic behavior. AdSync AI handles these risks specifically:

### 🔄 Handling: Random Changes
**Problem**: The AI might rewrite well-performing text or lose brand tone.
**Solution**: The system uses a **Selective Replacement** strategy. The AI is instructed to *only* return changes it deems "high impact." If a piece of text is already aligned with the ad, it is omitted from the JSON results. 90% of the page code remains identical to the original.

### 🧩 Handling: Broken UI
**Problem**: Most AI tools fail when they try to "Generate HTML," often stripping styles (Tailwind, CSS-in-JS) or breaking scripts.
**Solution**: AdSync AI **never allows the AI to touch HTML**. The AI works only with plain text. The Python backend handles the surgical insertion of that text into the original structure, guaranteeing that the UI remains 100% intact and functional.

### 🧪 Handling: Hallucinations
**Problem**: The AI might suggest replacing text that doesn't actually exist on the page.
**Solution**: **Grounding via Exact Matching**. Our injection engine performs a strict `key-lookup`. If the AI returns a "replacement" for text it hallucinated (invented), the code simply finds zero matches in the DOM and ignores the change.

### 📋 Handling: Inconsistent Outputs
**Problem**: One run it might output a list, another run it might output a sentence.
**Solution**: **API Schema Enforcement**. By using the `response_schema` in the Gemini API, the AI is physically unable to return anything other than the requested JSON structure. If the model fails to follow the schema, the request is rejected at the API level before it ever touches your UI.

---

## 🛠️ Tech Stack & Setup
- **Frontend**: Streamlit (Python-based UI)
- **Engine**: BeautifulSoup4 (HTML Parsing) & Requests
- **AI**: Google Gemini 1.5 Flash (via `google-genai` library)
- **Deployment**: Streamlit Cloud + GitHub
