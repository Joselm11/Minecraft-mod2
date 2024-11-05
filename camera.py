# camera.py

from settings import *
from frustum import Frustum
import glm

class Camera:
    def __init__(self, position, yaw, pitch):
        # Initialize position and orientation
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        # Define initial orientation vectors
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        # Perspective projection matrix
        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4()

        # Frustum for view culling
        self.frustum = Frustum(self)

    def update(self):
        # Update orientation vectors and view matrix
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        # Set up the view matrix based on position and orientation
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_vectors(self):
        # Update forward, right, and up vectors based on yaw and pitch
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)
        
        # Normalize to ensure consistent movement
        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate_pitch(self, delta_y):
        # Rotate pitch, clamping to prevent over-rotation
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
        # Adjust yaw rotation without clamping
        self.yaw += delta_x

    def move_left(self, velocity):
        # Move left on the x-z plane
        self.position -= self.right * velocity

    def move_right(self, velocity):
        # Move right on the x-z plane
        self.position += self.right * velocity

    def move_forward(self, velocity):
        # Move forward on the x-z plane
        self.position += self.forward * velocity

    def move_back(self, velocity):
        # Move back on the x-z plane
        self.position -= self.forward * velocity
