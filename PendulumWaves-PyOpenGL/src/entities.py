import numpy as np
from OpenGL.GL import *
import glm

class Entity:
    def __init__(self):
        self._vbo = GL_NONE
        self._vao = GL_NONE
        self._ebo = GL_NONE
        self._vertex_count = 0
        self._index_count = 0
        self._drawing_mode = GL_TRIANGLES
        self.translation_vector = glm.vec3(0.)
        self.scale_vector = glm.vec3(1.)
        self.transform_matrix = glm.mat4(1.)
        self.color = glm.vec4(1.)
        self.lightened = True

    def scale(self, scaling_factor: glm.vec3()) -> None:
        self.scale_vector = scaling_factor
        self.transform_matrix = glm.scale(glm.translate(glm.mat4(1.), self.translation_vector), self.scale_vector)

    def translate(self, translationDistance: glm.vec3) -> None:
        self.translation_vector = translationDistance
        self.transform_matrix = glm.scale(glm.translate(glm.mat4(1.), self.translation_vector), self.scale_vector)

    def render(self) -> None:
        glBindVertexArray(self._vao)
        if self._index_count == 0:
            glDrawArrays(self._drawing_mode, 0, self._vertex_count)
        else:
            glDrawElements(self._drawing_mode, self._index_count, GL_UNSIGNED_INT, None)
        glBindVertexArray(GL_NONE)

    def renderInstances(self, instanceCount):
        glBindVertexArray(self._vao)
        if self._index_count == 0:
            glDrawArraysInstanced(self._drawing_mode, 0, self._vertex_count, instanceCount)
        else:
            glDrawElementsInstanced(self._drawing_mode, self._index_count, GL_UNSIGNED_INT, None, instanceCount)
        glBindVertexArray(GL_NONE)

    def __del__(self):
        glDeleteBuffers(1, [self._vbo])
        glDeleteBuffers(1, [self._ebo])
        glDeleteVertexArrays(1, [self._vao])


class Cube(Entity):
    def __init__(self):
        super().__init__()
        self.construct_model()

    def construct_model(self):
        self.vertex_count = 24
        self._index_count = 36

        data = [
            # Back face
            0.5, -0.5, -0.5,
            0.0, 0.0, -1.0,
            -0.5, -0.5, -0.5,
            0.0, 0.0, -1.0,
            -0.5, 0.5, -0.5,
            0.0, 0.0, -1.0,
            0.5, 0.5, -0.5,
            0.0, 0.0, -1.0,

            # Right face
            0.5, -0.5, 0.5,
            1.0, 0.0, 0.0,
            0.5, -0.5, -0.5,
            1.0, 0.0, 0.0,
            0.5, 0.5, -0.5,
            1.0, 0.0, 0.0,
            0.5, 0.5, 0.5,
            1.0, 0.0, 0.0,

            # Front face
            -0.5, -0.5, 0.5,
            0.0, 0.0, 1.0,
            0.5, -0.5, 0.5,
            0.0, 0.0, 1.0,
            0.5, 0.5, 0.5,
            0.0, 0.0, 1.0,
            -0.5, 0.5, 0.5,
            0.0, 0.0, 1.0,

            # Left face
            -0.5, -0.5, -0.5,
            -1.0, 0.0, 0.0,
            -0.5, -0.5, 0.5,
            -1.0, 0.0, 0.0,
            -0.5, 0.5, 0.5,
            -1.0, 0.0, 0.0,
            -0.5, 0.5, -0.5,
            -1.0, 0.0, 0.0,

             # Top face
            -0.5, 0.5, 0.5,
            0.0, 1.0, 0.0,
            0.5, 0.5, 0.5,
            0.0, 1.0, 0.0,
            0.5, 0.5, -0.5,
            0.0, 1.0, 0.0,
            -0.5, 0.5, -0.5,
            0.0, 1.0, 0.0,

             # Bottom face
            -0.5, -0.5, -0.5,
            0.0, -1.0, 0.0,
            0.5, -0.5, -0.5,
            0.0, -1.0, 0.0,
            0.5, -0.5, 0.5,
            0.0, -1.0, 0.0,
            -0.5, -0.5, 0.5,
            0.0, -1.0, 0.0
        ]

        indices = []
        for i in range(6):
            for j in range(4):
                indices.append(i * 4 + j)
                if j == 2:
                    indices.append(i * 4 + j)
            indices.append(i * 4)

        data = np.array(data, np.float32)
        indices = np.array(indices, np.uint32)
        self._vbo = glGenBuffers(1)
        self._ebo = glGenBuffers(1)
        self._vao = glGenVertexArrays(1)
        glBindVertexArray(self._vao)
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo)
        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, GL_NONE)
        glBindVertexArray(GL_NONE)

