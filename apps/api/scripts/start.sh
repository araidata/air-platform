#!/usr/bin/env sh
set -eu

python - <<'PY'
import time

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings

for attempt in range(1, 31):
    try:
        engine = create_engine(settings.database_url, pool_pre_ping=True)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Database connection validated.")
        break
    except SQLAlchemyError as exc:
        if attempt == 30:
            raise
        print(f"Waiting for database ({attempt}/30): {exc}")
        time.sleep(2)
PY

alembic upgrade head

SHOULD_RUN_SEED="${RUN_SEED:-}"
if [ -z "${SHOULD_RUN_SEED}" ]; then
  if [ "${ENVIRONMENT:-development}" = "development" ]; then
    SHOULD_RUN_SEED="true"
  else
    SHOULD_RUN_SEED="false"
  fi
fi

if [ "${SHOULD_RUN_SEED}" = "true" ]; then
  echo "Development/demo bootstrap enabled; running seed phases."
  python -m app.seed.run_seed
else
  echo "Development/demo bootstrap disabled; skipping seed phases."
fi

UVICORN_ARGS=""
if [ "${ENVIRONMENT:-development}" = "development" ] && [ "${API_RELOAD:-true}" = "true" ]; then
  UVICORN_ARGS="--reload"
fi

exec uvicorn app.main:app \
  --host "${API_HOST:-0.0.0.0}" \
  --port "${API_PORT:-8000}" \
  ${UVICORN_ARGS}
