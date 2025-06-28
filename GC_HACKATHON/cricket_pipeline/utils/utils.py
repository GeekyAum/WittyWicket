import json
from typing import Dict, Any

def load_cricket_data(file_path: str) -> Dict[str, Any]:
    """Load cricket data from a JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Failed to load cricket data: {str(e)}")

def save_commentary(commentary: str, output_file: str) -> None:
    """Save generated commentary to a file."""
    try:
        with open(output_file, "w") as f:
            f.write(commentary)
        print(f"Commentary saved to {output_file}")
    except Exception as e:
        print(f"Failed to save commentary: {str(e)}")