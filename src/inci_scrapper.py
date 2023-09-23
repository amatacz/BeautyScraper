from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options





class INCIScraper:
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def open_website(self, url):
        self.driver.get(url)

    def accept_cookies(self):
        try:
            cookies_accept = WebDriverWait(self.driver, 10).until(
                exp.element_to_be_clickable((
                    By.XPATH, '//*[@id="consent-accept"]')))
            cookies_accept.click()
        except Exception as e:
            print(e)

    def get_ingredients_links(self):
        ingredients = WebDriverWait(self.driver, 10).until(
            exp.presence_of_all_elements_located((
                By.CLASS_NAME, 'color-inherit')))
        ingredient_links = []
        for ingredient in ingredients:
            ingredient_links.append(ingredient.get_attribute('href'))

        return ingredient_links

    def get_ingredients_functions(self, ingredients_links):
        """
        Komentarze
        """
        inci_dict = {}

        for link in ingredients_links:
            self.open_website(link)
            ingredient_name = WebDriverWait(self.driver, 10).until(
                exp.presence_of_element_located((
                    By.CLASS_NAME, 'm-0'))).text
            try:
                ingredient_function_list = WebDriverWait(self.driver, 10).until(
                    exp.presence_of_all_elements_located(
                        (By.CLASS_NAME, 'fonctions-inci')))
            except Exception as e:
                print(e)
                ingredient_function_list = []

            if ingredient_function_list:
                inci_dict[ingredient_name] = {}

                for function in ingredient_function_list:
                    try:
                        function_categories = function.text.split("\n")
                    except not function_categories:
                        continue

                    if function_categories:
                        function_details = []
                        for function_category in function_categories:
                            function_details.append(function_category.split(" : "))

                        for function_detail in function_details:
                            inci_dict[ingredient_name].update({function_detail[0]: function_detail[1]})

                    else:
                        function_details = function.text.split(" : ")
                        inci_dict[ingredient_name].update({function_details[0]: function_details[1]})
            else:
                pass
        return inci_dict

    def close_browser(self):
        self.driver.quit()
