import functions_framework
from gcloud_inci_scrapper.inci_scrapper import INCIScraper
from gcloud_sephora_scrapper.sephora_scrapper import ProductsScraper
from utils import DataConfigurator


@functions_framework
def gcloud_get_inci_data():

    # create data configurator object
    DataConfiguratorObject = DataConfigurator()

    # create scraper object
    INCIScraperObject = INCIScraper()

    # inci_data placeholder
    all_inci_data = {}

    # scrape data from each inci category
    for literal in DataConfiguratorObject.PAGE_LITERALS:
        # opens url with inci category
        INCIScraperObject.open_website(DataConfiguratorObject.inci_url+literal)
        # accepts cookies
        INCIScraperObject.accept_cookies()
        # scrape links for all category ingredients
        ingredients_links = INCIScraperObject.get_ingredients_links()
        # update dictionary placeholder with actual data
        all_inci_data.update(INCIScraperObject.get_inci_data(ingredients_links))

    # # upload dict data to GCP bucket
    # CloudIntegratorObject.upload_data_to_cloud_from_dict("amatacz-skincare-project-bucket", all_inci_data, "inci_dictionary.json")
    return all_inci_data


@functions_framework
def gcloud_get_product_data():
    # create data configurator object
    DataConfiguratorObject = DataConfigurator()

    # create sephora scraper
    SephoraScraperObject = ProductsScraper()

    # data placeholder
    all_products_data = {}

    # scrape data products data from given categories
    for category in DataConfiguratorObject.load_category_urls_from_yaml():

        # data placeholder
        category_data = {}
        # destination url for data per each category ad with specified rating - 5/5 by default
        destination_url = SephoraScraperObject.SEPHORA_BASE_URL + category['url'] + SephoraScraperObject.get_rating_filter()
        # Opening a website
        SephoraScraperObject.open_website(destination_url)
        # Decline cookies if any
        SephoraScraperObject.decline_cookies()
        # Scrape links to specific products
        category_info_links = SephoraScraperObject.get_product_tiles()
        # Update dictionary placeholder with actual data
        category_data.update(SephoraScraperObject.get_product_data(category_info_links))
        all_products_data[category['name']].append(category_data)

        # # upload products data as file per catgory
        # CloudIntegratorObject.upload_data_to_cloud_from_dict("amatacz-skincare-project-bucket", category_data, f"{category['name']}_data.json")
    return all_products_data
