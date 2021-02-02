FROM opus-mt:latest

COPY . .

# Write the service configuration
RUN set -eux; \
	venv/bin/python3 write_configuration.py > services.json;

EXPOSE 8888
CMD ["venv/bin/python3", "elg_server.py", "-c", "services.json", "-p", "8888"]
