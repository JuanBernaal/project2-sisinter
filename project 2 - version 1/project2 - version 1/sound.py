import os
import sys
import time
import wave
from ctypes import c_uint, c_int, byref
from openal import al, alc

def play_sound(sound, distance):
    fname = os.path.join(os.path.dirname(__file__), sound) if len(sys.argv) < 2 else sys.argv[1]

    with wave.open(fname, "rb") as wavefp:
        channels = wavefp.getnchannels()
        sampwidth = wavefp.getsampwidth()
        bitrate = sampwidth * 8
        samplerate = wavefp.getframerate()
        frames = wavefp.getnframes()
        wavbuf = wavefp.readframes(frames)

    formatmap = {
        (1, 8):  al.AL_FORMAT_MONO8,
        (2, 8):  al.AL_FORMAT_STEREO8,
        (1, 16): al.AL_FORMAT_MONO16,
        (2, 16): al.AL_FORMAT_STEREO16,
    }
    if (channels, bitrate) not in formatmap:
        raise ValueError(f"Unsupported WAV format: channels={channels}, bits={bitrate}. Use PCM 8/16-bit.")
    alformat = formatmap[(channels, bitrate)]

    device = alc.alcOpenDevice(None)
    if not device:
        raise RuntimeError("Failed to open OpenAL device.")
    context = alc.alcCreateContext(device, None)
    if not context:
        alc.alcCloseDevice(device)
        raise RuntimeError("Failed to create OpenAL context.")
    alc.alcMakeContextCurrent(context)

    source = c_uint()
    buf = c_uint()

    try:
        al.alGenSources(1, byref(source))
        al.alSourcef(source.value, al.AL_PITCH, 1.0)
        al.alSourcef(source.value, al.AL_GAIN, 1.0)
        al.alSource3f(source.value, al.AL_POSITION, float(distance), 0.0, 0.0)
        al.alSource3f(source.value, al.AL_VELOCITY, 0.0, 0.0, 0.0)
        al.alSourcei(source.value, al.AL_LOOPING, 0)

        al.alGenBuffers(1, byref(buf))
        al.alBufferData(buf.value, alformat, wavbuf, len(wavbuf), samplerate)
        al.alSourcei(source.value, al.AL_BUFFER, int(buf.value))

        al.alSourcePlay(source.value)

        state = c_int()
        while True:
            al.alGetSourcei(source.value, al.AL_SOURCE_STATE, byref(state))
            if state.value != al.AL_PLAYING:
                break
            time.sleep(0.05)

    finally:
        try:
            al.alSourceStop(source.value)
        except Exception:
            pass
        try:
            if source.value:
                al.alDeleteSources(1, byref(source))
        except Exception:
            pass
        try:
            if buf.value:
                al.alDeleteBuffers(1, byref(buf))
        except Exception:
            pass
        alc.alcMakeContextCurrent(None)
        alc.alcDestroyContext(context)
        alc.alcCloseDevice(device)
