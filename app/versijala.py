import math
from operator import itemgetter

def distancia(coord1, coord2):
    lat1 = coord1[0]
    lon1 = coord1[1]
    lat2 = coord2[0]
    lon2 = coord2[1]
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def en_ruta(rutas, c):
    for r in rutas:
        if c in r:
            return r
    return None

def peso_ruta(ruta, pedidos):
    return sum([pedidos[c] for c in ruta])

def distancia_total_ruta(ruta, coord, almacen):
    total = distancia(almacen, coord[ruta[0]])
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i + 1]])
    total += distancia(coord[ruta[-1]], almacen)
    return total

def consumo_gasolina(distancia_total, rendimiento_km_l):
    return distancia_total / rendimiento_km_l

def vrp_voraz(coord, pedidos, almacen, max_carga, max_distancia, max_gasolina, rendimiento_km_l):
    s = {}
    for c1 in coord:
        for c2 in coord:
            if c1 != c2 and (c2, c1) not in s:
                d_c1_c2 = distancia(coord[c1], coord[c2])
                d_c1_almacen = distancia(coord[c1], almacen)
                d_c2_almacen = distancia(coord[c2], almacen)
                s[(c1, c2)] = d_c1_almacen + d_c2_almacen - d_c1_c2

    s = sorted(s.items(), key=itemgetter(1), reverse=True)
    rutas = []

    for (c1, c2), _ in s:
        rc1 = en_ruta(rutas, c1)
        rc2 = en_ruta(rutas, c2)

        def es_valida(ruta):
            p = peso_ruta(ruta, pedidos)
            d = distancia_total_ruta(ruta, coord, almacen)
            g = consumo_gasolina(d, rendimiento_km_l)
            return p <= max_carga and d <= max_distancia and g <= max_gasolina

        if rc1 is None and rc2 is None:
            nueva_ruta = [c1, c2]
            if es_valida(nueva_ruta):
                rutas.append(nueva_ruta)
        elif rc1 is not None and rc2 is None:
            if rc1[0] == c1:
                nueva_ruta = [c2] + rc1
                if es_valida(nueva_ruta):
                    rutas.remove(rc1)
                    rutas.append(nueva_ruta)
            elif rc1[-1] == c1:
                nueva_ruta = rc1 + [c2]
                if es_valida(nueva_ruta):
                    rutas.remove(rc1)
                    rutas.append(nueva_ruta)
        elif rc1 is None and rc2 is not None:
            if rc2[0] == c2:
                nueva_ruta = [c1] + rc2
                if es_valida(nueva_ruta):
                    rutas.remove(rc2)
                    rutas.append(nueva_ruta)
            elif rc2[-1] == c2:
                nueva_ruta = rc2 + [c1]
                if es_valida(nueva_ruta):
                    rutas.remove(rc2)
                    rutas.append(nueva_ruta)
        elif rc1 != rc2:
            if rc1[-1] == c1 and rc2[0] == c2:
                nueva_ruta = rc1 + rc2
                if es_valida(nueva_ruta):
                    rutas.remove(rc1)
                    rutas.remove(rc2)
                    rutas.append(nueva_ruta)
            elif rc2[-1] == c2 and rc1[0] == c1:
                nueva_ruta = rc2 + rc1
                if es_valida(nueva_ruta):
                    rutas.remove(rc1)
                    rutas.remove(rc2)
                    rutas.append(nueva_ruta)

    return rutas

if __name__ == "__main__":
    coord = {
        'EDO.MEX': (19.2938258568844, -99.65366252023884),
        'QRO': (20.593537489366717, -100.39004057702225),
        'CDMX': (19.432854452264177, -99.13330004822943),
        'SLP': (22.151725492903953, -100.97657666103268),
        'MTY': (25.673156272083876, -100.2974200019319),
        'PUE': (19.063532268065185, -98.30729139446866),
        'GDL': (20.67714565083998, -103.34696388920293),
        'MICH': (19.702614895389996, -101.19228631929688),
        'SON': (29.075273188617818, -110.95962477655333)
    }

    pedidos = {
        'EDO.MEX': 10,
        'QRO': 13,
        'CDMX': 7,
        'SLP': 11,
        'MTY': 15,
        'PUE': 8,
        'GDL': 6,
        'MICH': 7,
        'SON': 8
    }

    almacen = (19.432854452264177, -99.13330004822943)
    max_carga = 40
    max_distancia = 25  # Cambiar según necesidad
    max_gasolina = 2    # Cambiar según necesidad
    rendimiento_km_l = 10

    rutas = vrp_voraz(coord, pedidos, almacen, max_carga, max_distancia, max_gasolina, rendimiento_km_l)

    for ruta in rutas:
        distancia_r = distancia_total_ruta(ruta, coord, almacen)
        consumo_r = consumo_gasolina(distancia_r, rendimiento_km_l)
        print(f"Ruta: {ruta}")
        print(f"  Distancia total: {distancia_r:.2f}")
        print(f"  Consumo gasolina: {consumo_r:.2f} litros\n")
