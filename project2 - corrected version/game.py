from typing import Optional

from audio_assets import INTERIORS
from config import HARD
from enums import ExitType
from models import Player
from sound_adapter import sfx, play_ambient
from world import GameWorld
from world_map import WorldMapBuilder
from sound import play_sound
from audio_assets import (
    RADIO_SOUNDS,
    AMBIENT_BY_ROOM,
    AMBIENT_SOURCE_POS,
    SFX_PARAMS,
    INTERIORS,
    CAMERA_ZONES,
)


class Game:
    def __init__(self) -> None:
        rooms = WorldMapBuilder.build_rooms()
        self.world = GameWorld(rooms, HARD)
        self.player = Player(location="exterior", inventory=["Guantes"])
        self.running: bool = True
        self.vault_open: bool = False
        self.has_entered: bool = False
        self.formally_entered: bool = False


    def intro_context(self) -> None:
        print("Cali. El centro baja las persianas; tú subes el pulso. Te quitaron horas, sueldos y paciencia. Esta noche decides si el banco es una caja o un espejo.")
        print("Regla simple: entra, entiende, elige. El dinero pesa; la verdad, más. No podrás llevarte todo, y tampoco deberías.")
        self.current_room().describe()
        play_ambient(self.player.location)
        print("Escribe 'ayuda' para ver comandos.")

    def current_room(self):
        return self.world.rooms[self.player.location]


    def cmd_move(self, direction: str) -> None:
        room = self.current_room()
        if direction not in room.exits:
            print("No puedes moverte en esa dirección.")
            sfx("error.wav")
            return

        exit_obj = room.exits[direction]

        if exit_obj.exit_type == ExitType.BLOCKED:
            print("Un bloqueo imposible de franquear.")
            sfx("bloqueado.wav")
            return

        if exit_obj.exit_type in {ExitType.LOCKED, ExitType.NEEDS}:
            if not self.world.resolve_locked_exit(exit_obj.requires or "", self.player):
                return

        sfx("pasos.wav")

        if (
            exit_obj.exit_type == ExitType.EVENT
            and self.player.location == "antec_boveda"
            and direction == "norte"
            and not self.vault_open
        ):
            print("La bóveda espera un código o el precio del ruido. Usa 'usar codigo' o 'usar taladro'.")
            sfx("teclado.wav")
            return

        self.player.location = exit_obj.target

        if self.player.location in INTERIORS:
            self.has_entered = True
            self.formally_entered = True

       
        if self.world.keypad_lock_moves > 0:
            self.world.keypad_lock_moves -= 1

        if self.world.disguise_moves_left > 0:
            self.world.disguise_moves_left -= 1
            if self.world.disguise_moves_left == 0:
                print("El uniforme pierde su magia. Vuelves a ser tú.")

        self.world.apply_room_entry_effects(self.player)

       
        self.current_room().describe()
        play_ambient(self.player.location)
        self.world.radio_message(self.player.location)

        if self.world.police_arrives():
            self.ending_police()
            return

        if self.player.location == "exterior" and self.formally_entered:
            self.check_escape()

    def cmd_examine(self, target: Optional[str] = None) -> None:
        room = self.current_room()

        if target is None or target.lower() in {room.key, room.name.lower()}:
            self.world.describe_objects(room)
            return

        obj = target.lower()

        if room.key == "oficina_gerente" and obj == "PapelRojo":
            print('PapelRojo: Primer dígito: 5. "No traigas más dinero sucio a casa". La firma tiembla como quien no quiere volver a firmar jamás.')
            sfx("beep_camara")
        elif room.key == "sala_seguridad" and obj == "PapelVerde":
            print('PapelVerde: Segundo dígito: 7. Nóminas infladas, cámaras nuevas, favores viejos. Al pie: "Calla y piensa en los niños". Lo escribió alguien que ya no duerme.')
            sfx("beep_camara")
        elif room.key == "antec_boveda" and obj == "PapelAzul":
            print('PapelAzul: Tercer dígito: 3. Transferencias que dan vueltas y nunca llegan. "Si cae uno, caen todos"; a veces el miedo es honesto.')
            sfx("beep_camara")
        elif room.key == "archivo" and obj == "PapelNegro":
            print('PapelNegro: "El uniforme compra cinco minutos de fe. Después pregunta quién eres". Hay una firma borrada y un sello mojado.')
            sfx("beep_camara")
        elif room.key in {"antec_boveda", "boveda"} and obj in {"teclado", "codigo", "boveda"}:
            print("Teclado frío. Tres dígitos hacen una llave. Tres errores invitan a cantar sirenas.")
            sfx("teclado")
        elif room.key == "boveda" and obj == "dossier":
            print("Dossier: rutas, nombres, empresas que viven de no mirarte a los ojos. Si esto sale, alguien desayuna justicia.")
            sfx("buscar")
        elif room.key == "sala_seguridad" and obj in {"panel", "panel de control"}:
            print("Panel conmutador: promesa de silencio en un gesto. La fe aquí se mide en voltios.")
            sfx("panel")
        else:
            print("No descubres nada más.")
            sfx("nada")

    def cmd_take(self, item: str) -> None:
        room = self.current_room()
        item_names = [i.lower() for i in room.items]

        if item.lower() not in item_names:
            print("No hay nada con ese nombre aquí.")
            sfx("nada")
            return

        real_name = room.items[item_names.index(item.lower())]
        self.player.inventory.append(real_name)
        room.items.remove(real_name)
        print(f"Recoges {real_name}.")
        sfx("recoger")

        if real_name.lower().startswith("nota"):
            self.player.notes += 1
        if real_name.lower() == "dossier":
            self.world.evidence = True
            print("Bernal (radio): Nombres, rutas, firmas. Con esto el banco deja de ser edificio y se vuelve confesión.")

    def cmd_use(self, obj: str) -> None:
        room = self.current_room()
        name = obj.lower()

        if not self.player.has_item(name):
            if name in {"panel", "panel de control"} and room.key == "sala_seguridad":
                pass
            else:
                print("No llevas eso.")
                sfx("error")
                return

  
        if name in {"panel", "panel de control"} and room.key == "sala_seguridad":
            if not self.world.cameras_disabled:
                self.world.cameras_disabled = True
                self.world.cams_off_moves_left = self.world.settings.CAMS_OFF_MOVES
                print("El murmullo eléctrico se apaga. La mirada del banco, también.")
                sfx("panel")
                sfx("radio_seguridad_off")
            else:
                print("Ya silenciaste las cámaras.")
                sfx("nada")
            return


        if name == "fusibles":
            if room.key == "mantenimiento":
                if not self.world.cameras_disabled:
                    self.world.cameras_disabled = True
                    self.world.cams_off_moves_left = self.world.settings.CAMS_OFF_MOVES_FUSE
                    self.world.alert_level += 1
                    print("Un chasquido y las luces tiemblan. La red parpadea a oscuras.")
                    sfx("panel")
                    print("Bernal (radio): Sombra ganada, tiempo perdido. Muévete pues.")
                else:
                    print("Ya silenciaste las cámaras por otro medio.")
                    sfx("nada")
            else:
                print("Aquí no hay tablero que obedecería.")
                sfx("nada")
            return

     
        if name == "uniforme":
            self.world.disguise_moves_left = self.world.settings.DISGUISE_MOVES
            print("Te ajustas el uniforme: el banco te cree del turno de noche por un rato.")
            sfx("recoger")
            print("Bernal (radio): La pinta también roba. Cruza donde miran.")
            return

        if name == "taladro":
            if room.key == "antec_boveda" and not self.vault_open:
                print("El metal grita. Cada segundo pesa como un delito.")
                sfx("taladro")
                print("Bernal (radio): A mí me botaron por menos. Si eso se oye afuera, aborta sin dudar.")
                self.world.alert_level += self.world.settings.ALERT_DRILL
                if self.world.police_arrives():
                    self.ending_police()
                    return
                self.vault_open = True
                print("Los pernos retroceden. El animal abre el ojo.")
                sfx("puerta_pesada")
                return
            else:
                print("No parece el lugar para taladrar.")
                sfx("nada")
                return

        if name == "tarjeta":
            if room.key in {"exterior", "vestibulo"}:
                print("La tarjeta estará lista cuando pases junto a un lector.")
                sfx("card_beep")
            else:
                print("Aquí no hay dónde pasarla.")
                sfx("nada")
            return

        if name == "ganzua":
            print("Tu mano y la ganzúa ensayan un diálogo viejo con el metal.")
            sfx("ganzua")
            return

        if name == "codigo":
            print("No es un objeto. Júntalo en la cabeza y úsalo frente al teclado.")
            sfx("teclado")
            return

        print("No consigues usarlo aquí.")
        sfx("nada")

    def cmd_use_code(self) -> None:
        room = self.current_room()

        if room.key != "antec_boveda":
            print("Aquí no hay teclado que respondería.")
            sfx("nada")
            return

        if self.world.keypad_lock_moves > 0:
            print(f"El teclado está bloqueado por {self.world.keypad_lock_moves} movimientos.")
            sfx("alarma_soft")
            print("Bernal (radio): Otra no. Cabeza antes que suerte.")
            return

        entry = input("Código de 3 dígitos: ").strip()
        sfx("teclado")

        if entry == self.world.vault_code:
            self.vault_open = True
            print("Un susurro hidráulico concede el paso. La bóveda te cree.")
            sfx("puerta_pesada")
        else:
            print("El pitido muerde. El edificio te huele.")
            sfx("alarma_soft")
            self.world.alert_level += self.world.settings.ALERT_WRONGCODE
            self.world.keypad_lock_moves = self.world.settings.KEYPAD_LOCK_MOVES
            print("Bernal (radio): No fuerces con fe. Si te falta un número, búscalo.")
            if self.world.police_arrives():
                self.ending_police()

    def cmd_inventory(self) -> None:
        if not self.player.inventory:
            print("Inventario vacío.")
        else:
            print("Inventario:", ", ".join(self.player.inventory))

    def cmd_help(self) -> None:
        print("Comandos:\n- 'mover [norte/sur/este/oeste]'\n- 'examinar' o 'examinar [objeto]'\n- 'recoger [objeto]'\n- 'usar [objeto]' (panel, taladro, tarjeta, ganzua, fusibles, uniforme)\n- 'usar codigo'\n- 'inventario'\n- 'estado'\n- 'pensar'\n- 'salir'")
        self.world.radio_audio("ayuda")

    def cmd_status(self) -> None:
        print(
            f"Alerta: {self.world.alert_level}/{self.world.settings.ALERT_THRESHOLD} | Cámaras: "
            f"{'OFF' if self.world.cameras_disabled else 'ON'} | Bóveda abierta: {self.vault_open}"
        )
        if self.world.cameras_disabled and self.world.cams_off_moves_left is not None:
            print(f"Ceguera cámaras: {self.world.cams_off_moves_left} movimientos")
        if self.world.keypad_lock_moves > 0:
            print(f"Teclado bloqueado: {self.world.keypad_lock_moves} movimientos")
        if self.world.disguise_moves_left > 0:
            print(f"Uniforme creíble por: {self.world.disguise_moves_left} movimientos")
        print(
            f"Tiempo: {self.world.total_moves} movimientos | Patrulla: "
            f"{'EN RUTA' if self.world.patrol_active else 'LEJOS'}"
        )
        if self.player.has_loot:
            print("Llevas el botín.")
        if self.world.evidence:
            print("Llevas el dossier.")

    def cmd_think(self) -> None:
        if not self.has_entered:
            print("El banco respira lento. Podrías dar la vuelta y seguir siendo la persona a la que todo se lo deben.")
            return
        if not self.world.cameras_disabled and self.world.disguise_moves_left <= 0:
            print("Cada cámara es un testigo. Apagar ojos no hace justicia, pero te acerca a elegir.")
            return
        if self.player.has_loot and self.world.evidence:
            print("El dinero te saca del hambre. La verdad saca a otros. No caben en la misma mano.")
            return
        if self.player.has_loot:
            print("El peso en la mochila no es solo metal. Asegura salida; decide quién paga mañana.")
            return
        if self.player.notes < 3 and not self.vault_open:
            print("Tres cifras para una puerta; tres cobardías para un sistema. Te falta una.")
            return
        print("El edificio calla. Puede ser complicidad. O bendición.")

    def try_take_loot(self) -> None:
        room = self.current_room()
        if room.key != "boveda":
            print("Aquí no hay botín.")
            sfx("nada")
            return
        if not self.vault_open:
            print("La bóveda sigue cerrada.")
            sfx("puerta_cerrada")
            return
        if self.player.has_loot:
            print("Ya cargas suficiente pecado.")
            sfx("nada")
            return
        print("Llenas la mochila con fajos y metal que no te pertenecen.")
        sfx("bolsa_dinero")
        self.player.has_loot = True
        print("Bernal (radio): Peso rápido. Paga cuentas de hoy, crea preguntas de mañana. Asegura la salida.")


    def check_escape(self) -> None:
        if self.player.location == "exterior" and self.formally_entered:
            if self.player.has_loot:
                self.ending_success()
            else:
                self.ending_empty()

    def ending_police(self) -> None:
        print("\nLas sirenas mastican la avenida. Te parten en luz blanca y manos arriba. El banco guarda tu nombre mejor que tus amigos.")
        sfx("sirena")
        print("FINAL: Capturado. La verdad no salió, el dinero tampoco.")
        self.running = False

    def ending_empty(self) -> None:
        print("\nSales con las manos limpias y vacías. Aprendiste el mapa, no el motivo. La ciudad bosteza y sigue sin ti.")
        sfx("vacio")
        print("FINAL: Vacio. Aprendiste el mapa, no el motivo.")
        self.running = False

    def ending_success(self) -> None:
        if self.world.evidence:
            choice = input("\nTienes botín y el dossier. ¿Qué haces? (huir/exponer): ").strip().lower()
            if choice == "exponer":
                print("\nFiltras el dossier donde duele leerlo. Un par de jubilaciones regresa a manos que tiemblan. Nadie pronuncia tu nombre, pero alguien duerme mejor.")
                self.world.radio_audio("final_etico")
                print("FINAL CORRUPTO: No te hiciste rico. Te hiciste cargo.")
                self.running = False
                return
            else:
                print("\nGuardas el dossier donde nadie lo encuentre. El motor tapa preguntas. Las cifras aprenden a callar.")

        if self.player.notes >= 3 and self.world.alert_level <= 2 and self.world.cameras_disabled:
            print("\nTe diluyes en el tráfico. El banco no recuerda tu cara. Tú recuerdas quién te enseñó a contar.")
            sfx("motor_suave")
            print("FINAL BUENO: Limpio, preciso, casi elegante.")
        elif self.world.alert_level >= 3:
            print("\nMuerdes el volante. Las sirenas pierden interés antes que tú el miedo. No todo cobró hoy, pero cobrará.")
            sfx("motor_apuro")
            print("FINAL NEUTRAL: Escapas con botín, pero la ciudad aprendió tu olor.")
        else:
            print("\nLa noche te acepta sin hacer preguntas. No todas las salidas son una victoria; algunas solo son salida.")
            sfx("motor")
            print("FINAL: Suficiente. Nunca perfecto.")
        self.running = False


    def loop(self) -> None:
        self.intro_context()
        while self.running:
            raw = input("\n¿Qué quieres hacer? ").strip().lower()
            if not raw:
                continue

            parts = raw.split()

            if parts[0] == "mover" and len(parts) == 2:
                self.cmd_move(parts[1])
            elif parts[0] == "examinar":
                if len(parts) == 1:
                    self.cmd_examine()
                else:
                    self.cmd_examine(" ".join(parts[1:]))
            elif parts[0] == "recoger" and len(parts) >= 2:
                self.cmd_take(" ".join(parts[1:]))
            elif parts[0] == "usar" and len(parts) >= 2:
                if parts[1] == "codigo":
                    self.cmd_use_code()
                elif parts[1] in {"botin"}:
                    self.try_take_loot()
                else:
                    self.cmd_use(" ".join(parts[1:]))
            elif parts[0] == "inventario":
                self.cmd_inventory()
            elif parts[0] == "estado":
                self.cmd_status()
            elif parts[0] == "pensar":
                self.cmd_think()
            elif parts[0] == "ayuda":
                self.cmd_help()
            elif parts[0] == "salir":
                print("Apagas la radio. Esta noche termina aquí.")
                sfx("bye")
                break
            else:
                if raw in {"coger botin", "tomar botin", "recoger botin"}:
                    self.try_take_loot()
                else:
                    print("Comando no reconocido. Escribe 'ayuda'.")
                    sfx("error")


if __name__ == "__main__":
    Game().loop()
