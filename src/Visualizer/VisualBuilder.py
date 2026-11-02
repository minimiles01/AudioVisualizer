from Controller.Handlers import *
from Visualizer import VisualPrototype
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

class VisualBuilder:
    def __init__(self):
        InitEvent.publish(status="Initializing", payload="| | |-Initializing VisualBuilder...")

        InitEvent.publish(status="Complete", payload="Done.\n")

    def build(self, shader_source_list, AudioChunk):
        vertex_buffer = self.setup_vertex_buffer()
        audiochunk_buffer = self.setup_audiochunk_buffer(AudioChunk)
        OpenGL_program = self.compile_shaders(shader_source_list)
        VisualProgram = VisualPrototype.VisualPrototype(OpenGL_program, vertex_buffer, audiochunk_buffer)
        return VisualProgram

    def compile_shaders(self, shader_source_list):
        shader_list = []
        for shader_source, shader_type in shader_source_list:
            if shader_type == "VERTEX":
                shader_list.append(compileShader(shader_source, GL_VERTEX_SHADER))
            elif shader_type == "FRAGMENT":
                shader_list.append(compileShader(shader_source, GL_FRAGMENT_SHADER))
        OpenGL_program = compileProgram(*shader_list)
        return OpenGL_program

    def setup_vertex_buffer(self):
        #Vertex array to act as screen
        #x, y, z, texture_x, texture_y    setup 2 triangles to use as screen
        vertices = (
            -1.0, -1.0, 0.0, 0.0, 0.0,
            -1.0, 1.0, 0.0, 0.0, 1.0,
            1.0, -1.0, 0.0, 1.0, 0.0,

            1.0, 1.0, 0.0, 1.0, 1.0,
            -1.0, 1.0, 0.0, 0.0, 1.0,
            1.0, -1.0, 0.0, 1.0, 0.0
        )
        
        vertices = np.array(vertices, dtype=np.float32)
        vertex_array = glGenVertexArrays(1)
        glBindVertexArray(vertex_array)
        
        vertex_buffer = VisualPrototype.VertexBuffer(binding_location=0, data_shape=[[3,20,0],[2,20,12]], data=vertices)
        return vertex_buffer

    def setup_audiochunk_buffer(self, AudioChunk):
        audiochunk_buffer = VisualPrototype.StorageBuffer(binding_location=1, data=AudioChunk)
        return audiochunk_buffer

class VisualSerializer:
    def __init__(self):
        InitEvent.publish(status="Initializing", payload="| | |-Initializing VisualSerializer...")

        InitEvent.publish(status="Complete", payload="Done.\n")

    def load_shaders(self, SHADER_PATHS, keywords):
        shader_source_list = []
        for shader_path in SHADER_PATHS:
            with open(shader_path[0], "r") as shader_file:
                shader_source = shader_file.read()

            for key, value in keywords.items():
                shader_source = shader_source.replace(key, str(value))

            shader_source_list.append((shader_source, shader_path[1]))
        return shader_source_list
