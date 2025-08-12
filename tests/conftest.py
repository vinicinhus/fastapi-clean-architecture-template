import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

from app.api.v1.routes import auth
from app.core.security import get_password_hash
from app.db.seed.role_seed import init_roles
from app.db.session import get_session
from app.enums.role import RoleID
from app.main import app
from app.models.user import User

DATABASE_URL = "sqlite:///:memory:"
engine_test = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    """
    Cria o schema e inicializa roles no banco de testes.
    Executa uma vez por sessão de testes.
    """
    SQLModel.metadata.create_all(engine_test)
    with Session(engine_test) as session:
        init_roles(session)
    yield
    SQLModel.metadata.drop_all(engine_test)


@pytest.fixture
def session():
    """
    Sessão do banco de testes isolada para cada teste.
    """
    with Session(engine_test) as session:
        yield session


@pytest.fixture
def client(session):
    """
    Configura o TestClient sobrescrevendo a sessão de banco.
    """

    def override_get_session():
        return session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def mock_current_user_admin(session: Session):
    """
    Cria ou retorna usuário ADMIN para autenticação.
    """
    test_user = session.exec(
        select(User).where(User.email == "test_user@example.com")
    ).first()

    if not test_user:
        test_user = User(
            username="test_user",
            email="test_user@example.com",
            hashed_password=get_password_hash("test123"),
            full_name="Test User",
            is_active=True,
            role_id=RoleID.ADMIN,
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)

    def _override_get_current_user():
        return test_user

    app.dependency_overrides[auth.get_current_user] = _override_get_current_user
    yield test_user
    app.dependency_overrides.pop(auth.get_current_user, None)
