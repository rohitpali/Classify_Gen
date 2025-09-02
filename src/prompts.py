from typing import List, Dict, Any

def build_prompt(asset_classification_name: str,
                 manufacturer: str,
                 model_number: str,
                 search_results: List[Dict[str, Any]]):
    """
    Build a strict JSON-only instruction prompt for Gemini,
    with a richer summary style.
    """
    # search results into short context
    bullets = []
    for item in (search_results or [])[:5]:
        title = item.get("title", "")
        url = item.get("url", item.get("source", ""))
        snippet = item.get("content", item.get("snippet", ""))
        bullets.append(f"- {title} | {url}\n  {snippet}")

    context_text = "\n".join(bullets) if bullets else "No web results."

    return f"""


{{
  "asset_classification": "<string>",
  "manufacturer": "<string>",
  "model_number": "<string>",
  "product_line": "<string>",
  "summary": "<string>"
}}

Rules:
- If any field is unknown, return an empty string "" for that field.
- Always echo the provided model_number in "model_number".
- In "summary", write 1–2 sentences in the following style:
  "The <Manufacturer> <Model_number> is a <Asset_classification> categorized under <Product_line>, designed for <main usage/features>."
- Use info from CONTEXT where available, otherwise keep it generic.
- Be concise, professional, and factual.

INPUT:
- asset_classification_name: "{asset_classification_name}"
- manufacturer (optional): "{manufacturer}"
- model_number: "{model_number}"

CONTEXT (web snippets):
{context_text}
"""
