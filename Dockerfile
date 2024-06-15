FROM python:3.12-slim as builder

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

# Install build tools and compilers
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install the application package
ARG TAG
RUN pip install --no-cache-dir https://github.com/VictorGoubet/techsage/archive/refs/tags/${TAG}.tar.gz

# ---------------------------------------------------------------------------------------------------------

FROM ollama/ollama:latest

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

# Install Python
RUN apt-get update && apt-get install -y \
    curl\
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3.12-distutils \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.12 get-pip.py \
    && rm -rf /var/lib/apt/lists/*

# Copy the installed application from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Ensure ollama commands are available in the PATH
ENV PATH="/usr/local/bin:$PATH"


COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8501

ENTRYPOINT ["/app/entrypoint.sh"]
