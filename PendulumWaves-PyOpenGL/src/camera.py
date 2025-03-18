import glm

class PerspectiveCamera:
    def __init__(self, position: glm.vec3):
        self.position = position
        self.center = glm.vec3(0., 0., 0.)
        self.up = glm.vec3(0., 1., 0.)
        self.near_plane = 0.1
        self.far_plane = 50.
        self.aspect_ratio = 1024. / 769.
        self.fov = 45.
        self._angle = 0.

    def project(self) -> glm.mat4:
        return glm.perspective(self.fov, self.aspect_ratio, self.near_plane, self.far_plane)
        
    def look_at(self) -> glm.mat4:
        return glm.lookAt(self.position, self.center, self.up)

    def rotate_around(self, isLeft: bool, delta_time: float) -> None:
        if isLeft == True:
            delta_time *= -1

        self._angle += delta_time
        if self._angle > 2 * glm.pi():
            self._angle = 0.
        elif self._angle < 0.:
            self._angle += 2 * glm.pi()

        radius = glm.length(self.position - self.center)
        self.position.x = glm.cos(self._angle) * radius
        self.position.z = -glm.sin(self._angle) * radius
