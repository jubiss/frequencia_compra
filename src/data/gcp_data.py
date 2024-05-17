import json
from google.cloud import bigquery, storage
import pickle
from src.utils import utils

class gcp_operations():

    """Class used to retrieve bigquery data from GCP"""
    
    def __init__(self, gcp_project):
        self.client_bq = bigquery.Client(gcp_project)
        self.client_bucket = storage.Client(gcp_project)
        
    def bigquery_data(self, query_path=None, query=None, query_parameters=None):
        """Used to query data using a file in query_path or direct by a query using query"""
        assert query_path != None or query != None, 'Need to define a query_path or a query'
        assert query_path != None and query != None, 'Query path and query defined, only one allowed'
        if query_parameters != None:
            if type(bq_query_parameters) == list:
                bq_query_parameters = [bigquery.ScalarQueryParameter(
                    name, type_, value
                    ) for name, type_, value in query_parameters]
                bq_query_parameters = bigquery.QueryJobConfig(query_parameters=bq_query_parameters)
        if query != None:
            data = self.client_bq.query(query, job_config=bq_query_parameters).result().to_dataframe()
        elif query_path != None:
            data = self.client_bq.query(utils.read_sql_file(query_path), job_config=bq_query_parameters
                                        ).result().to_dataframe()


    def save_to_bucket(self, bucket_name, save_path, object, type_format='csv'):
        """Save files in specific gcp bucket"""
        bucket = self.client_bucket.get_bucket(bucket_name)
        assert type_format == 'csv' or type_format == 'json', "Valid type: 'csv', 'json'"
        if type_format == 'csv':
            bucket.blob(save_path).upload_from_string(object.to_csv(index=False), 'text/csv')
        elif type_format == 'json':
            print("Saving json")
            bucket.blob(save_path).upload_from_string(json.dumps(object), 'application/json')

    def load_from_bucket(self, bucket_name, file_path, type_format='json'):
        """Load files from specific gcp bucket"""
        bucket = self.client_bucket.get_bucket(bucket_name)
        assert type_format == 'json' or type_format == 'pkl', "Valid types: 'json', 'pkl'"
        if type_format == 'json':
            object = json.loads(bucket.blob(file_path).download_as_string(client=None))
        elif type_format == 'pkl':
            blob_ = bucket.blob(file_path)
            with blob_.open('rb') as f:
                object = pickle.load(f)
        return object