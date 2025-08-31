# ベースイメージとしてUbuntu 22.04を指定
FROM ubuntu:22.04

# タイムゾーン設定を自動化するための環境変数を設定
ENV DEBIAN_FRONTEND=noninteractive
# システムのロケールを設定
ENV LANG=C.UTF-8
ENV TZ=Asia/Tokyo

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    make \
    unzip \
    build-essential \
    zlib1g-dev \
    libssl-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    tzdata \
    ca-certificates \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxdamage1 \
    libgbm1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    && apt-get clean

# CA証明書を更新
RUN update-ca-certificates

# pyenvのインストール
RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv

# pyenvを使用するための環境変数を設定
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"

# Python 3.12のインストール
RUN pyenv install 3.12.0 && pyenv global 3.12.0

# PIPのアップグレードとPlaywrightのインストール
RUN pip install --no-cache-dir --upgrade pip && pip install playwright && playwright install

# Playwright以外ライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 作業ディレクトリの設定
WORKDIR /app

# アプリケーションコードをコピー
COPY src/ ./src/
COPY main.py .
COPY config/ ./config/

# デフォルトコマンドを設定（引数で制御可能）
CMD ["python", "main.py", "--headless"]
