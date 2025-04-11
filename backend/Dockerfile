FROM ghcr.io/astral-sh/uv:python3.13-alpine

ADD uv.lock pyproject.toml /app/
WORKDIR /app

RUN uv sync --frozen
ENV PATH="/app/.venv/bin:$PATH"

ADD . /app

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c" , "fastapi run"]
