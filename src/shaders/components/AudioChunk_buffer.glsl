
//Need to figure out how to configure buffer to pass in data array, may need to use texture
layout(std430, binding=1) buffer AudioChunk_buffer {
    highp float volume_level;
    highp float audio_data[1024];
    highp float fft_data[100];
    highp float fft_decay[100];
} AudioChunk;
