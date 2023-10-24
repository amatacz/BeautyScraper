import os
from dotenv import load_dotenv
from google.cloud import storage, bigquery, secretmanager
import json


class CloudIntegration:

    def __init__(self) -> None:
        self.cloud_key = None
        self.project_id = None

    def get_secret(self, project_id, secret_id, version_id="latest"):
        """
        Return a secret value from gcloud secret instance.
        """
        # Create the Secret Manager Service Client
        client = secretmanager.SecretManagerServiceClient()
        # Build the resource name of the secret version.
        name = f"projects/{project_id}/secrets/{secret_id}/version/{version_id}"
        # Access the secret version
        response = client.access_secret_version(request={"name": name})

        # Return the decoded payload
        return response.payload.data.decode("UTF-8")

    def get_google_cloud_project_id(self) -> str:
        ''' return cloud project id '''
        return self.project_id

    def _get_google_client(self) -> storage.client.Client:
        ''' return a client to manage google cloud service from provided .json key file '''
        try:
            return storage.client.Client.from_service_account_json(self.cloud_key)  # return client if there is a api key provided
        except Exception as e:
            return None  # if there is no api key provided

    def upload_data_to_cloud_from_file(self, bucket_name, data_to_upload, blob_name):
        ''' Uloads files with data to GCP buckets. '''
        bucket = self._get_google_client().bucket(bucket_name)  # connect to bucket
        blob = bucket.blob(blob_name)  # create blob
        with open(data_to_upload, "rb") as file:
            blob.upload_from_file(file)

    def upload_data_to_cloud_from_dict(self, bucket_name, data_dict, blob_name):
        ''' Uploads data from a dictionary to GCP bucket. '''
        bucket = self._get_google_client().bucket(bucket_name)  # connect to bucket
        blob = bucket.blob(blob_name)  # create blob
        data_str = json.dumps(data_dict)  # convert dict to string
        blob.upload_from_string(data_str)  # upload data to blob
