from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def descargar_pagina_selenium(url, tiempo_espera=10):
    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz gráfica)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Inicializar el navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Cargar la página
        driver.get(url)

        # Esperar a que el cuerpo de la página esté presente
        WebDriverWait(driver, tiempo_espera).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Dar tiempo adicional para que se cargue el contenido dinámico
        time.sleep(2)

        # Obtener el contenido de la página
        contenido = driver.page_source

        return contenido

    except Exception as e:
        print(f"Error al descargar la página: {e}")
        return None

    finally:
        # Cerrar el navegador
        driver.quit()


if __name__ == '__main__':
    # Ejemplo de uso
    url = "https://www.ejemplo.com"
    contenido = descargar_pagina_selenium(url)

    if contenido:
        print("Contenido descargado con éxito.")
        # Aquí puedes procesar o guardar el contenido
        # Por ejemplo, guardar en un archivo:
        with open("pagina.html", "w", encoding="utf-8") as f:
            f.write(contenido)
    else:
        print("No se pudo descargar el contenido.")
