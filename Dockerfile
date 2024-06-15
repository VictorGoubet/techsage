FROM ollama/ollama:latest
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

# Install python 3.12, python3.12-dev, and build tools
RUN apt-get update && apt-get install -y \
    curl \
    software-properties-common \
    build-essential \
    g++ \
    coreutils \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    python3.12-distutils \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.12 get-pip.py \
    && rm -rf /var/lib/apt/lists/*

    

# Install app (default version is v1)
ARG TAG=v1
RUN pip install https://github.com/VictorGoubet/techsage/archive/refs/tags/${TAG}.tar.gz
RUN pip show techsage
EXPOSE 8501

CMD ["sleep", "infinity"]
