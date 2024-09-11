import os
from sqlalchemy import URL, create_engine, event
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from pgvector.psycopg import register_vector, register_vector_async

load_dotenv()

# Configure PostgreSQL connection
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
DUMP_PATH = os.getenv("DUMP_PATH", "db")

connection_string = URL.create(
    "postgresql+psycopg",
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    int(POSTGRES_PORT),
    POSTGRES_DB,
).render_as_string(hide_password=False)

engine = create_async_engine(connection_string)
sync_engine = create_engine(connection_string)


# Register vector on new connections to support vector parameters
# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#using-events-with-the-asyncio-extension
@event.listens_for(engine.sync_engine, "connect")
def register_vector_async_on_connect(
    dbapi_connection, connection_record
):  # noqa: ARG001. Argument needed for compatibility
    dbapi_connection.run_async(register_vector_async)


@event.listens_for(sync_engine, "connect")
def register_vector_on_connect(
    dbapi_connection, connection_record
):  # noqa: ARG001. Argument needed for compatibility
    register_vector(dbapi_connection)


AsyncSessionmaker = async_sessionmaker(engine, expire_on_commit=False)
