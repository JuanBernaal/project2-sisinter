from typing import Dict

from enums import ExitType
from models import Room, Exit


class WorldMapBuilder:

    @staticmethod
    def build_rooms() -> Dict[str, Room]:
        rooms: Dict[str, Room] = {}

        rooms["exterior"] = Room(
            "exterior",
            "Calle Oscura",
            "Calle desierta frente al banco. Norte: entrada. Oeste: callejón. Este: escalera de emergencia.",
            "Cali. Medianoche sin testigos. El banco respira con aire prestado: de día vende seguridad; de noche guarda silencios. No viniste por gloria: viniste a cobrar lo que nunca pagaron. Esta noche el banco será caja o espejo.",
        )
        rooms["callejon"] = Room(
            "callejon",
            "Callejón",
            "Callejón húmedo; una mochila espera tras palés.",
            "El callejón huele a lluvia vieja y neón cansado. Tras los palés, tu mochila reposa como un perro que recuerda tu silbido. Dentro, una ganzúa bruñida por trabajos cortos y promesas largas.",
            items=["Ganzua"],
        )
        rooms["escalera"] = Room(
            "escalera",
            "Escalera de Emergencia",
            "Escalera metálica hacia una puerta de servicio.",
            "La baranda está fría como un recibo vencido. La pintura descascarada dejó al descubierto años de alarmas que sonaron para nadie. Debajo de un extintor asoma una llave con esmalte pelado.",
            items=["Llave"],
        )
        rooms["vestibulo"] = Room(
            "vestibulo",
            "Vestíbulo",
            "Mármol silencioso y cámaras con sueño ligero.",
            "El mármol guarda huellas invisibles: zapatos caros, risas cuidadas, blindajes recién pagados. Sobre ti, ojos de vidrio que jamás parpadean por compasión. El eco aquí devuelve decisiones.",
        )
        rooms["oficina_gerente"] = Room(
            "oficina_gerente",
            "Oficina del Gerente",
            "Despacho pulcro; un cajón forzado delata prisa.",
            "Madera encerada y ascensos heredados. La foto de familia, boca abajo; un naufragio voluntario. El cajón cede: una tarjeta tibia y papeles que no saben mentir tanto.",
            items=["Tarjeta", "PapelRojo"],
        )
        rooms["archivo"] = Room(
            "archivo",
            "Archivo Legal",
            "Anaqueles oprimidos por carpetas sin verano.",
            "Papeles que pesan más que lingotes. Huele a tinta húmeda y aire acondicionado cansado. Entre legajos se esconde un uniforme de vigilancia doblado con pudor y una nota que nadie debía leer.",
            items=["Uniforme", "PapelNegro"],
        )
        rooms["sala_seguridad"] = Room(
            "sala_seguridad",
            "Sala de Seguridad",
            "Monitores verdes y un botón que promete silencio.",
            "Un enjambre de pantallas dibuja turnos mal pagados. El café seco es una guardia que envejeció en la taza. Un botón rojo espera fe; al oprimirlo, la ciudad queda ciega, pero no inocente.",
            items=["PapelVerde"],
        )
        rooms["pasillo_boveda"] = Room(
            "pasillo_boveda",
            "Pasillo hacia la Bóveda",
            "Pasillo reforzado; el aire suena a metal dormido.",
            "Las paredes conservan golpes que nunca se denunciaron. El aire vibra grave, como si el banco roncara. Nadie canta aquí; los secretos no llevan melodía.",
        )
        rooms["mantenimiento"] = Room(
            "mantenimiento",
            "Cuarto de Mantenimiento",
            "Paneles, fusibles y olor a ozono barato.",
            "Cables sin poesía y etiquetas a medio despegar. Un tablero general prometiendo milagros técnicos y factura en la alerta.",
            items=["Fusibles"],
        )
        rooms["antec_boveda"] = Room(
            "antec_boveda",
            "Antesala de la Bóveda",
            "Carros de valores y herramientas bajo una lona.",
            "Luz oblicua y polvo suspendido. Un carrito dejó surcos que cuentan mejor la historia que cualquier informe. Bajo la lona, un taladro impaciente; entre papeles, la última pieza del número que no quiere olvidarse.",
            items=["Taladro", "PapelAzul"],
        )
        rooms["boveda"] = Room(
            "boveda",
            "Bóveda",
            "El halo frío del dinero que no toca el sol.",
            "La puerta es un eclipse detenido. Dentro, fajos, lingotes y un archivador sin rótulo oficial. Hay botín; también hay un dossier con nombres y rutas que pesan distinto.",
            items=["Dossier"],
        )

        # Exits
        rooms["exterior"].exits = {
            "norte": Exit("vestibulo", ExitType.LOCKED, "Tarjeta"),
            "oeste": Exit("callejon", ExitType.FREE),
            "este": Exit("escalera", ExitType.FREE),
        }
        rooms["callejon"].exits = {
            "este": Exit("exterior", ExitType.FREE),
            "norte": Exit("vestibulo", ExitType.LOCKED, "Ganzua"),
        }
        rooms["escalera"].exits = {
            "oeste": Exit("exterior", ExitType.FREE),
            "norte": Exit("vestibulo", ExitType.LOCKED, "Ganzua"),
        }
        rooms["vestibulo"].exits = {
            "sur": Exit("exterior", ExitType.FREE),
            "este": Exit("oficina_gerente", ExitType.LOCKED, "Ganzua"),
            "oeste": Exit("sala_seguridad", ExitType.FREE),
            "norte": Exit("pasillo_boveda", ExitType.NEEDS, "Tarjeta"),
        }
        rooms["oficina_gerente"].exits = {
            "oeste": Exit("vestibulo", ExitType.FREE),
            "norte": Exit("archivo", ExitType.LOCKED, "Llave"),
        }
        rooms["archivo"].exits = {"sur": Exit("oficina_gerente", ExitType.FREE)}
        rooms["sala_seguridad"].exits = {"este": Exit("vestibulo", ExitType.FREE)}
        rooms["pasillo_boveda"].exits = {
            "sur": Exit("vestibulo", ExitType.FREE),
            "norte": Exit("antec_boveda", ExitType.FREE),
            "oeste": Exit("mantenimiento", ExitType.FREE),
        }
        rooms["mantenimiento"].exits = {"este": Exit("pasillo_boveda", ExitType.FREE)}
        rooms["antec_boveda"].exits = {"sur": Exit("pasillo_boveda", ExitType.FREE), "norte": Exit("boveda", ExitType.EVENT)}
        rooms["boveda"].exits = {"sur": Exit("antec_boveda", ExitType.FREE)}

        return rooms
