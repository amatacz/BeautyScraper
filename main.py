from src import (
    inci_scrapper,
    sephora_scrapper,
    cloud_integration,
    data_configuration
)
import json


if __name__ == '__main__':

    # create data configurator object
    DataConfiguratorObject = data_configuration.DataConfigurator()

    # create cloud integrator project
    CloudIntegratorObject = cloud_integration.CloudIntegration()

    # inci_data placeholder
    all_inci_data = {}
    for page_literal in inci_scrapper.PAGE_LITERALS:
        try:
            inci_db = inci_scrapper.INCIScraper()
            inci_db.open_website(f'https://incibeauty.com/en/ingredients/{page_literal}')
            inci_db.accept_cookies()
            links = inci_db.get_ingredients_links()
            all_inci_data.update(inci_db.get_ingredients_functions(links))
        except Exception as e:
            print(e)
            all_inci_data.update({page_literal: "BRAK DANYCH"})

        finally:
            inci_db.close_browser()

    # upload dict data to GCP bucket
    CloudIntegratorObject.upload_data_to_cloud_from_dict("amatacz-skincare-project-bucket", all_inci_data, "inci_dictionary.json")

    # scrape data products data from given categories
    for category in DataConfiguratorObject.load_category_urls_from_yaml():

        # data placeholder
        category_data = {}

        category_info = sephora_scrapper.ProductsScraper()
        category_info.open_website(sephora_scrapper.BASE_URL + category['url'] + sephora_scrapper.QUERY_PARAMS)
        category_info.decline_cookies()
        category_info_links = category_info.get_product_tiles()
        category_data.update(category_info.get_product_data(category_info_links))

        # helper, will be removed
        with open(f"data\\{category['name']}_data.json", "w", encoding="utf-8") as f:
            json.dump(category_data, f, indent=2)

        # upload products data as file per catgory
        CloudIntegratorObject.upload_data_to_cloud_from_dict("amatacz-skincare-project-bucket", category_data, f"{category['name']}_data.json")
