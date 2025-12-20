import os
import json
from typing import Any, Dict, Optional, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def read_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file: {file_path}")
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
    return None

def write_json_file(file_path: str, data: Dict[str, Any]) -> bool:
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error writing to file {file_path}: {str(e)}")
        return False

def ensure_directory_exists(dir_path: str) -> bool:
    try:
        os.makedirs(dir_path, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {dir_path}: {str(e)}")
        return False

def get_timestamp_string() -> str:
    return datetime.now().isoformat()

def filter_dict_keys(data: Dict[str, Any], keys_to_keep: List[str]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if k in keys_to_keep}

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]