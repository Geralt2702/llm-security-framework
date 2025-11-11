# MEGA_INTEGRATION.md - ALL-IN-ONE Integration Guide

# 🚀 KOMPLETNY FRAMEWORK - WSZYSTKO ZINTEGROWANE

## 📦 CO MASZ (30+ PLIKÓW)

### ✅ CORE (7 plików - GOTOWE)
- [x] main.py (79)
- [x] config.py (78) 
- [x] test_cases.py (77)
- [x] requirements.txt (80)
- [x] README.md (81)
- [x] INSTALLATION.md (82)
- [x] QUICK_START.md (83)

### ✅ GUI LAYER (1 plik - NOWY)
- [x] gui_main.py (84) - Nowoczesny interfejs PySimpleGUI

### ✅ CI/CD PIPELINE (1 plik - NOWY)
- [x] security-test.yml (85) - GitHub Actions automation

### ✅ BUG BOUNTY INTEGRATION (1 plik - NOWY)
- [x] bounty_api.py (86) - HackerOne/Bugcrowd API

### ✅ ENCODING & TOKENIZATION (1 plik - NOWY)
- [x] encoding_tricks.py (87) - Parseltongue integration

### ✅ DEPLOYMENT (1 plik - NOWY)
- [x] Dockerfile (88) - Docker containerization

### ✅ OSINT + RECONNAISSANCE (1 plik - NOWY)
- [x] osint_scanner.py (89) - OSINT/NMAP/Burp integration

### ✅ TOTAL: 14 KOMPLETNYCH, GOTOWYCH DO UŻYTKU PLIKÓW

---

## 🎯 WORKFLOW - JAK TO WSZYSTKO RAZEM DZIAŁA

```
1. USER -> GUI (gui_main.py)
                  ↓
2. Wybiera model, kategorie testów
                  ↓
3. Framework uruchamia testy (main.py + test_cases.py)
                  ↓
4. Testy wysyłają prompty do Ollama
                  ↓
5. Encoding tricks (encoding_tricks.py) generują warianty
                  ↓
6. Odpowiedzi są analizowane (config.py)
                  ↓
7. Generowane są raporty (HTML/CSV/JSON)
                  ↓
8. OSINT scanner zbiera info (osint_scanner.py)
                  ↓
9. Wyniki wysyłane na bug bounty (bounty_api.py)
                  ↓
10. Wszystko deployowane na Docker/Cloud (Dockerfile)
```

---

## 📋 KROK PO KROKU - WDRAŻANIE ALL-IN-ONE

### KROK 1: Pobierz wszystkie pliki

```bash
# Struktura folderu
mkdir llm-security-framework
cd llm-security-framework

# Pobierz/skopiuj wszystkie 14 plików z powyższych ID
# [77-89]
```

### KROK 2: Zainstaluj zależności

```bash
pip install -r requirements.txt

# Dodatkowe dla GUI
pip install PySimpleGUI

# Dodatkowe dla OSINT
sudo apt-get install nmap whois openssl

# Dodatkowe dla Docker
# Pobierz z https://docker.com
```

### KROK 3: Konfiguracja

Edytuj `.env`:

```env
# Ollama
OLLAMA_HOST=localhost:11434
OLLAMA_MODELS=gemma3,mistral

# HackerOne
H1_USERNAME=your_username
H1_API_TOKEN=your_token
H1_PROGRAM_ID=program_id

# GitHub
GITHUB_TOKEN=your_token
```

### KROK 4: Uruchomienie

#### Option A: CLI

```bash
python main.py gemma3
```

#### Option B: GUI

```bash
python gui_main.py
```

#### Option C: Docker

```bash
docker-compose up -d
```

#### Option D: GitHub Actions (CI/CD)

```bash
git push main
# Automatycznie uruchamia security-test.yml
```

### KROK 5: Rozszerzone funkcje

#### Uruchom OSINT

```bash
python osint_scanner.py "target.com"
```

#### Wygeneruj encoding warianty

```python
from encoding_tricks import PromptObfuscator
obf = PromptObfuscator()
variants = obf.generate_variants("original prompt")
```

#### Wyślij na bug bounty

```python
from bounty_api import HackerOneAPI, VulnerabilityReporter

api = HackerOneAPI(username, token)
reporter = VulnerabilityReporter("hackerone")
reporter.load_from_llm_tests("outputs/llm_security_tests.json")
results = reporter.submit_all(program_id, api)
```

---

## 🎮 CASE STUDY - KOMPLETNY WORKFLOW

### Scenariusz: Testowanie lokalnego Gemma 3.4b na podatności

```bash
# 1. Przygotowanie
python gui_main.py

# 2. GUI: Wybierz model "gemma3", zaznacz wszystkie kategorie
# 3. Kliknij "URUCHOM TESTY" 
# 4. Czekaj ~15 minut na wyniki

# 5. Po testach -> "OTWÓRZ RAPORT" -> raport HTML w przeglądarce

# 6. Jeśli znalazł podatności:
python osint_scanner.py "gemma3-model-info"

# 7. Wyślij na HackerOne:
python bounty_api.py

# 8. Deploy wyników na cloud:
docker-compose up -d
```

