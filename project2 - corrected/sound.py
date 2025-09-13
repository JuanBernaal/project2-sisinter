
import os
import time
import wave
from ctypes import c_uint, c_int, byref
from typing import Tuple, List
from openal import al, alc




def _project_root() -> str:
    return os.path.dirname(os.path.abspath(__file__))

def _candidate_dirs() -> List[str]:
    root = _project_root()
    return [
        os.path.join(root, "sounds"),
        os.path.join(root, "audios"),
        root,
        os.getcwd(),
    ]

def _locate_sound_file(name: str) -> str:
    if os.path.isabs(name) and os.path.exists(name):
        return name
    
    # Lista de nombres a probar
    candidates = [name]
    if not name.endswith('.wav'):
        candidates.append(name + '.wav')
    
    for candidate in candidates:
        for base in _candidate_dirs():
            path = os.path.join(base, candidate)
            if os.path.exists(path):
                return path
    
    tried = []
    for candidate in candidates:
        tried.extend([os.path.join(d, candidate) for d in _candidate_dirs()])
    raise FileNotFoundError(
        f"Audio file not found: {name}\nTried:\n  " + "\n  ".join(tried)
    )

def _al_format(channels: int, bits: int) -> int:
    format_map = {
        (1, 8):  al.AL_FORMAT_MONO8,
        (2, 8):  al.AL_FORMAT_STEREO8,
        (1, 16): al.AL_FORMAT_MONO16,
        (2, 16): al.AL_FORMAT_STEREO16,
    }
    if (channels, bits) not in format_map:
        raise ValueError(
            f"Unsupported WAV format: channels={channels}, bits={bits}. "
            "Use PCM 8/16-bit mono/stereo."
        )
    return format_map[(channels, bits)]

def _stereo_to_mono(wavbuf: bytes, sampwidth: int, channels: int) -> bytes:
    if channels == 1:
        return wavbuf
    
    if channels != 2:
        raise ValueError("Solo se soporta conversión de estéreo (2 canales) a mono")
    
    import struct
    
    if sampwidth == 1:
        samples = struct.unpack(f'{len(wavbuf)}B', wavbuf)
        mono_samples = []
        for i in range(0, len(samples), 2):
            left = samples[i]
            right = samples[i + 1] if i + 1 < len(samples) else left
            avg = (left + right) // 2
            mono_samples.append(avg)
        return struct.pack(f'{len(mono_samples)}B', *mono_samples)
    
    elif sampwidth == 2:
        samples = struct.unpack(f'{len(wavbuf)//2}h', wavbuf)
        mono_samples = []
        for i in range(0, len(samples), 2):
            left = samples[i]
            right = samples[i + 1] if i + 1 < len(samples) else left
            avg = (left + right) // 2
            mono_samples.append(avg)
        return struct.pack(f'{len(mono_samples)}h', *mono_samples)
    
    else:
        raise ValueError(f"Sampwidth {sampwidth} no soportado. Use 1 (8-bit) o 2 (16-bit)")

def _clamp_gain(g: float) -> float:
    return max(0.0, min(1.0, float(g)))




def play_sound_3d(sound_name: str, x: float = 0.0, y: float = 0.0, z: float = 0.0, gain: float = 1.0) -> None:
    fname = _locate_sound_file(sound_name)

    with wave.open(fname, "rb") as wf:
        channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        bits = sampwidth * 8
        samplerate = wf.getframerate()
        frames = wf.getnframes()
        wavbuf = wf.readframes(frames)

    if channels == 2:
        wavbuf = _stereo_to_mono(wavbuf, sampwidth, channels)
        channels = 1

    al_format = _al_format(channels, bits)

    device = alc.alcOpenDevice(None)
    if not device:
        raise RuntimeError("Failed to open OpenAL device.")
    context = alc.alcCreateContext(device, None)
    if not context:
        alc.alcCloseDevice(device)
        raise RuntimeError("Failed to create OpenAL context.")
    alc.alcMakeContextCurrent(context)

    source = c_uint()
    buffer_id = c_uint()

    try:
        al.alListener3f(al.AL_POSITION, 0.0, 0.0, 0.0)
        al.alListener3f(al.AL_VELOCITY, 0.0, 0.0, 0.0)

        al.alGenSources(1, byref(source))
        al.alSourcef(source.value, al.AL_PITCH, 1.0)
        al.alSourcef(source.value, al.AL_GAIN, _clamp_gain(gain))
        al.alSource3f(source.value, al.AL_POSITION, float(x), float(y), float(z))
        al.alSource3f(source.value, al.AL_VELOCITY, 0.0, 0.0, 0.0)
        al.alSourcei(source.value, al.AL_LOOPING, 0)

        al.alGenBuffers(1, byref(buffer_id))
        al.alBufferData(buffer_id.value, al_format, wavbuf, len(wavbuf), samplerate)
        al.alSourcei(source.value, al.AL_BUFFER, int(buffer_id.value))

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
            if buffer_id.value:
                al.alDeleteBuffers(1, byref(buffer_id))
        except Exception:
            pass
        alc.alcMakeContextCurrent(None)
        alc.alcDestroyContext(context)
        alc.alcCloseDevice(device)


def play_sound(sound_name: str, x: float = 0.0, y: float = 0.0, z: float = 0.0, gain: float = 1.0) -> None:
    
    fname = _locate_sound_file(sound_name)

    with wave.open(fname, "rb") as wf:
        channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        bits = sampwidth * 8
        samplerate = wf.getframerate()
        frames = wf.getnframes()
        wavbuf = wf.readframes(frames)

    is_positioned = x != 0.0 or y != 0.0 or z != 0.0
    
    if channels == 2 and is_positioned:
        wavbuf = _stereo_to_mono(wavbuf, sampwidth, channels)
        channels = 1
        

    al_format = _al_format(channels, bits)

    device = alc.alcOpenDevice(None)
    if not device:
        raise RuntimeError("Failed to open OpenAL device.")
    context = alc.alcCreateContext(device, None)
    if not context:
        alc.alcCloseDevice(device)
        raise RuntimeError("Failed to create OpenAL context.")
    alc.alcMakeContextCurrent(context)

    source = c_uint()
    buffer_id = c_uint()

    try:
        al.alListener3f(al.AL_POSITION, 0.0, 0.0, 0.0)
        al.alListener3f(al.AL_VELOCITY, 0.0, 0.0, 0.0)

        al.alGenSources(1, byref(source))
        al.alSourcef(source.value, al.AL_PITCH, 1.0)
        al.alSourcef(source.value, al.AL_GAIN, _clamp_gain(gain))
        al.alSource3f(source.value, al.AL_POSITION, float(x), float(y), float(z))
        al.alSource3f(source.value, al.AL_VELOCITY, 0.0, 0.0, 0.0)
        al.alSourcei(source.value, al.AL_LOOPING, 0)

        al.alGenBuffers(1, byref(buffer_id))
        al.alBufferData(buffer_id.value, al_format, wavbuf, len(wavbuf), samplerate)
        al.alSourcei(source.value, al.AL_BUFFER, int(buffer_id.value))

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
            if buffer_id.value:
                al.alDeleteBuffers(1, byref(buffer_id))
        except Exception:
            pass
        alc.alcMakeContextCurrent(None)
        alc.alcDestroyContext(context)
        alc.alcCloseDevice(device)


