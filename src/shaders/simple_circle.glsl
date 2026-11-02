#version 310 es

in vec2 fragmenttexcoord;

out vec4 color;

layout(std430, binding=1) buffer AudioChunk_buffer {
    highp float volume_level;
    highp float audio_data[AUDIO_SAMPLE_SIZE];
    highp float fft_data[AUDIO_FFT_BINS];
    highp float fft_decay[AUDIO_FFT_BINS];
} AudioChunk;

// Define color palette
vec3 palette[3] = vec3[](
    vec3(BACKGROUND_COLOR),
    vec3(FFT_BAR_COLOR),
    vec3(DECAY_BAR_COLOR)
);

void main () {

    //Normalize fragmenttexcoord to center (0.0, 0.0)
    vec2 uv = fragmenttexcoord.xy - vec2(0.5);

    //Calculate polar coordinates
    float r = length(uv);
    float a = atan(uv.y, uv.x);
    float normalizedAngle = (a / (2.0 * 3.14159265359)) + 0.5;
    float scaledAngle = normalizedAngle * WRAPPING_NUMBER;

    //Remap polar coordinates to [0.0, 1.0] for texture sampling
    float u = abs(fract(scaledAngle) * 2.0 - 1.0);
    float v = r;



    //Calculate bar coordinates
    int array_coord = int((u * AUDIO_FFT_BINS.0) - mod(u * AUDIO_FFT_BINS.0, 1.0));
    float y_coord = v / BAR_HEIGHT_SCALING;

    //Apply bar thresholding
    float fft_intensity = step(y_coord, AudioChunk.fft_data[array_coord]);
    float decay_intensity = step(y_coord - DECAY_BAR_HEIGHT, AudioChunk.fft_decay[array_coord]) * step(AudioChunk.fft_decay[array_coord], y_coord);

    //Calculate final colors
    int color_index = int(mod(fft_intensity + (2.0 * decay_intensity), 3.0)); 
    color = vec4(palette[color_index], 1.0);

}