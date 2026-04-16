# Troopod AI - PM Assignment Details

This document explains the technical flow, agent design, and error-handling strategies for the Landing Page Personalization Prototype.

## 1. How the System Works (Flow)

The prototype operates on a deterministic "Read -> Analyze -> Replace" sequence to safely personalize web pages without breaking structure:

1. **Input Stage**: The user supplies an Ad Creative (text/context) and a Landing Page URL.
2. **Scraping & Extraction Engine**: The backend acts as a proxy, fetching the raw HTML of the landing page. It then parses the DOM (Document Object Model) and extracts meaningful text nodes (e.g., `<p>`, `<h1>`, `<a>`) while discarding layout elements, scripts, and styles.
3. **AI Agent Contextualization**: The extracted texts, along with the ad creative context, are passed to the Large Language Model (Gemini / OpenAI).
4. **Structured JSON Output**: The AI acts as a Conversion Rate Optimization (CRO) expert. It returns a strict JSON array containing mapping pairs: `old_text` (found on the site) and `new_text` (personalized version).
5. **Deterministic DOM Injection (Crucial Step)**: The server receives the JSON mapping. It iterates through the original DOM tree. Instead of blindly searching and replacing string data (which could destroy HTML tags or CSS classes), it locates the exact text nodes in the parser matching `old_text` and applies the `new_text` substitution natively through the parser object.
6. **Delivery**: The modified, personalized HTML document is injected with a `<base>` URL tag to fix relative assets (like images) and rendered back to the user within a sandboxed viewer.

## 2. Key Components / Agent Design

Our agent is designed to be highly specific and constrained to limit unpredictable behavior.

- **System Instruction Constraints**: The agent is explicitly told to focus only on persuasive copy (headlines, sub-headlines, CTAs). It avoids modifying utility copy (like specific copyright dates or legal boilerplate).
- **Strict Output Schema Enforcement (Pydantic/JSON)**: The LLM is forced to return responses that adhere to a predefined schema schema. This prevents the LLM from entering a conversational state or generating markdown wrappers that break the programmatic parsing.

## 3. Handling Edge Cases & Systemic AI Risks

A naive AI system that asks an LLM to "rewrite this HTML" will fail continuously due to syntax errors or style stripping. Here is how we handle common pitfalls:

### How we handle: Random changes
**Problem:** The AI might try to rewrite the entire text sequence, losing the company's specific branding or tone.
**Solution:** The prompt explicitly restricts the agent to only output changes that make sense to align with the ad context. If the original text is already good, the agent is instructed not to include it in the replacement JSON array. By targeting only distinct arrays of text, most of the page remains 100% authentic.

### How we handle: Broken UI
**Problem:** AI-generated HTML often strips away Tailwind classes, CSS specificities, or JavaScript bindings, resulting in an unstyled mess.
**Solution:** The AI **never** touches or generates HTML. The AI only sees plain text arrays, and outputs plain text replacements. The backend engine handles the deterministic injection directly into the text nodes of the original HTML DOM, guaranteeing that the structure and CSS classes remain completely untouched.

### How we handle: Hallucinations
**Problem:** The AI might output a change for text that does not actually exist on the page, or invent elements.
**Solution:** Grounding via exact string matching. Since the LLM returns an `old_text` to `new_text` mapping, our replacement function simply checks if `old_text` exists precisely inside the target DOM. If the AI hallucinates a piece of text to replace that isn't on the page, the replacement function safely ignores it. Furthermore, the AI is prompted strictly: *"The old_text MUST exactly match one of the provided page texts."*

### How we handle: Inconsistent outputs
**Problem:** The LLM might output a list one time, and a paragraph the next.
**Solution:** Hardcoded API Schema constraints (e.g., using `response_schema` in Gemini or `response_format` in OpenAI with a Pydantic model). The API will throw an error at the generation level if the LLM fails to match the strict JSON structural requirements, ensuring the application code never receives an inconsistent or un-parsable format.
