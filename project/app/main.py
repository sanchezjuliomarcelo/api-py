# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

app = FastAPI()

class URLItem(BaseModel):
    url: str

@app.post("/scrape")
def scrape_website(url_item: URLItem):
    url = url_item.url

    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Actualizar la ubicación binaria de Chrome para Render
    chrome_options.binary_location = '/usr/bin/chromium-browser'

    # Configurar el WebDriver de Chrome
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Navegar al sitio web
        driver.get(url)

        # Esperar a que los elementos carguen
        time.sleep(5)

        # Encontrar todos los elementos de precio
        prices = driver.find_elements(By.CLASS_NAME, "vtex-product-price-1-x-sellingPrice")

        # Crear una lista para almacenar los datos
        data = []

        # Iterar a través de los elementos
        for price_element in prices:
            try:
                # Obtener el texto del precio
                price = price_element.text

                # Obtener el enlace del producto
                product_container = price_element.find_element(By.XPATH, "./ancestor::a")
                link = product_container.get_attribute("href")

                # Añadir los datos a la lista
                data.append({
                    "price": price,
                    "link": link
                })

            except Exception as e:
                print(f"Error al procesar el elemento: {e}")

        # Retornar los datos como respuesta
        return {"count": len(data), "data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Cerrar el navegador
        driver.quit()
