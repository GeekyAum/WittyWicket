import pathway as pw
import aiohttp
import asyncio

class WebSocketIngestor:
    def _init_(self, url: str):
        """
        Initialize the WebSocket ingestor with a URL.
        :param url: WebSocket URL for live cricket data.
        """
        self.url = url

    async def get_data_stream(self) -> pw.Table:
        """
        Connect to the WebSocket and ingest data as a Pathway table.
        :return: Pathway table containing live cricket data.
        """
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(self.url) as ws:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = await self._process_message(msg.data)
                        return pw.io.python.from_iterable(data)

    async def _process_message(self, message: str):
        """
        Process incoming WebSocket messages and parse them into Pathway-compatible format.
        :param message: Raw message from WebSocket.
        :return: Parsed data as a list of dictionaries.
        """
        import json
        parsed_data = json.loads(message)
        return [parsed_data]

    @staticmethod
    def _define_schema():
        """
        Define the schema for cricket data.
        :return: Pathway schema for parsing cricket data.
        """
        class CricketDataSchema(pw.Schema):
            match_id: str
            timestamp: int
            over: int
            ball: int
            batsman: str
            bowler: str
            runs: int
            wicket: bool
            context: str  
            team1: str  # Team 1 name
            team2: str  # Team 2 name
            current_score: str  # Current score (e.g., "125/3")
            match_status: str  # Match status (e.g., "ongoing", "paused", "completed")
            player_stats: dict  # Player statistics (e.g., {"batsman": {"runs": 45}, "bowler": {"wickets": 2}})
        
        return CricketDataSchema


# Example usage with multiple WebSocket URLs:
async def ingest_cricket_data():
    """
    Ingest cricket data from multiple WebSocket sources asynchronously.
    """
    websocket_urls = [
        "wss://live.cricbuzz.com/api/match/live",  
        # "wss://stream.sportradar.com/cricket",     # Example URL for SportRadar (paid service)
        # "wss://api.cricapi.com/live",              # Example URL for CricAPI (paid service)
    ]

    pathway_tables = []
    for url in websocket_urls:
        ingestor = WebSocketIngestor(url)
        try:
            table = await ingestor.get_data_stream()
            pathway_tables.append(table)
        except Exception as e:
            print(f"Failed to connect to {url}: {e}")

    return pathway_tables


# Process the ingested tables (example processing logic)
def process_data(tables):
    """
    Process and analyze the ingested cricket data tables.
    :param tables: List of Pathway tables containing cricket data.
    """
    for table in tables:
        table.print()  # Print the table content for debugging purposes


# Running the ingestion process asynchronously
if __name__ == "_main_":
    asyncio.run(ingest_cricket_data())