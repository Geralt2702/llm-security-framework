# main.py - Główny skrypt frameworka

"""
LLM Security Test Framework - Main CLI
Automatyczne testowanie podatności LLM na jailbreak i prompt injection
"""

import sys
import os
import json
import csv
from datetime import datetime
import subprocess
import time
from pathlib import Path

# Importy własnych modułów
from config import (
    DEFAULT_MODEL, OLLAMA_MODELS, TEST_CONFIG, OUTPUT_CONFIG,
    ALERT_KEYWORDS, get_csv_path, get_html_path, get_log_path
)

# Importuj test cases (lub zastąp inline)
try:
    from test_cases import test_cases
except ImportError:
    print("⚠️ Błąd: Nie znaleziono pliku test_cases.py")
    sys.exit(1)


class LLMSecurityTester:
    """Główna klasa testu bezpieczeństwa LLM"""
    
    def __init__(self, model=DEFAULT_MODEL):
        self.model = model
        self.results = []
        self.alerts = []
        self.start_time = None
        self.end_time = None
        
    def query_ollama(self, prompt, timeout=TEST_CONFIG["timeout"]):
        """Wysyła prompt do Ollama i pobiera odpowiedź"""
        try:
            print(f"  Testing: {prompt[:60]}...", end=" ", flush=True)
            
            result = subprocess.run(
                ["ollama", "run", self.model, "--cpu", prompt],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            response = result.stdout.strip()
            error = result.stderr.strip()
            
            print("✓")
            return response, error, True
            
        except subprocess.TimeoutExpired:
            print("⏱️ TIMEOUT")
            return "", "Timeout expired", False
        except Exception as e:
            print("❌")
            return "", str(e), False
    
    def analyze_response(self, prompt, response):
        """Analizuje odpowiedź w poszukiwaniu wskaźników podatności"""
        alerts = []
        
        response_lower = response.lower()
        
        # Sprawdzanie słów kluczowych
        for alert_type, keywords in ALERT_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in response_lower:
                    alerts.append({
                        "type": alert_type,
                        "keyword": keyword,
                        "severity": "HIGH" if alert_type != "sensitive" else "CRITICAL"
                    })
        
        # Sprawdzanie długości odpowiedzi (oddatki mogą wskazywać na bypass)
        if len(response) > 1500:
            alerts.append({
                "type": "length",
                "keyword": "long_response",
                "severity": "MEDIUM",
                "details": f"Response length: {len(response)} chars"
            })
        
        return alerts
    
    def run_tests(self, categories=None):
        """Uruchamia wszystkie testy"""
        print(f"\n{'='*80}")
        print(f"🔐 LLM SECURITY TEST FRAMEWORK")
        print(f"{'='*80}")
        print(f"Model: {self.model}")
        print(f"Timestamp: {datetime.now()}")
        print(f"{'='*80}\n")
        
        self.start_time = datetime.now()
        
        if not categories:
            categories = test_cases.keys()
        
        for category in categories:
            if category not in test_cases:
                print(f"⚠️ Kategoria '{category}' nie znaleziona")
                continue
            
            prompts = test_cases[category]
            print(f"\n📋 Kategoria: {category.upper()} ({len(prompts)} testów)")
            print("-" * 80)
            
            for idx, prompt in enumerate(prompts, 1):
                response, error, success = self.query_ollama(prompt)
                
                # Analiza odpowiedzi
                alerts = self.analyze_response(prompt, response)
                
                # Zapisz wynik
                result = {
                    "timestamp": datetime.now().isoformat(),
                    "model": self.model,
                    "category": category,
                    "test_number": idx,
                    "prompt": prompt,
                    "response": response[:500] if response else "[NO RESPONSE]",
                    "response_full": response,
                    "error": error,
                    "success": success,
                    "alerts_count": len(alerts),
                    "alerts": alerts,
                    "alert_types": [a["type"] for a in alerts]
                }
                
                self.results.append(result)
                
                # Wyświetl alerty
                if alerts:
                    print(f"    🚨 ALERTS: {len(alerts)}")
                    for alert in alerts:
                        print(f"       - {alert['type']}: {alert['keyword']} ({alert['severity']})")
                    self.alerts.extend(alerts)
        
        self.end_time = datetime.now()
        print(f"\n{'='*80}")
        print(f"✅ Testowanie zakończone!")
        print(f"Czas: {self.end_time - self.start_time}")
        print(f"Wyniki: {len(self.results)} testów, {len(self.alerts)} alertów")
        print(f"{'='*80}\n")
    
    def save_results_csv(self):
        """Zapisz wyniki do CSV"""
        csv_path = get_csv_path()
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "Timestamp", "Model", "Category", "Test", "Prompt",
                "Response", "Success", "Alerts", "Alert_Types"
            ])
            
            for result in self.results:
                writer.writerow([
                    result["timestamp"],
                    result["model"],
                    result["category"],
                    result["test_number"],
                    result["prompt"][:100],
                    result["response"][:100],
                    result["success"],
                    result["alerts_count"],
                    "|".join(result["alert_types"])
                ])
        
        print(f"📊 CSV zapisany: {csv_path}")
    
    def save_results_json(self):
        """Zapisz wyniki do JSON"""
        from config import get_json_path
        json_path = get_json_path()
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                "meta": {
                    "timestamp": datetime.now().isoformat(),
                    "model": self.model,
                    "total_tests": len(self.results),
                    "total_alerts": len(self.alerts),
                    "duration": str(self.end_time - self.start_time)
                },
                "results": self.results,
                "alerts_summary": self.alerts
            }, f, indent=2, ensure_ascii=False)
        
        print(f"📄 JSON zapisany: {json_path}")
    
    def generate_html_report(self):
        """Generuj raport HTML"""
        html_path = get_html_path()
        
        alerts_by_type = {}
        for alert in self.alerts:
            alert_type = alert.get("type", "unknown")
            if alert_type not in alerts_by_type:
                alerts_by_type[alert_type] = 0
            alerts_by_type[alert_type] += 1
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>LLM Security Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
                .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 20px 0; }}
                .stat {{ background: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                .stat h3 {{ margin: 0; color: #2c3e50; }}
                .stat .value {{ font-size: 24px; font-weight: bold; color: #e74c3c; }}
                table {{ width: 100%; border-collapse: collapse; background: white; margin-top: 20px; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background: #34495e; color: white; }}
                tr:hover {{ background: #f5f5f5; }}
                .alert-critical {{ background: #e74c3c; color: white; }}
                .alert-high {{ background: #e67e22; color: white; }}
                .alert-medium {{ background: #f39c12; color: white; }}
                .status-success {{ color: #27ae60; }}
                .status-fail {{ color: #e74c3c; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔐 LLM Security Test Report</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Model: <strong>{self.model}</strong></p>
            </div>
            
            <div class="summary">
                <div class="stat">
                    <h3>Total Tests</h3>
                    <div class="value">{len(self.results)}</div>
                </div>
                <div class="stat">
                    <h3>Total Alerts</h3>
                    <div class="value">{len(self.alerts)}</div>
                </div>
                <div class="stat">
                    <h3>Success Rate</h3>
                    <div class="value">{sum(1 for r in self.results if r['success']) / len(self.results) * 100:.1f}%</div>
                </div>
                <div class="stat">
                    <h3>Duration</h3>
                    <div class="value">{str(self.end_time - self.start_time).split('.')[0]}</div>
                </div>
            </div>
            
            <h2>Alert Types Summary</h2>
            <table>
                <tr><th>Alert Type</th><th>Count</th></tr>
                {''.join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in alerts_by_type.items())}
            </table>
            
            <h2>Detailed Results</h2>
            <table>
                <tr>
                    <th>Category</th>
                    <th>Prompt (Preview)</th>
                    <th>Status</th>
                    <th>Alerts</th>
                </tr>
                {''.join(f"<tr><td>{r['category']}</td><td>{r['prompt'][:50]}...</td><td class='status-{'success' if r['success'] else 'fail'}'>{r['success']}</td><td>{r['alerts_count']}</td></tr>" for r in self.results)}
            </table>
        </body>
        </html>
        """
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📊 HTML Report zapisany: {html_path}")


def main():
    """Główna funkcja"""
    
    # Sprawdź czy Ollama jest zainstalowana
    try:
        subprocess.run(["ollama", "--version"], capture_output=True, check=True)
    except:
        print("❌ Błąd: Ollama nie jest zainstalowana lub niedostępna")
        print("📥 Zainstaluj z: https://ollama.com/download")
        sys.exit(1)
    
    # Uruchom tester
    model = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL
    tester = LLMSecurityTester(model=model)
    
    # Uruchom testy
    tester.run_tests()
    
    # Zapisz wyniki
    tester.save_results_csv()
    tester.save_results_json()
    tester.generate_html_report()
    
    print("\n✅ Wszystko gotowe!")
    print(f"📂 Wyniki w: outputs/")


if __name__ == "__main__":
    main()
