#version 330 core

flat in vec3 start_pos;
in vec3 vert_pos;
in vec4 vertex_color;

out vec4 out_color;

uniform vec2  resolution;
uniform float dash_size;
uniform float gap_size;

void main() {
    vec2 dir = (vert_pos.xy-start_pos.xy) * resolution / 2.0;
    float dist = length(dir);
    float pattern_length = (dash_size + gap_size);
    if (fract(dist / pattern_length) > dash_size / pattern_length) {
        discard;
    }
    out_color = vertex_color;
}