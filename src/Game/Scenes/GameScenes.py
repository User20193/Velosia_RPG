import os
import sys
import random

# Ensure Python can find local Game modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import velosia_core
from Scripts.SceneManager import Scene
from Scripts.DataLoader import DataLoader
from Scripts.UI import ParallaxBackground, UIButton
from Scripts.LianaSystem import LianaSystem

class GameplayScene(Scene):
    def load(self):
        velosia_core.Logger.info("GameplayScene: Loading...")

        bus = velosia_core.EventBus.get_instance()
        bus.emit("SceneChanged", "Gameplay")

        res = velosia_core.ResourceManager.get_instance()

        # Load the newly generated ARPG textures
        res.load_texture("arpg_tileset", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'textures', 'arpg_tileset.png'))
        res.load_texture("tree_arpg", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'textures', 'tree_arpg.png'))
        res.load_texture("player_arpg", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'textures', 'player_arpg.png'))

        screen_width = velosia_core.DisplayManager.get_internal_width()
        screen_height = velosia_core.DisplayManager.get_internal_height()

        self.tile_scale = 2.0
        self.scaled_tile_size = int(32 * self.tile_scale)

        self.map_width = (int(screen_width * 1.5) // self.scaled_tile_size) + 1
        self.map_height = (int(screen_height * 1.5) // self.scaled_tile_size) + 1

        # Generate Tilemap Data (1D array)
        # Tiles: 1 = Base Grass, 2 = Flower Grass, 3 = Dirt Path
        self.map_data = []
        random.seed(42) # For consistent look during testing

        # Generate a pure grass/flower field without dirt paths
        for y in range(self.map_height):
            for x in range(self.map_width):
                r = random.random()
                if r > 0.95:
                    self.map_data.append(2) # Flower
                else:
                    self.map_data.append(1) # Grass

        # Spawn Player
        self.player_entity = self.ecs.create_entity()
        self.ecs.add_tag(self.player_entity, "Player")
        self.ecs.add_transform(self.player_entity, screen_width / 2, screen_height / 2)
        self.ecs.add_velocity(self.player_entity, 0.0, 0.0)
        self.ecs.add_sprite(self.player_entity, "player_arpg")
        player_sprite = self.ecs.get_sprite(self.player_entity)
        player_sprite.scale = 2.0
        player_sprite.src_width = 32
        player_sprite.src_height = 32
        # Set origin near bottom center so feet are the collision/sorting point
        player_sprite.origin_x = 16.0
        player_sprite.origin_y = 28.0

        # Spawn Trees (Obstacles)
        num_trees = 25
        for _ in range(num_trees):
            tree_ent = self.ecs.create_entity()
            # Random position, but try to avoid the dirt path center
            tx = random.uniform(50, screen_width * 1.5 - 50)
            ty = random.uniform(50, screen_height * 1.5 - 50)

            self.ecs.add_transform(tree_ent, tx, ty)
            self.ecs.add_sprite(tree_ent, "tree_arpg")
            tree_sprite = self.ecs.get_sprite(tree_ent)
            tree_sprite.scale = 2.0
            tree_sprite.src_width = 64
            tree_sprite.src_height = 64
            # Set origin to the base of the trunk for proper Y-sorting
            tree_sprite.origin_x = 32.0
            tree_sprite.origin_y = 56.0

    def update(self):
        # Update player input and velocity (reduced speed for better control)
        velosia_core.PlayerInputSystem.update(self.ecs, "Player", 15.0)
        # Apply velocity to transform
        velosia_core.MovementSystem.update(self.ecs)

    def render(self):
        velosia_core.RenderSystem.begin_draw()

        # Draw the ground using the fast TilemapSystem
        # Tileset has 3 columns (Grass, Flower, Dirt)
        velosia_core.TilemapSystem.draw_map(
            self.map_data,
            self.map_width,
            self.map_height,
            self.scaled_tile_size,
            "arpg_tileset",
            3
        )

        # Draw dynamic entities (Player, Trees) which will be Y-sorted automatically by C++ RenderSystem
        velosia_core.RenderSystem.draw_entities(self.ecs)
        velosia_core.RenderSystem.end_draw()

class MainMenuScene(Scene):
    def load(self):
        velosia_core.Logger.info("MainMenuScene: Loading...")
        res = velosia_core.ResourceManager.get_instance()

        # Load Textures
        res.load_texture("wall_bg", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'textures', 'wall_bg.png'))
        res.load_texture("liana_64", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'textures', 'liana_64.png'))
        res.load_texture("liana_128", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'textures', 'liana_128.png'))
        res.load_texture("liana_256", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'textures', 'liana_256.png'))
        res.load_texture("liana_384", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'textures', 'liana_384.png'))
        res.load_texture("fog", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'textures', 'fog.png'))

        # Load Fonts
        res.load_font("title_font", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'fonts', 'ThaleahFat.ttf'))
        res.load_font("pixel_rus", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'fonts', 'Pixellari.ttf'))

        # Initialize screen dimensions
        screen_width = velosia_core.DisplayManager.get_internal_width()
        screen_height = velosia_core.DisplayManager.get_internal_height()

        self.liana_system = LianaSystem()
        self.liana_entities = []
        self.ui_bg_entities = []

        # EnTT renders based on the reverse of creation order by default for a View.
        # This means entities created LAST are returned FIRST (at the bottom/back).
        # We want: 1. Background Wall (created last)
        #          2. Lianas (created earlier)
        # We'll create Lianas first, so they are returned LAST in view and drawn ON TOP.

        liana_types = [
            ("liana_64", 64),
            ("liana_128", 128),
            ("liana_256", 256),
            ("liana_384", 384)
        ]

        # Spawn Lianas
        num_lianas = 20
        for i in range(num_lianas):
            liana_ent = self.ecs.create_entity()
            x_pos = 10 + i * (screen_width / num_lianas) + random.uniform(-20, 20)

            # Start off the screen top slightly
            self.ecs.add_transform(liana_ent, x_pos, -10)

            l_tex, l_height = random.choice(liana_types)
            self.ecs.add_sprite(liana_ent, l_tex)

            sprite = self.ecs.get_sprite(liana_ent)
            sprite.scale = random.uniform(1.8, 3.5)
            sprite.src_width = 32
            sprite.src_height = l_height

            sprite.origin_x = 16.0
            sprite.origin_y = 0.0

            self.liana_entities.append(liana_ent)

        # Setup ECS Background Entities (Tiling the 32x32 texture)
        # Created last, so they render first.
        tile_scale = 2.0
        scaled_tile_size = int(32 * tile_scale)
        cols = (screen_width // scaled_tile_size) + 1
        rows = (screen_height // scaled_tile_size) + 1

        for r in range(rows):
            for c in range(cols):
                bg_entity = self.ecs.create_entity()
                self.ecs.add_transform(bg_entity, c * scaled_tile_size, r * scaled_tile_size)
                self.ecs.add_sprite(bg_entity, "wall_bg")
                bg_sprite = self.ecs.get_sprite(bg_entity)
                bg_sprite.scale = tile_scale
                bg_sprite.src_width = 32
                bg_sprite.src_height = 32

        # Setup Buttons
        self.btn_new_game = UIButton(600, 350, 150, 30, "ИГРАТЬ", "pixel_rus")
        self.btn_settings = UIButton(600, 420, 150, 30, "НАСТРОЙКИ", "pixel_rus")
        self.btn_exit = UIButton(600, 490, 150, 30, "ВЫХОД", "pixel_rus")

        self.fog_offset_x = 0.0

    def update(self):
        self.liana_system.update_lianas(self.ecs, self.liana_entities)

        self.fog_offset_x += 0.5
        if self.fog_offset_x > 1366:
            self.fog_offset_x = 0.0

        if self.btn_new_game.update():
            self.engine.scene_manager.change_scene(GameplayScene)
        if self.btn_settings.update():
            pass
        if self.btn_exit.update():
            self.engine.running = False

    def render(self):
        velosia_core.RenderSystem.begin_draw()

        # 1. Background (wall) & Lianas
        velosia_core.RenderSystem.draw_entities(self.ecs)

        screen_width = velosia_core.DisplayManager.get_internal_width()
        screen_height = velosia_core.DisplayManager.get_internal_height()

        # 2. Draw Fog at the bottom
        fog_y = screen_height - 256
        velosia_core.RenderSystem.draw_texture("fog", -self.fog_offset_x, fog_y, 1.0)
        velosia_core.RenderSystem.draw_texture("fog", 1366 - self.fog_offset_x, fog_y, 1.0)

        # 3. Draw a very large dark block for UI readability. We use the wall_bg texture to create a semi-transparent panel manually
        # Actually since we don't have Color tint for draw_texture in Python yet (only scale),
        # let's just make sure the UI has an aggressive drop shadow to be perfectly readable over green lianas.

        title_text = "VELOSIA RPG"
        title_font_size = 120
        title_spacing = 5.0
        title_width = velosia_core.RenderSystem.measure_text_width("title_font", title_text, title_font_size, title_spacing)
        center_x = (screen_width - title_width) / 2.0

        # Title Outline/Shadow (Multiple passes for thick outline)
        velosia_core.RenderSystem.draw_text("title_font", title_text, center_x + 4, 80 + 4, title_font_size, title_spacing, 0, 0, 0, 255)
        velosia_core.RenderSystem.draw_text("title_font", title_text, center_x - 4, 80 - 4, title_font_size, title_spacing, 0, 0, 0, 255)
        velosia_core.RenderSystem.draw_text("title_font", title_text, center_x + 4, 80 - 4, title_font_size, title_spacing, 0, 0, 0, 255)
        velosia_core.RenderSystem.draw_text("title_font", title_text, center_x - 4, 80 + 4, title_font_size, title_spacing, 0, 0, 0, 255)

        # Draw Title Main
        velosia_core.RenderSystem.draw_text("title_font", title_text, center_x, 80, title_font_size, title_spacing, 255, 215, 0, 255)

        # 4. Draw Buttons (They will render with standard or hover colors)
        self.btn_new_game.render()
        self.btn_settings.render()
        self.btn_exit.render()

        velosia_core.RenderSystem.end_draw()
