#version 330 core
layout (location=0) in vec3 position;
layout (location=1) in uvec2 tex;

uniform mat4 projection_view;
uniform mat4 model;
uniform mat4 texture_matrix;
uniform vec4 color;

out vec4 vertex_color;
out vec2 tex_coord;

void main() {
    vertex_color = color;
    gl_Position = projection_view * model * vec4(position, 1.0f);
    tex_coord = (texture_matrix * vec4(tex.x, tex.y, 0, 1)).xy;
}