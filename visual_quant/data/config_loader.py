import json
import os
import logging

CONFIG_DIR = "./config"
CONFIG_FILE = "config.json"

logger = logging.getLogger(__name__)
config_path = os.path.join(CONFIG_DIR, CONFIG_FILE)

if os.path.isfile(config_path):
    with open(config_path, "r") as f:
        config_data = json.load(f)
else:
    logger.error(f"config file {config_path} not found.")


def result_file_json():
    result_file_path = config_data["result_file"]
    if os.path.isfile(result_file_path):
        with open(result_file_path, "r") as f:
            return json.load(f)
