"""
Camada de Dominio, entidade Assinatura.
"""

from pydantic import BaseModel, Field


class AssinaturaCreate(BaseModel):
    assinante_nome: str = Field(..., min_length=3, max_length=100)
    kwh_contratados: float = Field(..., gt=0)
    desconto_percentual: float = Field(15.0, ge=0, le=100)
    usina_id: int = Field(..., gt=0)


class Assinatura(AssinaturaCreate):
    """Representacao completa de uma assinatura, como a API devolve."""

    id: int

    class Config:
        from_attributes = True
