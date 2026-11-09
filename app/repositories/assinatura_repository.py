"""
Camada de Persistencia, repositorios de Assinatura.
"""

from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.db.database import SessionLocal
from app.db.models import AssinaturaModel
from app.domain.assinatura import Assinatura, AssinaturaCreate


class AssinaturaRepository(Protocol):
    def listar(self) -> list[Assinatura]: ...
    def buscar_por_id(self, assinatura_id: int) -> Assinatura | None: ...
    def criar(self, dados: AssinaturaCreate) -> Assinatura: ...
    def remover(self, assinatura_id: int) -> bool: ...


class InMemoryAssinaturaRepository:
    def __init__(self) -> None:
        self._assinaturas: dict[int, Assinatura] = {}
        self._proximo_id: int = 1

    def listar(self) -> list[Assinatura]:
        return list(self._assinaturas.values())

    def buscar_por_id(self, assinatura_id: int) -> Assinatura | None:
        return self._assinaturas.get(assinatura_id)

    def criar(self, dados: AssinaturaCreate) -> Assinatura:
        assinatura = Assinatura(id=self._proximo_id, **dados.model_dump())
        self._assinaturas[assinatura.id] = assinatura
        self._proximo_id += 1
        return assinatura

    def remover(self, assinatura_id: int) -> bool:
        if assinatura_id not in self._assinaturas:
            return False
        del self._assinaturas[assinatura_id]
        return True


class SqlAssinaturaRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def listar(self) -> list[Assinatura]:
        with self._session_factory() as session:
            modelos = session.scalars(select(AssinaturaModel).order_by(AssinaturaModel.id)).all()
            return [Assinatura.model_validate(m) for m in modelos]

    def buscar_por_id(self, assinatura_id: int) -> Assinatura | None:
        with self._session_factory() as session:
            modelo = session.get(AssinaturaModel, assinatura_id)
            return Assinatura.model_validate(modelo) if modelo else None

    def criar(self, dados: AssinaturaCreate) -> Assinatura:
        with self._session_factory() as session:
            modelo = AssinaturaModel(**dados.model_dump())
            session.add(modelo)
            session.commit()
            session.refresh(modelo)
            return Assinatura.model_validate(modelo)

    def remover(self, assinatura_id: int) -> bool:
        with self._session_factory() as session:
            modelo = session.get(AssinaturaModel, assinatura_id)
            if modelo is None:
                return False
            session.delete(modelo)
            session.commit()
            return True


assinatura_repository: AssinaturaRepository = SqlAssinaturaRepository(SessionLocal)
