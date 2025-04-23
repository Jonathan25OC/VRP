# VRP API - Optimización de Rutas

## Cómo usar

1. Instala las dependencias:
```
pip install -r requirements.txt
```

2. Corre el servidor:
```
uvicorn app.main:app --reload
```

3. Prueba la API en: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Endpoints

- `POST /optimizar-rutas`: Calcula rutas optimizadas
- `POST /mapa`: Devuelve HTML con mapa de rutas