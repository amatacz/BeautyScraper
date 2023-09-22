import yaml


class DataConfigurator:

    def __init__(self) -> None:
        self.category_urls_yaml = 'conf/category_urls.yaml'

    def load_category_urls_from_yaml(self):
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
