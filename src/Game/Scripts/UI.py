import velosia_core

class ParallaxBackground:
    def __init__(self, layers_data):
        """
        layers_data is a list of tuples: (texture_id, speed_multiplier)
        e.g., [("bg_sky", 0.1), ("bg_mountains", 0.5), ("bg_trees", 1.0)]
        """
        self.layers = layers_data
        self.scroll_offsets = [0.0 for _ in self.layers]

    def update(self, delta_scroll):
        for i, (_, speed) in enumerate(self.layers):
            self.scroll_offsets[i] -= delta_scroll * speed

            # Reset offset for infinite scrolling
            # Note: For this to be seamless, the texture must be seamless!
            tex = velosia_core.ResourceManager.get_instance()
            # For simplicity, assuming the texture is wide enough (e.g., internal width)
            width = velosia_core.DisplayManager.get_internal_width()

            if self.scroll_offsets[i] <= -width:
                self.scroll_offsets[i] = 0

    def render(self):
        width = velosia_core.DisplayManager.get_internal_width()
        for i, (tex_id, _) in enumerate(self.layers):
            offset = self.scroll_offsets[i]
            # Draw first copy
            velosia_core.RenderSystem.draw_texture(tex_id, offset, 0, 1.0)
            # Draw second copy trailing immediately behind it for the seamless loop
            velosia_core.RenderSystem.draw_texture(tex_id, offset + width, 0, 1.0)

class UIButton:
    def __init__(self, x, y, width, height, text, font_id="default_font"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_id = font_id

        # Colors
        self.normal_color = (150, 150, 150, 255)
        self.hover_color = (200, 200, 200, 255)
        self.text_color = (255, 255, 255, 255)
        self.bg_color = self.normal_color

        self.is_hovered = False

    def update(self):
        mx = velosia_core.Input.get_mouse_x()
        my = velosia_core.Input.get_mouse_y()

        # Check AABB collision with mouse
        if self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height:
            self.is_hovered = True
            self.bg_color = self.hover_color
        else:
            self.is_hovered = False
            self.bg_color = self.normal_color

        return self.is_hovered and velosia_core.Input.is_mouse_button_pressed(velosia_core.MouseButton.LEFT)

    def render(self):
        # We don't have DrawRectangle directly exposed yet for UI,
        # so we'll just draw the text colored based on hover state.
        # In a full UI system we'd draw a button background texture here.
        if self.is_hovered:
            velosia_core.RenderSystem.draw_text(self.font_id, f"> {self.text} <", self.x - 20, self.y, 30, 2, *self.hover_color)
        else:
            velosia_core.RenderSystem.draw_text(self.font_id, self.text, self.x, self.y, 30, 2, *self.normal_color)
