import json
import google.generativeai as genai

class GeminiAnalyzer:
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def analyze_to_json(self, prompt: str) -> dict | None:
        """Call Gemini and parse a STRICT JSON response. Return dict or None."""
        resp = self.model.generate_content(prompt)
        text = getattr(resp, "text", None)
        if not text:
            return None

        cleaned = text.strip()

        # Remove code fences if model returns ```json ... ```
        if cleaned.startswith("```"):
            # remove opening ```
            cleaned = cleaned.strip("`")
            # try to locate the JSON body
            start_idx = cleaned.find("{")
            end_idx = cleaned.rfind("}")
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                cleaned = cleaned[start_idx:end_idx + 1]

        try:
            return json.loads(cleaned)
        except Exception:
            return None
