import yaml
import string


class DataConfigurator:

    def __init__(self) -> None:
        self.category_urls_yaml = 'conf/category_urls.yaml'
        self.inci_url = 'https://incibeauty.com/en/ingredients/'
        self.ALPHABET = list(string.ascii_uppercase)
        self.PAGE_LITERALS = ['1'] + self.ALPHABET

    def load_category_urls_from_yaml(self):
        '''
        Load categories from yaml.
            Get a name of category and url code.
        '''
        try:
            with open(self.category_urls_yaml, 'r') as file:
                data = yaml.safe_load(file)
            return data.get("category", [])
        except FileNotFoundError:
            print(f"Error: File {self.category_urls_yaml} not found.")
        except PermissionError:
            print(f"Error: No permission to read the file {self.category_urls_yaml}.")
        except yaml.YAMLError as exc:
            print(f"Error parsing the YAML file: {exc}.")
        return []

    def load_datasource_urls_from_yaml(self):
        '''
        Load datasource from yaml.
        '''
        try:
            with open(self.category_urls_yaml, 'r') as file:
                data = yaml.safe_load(file)
            return data.get("datasource", [])[1]['url']
        except FileNotFoundError:
            print(f"Error: file {self.category_urls_yaml} not found.")
        except PermissionError:
            print(f"Error: No permission to read the file {self.category_urls_yaml}.")
        except yaml.YAMLError as exc:
            print(f"Error parsing the YAML file: {exc}.")
        return []
