FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update
RUN apt-get install -y --no-install-recommends git
RUN rm -rf /var/lib/apt/lists/*

COPY requirements/ requirements/

RUN pip install --user -r requirements/dev.txt
RUN pip install --user -r requirements/shared.txt

COPY app/ app/


FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

COPY app/ app/

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]