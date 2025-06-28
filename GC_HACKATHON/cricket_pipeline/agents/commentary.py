import os
import argparse
from dotenv import load_dotenv
from agents.agent import cricket_commentary_team
from utils.utils import load_cricket_data, save_commentary


def generate_commentary(input_file: str, output_file: str = None) -> str:
    """Generate cricket commentary from input JSON data."""
    # Validate Gemini API key
    # if not os.environ.get("GEMINI_API_KEY"):
    #     raise ValueError("GEMINI_API_KEY environment variable not set.")
    
    # Load cricket data
    cricket_data = load_cricket_data(input_file)
    
    # Generate commentary using the agent team
    print("Generating cricket commentary...")
    result = cricket_commentary_team.run(cricket_data=cricket_data)
    
    commentary = result.get("final_commentary")
    
    if not commentary:
        raise Exception("Failed to generate commentary")
    
    # Save commentary if output file is specified
    if output_file:
        save_commentary(commentary, output_file)
    
    return commentary