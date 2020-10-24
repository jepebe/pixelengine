#version 330 core
uniform vec4 color = vec4(1, 1, 1, 1);

out vec4 out_color;

in vec4 vertex_color;
in vec2 tex_coord;

uniform sampler2DRect sprite_texture;

void main() {
//    float r = texture(sprite_texture, tex_coord).r;
    float r = texelFetch(sprite_texture, ivec2(tex_coord)).r;
    out_color = color * r;
}