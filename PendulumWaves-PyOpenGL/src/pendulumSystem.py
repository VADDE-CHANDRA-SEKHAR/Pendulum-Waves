from numpy import number
from shader import Shader
from entities import *
from pendulum import Pendulum
import glm

class PendulumSystem:
    def __init__(self) -> None:
        self.pendulums = []
        pendulum_position_x = 9.
        # The period of one complete cycle of the dance is 60 seconds. 
        # The length of the longest pendulum has been adjusted so that it executes 51 oscillations in this 60 second period. 
        # The length of each successive shorter pendulum is carefully adjusted so that it executes one additional oscillation in this period.
        # Thus, the 15th pendulum (shortest) undergoes 65 oscillations.
        # When all 15 pendulums are started together, they quickly fall out of sync—their relative phases continuously change
        # because of their different periods of oscillation. However, after 60 seconds they will all have executed an integral
        # number of oscillations and be back in sync again at that instant, ready to repeat the dance.
        # T = 2 * pi * sqrt(L / g)
        number_of_oscillations = 51.
        for i in range(10):
            frequency = number_of_oscillations / 80.
            pendulum_string_length = (1. / (4 * glm.pi()**2 * frequency**2)) * 9.81
            self.pendulums.append(Pendulum(glm.vec3(pendulum_position_x, 0., 0.), pendulum_string_length))
            self.pendulums[i].sphere.color = glm.vec4(1., 0.25, 0., 1.)
            pendulum_position_x -= 2.0
            number_of_oscillations += 1

        self.construction_cubes = [Cube() for i in range(5)]
        self.construction_cubes[0].scale(glm.vec3(19., 0.5, 0.5))
        self.construction_cubes[0].color = glm.vec4(0.35, 0.7, 1.0, 0.3)
        self.construction_cubes[1].scale(glm.vec3(0.5, 7., 0.5))
        self.construction_cubes[1].translate(glm.vec3(9.75, -3.25, 0.))
        self.construction_cubes[2].scale(glm.vec3(0.5, 7., 0.5))
        self.construction_cubes[2].translate(glm.vec3(-9.75, -3.25, 0.))
        self.construction_cubes[3].scale(glm.vec3(1., 1., 3.))
        self.construction_cubes[3].translate(glm.vec3(9.75, -7., 0.))
        self.construction_cubes[4].scale(glm.vec3(1., 1., 3.))
        self.construction_cubes[4].translate(glm.vec3(-9.75, -7., 0.))
        
    def draw(self, shader: Shader) -> None:
        shader.use()
        for pendulum in self.pendulums:
            pendulum.draw(shader)

        shader.update_uniform_int("lightened", self.construction_cubes[0].lightened)
        shader.update_uniform_vec4("material.color", self.construction_cubes[0].color)
        for cube in self.construction_cubes:
            shader.update_uniform_mat4("model", cube.transform_matrix)
            cube.render()


    def apply_physics(self, delta_time: float) -> None:
        for pendulum in self.pendulums:
            pendulum.apply_physics(delta_time)
        

        