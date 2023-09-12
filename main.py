from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp
from selenium.webdriver.common.by import By
import json
import string

ALPHABET = list(string.ascii_uppercase)
PAGE_LITERALS = ['1'] + ALPHABET
INCI_DICT = {}


def get_driver(url):
    """
    Takes URL string as an argument, connects to page using Chrome,
    accepts cookies and retrun Selenium web response.
    """

    driver = webdriver.Chrome()
    driver.get(url)

    try:
        cookies_accept = WebDriverWait(driver, 10).until(
            exp.element_to_be_clickable((
                By.XPATH, '//*[@id="consent-accept"]')))
        cookies_accept.click()
    except Exception as e:
        print(e)

    return driver


def get_ingredients_links(response):
    """
    Takes selenium response as an argument.
    Find all elements that represents ingredients 
    and extract links to detailed view.
    Stores links in list.
    """

    ingredients = WebDriverWait(response, 10).until(
        exp.presence_of_all_elements_located((
            By.CLASS_NAME, 'color-inherit')))
    ingredient_links = []
    for ingredient in ingredients:
        ingredient_links.append(ingredient.get_attribute('href'))

    return ingredient_links


def get_ingredient_functions(ingredient_links: list):
    """
    Takes list of links to ingredient details view.
    Extracts ingredient name and functions in cosmetics.
    Stores info in INCI_DICT in format:
    ingredient_name {
        [
            {function_category: function},
            {function_category: function}
        ]
    }
    """

    for link in ingredient_links:
        response = get_driver(link)
        ingredient_name = WebDriverWait(response, 10).until(
            exp.presence_of_element_located((
                By.CLASS_NAME, 'm-0'))).text

        try:
            ingredient_function_list = WebDriverWait(response, 10).until(
                exp.presence_of_all_elements_located(
                    (By.CLASS_NAME, 'fonctions-inci')))
        except Exception as e:
            print(e)
            ingredient_function_list = []

        if ingredient_function_list:
            for function in ingredient_function_list:
                try:
                    function_categories = function.text.split("\n")
                except not function_categories:
                    continue

                if function_categories:
                    function_details = []
                    for function_category in function_categories:
                        function_details.append(function_category.split(" : "))

                    INCI_DICT[ingredient_name] = []
                    for function_detail in function_details:
                        INCI_DICT[ingredient_name].append(
                            {function_detail[0]: function_detail[1]})

                else:
                    function_details = function.text.split(" : ")
                    INCI_DICT[ingredient_name] = {}
                    INCI_DICT[ingredient_name][function_details[0]] = function_details[1]
        else:
            pass

    return INCI_DICT


def save_inci_data_to_json(inci_data):
    """
    Saves INCI_DICT to JSON file.
    """
    with open("inci_data.json", "w") as f:
        json.dump(inci_data, f, indent=2)


def process():
    # TU JEST ZAWĘŻONA LISTA PODSTRON DO PIERWSZEJ
    for page_literal in PAGE_LITERALS[0]:
        start_page = get_driver(f"https://incibeauty.com/en/ingredients/{page_literal}")
        ingredients_links = get_ingredients_links(start_page)
        ingredient_functions = get_ingredient_functions(ingredients_links)
        save_inci_data_to_json(ingredient_functions)