class Sphere(Entity):
    def __init__(self, stack_count: int = 50, sector_count: int = 30):
        super().__init__()
        self.radius = 0.5
        self.vertex_count = (sector_count + 1) * (stack_count + 1)
        self._index_count = ((stack_count - 2) * sector_count * 6) + (6 * sector_count)
        self.drawingMode = GL_TRIANGLES
        self.constructModel(stack_count, sector_count)

    def constructModel(self, stack_count, sector_count):
        len = 1. / self.radius
        vertices = []
        PI = glm.pi()
        sector_step = 2 * PI / sector_count
        stack_step = PI / stack_count
        vertex = glm.vec3(0.)

        # Vertex loading
        for i in range(stack_count + 1):
            stack_angle = PI / 2 - i * stack_step
            xy = self.radius * glm.cos(stack_angle)
            vertex.z = self.radius * glm.sin(stack_angle)
            for j in range(sector_count + 1):
                sector_angle = j * sector_step
                vertex.x = xy * glm.cos(sector_angle)
                vertex.y = xy * glm.sin(sector_angle)
                vertices.append(vertex.x)
                vertices.append(vertex.y)
                vertices.append(vertex.z)

        # Index loading
        indices = []
        for i in range(stack_count):
            k1 = i * (sector_count + 1)
            k2 = k1 + sector_count + 1
            for j in range(sector_count):
                if i != 0:
                    indices.append(k1)
                    indices.append(k2)
                    indices.append(k1 + 1)

                if i != (stack_count - 1):
                    indices.append(k1 + 1)
                    indices.append(k2)
                    indices.append(k2 + 1)
                
                k1 += 1
                k2 += 1
        
        data = []
        for i in range(self.vertex_count):
            data.append(vertices[i*3])
            data.append(vertices[i*3+1])
            data.append(vertices[i*3+2])

            data.append(vertices[i*3] * len)
            data.append(vertices[i*3+1] * len)
            data.append(vertices[i*3+2] * len)

        data = np.array(data, np.float32)
        indices = np.array(indices, np.uint)
        self._vbo = glGenBuffers(1)
        self._ebo = glGenBuffers(1)
        self._vao = glGenVertexArrays(1)
        glBindVertexArray(self._vao)
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo)
        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, GL_NONE)
        glBindVertexArray(GL_NONE)
        
class Line(Entity):
    def __init__(self):
        super().__init__()
        self.construct_model()
        self._vertex_count = 2
        self._index_count = 0
        self._drawing_mode = GL_LINES
        self.starting_coordinate = glm.vec3(-0.5, 0., 0.)
        self.ending_coordinate = glm.vec3(0.5, 0., 0.)
        self.lightened = False

    def construct_model(self):
        data = np.array([-0.5, 0., 0., 0.5, 0., 0.], np.float32)

        self._vbo = glGenBuffers(1)
        self._vao = glGenVertexArrays(1)
        glBindVertexArray(self._vao)
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo)
        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, GL_NONE)
        glBindVertexArray(GL_NONE)



        


        

