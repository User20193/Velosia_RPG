import json
import sys
import os

# Ensure the build directory is in the path so we can import our C++ core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'build'))
import velosia_core

class DataLoader:
    @staticmethod
    def load_level(filepath, ecs_manager):
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Spawn Player
        player_data = data.get("player", {})
        player = ecs_manager.create_entity()
        ecs_manager.add_tag(player, player_data.get("tag", "Player"))
        ecs_manager.add_transform(player, player_data.get("start_x", 0), player_data.get("start_y", 0))
        ecs_manager.add_velocity(player, 0, 0) # Player moves via input

        entities = {"player": player, "enemies": []}

        # Spawn Enemies
        for enemy_data in data.get("enemies", []):
            enemy = ecs_manager.create_entity()
            ecs_manager.add_tag(enemy, enemy_data.get("tag", "Enemy"))
            ecs_manager.add_transform(enemy, enemy_data.get("start_x", 0), enemy_data.get("start_y", 0))
            ecs_manager.add_velocity(enemy, enemy_data.get("speed_x", 0), enemy_data.get("speed_y", 0))
            entities["enemies"].append(enemy)

        velosia_core.Logger.info(f"Loaded level from {filepath} with {len(entities['enemies'])} enemies.")
        return entities
