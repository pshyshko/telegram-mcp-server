from __future__ import annotations

import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.database.models.models import ItemDB  # nope

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

database_user = os.getenv("POSTGRES_USER", "user_db")
database_password = os.getenv("POSTGRES_PASSWORD", "host.docker.internal")
database_host = os.getenv("POSTGRES_HOST", "postgres_database")
database_port = os.getenv("POSTGRES_PORT", "5433")
database_name = os.getenv("POSTGRES_DB", "database_data")

database_url: str = (
    f"postgresql+asyncpg://{database_user}:{database_password}"
    f"@{database_host}:{database_port}/{database_name}"
)

database_url: str = (
    f"postgresql+psycopg2://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"
)

config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata


target_metadata = ItemDB.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
