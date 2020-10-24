#version 330 core

out vec4 out_color;

in vec4 vertex_color;
in vec2 tex_coord;

uniform sampler2DRect sprite_texture;

void main() {
    out_color = vertex_color * texture(sprite_texture, tex_coord);
}