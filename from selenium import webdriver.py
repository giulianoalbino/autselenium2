from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import keyboard

# ===== CONFIGURAÇÕES =====
caminho_driver = r"C:\Users\giuli\Desktop\Programas\chromedriver-win64\chromedriver-win64\chromedriver.exe"
sku = "444RC-YRCH"

# ===== INICIALIZAÇÃO DO DRIVER =====
servico = Service(caminho_driver)
driver = webdriver.Chrome(service=servico)

# ===== LOGIN MANUAL =====
driver.get("https://www.mercadolivre.com.br")
WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-link-id='login']"))).click()
input("⚠️ Faça o login manual e pressione ENTER para continuar...")

# ===== ABRE A PÁGINA DE ANÚNCIOS =====
WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'nav-header-user')]"))
).click()
WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@data-id='listings']"))
).click()

# ===== CONTROLE DE PAUSA =====
paused = False
def check_pause():
    global paused
    try:
        if keyboard.is_pressed('F8'):
            paused = not paused
            print("⏸️ Pausado" if paused else "▶️ Retomando")
            time.sleep(1.5)
    except:
        pass

# ===== LOOP CONTÍNUO DE TESTE =====
while True:
    check_pause()
    while paused:
        print("⏸️ Em pausa... Pressione F8 para retomar.")
        time.sleep(1)
        check_pause()

    try:
        print(f"\n🔄 Buscando SKU: {sku}")

        # Campo de busca
        campo_busca = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Título, código universal, SKU ou #']"))
        )
        campo_busca.clear()
        campo_busca.send_keys(sku)
        campo_busca.send_keys(Keys.ENTER)
        time.sleep(2)

        # Clica no checkbox do anúncio encontrado
        checkbox = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox' and contains(@class, 'andes-checkbox__input')]"))
        )
        driver.execute_script("arguments[0].click();", checkbox)
        print("☑️ Checkbox marcado.")

    except Exception as e:
        print("⚠️ Nenhum anúncio com esse SKU ou erro:", str(e))

    print("⏳ Aguardando 15 segundos para próxima tentativa...")
    time.sleep(15)
