# 開発用ステージ
FROM python:3.11-bullseye AS developer

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    bash=5.1-2+deb11u1 \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ビルドステージ
FROM python:3.11-bullseye AS builder
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 本番環境のDistrolessイメージを使用して最終イメージをビルド
FROM gcr.io/distroless/python3-debian12:nonroot AS production

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11

ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages
COPY --from=builder /app/ .

EXPOSE 8000

USER nonroot

CMD ["/app/opt/main.py"]
