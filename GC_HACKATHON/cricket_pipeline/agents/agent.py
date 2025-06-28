import os
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from config import key_instance
# Initialize Gemini
model=Groq(id="llama-3.3-70b-versatile",api_key=os.getenv("GROQ_API_KEY'"))

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


