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

        # Load Parallax assets
        res = velosia_core.ResourceManager.get_instance()
        res.load_texture("bg_layer1", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'ui', 'parallax', 'layer1.png'))
        res.load_texture("bg_layer2", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'ui', 'parallax', 'layer2.png'))
        res.load_texture("bg_layer3", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'ui', 'parallax', 'layer3.png'))

        # Load Custom Font
        res.load_font("fantasy_font", os.path.join(os.path.dirname(__file__), '..', '..', '..', 'assets', 'fonts', 'custom_alagard.png'))

        # Setup Parallax system
        self.parallax = ParallaxBackground([
            ("bg_layer1", 0.2), # Slowest (Sky)
            ("bg_layer2", 0.5), # Mid
            ("bg_layer3", 1.0)  # Fastest (Foreground)
        ])

        # Setup Buttons
        self.btn_new_game = UIButton(250, 180, 150, 30, "NEW GAME", "fantasy_font")
        self.btn_settings = UIButton(250, 230, 150, 30, "SETTINGS", "fantasy_font")
        self.btn_exit = UIButton(250, 280, 150, 30, "EXIT", "fantasy_font")

    def update(self):
        # Update parallax
        self.parallax.update(1.0) # Delta scroll

        # Check Buttons
        if self.btn_new_game.update():
            self.engine.scene_manager.change_scene(GameplayScene)
        if self.btn_settings.update():
            pass # We don't have a settings scene yet
        if self.btn_exit.update():
            self.engine.running = False # Exit game

    def render(self):
        velosia_core.RenderSystem.begin_draw()

        # 1. Draw Background
        self.parallax.render()

        # 2. Draw Title
        velosia_core.RenderSystem.draw_text("fantasy_font", "VELOSIA RPG", 150, 50, 60, 4, 255, 215, 0, 255) # Gold tint

        # 3. Draw Buttons
        self.btn_new_game.render()
        self.btn_settings.render()
        self.btn_exit.render()

        velosia_core.RenderSystem.end_draw()
