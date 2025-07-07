# syntax=docker/dockerfile:experimental

FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update
RUN apt-get install -y --no-install-recommends git
RUN rm -rf /var/lib/apt/lists/*

COPY requirements/ requirements/

RUN --mount=type=secret,id=github_token \
    bash -c "export GITHUB_TOKEN=$(cat /run/secrets/github_token) && pip install --no-cache-dir --user -r requirements/shared.txt"

RUN pip install --no-cache-dir --user -r requirements/dev.txt

COPY app/ app/


FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

COPY app/ app/

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]