
//Need to figure out how to configure buffer to pass in data array, may need to use texture
layout(binding=0) buffer AudioChunk_buffer {
    float audio_data
    float fft_data
    float amplitude
    float volume_meter
}AudioChunk ;
