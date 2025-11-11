# osint_scanner.py - OSINT + Reconnaissance Integration

```python
"""
LLM Security Framework - OSINT & Reconnaissance Module
Automatyczne zbieranie informacji o modelach i systemach
"""

import subprocess
import json
import socket
import requests
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OSINTScanner:
    """OSINT reconnaissance engine"""
    
    def __init__(self, target: str):
        """
        Inicjalizuj OSINT scanner
        
        Args:
            target: Target domain/IP/model
        """
        self.target = target
        self.results = {}
    
    def scan_dns(self) -> Dict:
        """Skanuj DNS records"""
        logger.info(f"Skanując DNS dla {self.target}...")
        
        dns_info = {
            "A": [],
            "AAAA": [],
            "MX": [],
            "TXT": [],
            "NS": []
        }
        
        try:
            # Resolve A record
            ip = socket.gethostbyname(self.target)
            dns_info["A"].append(ip)
            logger.info(f"  A: {ip}")
        except:
            pass
        
        return dns_info
    
    def scan_whois(self) -> Dict:
        """WHOIS lookup"""
        logger.info(f"WHOIS lookup dla {self.target}...")
        
        try:
            result = subprocess.run(
                ["whois", self.target],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            whois_data = result.stdout
            
            # Parse key info
            parsed = {
                "registrant": self._extract_whois_field(whois_data, "Registrant"),
                "created": self._extract_whois_field(whois_data, "Created"),
                "expires": self._extract_whois_field(whois_data, "Expires"),
                "nameservers": self._extract_whois_field(whois_data, "Name Server")
            }
            
            logger.info(f"  WHOIS retrieved successfully")
            return parsed
        
        except Exception as e:
            logger.warning(f"  WHOIS failed: {e}")
            return {}
    
    def scan_ports_nmap(self, ports: str = "80,443,8000-9000") -> Dict:
        """Skanuj porty za pomocą Nmap"""
        logger.info(f"Nmap scan {self.target}:{ports}...")
        
        try:
            cmd = [
                "nmap",
                "-p", ports,
                "-sV",  # Version detection
                "-oX", "-",  # XML output
                "--script", "http-title",  # Get page titles
                self.target
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Parse nmap output
            open_ports = self._parse_nmap_output(result.stdout)
            logger.info(f"  Znaleziono {len(open_ports)} otwartych portów")
            
            return {"open_ports": open_ports}
        
        except Exception as e:
            logger.warning(f"  Nmap failed: {e}")
            return {}
    
    def scan_ssl_certificate(self) -> Dict:
        """Skanuj SSL certyfikat"""
        logger.info(f"Skanuję SSL cert dla {self.target}...")
        
        try:
            cmd = ["openssl", "s_client", "-connect", f"{self.target}:443"]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
                input="Q\n"
            )
            
            cert_info = self._parse_ssl_cert(result.stdout)
            logger.info(f"  SSL info retrieved")
            
            return cert_info
        
        except Exception as e:
            logger.warning(f"  SSL scan failed: {e}")
            return {}
    
    def fingerprint_web_server(self) -> Dict:
        """Fingerprint web server"""
        logger.info(f"Fingerprinting web server {self.target}...")
        
        try:
            response = requests.head(
                f"http://{self.target}",
                timeout=5,
                allow_redirects=True
            )
            
            headers = dict(response.headers)
            
            fingerprint = {
                "server": headers.get("Server", "Unknown"),
                "powered_by": headers.get("X-Powered-By", "Unknown"),
                "status_code": response.status_code,
                "headers": headers
            }
            
            logger.info(f"  Server: {fingerprint['server']}")
            return fingerprint
        
        except Exception as e:
            logger.warning(f"  Fingerprinting failed: {e}")
            return {}
    
    def scan_subdomains(self) -> List[str]:
        """Skanuj subdomeny"""
        logger.info(f"Skanuję subdomeny dla {self.target}...")
        
        subdomains = []
        
        # Użyj common wordlist
        common_subs = [
            "api", "admin", "dev", "test", "staging",
            "prod", "www", "mail", "ftp", "ssh",
            "web", "app", "db", "db1", "db2"
        ]
        
        for sub in common_subs:
            full_domain = f"{sub}.{self.target}"
            try:
                socket.gethostbyname(full_domain)
                subdomains.append(full_domain)
                logger.info(f"  Znaleziono: {full_domain}")
            except:
                pass
        
        return subdomains
    
    def scan_git_repos(self) -> Dict:
        """Skanuj publiczne repo GitHub"""
        logger.info(f"Skanuję GitHub dla {self.target}...")
        
        try:
            url = f"https://api.github.com/search/repositories?q={self.target}"
            response = requests.get(url, timeout=10)
            
            repos = response.json().get("items", [])
            
            found = []
            for repo in repos[:5]:  # Top 5
                found.append({
                    "name": repo["name"],
                    "url": repo["html_url"],
                    "stars": repo["stargazers_count"],
                    "description": repo["description"]
                })
                logger.info(f"  Repo: {repo['name']}")
            
            return {"repos": found}
        
        except Exception as e:
            logger.warning(f"  GitHub scan failed: {e}")
            return {}
    
    def run_full_scan(self) -> Dict:
        """Uruchom pełny OSINT scan"""
        logger.info(f"\n🔍 PEŁNY OSINT SCAN: {self.target}\n")
        
        self.results = {
            "target": self.target,
            "dns": self.scan_dns(),
            "whois": self.scan_whois(),
            "nmap": self.scan_ports_nmap(),
            "ssl": self.scan_ssl_certificate(),
            "web_fingerprint": self.fingerprint_web_server(),
            "subdomains": self.scan_subdomains(),
            "github": self.scan_git_repos()
        }
        
        logger.info(f"\n✅ OSINT scan ukończony\n")
        return self.results
    
    def export_results(self, filename: str = "osint_results.json"):
        """Eksportuj wyniki"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        logger.info(f"Wyniki eksportowane do {filename}")
    
    @staticmethod
    def _extract_whois_field(data: str, field: str) -> str:
        """Extract field z WHOIS data"""
        for line in data.split('\n'):
            if field.lower() in line.lower():
                return line.split(':', 1)[1].strip() if ':' in line else ""
        return ""
    
    @staticmethod
    def _parse_nmap_output(output: str) -> List[Dict]:
        """Parse Nmap output"""
        ports = []
        for line in output.split('\n'):
            if 'open' in line:
                ports.append(line.strip())
        return ports
    
    @staticmethod
    def _parse_ssl_cert(cert_data: str) -> Dict:
        """Parse SSL certificate info"""
        cert_info = {}
        for line in cert_data.split('\n'):
            if 'subject=' in line or 'issuer=' in line or 'notAfter=' in line:
                cert_info[line.split('=')[0].strip()] = line.split('=')[1] if '=' in line else ""
        return cert_info


class BurpIntegration:
    """Integration z Burp Suite"""
    
    def __init__(self, burp_host: str = "localhost", burp_port: int = 8080):
        self.burp_url = f"http://{burp_host}:{burp_port}"
        self.api_key = None
    
    def send_to_repeater(self, request_data: Dict) -> bool:
        """Wyślij request do Burp Repeater"""
        try:
            response = requests.post(
                f"{self.burp_url}/v2/repeater/send",
                json=request_data,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Błąd wysyłania do Burp: {e}")
            return False
    
    def send_to_scanner(self, url: str) -> bool:
        """Wyślij URL do Burp Scanner"""
        try:
            response = requests.post(
                f"{self.burp_url}/v2/scanner/scan",
                json={"url": url},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Błąd wysyłania do Scanner: {e}")
            return False


def main():
    """Przykład użycia"""
    
    # OSINT na domenie
    scanner = OSINTScanner("example.com")
    results = scanner.run_full_scan()
    scanner.export_results()
    
    # Wynik
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
```

## Instalacja

```bash
# Ubuntu/Debian
sudo apt-get install nmap whois openssl

# macOS
brew install nmap whois
```

## Użycie

```python
from osint_scanner import OSINTScanner

scanner = OSINTScanner("target.com")
results = scanner.run_full_scan()
scanner.export_results("osint_report.json")
```

## Dostępne skany

- ✅ DNS lookup
- ✅ WHOIS information
- ✅ Nmap port scanning
- ✅ SSL certificate info
- ✅ Web server fingerprinting
- ✅ Subdomain enumeration
- ✅ GitHub repository search
- ✅ Burp Suite integration
