#version 330 core

out vec4 out_color;

in vec4 vertex_color;

void main() {
    out_color = vertex_color;
}