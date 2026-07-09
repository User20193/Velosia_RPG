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

        level_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'data', 'level_01.json')
        self.entities = DataLoader.load_level(level_path, self.ecs)

    def update(self):
        # 1. Player Input System: modifies velocity based on WASD
        velosia_core.PlayerInputSystem.update(self.ecs, "Player", 5.0)

        # 2. Movement System: applies velocity to transform
        velosia_core.MovementSystem.update(self.ecs)

    def render(self):
        velosia_core.RenderSystem.begin_draw()
        velosia_core.RenderSystem.draw_entities(self.ecs)
        velosia_core.RenderSystem.end_draw()

from Scripts.UI import ParallaxBackground, UIButton

class MainMenuScene(Scene):
    def load(self):
        velosia_core.Logger.info("MainMenuScene: Loading...")

        # Parallax assets are currently deferred.
        res = velosia_core.ResourceManager.get_instance()

        # Load Custom Font (Updated to TTF with Cyrillic support)
        res.load_font("fantasy_font", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'fonts', 'fantasy.ttf'))

        # Setup Parallax system deferred for now
        # self.parallax = ParallaxBackground([...])

        # Setup Buttons (Translated and centered for 1366 resolution)
        self.btn_new_game = UIButton(600, 350, 150, 30, "ИГРАТЬ", "fantasy_font")
        self.btn_settings = UIButton(600, 420, 150, 30, "НАСТРОЙКИ", "fantasy_font")
        self.btn_exit = UIButton(600, 490, 150, 30, "ВЫХОД", "fantasy_font")

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

        # 1. Background (Parallax deferred, Raylib clears screen to black by default)

        # 2. Draw Title (Centered for 1366 width)
        # Using approximation: letters are ~40 pixels wide on average for size 80.
        # "VELOSIA RPG" is 11 chars. 11 * ~40 = 440 width.
        # Center x = (1366 - 440) / 2 = 463
        velosia_core.RenderSystem.draw_text("fantasy_font", "VELOSIA RPG", 463, 100, 80, 4, 255, 215, 0, 255) # Gold tint

        # 3. Draw Buttons
        self.btn_new_game.render()
        self.btn_settings.render()
        self.btn_exit.render()

        velosia_core.RenderSystem.end_draw()
