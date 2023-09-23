import os
from dotenv import load_dotenv
from google.cloud import storage
import json


class CloudIntegration:

    def __init__(self) -> None:
        load_dotenv('secrets/.env')
        self.cloud_key = os.environ['GCLOUD_JSON_KEY_LOCATION']
        self.project_id = None

        ''' Retrieve project id from .json key file for google cloud project '''
        if os.path.exists(self.cloud_key):
            # open json file
            with open(self.cloud_key, 'r') as file:
                try:
                    self.project_id = json.load(file).get('project_id', None)
                except json.JSONDecodeError:
                    pass

    def get_google_cloud_project_id(self) -> str:
        ''' 
        return cloud project id 
        '''
        return self.project_id

    def _get_google_client(self) -> storage.client.Client:
        ''' 
        return a client to manage google cloud service from provided .json key file 
        '''
        try:
            return storage.client.Client.from_service_account_json(self.cloud_key)  # return client if there is a api key provided
        except Exception as e:
            return None  # if there is no api key provided

    def upload_data_to_cloud_from_file(self, bucket_name, data_to_upload, blob_name):
        ''' 
        Uloads files with daa to GCP buckets. 
        '''
        bucket = self._get_google_client().bucket(bucket_name)  # connect to bucket
        blob = bucket.blob(blob_name)  # create blob
        with open(data_to_upload, "rb") as file:
            blob.upload_from_file(file)

    def upload_data_to_cloud_from_dict(self, bucket_name, data_dict, blob_name):
        ''' 
        Uploads data from a dictionary to GCP bucket. 
        '''
        bucket = self._get_google_client().bucket(bucket_name)  # connect to bucket
        blob = bucket.blob(blob_name)  # create blob
        data_str = json.dumps(data_dict)  # convert dict to string
        blob.upload_from_string(data_str)  # upload data to blob
