import time
import math
from typing import Tuple

from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor

from .movement import girar_solo_derecha, girar_solo_izquierda, recto, parar

DISTANCIA_PALOS_PORTERIA_M = 0.35
DISTANCIA_PORTERIA_ALTA_M = 1.70
DISTANCIA_PORTERIA_BAJA_M = 0.30

color_sensor = ColorSensor(INPUT_1)

def calibrar_sensor_color_en_movimiento(color_sensor, distancia_m=0.05, n_muestras=50, desviaciones_sigma=3):
    """
    Mueve el robot hacia adelante y toma muestras estadisticas del suelo.

    Args:
        distancia_m: Distancia a recorrer en metros.
        n_muestras: Cantidad de lecturas a tomar.
        sigma_threshold: Cuántas desviaciones estandar por debajo de la media
                         consideramos que ya es "linea" (valor atipico).

    Returns:
        tuple: (media, umbral_linea)
    """
    lecturas = []

    recto(distancia_m, velocidad=15, block=False)

    tiempo_espera = 1 / n_muestras

    for _ in range(n_muestras):
        lecturas.append(color_sensor.reflected_light_intensity)
        time.sleep(tiempo_espera)

    n = len(lecturas)
    if n == 0: return 0, 0
    media = sum(lecturas) / n
    varianza = sum((x - media) ** 2 for x in lecturas) / n
    desviacion_tipica = math.sqrt(varianza)
    umbral_linea = desviaciones_sigma * desviacion_tipica
    umbral_linea += 15

    print("Calibracion Sensor de Color -> Media: ", media, ", Desv: ", desviacion_tipica, ", Umbral: ", umbral_linea)
    return media, umbral_linea

def ancho_angular_porteria() -> Tuple[float, float]:
    cateto_opuesto = DISTANCIA_PALOS_PORTERIA_M / 2.0
    cateto_contiguo1 = DISTANCIA_PORTERIA_ALTA_M
    alpha1 = math.atan(cateto_opuesto / cateto_contiguo1)
    cateto_contiguo2 = DISTANCIA_PORTERIA_BAJA_M
    alpha2 = math.atan(cateto_opuesto / cateto_contiguo2)
    return (alpha1 * 2 * 180 / math.pi, alpha2 * 2 * 180 / math.pi)

def seguir_linea(media, umbral, direccion_derecha: bool, distancia_m: float, seg_p_m: float):
    recto(0.035, 30, True)
    velocidad = 30
    limite_inf, limite_sup = media - umbral, media + umbral
    t_final = time.time() + seg_p_m * distancia_m

    while time.time() < t_final:
        lectura = color_sensor.reflected_light_intensity
        if direccion_derecha:
            # rueda derecha si sale del rango (en linea)
            # rueda izquierda si entra
            if lectura < limite_inf or lectura > limite_sup:
                girar_solo_derecha(15, velocidad, True)
            else:
                girar_solo_izquierda(15, velocidad, True)
        else:
            # rueda izquierda si sale del rango (en linea)
            # rueda derecha si entra
            if lectura < limite_inf or lectura > limite_sup:
                girar_solo_izquierda(15, velocidad, True)
            else:
                girar_solo_derecha(15, velocidad, True)
    parar()

def convertir_tiempo_a_angulo(points, grados_totales=360):
    """
    Convierte una lista de tuplas (tiempo, distancia) a (angulo, distancia).
    Asume que el primer punto es 0 grados y el ultimo es grados_totales.
    """
    if not points or len(points) < 2:
        return []

    t_inicio = points[0][0]
    t_fin = points[-1][0]
    duracion_total = t_fin - t_inicio
    datos_angulares = []

    for t, distancia in points:
        progreso = (t - t_inicio) / duracion_total
        angulo = progreso * grados_totales

        datos_angulares.append((angulo, distancia))
    return datos_angulares

