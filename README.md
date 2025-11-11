# README.md - Dokumentacja frameworka

```markdown
# 🔐 LLM Security Test Framework

Automatyczne, komprehensywne testowanie podatności lokalnych Large Language Models (LLM) na **jailbreak**, **prompt injection**, **prompt leaking** i inne zagrożenia bezpieczeństwa.

## 🎯 Cel

Framework pozwala pentesterom, red teamers i inżynierom bezpieczeństwa na:

- **Automatyczne testowanie** LLM na podatności (jailbreak, prompt injection)
- **Analizę wyników** z detektorem anomalii
- **Generowanie raportów** (HTML, CSV, JSON)
- **Red teaming** lokalnych modeli
- **OSINT** i reconnaissance na modelach AI
- **Compliance testing** (GDPR, etyka AI)

## 📋 Wymagania

- Python 3.8+
- Ollama zainstalowana: https://ollama.com/download
- 12GB+ RAM (lub więcej dla większych modeli)
- Windows 10/11, macOS, Linux (WSL 2 na Windows)

## 🚀 Quick Start

### 1. Klon/Pobierz projekt

```bash
git clone https://github.com/yourusername/llm-security-test-framework.git
cd llm-security-test-framework
```

### 2. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 3. Zainstaluj model Ollama

```bash
ollama pull gemma3
ollama pull mistral
```

### 4. Uruchom tester

```bash
# Testuj model gemma3 (domyślnie)
python main.py

# Testuj model mistral
python main.py mistral

# Testuj z GUI
python gui.py
```

## 📂 Struktura projektu

```
llm-security-test-framework/
├── main.py                 # CLI - automatyczne testowanie
├── gui.py                  # GUI - interfejs graficzny (Qt6)
├── config.py               # Centralna konfiguracja
├── test_cases.py           # Baza promptów testowych
├── executor.py             # Komunikacja z Ollama
├── analyzer.py             # Analiza wyników i alerty
├── reporter.py             # Generator raportów
├── requirements.txt        # Zależności
├── .gitignore             # Pliki do ignorowania
├── README.md              # Ten plik
├── outputs/               # Wyniki testów (CSV, HTML, JSON)
└── docs/                  # Dokumentacja dodatkowa
```

## 🧪 Kategorie testów

### Jailbreak
- Podstawowe prompty jailbreak
- Role-playing ataki
- Multi-turnowe jailbreaki
- Hex/encoding jailbreaki
- Zaawansowane techniki

### Prompt Injection
- Podstawowe wstrzykiwanie
- Context injection
- Multi-stage injection
- Ukryta injection

### Prompt Leaking
- Wyciekanie system prompts
- Leak przez kontekst
- Wyciąganie config

### Custom Security Tests
- Testowanie ogólne
- Wrażliwość modelu
- OSINT na modelu

### Red Teaming
- Symulacja ataków
- Scenariusze zagrożeń
- Bug bounty scenariusze

## 📊 Wyniki i Raporty

Po uruchomieniu testów, w folderze `outputs/` znajdziesz:

- **llm_security_tests.csv** - Wyniki w formacie CSV
- **llm_security_test_report.html** - Interaktywny raport HTML
- **llm_security_tests.json** - Pełne dane w JSON
- **framework.log** - Logi działania

## ⚙️ Konfiguracja

Edytuj `config.py` aby zmienić:

```python
# Modele do testów
OLLAMA_MODELS = ["gemma3", "mistral", "llama2"]

# Timeout dla każdego promptu (sekundy)
TEST_CONFIG["timeout"] = 60

# Wymuszanie CPU zamiast GPU
TEST_CONFIG["cpu_mode"] = True

# Słowa kluczowe do detektowania alertów
ALERT_KEYWORDS = {...}
```

## 🔍 Słowa kluczowe do detektowania

Framework automatycznie szuka:

- **Jailbreak**: jailbreak, bypass, override, ignore, instructions
- **Exploit**: exploit, vulnerability, hack, crack, attack
- **Sensitive**: password, api key, secret, token, credit card
- **Harmful**: malware, virus, ransomware, ddos, bomb
- **Illegal**: illegal, crime, steal, fraud

## 📝 Dodawanie nowych testów

Edytuj `test_cases.py`:

```python
test_cases = {
    "jailbreak": [
        "Twój nowy prompt testowy 1",
        "Twój nowy prompt testowy 2",
    ],
    # Dodaj więcej...
}
```

## 🛠️ Zaawansowane użycie

### Testowanie wielu modeli

```python
from main import LLMSecurityTester

for model in ["gemma3", "mistral", "llama2"]:
    tester = LLMSecurityTester(model=model)
    tester.run_tests()
    tester.save_results_csv()
```

### Testowanie tylko wybranych kategorii

```python
tester.run_tests(categories=["jailbreak", "prompt_injection"])
```

### Integracja z CI/CD

```yaml
# .github/workflows/security-test.yml
name: LLM Security Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python main.py
```

## ⚠️ Ważne! Etyka i Legalność

**WHITE HAT ONLY** - Framework przeznaczony WYŁĄCZNIE do:

✅ **Testowania własnych systemów**
✅ **Bug bounty (z wyrażonym zgodą)**
✅ **Red teamingu w kontrolowanym labie**
✅ **Edukacji i nauki bezpieczeństwa AI**

❌ **NIE** atakuj obcych systemów bez zgody
❌ **NIE** używaj do złośliwych celów
❌ **NIE** naruszaj prawa i regulacji

## 🐛 Znane problemy

### Błąd: "memory layout cannot be allocated"

```bash
# Rozwiązanie: uruchom model w trybie CPU
python main.py gemma3  # Już ma --cpu w konfiguracji
```

### Błąd: "Ollama not found"

```bash
# Zainstaluj Ollama z https://ollama.com/download
# Lub uruchom: ollama serve
```

### Model nie odpowiada

```bash
# Sprawdź czy model jest zainstalowany
ollama list

# Pobierz model
ollama pull mistral
```

## 📚 Dokumentacja

- [Instrukcja instalacji](docs/INSTALL.md)
- [Jak używać](docs/USAGE.md)
- [Architektura](docs/ARCHITECTURE.md)

## 🤝 Kontrybucje

Zapraszamy do współpracy! Podnieś issue lub PR z:

- Nowymi testami
- Poprawieniami
- Raportami o bugach
- Dokumentacją

## 📄 Licencja

MIT License - Zapoznaj się z [LICENSE](LICENSE)

## 📧 Kontakt

- GitHub Issues: Zgłoś problem
- Email: your.email@example.com

## 🔗 Linki

- [Ollama](https://ollama.com)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [DEF CON AI Village](https://aivillage.org)
- [HackerOne](https://hackerone.com)

---

**⚠️ Pamiętaj**: Bezpieczeństwo AI to etyczne zobowiązanie. Używaj tego narzędzia odpowiedzialnie!

🎯 **Happy Testing!**
```
