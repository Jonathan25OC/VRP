import math

def distancia(coord1, coord2):
    # Haversine
    R = 6371
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return R * (2 * math.asin(math.sqrt(a)))

def en_ruta(rutas, c):
    for r in rutas:
        if c in r:
            return r
    return None

def peso_ruta(ruta, pedidos):
    return sum([pedidos[c] for c in ruta])

def vrp_voraz(coord, pedidos, almacen, max_carga):
    from operator import itemgetter
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
        if rc1 is None and rc2 is None:
            if peso_ruta([c1, c2], pedidos) <= max_carga:
                rutas.append([c1, c2])
        elif rc1 is not None and rc2 is None:
            if rc1[0] == c1 and peso_ruta(rc1, pedidos) + pedidos[c2] <= max_carga:
                rc1.insert(0, c2)
            elif rc1[-1] == c1 and peso_ruta(rc1, pedidos) + pedidos[c2] <= max_carga:
                rc1.append(c2)
        elif rc1 is None and rc2 is not None:
            if rc2[0] == c2 and peso_ruta(rc2, pedidos) + pedidos[c1] <= max_carga:
                rc2.insert(0, c1)
            elif rc2[-1] == c2 and peso_ruta(rc2, pedidos) + pedidos[c1] <= max_carga:
                rc2.append(c1)
        elif rc1 != rc2:
            if rc1[0] == c1 and rc2[-1] == c2 and peso_ruta(rc1 + rc2, pedidos) <= max_carga:
                rutas.remove(rc1)
                rc2.extend(rc1)
            elif rc1[-1] == c1 and rc2[0] == c2 and peso_ruta(rc1 + rc2, pedidos) <= max_carga:
                rutas.remove(rc2)
                rc1.extend(rc2)
    return rutas