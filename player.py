import pygame as pg
from camera import Camera
from settings import *
from terrain_gen import get_height  # Ensure get_height is accessible

class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app

        # Initialize player position to slightly above the ground
        ground_y = get_height(position[0], position[1])
        start_position = (position[0], ground_y + 0.1, position[1])

        super().__init__(start_position, yaw, pitch)

        # Gravity and jump variables
        self.is_jumping = False
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_strength = 15
        self.ground_buffer = 0.05  # Small buffer to prevent sticking

    def update(self):
        self.apply_gravity()
        self.keyboard_control()
        self.mouse_control()
        super().update()

    def apply_gravity(self):
        GRAVITY = 0.8
        # Get the height of the terrain at the current position
        terrain_y = get_height(self.position.x, self.position.z)
        target_height = terrain_y + 2  # Ensuring the player is two blocks above terrain

    # Apply gravity if above the target height
        if self.position.y > target_height:
            self.position.y -= GRAVITY * self.app.delta_time
        else:
        # Snap to the target height if below or on ground
            self.position.y = target_height

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time

        # Movement controls for forward, backward, left, and right
        if key_state[pg.K_w]:
            self.move_forward(vel)
        if key_state[pg.K_s]:
            self.move_back(vel)
        if key_state[pg.K_d]:
            self.move_right(vel)
        if key_state[pg.K_a]:
            self.move_left(vel)
        
        # Jumping control
        if key_state[pg.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -self.jump_strength

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def handle_event(self, event):
        # Handle mouse clicks for voxel interaction
        if event.type == pg.MOUSEBUTTONDOWN:
            voxel_handler = self.app.scene.world.voxel_handler
            if event.button == 1:
                voxel_handler.set_voxel()
            if event.button == 3:
                voxel_handler.switch_mode()
