FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY requirements-scanners.txt .
RUN pip install --no-cache-dir -r requirements-scanners.txt
COPY requirements-pyrit-langfuse.txt .
RUN pip install --no-cache-dir -r requirements-pyrit-langfuse.txt
COPY requirements-giskard.txt .
RUN python -m venv /opt/giskard-venv \
    && /opt/giskard-venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/giskard-venv/bin/pip install --no-cache-dir -r requirements-giskard.txt

ENV GISKARD_PYTHON=/opt/giskard-venv/bin/python

COPY . .
RUN chmod +x /app/scripts/start.sh

EXPOSE 8000

CMD ["sh", "/app/scripts/start.sh"]
