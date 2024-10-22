from typing import List, Optional

from pydantic import BaseModel


class PCalculatorRawMaterials(BaseModel):
    raw_material_id: int
    quantity: float


class PCalculatorRequestContract(BaseModel):
    stage_id: int
    pelet: bool
    target_value: float
    target_type: str
    raw_materials: List[PCalculatorRawMaterials]
    concentration: Optional[float]
    digestibility: Optional[float]
    cost: Optional[float]
