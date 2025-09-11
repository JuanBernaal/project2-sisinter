from dataclasses import dataclass, field
from typing import Dict, List, Optional

try:
    from sound import play_sound
except Exception:
    def play_sound(_name: str, _distance: int = 0):
        pass

SFX_DEFAULTS: Dict[str, int] = {
    "intro.wav": 2,
    "beep_camara.wav": 6,
    "buscar.wav": 2,
    "nada.wav": 2,
    "bloqueado.wav": 4,
    "puerta_cerrada.wav": 3,
    "ganzua.wav": 2,
    "card_beep.wav": 2,
    "teclado.wav": 3,
    "nota.wav": 2,
    "panel.wav": 2,
    "taladro.wav": 7,
    "puerta_pesada.wav": 3,
    "alarma_soft.wav": 5,
    "recoger.wav": 1,
    "sirena.wav": 8,
    "vacio.wav": 4,
    "motor_suave.wav": 4,
    "motor_apuro.wav": 6,
    "motor.wav": 5,
    "bolsa_dinero.wav": 3,
    "bye.wav": 2,
    "error.wav": 3,
    "pasos.wav": 1,
    "amb_calle.wav": 4,
    "amb_callejon.wav": 6,
    "amb_escalera.wav": 5,
    "amb_marmol.wav": 4,
    "amb_oficina.wav": 4,
    "amb_servidores.wav": 5,
    "amb_pasillo.wav": 4,
    "amb_antec.wav": 4,
    "amb_boveda.wav": 4,
    "radio_vestibulo.wav": 2,
    "radio_seguridad_on.wav": 2,
    "radio_seguridad_off.wav": 2,
    "radio_oficina.wav": 2,
    "radio_pasillo.wav": 2,
    "radio_antec.wav": 2,
    "radio_boveda.wav": 2,
    "radio_ayuda.wav": 2,
    "radio_exponer.wav": 2,
}

RADIO_SOUNDS: Dict[str, str] = {
    "vestibulo": "radio_vestibulo.wav",
    "sala_seguridad_on": "radio_seguridad_on.wav",
    "sala_seguridad_off": "radio_seguridad_off.wav",
    "oficina_gerente": "radio_oficina.wav",
    "pasillo_boveda": "radio_pasillo.wav",
    "antec_boveda": "radio_antec.wav",
    "boveda": "radio_boveda.wav",
    "ayuda": "radio_ayuda.wav",
    "final_etico": "radio_exponer.wav",
}

AMBIENT_BY_ROOM: Dict[str, str] = {
    "exterior": "amb_calle.wav",
    "callejon": "amb_callejon.wav",
    "escalera": "amb_escalera.wav",
    "vestibulo": "amb_marmol.wav",
    "oficina_gerente": "amb_oficina.wav",
    "sala_seguridad": "amb_servidores.wav",
    "pasillo_boveda": "amb_pasillo.wav",
    "antec_boveda": "amb_antec.wav",
    "boveda": "amb_boveda.wav",
    "archivo": "amb_oficina.wav",
    "mantenimiento": "amb_servidores.wav",
}

INTERIORS = {
    "vestibulo",
    "oficina_gerente",
    "archivo",
    "sala_seguridad",
    "pasillo_boveda",
    "mantenimiento",
    "antec_boveda",
    "boveda",
}
CAMERA_ZONES = {"vestibulo", "pasillo_boveda"}


def sfx(name: str, distance: Optional[int] = None) -> None:
    dist = SFX_DEFAULTS.get(name, 3) if distance is None else distance
    try:
        play_sound(name, dist)
    except Exception:
        pass


def play_ambient(room_key: str) -> None:
    amb = AMBIENT_BY_ROOM.get(room_key)
    if amb:
        sfx(amb)



DIFFICULTY = "HARD"
CFG = {
    "HARD": {
        "ALERT_THRESHOLD": 4,
        "ALERT_MOVE": 2,
        "ALERT_DRILL": 4,
        "ALERT_WRONGCODE": 3,
        "CAMS_OFF_MOVES": 8,
        "CAMS_OFF_MOVES_FUSE": 5,
        "KEYPAD_LOCK_MOVES": 3,
        "PICK_DURABILITY": 3,
        "LOOT_NOISE": 1,
        "DISGUISE_MOVES": 6,
        "PATROL_START_MOVES": 12,
        "PATROL_ALERT_PER_MOVE": 1,
    },
}


