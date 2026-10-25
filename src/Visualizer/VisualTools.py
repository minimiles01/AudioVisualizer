from Controller.Handlers import *
from OpenGL.GL import *
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
import json
import numpy as np

class VisualBuilder:
    def __init__(self, serializer):
        InitEvent.publish(status="Initializing", payload="| | |-Initializing VisualBuilder...")

        self.serializer = serializer

        InitEvent.publish(status="Complete", payload="Done.\n")

    def build(self, recipe_path, keywords=None):
        try:
            recipe = self.serializer.load_recipe(recipe_path)
            shader_source_list = self.serializer.parse_recipe(recipe, keywords)
        except Exception as e:
            ErrorEvent.publish(status="VisualProgram_RecipeLoadingFailed", payload=e)

        try:
            VisualProgram = self.compile_shaders(shader_source_list)    
            self.setup_vertices()
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
        VisualProgram = VisualPrototype(OpenGL_program)
        return VisualProgram

    def setup_vertices(self):
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

        """
        #Create VAO (Vertex Array Object) and VBO (Vertex Buffer Object)
        self.VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)
        
        glBindVertexArray(self.VAO)

        # Bind and upload vertex data to GPU
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Position Attribute Pointer (location = 0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Color Attribute Pointer (location = 1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        # Unbind for safety
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        #"""
    
class VisualSerializer:
    def __init__(self):
        InitEvent.publish(status="Initializing", payload="| | |-Initializing VisualSerializer...")

        InitEvent.publish(status="Complete", payload="Done.\n")

    def load_recipe(self, recipe_path):
            with open(recipe_path, "r") as recipe_file:
                recipe = json.load(recipe_file)
            return recipe
    
    def parse_recipe(self, recipe, keywords=None):
        shader_source_list = []
        for shader in recipe:
            component_list = []
            for component in shader["COMPONENTS"]:
                if component["SOURCE_TYPE"] == "STRING":
                    component_list.append(component["SOURCE"])

                elif component["SOURCE_TYPE"] == "FILE":
                    with open(component["SOURCE"], "r") as component_file:
                        component_source = "".join(component_file.readlines())
                        component_list.append(component_source)

            shader_source = "\n".join(component_list)

            if keywords is not None:
                for key, value in keywords.items():
                    shader_source = shader_source.replace(key, value)

            shader_source_list.append((shader_source, shader["TYPE"]))
                
        return shader_source_list

class VisualPrototype:
    def __init__(self, OpenGL_Program):
        self.OpenGL_Program = OpenGL_Program

    def delete(self):
        glDeleteProgram(self.OpenGL_Program)

    def update_buffer(self, AudioChunk):
        pass

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
