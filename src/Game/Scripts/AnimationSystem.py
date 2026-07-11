import velosia_core
import math

class AnimationState:
    def __init__(self):
        self.frame = 0.0
        self.direction = 0 # 0: Down, 1: Left, 2: Right, 3: Up
        self.frame_speed = 6.0 # frames per second
        self.num_frames = 3

class AnimationSystem:
    def __init__(self):
        # We store python-side animation state per entity
        self.states = {}

    def get_or_create_state(self, entity):
        if entity not in self.states:
            self.states[entity] = AnimationState()
        return self.states[entity]

    def update(self, ecs, entities, delta_time):
        """
        Updates animation state for given entities based on their velocity.
        """
        for entity in entities:
            if not ecs.has_velocity(entity) or not ecs.has_sprite(entity):
                continue

            vel = ecs.get_velocity(entity)
            sprite = ecs.get_sprite(entity)
            state = self.get_or_create_state(entity)

            is_moving = abs(vel.dx) > 0.1 or abs(vel.dy) > 0.1

            if is_moving:
                # Update direction
                if abs(vel.dx) > abs(vel.dy):
                    if vel.dx < 0:
                        state.direction = 1 # Left
                    else:
                        state.direction = 2 # Right
                else:
                    if vel.dy < 0:
                        state.direction = 3 # Up
                    else:
                        state.direction = 0 # Down

                # Update frame
                state.frame += state.frame_speed * delta_time
                if state.frame >= state.num_frames:
                    state.frame = 0.0
            else:
                # If standing still, reset to idle frame (middle frame typically, or frame 1 in a 3-frame 0-indexed where 1 is idle)
                # Actually for pipoya 3-frame: 0 is step, 1 is idle, 2 is step
                state.frame = 1.0

            # Update sprite src_x and src_y
            # Column is integer part of frame
            col = int(state.frame) % state.num_frames
            row = state.direction

            sprite.src_x = int(col * 32)
            sprite.src_y = int(row * 32)
