# import time
# import json
# from ingestion.match_finder import CricketMatchFinder
# from ingestion.CricketScraper import CricketScraper
# from ingestion.file_monitor import FileMonitor
# from ingestion.data_parser import DataParser

# class CricketDataPipeline:
#     def __init__(self):
#         self.match_finder = CricketMatchFinder()
#         self.scraper = CricketScraper()
#         self.file_monitor = FileMonitor(directory="./live_cricket_media")
#         self.parser = DataParser()
#         self.output_dir = "./cricket_data"

#     def fetch_live_data(self, match_ids):
#         """Fetch data from API and file monitor."""
#         match_data = []
#         for match_id in match_ids:
#             api_data = self.scraper.fetch_match_data(match_id)
#             if api_data:
#                 match_data.append(api_data)

#         multimedia_data = self.file_monitor.get_data_stream()
#         combined_data = match_data + multimedia_data
#         return self._process_data(combined_data)

#     def _process_data(self, raw_data):
#         """Parse and process raw data."""
#         parsed = []
#         for data in raw_data:
#             parsed.append(self.parser.parse_row(data))
#         return parsed

#     def save_as_json(self, data):
#         """Save processed data as JSON."""
#         timestamp = int(time.time())
#         output_file = f"{self.output_dir}/match_{timestamp}.json"
        
#         # Ensure output directory exists
#         Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
#         with open(output_file, 'w') as f:
#             json.dump(data, f, indent=2)
#         return output_file

#     def run(self, poll_interval=30):
#         """Run the pipeline continuously."""
#         while True:
#             try:
#                 match_ids = self.match_finder.get_live_match_ids()
#                 if not match_ids:
#                     print("No active matches found")
#                     time.sleep(poll_interval)
#                     continue

#                 live_data = self.fetch_live_data(match_ids)
#                 if live_data:
#                     saved_path = self.save_as_json(live_data)
#                     print(f"Data saved to {saved_path}")
                
#                 time.sleep(poll_interval)

#             except KeyboardInterrupt:
#                 print("Pipeline stopped by user")
#                 break
#             except Exception as e:
#                 print(f"Error: {str(e)}")
#                 time.sleep(60)  # Backoff on critical errors


# if __name__ == "__main__":
#     pipeline = CricketDataPipeline()
#     pipeline.run(poll_interval=30)  # Polling interval of 30 seconds


# CricketScraper.py
import requests
import time

class CricketScraper:
    def __init__(self, base_url="https://www.cricbuzz.com/live-cricket-scores"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'CricketScraper/1.0'})

    def fetch_match_data(self, match_id):
        """Fetch live match data from API"""
        try:
            response = self.session.get(f"{self.base_url}/{match_id}", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Error: {str(e)}")
            return None
