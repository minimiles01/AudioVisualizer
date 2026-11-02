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
    //Calculate bar coordinates
    int array_coord = int((fragmenttexcoord.x * AUDIO_FFT_BINS.0) - mod(fragmenttexcoord.x * AUDIO_FFT_BINS.0, 1.0));
    float y_coord = fragmenttexcoord.y / BAR_HEIGHT_SCALING;

    //Apply bar thresholding
    float fft_intensity = step(y_coord, AudioChunk.fft_data[array_coord]);
    float decay_intensity = step(y_coord - DECAY_BAR_HEIGHT, AudioChunk.fft_decay[array_coord]) * step(AudioChunk.fft_decay[array_coord], y_coord);

    //Calculate final colors
    int color_index = int(mod(fft_intensity + (2.0 * decay_intensity), 3.0)); 
    color = vec4(palette[color_index], 1.0);

}