def analizar_valles(points, umbral_distancia=80, max_salto=20, grados_totales=360):
    """
    Analiza los puntos para detectar objetos. Detecta un nuevo valle si:
    1. Se entra en el umbral de distancia.
    2. Estando dentro, hay un cambio brusco de profundidad (max_salto).

    Args:
        points: lista [(tiempo, dist), ...]
        umbral_distancia: Distancia maxima para considerar deteccion.
        max_salto: Diferencia de cm para considerar que son dos objetos distintos pegados.

    Devuelve list[(angulo, dist, ancho)...]
    """
    datos = convertir_tiempo_a_angulo(points, grados_totales)

    valles_crudos = []

    # Estado del sistema
    en_valle = False
    inicio_valle = 0
    puntos_valle = []
    ultima_distancia_valida = 0

    for angulo, dist in datos:

        # CASO 1: Estamos fuera del rango de deteccion global
        if dist > umbral_distancia:
            if en_valle:
                # SE ACABO EL VALLE (Salimos al fondo)
                en_valle = False
                fin_valle = angulo

                # Guardamos el valle que teniamos
                dist_promedio = sum(puntos_valle) / len(puntos_valle)
                ancho = fin_valle - inicio_valle
                centro = (inicio_valle + fin_valle) / 2

                valles_crudos.append({
                    'centro': centro,
                    'distancia': dist_promedio,
                    'ancho': ancho,
                    'min_ang': inicio_valle,
                    'max_ang': fin_valle
                })
                puntos_valle = []

            # Si no estabamos en valle, seguimos ignorando (es fondo)
            continue

        # CASO 2: Estamos dentro del rango (dist < umbral)
        else:
            if not en_valle:
                # EMPIEZA UN VALLE NUEVO (Venimos del fondo)
                en_valle = True
                inicio_valle = angulo
                puntos_valle = [dist]
                ultima_distancia_valida = dist

            else:
                # YA ESTABAMOS EN UN VALLE, CHEQUEAR
                # Calculamos si hay un salto brusco respecto a la medida anterior
                salto = abs(dist - ultima_distancia_valida)

                if salto > max_salto:
                    # SALTO DETECTADO: SON DOS OBJETOS DISTINTOS PEGADOS
                    # Cerramos el valle anterior justo aqui
                    fin_valle = angulo

                    dist_promedio = sum(puntos_valle) / len(puntos_valle)
                    ancho = fin_valle - inicio_valle
                    centro = (inicio_valle + fin_valle) / 2

                    valles_crudos.append({
                        'centro': centro,
                        'distancia': dist_promedio,
                        'ancho': ancho,
                        'min_ang': inicio_valle,
                        'max_ang': fin_valle
                    })

                    # Abrimos inmediatamente el nuevo valle
                    # (No ponemos en_valle=False porque seguimos dentro del umbral)
                    inicio_valle = angulo
                    puntos_valle = [dist]
                    ultima_distancia_valida = dist

                else:
                    # CONTINUACION NORMAL DEL MISMO OBJETO
                    puntos_valle.append(dist)
                    ultima_distancia_valida = dist # Actualizamos referencia

    # (Caso borde: Limpiar si quedo uno abierto al final del loop)
    if en_valle:
        fin_valle = datos[-1][0]
        dist_promedio = sum(puntos_valle) / len(puntos_valle)
        valles_crudos.append({
            'centro': (inicio_valle + fin_valle) / 2,
            'distancia': dist_promedio,
            'ancho': fin_valle - inicio_valle,
            'min_ang': inicio_valle,
            'max_ang': fin_valle
        })

    valles_finales = valles_crudos

    resultado = []
    for v in valles_finales:
        if v['ancho'] > 1.5: # Filtro minimo angular
            resultado.append((v['centro'], v['distancia'], v['ancho']))

    print("Angulo Central | Distancia | Ancho")
    for angulo, dist, ancho in resultado:
        print("{:.1f} deg \t| {:.1f} cm \t| {:.1f} deg".format(angulo, dist, ancho))

    return resultado
