from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class StatusUsina(str, Enum):
    ativa = "ativa"
    em_manutencao = "em_manutencao"
    inativa = "inativa"


class UsinaBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100, description="Nome da usina solar")
    localizacao: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Cidade e estado, ex: Uberlandia, MG",
    )
    capacidade_geracao_kwh: float = Field(..., gt=0, description="Capacidade de geracao em kWh")
    status: StatusUsina = StatusUsina.ativa


class UsinaCreate(UsinaBase):
    pass


class UsinaUpdate(BaseModel):
    nome: str | None = Field(None, min_length=3, max_length=100)
    localizacao: str | None = Field(None, min_length=3, max_length=100)
    capacidade_geracao_kwh: float | None = Field(None, gt=0)
    status: StatusUsina | None = None


class Usina(UsinaBase):
    id: int
    data_ativacao: date

    class Config:
        from_attributes = True
