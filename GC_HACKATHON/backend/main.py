import pathway as pw
import requests
import subprocess
import time
from pathlib import Path
import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo

# Initialize Groq model
# Ensure the environment variable 'GROQ_API_KEY' is set
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    # In a real application, you'd handle this more gracefully than raising an error here
    # For now, we'll raise an error to indicate the missing key
    raise ValueError("GROQ_API_KEY environment variable not set.")

model = Groq(model="llama-3.3-70b-versatile", api_key=groq_api_key)

# Stats Analyzer Assistant
stats_analyzer = Agent(
    name="StatsAnalyzer",
    model=model,
    tools = [DuckDuckGo()],
    instructions=["""
    You are an expert cricket statistician and analyst. Analyze the provided cricket match data to:
    
    1. Summarize the current match situation and key statistics
    2. Identify exceptional performances from batsmen (high strike rates, milestones)
    3. Highlight impressive bowling figures (economy rates, wicket-taking spells)
    4. Calculate partnership statistics and run rate trends
    5. Identify potential record-breaking performances or notable achievements
    6. Detect important game-changing moments worth highlighting
    7. Use websearch for some interesting statistics related to the batsman and the bowler

    The match data will include: score, run rates, batsmen stats (runs, balls, SR),
    bowler stats (overs, runs, wickets, economy), and recent commentary.
    
    Provide your analysis in a structured format that helps the commentary team understand
    key aspects of the current match situation and noteworthy performances.
    """],
    markdown=True
)

# Commentary Generator Assistant
commentary_generator = Agent(
    name="CommentaryGenerator",
    model=model,
    instructions=["""
    You are an elite cricket commentator renowned for captivating, insightful, and engaging commentary.
    
    Using the match data and statistical analysis provided:
    
    1. Create vibrant play-by-play commentary that brings the cricket match to life
    2. Weave statistical insights naturally into your narrative
    3. Use colorful language, cricket terminology, and appropriate expressions
    4. Vary your tone to match the game situation - excited for boundaries, analytical for strategy
    5. Incorporate the latest match developments from the 'latest_commentary' field
    6. Build upon but don't simply repeat existing commentary
    7. Include both immediate action description and strategic analysis
    
    Your commentary should feel authentic, passionate, and knowledgeable - like listening to
    an expert commentator during a live broadcast. Create at least 250 words of rich,
    compelling cricket commentary that truly engages fans.
    """],
    markdown=True
)

cricket_commentary_team = Agent(
    name="Cricket Commentary Team",
    team=[stats_analyzer, commentary_generator],
    model=model,
    instructions=[
        "Coordinate the team to generate engaging cricket commentary",
        "First, have the StatsAnalyzer analyze the match data and identify highlights",
        "Then, have the CommentaryGenerator use the analysis to create engaging commentary",
        "Ensure the final output is a cohesive and engaging cricket commentary"
    ],
    markdown=True,
)

# --- CricketDataPipeline Class (Copied from original main.py) ---
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

            # Check if server is already running
            try:
                requests.get("http://127.0.0.1:5000/", timeout=1)
                print("Flask server is already running.")
                return # Server is already running, no need to start again
            except requests.exceptions.RequestException:
                pass # Server is not running, continue to start it

            # Start the server process
            print("Starting Flask server...")
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
            # In a web server, you might not want to raise here, but log and return an error response
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

    # Pathway related methods - may need adjustment or can be omitted if not writing to CSV directly from backend
    def create_pathway_table(self, data: dict) -> pw.Table:
        """Convert API response to Pathway table with schema"""
        processed_data = self._process_api_response(data)

        class CricketDataSubject(pw.io.python.ConnectorSubject):
            def __init__(self, data_dict):
                super().__init__()
                self.data = data_dict

            def run(self):
                self.next(**self.data)

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
                    },
                     data.get("battertwo", ""): {
                        "runs": data.get("batsmantworun", 0),
                        "balls": data.get("batsmantwoball", 0)
                    }
                },
                 "bowlers": {
                    data.get("bowlerone", ""): {
                        "overs": data.get("bowleroneovers", 0),
                        "runs": data.get("bowleronerun", 0),
                        "wickets": data.get("bowleronewicket", 0)
                    }
                }
            }
        }

    def _get_schema(self):
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
        teams = title.split("vs") if "vs" in title else ["Unknown", "Unknown"]
        return teams[index].split("-")[0].strip()

    def _parse_runs(self, score: str) -> int:
        try:
            return int(score.split("/")[0])
        except (IndexError, ValueError):
            return 0

# --- FastAPI Endpoints ---
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow frontend to access the backend
# In a production environment, you should restrict the origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Keep track of the pipeline instance (simple for now)
pipeline_instance = None

@app.post("/api/set-match/{match_id}")
def set_match(match_id: str):
    global pipeline_instance
    try:
        # Start the local API server when setting the match
        pipeline = CricketDataPipeline(match_id)
        pipeline.start_api_server()
        pipeline_instance = pipeline # Store the pipeline instance
        return {"message": f"Match ID set to {match_id} and API server started."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set match or start API server: {e}")

@app.get("/api/live-data")
def get_live_data():
    global pipeline_instance
    if not pipeline_instance:
        raise HTTPException(status_code=400, detail="Match ID not set. Please call /api/set-match/{match_id} first.")

    try:
        # Fetch data
        cricket_data = pipeline_instance.fetch_cricket_data()
        if not cricket_data:
            return {"message": "Could not fetch live data.", "data": {}}

        # Process data and run agents
        processed_data = pipeline_instance._process_api_response(cricket_data)

        # Run commentary agent team
        print("Running commentary agent team...")
        agent_result = cricket_commentary_team.run(cricket_data=processed_data)

        # The agent result might be a dictionary or a string depending on the agent's last step
        # We'll return the raw data, processed data, and the agent's result
        return {
            "raw_data": cricket_data,
            "processed_data": processed_data,
            "agent_output": agent_result
        }

    except Exception as e:
        # In a real application, you might want more specific error handling
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching data or running agents: {e}")

# Optional: Add an endpoint to stop the server process on shutdown
# This is tricky with FastAPI and uvicorn lifecycle, may require custom handlers
# For simplicity, we'll omit this for the basic version.
# @app.on_event("shutdown")
# def shutdown_event():
#     global pipeline_instance
#     if pipeline_instance and pipeline_instance.server_process:
#         pipeline_instance.server_process.terminate()
#         print("Flask server process terminated.") 