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

        if "texture_id" in player_data:
            ecs_manager.add_sprite(player, player_data["texture_id"])
            sprite = ecs_manager.get_sprite(player)
            sprite.src_width = 32 # Match placeholder asset size
            sprite.src_height = 32
            sprite.scale = 1.0 # Scale down to ~64px

        entities = {"player": player, "enemies": []}

        # Spawn Enemies
        for enemy_data in data.get("enemies", []):
            enemy = ecs_manager.create_entity()
            ecs_manager.add_tag(enemy, enemy_data.get("tag", "Enemy"))
            ecs_manager.add_transform(enemy, enemy_data.get("start_x", 0), enemy_data.get("start_y", 0))
            ecs_manager.add_velocity(enemy, enemy_data.get("speed_x", 0), enemy_data.get("speed_y", 0))

            if "texture_id" in enemy_data:
                ecs_manager.add_sprite(enemy, enemy_data["texture_id"])
                sprite = ecs_manager.get_sprite(enemy)
                sprite.src_width = 32
                sprite.src_height = 32
                sprite.scale = 1.0
                # Tint enemies red to distinguish them from the player
                sprite.tint_g = 100
                sprite.tint_b = 100

            entities["enemies"].append(enemy)

        velosia_core.Logger.info(f"Loaded level from {filepath} with {len(entities['enemies'])} enemies.")
        return entities
