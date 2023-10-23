from selenium import webdriver
from selenium.webdriver.support import expected_conditions as exp
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, ElementNotInteractableException, WebDriverException
from src.data_configuration import DataConfigurator
import time


class ProductsScraper:
    def __init__(self) -> None:
        options = Options()
        # options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)

        # define XPath contants
        self.BRAND_XPATH = '//*[@id="pdpMain"]/div[1]/div[2]/div[2]/div[1]/div[1]'
        self.PRODUCT_NAME_XPATH = '//*[@id="pdpMain"]/div[1]/div[2]/div[2]/div[1]/h1/span'
        self.PRODUCT_PRICE_XPATH = '//*[@id="price-block"]/div[1]/span'
        self.PAYMENT_SEC_XPATH = '//*[@id="delivery-availability-section"]'
        self.PRODUCT_INCI_SECTION_ID = 'tab-ingredients'
        self.PRODUCT_INCI_XPATH = '//*[@id="product-info"]/div'
        # Define IDs contstants
        self.PRODUCT_INCI_ID = 'product-info'
        # Retrieve sephora base url from YAML
        self.SEPHORA_BASE_URL = DataConfigurator().load_datasource_urls_from_yaml()

    def open_website(self, url):
        '''
        Ope the website specified by the given URL.

        :param url: The URL of the website to open.
        :type url: str
        :raises WebDriverException: Raised for errors involving the WebDriver instance.
        :raises TimeoutException: Raised when a command does not complete in enough time.
        '''
        try:
            self.driver.get(url)
        except TimeoutException as e:
            raise TimeoutException(f"Timed out wwhile loading the website: {url}. Error: {e}")
        except WebDriverException as e:
            raise WebDriverException(f"An error occurred while trying to open the website: {url}. Error: {e}")

    def decline_cookies(self):
        '''
        Decline cookies on a webpage by clicking the decline cookies button.

        This method waits for the decline cookies button to be clickable and then clicks it.
        If the button is not found, is not clickable, or if any other WebDriver exception occurs,
        it will print an aprpropriate error message.

        :raises NoSuchElementException: Decline cookies button was not found on webpage.
        :raises ElementNotInterctableException: Raised when a cookies element is not iterable.
        :raises Timeout Exception: Raised when a command does not complete in enough time.
        :raises Exception: Raised whe a command fail with unknown reasons.
        '''
        try:
            # wait for the decline cookies button to be clickable and click it
            cookies_decline = WebDriverWait(self.driver, 10).until(
                exp.element_to_be_clickable((
                    By.XPATH, '//*[@id="footer_tc_privacy_button_2"]')))
            # decline cookies
            cookies_decline.click()
        except NoSuchElementException:
            print("Error: Decline cookies button was not found on the webpage.")
        except ElementClickInterceptedException:
            print("Error: Decline cookies button was not interactable.")
        except TimeoutException:
            print("Error: Timed out waiting for the decline cookies button to become clickable.")
        except Exception as e:
            print(f"An unexpected error occured: {e}")

    def _scroll_to_bottom(self, scroll_paulse_time: float = 0.5, max_scroll_time: float = 60.0) -> None:
        """
        Scroll to the bottom of a dynamically loading webpage.
            The method keeps scrolling until no additional content is loaded or the maximum scroll time is reached.

        :param scroll_pause_time: Time to pause between scrolls, in seconds.
        :param max_scroll_time: Maximum time to keep scrolling, in seconds.
        :raises KeyboardInterrupt: Raised when user force stop the process.
        """

        # current time
        start_time = time.time()
        # current height
        last_height = self.driver.execute("return document.body.scrollHeight")
        try:
            while True:
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(scroll_paulse_time)

                # calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")

                # Break if reach the bottom of the page or scrolling threshold is passed
                if (new_height == last_height) or (time.time() - start_time > max_scroll_time):
                    break

                # Keep track of last height
                last_height = new_height
        except KeyboardInterrupt:
            print("Scrolling interrupted by user.")

    def get_rating_filter(self, rating: int = 5, sort: str = "Best%20Sellers"):
        """
        Query parameters -> products with:

        :param rating: average rating 5 (by default)
        :param sort: sorted by Bestsellers (by default)
        """
        return f"/?prefn1=bvAverageRating&prefv1={rating}&srule={sort}"

    def get_product_tiles(self):
        """
        Scrolls through the webpage and retrieves a list of URLs,
        each corresponding to a different product tile on page.

        :return: A list of product tile URLs.
        :rtype: List[str]
        """

        # Scroll through the webpage to ensure all product tiles are loaded
        self._scroll_to_bottom()

        # Attempt to retrieve a list of elements by their class name
        product_tile_links = self.get_list_of_elements(By.CLASS_NAME, "product-tile_link")

        # Check if any product tile links are found.
        if product_tile_links is None:
            print("No product tiles were found on the webpage.")
            return []

        # Extract the href attribute from each product tile link and return the list of URLs.
        return [link.get_attribute('href') for link in product_tile_links]

    def get_list_of_elements(self, by, value):
        """
        Wait 10 sec until you find and element located under given value.
            If no element found return None.
        """
        try:
            return WebDriverException(self.driver, 10).until(exp.presence_of_all_elements_located((by, value)))
        except (NoSuchElementException, TimeoutException) as e:
            return None

    def get_element_text(self, by, value):
        """
        Wait 10 sec until you find element located under given value.
            If no element found return None.
        """
        try:
            return WebDriverException(self.driver, 10).until(exp.presence_of_element_located((by, value)))
        except (NoSuchElementException, TimeoutException) as e:
            return None

    def get_product_brand(self):
        """
        Get a brand name from provided path and section.
            Return None if no data found
        """
        try:
            return self.get_element_text(By.XPATH, self.BRAND_XPATH).text
        except Exception as e:
            print("Error occured: ", e)
            return None

    def get_product_name(self):
        """
        Get a product name from provided path and section
            Return None if no data found.
        """
        try:
            return self.get_element_text(By.XPATH, self.PRODUCT_NAME_XPATH).text
        except Exception as e:
            print("Error occured: ", e)
            return None

    def get_product_price(self):
        """
        Get a product price from provided path and section.
            Return None if no data found.
        """
        try:
            return self.get_element_text(By.XPATH, self.PRODUCT_PRICE_XPATH).text
        except Exception as e:
            print("Error occured: ", e)
            return None
        
    def get_product_ingredients(self):
        """
        Retrieves the product ingredients from the web page.

        Returns:
            list: A list of ingredients of found, otherwise an empty list.

        Raises:
            NoSuchElementException: If the element with the given ID is not found.
            ElementNotInteractableException: If the element is not interactable.
            TimeoutException: If the element does not reach the desired state within the timeout.
        """
        try:
            # Wait for the ingredient section to be clickable and click it.
            WebDriverWait(self.driver, 10).until(
                exp.element_to_be_clickable((By.ID, self.PRODUCT_INCI_SECTION_ID))
                ).click()
            # Wait for the ingredient text to be present and retrieve it
            ingredients_text = self.get_element_text(By.ID, self.PRODUCT_INCI_ID).text

            # Split the ingredients text into a list
            return ingredients_text.split(',') if ingredients_text else []
        except (NoSuchElementException, ElementNotInteractableException, TimeoutException) as e:
            print(f"An error occured: {e}")
            return []

    def get_product_data(self, product_links):
        """
        Iterate through all products links and return dictionary with:
            - brand
            - price
            - ingredients

        :params product_links: list of products links (urls)
        """
        product_info = {}
        for product_link in product_links:
            try:
                # Open website of specific product
                self.open_website(product_link)
                # Retrieve data from product url
                product_info[self.get_product_name()] = {
                    'Brand': self.get_product_brand(),  # Get product brand
                    'Price': self.get_product_price(),  # Get product price
                    'Ingredients': self.get_product_ingredients(),  # Get product ingredients
                }
            except Exception as e:
                print("Error during data exploration...\n", e)
                continue

        # Return data
        return product_info
