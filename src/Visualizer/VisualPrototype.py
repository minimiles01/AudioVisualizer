from Controller.Handlers import *
from OpenGL.GL import *
import ctypes

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
