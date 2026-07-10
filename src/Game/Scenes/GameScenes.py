import os
import sys

# Ensure Python can find local Game modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import velosia_core
from Scripts.SceneManager import Scene
from Scripts.DataLoader import DataLoader

class GameplayScene(Scene):
    def load(self):
        velosia_core.Logger.info("GameplayScene: Loading...")

        # We can use the Event Bus to notify UI or Audio systems
        bus = velosia_core.EventBus.get_instance()
        bus.emit("SceneChanged", "Gameplay")

        # We must load the texture into the ResourceManager before Data-loader asks for it!
        img_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'sprites', 'hero.png')
        velosia_core.ResourceManager.get_instance().load_texture("hero_tex", img_path)

        # Load grass tilemap texture
        grass_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'textures', 'grass.png')
        velosia_core.ResourceManager.get_instance().load_texture("grass_tileset", grass_path)

        level_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'data', 'level_01.json')
        self.entities = DataLoader.load_level(level_path, self.ecs)

        # Generate a 20x15 map of grass tiles (id=1)
        self.map_width = 45 # roughly screen width / 32
        self.map_height = 25
        self.tile_size = 32
        # map_data is just a list of 1s
        self.map_data = [1] * (self.map_width * self.map_height)

    def update(self):
        # 1. Player Input System: modifies velocity based on WASD
        velosia_core.PlayerInputSystem.update(self.ecs, "Player", 5.0)

        # 2. Movement System: applies velocity to transform
        velosia_core.MovementSystem.update(self.ecs)

    def render(self):
        velosia_core.RenderSystem.begin_draw()

        # Draw tilemap
        velosia_core.TilemapSystem.draw_map(
            self.map_data,
            self.map_width,
            self.map_height,
            self.tile_size,
            "grass_tileset",
            1 # columns in tileset (it's just a single 32x32 image for now)
        )

        velosia_core.RenderSystem.draw_entities(self.ecs)
        velosia_core.RenderSystem.end_draw()

from Scripts.UI import ParallaxBackground, UIButton

class MainMenuScene(Scene):
    def load(self):
        velosia_core.Logger.info("MainMenuScene: Loading...")

        res = velosia_core.ResourceManager.get_instance()

        # Load static background
        res.load_texture("main_menu_bg", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'textures', 'main_menu_bg.png'))

        # Load Fonts
        res.load_font("fantasy_font", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'fonts', 'fantasy.ttf'))
        # Using ThaleahFat for English title and Pixellari for Cyrillic buttons
        res.load_font("title_font", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'fonts', 'ThaleahFat.ttf'))
        res.load_font("pixel_rus", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'fonts', 'Pixellari.ttf'))

        # Setup Buttons (Translated and centered for 1366 resolution)
        # Assuming the buttons need to be centered, we calculate standard x starting position for ~150 width button
        self.btn_new_game = UIButton(600, 350, 150, 30, "ИГРАТЬ", "pixel_rus")
        self.btn_settings = UIButton(600, 420, 150, 30, "НАСТРОЙКИ", "pixel_rus")
        self.btn_exit = UIButton(600, 490, 150, 30, "ВЫХОД", "pixel_rus")

    def update(self):
        # Parallax update deferred
        # self.parallax.update(1.0) # Delta scroll

        # Check Buttons
        if self.btn_new_game.update():
            self.engine.scene_manager.change_scene(GameplayScene)
        if self.btn_settings.update():
            pass # We don't have a settings scene yet
        if self.btn_exit.update():
            self.engine.running = False # Exit game

    def render(self):
        velosia_core.RenderSystem.begin_draw()

        # 1. Background
        velosia_core.RenderSystem.draw_texture("main_menu_bg", 0, 0, 1.0)

        # 2. Draw Title (Perfectly Centered for 1366 width using C++ Text Measurement)
        title_text = "VELOSIA RPG"
        title_font_size = 120
        title_spacing = 5.0

        title_width = velosia_core.RenderSystem.measure_text_width("title_font", title_text, title_font_size, title_spacing)
        screen_width = velosia_core.DisplayManager.get_internal_width()
        center_x = (screen_width - title_width) / 2.0

        velosia_core.RenderSystem.draw_text("title_font", title_text, center_x, 80, title_font_size, title_spacing, 255, 215, 0, 255) # Gold tint

        # 3. Draw Buttons
        self.btn_new_game.render()
        self.btn_settings.render()
        self.btn_exit.render()

        velosia_core.RenderSystem.end_draw()
