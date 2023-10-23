from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, WebDriverException


class INCIScraper:
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def open_website(self, url: str):
        """
        Open the website specified by given URL.

        :param url: The URL of the website to open.
        :raises WebDriverException: Raised for errors involving the WebDriver instance.
        :raises TimeoutException: Raised when a command does not complete in enough time.
        """
        try:
            self.driver.get(url)
        except TimeoutException as e:
            raise TimeoutException(f"Timed out while loading the website: {url}. Error {e}.")
        except WebDriverException as e:
            raise WebDriverException(f"An error occurred while trying to open the website: {url}. Error: {e}.")

    def accept_cookies(self):
        """
        Accept cookies on a webpage by clicking the accept cookies button.
        This method waits for accept cookies button to be clickable and clicks it.

        :raises TimeoutException: Raised when a command does not complete in enough time.
        :raises NoSuchElementException: Accept cookies button was not found on the webpage.
        :raises ElementNotInteractableException: Raised when a cookies element is not interactable.
        :raises Exception: Raised with command fail with unknown reason.

        """
        try:
            # Wait for the accept cookies button to be clickable and click it
            cookies_accept = WebDriverWait(self.driver, 10).until(
                exp.element_to_be_clickable((
                    By.ID, "consent-accept")))
            # accept cookies
            cookies_accept.click()
        except NoSuchElementException:
            print("Error: Accept cookies button was not found on the webpage.")
        except ElementNotInteractableException:
            print("Error: Accept cookies element was not interactable.")
        except TimeoutException:
            print("Error: Timed out waiting for the accept cookies button to become clickable.")
        except Exception as e:
            print(f"An unexpected error occured. Error: {e}.")

    def get_ingredients_links(self):
        """
        Gets links to each ingredients from provided path and section.
            Returns None if no data found.
        """
        # Attempt to retrieve a list of elements by their class name
        ingredients = self.get_list_of_elements(By.CLASS_NAME, 'color-inherit')

        # Check if any ingredient links are found..
        if ingredients is None:
            return []
        # Extract the gref attribute from list of ingredients and return list of URLs.
        return [ingredient.get_attribute('href') for ingredient in ingredients]

    def get_ingredient_name(self):
        """
        Gets name of ingredient from provided path and section.
            Returns None if no data found.
        """ 
        try:
            return self.get_element_text(By.CLASS_NAME, 'm-0').text
        except Exception as e:
            print("Error occured: ", e)
            return None

    def get_ingredient_functions(self):
        """
        Gets all ingredient functions and stores it in dictionary.
            Returns None if no data found.
        """
        function_categories = self.get_list_of_elements(By.CLASS_NAME, 'fonctions-inci')

        if function_categories is None:
            return {}

        ingredient_functions = [function_category.text.split("\n") for function_category in function_categories]
        function_details = [ingredient_function.split(" : ") for ingredient_function in ingredient_functions[0]]
        return {detail[0]: detail[1] for detail in function_details}

    def get_list_of_elements(self, by, value):
        """
        Wait 10 sec until you find all elements located under given value.
            If no element found, return None.
        """
        try:
            return WebDriverWait(self.driver, 10).until(exp.presence_of_all_elements_located((by, value)))
        except (NoSuchElementException, TimeoutException) as e:
            return None

    def get_element_text(self, by, value):
        """
        Wait 10 sec until you find element located under given value.
            If no element found, return None.
        """
        try:
            return WebDriverWait(self.driver, 10).until(exp.presence_of_element_located((by, value)))
        except (NoSuchElementException, TimeoutException) as e:
            return None

    def get_inci_data(self, ingredients_links):
        """
        Iterates by ingredients links and saves ingredients data
        (name and functions) to dict.

        :params ingredients_links: list of ingredients links (urls)

        """
        inci_info = {}

        for link in ingredients_links:
            try:
                # Open website of specific ingredient
                self.open_website(link)
                inci_info[self.get_ingredient_name()] = { 
                    'Functions': self.get_ingredient_functions()  # Get ingredient functions
                }
            except Exception as e:
                print('Error during data exploration... \n', e)
                continue

        # Return data
        return inci_info
