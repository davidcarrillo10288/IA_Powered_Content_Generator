import requests
from bs4 import BeautifulSoup
import re
import os
from scr.image_describer import ImageGridDescriber
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait

class FalabellaScraper:
    def __init__(self, url):
        # Inicializar el scraper con la URL y obtener el HTML
        self.url = url
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        self.soup = self._get_soup()  # Obtén el contenido HTML al inicializar la clase
        # print("Contenido HTML cargado:", self.soup)
        # print(self.soup.prettify()[:1000])

    def get_html_content(self):
        # service = Service(ChromeDriverManager().install())
        # chrome_options = Options()
        chrome_options = Options()
        chrome_options.binary_location = os.getenv("CHROME_BIN")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--enable-unsafe-swiftshader")
        chrome_options.add_argument("--enable-logging")
        chrome_options.add_argument("--v=1")
        chrome_options.add_argument('--headless')  # Debe ejecutarse en modo headless en entornos como Colab
        chrome_options.add_argument('--no-sandbox')  # Requerido para Colab/Linux
        chrome_options.add_argument('--disable-dev-shm-usage')

        service = Service(executable_path=os.getenv("CHROMEDRIVER_BIN"))

        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(self.url)
            # print("⌛ Esperando que cargue el contenedor de productos...")


            # Uncomment and update this section in get_html_content()
            # print("⌛ Waiting for page to load...")
            # WebDriverWait(driver, 15).until(
            #     EC.presence_of_element_located((By.TAG_NAME, "body"))
            # )

            print("✅ Contenido dinámico cargado.")
            html_content = driver.page_source
            driver.quit()
        except Exception as e:
            print(f"An Error Occurred during Selenium execution: {e}")
            html_content = None
        return html_content

    def _get_soup(self):
        # Obtiene el contenido HTML y lo parseamos con BeautifulSoup
        html_content = self.get_html_content()
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            # print(soup)
            return soup
        else:
            return None

    def get_product_name(self):
        # Example method for students to follow
        if self.soup:
            name_tag = self.soup.find("h1", class_="jsx-783883818 product-name fa--product-name false")
            if name_tag:
              return name_tag.text
            else:
              return "No se pudo obtener el nombre del producto"
        else:
            return "No se pudo obtener el nombre del producto"

    def get_product_price(self):
        # TODO: Find and extract the product price from the parsed HTML
        if self.soup:
            producto = self.soup.find("div", id=re.compile(r"^testId-pod-prices-\d+"))
            precios = producto.find_all("li", class_=re.compile(r'prices-\d+'))

            if len(precios) == 2:
                discount_price = precios[0].text.strip().split()[-1]
                data_internet_price = precios[0].text.strip().split()[-2]
                data_normal_price = precios[1].text.replace(" ","")
                return [data_internet_price, discount_price, data_normal_price]
            elif len(precios) == 3:
                discount_price = precios[0].text.strip().split()[-1]
                data_cmr_price = precios[0].text.strip().split()[-2]
                data_internet_price = precios[1].text.replace(" ","")
                data_normal_price = precios[2].text.replace(" ","")
                return [data_cmr_price, data_internet_price, discount_price, data_normal_price]
            elif len(precios) == 1:
                data_internet_price = precios[0].text.strip().split()[-1]
                return [data_internet_price]
            else:
                return []

    def get_image_links(self):
        # TODO: Find all image tags and extract their source links
        if self.soup:
            images_url = self.soup.find_all('img', class_="jsx-2487856160")
            return [x.get('src').replace('thumbnail', 'w=800,h=800,fit=pad') for x in images_url]
        else:
            return []

    def get_product_specifications(self):
        # TODO: Extract product specifications from the HTML table
        if self.soup:
            especificaciones = {}
            specifications = self.soup.find("table", class_="jsx-960159652 specification-table")
            for fila in specifications.find_all("tr"):
                celdas = fila.find_all("td")
                if len(celdas) == 2:
                    nombre = celdas[0].get_text(strip=True)
                    valor = celdas[1].get_text(strip=True)
                    especificaciones[nombre] = valor
                else:
                    return {}
            return especificaciones

    def get_additional_info(self):
        # TODO: Extract additional product information from the HTML
        return None

    def get_available_sizes(self):
        # TODO: Extract available sizes for the product
        if self.soup:
            sizes = self.soup.find_all('button', class_="jsx-3027654667 size-button rebranded enhanced-size-selector")
            return [x.text for x in sizes]
        else:
            return []

    def get_image_description(self):
        # TODO: Use the ImageGridDescriber to concatenate images and generate a description
        img_describer = ImageGridDescriber()
        image_links = self.get_image_links()
        concatenated_image = img_describer.concatenate_images_square(image_links)
        description = img_describer.get_image_description(concatenated_image)
        return description

    def scrape(self):
        # TODO: Scrape all relevant product data and return it as a dictionary
        return {
            'title': self.get_product_name(),
            'price': self.get_product_price(),
            'description': self.get_product_specifications(),
            'available_sizes': self.get_available_sizes(),
            'additional_info': self.get_additional_info(),
            'image_description': self.get_image_description()
        }