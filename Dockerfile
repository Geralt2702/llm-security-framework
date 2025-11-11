# Dockerfile - Docker container dla frameworka

```dockerfile
# Multi-stage build dla minimalnego finału

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Zainstaluj system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Skopiuj requirements
COPY requirements.txt .

# Zainstaluj Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Zainstaluj runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Zainstaluj Ollama
RUN curl https://ollama.ai/install.sh | sh

# Skopiuj Python packages z builder stage
COPY --from=builder /root/.local /root/.local

# Skopiuj aplikację
COPY . .

# Utwórz output directory
RUN mkdir -p outputs

# Expose port (dla potential API)
EXPOSE 8000

# Environment
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV OLLAMA_HOST=0.0.0.0:11434

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:11434 || exit 1

# Entrypoint
CMD ["/bin/bash", "-c", "ollama serve & sleep 5 && python main.py"]
```

## docker-compose.yml - Multi-container setup

```yaml
version: '3.9'

services:
  # Główny framework
  llm-security-framework:
    build:
      context: .
      dockerfile: Dockerfile
    image: llm-security-framework:latest
    container_name: llm-security-framework
    
    environment:
      - OLLAMA_HOST=ollama:11434
      - PYTHONUNBUFFERED=1
      - TZ=Europe/Warsaw
    
    ports:
      - "8000:8000"
    
    volumes:
      - ./outputs:/app/outputs
      - ./test_cases.py:/app/test_cases.py
      - ./config.py:/app/config.py
    
    depends_on:
      - ollama
    
    networks:
      - llm-network
    
    restart: unless-stopped
  
  # Ollama service (LLM backend)
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
    
    ports:
      - "11434:11434"
    
    volumes:
      - ollama-data:/root/.ollama
    
    networks:
      - llm-network
    
    restart: unless-stopped
    
    # GPU support (jeśli masz NVIDIA GPU)
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: all
    #           capabilities: [gpu]
  
  # PostgreSQL dla raportów (opcjonalnie)
  postgres:
    image: postgres:15-alpine
    container_name: llm-security-db
    
    environment:
      - POSTGRES_USER=llm_security
      - POSTGRES_PASSWORD=secure_password
      - POSTGRES_DB=llm_security
    
    ports:
      - "5432:5432"
    
    volumes:
      - postgres-data:/var/lib/postgresql/data
    
    networks:
      - llm-network
    
    restart: unless-stopped
  
  # Prometheus dla monitoring (opcjonalnie)
  prometheus:
    image: prom/prometheus:latest
    container_name: llm-security-prometheus
    
    ports:
      - "9090:9090"
    
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    
    networks:
      - llm-network
    
    restart: unless-stopped

volumes:
  ollama-data:
  postgres-data:
  prometheus-data:

networks:
  llm-network:
    driver: bridge
```

## Użycie

### Uruchomienie z Docker

```bash
# Build image
docker build -t llm-security-framework .

# Run container
docker run -v $(pwd)/outputs:/app/outputs \
           -e OLLAMA_MODELS="gemma3" \
           llm-security-framework
```

### Uruchomienie z Docker Compose

```bash
# Start all services
docker-compose up -d

# Sprawdź logi
docker-compose logs -f llm-security-framework

# Zatrzymaj
docker-compose down
```

### Pobieranie modeli w container

```bash
# SSH do container
docker exec -it ollama ollama pull gemma3
docker exec -it ollama ollama pull mistral

# Lub w docker-compose
docker exec llm-security-framework ollama pull gemma3
```

### Monitoring

- Framework: http://localhost:8000
- Ollama: http://localhost:11434
- Prometheus: http://localhost:9090 (jeśli włączony)

## GPU Support

Jeśli chcesz GPU (NVIDIA):

1. Zainstaluj nvidia-docker:
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
```

2. Odkomentuj sekcję `deploy` w docker-compose.yml

3. Uruchom:
```bash
docker-compose up -d
```