EXIT_BLOCKED = 0
EXIT_FREE = 1
EXIT_NEEDS = 2
EXIT_EVENT = 3
EXIT_LOCKED = 4



@dataclass
class Exit:
    target: str
    exit_type: int = EXIT_FREE
    requires: Optional[str] = None


@dataclass
class Room:
    key: str
    name: str
    short_desc: str
    long_desc: str
    exits: Dict[str, "Exit"] = field(default_factory=dict)
    items: List[str] = field(default_factory=list)
    visited: bool = False

    def describe(self) -> None:
        print(self.long_desc if not self.visited else self.short_desc)
        self.visited = True


@dataclass
class Player:
    location: str
    inventory: List[str] = field(default_factory=list)
    notes: int = 0
    has_loot: bool = False

    def has_item(self, item: str) -> bool:
        return any(i.lower() == item.lower() for i in self.inventory)


class World:
    def __init__(self) -> None:
        self.rooms: Dict[str, Room] = {}
        self.vault_code: str = "573"
        self.cameras_disabled: bool = False
        self.alert_level: int = 0
        self.evidence: bool = False
        self.fired_messages: Dict[str, bool] = {}
        self.cfg = CFG[DIFFICULTY]
        self.cams_off_moves_left: Optional[int] = None
        self.keypad_lock_moves: int = 0
        self.pick_uses: Optional[int] = self.cfg["PICK_DURABILITY"]
        self.disguise_moves_left: int = 0
        self.total_moves: int = 0
        self.patrol_active: bool = False
        self._build_map()

    def _build_map(self) -> None:
        self.rooms["exterior"] = Room(
            "exterior",
            "Calle Oscura",
            "Calle desierta frente al banco. Norte: entrada. Oeste: callejón. Este: escalera de emergencia.",
            "Cali. Medianoche sin testigos. El banco respira con aire prestado: de día vende seguridad; de noche guarda silencios. No viniste por gloria: viniste a cobrar lo que nunca pagaron. Esta noche el banco será caja o espejo.",
        )
        self.rooms["callejon"] = Room(
            "callejon",
            "Callejón",
            "Callejón húmedo; una mochila espera tras palés.",
            "El callejón huele a lluvia vieja y neón cansado. Tras los palés, tu mochila reposa como un perro que recuerda tu silbido. Dentro, una ganzúa bruñida por trabajos cortos y promesas largas.",
            items=["Ganzua"],
        )
        self.rooms["escalera"] = Room(
            "escalera",
            "Escalera de Emergencia",
            "Escalera metálica hacia una puerta de servicio.",
            "La baranda está fría como un recibo vencido. La pintura descascarada dejó al descubierto años de alarmas que sonaron para nadie. Debajo de un extintor asoma una llave con esmalte pelado.",
            items=["Llave"],
        )
        self.rooms["vestibulo"] = Room(
            "vestibulo",
            "Vestíbulo",
            "Mármol silencioso y cámaras con sueño ligero.",
            "El mármol guarda huellas invisibles: zapatos caros, risas cuidadas, blindajes recién pagados. Sobre ti, ojos de vidrio que jamás parpadean por compasión. El eco aquí devuelve decisiones.",
        )
        self.rooms["oficina_gerente"] = Room(
            "oficina_gerente",
            "Oficina del Gerente",
            "Despacho pulcro; un cajón forzado delata prisa.",
            "Madera encerada y ascensos heredados. La foto de familia, boca abajo; un naufragio voluntario. El cajón cede: una tarjeta tibia y papeles que no saben mentir tanto.",
            items=["Tarjeta", "Nota1"],
        )
        self.rooms["archivo"] = Room(
            "archivo",
            "Archivo Legal",
            "Anaqueles oprimidos por carpetas sin verano.",
            "Papeles que pesan más que lingotes. Huele a tinta húmeda y aire acondicionado cansado. Entre legajos se esconde un uniforme de vigilancia doblado con pudor y una nota que nadie debía leer.",
            items=["Uniforme", "Nota4"],
        )
        self.rooms["sala_seguridad"] = Room(
            "sala_seguridad",
            "Sala de Seguridad",
            "Monitores verdes y un botón que promete silencio.",
            "Un enjambre de pantallas dibuja turnos mal pagados. El café seco es una guardia que envejeció en la taza. Un botón rojo espera fe; al oprimirlo, la ciudad queda ciega, pero no inocente.",
            items=["Nota2"],
        )
        self.rooms["pasillo_boveda"] = Room(
            "pasillo_boveda",
            "Pasillo hacia la Bóveda",
            "Pasillo reforzado; el aire suena a metal dormido.",
            "Las paredes conservan golpes que nunca se denunciaron. El aire vibra grave, como si el banco roncara. Nadie canta aquí; los secretos no llevan melodía.",
        )
        self.rooms["mantenimiento"] = Room(
            "mantenimiento",
            "Cuarto de Mantenimiento",
            "Paneles, fusibles y olor a ozono barato.",
            "Cables sin poesía y etiquetas a medio despegar. Un tablero general prometiendo milagros técnicos y factura en la alerta.",
            items=["Fusibles"],
        )
        self.rooms["antec_boveda"] = Room(
            "antec_boveda",
            "Antesala de la Bóveda",
            "Carros de valores y herramientas bajo una lona.",
            "Luz oblicua y polvo suspendido. Un carrito dejó surcos que cuentan mejor la historia que cualquier informe. Bajo la lona, un taladro impaciente; entre papeles, la última pieza del número que no quiere olvidarse.",
            items=["Taladro", "Nota3"],
        )
        self.rooms["boveda"] = Room(
            "boveda",
            "Bóveda",
            "El halo frío del dinero que no toca el sol.",
            "La puerta es un eclipse detenido. Dentro, fajos, lingotes y un archivador sin rótulo oficial. Hay botín; también hay un dossier con nombres y rutas que pesan distinto.",
            items=["Dossier"],
        )

        self.rooms["exterior"].exits = {
            "norte": Exit("vestibulo", EXIT_LOCKED, "Tarjeta"),
            "oeste": Exit("callejon", EXIT_FREE),
            "este": Exit("escalera", EXIT_FREE),
        }
        self.rooms["callejon"].exits = {
            "este": Exit("exterior", EXIT_FREE),
            "norte": Exit("vestibulo", EXIT_LOCKED, "Ganzua"),
        }
        self.rooms["escalera"].exits = {
            "oeste": Exit("exterior", EXIT_FREE),
            "norte": Exit("vestibulo", EXIT_LOCKED, "Ganzua"),
        }
        self.rooms["vestibulo"].exits = {
            "sur": Exit("exterior", EXIT_FREE),
            "este": Exit("oficina_gerente", EXIT_LOCKED, "Ganzua"),
            "oeste": Exit("sala_seguridad", EXIT_FREE),
            "norte": Exit("pasillo_boveda", EXIT_NEEDS, "Tarjeta"),
        }
        self.rooms["oficina_gerente"].exits = {
            "oeste": Exit("vestibulo", EXIT_FREE),
            "norte": Exit("archivo", EXIT_LOCKED, "Llave"),
        }
        self.rooms["archivo"].exits = {"sur": Exit("oficina_gerente", EXIT_FREE)}
        self.rooms["sala_seguridad"].exits = {"este": Exit("vestibulo", EXIT_FREE)}
        self.rooms["pasillo_boveda"].exits = {
            "sur": Exit("vestibulo", EXIT_FREE),
            "norte": Exit("antec_boveda", EXIT_FREE),
            "oeste": Exit("mantenimiento", EXIT_FREE),
        }
        self.rooms["mantenimiento"].exits = {"este": Exit("pasillo_boveda", EXIT_FREE)}
        self.rooms["antec_boveda"].exits = {
            "sur": Exit("pasillo_boveda", EXIT_FREE),
            "norte": Exit("boveda", EXIT_EVENT),
        }
        self.rooms["boveda"].exits = {"sur": Exit("antec_boveda", EXIT_FREE)}

    def describe_objects(self, room: Room) -> None:
        if room.items:
            print(f"Ves: {', '.join(room.items)}.")
            sfx("buscar.wav")
        else:
            print("No parece haber algo útil a la vista.")
            sfx("nada.wav")

    def update_alert_on_move(self, room_key: str) -> None:
        if not self.cameras_disabled and self.disguise_moves_left <= 0 and room_key in CAMERA_ZONES:
            self.alert_level += self.cfg["ALERT_MOVE"]
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
        if not self.patrol_active and self.total_moves >= self.cfg["PATROL_START_MOVES"]:
            self.patrol_active = True
            print("A lo lejos, una patrulla agarra la avenida. No mira, pero aprende.")
            print("Bernal (radio): El tiempo se les puso a favor. Remata lo tuyo.")
        if self.patrol_active and inside_bank:
            self.alert_level += self.cfg["PATROL_ALERT_PER_MOVE"]
            sfx("beep_camara.wav")

    def police_arrives(self) -> bool:
        return self.alert_level >= self.cfg["ALERT_THRESHOLD"]

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



