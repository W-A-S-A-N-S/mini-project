import requests
from .models import Game

def get_or_create_game_from_steam(steam_app_id):
    try:
        game = Game.objects.get(steam_app_id=steam_app_id)
        return game
    except Game.DoesNotExist:
        try:
            response = requests.get(f'https://store.steampowered.com/api/appdetails?appids={steam_app_id}')
            response.raise_for_status()
            data = response.json()[str(steam_app_id)]['data']

            # Extract data and create a new game
            game = Game.objects.create(
                name=data.get('name'),
                steam_app_id=steam_app_id,
                description=data.get('short_description'),
                image_url=data.get('header_image'),
                genre=data.get('genres', [{}])[0].get('description', 'other'),
                max_players=4,  # Simplification: default to 4
                min_players=1,  # Simplification: default to 1
            )
            return game
        except (requests.RequestException, KeyError) as e:
            # Handle cases where the game is not found on Steam or other API errors
            return None
