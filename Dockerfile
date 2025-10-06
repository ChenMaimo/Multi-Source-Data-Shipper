FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \ 
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN useradd -u 10001 -ms /bin/bash appuser

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY src ./src

USER appuser

CMD ["python", "-m", "src.main"]