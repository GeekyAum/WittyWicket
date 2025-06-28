import pathway as pw
import requests
import subprocess
import time
from pathlib import Path
import json
import sys
import os
from ingestion.match_finder import CricketMatchFinder
from agents.agent import cricket_commentary_team,commentary_generator,stats_analyzer
from utils.utils import load_cricket_data
from agents.commentary import generate_commentary
import warnings
warnings.filterwarnings("ignore")
class CricketDataPipeline:
    def __init__(self, match_id: str):
        self.match_id = match_id
        self.api_url = f"http://127.0.0.1:5000/score?id={self.match_id}"
        self.server_process = None

    def start_api_server(self):
        """Start local API server from cricket-api repository"""
        try:
            repo_path = Path("cricket-api/api")
            if not repo_path.exists():
                # print("Cloning cricket-api repository...")
                subprocess.run(["git", "clone", "https://github.com/sanwebinfo/cricket-api"])
                
            # Start the server process
            self.server_process = subprocess.Popen(
                ["flask", "--app", "index.py", "run", "--host=0.0.0.0", "--port=5000"],
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for server to become available
            max_attempts = 30
            for attempt in range(max_attempts):
                try:
                    # Try connecting to the server
                    response = requests.get("http://127.0.0.1:5000/", timeout=2)
                    if response.status_code == 200:
                        print("Flask server started successfully!")
                        return
                except requests.exceptions.RequestException:
                    # Server not ready yet, wait and try again
                    time.sleep(1)
                    
            raise TimeoutError(f"Flask server failed to start after {max_attempts} seconds")
        except Exception as e:
            print(f"Server startup failed: {e}")
            raise


    def fetch_cricket_data(self) -> dict:
        """Fetch data from local API endpoint"""
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return {}

    def create_pathway_table(self, data: dict) -> pw.Table:
        """Convert API response to Pathway table with schema"""
        processed_data = self._process_api_response(data)
        
        # Create a ConnectorSubject class to feed the data
        class CricketDataSubject(pw.io.python.ConnectorSubject):
            def __init__(self, data_dict):
                super().__init__()
                self.data = data_dict
                
            def run(self):
                self.next(**self.data)
        
        # Create and return the table using a ConnectorSubject
        return pw.io.python.read(
            CricketDataSubject(processed_data),
            schema=self._get_schema()
        )


    def _process_api_response(self, data: dict) -> dict:
        """Transform API response to match document store schema"""
        return {
            "match_id": self.match_id,
            "timestamp": int(time.time()),
            "current_score": data.get("livescore", ""),
            "context": data.get("update", ""),
            "team1": self._extract_team(data.get("title", ""), 0),
            "team2": self._extract_team(data.get("title", ""), 1),
            "batsman": f"{data.get('batterone', '')}/{data.get('battertwo', '')}",
            "bowler": f"{data.get('bowlerone', '')}/{data.get('bowlertwo', '')}",
            "runs": self._parse_runs(data.get("livescore", "0/0")),
            "wicket": "wicket" in data.get("context", "").lower(),
            "player_stats": {
                "batsmen": {
                    data.get("batterone", ""): {
                        "runs": data.get("batsmanonerun", 0),
                        "balls": data.get("batsmanoneball", 0)
                    }
                }
            }
        }

    def _get_schema(self):
        """Document store schema for Pathway"""
        class CricketSchema(pw.Schema):
            match_id: str
            timestamp: int
            current_score: str
            context: str
            team1: str
            team2: str
            batsman: str
            bowler: str
            runs: int
            wicket: bool
            player_stats: dict
        return CricketSchema

    def _extract_team(self, title: str, index: int) -> str:
        """Extract team names from match title"""
        teams = title.split("vs") if "vs" in title else ["Unknown", "Unknown"]
        return teams[index].split("-")[0].strip()

    def _parse_runs(self, score: str) -> int:
        """Extract total runs from score string"""
        try:
            return int(score.split("/")[0])
        except (IndexError, ValueError):
            return 0

# Usage Example
if __name__ == "__main__":
    # Replace with your actual match ID from agent
    match_ids,match_titles = CricketMatchFinder().get_live_match_info()
    if not match_ids:
        raise ValueError("No live matches found")


    try:
        print("Waiting for input...")
        time.sleep(1)
        match_id = input("\nEnter the ID of the match you want to see results for: ")
        print(f"You entered: {match_id}")
    except EOFError:
        print("Input not available. Using first match as default.")
        match_id = match_ids[-1] if match_ids else None

    
    # match_id = "107563"
    pipeline = CricketDataPipeline(match_id)
    

    data_folder = "data"
    os.makedirs(data_folder, exist_ok=True)



    try:
        # Step 1: Start local API server
        pipeline.start_api_server()
        
        # Step 2: Fetch data from API
        cricket_data = pipeline.fetch_cricket_data()
        print("API Response:", cricket_data)

        data = cricket_data  # cricket_data is already a parsed dictionary

        # If you need to save it to a file:
        output_json_file = os.path.join(data_folder, "output_cricket_data.json")
        with open(output_json_file, "w", encoding="utf-8") as f:
            print("Data s")
            json.dump(data, f, indent=4)
        
        
        # Step 3: Create Pathway table
        pw_table = pipeline.create_pathway_table(cricket_data)
        
        # Step 4: Ingest into document store
        doc_store = pw.io.csv.write(pw_table, "./document_store.csv")
        stats_analyzer.print_response(f"Based upon the following cricket data {cricket_data} generate engaging and exciting commentary")

    except Exception as e:
        print(f"Pipeline failed: {e}")
    finally:
        if pipeline.server_process:
            pipeline.server_process.terminate()
