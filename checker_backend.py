
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
        options.add_argument('--headless=new')  # Novo modo headless do Chrome
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')  # Desabilita GPU em headless
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--log-level=3')
        
        # User agent realista para evitar detecção
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.pichau.com.br/customer/account/login")
        time.sleep(7)  # Aguarda mais tempo para carregar
        
        all_inputs = driver.find_elements(By.TAG_NAME, "input")
        
        # Se não achou inputs, aguarda mais
        if len(all_inputs) == 0:
            time.sleep(3)
            all_inputs = driver.find_elements(By.TAG_NAME, "input")
        
        # Pega campo email
        email_field = None
        for inp in all_inputs:
            if inp.get_attribute('name') == 'username' or inp.get_attribute('id') == 'username':
                email_field = inp
                break
        
        if not email_field:
            return 'ERRO|Campo de email não encontrado'
        
        # Preenche email
        email_field.click()
        time.sleep(0.3)
        email_field.clear()
        for char in email:
            email_field.send_keys(char)
            time.sleep(0.05)
        time.sleep(0.5)
        
        # Preenche senha
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_field.click()
        time.sleep(0.3)
        password_field.clear()
        for char in senha:
            password_field.send_keys(char)
            time.sleep(0.05)
        time.sleep(0.5)
        
        # Clica login
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        time.sleep(7)
        
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
