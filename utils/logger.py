import logging
import os
from config.config import Config

def setup_logger():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename=Config.LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)
