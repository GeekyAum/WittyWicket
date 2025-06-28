# AI Sports Commentator

This project creates an AI-based **sports commentator** that generates real-time commentary for live matches, initially focusing on cricket, and is designed to be extensible for other sports in the future. The system uses **web scraping**, **Pathway Vector Store**, and **Agentic Team Large Language Models (LLMs)** to simulate dynamic and immersive commentary experiences.

---

## Problem Statement

Our goal is to create an AI-based **sports commentator** that can simulate real-time commentary during sports events. Initially focused on cricket, we plan to expand this system for other sports in the future. The flow of the system includes several key steps:

1. **Match Information Scraping**:  
   - We scrape live match data (such as match IDs and titles) from the internet.
   - The user is then prompted to select the match ID for which they want to view commentary.

2. **Ball-to-Ball (or Event-by-Event) Details Scraping**:  
   - Once the match ID is selected, we scrape detailed match information such as runs, wickets, scores, or other events.

3. **Ingesting Data into Pathway Vector Store**:  
   - We use **Pathway** to ingest the scraped data into a **vector store** for efficient querying and analysis.

4. **Agentic Team LLMs for Commentary Generation**:  
   - We leverage an **Agentic Team of LLMs** consisting of two specialized models:
     - **Commentary Generator**: Generates dynamic, engaging commentary based on real-time events.
     - **Stats Analyzer**: Analyzes match statistics to enhance commentary with relevant insights (e.g., player performance, historical data).
   - These two models communicate with each other to create an immersive commentary experience for the user.

5. **Future Modifications**:  
   - **Personalized Commentary**: We aim to introduce a **personalized touch** for users, considering preferences, player/team history, and user behavior.
   - **Deeper Integration of Past Data**: We plan to use more **historical match data** to make the commentary more in-depth and nuanced.
   - **Multi-Sport Accessibility**: In the future, we want to expand the system to make it **accessible for commentary of all other sports** (e.g., football, basketball, tennis) by modifying the data scraping and commentary generation flow to accommodate the unique events of each sport.

---

## How It Works

### 1. **Setup API Keys**  
   Before running the application, you must configure your **Gemini API Key** and **Pathway License Key**.

   - Open the `config.py` file.
   - Set your **Groq API Key** and **Pathway License Key**.

```python
# config.py

# Set your Gemini API Key
gemini_api_key = "your_groq_api_key"

# Set your Pathway License Key
license_key = "your-pathway-license-key"
```
# Cricket Pipeline Application

This application can be run using Docker to ensure all dependencies are installed and configured correctly.

## Steps to Run the Application

### 1. Build the Docker Image

First, navigate to the project repository:

```bash
cd path_to_the_repo
```

Then, build the Docker image using the following command:
```bash
docker build -f cricket_pipeline/Dockerfile -t cricket-pipeline .
```
Once the image is built, you can run the Docker container with the following command:
```bash
docker run -p 9000:9000 cricket-pipeline
```

## Interact with the Script

The script will ask for the match ID and display real-time commentary for the selected match.

---

## Flowchart

### System Flow:

1. **Scrape Match Information**:  
   We scrape the live match IDs and titles from the internet.

2. **User Match Selection**:  
   The user is asked which match they want to see commentary for.

3. **Scrape Ball-to-Ball or Event-by-Event Data**:  
   We scrape event-based data such as runs, wickets, scores, and other key moments.

4. **Ingest Data into Pathway Vector Store**:  
   Event-by-event data is ingested into the **Pathway Vector Store** for analysis.

5. **Generate Commentary with LLMs**:
   - The **Commentary Generator** produces the commentary.
   - The **Stats Analyzer** provides insightful statistics for the match, enhancing the commentary. It also has the access to websearch interesting stats as well.

6. **Deliver Real-Time Commentary**:  
   The system generates and delivers real-time commentary to the user.

---

## Future Enhancements

1. **Personalized Commentary**:  
   We plan to introduce features that allow users to tailor the commentary to their preferences, such as their favorite players, teams, or even certain types of commentary (e.g., aggressive, analytic, or humorous).

2. **Incorporate Historical Match Data**:  
   We will incorporate more historical match data to provide deeper insights and make the commentary more nuanced and interesting, enhancing the context of each game.

3. **Multi-Sport Support**:  
   While the system is currently designed for cricket, we aim to make the framework extendable for other sports like football, basketball, and tennis. The data scraping and commentary generation models will be adapted to handle the unique dynamics and events of each sport, ensuring an immersive experience for all sports fans.
