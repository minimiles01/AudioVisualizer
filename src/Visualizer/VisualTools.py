from Controller.Handlers import *
from OpenGL.GL import *
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from dataclasses import astuple

class VisualBuilder:
    def __init__(self, serializer):
        InitEvent.publish(status="Initializing", payload="| | |-Initializing VisualBuilder...")

        self.serializer = serializer

        InitEvent.publish(status="Complete", payload="Done.\n")

    def build(self, shader_paths, AudioChunk, keywords=None):
        try:
            shader_source_list = self.serializer.load_shaders(shader_paths, keywords)
        except Exception as e:
            ErrorEvent.publish(status="VisualProgram_LoadShadersFailed", payload=e)

        try:
            vertex_buffer = self.setup_vertex_buffer()
            audiochunk_buffer = self.setup_audiochunk_buffer(AudioChunk)
            OpenGL_program = self.compile_shaders(shader_source_list)
            VisualProgram = VisualPrototype(OpenGL_program, vertex_buffer, audiochunk_buffer)
            return VisualProgram
        except Exception as e:
            ErrorEvent.publish(status="VisualProgram_BuildFailed", payload=e)

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
        
        vertex_buffer = VertexBuffer(binding_location=0, data_shape=[[3,20,0],[2,20,12]], data=vertices)
        return vertex_buffer

    def setup_audiochunk_buffer(self, AudioChunk):
        audiochunk_buffer = StorageBuffer(binding_location=1, data=AudioChunk)
        return audiochunk_buffer

class VisualSerializer:
    def __init__(self):
        InitEvent.publish(status="Initializing", payload="| | |-Initializing VisualSerializer...")

        InitEvent.publish(status="Complete", payload="Done.\n")

    def load_shaders(self, shader_paths, keywords=None):
        shader_source_list = []
        for shader_path in shader_paths:
            with open(shader_path[0], "r") as shader_file:
                shader_source = shader_file.read()

            if keywords is not None:
                for key, value in keywords.items():
                    shader_source = shader_source.replace(key, value)

            shader_source_list.append((shader_source, shader_path[1]))
        return shader_source_list

class VisualPrototype:
    def __init__(self, OpenGL_Program, vertex_buffer, audiochunk_buffer):
        self.OpenGL_Program = OpenGL_Program
        self.vertex_buffer = vertex_buffer
        self.audiochunk_buffer = audiochunk_buffer

    def delete(self):
        self.vertex_buffer.delete()
        self.audiochunk_buffer.delete()
        glDeleteProgram(self.OpenGL_Program)

    def update_buffer(self, AudioChunk):
        self.audiochunk_buffer.update(AudioChunk)

    def step_VisualProgram(self):
        glClear(GL_COLOR_BUFFER_BIT) #Not sure this is needed here
        glUseProgram(self.OpenGL_Program)
        
        #glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)

class VertexBuffer:
    def __init__(self, binding_location, data_shape, data):
        self.buffer_object = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_object)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        for data_index, shape in enumerate(data_shape):
            glEnableVertexAttribArray(data_index)
            glVertexAttribPointer(binding_location + data_index, shape[0], GL_FLOAT, GL_FALSE, shape[1], ctypes.c_void_p(shape[2]))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    def delete(self):
        #glDeleteTextures(1, (self.buffer_object,))
        glDeleteTextures(1, [self.buffer_object])

class StorageBuffer:
    def __init__(self, binding_location, data):
        self.buffer_object = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.buffer_object)
        glBufferData(GL_SHADER_STORAGE_BUFFER, data.nbytes, data, GL_DYNAMIC_READ)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, binding_location, self.buffer_object)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

    def update(self, data):
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.buffer_object)
        glBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, data.nbytes, data)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

    def delete(self):    
        #glDeleteBuffers(1, (self.buffer_object,))
        glDeleteBuffers(1, [self.buffer_object])