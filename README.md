# HEIST

A Spanish-language, narrative-heavy text adventure set in Cali at midnight. Infiltrate a bank, juggle stealth, time, and morality, then choose between money (botín) and truth (dossier). Every move can raise the alert. Bernal—your ex-guard partner—guides you on the radio with grounded, in-world hints.

## Overview
- **Genre:** Text adventure (terminal)
- **Language:** Spanish (story, UI, and commands)
- **Core Pillars:** Stealth, time pressure, meaningful choices, and audio-driven atmosphere
- **Endings:** Empty, Captured, Neutral, Clean, Expose
- [Showcase video (YouTube)](}[https://youtu.be/xn88LEFtiJ4])

## Team Members
- **RUI YU LEI WU**
- **JUAN DAVID BERNAL**

## Features
- **Alert system:** Cameras, patrol timer, wrong codes, and drilling raise alert. Low thresholds on HARD.
- **Camera blackout:** Temporarily disable via Security Room panel or Maintenance fuses (shorter blackout, minor alert).
- **Disguise:** Guard **Uniforme** grants a limited “credibility window.”
- **Lockpick durability:** **Ganzúa** breaks after limited uses.
- **Vault entry:** Open silently with the 3-digit code (from notes) or noisily with the **Taladro**.
- **Branching endings:** Including an ethical route where you leak the dossier.

## Requirements
- **Python** 3.10+
- Optional: OpenAL + WAV assets (mono recommended) for spatial attenuation via `sound.play_sound(name, distance)`

## Setup
1. Clone the repository and place all `.wav` files in the project directory (or adjust paths in `sound.py`).
2. Ensure `sound.py` exposes:
   ```python
   def play_sound(sound: str, distance: int) -> None: ...
