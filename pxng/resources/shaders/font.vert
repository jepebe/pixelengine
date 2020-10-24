#version 330 core
layout (location=0) in vec3 position;
layout (location=1) in uint character;

uniform mat4 projection_view;
uniform mat4 model;
uniform uint grid_width = 16u;

out ivec2 char_tex;

void main() {
    gl_Position = vec4(position, 1.0f);
    ivec2 xy = ivec2(character % grid_width, character / grid_width - 2u);
    char_tex = xy * 8;
}