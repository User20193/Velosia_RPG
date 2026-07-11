# Base Scene interface
class Scene:
    def __init__(self, engine):
        self.engine = engine
        self.ecs = engine.ecs # We share the core ECS across scenes, but clear it on transition

    def load(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def unload(self):
        self.ecs.clear()

# The Scene Manager
class SceneManager:
    def __init__(self, engine):
        self.engine = engine
        self.current_scene = None

    def change_scene(self, new_scene_class):
        if self.current_scene:
            self.current_scene.unload()

        self.current_scene = new_scene_class(self.engine)
        self.current_scene.load()

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def render(self):
        if self.current_scene:
            self.current_scene.render()
