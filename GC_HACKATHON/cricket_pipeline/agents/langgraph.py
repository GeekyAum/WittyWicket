import langgraph.graph as lg
from langgraph.graph import END, StateGraph

def create_sports_commentary_graph():
    # Define the agents for different responsibilities
    agents = {
        "data_ingestion": DataIngestionAgent(),
        "context_retrieval": ContextRetrievalAgent(),
        "commentary_generator": CommentaryGeneratorAgent(),
        "stats_analyzer": StatsAnalyzerAgent(),
        "highlight_detector": HighlightDetectorAgent(),
        "user_personalizer": UserPersonalizerAgent()
    }
    
    graph = StateGraph(agents)
   
    graph.add_edge("data_ingestion", "context_retrieval")
    graph.add_edge("context_retrieval", "commentary_generator")
    graph.add_edge("context_retrieval", "stats_analyzer")
    graph.add_edge("stats_analyzer", "highlight_detector")
    graph.add_edge("highlight_detector", "user_personalizer")
    graph.add_edge("user_personalizer", END)
    
    return graph.compile()