class Game:
    def __init__(self) -> None:
        self.world = World()
        self.player = Player(location="exterior", inventory=["Guantes"])
        self.running: bool = True
        self.vault_open: bool = False
        self.has_entered: bool = False
        self.formally_entered: bool = False

    def intro_context(self) -> None:
        print("Cali. El centro baja las persianas; tú subes el pulso. Te quitaron horas, sueldos y paciencia. Esta noche decides si el banco es una caja o un espejo.")
        print("Regla simple: entra, entiende, elige. El dinero pesa; la verdad, más. No podrás llevarte todo, y tampoco deberías.")
        sfx("intro.wav")
        self.current_room().describe()
        play_ambient(self.player.location)
        print("Escribe 'ayuda' para ver comandos.")

    def current_room(self) -> Room:
        return self.world.rooms[self.player.location]

    def cmd_move(self, direction: str) -> None:
        room = self.current_room()
        if direction not in room.exits:
            print("No puedes moverte en esa dirección.")
            sfx("error.wav")
            return

        exit_obj = room.exits[direction]

        if exit_obj.exit_type == EXIT_BLOCKED:
            print("Un bloqueo imposible de franquear.")
            sfx("bloqueado.wav")
            return

        if exit_obj.exit_type in {EXIT_LOCKED, EXIT_NEEDS}:
            req = exit_obj.requires
            if not req:
                print("La salida no cede.")
                sfx("puerta_cerrada.wav")
                return
            if not self.player.has_item(req):
                print(f"Necesitas {req}.")
                sfx("puerta_cerrada.wav")
                return

            if req.lower() == "ganzua":
                print("La cerradura aprende a ceder. *clic*")
                sfx("ganzua.wav")
                if self.world.pick_uses is not None:
                    self.world.pick_uses -= 1
                    if self.world.pick_uses <= 0:
                        print("La ganzúa se parte en el último giro.")
                        self.player.inventory = [i for i in self.player.inventory if i.lower() != "ganzua"]
                        print("Bernal (radio): Se te partió la ganzúa. Sin eso, cada puerta pesa el doble. Calculá.")
            elif req.lower() == "tarjeta":
                print("El lector suspira en verde.")
                sfx("card_beep.wav")
            elif req.lower() == "llave":
                print("La llave gira con resistencia y cede.")
                sfx("card_beep.wav")

        sfx("pasos.wav")

        if (
            exit_obj.exit_type == EXIT_EVENT
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

        self.world.update_alert_on_move(self.player.location)

        if self.player.has_loot and self.player.location in {"vestibulo", "pasillo_boveda"}:
            self.world.alert_level += self.world.cfg["LOOT_NOISE"]

        if self.world.keypad_lock_moves > 0:
            self.world.keypad_lock_moves -= 1

        if self.world.disguise_moves_left > 0:
            self.world.disguise_moves_left -= 1
            if self.world.disguise_moves_left == 0:
                print("El uniforme pierde su magia. Vuelves a ser tú.")

        inside = self.player.location in INTERIORS
        self.world.tick_time(inside)

        self.current_room().describe()
        play_ambient(self.player.location)
        self.world.radio_message(self.player.location)

        if self.world.police_arrives():
            self.ending_police()

        if self.player.location == "exterior" and self.formally_entered:
            self.check_escape()

    def cmd_examine(self, target: Optional[str] = None) -> None:
        room = self.current_room()

        if target is None or target.lower() in {room.key, room.name.lower()}:
            self.world.describe_objects(room)
            return

        obj = target.lower()

        if room.key == "oficina_gerente" and obj == "nota1":
            print('Nota1: Primer dígito: 5. "No traigas más dinero sucio a casa". La firma tiembla como quien no quiere volver a firmar jamás.')
            sfx("nota.wav")
        elif room.key == "sala_seguridad" and obj == "nota2":
            print('Nota2: Segundo dígito: 7. Nóminas infladas, cámaras nuevas, favores viejos. Al pie: "Calla y piensa en los niños". Lo escribió alguien que ya no duerme.')
            sfx("nota.wav")
        elif room.key == "antec_boveda" and obj == "nota3":
            print('Nota3: Tercer dígito: 3. Transferencias que dan vueltas y nunca llegan. "Si cae uno, caen todos"; a veces el miedo es honesto.')
            sfx("nota.wav")
        elif room.key == "archivo" and obj == "nota4":
            print('Nota4: "El uniforme compra cinco minutos de fe. Después pregunta quién eres". Hay una firma borrada y un sello mojado.')
            sfx("nota.wav")
        elif room.key in {"antec_boveda", "boveda"} and obj in {"teclado", "codigo", "boveda"}:
            print("Teclado frío. Tres dígitos hacen una llave. Tres errores invitan a cantar sirenas.")
            sfx("teclado.wav")
        elif room.key == "boveda" and obj == "dossier":
            print("Dossier: rutas, nombres, empresas que viven de no mirarte a los ojos. Si esto sale, alguien desayuna justicia.")
            sfx("buscar.wav")
        elif room.key == "sala_seguridad" and obj in {"panel", "panel de control"}:
            print("Panel conmutador: promesa de silencio en un gesto. La fe aquí se mide en voltios.")
            sfx("panel.wav")
        else:
            print("No descubres nada más.")
            sfx("nada.wav")

    def cmd_take(self, item: str) -> None:
        room = self.current_room()
        item_names = [i.lower() for i in room.items]

        if item.lower() not in item_names:
            print("No hay nada con ese nombre aquí.")
            sfx("nada.wav")
            return

        real_name = room.items[item_names.index(item.lower())]
        self.player.inventory.append(real_name)
        room.items.remove(real_name)
        print(f"Recoges {real_name}.")
        sfx("recoger.wav")

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
                sfx("error.wav")
                return

        if name in {"panel", "panel de control"} and room.key == "sala_seguridad":
            if not self.world.cameras_disabled:
                self.world.cameras_disabled = True
                self.world.cams_off_moves_left = self.world.cfg["CAMS_OFF_MOVES"]
                print("El murmullo eléctrico se apaga. La mirada del banco, también.")
                sfx("panel.wav")
                sfx("radio_seguridad_off.wav")
            else:
                print("Ya silenciaste las cámaras.")
                sfx("nada.wav")
            return

        if name == "fusibles":
            if room.key == "mantenimiento":
                if not self.world.cameras_disabled:
                    self.world.cameras_disabled = True
                    self.world.cams_off_moves_left = self.world.cfg["CAMS_OFF_MOVES_FUSE"]
                    self.world.alert_level += 1
                    print("Un chasquido y las luces tiemblan. La red parpadea a oscuras.")
                    sfx("panel.wav")
                    print("Bernal (radio): Sombra ganada, tiempo perdido. Muévete pues.")
                else:
                    print("Ya silenciaste las cámaras por otro medio.")
                    sfx("nada.wav")
            else:
                print("Aquí no hay tablero que obedecería.")
                sfx("nada.wav")
            return

        if name == "uniforme":
            self.world.disguise_moves_left = self.world.cfg["DISGUISE_MOVES"]
            print("Te ajustas el uniforme: el banco te cree del turno de noche por un rato.")
            sfx("recoger.wav")
            print("Bernal (radio): La pinta también roba. Cruza donde miran.")
            return

        if name == "taladro":
            if room.key == "antec_boveda" and not self.vault_open:
                print("El metal grita. Cada segundo pesa como un delito.")
                sfx("taladro.wav")
                print("Bernal (radio): A mí me botaron por menos. Si eso se oye afuera, aborta sin dudar.")
                self.world.alert_level += self.world.cfg["ALERT_DRILL"]
                if self.world.police_arrives():
                    self.ending_police()
                    return
                self.vault_open = True
                print("Los pernos retroceden. El animal abre el ojo.")
                sfx("puerta_pesada.wav")
                return
            else:
                print("No parece el lugar para taladrar.")
                sfx("nada.wav")
                return

        if name == "tarjeta":
            if room.key in {"exterior", "vestibulo"}:
                print("La tarjeta estará lista cuando pases junto a un lector.")
                sfx("card_beep.wav")
            else:
                print("Aquí no hay dónde pasarla.")
                sfx("nada.wav")
            return

        if name == "ganzua":
            print("Tu mano y la ganzúa ensayan un diálogo viejo con el metal.")
            sfx("ganzua.wav")
            return

        if name == "codigo":
            print("No es un objeto. Júntalo en la cabeza y úsalo frente al teclado.")
            sfx("teclado.wav")
            return

        print("No consigues usarlo aquí.")
        sfx("nada.wav")

    def cmd_use_code(self) -> None:
        room = self.current_room()

        if room.key != "antec_boveda":
            print("Aquí no hay teclado que respondería.")
            sfx("nada.wav")
            return

        if self.world.keypad_lock_moves > 0:
            print(f"El teclado está bloqueado por {self.world.keypad_lock_moves} movimientos.")
            sfx("alarma_soft.wav")
            print("Bernal (radio): Otra no. Cabeza antes que suerte.")
            return

        entry = input("Código de 3 dígitos: ").strip()
        sfx("teclado.wav")

        if entry == self.world.vault_code:
            self.vault_open = True
            print("Un susurro hidráulico concede el paso. La bóveda te cree.")
            sfx("puerta_pesada.wav")
        else:
            print("El pitido muerde. El edificio te huele.")
            sfx("alarma_soft.wav")
            self.world.alert_level += self.world.cfg["ALERT_WRONGCODE"]
            self.world.keypad_lock_moves = self.world.cfg["KEYPAD_LOCK_MOVES"]
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
            f"Alerta: {self.world.alert_level}/{self.world.cfg['ALERT_THRESHOLD']} | Cámaras: "
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
            sfx("nada.wav")
            return
        if not self.vault_open:
            print("La bóveda sigue cerrada.")
            sfx("puerta_cerrada.wav")
            return
        if self.player.has_loot:
            print("Ya cargas suficiente pecado.")
            sfx("nada.wav")
            return
        print("Llenas la mochila con fajos y metal que no te pertenecen.")
        sfx("bolsa_dinero.wav")
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
        sfx("sirena.wav")
        print("FINAL: Capturado. La verdad no salió, el dinero tampoco.")
        self.running = False

    def ending_empty(self) -> None:
        print("\nSales con las manos limpias y vacías. Aprendiste el mapa, no el motivo. La ciudad bosteza y sigue sin ti.")
        sfx("vacio.wav")
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
            sfx("motor_suave.wav")
            print("FINAL BUENO: Limpio, preciso, casi elegante.")
        elif self.world.alert_level >= 3:
            print("\nMuerdes el volante. Las sirenas pierden interés antes que tú el miedo. No todo cobró hoy, pero cobrará.")
            sfx("motor_apuro.wav")
            print("FINAL NEUTRAL: Escapas con botín, pero la ciudad aprendió tu olor.")
        else:
            print("\nLa noche te acepta sin hacer preguntas. No todas las salidas son una victoria; algunas solo son salida.")
            sfx("motor.wav")
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
                sfx("bye.wav")
                break
            else:
                if raw in {"coger botin", "tomar botin", "recoger botin"}:
                    self.try_take_loot()
                else:
                    print("Comando no reconocido. Escribe 'ayuda'.")
                    sfx("error.wav")


if __name__ == "__main__":
    Game().loop()
