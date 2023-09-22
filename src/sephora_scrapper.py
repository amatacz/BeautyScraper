from selenium import webdriver
from selenium.webdriver.support import expected_conditions as exp
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# base url
BASE_URL = "https://www.sephora.pl/wszystkie-produkty/pielegnacja-twarzy/kosmetyki-do-pielegnacji/"

# query parameters -> products with average rating 5 sorted by Bestsellers
QUERY_PARAMS = "/?prefn1=bvAverageRating&prefv1=5&srule=Best%20Sellers"

CATEGORY_URL = "kremy-na-dzien-c299901"

class ProductsScraper:
    def __init__(self) -> None:
        options = Options()
        #options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)

    def open_website(self, url):
        self.driver.get(url)

    def decline_cookies(self):
        try:
            cookies_decline = WebDriverWait(self.driver, 10).until(
                exp.element_to_be_clickable((
                    By.XPATH, '//*[@id="footer_tc_privacy_button_2"]')))
            cookies_decline.click()
        except Exception as e:
            print(e)

    def scroll_to_bottom(self) -> None:
        # scroll to the bottom of page
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_product_tiles(self):
        self.scroll_to_bottom()

        product_tile_links = WebDriverWait(self.driver, 10).until(
            exp.presence_of_all_elements_located((
                By.CLASS_NAME, 'product-tile-link')))

        product_links = []
        for product_link in product_tile_links:
            link = product_link.get_attribute('href')
            product_links.append(link)

        return product_links

    def get_product_data(self, product_links):
        product_info = {}
        for product_link in product_links:
            try:
                self.open_website(product_link)
                brand = self.driver.find_element(By.XPATH, '//*[@id="pdpMain"]/div[1]/div[2]/div[2]/div[1]/div[1]').text
                product_name = self.driver.find_element(By.XPATH, '//*[@id="pdpMain"]/div[1]/div[2]/div[2]/div[1]/h1/span').text
                product_price = self.driver.find_element(By.XPATH, '//*[@id="price-block"]/div[1]/span').text
                try:
                    payment_sec = self.driver.find_element(By.XPATH, '//*[@id="delivery-availability-section"]')
                    self.driver.execute_script("arguments[0].scrollIntoView();", payment_sec)
                    product_inci_section = self.driver.find_element(By.ID, "tab-ingredients")
                    product_inci_section.click()

                    product_inci = WebDriverWait(self.driver, 10).until(exp.presence_of_element_located((By.XPATH, '//*[@id="product-info"]/div'))).text
                    product_inci_formatted = product_inci.split(',')
                except Exception as e:
                    product_inci_formatted = "BRAK DANYCH"

                product_info[product_name] = {'Brand': brand, 'Price': product_price, 'Ingredients': product_inci_formatted}
            except Exception as e:
                print(e)

        return product_info