#version 310 es

in vec2 fragmenttexcoord;

out vec4 color;

layout(std430, binding=1) buffer AudioChunk_buffer {
    highp float volume_level;
    highp float audio_data[1024];
    highp float fft_data[100];
    highp float fft_decay[100];
} AudioChunk;

void main () {
    int array_coord = int((fragmenttexcoord.x * 100.0) - mod(fragmenttexcoord.x * 100.0, 1.0));
    float y_coord = fragmenttexcoord.y * 2.0;

    float fft_intensity = step(y_coord, AudioChunk.fft_data[array_coord]);
    float decay_intensity = step(y_coord - 0.1, AudioChunk.fft_decay[array_coord]) * step(AudioChunk.fft_decay[array_coord], y_coord);

    vec4 fft_out = vec4(1.0) * fft_intensity;
    vec4 decay_out = vec4(1.0, 0.0, 0.0, 1.0) * decay_intensity;
    color = fft_out + decay_out;
}