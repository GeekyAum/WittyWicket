def parse_match_data(data):
    return {
        'match_title': data.get('title'),
        'current_score': data.get('livescore'),
        'batters': [
            {
                'name': data.get('batterone'),
                'runs': data.get('batsmanonerun'),
                'strike_rate': data.get('batsmanonesr')
            },
            {
                'name': data.get('battertwo'),
                'runs': data.get('batsmantworun'),
                'strike_rate': data.get('batsmantwosr')
            }
        ],
        'bowlers': [
            {
                'name': data.get('bowlerone'),
                'overs': data.get('bowleroneover'),
                'economy': data.get('bowleroneeconomy')
            },
            {
                'name': data.get('bowlertwo'),
                'overs': data.get('bowlertwoover'),
                'economy': data.get('bowlertwoeconomy')
            }
        ]
    }
