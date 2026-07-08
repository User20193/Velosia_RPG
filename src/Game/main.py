import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'build'))
import velosia_core
from Scripts.DataLoader import DataLoader

class Game:
    def __init__(self):
        velosia_core.init()
        velosia_core.RenderSystem.init_window(800, 600, "Velosia RPG")
        self.ecs = velosia_core.ECSManager()
        self.running = True

    def load_content(self):
        # Data-driven level loading
        level_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'data', 'level_01.json')
        self.entities = DataLoader.load_level(level_path, self.ecs)

    def process_input(self):
        # Here we would normally read keyboard input.
        # For this milestone, the core physics simulation runs automatically.
        if velosia_core.RenderSystem.should_close():
            self.running = False

    def update(self):
        # Simple AI / Physics update script running on Python using C++ ECS data
        for enemy in self.entities["enemies"]:
            transform = self.ecs.get_transform(enemy)
            velocity = self.ecs.get_velocity(enemy)

            transform.x += velocity.dx
            transform.y += velocity.dy

            # Bounce logic
            if transform.x > 800 or transform.x < 0: velocity.dx *= -1
            if transform.y > 600 or transform.y < 0: velocity.dy *= -1

    def render(self):
        velosia_core.RenderSystem.begin_draw()
        velosia_core.RenderSystem.draw_entities(self.ecs)
        velosia_core.RenderSystem.end_draw()

    def run(self):
        self.load_content()
        # In a real scenario we use while self.running:
        # We will run 60 frames for testing
        for _ in range(60):
            self.process_input()
            if not self.running: break
            self.update()
            self.render()

    def shutdown(self):
        velosia_core.RenderSystem.close_window()
        velosia_core.shutdown()

if __name__ == "__main__":
    game = Game()
    game.run()
    game.shutdown()
