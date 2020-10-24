#version 330 core
layout (location=0) in vec3 position;
layout (location=1) in vec4 color;

uniform mat4 projection_view;

out vec4 vertex_color;

void main() {
    vertex_color = color;
    gl_Position = projection_view * vec4(position, 1.0f);
}