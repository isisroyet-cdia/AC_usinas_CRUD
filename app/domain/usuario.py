from enum import Enum

from pydantic import BaseModel, Field


class PerfilUsuario(str, Enum):
    operador = "operador"
    administrador = "administrador"


class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    email: str = Field(..., pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", description="Email do usuario")
    senha: str = Field(..., min_length=8, max_length=72, description="Minimo de 8 caracteres")
    perfil: PerfilUsuario = PerfilUsuario.operador


class Usuario(BaseModel):
    id: int
    nome: str
    email: str
    perfil: PerfilUsuario


class UsuarioInterno(Usuario):
    senha_hash: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
