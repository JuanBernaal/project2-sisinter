from typing import Dict, Optional

from audio_assets import RADIO_SOUNDS, INTERIORS, CAMERA_ZONES
from config import HARD, GameSettings
from enums import ExitType
from models import Room, Player
from sound_adapter import sfx


class GameWorld:
    def __init__(self, rooms: Dict[str, Room], settings: GameSettings = HARD) -> None:
        self.rooms = rooms
        self.settings = settings

        self.vault_code: str = "573"
        self.cameras_disabled: bool = False
        self.alert_level: int = 0
        self.evidence: bool = False
        self.fired_messages: Dict[str, bool] = {}
        self.cams_off_moves_left: Optional[int] = None
        self.keypad_lock_moves: int = 0
        self.pick_uses: Optional[int] = self.settings.PICK_DURABILITY
        self.disguise_moves_left: int = 0
        self.total_moves: int = 0
        self.patrol_active: bool = False

    def describe_objects(self, room: Room) -> None:
        if room.items:
            print(f"Ves: {', '.join(room.items)}.")
            sfx("buscar.wav")
        else:
            print("No parece haber algo útil a la vista.")
            sfx("nada.wav")

    def update_alert_on_move(self, room_key: str) -> None:
        if (not self.cameras_disabled) and (self.disguise_moves_left <= 0) and (room_key in CAMERA_ZONES):
            self.alert_level += self.settings.ALERT_MOVE
            sfx("beep_camara.wav")
            print("Bernal (radio): Cuidado. No hagas mucho ruido aqui.")
        if self.cameras_disabled and self.cams_off_moves_left is not None:
            self.cams_off_moves_left -= 1
            if self.cams_off_moves_left <= 0:
                self.cameras_disabled = False
                self.cams_off_moves_left = None
                print("Las cámaras vuelven a parpadear.")
                sfx("beep_camara.wav")
                print("Bernal (radio): Se acabó el préstamo de oscuridad. De aquí en adelante es pulso.")

    def tick_time(self, inside_bank: bool) -> None:
        self.total_moves += 1
        if not self.patrol_active and self.total_moves >= self.settings.PATROL_START_MOVES:
            self.patrol_active = True
            print("A lo lejos, una patrulla agarra la avenida. No mira, pero aprende.")
            print("Bernal (radio): El tiempo se les puso a favor. Remata lo tuyo.")
        if self.patrol_active and inside_bank:
            self.alert_level += self.settings.PATROL_ALERT_PER_MOVE
            sfx("beep_camara.wav")

    def police_arrives(self) -> bool:
        return self.alert_level >= self.settings.ALERT_THRESHOLD

    def radio_audio(self, key: str) -> None:
        sfx(RADIO_SOUNDS.get(key, "radio_ayuda.wav"))

    def radio_message(self, room_key: str) -> None:
        if self.fired_messages.get(room_key):
            return
        self.fired_messages[room_key] = True

        if room_key == "vestibulo":
            self.radio_audio("vestibulo")
            print("Bernal (radio): Ya estás adentro. Esto no es deporte: nos tumbaron primero. Cae esas cámaras, cada segundo grabado es testigo en tu contra.")
            print("Bernal (radio): Yo fui guardia aquí. Dos ascensos y la pensión en veremos. Hoy se las cobramos.")
        elif room_key == "sala_seguridad":
            if not self.cameras_disabled:
                self.radio_audio("sala_seguridad_on")
                print("Bernal (radio): Ese botón rojo es un milagro, pulsalo nos ayudara mucho.")
                print("Bernal (radio): Cuando caigan las cámaras baja la presión, pero no te confíes: este sitio huele el miedo.")
            else:
                self.radio_audio("sala_seguridad_off")
                print("Bernal (radio): Bien ahí. Quedaron ciegas… por un ratico. Ese silencio nos lo debían. Camina como si trabajaras acá.")
        elif room_key == "oficina_gerente":
            self.radio_audio("oficina_gerente")
            print("Bernal (radio): Molina firmó recortes con mano dura y ojos prestados. Si aparece su tarjeta, úsala contra él.")
            print("Bernal (radio): La primera pista está ahí: el cinco abre y deja gente sin voz.")
        elif room_key == "archivo":
            print("Bernal (radio): Ironico que la sala de archivos legales sea la más oscura, si ves un uniforme no dudes en ponertelo.")
            print("Bernal (radio): Lee lo justo. Cargar papeles en la cabeza también pesa.")
        elif room_key == "pasillo_boveda":
            self.radio_audio("pasillo_boveda")
            print("Bernal (radio): Aquí late el banco. El eco canta más que las cámaras. No hagas mucho ruido aquí.")
        elif room_key == "mantenimiento":
            print("Bernal (radio): Ese tablero es un dios eléctrico. Si lo obedeces, el banco se queda ciego.")
        elif room_key == "antec_boveda":
            self.radio_audio("antec_boveda")
            print("Bernal (radio): Si no es código, es ruido. El taladro abre, pero cobra intereses.")
            print("Bernal (radio): Ya deberías tener los tres números. No es suerte.")
        elif room_key == "boveda":
            self.radio_audio("boveda")
            print("Bernal (radio): Los secretos pesan más que el oro.")
            print("Bernal (radio): Si vas a exponer, no me nombres. A mí me botaron por menos; vos ya estás adentro.")

    def resolve_locked_exit(self, requirement: str, player: Player) -> bool:
        req = requirement.lower()
        if not player.has_item(requirement):
            print(f"Necesitas {requirement}.")
            sfx("puerta_cerrada.wav")
            return False
        if req == "ganzua":
            print("La cerradura aprende a ceder. *clic*")
            sfx("ganzua.wav")
            if self.pick_uses is not None:
                self.pick_uses -= 1
                if self.pick_uses <= 0:
                    print("La ganzúa se parte en el último giro.")
                    player.remove_item_case_insensitive("ganzua")
                    print("Bernal (radio): Se te partió la ganzúa. Sin eso, cada puerta pesa el doble. Calculá.")
        elif req == "tarjeta":
            print("El lector suspira en verde.")
            sfx("card_beep.wav")
        elif req == "llave":
            print("La llave gira con resistencia y cede.")
            sfx("card_beep.wav")
        return True

    def apply_room_entry_effects(self, player: Player) -> None:
        inside = player.location in INTERIORS
        if inside:
            self.radio_message(player.location)

        self.update_alert_on_move(player.location)

        if player.has_loot and player.location in {"vestibulo", "pasillo_boveda"}:
            self.alert_level += self.settings.LOOT_ALERT_NOISE if hasattr(self.settings, "LOOT_ALERT_NOISE") else self.settings.LOOT_NOISE  
        self.tick_time(inside)

from sound_adapter import play_ambient  

class GameWorld(GameWorld):  
    def on_enter_room(self, room: Room) -> None:
        room.describe()
        play_ambient(room.key)
        self.radio_message(room.key)