class HighlightDetectorAgent:
    def __init__(self, threshold=0.8):
        self.excitement_threshold = threshold
        
    def run(self, state):
        # Analyze the current play for highlight potential
        excitement_score = self._calculate_excitement(state['current_play'])
        
        if excitement_score > self.excitement_threshold:
            return {
                "is_highlight": True,
                "highlight_description": self._generate_highlight_description(state),
                "share_suggestion": self._create_share_text(state)
            }
        return {"is_highlight": False}
