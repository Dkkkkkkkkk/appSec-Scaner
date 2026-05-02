#!/usr/bin/env python3
"""
AppSec Scanner - Utilitário de Auditoria de Cabeçalhos de Segurança Web
Desenvolvido para análise rápida de segurança de aplicações.
"""

import requests
import sys


SECURITY_HEADERS = {
    "X-Frame-Options": {
        "expected": ["DENY", "SAMEORIGIN"],
        "desc": "Protege contra ataques de Clickjacking."
    },
    "X-Content-Type-Options": {
        "expected": ["nosniff"],
        "desc": "Evita o 'MIME sniffing' impedindo o navegador de interpretar arquivos como diferentes do declarado."
    },
    "Strict-Transport-Security": {
        "expected": ["max-age="],
        "desc": "Garante a comunicação segura apenas via HTTPS (HSTS)."
    },
    "Content-Security-Policy": {
        "expected": ["default-src"],
        "desc": "Mitiga ataques de Cross-Site Scripting (XSS) e injeção de dados."
    }
}


GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

def print_banner():
    
    banner = r"""
  ___          ____            ____                                
 / _ \ _ __   / ___|  ___  ___/ ___|  ___ __ _ _ __  _ __   ___ _ __ 
| | | | '_ \  \___ \ / _ \/ __\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
| |_| | |_) |  ___) |  __/ (__ ___) | (_| (_| | | | | | | |  __/ |   
 \___/| .__/  |____/ \___|\___|____/ \___\__,_|_| |_|_| |_|\___|_|   
      |_|                                                            
    """
    print(f"{CYAN}{banner}{RESET}")
    print(f" {GREEN}v1.0{RESET} | Ferramenta de Auditoria AppSec | {YELLOW}@fernandes.dev{RESET}\n")

def analyze_url(target_url):
    
  if not target_url.startswith("http"):
        
        target_url = "https://" + target_url

    print(f"[*] Iniciando auditoria de segurança em: {CYAN}{target_url}{RESET}\n")

    try:
        
        headers_request = {
            'User-Agent': 'AppSecScanner/1.0 (@fernandes audit tool)'
        }
        
        response = requests.get(target_url, headers=headers_request, timeout=10, allow_redirects=True)
        headers = response.headers
        
        
        if response.url != target_url and response.url != target_url + "/":
             print(f"[*] Redirecionado para: {CYAN}{response.url}{RESET}")

        print(f"[✓] Conexão estabelecida. Status Code: {response.status_code}\n")
        print("="*75)
        print(f"{'CABEÇALHO':<32} | {'STATUS':<12} | AVALIAÇÃO")
        print("="*75)

        for header_name, rules in SECURITY_HEADERS.items():
            actual_value = headers.get(header_name)
            
            if actual_value:
                 
                is_secure = any(rule in actual_value for rule in rules["expected"])
                status = "SEGURO" if is_secure else "INCOMPLETO"
                status_color = GREEN if is_secure else YELLOW
                
                
                display_value = actual_value if len(actual_value) < 30 else actual_value[:27] + "..."
                
                print(f"{header_name:<32} | {status_color}{status:<12}{RESET} | {rules['desc']}")
                if not is_secure:
                     print(f"  {YELLOW}-> Valor encontrado:{RESET} {display_value}")
            else:
                print(f"{header_name:<32} | {RED}MISSING    {RESET} | Ausente! {rules['desc']}")
        
        print("="*75)
        print(f"\n{GREEN}[✓] Auditoria concluída.{RESET}")
        
    except requests.exceptions.MissingSchema:
         print(f"{RED}[!] Erro:{RESET} URL inválida. Certifique-se de usar um formato válido (ex: exemplo.com ou https://exemplo.com).")
    except requests.exceptions.ConnectionError:
         print(f"{RED}[!] Erro:{RESET} Não foi possível conectar ao alvo {target_url}. Verifique se a URL está correta e se você tem conexão com a internet.")
    except requests.exceptions.Timeout:
         print(f"{RED}[!] Erro:{RESET} A requisição para {target_url} expirou (timeout). O servidor pode estar lento ou fora do ar.")
    except requests.exceptions.RequestException as e:
        print(f"{RED}[!] Erro genérico ao conectar ao alvo:{RESET} {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        print_banner()
    else:
        print_banner()
        try:
            target = input(f"Digite a URL ou o alvo para auditoria (ex: example.com): {CYAN}")
            print(f"{RESET}", end="") 
        except EOFError: 
            print(f"{RESET}\n[!] Execução interrompida pelo usuário.")
            sys.exit(0)
    
    if target:
        analyze_url(target)
    else:
        print(f"{RED}[!] Erro:{RESET} Nenhum alvo fornecido.")
      
