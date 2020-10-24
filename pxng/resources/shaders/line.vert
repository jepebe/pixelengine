#version 330 core
layout (location=0) in vec3 position;

uniform vec4 color;
uniform mat4 projection_view;
uniform mat4 model;

flat out vec3 start_pos;
out vec3 vert_pos;

out vec4 vertex_color;

void main() {
    vertex_color = color;
    vec4 pos = projection_view * model * vec4(position, 1.0f);
    gl_Position = pos;
    vert_pos = pos.xyz / pos.w;
    start_pos = vert_pos;
}