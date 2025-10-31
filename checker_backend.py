
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
def check_account(email, senha):
    """Verifica conta com Selenium"""
    driver = None
    try:
        options = Options()
        # Modo headless para produção (sem interface gráfica)
        options.add_argument('--headless=new')
        options.add_argument('--window-size=1280,720')  # Menor resolução = menos memória
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Otimizações para economizar memória (importante em Nano instance)
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-images')  # Não carrega imagens
        options.add_argument('--disable-javascript')  # Site funciona sem JS
        options.add_argument('--single-process')
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-sync')
        options.add_argument('--metrics-recording-only')
        options.add_argument('--mute-audio')
        
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--log-level=3')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        options.page_load_strategy = 'eager'  # Não espera página carregar 100%
        
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(10)  # Timeout de 10s
        driver.get("https://www.pichau.com.br/customer/account/login")
        time.sleep(3)  # Reduzido de 7 para 3 segundos
        
        all_inputs = driver.find_elements(By.TAG_NAME, "input")
        
        # Se não achou inputs, aguarda mais
        if len(all_inputs) == 0:
            time.sleep(1.5)  # Reduzido de 3 para 1.5
            all_inputs = driver.find_elements(By.TAG_NAME, "input")
        
        # Pega campo email
        email_field = None
        for inp in all_inputs:
            if inp.get_attribute('name') == 'username' or inp.get_attribute('id') == 'username':
                email_field = inp
                break
        
        if not email_field:
            return 'ERRO|Campo de email não encontrado'
        
        # Preenche email (direto, sem delay)
        email_field.click()
        time.sleep(0.1)
        email_field.clear()
        email_field.send_keys(email)  # Envia tudo de uma vez
        time.sleep(0.2)
        
        # Preenche senha (direto, sem delay)
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_field.click()
        time.sleep(0.1)
        password_field.clear()
        password_field.send_keys(senha)  # Envia tudo de uma vez
        time.sleep(0.2)
        
        # Clica login
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        time.sleep(4)  # Reduzido de 7 para 4 segundos
        
        # Verifica resultado
        url = driver.current_url
        html = driver.page_source.lower()
        
        if '/login' in url:
            return 'REPROVADA|Login falhou'
        
        if '/account' in url:
            if 'sair' in html or 'logout' in html or 'pedidos' in html:
                # Tenta pegar nome do usuário
                try:
                    nome_elem = driver.find_element(By.XPATH, "//*[contains(text(), 'Olá') or contains(text(), 'Bem-vindo')]")
                    nome = nome_elem.text.replace('Olá,', '').replace('Bem-vindo,', '').strip()
                    return f'APROVADA|Nome: {nome}'
                except:
                    return 'APROVADA|Logado com sucesso'
            else:
                return 'REPROVADA|Não logou'
        
        return 'REPROVADA|Falhou'
        
    except Exception as e:
        return f'ERRO|{str(e)[:100]}'
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ERRO|Parâmetros insuficientes")
        sys.exit(1)
    
    email = sys.argv[1]
    senha = sys.argv[2]
    
    resultado = check_account(email, senha)
    print(resultado)
