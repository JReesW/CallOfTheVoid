#version 420


in vec2 v_uv;
out vec4 f_color;

layout(binding = 0) uniform sampler2D s_texture;
layout(binding = 1) uniform sampler2D s_prev;


void main() {
    // Flip Y for pygame
    vec2 uv = vec2(v_uv.x, 1.0 - v_uv.y);

    vec4 color_tex = texture(s_texture, uv);
    vec4 color_prev = texture(s_prev, uv);
    vec3 final_color = color_prev.rgb + (color_tex.rgb * color_tex.a);

    // RGB -> BGR for pygame
    f_color = vec4(final_color.bgr, 1.0);
}