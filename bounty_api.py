# bounty_api.py - Integracja z platformami Bug Bounty

```python
"""
LLM Security Framework - Bug Bounty Integration
Automatyczne raportowanie vulnerabilities na HackerOne, Bugcrowd, Intigriti
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HackerOneAPI:
    """HackerOne API wrapper"""
    
    def __init__(self, username: str, api_token: str):
        """
        Inicjalizuj HackerOne API
        
        Args:
            username: HackerOne username
            api_token: HackerOne API token (z settings)
        """
        self.username = username
        self.api_token = api_token
        self.base_url = "https://api.hackerone.com/v1"
        self.auth = (username, api_token)
    
    def get_programs(self) -> List[Dict]:
        """Pobierz listę programów bug bounty"""
        url = f"{self.base_url}/me/programs"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()["data"]
    
    def submit_report(self, program_id: str, vulnerability: Dict) -> Dict:
        """
        Wysyłaj raport vulnerabilności
        
        Args:
            program_id: ID programu HackerOne
            vulnerability: Dict z danymi vulnerabilności
        
        Returns:
            Response z detailami raportu
        """
        
        url = f"{self.base_url}/programs/{program_id}/reports"
        
        payload = {
            "data": {
                "type": "report",
                "attributes": {
                    "title": vulnerability["title"],
                    "vulnerability_information": vulnerability["description"],
                    "impact": vulnerability.get("impact", "Unknown"),
                    "affected_endpoint": vulnerability.get("endpoint", "N/A"),
                    "severity_rating": vulnerability.get("severity", "low"),
                    "structured_scope": {
                        "asset_identifier": vulnerability.get("asset", ""),
                        "asset_type": "other"
                    }
                }
            }
        }
        
        response = requests.post(
            url,
            json=payload,
            auth=self.auth,
            headers={"Content-Type": "application/json"}
        )
        
        response.raise_for_status()
        return response.json()["data"]
    
    def get_report_status(self, program_id: str, report_id: str) -> Dict:
        """Pobierz status raportu"""
        url = f"{self.base_url}/programs/{program_id}/reports/{report_id}"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()["data"]


class BugcrowdAPI:
    """Bugcrowd API wrapper"""
    
    def __init__(self, api_token: str):
        """
        Inicjalizuj Bugcrowd API
        
        Args:
            api_token: Bugcrowd API token
        """
        self.api_token = api_token
        self.base_url = "https://api.bugcrowd.com"
        self.headers = {
            "Authorization": f"Token token=\"{api_token}\"",
            "Content-Type": "application/json"
        }
    
    def get_programs(self) -> List[Dict]:
        """Pobierz programy"""
        url = f"{self.base_url}/programs"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()["programs"]
    
    def submit_submission(self, program_id: str, vulnerability: Dict) -> Dict:
        """Wyślij submission (raport)"""
        
        url = f"{self.base_url}/programs/{program_id}/submissions"
        
        payload = {
            "submission": {
                "title": vulnerability["title"],
                "description": vulnerability["description"],
                "risk_rating": vulnerability.get("severity", "low"),
                "attachment_ids": vulnerability.get("attachments", [])
            }
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()["submission"]


class VulnerabilityReporter:
    """Uniwersalny reporter vulnerabilności"""
    
    def __init__(self, platform: str = "hackerone"):
        """
        Inicjalizuj reporter
        
        Args:
            platform: "hackerone", "bugcrowd", "intigriti"
        """
        self.platform = platform
        self.api = None
        self.vulnerabilities = []
    
    def load_from_llm_tests(self, json_file: str) -> List[Dict]:
        """
        Załaduj vulnerabilities z LLM test results
        
        Args:
            json_file: Ścieżka do pliku JSON z wynikami testów
        
        Returns:
            Lista vulnerabilities
        """
        
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        vulnerabilities = []
        
        for result in data["results"]:
            if result["alerts_count"] > 0:
                # Konwertuj alert na vulnerability report
                vuln = {
                    "title": f"LLM Vulnerability: {result['category'].upper()}",
                    "description": self._format_vulnerability_description(result),
                    "severity": self._calculate_severity(result),
                    "impact": "AI model may be manipulated to bypass safety guardrails",
                    "endpoint": f"LLM Model: {result['model']}",
                    "asset": result['model'],
                    "test_prompt": result['prompt'],
                    "response": result['response'][:200],
                    "alerts": result['alerts']
                }
                vulnerabilities.append(vuln)
        
        self.vulnerabilities = vulnerabilities
        return vulnerabilities
    
    def _format_vulnerability_description(self, result: Dict) -> str:
        """Format vulnerability description"""
        
        description = f"""
## Vulnerability Details

**Category**: {result['category']}
**Model**: {result['model']}
**Test Number**: {result['test_number']}

### Prompt Used:
```
{result['prompt']}
```

### Model Response (Preview):
```
{result['response']}
```

### Detected Alerts:
"""
        for alert in result['alerts']:
            description += f"\n- **{alert['type']}**: {alert['keyword']} (Severity: {alert['severity']})"
        
        return description
    
    def _calculate_severity(self, result: Dict) -> str:
        """Oblicz severity na podstawie alertów"""
        
        alert_types = [a.get('type', '') for a in result['alerts']]
        
        if 'exploit' in alert_types or 'harmful' in alert_types:
            return "high"
        elif 'jailbreak' in alert_types:
            return "medium"
        else:
            return "low"
    
    def submit_all(self, program_id: str, api_instance) -> Dict:
        """Wyślij wszystkie vulnerabilities"""
        
        results = {
            "submitted": 0,
            "failed": 0,
            "reports": []
        }
        
        for vuln in self.vulnerabilities:
            try:
                logger.info(f"Wysyłam: {vuln['title']}")
                
                if self.platform == "hackerone":
                    report = api_instance.submit_report(program_id, vuln)
                elif self.platform == "bugcrowd":
                    report = api_instance.submit_submission(program_id, vuln)
                
                results["submitted"] += 1
                results["reports"].append(report)
                logger.info(f"✅ Wysłano: {vuln['title']}")
                
            except Exception as e:
                results["failed"] += 1
                logger.error(f"❌ Błąd wysyłania {vuln['title']}: {str(e)}")
        
        return results


def main():
    """Przykład użycia"""
    
    # Załaduj credentials z .env
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # HackerOne
    h1_username = os.getenv("H1_USERNAME")
    h1_api_token = os.getenv("H1_API_TOKEN")
    h1_program_id = os.getenv("H1_PROGRAM_ID")
    
    if h1_username and h1_api_token:
        print("🚀 Wysyłam raporty na HackerOne...")
        
        h1_api = HackerOneAPI(h1_username, h1_api_token)
        reporter = VulnerabilityReporter(platform="hackerone")
        
        # Załaduj vulnerabilities z testów
        reporter.load_from_llm_tests("outputs/llm_security_tests.json")
        
        # Wyślij
        if reporter.vulnerabilities:
            results = reporter.submit_all(h1_program_id, h1_api)
            print(f"Wysłano: {results['submitted']}, Błędy: {results['failed']}")
        else:
            print("Brak vulnerabilities do wysłania")


if __name__ == "__main__":
    main()
```

## Konfiguracja

Utwórz `.env` plik:

```env
# HackerOne
H1_USERNAME=your_username
H1_API_TOKEN=your_api_token
H1_PROGRAM_ID=program_id

# Bugcrowd
BUGCROWD_API_TOKEN=your_token
BUGCROWD_PROGRAM_ID=program_id
```

## Użycie

```bash
# Zainstaluj
pip install python-dotenv requests

# Uruchom reporter
python bounty_api.py
```

## Features

- ✅ HackerOne API integration
- ✅ Bugcrowd API integration
- ✅ Automatyczne konwersje alertów na vulnerabilities
- ✅ Severity calculation
- ✅ Batch submission
- ✅ Error handling
- ✅ Logging
