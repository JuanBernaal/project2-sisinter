# HEIST

A Spanish-language, narrative-heavy text adventure set in Cali at midnight. Infiltrate a bank, juggle stealth, time, and morality, then choose between money (botín) and truth (dossier). Every move can raise the alert. Bernal—your ex-guard partner—guides you on the radio with grounded, in-world hints.

## Overview
- **Genre:** Text adventure (terminal)
- **Language:** Spanish (story, UI, and commands)
- **Core Pillars:** Stealth, time pressure, meaningful choices, and audio-driven atmosphere
- **Endings:** Empty, Captured, Neutral, Clean, Expose
- **Demo:** <https://youtu.be/wThK72CoiBQ?si=WlJ6Zye0Q626PMUI>

## Team Members
- **RUI YU LEI WU**
- **JUAN DAVID BERNAL**

## Features
- **Alert system:** Cameras, patrol timer, wrong codes, and drilling raise alert. Low thresholds on HARD.
- **Camera blackout:** Temporarily disable via Security Room panel or Maintenance fuses (shorter blackout, minor alert).
- **Disguise:** Guard **Uniforme** grants a limited "credibility window."
- **Lockpick durability:** **Ganzúa** breaks after limited uses.
- **Vault entry:** Open silently with the 3-digit code (from notes) or noisily with the **Taladro**.
- **3D Spatial Audio:** Immersive audio system with positional sound effects and ambient environments.
- **Branching endings:** Including an ethical route where you leak the dossier.

## Requirements

### System Requirements
- **Python** 3.8+ (tested with 3.10+)
- **Windows/Linux/macOS** (OpenAL support)

### Audio Dependencies
For the full audio experience:
```bash
pip install PyOpenAL
```

**System Libraries:**
- **Windows:** OpenAL32.dll (usually pre-installed)
- **Linux:** `sudo apt-get install libopenal-dev libopenal1`
- **macOS:** `brew install openal-soft`

## Project Structure
```
project 2 - corrected/
├── game.py              # Main game loop and logic
├── sound.py             # OpenAL 3D audio system
├── sound_adapter.py     # Audio interface layer
├── audio_assets.py      # Audio configuration and parameters
├── world.py             # Game world and mechanics
├── world_map.py         # Room definitions and map builder
├── models.py            # Data structures (Player, Room, Exit)
├── enums.py             # Game enumerations
├── config.py            # Game difficulty settings
└── sounds/              # Audio assets directory
    ├── amb_*.wav        # Ambient sounds
    ├── radio_*.wav      # Radio messages
    ├── *.wav            # Sound effects
    └── ...
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JuanBernaal/project2-sisinter.git
   cd 'project 2 - corrected'
   ```

2. **Install audio dependencies:**
   ```bash
   pip install PyOpenAL
   ```

3. **Verify audio setup (optional):**
   ```bash
   python -c "from sound_adapter import sfx; sfx('pasos.wav'); print('Audio working!')"
   ```

4. **Run the game:**
   ```bash
   python game.py
   ```

## Audio System

The game features a sophisticated 3D audio system:

- **Spatial Audio:** Sounds positioned in 3D space with distance attenuation
- **Ambient Environments:** Each room has unique atmospheric audio
- **Radio Communications:** Contextual messages from Bernal
- **Sound Effects:** Over 35 interactive sound effects

### Audio Configuration
- **File Format:** WAV (PCM 8/16-bit, mono/stereo)
- **Positioning:** 3D coordinates (x, y, z) with gain control
- **Auto-conversion:** Stereo files automatically converted to mono for positioned sounds

## Game Commands

### Movement
- `mover [norte/sur/este/oeste]` - Move between rooms

### Interaction
- `examinar` - Look around current room
- `examinar [objeto]` - Examine specific object
- `recoger [objeto]` - Pick up items
- `usar [objeto]` - Use items (panel, taladro, tarjeta, ganzua, fusibles, uniforme)
- `usar codigo` - Enter vault code

### Information
- `inventario` - Check inventory
- `estado` - Check game status
- `pensar` - Get hints and strategy advice
- `ayuda` - Show command list
- `salir` - Quit game

## Technical Details

### Audio Implementation
The audio system uses OpenAL for 3D spatial audio:
```python
# Example audio call
sfx("pasos.wav")  # Play footsteps
play_ambient("vestibulo")  # Play lobby ambience
```

### Configuration
Game difficulty and audio parameters can be adjusted in:
- `config.py` - Game mechanics settings
- `audio_assets.py` - Audio positioning and volume levels

## Troubleshooting

### Audio Issues
1. **No sound:** Ensure PyOpenAL is installed and OpenAL device is available
2. **Missing files:** Check that all `.wav` files are in the `sounds/` directory
3. **Performance:** Reduce audio quality or disable 3D positioning if needed

### Game Issues
1. **Import errors:** Ensure all Python files are in the same directory
2. **Command not found:** Use Spanish commands (e.g., `mover norte`, not `move north`)

