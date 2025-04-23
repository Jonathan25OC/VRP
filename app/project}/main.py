from flask import Flask, render_template, request, jsonify
import math
from operator import itemgetter

app = Flask(__name__)

# === FUNCIONES DE APOYO ===
def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
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

# === ALGORITMO VRP ===
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

# === RUTAS FLASK ===
@app.route("/")
def formulario():
    return render_template("formulario.html")

@app.route("/procesar", methods=["POST"])
def procesar():
    try:
        coord = eval(request.form["coord"])
        pedidos = eval(request.form["pedidos"])
        almacen = eval(request.form["almacen"])
        max_carga = float(request.form["max_carga"])
        max_distancia = float(request.form["max_distancia"])
        max_gasolina = float(request.form["max_gasolina"])
        rendimiento_km_l = float(request.form["rendimiento_km_l"])

        rutas = vrp_voraz(coord, pedidos, almacen, max_carga, max_distancia, max_gasolina, rendimiento_km_l)

        resultados = []
        for ruta in rutas:
            dist = distancia_total_ruta(ruta, coord, almacen)
            gas = consumo_gasolina(dist, rendimiento_km_l)
            resultados.append({
                "ruta": ruta,
                "distancia_total": round(dist, 2),
                "consumo_gasolina": round(gas, 2)
            })

        return render_template("resultado.html", rutas=resultados)

    except Exception as e:
        return f"Error en el procesamiento: {e}"

if __name__ == "__main__":
    app.run(debug=True)
