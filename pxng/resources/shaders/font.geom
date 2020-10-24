#version 330 core
layout (points) in;
layout (triangle_strip, max_vertices=4) out;

uniform mat4 projection_view;
uniform mat4 model;
uniform int font_size = 8;

in ivec2 char_tex[];
out vec2 tex_coord;

void main() {
    mat4 transform = projection_view * model;
    vec4 pos = gl_in[0].gl_Position;

    gl_Position = transform  * (pos + vec4(0, 0, 0, 0));
    tex_coord = char_tex[0] + ivec2(0, 0);
    EmitVertex();

    gl_Position = transform * (pos + vec4(font_size, 0, 0, 0));
    tex_coord = char_tex[0] + ivec2(font_size, 0);
    EmitVertex();

    gl_Position = transform * (pos + vec4(0, font_size, 0, 0));
    tex_coord = char_tex[0] + ivec2(0, font_size);
    EmitVertex();

    gl_Position = transform * (pos + vec4(font_size, font_size, 0, 0));
    tex_coord = char_tex[0] + ivec2(font_size, font_size);
    EmitVertex();

    EndPrimitive();
}