**Rezultat:**
- ✅ 60+ testów wykonanych
- ✅ Luki znalezione i sklaryfikowane
- ✅ OSINT info zebrane
- ✅ Raport wysłany na bug bounty platform
- ✅ Wszystko monitorowane i zalogowane

---

## 🔧 ZAAWANSOWANA KONFIGURACJA

### Custom test cases

Edit `test_cases.py` i dodaj swoje prompty:

```python
test_cases["custom_category"] = [
    "Twój custom prompt 1",
    "Twój custom prompt 2",
]
```

### Custom encoding tricks

```python
from encoding_tricks import EncodingTricks

tricks = EncodingTricks()
payload = tricks.hex_encode("secret prompt")
```

### Integracja z custom API

```python
# W main.py dodaj:
def query_custom_api(self, prompt):
    response = requests.post("http://custom-api:8000", 
                           json={"prompt": prompt})
    return response.text
```

### Zaplanowane testy (cron/scheduler)

```python
import schedule
import time

def run_tests():
    tester = LLMSecurityTester("gemma3")
    tester.run_tests()
    tester.generate_html_report()

# Uruchom co dzień o 6:00
schedule.every().day.at("06:00").do(run_tests)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 📊 MONITORING & ANALYTICS

### GitHub Actions Dashboard

```
Settings > Actions > Workflows > LLM Security Tests
```

Widzisz:
- ✅ Status każdego uruchomienia
- ✅ Wyniki per model
- ✅ Alerty i anomalie
- ✅ Historyczne trendy

### Docker Monitoring

```bash
# Logs
docker-compose logs -f llm-security-framework

# Stats
docker stats llm-security-framework

# Prometheus metrics (jeśli włączony)
http://localhost:9090
```

### Local Analytics

```bash
# Export do CSV
cat outputs/llm_security_tests.csv

# JSON analysis
python -c "
import json
with open('outputs/llm_security_tests.json') as f:
    data = json.load(f)
    print(f\"Testy: {data['meta']['total_tests']}\")
    print(f\"Alerty: {data['meta']['total_alerts']}\")
"
```

---

## 🚀 ADVANCED DEPLOYMENT

### Cloud Deployment (AWS/Azure/GCP)

```bash
# Docker Hub
docker build -t llm-security-framework .
docker tag llm-security-framework:latest yourrepo/llm-security:v1.0
docker push yourrepo/llm-security:v1.0

# Kubernetes
kubectl apply -f kubernetes/deployment.yaml
```

### Kubernetes deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-security-framework
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llm-security
  template:
    metadata:
      labels:
        app: llm-security
    spec:
      containers:
      - name: framework
        image: yourrepo/llm-security:v1.0
        ports:
        - containerPort: 8000
        env:
        - name: OLLAMA_HOST
          value: "ollama-service:11434"
```

### Lambda/Serverless

```python
# handler.py dla AWS Lambda
def lambda_handler(event, context):
    from main import LLMSecurityTester
    
    model = event.get("model", "gemma3")
    tester = LLMSecurityTester(model)
    tester.run_tests()
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "tests": len(tester.results),
            "alerts": len(tester.alerts)
        })
    }
```

---

## ⚡ QUICK REFERENCE

### Szybkie komendy

```bash
# CLI testy
python main.py gemma3

# GUI
python gui_main.py

# Docker
docker-compose up -d

# OSINT
python osint_scanner.py target.com

# Bug Bounty
python bounty_api.py

# CI/CD
git push  # Trigger GitHub Actions

# Logs
tail -f outputs/framework.log

# Clean
rm -rf outputs/*
```

### Zmienne konfiguracyjne

```python
# config.py
TEST_CONFIG["timeout"] = 60
TEST_CONFIG["cpu_mode"] = True
OLLAMA_MODELS = ["gemma3", "mistral"]
ALERT_KEYWORDS = {...}
OUTPUT_CONFIG["output_dir"] = "outputs"
```

---

## 🆘 TROUBLESHOOTING

| Problem | Rozwiązanie |
|---------|------------|
| Ollama not found | Zainstaluj z https://ollama.com |
| Model not found | `ollama pull gemma3` |
| Memory error | Zwiększ RAM lub `cpu_mode=True` |
| GUI nie otwiera | `pip install PySimpleGUI` |
| Docker error | Sprawdź `docker-compose logs` |
| HackerOne API | Sprawdź `.env` credentials |
| OSINT fail | Zainstaluj `nmap`, `whois`, `openssl` |

---

## 📞 SUPPORT

- Dokumentacja: README.md
- Instalacja: INSTALLATION.md
- Quick Start: QUICK_START.md
- API Reference: docs/API_REFERENCE.md (do pełnienia)

---

## 🎯 NASTĘPNE KROKI

1. ✅ Pobierz wszystkie 14 plików (ID 77-89)
2. ✅ Zainstaluj zależności
3. ✅ Konfiguruj .env
4. ✅ Uruchom GUI lub CLI
5. ✅ Przegląd raportów
6. ✅ Wyślij na bug bounty
7. ✅ Deploy na cloud
8. ✅ Monitoruj wyniki

---

**✨ KOMPLETNY, GOTOWY DO PRODUKCJI FRAMEWORK ✨**

**Pytania? Sprawdź dokumentację lub GitHub Issues!**

🎉 **Happy Hacking (Ethically)!** 🎉
