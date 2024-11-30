import pygame as pg
from camera import Camera
from settings import *
from terrain_gen import get_height  # Ensure get_height is accessible

class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app

        # Calculate initial ground height based on terrain
        ground_y = get_height(position[0], position[1])
        start_position = (position[0], ground_y + PLAYER_HEIGHT_OFFSET, position[1])

        # Pass the adjusted position to the Camera init
        super().__init__(start_position, yaw, pitch)

        # Initialize jumping and physics properties
        self.is_jumping = False
        self.velocity_y = 0
        self.ground_level = ground_y
        self.gravity = 0.8  # Gravity strength
        self.jump_strength = 15  # Jumping strength

    def update(self):
        # Update movement and gravity
        self.apply_gravity()
        self.keyboard_control()
        self.mouse_control()
        super().update()

    def apply_gravity(self):
        """
        Applies gravity and prevents the player from falling through the terrain.
        Ensures smooth vertical movement and height offset above terrain.
        """
        terrain_y = get_height(self.position.x, self.position.z)
        target_height = terrain_y + PLAYER_HEIGHT_OFFSET

        # If the player is above the ground, apply gravity
        if self.position.y > target_height:
            self.velocity_y += self.gravity * self.app.delta_time
            self.position.y -= self.velocity_y * self.app.delta_time

        # If the player is below the ground, smoothly adjust to target height
        elif self.position.y < target_height:
            self.velocity_y = 0  # Reset downward velocity
            self.position.y = target_height  # Correct position smoothly

        else:
            # Reset velocity when on the ground
            self.velocity_y = 0

    def check_ground_collision(self):
        """
        Prevents the player from sinking below the ground while maintaining smooth motion.
        """
        terrain_y = get_height(self.position.x, self.position.z)
        target_height = terrain_y + PLAYER_HEIGHT_OFFSET

        # Adjust position if below ground
        if self.position.y < target_height:
            self.position.y = target_height

    def keyboard_control(self):
        """
        Handles player movement and jumping using keyboard inputs.
        """
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time

        # XZ plane movement controlled by Camera methods
        if key_state[pg.K_w]:
            self.move_forward(vel)
        if key_state[pg.K_s]:
            self.move_back(vel)
        if key_state[pg.K_d]:
            self.move_right(vel)
        if key_state[pg.K_a]:
            self.move_left(vel)

        # Jumping (y-axis) control in Player class
        if key_state[pg.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -self.jump_strength

    def mouse_control(self):
        """
        Rotates the camera based on mouse movement.
        """
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def handle_event(self, event):
        """
        Handles mouse clicks for voxel interaction.
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            voxel_handler = self.app.scene.world.voxel_handler
            if event.button == 1:
                voxel_handler.set_voxel()
            if event.button == 3:
                voxel_handler.switch_mode()
