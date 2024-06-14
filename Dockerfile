FROM python:3.12-slim

WORKDIR /app
RUN curl -fsSL https://ollama.com/install.sh | sh

RUN pip install git+https://github.com/VictorGoubet/techsage.git

COPY . /app/

EXPOSE 8501

CMD ["poetry", "run", "launch-sage"]
