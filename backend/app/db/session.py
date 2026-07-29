from sqlmodel import SQLModel, Session, create_engine

from app.core.config import settings

engine = create_engine(settings.database_url, echo=False)


def init_db() -> None:
    """
    Cria as tabelas no banco caso ainda não existam.
    Em produção prefira usar as migrations do Alembic (pasta /alembic).
    Útil apenas para rodar rápido em desenvolvimento local.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency do FastAPI: entrega uma sessão de banco e garante que ela
    seja fechada ao final da requisição.
    """
    with Session(engine) as session:
        yield session
