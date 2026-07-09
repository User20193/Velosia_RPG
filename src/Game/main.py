import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'build'))
import velosia_core
from Scripts.SceneManager import SceneManager
from Scenes.GameScenes import MainMenuScene

class Game:
    def __init__(self):
        velosia_core.init()
        velosia_core.RenderSystem.init_window(800, 600, "Velosia RPG")

        self.ecs = velosia_core.ECSManager()
        self.scene_manager = SceneManager(self)
        self.running = True
        self.frames = 0 # For testing

        # Subscribe to a global event just to prove it works
        self.bus = velosia_core.EventBus.get_instance()
        self.bus.subscribe("SceneChanged", self.on_scene_changed)

    def on_scene_changed(self, scene_name):
        velosia_core.Logger.info(f"Global Event Received: Transitioned to {scene_name}")

    def run(self):
        # Start in Main Menu
        self.scene_manager.change_scene(MainMenuScene)

        while self.running:
            if velosia_core.RenderSystem.should_close():
                self.running = False

            self.scene_manager.update()
            self.scene_manager.render()

    def shutdown(self):
        # Take a screenshot to prove it works before closing!
        velosia_core.RenderSystem.take_screenshot("final_screenshot.png")
        velosia_core.Logger.info("Saved final_screenshot.png successfully.")

        self.bus.clear() # Prevent Segfault on exit
        # CRITICAL FIX: Shutdown C++ Core (which unloads VRAM textures) BEFORE destroying the OpenGL context via close_window!
        velosia_core.shutdown()
        velosia_core.RenderSystem.close_window()

if __name__ == "__main__":
    game = Game()
    game.run()
    game.shutdown()
