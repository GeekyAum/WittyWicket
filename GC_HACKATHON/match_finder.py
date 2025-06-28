import requests
from bs4 import BeautifulSoup

class CricketMatchFinder:
    def __init__(self):
        self.base_url = "https://www.cricbuzz.com"
        self.live_url = "https://www.cricbuzz.com/cricket-match/live-scores"

    def get_live_match_ids(self):
        """Scrape live match IDs from Cricbuzz"""
        try:
            response = requests.get(self.live_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return [
                link.get('href').split('/')[-1] 
                for link in soup.find_all('a', href=True)
                if '/live-cricket-scores/' in link['href']
            ]
        except Exception as e:
            print(f"Error fetching matches: {e}")
            return []

finder = CricketMatchFinder()
live_match_ids = finder.get_live_match_ids()
print(f"Live Match IDs: {live_match_ids}")
