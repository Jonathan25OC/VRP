from pydantic import BaseModel
from typing import Dict, Tuple

class VRPRequest(BaseModel):
    coord: Dict[str, Tuple[float, float]]
    pedidos: Dict[str, int]
    almacen: Tuple[float, float]
    max_carga: int