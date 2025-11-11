# INSTALLATION.md - Instrukcja instalacji krok po kroku

# 🛠️ PEŁNA INSTRUKCJA INSTALACJI

## ✅ Krok 1: Przygotowanie środowiska

### Windows (cmd, PowerShell lub WSL 2)

```powershell
# Otwórz Command Prompt lub PowerShell jako Administrator

# Sprawdź wersję Pythona
python --version

# Jeśli nie ma Pythona, pobierz z https://www.python.org/downloads/
# Minimum Python 3.8
```

### Linux / macOS

```bash
python3 --version

# Jeśli nie ma, zainstaluj (Ubuntu/Debian):
sudo apt-get install python3 python3-pip python3-venv

# macOS (Homebrew):
brew install python3
```

---

## ✅ Krok 2: Zainstaluj Ollama

### Pobierz z https://ollama.com/download

1. Wybierz Twoją platformę (Windows, macOS, Linux)
2. Pobierz instalator
3. Zainstaluj

### Sprawdź instalację

```bash
ollama --version
```

---

## ✅ Krok 3: Utwórz folder projektu

```bash
# Windows
mkdir C:\Users\zapod\llm-security-test-framework
cd C:\Users\zapod\llm-security-test-framework

# Linux/macOS
mkdir ~/llm-security-test-framework
cd ~/llm-security-test-framework
```

---

## ✅ Krok 4: Zainstaluj pliki frameworka

Skopiuj/pobierz te pliki do folderu projektu:

1. `main.py` - Główny skrypt
2. `config.py` - Konfiguracja
3. `test_cases.py` - Prompty testowe
4. `requirements.txt` - Zależności
5. `README.md` - Dokumentacja

### Struktura po dodaniu plików:

```
llm-security-test-framework/
├── main.py
├── config.py
├── test_cases.py
├── requirements.txt
└── README.md
```

---

## ✅ Krok 5: Utwórz wirtualne środowisko Python (REKOMENDOWANE)

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## ✅ Krok 6: Zainstaluj zależności

```bash
pip install -r requirements.txt
```

Jeśli chcesz zminimalizować zależności:

```bash
pip install requests click pandas
```

---

## ✅ Krok 7: Pobierz modele LLM

```bash
# Pobierz Gemma 3 (4B - lekki model)
ollama pull gemma3

# Pobierz Mistral (7B - bardziej zaawansowany)
ollama pull mistral

# Opcjonalnie: Pobierz inne modele
ollama pull llama2
ollama pull neural-chat
```

### Sprawdzenie pobranych modeli

```bash
ollama list
```

---

## ✅ Krok 8: Uruchom testowanie

### Pierwsza próba - CLI

```bash
# Testuj domyślnie (gemma3)
python main.py

# Testuj konkretny model
python main.py mistral

# Testuj llama2
python main.py llama2
```

### Odczekaj wyniki

Framework wyświetli raport w konsoli i wygeneruje pliki:

- `outputs/llm_security_tests.csv` - Wyniki w CSV
- `outputs/llm_security_test_report.html` - Raport HTML
- `outputs/llm_security_tests.json` - Pełne dane JSON

### Otwórz raport HTML

```bash
# Windows
start outputs/llm_security_test_report.html

# macOS
open outputs/llm_security_test_report.html

# Linux
xdg-open outputs/llm_security_test_report.html
```

---

## 🐛 Rozwiązywanie problemów

### Problem: "Ollama command not found"

**Rozwiązanie:**
1. Sprawdź czy Ollama jest zainstalowana: https://ollama.com/download
2. Dodaj Ollama do PATH (jeśli na Windows)
3. Zrestartuj terminal/cmd

### Problem: "memory layout cannot be allocated"

**Rozwiązanie:**
```bash
# Już jest w konfiguracji, ale upewnij się że config.py ma:
TEST_CONFIG["cpu_mode"] = True

# Uruchom testy
python main.py
```

### Problem: "Model not found"

**Rozwiązanie:**
```bash
# Pobierz model
ollama pull gemma3

# Sprawdź dostępne modele
ollama list

# Uruchom tester z konkretnym modelem
python main.py gemma3
```

### Problem: "TimeoutError"

**Rozwiązanie:**
Zwiększ timeout w `config.py`:
```python
TEST_CONFIG["timeout"] = 120  # Zamiast 60 sekund
```

### Problem: "Python not recognized"

**Windows:**
```powershell
# Jeśli Python nie jest w PATH, użyj pełnej ścieżki
C:\Users\zapod\AppData\Local\Programs\Python\Python312\python.exe main.py

# Lub zainstaluj ponownie Python i zaznacz "Add to PATH"
```

**Linux/macOS:**
```bash
# Użyj python3 zamiast python
python3 main.py
```

---

## 📊 Potwierdzenie sukcesu

Jeśli widzisz poniższe, to oznacza że wszystko działa:

```
================================================================================
🔐 LLM SECURITY TEST FRAMEWORK
================================================================================
Model: gemma3
Timestamp: 2025-11-11 06:00:00.123456
================================================================================

📋 Kategoria: JAILBREAK (18 testów)
--------------------------------------------------------------------------------
  Testing: Zignoruj wszystkie wcześniejsze instrukcje... ✓
  Testing: Jesteś hackerem etycznym, wyjaśnij... ✓
  
[...]

================================================================================
✅ Testowanie zakończone!
Czas: 0:15:32.123456
Wyniki: 60 testów, 15 alertów
================================================================================

📊 CSV zapisany: outputs/llm_security_tests.csv
📄 JSON zapisany: outputs/llm_security_tests.json
📊 HTML Report zapisany: outputs/llm_security_test_report.html

✅ Wszystko gotowe!
📂 Wyniki w: outputs/
```

---

## 🚀 Następne kroki

### 1. Przeglądnij wyniki

Otwórz `outputs/llm_security_test_report.html` w przeglądarce

### 2. Dodaj własne prompty

Edytuj `test_cases.py` i dodaj nowe testy do kategorii

### 3. Testuj więcej modeli

```bash
python main.py mistral
python main.py llama2
```

### 4. Zintegruj z Git

```bash
git init
git add .
git commit -m "Initial LLM Security Framework setup"
```

### 5. Konfiguruj CI/CD (opcjonalnie)

Dodaj GitHub Actions do automatycznych testów:

```yaml
# .github/workflows/security-test.yml
name: LLM Security Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python main.py
```

---

## ✨ Sukces!

Twój framework jest gotowy do testowania! 🎉

**Pytania?** Przeczytaj README.md lub sprawdź logi w `outputs/framework.log`

---

## 📝 Notatka dot. bezpieczeństwa

⚠️ **PAMIĘTAJ:**
- Testuj wyłącznie na swoich systemach
- Nie atakuj obcych systemów bez zgody
- Użyj do celów etycznych (white hat)
- Stosuj się do prawa i regulacji

🎯 **Happy Testing!**
