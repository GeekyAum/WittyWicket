import requests
from bs4 import BeautifulSoup

class CricketMatchFinder:
    def __init__(self):
        self.base_url = "https://www.cricbuzz.com"
        self.live_url = "https://www.cricbuzz.com/cricket-match/live-scores"

    def get_live_match_info(self):
        """Scrape live match IDs and titles from Cricbuzz"""
        try:
            response = requests.get(self.live_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            matches = soup.find_all('a', href=True)
            match_ids = []
            match_titles = []
            
            for link in matches:
                href = link.get('href')
                if '/live-cricket-scores/' in href:
                    parts = href.split('/')
                    match_ids.append(parts[-2])
                    match_titles.append(parts[-1])
            
            return match_ids, match_titles
        except Exception as e:
            print(f"Error fetching matches: {e}")
            return [], []

finder = CricketMatchFinder()
match_ids, match_titles = finder.get_live_match_info()

# Display matches to the user
print("Available matches:")
for i, (match_id, title) in enumerate(zip(match_ids, match_titles)):
    print(f"{i+1}. {title.replace('-', ' ')} (ID: {match_id})")

# Get user input
# selected_id = input("\nEnter the ID of the match you want to see results for: ")
