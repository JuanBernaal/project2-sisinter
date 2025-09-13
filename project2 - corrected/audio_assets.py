from typing import Dict, Tuple


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
    "archivo": "radio_archivo.wav",
    "ganzua_rota": "radio_ganzua_rota.wav",
    "mantenimiento": "radio_mantenimiento.wav",
    "patrulla": "radio_patrulla.wav",
    "rearme_camaras": "radio_rearme_camaras.wav",
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


AMBIENT_SOURCE_POS: Dict[str, Tuple[float, float, float, float]] = {
    "exterior":        ( 2.0,  0.0,  2.5, 0.60),  
    "callejon":        (-1.5,  0.0,  1.0, 0.55), 
    "escalera":        ( 0.0,  2.0,  0.5, 0.50), 
    "vestibulo":       ( 0.0,  0.0,  2.0, 0.50),  
    "oficina_gerente": ( 0.8,  0.0,  1.0, 0.45),  
    "sala_seguridad":  ( 0.0,  0.0, -1.0, 0.55),  
    "pasillo_boveda":  ( 0.0,  0.0,  2.5, 0.50),  
    "antec_boveda":    (-0.8,  0.0,  1.0, 0.50),  
    "boveda":          ( 0.0,  0.0,  1.5, 0.50),  
    "archivo":         ( 0.8,  0.0,  1.0, 0.45),  
    "mantenimiento":   (-0.8,  0.0,  0.5, 0.55),  
}


SFX_PARAMS: Dict[str, Tuple[float, float, float, float]] = {
    "intro.wav":         (0.0, 0.0, 0.1, 0.70),
    "bye.wav":           (0.0, 0.0, 0.1, 0.50),
    "error.wav":         (0.0, 0.0, 0.0, 0.55),
    "error":             (0.0, 0.0, 0.0, 0.55),

    "pasos.wav":         (0.0,-0.2, 0, 0.50),
    "buscar.wav":        (0.0, 0.0, 0.0, 0.50),
    "buscar":            (0.0, 0.0, 0.0, 0.50),
    "recoger.wav":       (0.2, 0.0, 0.0, 0.30),
    "recoger":           (0.2, 0.0, 0.0, 0.30),
    "nada.wav":          (0.0, 0.0, 0.0, 0.35),
    "nada":              (0.0, 0.0, 0.0, 0.35),

    "bloqueado.wav":     (0.0, 0.0, 1.0, 0.70),
    "puerta_cerrada.wav":(0.0, 0.0, 1.0, 0.75),
    "ganzua.wav":        (0.2, 0.0, 0.0, 0.50),
    "card_beep.wav":     (0.4, 0.0, 0.8, 0.65),
    "puerta_pesada.wav": (0.0, 0.0, 1.5, 0.85),

    "teclado.wav":       (0.0, 0.0, 0.5, 0.60),
    "teclado":           (0.0, 0.0, 0.5, 0.60),
    "panel.wav":         (0.6, 0.0, 0.2, 0.60),
    "panel":             (0.6, 0.0, 0.2, 0.60),

    "beep_camara.wav":   (0.0, 2.0, 0.5, 0.60),
    "beep_camara":       (0.0, 2.0, 0.5, 0.60),
    "alarma_soft.wav":   (0.0, 2.0, 0.0, 0.80),

    "taladro.wav":       (-0.4, 0.0, 1.0, 0.90),

    "bolsa_dinero.wav":  (0.2, 0.0, 0.2, 0.65),
    "nota.wav":          (0.0, 0.0, 0.2, 0.55),

    "sirena.wav":        (3.0, 0.0, 5.0, 0.90),
    "sirena":            (3.0, 0.0, 5.0, 0.90),
    "vacio.wav":         (0.0, 0.0, 2.0, 0.50),
    "motor_suave.wav":   (2.5, 0.0, 4.0, 0.65),
    "motor_apuro.wav":   (2.5, 0.0, 4.0, 0.85),
    "motor.wav":         (2.0, 0.0, 3.0, 0.70),

    "radio_vestibulo.wav":      (0.0, 0.0, 0.1, 0.75),
    "radio_seguridad_on.wav":   (0.0, 0.0, 0.1, 0.75),
    "radio_seguridad_off.wav":  (0.0, 0.0, 0.1, 0.75),
    "radio_seguridad_off":      (0.0, 0.0, 0.1, 0.75),
    "radio_oficina.wav":        (0.0, 0.0, 0.1, 0.75),
    "radio_pasillo.wav":        (0.0, 0.0, 0.1, 0.75),
    "radio_antec.wav":          (0.0, 0.0, 0.1, 0.75),
    "radio_boveda.wav":         (0.0, 0.0, 0.1, 0.75),
    "radio_ayuda.wav":          (0.0, 0.0, 0.1, 0.70),
    "radio_exponer.wav":        (0.0, 0.0, 0.1, 0.80),
    "radio_uniforme.wav":      (0.0, 0.0, 0.1, 0.75),
    "radio_archivo.wav":        (0.0, 0.0, 0.1, 0.75),
    "radio_ganzua_rota.wav":    (0.0, 0.0, 0.1, 0.75),
    "radio_mantenimiento.wav":  (0.0, 0.0, 0.1, 0.75),
    "radio_patrulla.wav":       (0.0, 0.0, 0.1, 0.75),
    "radio_rearme_camaras.wav": (0.0, 0.0, 0.1, 0.75),
}


FORCE_MONO_SOUNDS = {
    "sirena.wav",
    "sirena",
    "motor_suave.wav",
    "motor_apuro.wav",
    "motor.wav",
    "taladro.wav",
    "beep_camara.wav",
    "beep_camara",
    "alarma_soft.wav",
    "pasos.wav",
}