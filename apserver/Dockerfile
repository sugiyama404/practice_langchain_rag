# 開発用ステージ
FROM python:3.11-bookworm AS developer

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ビルドステージ
FROM python:3.11-bookworm AS builder
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
