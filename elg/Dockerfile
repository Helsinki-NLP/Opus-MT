FROM opus-mt-base:latest

WORKDIR /usr/src/app

COPY server.py content_processor.py apply_bpe.py elg_server.py services.json ./
COPY models ./models

EXPOSE 8888
CMD ["venv/bin/python3", "elg_server.py", "-c", "services.json", "-p", "8888"]
