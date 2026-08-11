#!/bin/bash
echo "Iniciando Servidor Web FastAPI para SynthMind AI..."
uvicorn app:app --reload --host 0.0.0.0 --port 8000
