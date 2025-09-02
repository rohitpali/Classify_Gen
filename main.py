import json
from config.config import Config
from utils.logger import setup_logger
from utils.custom_exception import CustomException
from pipeline.pipeline import AssetCheckPipeline

logger = setup_logger()

# fields based on your input
REQUIRED_INPUT_FIELDS = ["model_number", "asset_classification_name"]


def validate_input(data):
    """Validate input.json (single object or list)."""
    entries = data if isinstance(data, list) else [data]

    for i, entry in enumerate(entries, 1):
        for field in REQUIRED_INPUT_FIELDS:
            if field not in entry or not isinstance(entry[field], str) or not entry[field].strip():
                raise CustomException(f"Missing required field in input {i}: {field}")


def process_input(input_data):
    """Run the full pipeline for one or multiple entries."""
    validate_input(input_data)

    pipeline = AssetCheckPipeline(
        tavily_api_key=Config.TAVILY_API_KEY,
        gemini_api_key=Config.GEMINI_API_KEY,
    )

    entries = input_data if isinstance(input_data, list) else [input_data]
    outputs = []

    for entry in entries:
        output = pipeline.run(
            model_number=entry["model_number"].strip(),
            asset_classification_name=entry["asset_classification_name"].strip(),
            manufacturer=entry.get("manufacturer", "").strip(),
            asset_classification_guid2=entry.get("asset_classification_guid2", "").strip(),
        )
        outputs.append(output)

    return outputs if isinstance(input_data, list) else outputs[0]


if __name__ == "__main__":
    logger.info("Started Classify Gen pipeline")

    try:
        with open("input.json", "r", encoding="utf-8") as f:
            input_data = json.load(f)

        result = process_input(input_data)

        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        logger.info("Output saved successfully to output.json")

    except CustomException as ce:
        logger.error(f" Validation failed: {ce}")
    except Exception as e:
        logger.exception(f" Pipeline failed: {e}")

    finally:
        logger.info(" Finished.\n")
