#!/bin/bash

chmod +x start.sh

# Iniciar la aplicación con Gunicorn y Uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
