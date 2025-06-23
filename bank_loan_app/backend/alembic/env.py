from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database import engine
from models import SQLModel

# this is the Alembic Config object
config = context.config
# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Подставляем metadata наших моделей
target_metadata = SQLModel.metadata

def run_migrations_offline():
    url = engine.url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
