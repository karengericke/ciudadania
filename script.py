from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import datetime
import os
from PIL import ImageGrab
import time
import random

# URL de Prenotami
url = 'https://prenotami.esteri.it/Services'

# Ruta local donde se almacenarán las capturas
screenshot_path = r'C:\Users\Kmger\OneDrive\Bureau\karenina\ciudadania\capturas'

# Credenciales, cambiar por tus credenciales personales
username = "YOUR_USER"
password = "YOUR_PASSWORD"

def type_slowly(element, text):
    """Escribe texto lentamente para simular ingreso manual."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.2, 0.5))

def save_screenshot_with_taskbar(lang, crop_top=120):
    """
    Toma una captura de pantalla completa usando Pillow (ImageGrab).
    Luego recorta la parte superior 'crop_top' píxeles (para omitir la barra del navegador).
    El archivo final se llama: captura_{lang}_YYYYmmdd_HHMMSS.png
    """
    # 1. Capturar la pantalla completa
    screenshot = ImageGrab.grab()
    
    # 2. Definir el recorte (left, upper, right, lower)
    #    - left: 0
    #    - upper: crop_top (la cantidad de px a eliminar de arriba)
    #    - right: screenshot.width
    #    - lower: screenshot.height
    width, height = screenshot.size
    cropped_screenshot = screenshot.crop((0, crop_top, width, height))
    
    # 3. Guardar la captura con el nombre deseado
    filename = f"captura_{lang}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    full_path = os.path.join(screenshot_path, filename)
    cropped_screenshot.save(full_path)
    
    print(f"Captura {lang} guardada en: {full_path}")
    return full_path

def main():
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
    driver.maximize_window()

    try:
        # 1) Ingresar a Prenotami
        driver.get(url)
        time.sleep(5)

        # 2) Completar email
        email_field = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
        )
        type_slowly(email_field, username)

        # 3) Completar password
        password_field = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        type_slowly(password_field, password)

        # 4) Botón "Avanti"
        WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(), 'Avanti')]"))
        ).click()

        # Esperar que la tabla o la página cargue
        time.sleep(5)

        # 5) Clic en "Prenota" del segundo renglón de la tabla (versión ITA)
        xpath_prenota_segundo_ita = "(//table//tr)[3]//button[contains(text(), 'Prenota')]"
        WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, xpath_prenota_segundo_ita))
        ).click()

        # Esperar que la tabla o la página cargue
        time.sleep(5)

        # 6) Tomar la captura de pantalla de ITA, recortando 120px de arriba
        save_screenshot_with_taskbar("ITA", crop_top=120)

        # 7) Volver a la página principal
        driver.get(url)
        time.sleep(5)

        # 8) Clic en el botón "SPA"
        spa_button = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/Language/ChangeLanguage?lang=13')]"))
        )
        spa_button.click()

        # Esperar para asegurarnos de que el cambio de idioma se aplique
        time.sleep(5)

        # 9) Clic en "RESERVAR" del segundo renglón de la tabla (versión SPA)
        xpath_reservar_segundo_spa = "(//table//tr)[3]//button[contains(text(), 'Reservar')]"
        WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, xpath_reservar_segundo_spa))
        ).click()

        # Esperar que la tabla o la página cargue
        time.sleep(5)

        # 10) Tomar la captura de pantalla de SPA, recortando 120px de arriba
        save_screenshot_with_taskbar("SPA", crop_top=120)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
