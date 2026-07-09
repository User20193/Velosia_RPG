import os
import velosia_core
from Scripts.SceneManager import Scene
from Scripts.DataLoader import DataLoader

class GameplayScene(Scene):
    def load(self):
        velosia_core.Logger.info("GameplayScene: Loading...")

        # We can use the Event Bus to notify UI or Audio systems
        bus = velosia_core.EventBus.get_instance()
        bus.emit("SceneChanged", "Gameplay")

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

class MainMenuScene(Scene):
    def load(self):
        velosia_core.Logger.info("MainMenuScene: Loading...")
        # Imagine UI buttons created here

    def update(self):
        # In a real game, clicking "Start" would call:
        # self.engine.scene_manager.change_scene(GameplayScene)
        # For our test, we'll auto-transition after 30 frames
        if not hasattr(self, 'frames'): self.frames = 0
        self.frames += 1
        if self.frames > 30:
            self.engine.scene_manager.change_scene(GameplayScene)

    def render(self):
        velosia_core.RenderSystem.begin_draw()
        # Raylib draw text could go here in C++ bindings, for now just clear screen
        velosia_core.RenderSystem.end_draw()
