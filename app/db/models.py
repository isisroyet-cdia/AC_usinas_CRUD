"""
Modelos do SQLAlchemy: cada classe e uma tabela do banco.

Atencao: estes NAO sao os modelos do Dominio. Os modelos Pydantic de
app/domain continuam sendo o que a API recebe e devolve. Estes aqui
descrevem apenas como os dados ficam guardados.
"""

from datetime import date

from sqlalchemy import Date, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class UsinaModel(Base):
    __tablename__ = "usinas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    localizacao: Mapped[str] = mapped_column(String(100))
    capacidade_geracao_kwh: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(20), default="ativa")
    data_ativacao: Mapped[date] = mapped_column(Date)
    potencia_instalada_kwp: Mapped[float | None] = mapped_column(Float, nullable=True)

    assinaturas: Mapped[list["AssinaturaModel"]] = relationship(back_populates="usina")


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(100))
    perfil: Mapped[str] = mapped_column(String(20), default="operador")


class AssinaturaModel(Base):
    """
    Exemplo de chave estrangeira: cada assinatura pertence a uma usina.
    Um assinante da Bulbe recebe creditos de energia gerados por ela.
    """

    __tablename__ = "assinaturas"

    id: Mapped[int] = mapped_column(primary_key=True)
    assinante_nome: Mapped[str] = mapped_column(String(100))
    kwh_contratados: Mapped[float] = mapped_column(Float)
    desconto_percentual: Mapped[float] = mapped_column(Float, default=15.0)
    usina_id: Mapped[int] = mapped_column(ForeignKey("usinas.id"))

    usina: Mapped["UsinaModel"] = relationship(back_populates="assinaturas")
