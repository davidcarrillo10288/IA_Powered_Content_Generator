# scr/scraping.py

import requests # Keep import if needed elsewhere, but not for initial HTML fetch
from bs4 import BeautifulSoup
import re
# from scr.image_describer import ImageGridDescriber # Keep if you have this file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # Keep the import for fallback
from selenium.webdriver.chrome.service import Service
# Import necessary exceptions for robust error handling
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException, TimeoutException, NoSuchElementException, InvalidArgumentException
# Import modules for finding elements and waiting
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging
import time # Optional: for potential sleep/waits if needed

logger = logging.getLogger(__name__) # Get logger for this module

# --- Placeholder for your ImageGridDescriber ---
# If you have scr/image_describer.py, keep it.
# Otherwise, define a simple placeholder class
class ImageGridDescriber:
    def concatenate_images_square(self, image_links):
        logger.warning("Placeholder: ImageGridDescriber.concatenate_images_square called.")
        # In a real scenario, this would download/process images
        return "placeholder_concatenated_image_data"

    def get_image_description(self, image_data):
        logger.warning("Placeholder: ImageGridDescriber.get_image_description called.")
        # In a real scenario, this would use an image description model
        return "Placeholder image description from AI."
# --------------------------------------


class FalabellaScraper:
    def __init__(self, url: str):
        # Initialize the scraper with the URL
        self.url = url
        # Headers are often needed for requests, but less so for Selenium's real browser behavior,
        # though you can set a specific user agent via chrome_options.
        # self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        self.driver = None # Initialize driver attribute to None
        self.soup = None # Initialize soup attribute to None

    def _initialize_driver(self):
        """Initializes the Selenium WebDriver with preferred methods."""
        logger.info("Attempting to initialize ChromeDriver...")
        chrome_options = Options()
        # Common options for headless scraping in Docker
        chrome_options.add_argument("--headless=new") # Use new headless mode (more stable)
        chrome_options.add_argument("--no-sandbox") # Essential in Docker/constrained environments
        chrome_options.add_argument("--disable-dev-shm-usage") # Recommended in Docker
        chrome_options.add_argument("--disable-gpu") # Recommended in headless mode
        chrome_options.add_argument("--window-size=1920,1080") # Set a common window size
        chrome_options.add_argument("--disable-extensions") # Disable extensions
        chrome_options.add_argument("--disable-features=VizDisplayCompositor") # May help in some environments
        # chrome_options.add_argument("--proxy-server='direct://'") # Example proxy settings if needed
        # chrome_options.add_argument("--proxy-bypass-list='*'") # Example proxy settings if needed

        # Set the user agent via chrome_options (good practice)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36")


        # Explicitly set the binary location for Chromium installed by apt-get
        # This path should be correct based on the Debian/Ubuntu package
        chrome_options.binary_location = "/usr/bin/chromium"

        driver = None # Local variable for the driver instance

        try:
            logger.info("Attempt #1: Using ChromeDriver installed by apt-get at /usr/bin/chromedriver...")
            # --- FIRST ATTEMPT: Use the ChromeDriver installed via apt-get ---
            # The executable_path points directly to the driver installed by 'chromium-driver' package
            service = Service(executable_path="/usr/bin/chromedriver")
            driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Attempt #1 Successful: Initialized driver using /usr/bin/chromedriver.")
            return driver # Return the initialized driver

        except (WebDriverException, FileNotFoundError, SessionNotCreatedException, InvalidArgumentException) as e_apt:
            # Catch specific exceptions related to driver initialization failure for the first attempt
            logger.warning(f"Attempt #1 Failed: {type(e_apt).__name__} - {e_apt}")
            logger.info("Attempt #2: Using webdriver-manager as a fallback...")
            try:
                # --- SECOND ATTEMPT: Use webdriver-manager (fallback) ---
                # This will try to download a compatible driver based on detected browser version.
                # If webdriver-manager is up-to-date, it should find a driver for Chromium 135+.
                # We removed the 'version' argument based on the previous error.
                # Setting path=None tells WDM to put it in its default cache.
                service = Service(ChromeDriverManager(path=None).install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("Attempt #2 Successful: Initialized driver using webdriver-manager.")
                return driver # Return the initialized driver

            except (WebDriverException, SessionNotCreatedException, InvalidArgumentException) as e_wdm:
                logger.error(f"Attempt #2 Failed: {type(e_wdm).__name__} - {e_wdm}")
                logger.critical("FATAL: Could not initialize any ChromeDriver after two attempts.")
                # Re-raise a custom exception or a more informative one indicating driver failure
                raise RuntimeError("Failed to initialize ChromeDriver for scraping") from e_wdm
            except Exception as e_other_wdm:
                 # Catch any other unexpected errors during the webdriver-manager attempt
                 logger.error(f"Attempt #2 Failed: An unexpected error occurred - {type(e_other_wdm).__name__} - {e_other_wdm}")
                 raise RuntimeError("Unexpected error during driver initialization fallback") from e_other_wdm

        except Exception as e_other_apt:
            # Catch any other unexpected errors during the first attempt
            logger.error(f"Attempt #1 Failed: An unexpected error occurred - {type(e_other_apt).__name__} - {e_other_apt}")
            # If the first attempt fails with an unexpected error, still try the second
            logger.info("Attempt #2: Using webdriver-manager as a fallback (due to unexpected error in Attempt #1)...")
            try:
                service = Service(ChromeDriverManager(path=None).install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("Attempt #2 Successful: Initialized driver using webdriver-manager (fallback after unexpected error).")
                return driver
            except Exception as e_wdm_fallback:
                 logger.error(f"Attempt #2 Failed: Fallback to webdriver-manager also failed - {type(e_wdm_fallback).__name__} - {e_wdm_fallback}")
                 raise RuntimeError("Failed to initialize ChromeDriver even with fallback") from e_wdm_fallback


    def scrape(self) -> dict:
        """Performs the scraping operation and returns metadata."""
        metadata = {}
        # Ensure driver and soup are None before starting a new scrape
        self.driver = None
        self.soup = None

        try:
            # --- Step 1: Initialize the driver ---
            self.driver = self._initialize_driver()

            if not self.driver: # This check is technically redundant if _initialize_driver raises error
                 raise RuntimeError("Driver initialization failed before navigation.")

            # --- Step 2: Navigate to the URL using the driver ---
            logger.info(f"Navigating to URL: {self.url}")
            # Add a timeout for page loading (including fetching initial HTML and resources)
            self.driver.set_page_load_timeout(30) # Set page load timeout to 30 seconds

            try:
                self.driver.get(self.url)
                logger.info("Page navigation successful.")

                # --- Step 3: Wait for dynamic content to load ---
                # This is CRUCIAL for modern single-page applications (SPAs) like Falabella
                # Wait up to 15 seconds for a key element (like the product title) to be visible
                # Replace 'h1.jsx-783883818.product-name' with the actual CSS selector for the product title
                # Inspect the Falabella page source in your browser to find the current stable selector
                product_title_selector = "h1.product-name" # <<< Check and replace with current Falabella selector if needed
                logger.info(f"Waiting for key element ('{product_title_selector}') to be visible...")
                WebDriverWait(self.driver, 15).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, product_title_selector))
                )
                logger.info("Key element found. Page content likely loaded dynamically.")

                # You might need additional waits for other parts of the page (prices, specs, images)
                # Example: WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-price")))


            except TimeoutException:
                logger.warning(f"Timeout waiting for key page elements to appear on {self.url}. Proceeding with extraction might get incomplete data.")
                # Decide how to handle this - maybe raise a specific exception or return partial data
                # For now, we'll proceed but log a warning.
            except InvalidArgumentException as e_invalid_url:
                # Catches errors if the URL itself is somehow invalid for navigation
                logger.error(f"Invalid URL provided for navigation: {self.url} - {e_invalid_url}")
                raise InvalidArgumentException(f"Invalid URL: {self.url}") from e_invalid_url
            except Exception as e_nav_wait:
                 # Catch other errors during navigation or waiting
                 logger.error(f"An error occurred during page navigation or waiting for elements on {self.url}: {type(e_nav_wait).__name__} - {e_nav_wait}")
                 # Re-raise to indicate that the page wasn't ready
                 raise RuntimeError(f"Page not ready for scraping: {e_nav_wait}") from e_nav_wait


            # --- Step 4: Get the page source from the loaded page ---
            html_content = self.driver.page_source
            logger.info("Obtained page source from WebDriver.")

            # --- Step 5: Parse the HTML content with BeautifulSoup ---
            self.soup = BeautifulSoup(html_content, 'html.parser')
            logger.info("Parsed page source with BeautifulSoup.")

            # --- Step 6: Extract data using BeautifulSoup (your existing methods) ---
            logger.info("Starting data extraction with BeautifulSoup...")
            try:
                metadata['url'] = self.url # Always include the URL

                # Call your existing extraction methods
                metadata['title'] = self.get_product_name()
                metadata['price'] = self.get_product_price()
                metadata['description'] = self.get_product_specifications()
                metadata['available_sizes'] = self.get_available_sizes()
                metadata['additional_info'] = self.get_additional_info()
                # metadata['image_description'] = self.get_image_description() # Uncomment if ImageGridDescriber is ready


                logger.info(f"Extraction complete. Extracted keys: {list(metadata.keys())}. Partial data: {str(metadata)[:500]}...") # Log partial data

            except Exception as e_extract:
                 # Catch errors specifically during the element finding/extraction phase using BeautifulSoup
                 logger.error(f"Error during data extraction on {self.url}: {type(e_extract).__name__} - {e_extract}")
                 # Decide if you want to raise this error or return partial data
                 # If you return partial data, ensure the FastAPI endpoint handles missing keys.
                 # For now, let's re-raise to indicate a problem with scraping the *content*.
                 raise RuntimeError(f"Data extraction failed: {e_extract}") from e_extract


        except RuntimeError as re_init:
             # This catches the specific RuntimeError raised by _initialize_driver or navigation/waiting
             # We re-raise it here so the FastAPI endpoint can catch it and return 500
             raise re_init
        except Exception as e_any:
            # This catches any other unexpected error during the entire scrape process
            logger.error(f"An unexpected error occurred during scraping for {self.url}: {type(e_any).__name__} - {e_any}")
            # Re-raise the exception so the FastAPI endpoint can catch it
            raise RuntimeError(f"An unexpected scraping error occurred: {e_any}") from e_any


        finally:
            # --- Step 7: Ensure the driver is closed ---
            if self.driver:
                logger.info("Quitting WebDriver.")
                self.driver.quit()
                self.driver = None # Set to None after quitting

        return metadata # Return the scraped data (might be empty or partial if extraction failed)

    # --- Your Existing Data Extraction Methods (Modified to check self.soup) ---

    def get_product_name(self):
        # Example method for students to follow
        if self.soup:
            # !!! IMPORTANT: Update this selector if Falabella's HTML changes !!!
            name_tag = self.soup.find("h1", class_="jsx-783883818 product-name fa--product-name false") # Your original selector
            # Consider alternative or more general selectors if the specific class names change
            # name_tag = self.soup.select_one("h1.product-name, [data-test-id='product-info-title']") # Example of trying multiple selectors

            if name_tag:
              name = name_tag.text.strip()
              logger.debug(f"Extracted Product Name: {name}")
              return name
            else:
              logger.warning("Product name element not found.")
              return None # Return None instead of a string indicating failure
        else:
            logger.error("Cannot get product name: self.soup is None.")
            return None


    def get_product_price(self):
        # TODO: Find and extract the product price from the parsed HTML
        if self.soup:
            prices = []
            # !!! IMPORTANT: Update these selectors if Falabella's HTML changes !!!
            # Your original selectors relied on regex and class names which are prone to change
            # Consider using more stable attributes like data-test-id if available
            # Example (hypothetical Falabella data-test-ids):
            # main_price_element = self.soup.select_one("[data-test-id='product-price-main']")
            # discount_price_element = self.soup.select_one("[data-test-id='product-price-discount']")
            # normal_price_element = self.soup.select_one("[data-test-id='product-price-normal']")

            # Using your original regex/class based approach (might be fragile)
            producto = self.soup.find("div", id=re.compile(r"^testId-pod-prices-\d+"))
            if producto:
                 precios_elements = producto.find_all("li", class_=re.compile(r'prices-\d+'))

                 if precios_elements:
                     # Iterate through elements and extract text, cleaning whitespace
                     for precio_el in precios_elements:
                         prices.append(precio_el.get_text(strip=True))

                     logger.debug(f"Extracted Product Prices: {prices}")
                     # You might want to parse these strings into numbers and identify types (CMR, Internet, Normal)
                     # This parsing logic needs to be robust to variations
                     # Example basic parsing (needs refinement for currency symbols, commas, etc.)
                     parsed_prices = {}
                     for p_text in prices:
                         if 'cmr' in p_text.lower():
                             parsed_prices['cmr'] = p_text.split('cmr:')[-1].strip() if 'cmr:' in p_text.lower() else p_text
                         elif 'internet' in p_text.lower() or 'online' in p_text.lower():
                             parsed_prices['internet'] = p_text.split('internet:')[-1].strip() if 'internet:' in p_text.lower() else p_text
                         elif 'normal' in p_text.lower():
                            parsed_prices['normal'] = p_text.split('normal:')[-1].strip() if 'normal:' in p_text.lower() else p_text
                         else:
                             # Fallback for simple price listings
                             if 'internet' not in parsed_prices and 'cmr' not in parsed_prices: # Assume first is internet if no type is specified
                                 parsed_prices['internet'] = p_text
                             elif 'normal' not in parsed_prices: # Assume second is normal
                                  parsed_prices['normal'] = p_text


                     return parsed_prices # Return a dictionary with price types

                 else:
                    logger.warning("Product price elements not found within the price div.")
                    return {} # Return empty dict if no price elements found
            else:
                logger.warning("Product prices container div not found.")
                return {} # Return empty dict if the main price container not found

        else:
            logger.error("Cannot get product price: self.soup is None.")
            return {}


    def get_image_links(self):
        # TODO: Find all image tags and extract their source links
        if self.soup:
            # !!! IMPORTANT: Update this selector if Falabella's HTML changes !!!
            # Your original selector might only get the first image or thumbnails
            # Inspect the page to find the correct selector for the main product images
            # Look for img tags within a gallery container, or with specific data attributes
            images_elements = self.soup.find_all('img', class_="jsx-2487856160") # Your original selector

            # Example of a potentially better selector (needs verification on live site)
            # images_elements = self.soup.select("div.product-image-gallery img.product-image")

            image_links = []
            if images_elements:
                for img_tag in images_elements:
                    src = img_tag.get('src') or img_tag.get('data-src') # Try both src and data-src
                    if src:
                         # You might need to adjust the URL manipulation for higher resolution
                         # This regex replacement might not work for all image URLs
                         # Consider a more robust way to get full-size images if possible
                         # Example: replacing query parameters, or finding a data attribute with full size
                         try:
                             processed_src = re.sub(r'(w|h)=\d+,fit=\w+', 'w=800,h=800,fit=pad', src)
                             if not processed_src.startswith('http'): # Handle relative URLs
                                 # Need logic to construct absolute URL if necessary
                                 processed_src = f"https://falabella.com.pe{processed_src}" # Example, verify base URL
                             image_links.append(processed_src)
                         except Exception as url_proc_err:
                             logger.warning(f"Failed to process image URL {src}: {url_proc_err}")
                             # Optionally append the original src if processing fails
                             # image_links.append(src)


            logger.debug(f"Extracted Image Links: {image_links}")
            return image_links
        else:
            logger.error("Cannot get image links: self.soup is None.")
            return []


    def get_product_specifications(self):
        # TODO: Extract product specifications from the HTML table
        if self.soup:
            especificaciones = {}
            # !!! IMPORTANT: Update this selector if Falabella's HTML changes !!!
            specifications_table = self.soup.find("table", class_="jsx-960159652 specification-table") # Your original selector

            if specifications_table:
                 rows = specifications_table.find_all("tr")
                 if rows:
                     for fila in rows:
                         celdas = fila.find_all("td")
                         if len(celdas) == 2:
                             nombre = celdas[0].get_text(strip=True)
                             valor = celdas[1].get_text(strip=True)
                             if nombre and valor: # Only add if both name and value are found
                                 especificaciones[nombre] = valor
                         # else: # Handle rows that don't have exactly 2 cells if necessary
                             # logger.warning(f"Skipping specification row with {len(celdas)} cells.")

                 logger.debug(f"Extracted Specifications: {especificaciones}")
                 return especificaciones
            else:
                logger.warning("Product specifications table not found.")
                return {} # Return empty dict if table not found

        else:
            logger.error("Cannot get product specifications: self.soup is None.")
            return {}


    def get_additional_info(self):
        # TODO: Extract additional product information from the HTML
        # This method needs specific selectors based on where additional info is on the page
        # Example: Look for divs/sections with headings like "Características", "Detalles", etc.
        if self.soup:
             additional_info = {}
             # --- Implement logic to find and extract additional info ---
             # Example: Find a description section (replace selectors)
             # description_section = self.soup.select_one(".product-description-section")
             # if description_section:
             #     additional_info['description_text'] = description_section.get_text(strip=True)

             # Example: Find a list of features (replace selectors)
             # features_list = self.soup.select(".product-features-list li")
             # if features_list:
             #     additional_info['features'] = [li.get_text(strip=True) for li in features_list]

             logger.warning("Placeholder: get_additional_info is not implemented yet.")
             return additional_info # Return the extracted info dictionary
        else:
            logger.error("Cannot get additional info: self.soup is None.")
            return {}


    def get_available_sizes(self):
        # TODO: Extract available sizes for the product
        if self.soup:
            sizes_list = []
            # !!! IMPORTANT: Update this selector if Falabella's HTML changes !!!
            # Look for buttons, divs, or inputs representing selectable sizes
            sizes_elements = self.soup.find_all('button', class_="jsx-3027654667 size-button rebranded enhanced-size-selector") # Your original selector

            if sizes_elements:
                for size_el in sizes_elements:
                    size_text = size_el.get_text(strip=True)
                    if size_text:
                        sizes_list.append(size_text)

            logger.debug(f"Extracted Available Sizes: {sizes_list}")
            return sizes_list
        else:
            logger.error("Cannot get available sizes: self.soup is None.")
            return []


    def get_image_description(self):
        # TODO: Use the ImageGridDescriber to concatenate images and generate a description
        # This part depends on whether scr.image_describer is correctly implemented
        if self.soup: # Check if soup is available before trying to get image links
            try:
                img_describer = ImageGridDescriber() # Assuming this class is available
                image_links = self.get_image_links() # Get image links using the method above
                if image_links:
                    logger.info(f"Attempting to describe {len(image_links)} images.")
                    concatenated_image = img_describer.concatenate_images_square(image_links)
                    # Check if concatenation was successful before describing
                    if concatenated_image:
                         description = img_describer.get_image_description(concatenated_image)
                         logger.debug(f"Generated Image Description: {description[:100]}...") # Log snippet
                         return description
                    else:
                         logger.warning("Image concatenation failed, cannot get description.")
                         return None
                else:
                    logger.warning("No image links found to generate image description.")
                    return None

            except Exception as e_img_desc:
                 logger.error(f"Error during image description process: {type(e_img_desc).__name__} - {e_img_desc}")
                 return None # Return None on error
        else:
            logger.error("Cannot get image description: self.soup is None.")
            return None