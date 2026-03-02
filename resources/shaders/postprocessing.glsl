#version 330


in vec2 v_uv;
out vec4 f_color;

uniform sampler2D s_texture;

uniform float u_exposure;
uniform float u_hue;
uniform float u_saturation;
uniform float u_value;


/******************************************************

                Mathematical Constants

 ******************************************************/

#define PI      3.141592653589793238462643383279
#define TAU     6.283185307179586476925286766559
#define INV_PI  0.318309886183790671537767526745 // 1.0 / pi
#define INV_TAU 0.159154943091895335768883763372 // 1.0 / tau

#define GAMMA   0.454545454545454545454545454545 // 1.0 / 2.2
#define GAMMA0  0.416666666666666666666666666667 // 1.0 / 2.4
#define SQRT2   1.414213562373095048801688724209 // sqrt(2.0)


/******************************************************

                    Color Functions

 ******************************************************/
 
/*
    Human eyes don't see each color equally, we are more sensitive
    to some than others.

    Instead of using 1/3 for each channel, we use a weight distribution
    more suitable for our eyes to determine the luminance of a color.

    Weights are taken from https://en.wikipedia.org/wiki/Relative_luminance
*/
float luminance(vec3 color) {
    return dot(color, vec3(0.2125, 0.7154, 0.0721));
}

//
// Linear RGB <-> Nonlinear sRGB conversion functions
//

vec3 linear_to_sRGB(vec3 linear) {
    bvec3 cutoff = lessThan(linear, vec3(0.0031308));
    vec3 higher = vec3(1.055) * pow(linear, vec3(GAMMA0)) - vec3(0.055);
    vec3 lower = linear * vec3(12.92);

    return mix(higher, lower, cutoff);
}

vec3 sRGB_to_linear(vec3 sRGB) {
    bvec3 cutoff = lessThan(sRGB, vec3(0.04045));
    vec3 higher = pow((sRGB + vec3(0.055)) / vec3(1.055), vec3(2.4));
    vec3 lower = sRGB / vec3(12.92);

    return mix(higher, lower, cutoff);
}

vec3 linear_to_sRGB_cheap(vec3 linear) {
    return pow(linear, vec3(GAMMA));
}

vec3 sRGB_to_linear_cheap(vec3 linear) {
    return pow(linear, vec3(2.2));
}

//
// HSV <-> RGB conversions
//

vec3 HSV_to_RGB(vec3 HSV) {
    const vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(HSV.xxx + K.xyz) * 6.0 - K.www);
    return HSV.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), HSV.y);
}

vec3 RGB_to_HSV(vec3 RGB) {
    float Cmax = max(RGB.r, max(RGB.g, RGB.b));
    float Cmin = min(RGB.r, min(RGB.g, RGB.b));
    float delta = Cmax - Cmin;

    vec3 hsv = vec3(0.0, 0.0, Cmax);

    if (Cmax > Cmin) {
        hsv.y = delta / Cmax;

        if (RGB.r == Cmax)
            hsv.x = (RGB.g - RGB.b) / delta;
        else {
            if (RGB.g == Cmax)
                hsv.x = 2.0 + (RGB.b - RGB.r) / delta;
            else
                hsv.x = 4.0 + (RGB.r - RGB.g) / delta;
        }
        hsv.x = fract(hsv.x / 6.0);
    }
    return hsv;
}


/******************************************************

                         Main

 ******************************************************/

void main() {
    // Flip Y for pygame
    vec2 uv = vec2(v_uv.x, 1.0 - v_uv.y);

    vec3 color = texture(s_texture, uv).rgb;

    color *= pow(SQRT2, u_exposure);

    vec3 hsv = RGB_to_HSV(color);

    hsv.x += u_hue;
    hsv.y *= u_saturation;
    hsv.z *= u_value;

    color = HSV_to_RGB(hsv);

    // RGB -> BGR for pygame surface
    f_color = vec4(color.bgr, 1.0);
}