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

    # create cloud integrator object
    CloudIntegratorObject = cloud_integration.CloudIntegration()

    # create scraper object
    INCIScraperObject = inci_scrapper.INCIScraper()

    # create sephora scraper
    SephoraScraperObject = sephora_scrapper.ProductsScraper()


    # # inci_data placeholder
    # all_inci_data = {}
    # for page_literal in DataConfiguratorObject.PAGE_LITERALS:
    #     try:
    #         INCIScraperObject.open_website(f'https://incibeauty.com/en/ingredients/{page_literal}')
    #         INCIScraperObject.accept_cookies()
    #         links = INCIScraperObject.get_ingredients_links()
    #         all_inci_data.update(INCIScraperObject.get_ingredients_functions(links))
    #     except Exception as e:
    #         print(e)
    #         all_inci_data.update({page_literal: "BRAK DANYCH"})
    #     finally:
    #         INCIScraperObject.close_browser()

    # upload dict data to GCP bucket
    # CloudIntegratorObject.upload_data_to_cloud_from_dict("amatacz-skincare-project-bucket", all_inci_data, "inci_dictionary.json")

    # scrape data products data from given categories
    for category in DataConfiguratorObject.load_category_urls_from_yaml():

        # data placeholder
        category_data = {}
        # destination url for data per each category and with specified raiting - 5/5 by default
        destination_url = SephoraScraperObject.SEPHORA_BASE_URL + category['url'] +  SephoraScraperObject.get_raiting_filter()
        # Opening a website 
        SephoraScraperObject.open_website(destination_url)
        # Decline cookies if any
        SephoraScraperObject.decline_cookies()
        # Scrape links to specific products
        category_info_links = SephoraScraperObject.get_product_tiles()
        # Update dictionary placeholder with actual data
        category_data.update(SephoraScraperObject.get_product_data(category_info_links))

        # helper, will be removed
        with open(f"data\\{category['name']}_data.json", "w", encoding="utf-8") as f:
            json.dump(category_data, f, indent=2)

        # # upload products data as file per catgory
        # CloudIntegratorObject.upload_data_to_cloud_from_dict("amatacz-skincare-project-bucket", category_data, f"{category['name']}_data.json")
