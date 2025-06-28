class UserPersonalizerAgent:
    def __init__(self, vector_client):
        self.vector_client = vector_client
        
    def run(self, state):
        user_id = state['user_id']
        user_preferences = self._get_user_preferences(user_id)
        
        # Personalize the commentary based on preferences
        if user_preferences.get('favorite_player') in state['players_involved']:
            # Emphasize this player's contribution
            state['commentary'] = self._highlight_player(
                state['commentary'], 
                user_preferences['favorite_player']
            )
            
        # Adjust detail level based on user expertise
        state['commentary'] = self._adjust_detail_level(
            state['commentary'],
            user_preferences.get('expertise_level', 'casual')
        )
        
        return state
