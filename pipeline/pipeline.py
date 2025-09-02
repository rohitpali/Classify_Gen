import time
import logging
from typing import Dict, Any
from utils.web_search import TavilySearch
from utils.gemini import GeminiAnalyzer
from src.prompts import build_prompt
from config.config import Config

logger = logging.getLogger(__name__)

REQUIRED_OUTPUT_FIELDS = [
    "asset_classification",
    "manufacturer",
    "model_number",
    "product_line",
    "summary",
]

class AssetCheckPipeline:
    def __init__(self, tavily_api_key: str, gemini_api_key: str):
        self.search = TavilySearch(tavily_api_key)
        self.analyzer = GeminiAnalyzer(gemini_api_key)

    def _is_complete(self, data: Dict[str, Any]) -> bool:
        if not isinstance(data, dict):
            return False
        #contain all required keys
        for k in REQUIRED_OUTPUT_FIELDS:
            if k not in data:
                return False
        # contain 2 fields not empty
        if not data.get("asset_classification") or not data.get("model_number"):
            return False
        return True

    def run(
        self,
        model_number: str,
        asset_classification_name: str,
        manufacturer: str = "",
        asset_classification_guid2: str = "",
    ) -> Dict[str, Any]:
        # query for search
        query_parts = [model_number]
        if manufacturer:
            query_parts.append(manufacturer)
        if asset_classification_name:
            query_parts.append(asset_classification_name)
        if asset_classification_guid2:
            query_parts.append(asset_classification_guid2)
        query = " ".join(query_parts)

        logger.info(
            f"Input received | model_number={model_number} | "
            f"asset_classification_name={asset_classification_name} | manufacturer={manufacturer}"
        )

        # search with retries
        search_results = []
        for attempt in range(1, Config.MAX_SEARCH_RETRIES + 1):
            try:
                logger.info(f"Tavily attempt {attempt} | query='{query}'")
                search_results = self.search.search(query)
                if search_results:
                    break
            except Exception as e:
                logger.warning(f"Tavily attempt {attempt} failed: {e}")
            time.sleep(1)

        if not search_results:
            logger.warning("No Tavily results; proceeding with empty context.")

        # LLM attempts (up to 5)
        for attempt in range(1, Config.MAX_LLM_RETRIES + 1):
            logger.info(f"Gemini attempt {attempt}")
            prompt = build_prompt(
                asset_classification_name=asset_classification_name,
                manufacturer=manufacturer,
                model_number=model_number,
                search_results=search_results,
            )
            parsed = self.analyzer.analyze_to_json(prompt)

            if parsed and self._is_complete(parsed):
                logger.info(f"✅ Gemini succeeded on attempt {attempt}")
                return parsed

            logger.warning("Gemini returned invalid/incomplete JSON. Retrying...")
            time.sleep(1)

        #   Fallback per spec
        logger.error(" Gemini failed after retries. Returning fallback response.")
        return {
            "asset_classification": "Generator Emissions/UREA/DPF Systems",
            "manufacturer": "",
            "model_number": model_number,
            "product_line": "",
            "summary": "",
        }
