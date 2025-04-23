import folium
from folium.plugins import MarkerCluster

def generar_mapa(rutas, coord, almacen):
    m = folium.Map(location=almacen, zoom_start=5)
    folium.Marker(almacen, tooltip="Almacén", icon=folium.Icon(color="green")).add_to(m)
    colors = ["red", "blue", "orange", "purple", "cadetblue", "darkgreen"]
    for i, ruta in enumerate(rutas):
        puntos = [almacen] + [coord[c] for c in ruta] + [almacen]
        folium.PolyLine(puntos, color=colors[i % len(colors)], weight=5).add_to(m)
        for c in ruta:
            folium.Marker(coord[c], tooltip=c).add_to(m)
    return m._repr_html_()