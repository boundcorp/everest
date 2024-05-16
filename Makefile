run:
	rm everest/.watchdog.lock || true && docker compose up -d && poetry run runserver
