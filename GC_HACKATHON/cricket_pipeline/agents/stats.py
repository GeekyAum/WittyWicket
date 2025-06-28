class StatsAnalyzerAgent:
    def __init__(self, vector_client):
        self.vector_client = vector_client
        
    def run(self, state):
        current_play = state['current_play']
        player_involved = state['player_involved']
        
        # Query for relevant stats and records
        stat_query = f"Statistics and records for {player_involved} in similar situations"
        relevant_stats = self.vector_client.similarity_search(stat_query)
        
        # Process and format the stats
        return {
            "interesting_stats": self._format_stats(relevant_stats),
            "player_records": self._detect_records(relevant_stats, current_play)
        }
