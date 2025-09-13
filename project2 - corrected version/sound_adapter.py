from typing import Optional

try:
    from sound import play_sound, play_sound_3d
except Exception: 
    def play_sound(_name: str, _x: float = 0.0, _y: float = 0.0, _z: float = 0.0, _gain: float = 1.0):
        pass
    def play_sound_3d(_name: str, _x: float = 0.0, _y: float = 0.0, _z: float = 0.0, _gain: float = 1.0):
        pass

from audio_assets import AMBIENT_SOURCE_POS, AMBIENT_BY_ROOM, SFX_PARAMS, FORCE_MONO_SOUNDS


def sfx(name: str, pos: Optional[tuple] = None, gain: Optional[float] = None) -> None:
    params = SFX_PARAMS.get(name)
    if params:
        x, y, z, g = params
    else:
        x, y, z, g = 0.0, 0.0, 0.0, 0.60

    if pos is not None:
        x, y, z = pos
    if gain is not None:
        g = gain

    try:
        if name in FORCE_MONO_SOUNDS:
            play_sound_3d(name, x, y, z, g)
        else:
            play_sound(name, x, y, z, g)
    except Exception:
        pass


def sfx_3d(name: str, pos: Optional[tuple] = None, gain: Optional[float] = None) -> None:
    params = SFX_PARAMS.get(name)
    if params:
        x, y, z, g = params
    else:
        x, y, z, g = 0.0, 0.0, 0.0, 0.60

    if pos is not None:
        x, y, z = pos
    if gain is not None:
        g = gain

    try:
        play_sound_3d(name, x, y, z, g)
    except Exception:
        pass


def play_ambient(room_key: str) -> None:
    amb = AMBIENT_BY_ROOM.get(room_key)
    if not amb:
        return
    x, y, z, g = AMBIENT_SOURCE_POS.get(room_key, (0.0, 0.0, 1.2, 0.50))
    sfx(amb, pos=(x, y, z), gain=g)
