#version 310 es

//THIS SHADER SIMPLY PASSES COORDINATES TO THE NEXT SHADER.
//IT'S NEEDED TO SETUP THE SCREEN THAT THE IMAGE IS DISPLAYED ON.

layout (location=0) in vec3 vertexpos;
layout (location=1) in vec2 vertextexcoord;

out vec2 fragmenttexcoord;

void main()
{
    gl_Position = vec4(vertexpos, 1.);
    fragmenttexcoord = vertextexcoord;
}