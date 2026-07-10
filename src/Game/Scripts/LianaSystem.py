import math
import velosia_core

class LianaSystem:
    def __init__(self):
        # Physics constants
        self.interaction_radius = 100.0   # How close the mouse needs to be to affect the liana
        self.max_force = 45.0             # Maximum rotation applied in degrees
        self.spring_constant = 0.05       # How fast it springs back (0.0 to 1.0)
        self.damping = 0.90               # Friction/Damping (0.0 to 1.0)

        # We need to store velocity of rotation for each entity to make it springy
        # dict mapping entity_id -> rotation_velocity
        self.velocities = {}

    def update(self, ecs):
        # Get mouse position
        mx = velosia_core.Input.get_mouse_x()
        my = velosia_core.Input.get_mouse_y()

        # In a real ECS we'd query by Component. Here we query all entities with a "Liana" tag
        # Since our bindings might not have a direct query for "all entities with Tag",
        # let's assume we can loop through a known list of liana entities or we handle it via scene.
        pass

    def update_lianas(self, ecs, liana_entities):
        """
        Takes a list of liana entity IDs and applies pseudo-physics based on mouse position.
        """
        mx = velosia_core.Input.get_mouse_x()
        my = velosia_core.Input.get_mouse_y()

        # Using letterboxed mouse coordinates might be needed depending on internal resolution vs window,
        # but Input.get_mouse_x/y already handles letterboxing scaling based on previous memory if implemented correctly.
        # Wait, the memory says letterbox-aware mouse coordinates from C++ Input system are used.

        for entity in liana_entities:
            transform = ecs.get_transform(entity)
            sprite = ecs.get_sprite(entity)

            if transform is None or sprite is None:
                continue

            if entity not in self.velocities:
                self.velocities[entity] = 0.0

            # Liana base position (where it hangs from)
            # Assuming origin is set to top-center in MainMenuScene
            liana_x = transform.x
            liana_y = transform.y

            # Approximate the center of mass of the liana for interaction
            # (a bit lower than the origin so brushing the bottom affects it more)
            center_mass_y = liana_y + (sprite.src_height * sprite.scale) / 2.0

            dist_x = mx - liana_x
            dist_y = my - center_mass_y
            distance = math.sqrt(dist_x**2 + dist_y**2)

            target_rotation = 0.0

            if distance < self.interaction_radius:
                # Calculate how strong the push is (closer = stronger)
                force_factor = 1.0 - (distance / self.interaction_radius)

                # Push direction based on mouse X relative to liana X
                # If mouse is on the left (dist_x < 0), push right (positive rotation)
                direction = -1 if dist_x > 0 else 1

                target_rotation = self.max_force * force_factor * direction

            # Spring physics calculation
            # Force pulling back to target_rotation
            spring_force = (target_rotation - sprite.rotation) * self.spring_constant

            self.velocities[entity] += spring_force
            self.velocities[entity] *= self.damping

            sprite.rotation += self.velocities[entity]
